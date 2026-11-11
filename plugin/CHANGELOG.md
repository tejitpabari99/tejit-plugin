# Changelog

Newest first. Each release: add a `## <version> (<date>)` section, bump `plugin/.claude-plugin/plugin.json` and `plugin/gemini-extension.json`, and bump `metadata.version` in each changed skill. Patch: wording and fixes. Minor: new or changed behavior, new skill. Major: breaking change.

## 0.2.0 (2026-11-11)
- `dev-setup`: new `continue` prompt hook in `references/agent-setup.md` section c; it injects the handoff file when the prompt is `continue`, including from another worktree. Optional helper `scripts/continue-context.sh`.
- Test `tests/test_continue_context.sh`, run in CI.

## 0.1.0 (2026-11-06)
- First release.
- Skills: `start`, `dev-docs`, `brainstorm`, `dev-design`, `dev-tasks`, `dev-code`, `dev-review`, `dev-security-review`, `dev-critique`, `dev-ship`, `dev-bug`, `dev-cleanup`, `dev-setup`, `deep-research`, `index-drive-folders`, `answer-from-drive-indexes`.
- Shared files: `_shared/dev-common.md`, `_shared/update-check.md`.
- Rules file `dev-setup/references/rules.md`, installed by `dev-setup`; root `AGENTS.md` points to it.
- `dev-setup/references/agent-setup.md` tells the installing agent to set up a session-start handoff pointer and a `next` command; optional helper `dev-setup/scripts/handoff-pointer.sh`.
- CI scrub also rejects other skill packs, task trackers and `code-review`.
