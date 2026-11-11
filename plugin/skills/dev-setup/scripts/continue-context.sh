#!/usr/bin/env bash
# Optional helper for the `continue` prompt hook. Always exits 0.
# Input: the user's prompt as $1, else on stdin. A tool wrapper that receives JSON
# should extract the prompt text and pass it here.
# Output (plain text, no tool-specific format):
#   - prompt is not `continue`: nothing.
#   - `continue` and a handoff file exists: one line telling the agent to read the
#     handoff file at its absolute path now. The file contents are never printed.
#   - `continue` and no handoff file: a message telling the agent to ask the user.
# The handoff file is found by handoff-pointer.sh in this same folder.

if [ "$#" -ge 1 ]; then prompt=$1; else prompt=$(cat 2>/dev/null); fi

# Trim and lowercase.
prompt=$(printf '%s' "$prompt" | tr '[:upper:]' '[:lower:]')
prompt="${prompt#"${prompt%%[![:space:]]*}"}"
prompt="${prompt%"${prompt##*[![:space:]]}"}"

# Trigger: exactly `continue`, or `continue` followed by a non-word character.
[[ "$prompt" =~ ^continue([^[:alnum:]_]|$) ]] || exit 0

found=$(bash "$(dirname "$0")/handoff-pointer.sh" 2>/dev/null)

if [ -n "$found" ] && { [ -L "$found" ] || [ ! -f "$found" ]; }; then
  printf 'The user said continue, but the handoff file at %s is a symlink or not a regular file, so it was not loaded. Tell the user.\n' "$found"
  exit 0
fi

if [ -n "$found" ] && git -C "$(dirname "$found")" ls-files --error-unmatch "$found" >/dev/null 2>&1; then
  printf 'The user said continue, but the handoff file at %s is tracked by git (handoff files must be git-ignored), so it was not loaded. Tell the user.\n' "$found"
  exit 0
fi

if [ -z "$found" ] || [ ! -r "$found" ]; then
  where=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
  printf 'The user said continue, but no _next-context_.md was found in %s. Tell the user and ask which project/branch to resume; do not guess.\n' "$where"
  exit 0
fi

printf 'The user said continue. Read the handoff file %s now, before anything else, and resume from it.\n' "$found"
exit 0
