# tejit-plugin

Shareable developer skills for AI coding tools: a dev workflow (brainstorm, design, tasks, code, review, docs), deep research, and Google Drive index skills.

**Audience:** developers.

## Skills

| Skill | Use for |
|---|---|
| `start` | Setup: connect GitHub (required), list skills |
| `brainstorm` | Turn a fuzzy idea into a decided design |
| `dev-design` | Split a design into sub-project PRDs |
| `dev-tasks` | PRDs into TASKS.md |
| `dev-code` | Implement tasks via sub-agents, one commit per task; all coding goes through it |
| `dev-review` | 3-persona review of a diff |
| `dev-security-review` | Deep security audit of a diff |
| `dev-critique` | Optional second opinion on plans or work, only on request |
| `dev-ship` | Run all tests, push, open or update the PR, watch CI |
| `dev-bug` | Reproduce, explain and fix a bug with a regression test |
| `dev-cleanup` | Remove merged worktrees and branches, sync main |
| `dev-setup` | Install the plugin rules and ignore entries; rerun any time |
| `dev-docs` | Write and keep project docs |
| `deep-research` | Multi-source research with a cited report |
| `index-drive-folders` | Create and refresh `index.md` files in a Drive folder tree |
| `answer-from-drive-indexes` | Answer questions from a Drive folder using its indexes |

Flow: `brainstorm` -> `dev-design` -> `dev-tasks` -> `dev-code` -> `dev-review` -> `dev-ship`. `dev-bug` is a side entry into `dev-code`; `dev-critique` is optional. Say `auto` to run all remaining stages without stopping.

## Install

See [docs/install.md](docs/install.md). Then run the `start` skill. It requires a GitHub connection.

## Rules

Run the `dev-setup` skill. It writes the rules ([rules.md](plugin/skills/dev-setup/references/rules.md)) into the global instructions file of each tool it finds. Rerun it any time to refresh them. The skills assume those rules.

## Docs

[docs/](docs/README.md). License: MIT.
