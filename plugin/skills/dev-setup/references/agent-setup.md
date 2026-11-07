# Agent setup

For the agent that is installing this plugin. Set up the two items below in whatever way
your tool supports. Then tell the user what you did and what your tool could not do. If
your tool has neither session-start hooks nor user-invoked commands, say so. The
`continue` rule in the rules file still works without them.

## a. Session-start handoff pointer

Why: after a context clear or a new session, the agent should know that saved work exists,
without loading it.

At session start and after a context clear:
1. Find `_next-context_.md`: first `docs/agent_files/*/_next-context_.md` in the current
   worktree, then the newest one across `git worktree list --porcelain`.
2. If found, tell the agent: "A handoff file exists at <path>. Read it only if the user
   says continue." Pass this pointer, never the file contents.
3. If there is no file, or the directory is not a git repo, print nothing.

An optional helper, `scripts/handoff-pointer.sh`, prints the found path or nothing. Wrap
it in whatever format your tool needs.

## b. `next` command

Why: lets the user save their place on demand, before clearing.

A user-invoked command, never triggered automatically:
1. Find the handoff file with the same search as above.
2. If it is missing, or this conversation holds newer state, write or refresh your own
   section, following the Handoff section of the rules.
3. Print the resume line in a code block: `read <absolute path> and continue`.
