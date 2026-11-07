#!/usr/bin/env bash
# Optional helper. Prints the absolute path of the newest handoff file
# (_next-context_.md), or nothing. Always exits 0.
# Search order: current worktree docs/agent_files/*/ first, then the newest across
# all worktrees of this repo.

git rev-parse --show-toplevel >/dev/null 2>&1 || exit 0
top=$(git rev-parse --show-toplevel)

found=$(ls -t "$top"/docs/agent_files/*/_next-context_.md 2>/dev/null | head -n 1)

if [ -z "$found" ]; then
  while IFS= read -r wt; do
    [ -n "$wt" ] || continue
    for f in "$wt"/docs/agent_files/*/_next-context_.md; do
      [ -f "$f" ] || continue
      if [ -z "$found" ] || [ "$f" -nt "$found" ]; then found=$f; fi
    done
  done < <(git worktree list --porcelain 2>/dev/null | sed -n 's/^worktree //p')
fi

[ -n "$found" ] && printf '%s\n' "$found"
exit 0
