---
name: handoff
description: Use to save your place before clearing context or ending a session. User-invoked via /handoff. Writes or refreshes the handoff file from this conversation and prints the resume line.
disable-model-invocation: true
metadata:
  version: "0.1.0"
---

# handoff — Save Your Place

Before anything else, follow `../_shared/update-check.md`.

User-invoked only. Produces a resume line so work can continue in fresh context.

1. **Find** `_next-context_.md`: first `docs/agent_files/*/_next-context_.md` in the
   current worktree (newest), then the newest across all worktrees from
   `git worktree list --porcelain`. Not a git repo: say so and stop.
2. **Write or refresh.** If none exists, or this conversation holds newer state than the
   file, write or refresh only your own `## <sub-project>` section, following the Handoff
   section of `../_shared/dev-common.md` (read it; do not duplicate it here). Folder:
   `docs/agent_files/<branch-slug>-<YYYYMMDD-HHMM>/`, timestamp from
   `date +%Y%m%d-%H%M`; reuse the existing folder for this branch. Read the file first and
   keep other sections untouched. The section holds: stage, branch, worktree, PR and CI
   state, what is done, the exact next step, open decisions, PRD and TASKS paths (point to
   them, do not copy), and `Mode: auto` if on.
3. **Ignore.** Ensure `**/_next-context_.md` is in the repo's `.gitignore`.
4. **Print** the resume line in a code block, then the fresh-context line:

   ```
   read <absolute path> and continue
   ```
   or: `/clear`, then `continue`
