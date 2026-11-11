# Agent setup

For the agent that is installing this plugin. Set up the three items below in whatever way
your tool supports. Then tell the user what you did and what your tool could not do. If
your tool has neither session-start hooks nor user-invoked commands, say so. The
`continue` rule in the rules file still works without them.

If already set up, update in place; do not add a second copy. Copy the helper script into
the tool's own config folder and point to that copy, not to the plugin install path, which
can change on update.

## a. Session-start handoff pointer

Why: after a context clear or a new session, the agent should know that saved work exists,
without loading it.

At session start and after a context clear:
1. Find `_next-context_.md`: first `docs/agent_files/*/_next-context_.md` in the current
   worktree, then the newest one across `git worktree list --porcelain`.
2. If found, tell the agent: "A handoff file exists at <path>. Read it only if the user
   says continue." Pass this pointer, never the file contents (the only exception is section c, on an explicit `continue`).
3. If there is no file, or the directory is not a git repo, print nothing.

An optional helper, `scripts/handoff-pointer.sh`, prints the found path or nothing. Wrap
it in whatever format your tool needs.

## b. `next` command

Why: lets the user save their place on demand, before clearing.

A user-invoked command, never triggered automatically:
1. Find the handoff file with the same search as above.
2. If it is missing, or this conversation holds newer state, write or refresh your own
   section, following the Handoff bullet of the rules.
3. Print the resume line in a code block: `read <absolute path> and continue`.

## c. `continue` prompt hook

Why: the `continue` rule is only text, and an agent can skip it. When the user's prompt is
`continue`, the agent should be handed the handoff file for certain, even if the file lives
in another worktree. This is the one hook that passes file contents, and only on an explicit
`continue`, so it does not conflict with section a.

On each user prompt, before the agent sees it:
1. Do nothing unless the trimmed prompt is `continue` (any case) or starts with `continue`
   followed by whitespace or punctuation (`Continue.`, `continue with X`). `continued`,
   `continues` and a mid-sentence `continue` do not count.
2. Find `_next-context_.md` with the search from section a and add its contents (first
   20000 bytes; if cut, say so and tell the agent to read the full file) to the agent's
   context, with the path.
3. If there is no file, or the directory is not a git repo, add a note instead: no handoff
   was found; tell the user and ask which project or branch to resume, do not guess.

An optional helper, `scripts/continue-context.sh`, does steps 1 to 3 and prints plain text
or nothing. It takes the prompt as its first argument, else on stdin, and calls
`handoff-pointer.sh` from its own folder, so copy both scripts into the same folder.

Claude Code wiring: copy both scripts to `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/hooks/` and add
this `UserPromptSubmit` hook command. It reads the prompt from the hook's JSON on stdin and
emits `additionalContext` only when the helper printed something:
```
p=$(python3 -c 'import sys,json;print(json.load(sys.stdin).get("prompt",""))'); o=$(bash "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/hooks/continue-context.sh" "$p"); [ -n "$o" ] && python3 -c 'import sys,json;print(json.dumps({"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":sys.argv[1]}}))' "$o"; exit 0
```
