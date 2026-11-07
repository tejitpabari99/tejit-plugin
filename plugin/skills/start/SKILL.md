---
name: start
description: Front door of the tejit-plugin developer skills. Use when someone says "get started", "set up tejit-plugin", "what skills are there", "what can you do", or opens the plugin without naming a skill. Connects GitHub (required), lists the skills and explains how the dev flow fits together.
metadata:
  version: "0.1.0"
---

# Start

Short, technical answers. One question at a time.

## Steps
1. **Update check.** Follow `../_shared/update-check.md`. Silent unless an update exists.
2. **Connect GitHub (required).** Follow `references/github-connect.md`. Setup is not finished until GitHub is connected. Do not continue to step 3 until it is.
3. **Star the repo.** Follow the star step in `references/github-connect.md`.
4. **List the skills** (name and one line each):
   - `dev-docs`: write and keep project docs.
   - `brainstorm`: interview an idea into a decided design.
   - `dev-design`: split a design into sub-project PRDs.
   - `dev-tasks`: PRDs into TASKS.md.
   - `dev-code`: implement tasks via sub-agents, one commit per task.
   - `dev-review`: 3-persona review of a diff.
   - `dev-security-review`: deep security audit of a diff.
   - `dev-critique`: optional second opinion on a plan or work, only when you ask.
   - `dev-ship`: run all tests, push, open or update the PR, watch CI.
   - `dev-bug`: reproduce, explain and fix a bug with a regression test.
   - `dev-cleanup`: remove merged worktrees and branches, sync main.
   - `dev-setup`: install the plugin rules and ignore entries; rerun any time.
   - `deep-research`: multi-source research with a cited report.
   - `index-drive-folders`: create and refresh `index.md` files in a Drive folder tree.
   - `answer-from-drive-indexes`: answer questions from a Drive folder using its indexes.
5. **Explain the dev flow.** `brainstorm` -> `dev-design` -> `dev-tasks` -> `dev-code` -> `dev-review` -> `dev-ship`. `dev-bug` is a side entry into `dev-code`. `dev-critique` is optional and runs only when asked. `dev-security-review` runs on security-sensitive diffs. Say `auto` at any time to run all remaining stages without stopping. `dev-docs` applies to every change. Files go in `docs/agent_files/<branch>-<timestamp>/`.
6. **Install the rules.** Hand off to `dev-setup`. It writes the plugin rules into the global instructions file of each tool found. The skills assume those rules.
7. Ask which skill to use first, and hand off.
