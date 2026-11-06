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
   - `dev-critique`: independent second opinion on a plan or work in progress.
   - `deep-research`: multi-source research with a cited report.
   - `index-drive-folders`: create and refresh `index.md` files in a Drive folder tree.
   - `answer-from-drive-indexes`: answer questions from a Drive folder using its indexes.
5. **Explain the dev flow.** `brainstorm` -> `dev-design` -> `dev-tasks` -> `dev-code` -> `dev-review`. `dev-critique` can run at any stage. `dev-security-review` runs on security-sensitive diffs. `dev-docs` applies to every change. Files go in `docs/agent_files/<branch>-<timestamp>/`.
6. **Install the rules.** Tell the person to add the contents of the plugin repo's `AGENTS.md` (`https://github.com/tejitpabari99/tejit-plugin/blob/main/AGENTS.md`) to their own `AGENTS.md`, or their tool's equivalent instructions file. The skills assume those rules.
7. Ask which skill to use first, and hand off.
