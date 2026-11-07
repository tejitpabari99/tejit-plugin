# How it works

Repo layout and how updates work.

**Audience:** developers.

```
tejit-plugin/
├── .claude-plugin/marketplace.json   marketplace file; source ./plugin
├── plugin/
│   ├── .claude-plugin/plugin.json    plugin manifest
│   ├── gemini-extension.json         Gemini CLI manifest (must match)
│   ├── skills/                       one folder per skill, plus _shared/
│   └── CHANGELOG.md
├── docs/                             these docs
├── scripts/build_zip.py              upload ZIP builder
├── .github/                          CI: validate.yml, validate_plugin.py
├── AGENTS.md                         pointer to the rules
└── LICENSE, README.md
```

The marketplace file stays at the repo root. The manifest lives in `plugin/.claude-plugin/`. All tools read the same `plugin/skills/`.

## Skills
Each skill is a folder with `SKILL.md` (frontmatter: `name` equals the folder, `description`, `metadata.version`) plus prompt templates and references. Skills share `skills/_shared/`: `dev-common.md` (dispatch, commit, branch and output conventions) and `update-check.md`. They reference it as `../_shared/...`.

## Rules
The rules live in `plugin/skills/dev-setup/references/rules.md`. `dev-setup` writes them into the global instructions file of each tool, between `<!-- tejit-plugin:start -->` and `<!-- tejit-plugin:end -->`. Rerun `dev-setup` to refresh the block; text outside the markers is never touched. The root `AGENTS.md` only points there.

## Handoff pointer and `next`
The plugin ships no tool-specific hook or command files. `dev-setup` runs `references/agent-setup.md`, which tells the installing agent to set up, in whatever way its tool supports, a session-start pointer to the `_next-context_.md` handoff file and a user-invoked `next` command. `scripts/handoff-pointer.sh` is an optional helper that prints the file path. Without them, `continue` still works: the rules say to look under `docs/agent_files/*/`.

## Updates
- Installed copies update when the marketplace syncs and `version` in `plugin.json` is higher.
- Each skill runs `_shared/update-check.md`: compares its `metadata.version` with `plugin.json` on `main`, and prints the update command if newer.
- A plugin cannot replace its own files. The user updates.

## Scrub
CI fails if skills or `AGENTS.md` mention platform names, personal names, local paths or Drive IDs, or the names of other skill packs, task trackers or `code-review`. One exception exists: `dev-setup` names the instruction file paths. Skills must work in any AI tool.
