#!/usr/bin/env python3
"""Validate the plugin repo. Stdlib only. Usage: validate_plugin.py [--base <git-ref>]"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "plugin"
PJ_REL = "plugin/.claude-plugin/plugin.json"
OLD_PJ_REL = ".claude-plugin/plugin.json"  # location before the move into plugin/
REPO_URL = "https://github.com/tejitpabari99/tejit-plugin"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
errors = []


def err(msg):
    errors.append(msg)


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        err(f"{path.relative_to(ROOT)}: invalid or unreadable JSON: {e}")
        return None


def semver_tuple(v):
    m = SEMVER.match(v or "")
    return tuple(int(x) for x in m.groups()[:3]) if m else None


def frontmatter(text):
    """Return (name, description, metadata_version) from simple YAML frontmatter."""
    m = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return None
    block = m.group(1)
    name = re.search(r"^name:\s*(.+?)\s*$", block, re.M)
    desc = re.search(r"^description:\s*(.+?)\s*$", block, re.M)
    meta = re.search(r"^metadata:\s*\n((?:[ \t]+.*\n?)+)", block + "\n", re.M)
    ver = None
    if meta:
        v = re.search(r"^[ \t]+version:\s*['\"]?([^'\"\s]+)['\"]?\s*$", meta.group(1), re.M)
        ver = v.group(1) if v else None
    return (name.group(1).strip("'\"") if name else None,
            desc.group(1) if desc else None, ver)


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def check_json_and_names():
    mp_path = ROOT / ".claude-plugin" / "marketplace.json"
    pj_path = PLUGIN / ".claude-plugin" / "plugin.json"
    mp, pj = load_json(mp_path), load_json(pj_path)
    if not (mp and pj):
        return None
    if "version" in mp:
        err("marketplace.json must not have a top-level 'version'")
    for i, p in enumerate(mp.get("plugins", [])):
        if "version" in p:
            err(f"marketplace.json plugins[{i}] must not have 'version'")
    names = [p.get("name") for p in mp.get("plugins", [])]
    if pj.get("name") not in names:
        err(f"marketplace plugin entry name {names} != plugin.json name {pj.get('name')!r}")
    for key in ("repository", "homepage"):
        if pj.get(key) != REPO_URL:
            err(f"plugin.json {key} is {pj.get(key)!r}, expected {REPO_URL!r}")
    ver = pj.get("version")
    if not semver_tuple(ver):
        err(f"plugin.json version {ver!r} is not valid semver")
    else:
        cl = PLUGIN / "CHANGELOG.md"
        if not cl.exists() or not re.search(r"^## " + re.escape(ver) + r" \(", cl.read_text(encoding="utf-8"), re.M):
            err(f"CHANGELOG.md has no '## {ver} (' section")
    return pj


def skill_dirs():
    return sorted(p.parent for p in (PLUGIN / "skills").glob("*/SKILL.md"))


def check_skills():
    for d in skill_dirs():
        fm = frontmatter((d / "SKILL.md").read_text(encoding="utf-8"))
        rel = f"plugin/skills/{d.name}/SKILL.md"
        if not fm:
            err(f"{rel}: missing frontmatter")
            continue
        name, desc, ver = fm
        if not name:
            err(f"{rel}: frontmatter missing name")
        elif name != d.name:
            err(f"{rel}: name {name!r} does not match folder {d.name!r}")
        if not desc:
            err(f"{rel}: frontmatter missing description")
        if not ver:
            err(f"{rel}: frontmatter missing metadata.version")
        elif not semver_tuple(ver):
            err(f"{rel}: metadata.version {ver!r} is not valid semver")


def check_references():
    pat = re.compile(r"`((?:prompts/|templates/|references/|scripts/|\.\./)[^`\s]*)`")
    for f in sorted((PLUGIN / "skills").rglob("*.md")):
        parts = f.relative_to(PLUGIN / "skills").parts
        skill_root = PLUGIN / "skills" / parts[0]
        for m in pat.finditer(f.read_text(encoding="utf-8")):
            ref = m.group(1)
            if any(c in ref for c in "<>*{}"):
                continue
            if not ((skill_root / ref).exists() or (f.parent / ref).exists()):
                err(f"{f.relative_to(ROOT)}: broken reference `{ref}`")


def check_release_files(pj):
    """License and Gemini manifest."""
    if pj.get("license") != "MIT":
        err(f"plugin.json license is {pj.get('license')!r}, expected 'MIT'")
    if not (ROOT / "LICENSE").is_file():
        err("LICENSE file is missing")
    gp = PLUGIN / "gemini-extension.json"
    if not gp.is_file():
        err("plugin/gemini-extension.json is missing")
    else:
        g = load_json(gp)
        if g is not None:
            for key in ("name", "version", "description"):
                if g.get(key) != pj.get(key):
                    err(f"plugin/gemini-extension.json {key} {g.get(key)!r} != plugin.json {pj.get(key)!r}")


def check_scrub():
    """Skills and AGENTS.md must be platform-neutral and free of personal data."""
    bad = re.compile(r"claude|anthropic|\bsonnet\b|\bopus\b|\bhaiku\b|pabari|columbia|/root/|washu|granola|cc-gateway"
                     r"|superpowers|gstack|TaskCreate|TodoWrite|dev-agent|code-review", re.I)
    tejit = re.compile(r"tejit", re.I)
    ok_tejit = re.compile(r"tejitpabari99/tejit-plugin|tejit-plugin", re.I)
    drive_id = re.compile(r"\b1[A-Za-z0-9_-]{32}\b")
    # Tool names are unavoidable in the install/update instructions of these files.
    tool_names_ok = {PLUGIN / "skills/_shared/update-check.md"}
    files = [p for p in (PLUGIN / "skills").rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    files.append(ROOT / "AGENTS.md")
    # Narrow, exact exceptions: strings removed from a line before scanning, per file.
    exact_ok = {
        # dev-setup names the instruction files of each supported tool.
        PLUGIN / "skills/dev-setup/SKILL.md": ["Claude Code", "~/.claude/CLAUDE.md"],
    }
    for f in sorted(files):
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:  # noqa: BLE001
            continue
        rel = f.relative_to(ROOT)
        text = text.replace(".claude-plugin", "")
        for allowed in exact_ok.get(f, []):
            text = text.replace(allowed, "")
        for lineno, line in enumerate(text.splitlines(), 1):
            rest = ok_tejit.sub("", line)  # the repo URL and plugin name are allowed
            for m in bad.finditer(rest):
                if m.group(0).lower() == "claude" and f in tool_names_ok:
                    continue
                err(f"{rel}:{lineno}: scrub: found {m.group(0)!r}")
            if tejit.search(rest):
                err(f"{rel}:{lineno}: scrub: 'tejit' outside tejitpabari99/tejit-plugin or tejit-plugin")
            if drive_id.search(line):
                err(f"{rel}:{lineno}: scrub: Drive-ID-like token")


def check_links():
    link = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)\)|!\[[^\]]*\]\(([^)\s]+)\)|src=\"([^\"]+)\"")
    files = [ROOT / "README.md"] + sorted((ROOT / "docs").rglob("*.md"))
    for f in files:
        text = re.sub(r"```.*?```", "", f.read_text(encoding="utf-8"), flags=re.S)
        for m in link.finditer(text):
            target = next(g for g in m.groups() if g)
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            path = target.split("#")[0]
            if path and not (f.parent / path).exists():
                err(f"{f.relative_to(ROOT)}: broken link {target}")


def check_base(base, pj):
    if git("rev-parse", "--verify", base).returncode != 0:
        err(f"--base ref {base!r} not found")
        return
    # Base may predate the move into plugin/: fall back to the old layout.
    prefix = "plugin/"
    show = git("show", f"{base}:{PJ_REL}")
    if show.returncode != 0:
        prefix = ""
        show = git("show", f"{base}:{OLD_PJ_REL}")
    if show.returncode != 0:
        print(f"base {base} has no plugin.json: skipping version-bump checks")
        return
    watched = ["plugin/skills/", PJ_REL, "plugin/gemini-extension.json"]
    if not prefix:
        watched += ["skills/", OLD_PJ_REL]
    diff = git("diff", "--name-only", f"{base}...HEAD", "--", *watched)
    changed = [l for l in diff.stdout.splitlines() if l]
    if not changed:
        print("no plugin files changed versus base: skipping version-bump checks")
        return
    try:
        base_ver = json.loads(show.stdout).get("version")
    except Exception as e:  # noqa: BLE001
        err(f"base plugin.json invalid JSON: {e}")
        return
    new, old = semver_tuple(pj.get("version")), semver_tuple(base_ver)
    if new and old and not new > old:
        err(f"plugin version {pj.get('version')} must be higher than base {base_ver} (changed: {', '.join(changed[:5])})")
    for name in sorted({c.split("/")[1] for c in changed if c.startswith("skills/") and c.count("/") >= 2}
                       | {c.split("/")[2] for c in changed if c.startswith("plugin/skills/") and c.count("/") >= 3}):
        cur_p = PLUGIN / "skills" / name / "SKILL.md"
        cur = frontmatter(cur_p.read_text(encoding="utf-8"))[2] if cur_p.exists() else None
        b = git("show", f"{base}:{prefix}skills/{name}/SKILL.md")
        if b.returncode != 0:
            continue  # new skill
        bfm = frontmatter(b.stdout)
        bver = bfm[2] if bfm else None
        if not cur:
            continue  # reported by check_skills
        if semver_tuple(cur) and semver_tuple(bver) and not semver_tuple(cur) > semver_tuple(bver):
            err(f"plugin/skills/{name} changed but metadata.version {cur} is not higher than base {bver}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base")
    a = ap.parse_args()
    pj = check_json_and_names()
    check_skills()
    check_references()
    if pj:
        check_release_files(pj)
    check_scrub()
    check_links()
    if a.base and pj:
        check_base(a.base, pj)
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("OK: all checks passed")


if __name__ == "__main__":
    main()
