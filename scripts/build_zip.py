#!/usr/bin/env python3
"""Build an upload ZIP of the plugin. Python 3 standard library only.

  python3 scripts/build_zip.py                  -> dist/tejit-plugin-<version>.zip
  python3 scripts/build_zip.py --skill <name>   -> dist/<name>-<version>.zip (one skill, SKILL.md at the root)
"""
import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugin"
ROOT_FILES = ["LICENSE", "README.md"]  # repo-level files added to the ZIP root
SKIP_DIRS = {"__pycache__"}
SKIP_FILES = {".DS_Store"}


def files_under(path):
    """Yield files in path (or path itself if a file), skipping junk, in stable order."""
    if path.is_file():
        if path.name not in SKIP_FILES:
            yield path
        return
    for p in sorted(path.rglob("*")):
        if p.is_file() and p.name not in SKIP_FILES and not (set(p.relative_to(path).parts) & SKIP_DIRS):
            yield p


def write_zip(out, items):
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for src, arc in items:
            z.write(src, arc.as_posix())
    print(f"Wrote {out.relative_to(ROOT)} ({len(items)} files)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skill", help="build a ZIP of a single skill (SKILL.md at the ZIP root)")
    args = ap.parse_args()

    version = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]

    if args.skill:
        sdir = PLUGIN / "skills" / args.skill
        if not (sdir / "SKILL.md").is_file():
            sys.exit(f"No such skill: plugin/skills/{args.skill}/SKILL.md not found")
        items = [(f, f.relative_to(sdir)) for f in files_under(sdir)]
        shared = PLUGIN / "skills" / "_shared"
        if shared.is_dir():  # skills reference ../_shared/; ship it next to SKILL.md
            items += [(f, Path("_shared") / f.relative_to(shared)) for f in files_under(shared)]
        for f, arc in items:
            if f.suffix == ".md" and re.search(r"\.\./", f.read_text(encoding="utf-8", errors="ignore")):
                print(f"WARNING: {arc.as_posix()} refers to files outside the skill folder with '../'. "
                      "Those files are not in this ZIP.")
        write_zip(ROOT / "dist" / f"{args.skill}-{version}.zip", items)
        return

    items = []
    items += [(f, f.relative_to(PLUGIN)) for f in files_under(PLUGIN)]
    for name in ROOT_FILES:
        p = ROOT / name
        if not p.is_file():
            sys.exit(f"Missing required path: {name}")
        items.append((p, Path(name)))
    write_zip(ROOT / "dist" / f"tejit-plugin-{version}.zip", items)


if __name__ == "__main__":
    main()
