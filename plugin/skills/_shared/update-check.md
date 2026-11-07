# Update check

Run once per session, before the skill's own steps. Keep it silent unless an update exists.

1. Read this skill's `metadata.version` (frontmatter of its `SKILL.md`).
2. Fetch `https://raw.githubusercontent.com/tejitpabari99/tejit-plugin/main/plugin/.claude-plugin/plugin.json` and read `version`. If it cannot be fetched or parsed, skip quietly.
3. Compare as semver.
   - Remote is newer: say so once, give the update command for the user's tool (below), then continue with the installed version.
   - Same or older: say nothing.

A plugin cannot replace its own files. Never claim you updated it.

## Update commands
- Claude Code: `/plugin marketplace update tejit-plugin`, or enable auto-update for the marketplace.
- Claude app: update from the plugin's page in the plugins list.
- GitHub Copilot CLI: `copilot plugin update tejit-plugin`
- Gemini CLI: `git pull` in your clone, then `gemini extensions update tejit-plugin`
- Codex: update the marketplace per your Codex plugin docs (untested).
- ZIP install: get the newest source from `https://github.com/tejitpabari99/tejit-plugin`, build a ZIP with `python3 scripts/build_zip.py`, then upload it again.
- Other tools: use the tool's plugin update option.
