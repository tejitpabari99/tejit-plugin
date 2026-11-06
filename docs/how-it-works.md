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
├── AGENTS.md                         rules for users to adopt
└── LICENSE, README.md
```

The marketplace file stays at the repo root. The manifest lives in `plugin/.claude-plugin/`. All tools read the same `plugin/skills/`.

## Skills
Each skill is a folder with `SKILL.md` (frontmatter: `name` equals the folder, `description`, `metadata.version`) plus prompt templates and references. Skills share `skills/_shared/`: `dev-common.md` (dispatch, commit, branch and output conventions) and `update-check.md`. They reference it as `../_shared/...`.

## Updates
- Installed copies update when the marketplace syncs and `version` in `plugin.json` is higher.
- Each skill runs `_shared/update-check.md`: compares its `metadata.version` with `plugin.json` on `main`, and prints the update command if newer.
- A plugin cannot replace its own files. The user updates.

## Scrub
CI fails if skills or `AGENTS.md` mention platform names, personal names, local paths or Drive IDs. Skills must work in any AI tool.
