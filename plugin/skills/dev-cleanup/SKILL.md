---
name: dev-cleanup
description: Use to tidy a repo. Triggers include "cleanup", "clean up", "update", "tidy worktrees", "sync main". Updates the default branch and removes worktrees and local branches that are fully merged. Asks no questions and only makes safe deletions.
metadata:
  version: "0.1.0"
---

# dev-cleanup — Sync Main, Remove Merged Work

Before anything else, follow `../_shared/update-check.md`.

No questions. Safe deletions only. Never delete remote branches, never touch dirty
worktrees or unmerged branches.

## Merged means

Either of:
- the branch tip is an ancestor of `origin/<default-branch>`
  (`git merge-base --is-ancestor <branch> origin/<default-branch>`) and is not equal to it
  (a brand-new branch sitting at the default tip is fresh work, not merged), or
- a merged GitHub PR has a head SHA equal to the branch tip. This covers squash merges:
  `gh pr list --state merged --head <branch> --json headRefOid`.

A branch that was never pushed (no upstream and no merged PR) is kept and reported.

## Steps

1. Go to the primary checkout (the first entry of `git worktree list`).
2. `git fetch origin --prune`.
3. Update the default branch:
   - Primary checkout clean and on it: `git pull --ff-only`.
   - Not checked out there: `git fetch origin <default>:<default>`.
   - Otherwise (dirty, or on another branch with a conflict): leave it and report.
4. `git worktree prune`.
5. For each linked worktree except the one this session started in (keep it, report as
   kept): remove it (`git worktree remove <path>`) only if it is clean, its tip is on its
   upstream or matches a merged PR SHA, and its branch is merged.
6. For each local non-default branch: `git branch -d <branch>` if merged. If it is merged
   only by the PR SHA match (so `-d` refuses), `git branch -D <branch>` is allowed, because
   the SHA match verified it. Never force otherwise.
7. Report: removed, kept with the reason for each, and `main at <sha>`.
