#!/usr/bin/env python3
"""Deterministically merge Google Drive index entries by stable Drive ID."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


HEADING_RE = re.compile(r"^### \[(?P<name>.*)\]\((?P<url>.+)\)\s*$")
ID_PATTERNS = (
    re.compile(r"/folders/([^/?#]+)"),
    re.compile(r"/d/([^/?#]+)"),
    re.compile(r"[?&]id=([^&#]+)"),
)


@dataclass(frozen=True)
class Entry:
    item_id: str
    name: str
    url: str
    description: str
    tags: tuple[str, ...]


def drive_id(url: str) -> str:
    for pattern in ID_PATTERNS:
        match = pattern.search(url)
        if match:
            return match.group(1)
    raise ValueError(f"Cannot extract a Drive ID from URL: {url}")


def normalize_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return " ".join(value.split())


def normalize_tags(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        candidates = value.split(",")
    elif isinstance(value, list):
        candidates = value
    else:
        raise ValueError("tags must be a string or a list of strings")

    seen: set[str] = set()
    tags: list[str] = []
    for candidate in candidates:
        tag = normalize_text(candidate, "tag")
        folded = tag.casefold()
        if folded not in seen:
            seen.add(folded)
            tags.append(tag)
    if not tags:
        raise ValueError("tags must contain at least one tag")
    return tuple(tags)


def entry_from_json(item: Any, require_content: bool) -> Entry:
    if not isinstance(item, dict):
        raise ValueError("Each entry must be an object")
    item_id = normalize_text(item.get("id"), "id")
    name = normalize_text(item.get("name"), "name")
    url = normalize_text(item.get("url"), "url")
    url_id = drive_id(url)
    if url_id != item_id:
        raise ValueError(f"Entry ID {item_id!r} does not match URL ID {url_id!r}")
    if require_content:
        description = normalize_text(item.get("description"), "description")
        tags = normalize_tags(item.get("tags"))
    else:
        description = ""
        tags = ()
    return Entry(item_id, name, url, description, tags)


def parse_existing(markdown: str) -> dict[str, dict[str, Entry]]:
    entries: dict[str, dict[str, Entry]] = {"folders": {}, "files": {}}
    section: str | None = None
    current: dict[str, str] | None = None

    def finish() -> None:
        nonlocal current
        if current is None or section is None:
            current = None
            return
        item_id = drive_id(current["url"])
        entry = Entry(
            item_id=item_id,
            name=unescape_name(current["name"]),
            url=current["url"],
            description=normalize_text(current.get("description"), "description"),
            tags=normalize_tags(current.get("tags")),
        )
        if item_id in entries[section]:
            raise ValueError(f"Duplicate Drive ID {item_id!r} in existing {section} section")
        entries[section][item_id] = entry
        current = None

    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if line == "## Folders":
            finish()
            section = "folders"
            continue
        if line == "## Files":
            finish()
            section = "files"
            continue
        heading = HEADING_RE.match(line)
        if heading and section is not None:
            finish()
            current = heading.groupdict()
            continue
        if current is not None and line.startswith("Description:"):
            current["description"] = line.removeprefix("Description:").strip()
        elif current is not None and line.startswith("Tags:"):
            current["tags"] = line.removeprefix("Tags:").strip()
    finish()
    return entries


def escape_name(name: str) -> str:
    return name.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")


def unescape_name(name: str) -> str:
    return name.replace("\\]", "]").replace("\\[", "[").replace("\\\\", "\\")


def render_section(title: str, entries: list[Entry]) -> list[str]:
    lines = [f"## {title}", ""]
    if not entries:
        return lines + ["None."]
    for index, entry in enumerate(sorted(entries, key=lambda item: item.name.casefold())):
        if index:
            lines.append("")
        lines.extend(
            (
                f"### [{escape_name(entry.name)}]({entry.url})",
                f"Description: {entry.description}",
                f"Tags: {', '.join(entry.tags)}",
            )
        )
    return lines


def merge(spec: Any, existing_markdown: str) -> str:
    if not isinstance(spec, dict):
        raise ValueError("Spec must be a JSON object")
    current_json = spec.get("current")
    updates_json = spec.get("updates")
    if not isinstance(current_json, dict) or not isinstance(updates_json, dict):
        raise ValueError("Spec must contain current and updates objects")

    existing = parse_existing(existing_markdown) if existing_markdown.strip() else {"folders": {}, "files": {}}
    merged: dict[str, list[Entry]] = {"folders": [], "files": []}

    for section in ("folders", "files"):
        current_section = current_json.get(section, [])
        updates_section = updates_json.get(section, [])
        if not isinstance(current_section, list) or not isinstance(updates_section, list):
            raise ValueError(f"current.{section} and updates.{section} must be lists")
        current_items = [entry_from_json(item, False) for item in current_section]
        update_items = [entry_from_json(item, True) for item in updates_section]
        updates = {entry.item_id: entry for entry in update_items}
        if len(updates) != len(update_items):
            raise ValueError(f"Duplicate IDs in updates.{section}")
        current_ids = {entry.item_id for entry in current_items}
        if len(current_ids) != len(current_items):
            raise ValueError(f"Duplicate IDs in current.{section}")
        unexpected = set(updates) - current_ids
        if unexpected:
            raise ValueError(f"updates.{section} contains IDs absent from current: {sorted(unexpected)}")

        for item in current_items:
            replacement = updates.get(item.item_id)
            if replacement is not None:
                merged[section].append(replacement)
                continue
            previous = existing[section].get(item.item_id)
            if previous is None:
                raise ValueError(
                    f"Current {section} item {item.name!r} ({item.item_id}) has no existing or updated description"
                )
            merged[section].append(
                Entry(item.item_id, item.name, item.url, previous.description, previous.tags)
            )

    last_updated = spec.get("last_updated")
    lines = ["# Index.md", ""]
    if last_updated is not None:
        lines.extend((f"Last updated: {normalize_text(last_updated, 'last_updated')}", ""))
    lines.extend(("---", ""))
    lines.extend(render_section("Folders", merged["folders"]))
    lines.extend(("", "---", ""))
    lines.extend(render_section("Files", merged["files"]))
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", default="-", help="JSON spec path, or - for stdin")
    parser.add_argument("--existing", help="Existing index.md path")
    parser.add_argument("--last-updated", help="Optional root-only checkpoint timestamp")
    parser.add_argument("--output", default="-", help="Output path, or - for stdout")
    args = parser.parse_args()

    try:
        raw_spec = sys.stdin.read() if args.spec == "-" else Path(args.spec).read_text(encoding="utf-8")
        spec = json.loads(raw_spec)
        if args.last_updated is not None:
            spec["last_updated"] = args.last_updated
        existing = Path(args.existing).read_text(encoding="utf-8") if args.existing else ""
        output = merge(spec, existing)
        if args.output == "-":
            sys.stdout.write(output)
        else:
            Path(args.output).write_text(output, encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"merge_index.py: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
