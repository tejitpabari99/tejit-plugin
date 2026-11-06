---
name: index-drive-folders
description: Create or incrementally update navigational index.md files throughout a Google Drive folder tree using one dedicated successful sub-agent per folder, one root-index checkpoint, and centralized Drive writes. Use when a user provides a Drive folder and asks to index, reindex, refresh, or update folder indexes, including requests such as "update since last week" or "update anything changed since the previous index." Read source contents, preserve unchanged entries, refresh newly created or edited items, reconcile moved or deleted items, always refresh the root index checkpoint safely, and modify only index.md files.
metadata:
  version: "0.1.0"
---

# Index Drive Folders

Before anything else, follow `../_shared/update-check.md`.

Create concise, content-grounded `index.md` files in a Google Drive folder and every nested folder. Use the connected Google Drive tools.

## Inputs

Require a Google Drive folder URL or resolvable folder ID. Accept an optional explicit timeframe such as `since last week`, `past 30 days`, or `since 2026-08-01`. Also accept an explicit `full reindex`, `rebuild all indexes`, or equivalent override.

Resolve relative time expressions against the current date, time, and timezone. Interpret `since last week` as the preceding seven days unless the user says `previous calendar week`. Interpret a date without a time as 00:00 in the user's timezone. Ask only when an expression still has materially different plausible interpretations.

## Establish one root checkpoint

Have the coordinator capture `run_started_at` in RFC3339 format, then determine the run mode before spawning folder agents:

1. List the supplied root's direct children and locate exact, non-trashed `index.md` files.
2. If the user explicitly requested a full reindex, use full-baseline mode for the entire tree.
3. If the user supplied a timeframe, resolve it once and use that global cutoff for every folder that already has an index.
4. If no timeframe was supplied and exactly one root index exists, use its single valid root-only `Last updated` timestamp as the global cutoff. For a legacy root index without that line, or with an invalid marker, use its Drive `modifiedTime` and replace the marker during this run. Apply this global cutoff to every folder that already has an index.
5. If no timeframe was supplied and the root has no index, use full-baseline mode for the entire tree.
6. If multiple root indexes exist, stop before writes and ask the user to resolve the ambiguity. Do not choose a checkpoint silently.

For any non-root folder with no existing index, perform a full baseline for that folder even during a global incremental run. A partial first index is not useful. Treat an item as changed when its Drive `createdTime >= global cutoff` or `modifiedTime >= global cutoff`.

The root index is the single incremental checkpoint. Do not substitute child-index modification times for the global cutoff. Advance the checkpoint to `run_started_at`, not to the later write time, so a source edited during the run remains eligible on the next run.

## Respect terminal collection boundaries

Some folders are deliberately indexed as terminal collections even when they contain organizational subfolders. Index the boundary folder itself, include its direct child folders in that boundary folder's `index.md`, and do not recurse into those child folders or create, update, verify, or require `index.md` files inside them.

Treat a folder as a terminal collection only when the user explicitly designates it as a leaf/boundary. Do not infer a boundary from a folder name.

For a terminal collection:

- stop recursive tree discovery after listing the boundary folder's direct children; do not add its child folders to the agent-owned folder tree;
- assign exactly one folder agent to the boundary folder itself, as usual;
- allow that agent to list metadata for the direct files inside each immediate child folder solely to produce or refresh a concise child-folder description and tags;
- do not download or inspect file contents merely to build the navigation index; use child folder names, filenames, and MIME types;
- during an incremental run, list the immediate child folder contents so a new, renamed, moved, or edited file can refresh its child folder entry even if Drive does not advance the child folder's own `modifiedTime`;
- leave any pre-existing files inside child folders untouched, including any old `index.md` files; they are outside this run's indexing scope;
- treat intentionally excluded descendants as complete, not skipped or failed, for checkpoint advancement.

If the supplied root is itself a terminal collection, it still receives the root-only `Last updated` checkpoint. If a terminal collection sits below the supplied root, its own index remains a child index and must not receive a `Last updated` line.

## Mandatory agent orchestration

Use the main agent only as the coordinator and Drive writer. Delegate the content work for every folder—including the supplied root folder—to one dedicated primary sub-agent. Require exactly one successful manifest per folder; a failed primary may be replaced by the single retry allowed below. Do not silently perform a folder's content work in the main agent.

### Phase 1: discover the tree

Have the main agent recursively list folder metadata to build the complete in-scope tree, even during incremental runs; a parent's modified time does not reliably reveal deeper changes. Record each folder's ID, observed URL, parent, and depth. Do not read or summarize source-file contents during discovery. Apply terminal collection boundaries during discovery so their direct child folders remain index entries rather than separately assigned folders.

### Phase 2: process folders bottom-up

Process the deepest depth first and the root last. Run sibling folder agents in parallel, subject to the available concurrency slots; wait and reuse slots when the tree is larger. The coordinator must spawn the folder agents itself rather than asking folder agents to spawn children, which avoids slot deadlocks and duplicate ownership.

For every folder, spawn exactly one sub-agent with:

- that folder's ID, observed URL, parent, and depth;
- the coordinator-resolved global cutoff and run mode;
- whether the folder has an existing index and therefore uses the global cutoff, or needs a full baseline;
- completed summaries and draft-change status from its direct child-folder agents;
- the required output format and write-safety rules.

Each folder agent must:

1. Own only that folder's direct inventory, content reads, merge, summary, and local draft.
2. Use only read-only Google Drive calls; never upload, update, move, rename, or delete a Drive item.
3. Apply the supplied global cutoff or full-baseline mode, read its existing index, and inspect the required direct source files.
4. Use completed child-agent summaries for folder entries instead of re-reading nested contents.
5. Save the merge spec and run `scripts/merge_index.py`, writing the result to unique local paths containing the folder ID.
6. Compare the draft with the existing index when possible and mark it `created`, `updated`, or `unchanged`; always mark the root `updated` when it already exists because its checkpoint line must advance.
7. Return a manifest containing: folder ID/URL/name/depth, existing index ID/URL/MIME type, cutoff and update mode, merge-spec path, existing-index local path, draft path, status, folder summary and tags, source files read, unreadable items, and any ambiguity or failure.

Never assign the same folder to multiple agents concurrently or accept more than one successful manifest. If a folder's primary agent fails, retry that folder once in a fresh sub-agent. If it still fails, skip its write and report it; do not replace the required folder agent with main-agent content work.

### Phase 3: write centrally

After all folder agents finish, have only the main agent perform Drive writes, bottom-up, with the root written last. Centralized writes preserve the original user authorization context and prevent duplicate indexes from concurrent uploads.

For each successful manifest:

- skip `unchanged` drafts except for the root;
- update exactly one existing index in place;
- upload a new raw Markdown index only when none exists;
- stop and report the folder when multiple indexes exist;
- verify the parent, name, MIME type, and exactly-one-index invariant after the write.

Always create or update the root index when the root itself is not ambiguous and is writable, even when no source entry changed. Immediately before the final root write, have the coordinator mechanically regenerate the root draft from the returned merge spec with `--last-updated <checkpoint>`; this is not folder-content work. Use `run_started_at` only when every required folder produced one successful manifest and every planned child-index write succeeded. If the run is incomplete, retain a safe checkpoint: use the earliest of the pre-run root checkpoint and explicit/global cutoff; for an incomplete full baseline with no safe prior checkpoint, use `1970-01-01T00:00:00Z`. Report the retained checkpoint and the incomplete folders. This prevents a failed branch from falling behind the next cutoff.

Render `Last updated: <checkpoint>` directly below `# Index.md` in the root only. Do not add this line to child indexes. The root write is the final checkpoint update; if it fails, report that the checkpoint did not change.

Never retry a write by moving or copying source files.

## Inventory and read

For each folder:

1. List every direct, non-trashed child. Exclude `index.md` itself from the Files section.
2. Capture stable Drive IDs, exact names, MIME types, `createdTime`, `modifiedTime`, parents, and observed web URLs. Use metadata reads when folder listings omit timestamps or URLs.
3. Fetch readable contents for every new or changed file, not merely its filename. Use type-specific inspection when a Google Doc, Sheet, or Slides file needs it.
4. For a new baseline, read every direct file and use the completed summaries from direct child-folder agents. For a terminal collection, instead summarize each immediate child folder from its shallow file metadata under the terminal-boundary rules above.
5. For an incremental update, preserve unchanged descriptions and tags from the existing index. Re-read new or changed files. Refresh a direct folder entry when the folder metadata changed after the global cutoff, the child index changed during the run, or its prior entry is missing.
6. If a file cannot be read, do not invent a content description. Use a clearly limited metadata-based description only when it remains useful, and report the item as unreadable in the final result.

## Reconcile the index

Read the existing `index.md` when present. Build a complete current inventory for both folders and files, plus full replacement entries for items that need updating.

If an existing index is malformed or cannot be merged safely by stable Drive ID, perform a full baseline for that folder and replace only that index's contents. Do not guess which old entry maps to which current item.

Use `scripts/merge_index.py` to merge by stable Drive ID:

```bash
python3 scripts/merge_index.py --spec updates.json --existing existing-index.md --output index.md
```

The JSON spec has this shape:

```json
{
  "current": {
    "folders": [{"id": "folder-id", "name": "Folder", "url": "observed-url"}],
    "files": [{"id": "file-id", "name": "File", "url": "observed-url"}]
  },
  "updates": {
    "folders": [{"id": "folder-id", "name": "Folder", "url": "observed-url", "description": "Concise summary.", "tags": ["tag one", "tag two"]}],
    "files": [{"id": "file-id", "name": "File", "url": "observed-url", "description": "Concise summary.", "tags": ["tag one", "tag two"]}]
  }
}
```

For the final root render only, pass `--last-updated "<safe RFC3339 checkpoint>"` or add the equivalent top-level `"last_updated"` value to its merge spec. Use `run_started_at` after a complete run and the retained safe value after an incomplete run. Omit both for every child folder.

Include every current direct child in `current`, even when unchanged. Include only new, changed, or missing entries in `updates` during an incremental run. The merge script preserves unchanged descriptions, updates names and links, removes entries no longer present, and fails rather than silently emitting an incomplete index.

## Description and tag rules

- Keep each description to one concise sentence that helps a reader choose the right item.
- Describe contents and purpose, not file-format trivia.
- Use specific comma-separated tags; prefer subject, assessment, organization, workflow, method, or artifact type.
- Base folder descriptions on inspected direct contents and completed child summaries.
- Use exact observed Drive links in headings. Never synthesize a URL.
- Sort folders and files alphabetically for stable diffs.

The output format is:

```markdown
# Index.md

Last updated: 2026-08-15T23:59:59-07:00

---

## Folders

### [Folder name](observed Drive URL)
Description: Concise description.
Tags: tag one, tag two

---

## Files

### [File name](observed Drive URL)
Description: Concise description.
Tags: tag one, tag two
```

Write `None.` beneath an empty section.

Include the `Last updated` line only in the supplied root folder's index.

## Write safety and verification

- Permit only the main coordinating agent to create or update Drive indexes; folder agents produce local drafts and manifests only.
- Modify only `index.md` files. Do not rename, move, share, delete, or edit any source item.
- Create a raw `text/markdown` file, not a native Google Doc.
- If exactly one index exists, update it in place to preserve its Drive identity and history.
- If no index exists, upload one to the exact parent folder.
- If multiple indexes already exist, stop for that folder and report the ambiguity; do not choose or delete one silently.
- After every write, read folder metadata or list the folder again and verify exactly one `index.md`, the correct parent, and MIME type `text/markdown`.
- Avoid a no-op write when the generated Markdown is byte-for-byte identical to the existing index, except that the root must always receive its fresh checkpoint line.

## Completion report

Report:

- folders scanned and indexes created, updated, or unchanged;
- terminal collections encountered and the number of descendant child folders intentionally excluded from recursive indexing;
- folder agents completed, retried, skipped, or failed; the completed-agent count must account for every scanned folder;
- source files read and unreadable items;
- effective explicit cutoff, root-index checkpoint cutoff, or full-baseline mode;
- the root `Last updated` checkpoint, whether it advanced or was retained, and why;
- links to every created or updated index;
- any folder skipped because of duplicate indexes or missing access;
- confirmation that no source file was altered.
