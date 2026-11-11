#!/usr/bin/env bash
# Optional helper for the `continue` prompt hook. Always exits 0.
# Input: the user's prompt as $1, else on stdin. A tool wrapper that receives JSON
# should extract the prompt text and pass it here.
# Output (plain text, no tool-specific format):
#   - prompt is not `continue`: nothing.
#   - `continue` and a handoff file exists: a header, then the file contents
#     (capped at 20000 bytes; if cut, says so and tells the agent to read the full file).
#   - `continue` and no handoff file: a message telling the agent to ask the user.
# The handoff file is found by handoff-pointer.sh in this same folder.

max=20000

if [ "$#" -ge 1 ]; then prompt=$1; else prompt=$(cat 2>/dev/null); fi

# Trim and lowercase.
prompt=$(printf '%s' "$prompt" | tr '[:upper:]' '[:lower:]')
prompt="${prompt#"${prompt%%[![:space:]]*}"}"
prompt="${prompt%"${prompt##*[![:space:]]}"}"

# Trigger: exactly `continue`, or `continue` followed by a non-word character.
[[ "$prompt" =~ ^continue([^[:alnum:]_]|$) ]] || exit 0

found=$(bash "$(dirname "$0")/handoff-pointer.sh" 2>/dev/null)

if [ -z "$found" ] || [ ! -r "$found" ]; then
  where=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
  printf 'The user said continue, but no _next-context_.md was found in %s. Tell the user and ask which project/branch to resume; do not guess.\n' "$where"
  exit 0
fi

printf 'The user said continue. Handoff file: %s. Its contents follow; resume from it per the rules.\n\n' "$found"
head -c "$max" "$found"
size=$(wc -c < "$found" | tr -d ' ')
if [ "$size" -gt "$max" ]; then
  printf '\n\n[truncated: showing the first %s of %s bytes. Read the full file at %s before resuming.]\n' "$max" "$size" "$found"
fi
exit 0
