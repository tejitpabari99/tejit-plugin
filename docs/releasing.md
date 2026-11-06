# Releasing

Release steps, CI checks and ZIP builds.

**Audience:** maintainer.

## Steps
1. Change the plugin. Add a section to `plugin/CHANGELOG.md`.
2. Bump `version` in `plugin/.claude-plugin/plugin.json` and `plugin/gemini-extension.json` (must match), and `metadata.version` in each changed skill.
3. Run `claude plugin validate .`, `claude plugin validate plugin`, `python3 .github/scripts/validate_plugin.py`.
4. Pull request into `main`, merge.

## CI (`.github/workflows/validate.yml`)
- Plugin validates (Claude Code, Gemini CLI). JSON and skill frontmatter are well formed; `name` equals folder; `metadata.version` is semver.
- Changelog has a section for the plugin version.
- Referenced files exist. Relative links in `README.md` and `docs/` resolve.
- `gemini-extension.json` matches `plugin.json`. License is MIT and `LICENSE` exists.
- Scrub: `plugin/skills/` and `AGENTS.md` contain no platform names, personal names, local paths or Drive IDs. `tejit` is allowed only as `tejitpabari99/tejit-plugin` or `tejit-plugin`.
- On pull requests: plugin and changed-skill versions are higher than on the base.
- ZIP builds and has no `.github/` or `docs/`.

## ZIP
```
python3 scripts/build_zip.py
```
Writes `dist/tejit-plugin-<version>.zip`: `plugin/` contents plus `LICENSE` and `README.md`.

```
python3 scripts/build_zip.py --skill dev-code
```
Writes `dist/dev-code-<version>.zip` with `SKILL.md` at the root. Skills reference `../_shared/`, which sits outside a skill folder, so the script copies `_shared/` into the ZIP root and warns about the `../` references. From a root `SKILL.md`, `../_shared/` does not resolve, so the agent must be pointed at the bundled `_shared/` folder. For a portal where that does not work, upload the full ZIP instead. `dist/` is not committed.
