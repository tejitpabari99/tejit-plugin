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
| `dev-code` | Implement tasks via sub-agents, one commit per task |
| `dev-review` | 3-persona review of a diff |
| `dev-security-review` | Deep security audit of a diff |
| `dev-critique` | Independent second opinion on plans or work in progress |
| `dev-docs` | Write and keep project docs |
| `deep-research` | Multi-source research with a cited report |
| `index-drive-folders` | Create and refresh `index.md` files in a Drive folder tree |
| `answer-from-drive-indexes` | Answer questions from a Drive folder using its indexes |

Flow: `brainstorm` -> `dev-design` -> `dev-tasks` -> `dev-code` -> `dev-review`.

## Install

See [docs/install.md](docs/install.md). Then run the `start` skill. It requires a GitHub connection.

## Rules

Add the contents of [AGENTS.md](AGENTS.md) to your own `AGENTS.md` (project or global) or your tool's equivalent instructions file. The skills assume those rules.

## Docs

[docs/](docs/README.md). License: MIT.
