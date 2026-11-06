# Install

Install and update, tool by tool.

**Audience:** developers.

Marketplace: `tejitpabari99/tejit-plugin`. Plugin: `tejit-plugin`.

## Tested
- Claude Code and GitHub Copilot CLI: installs worked for a sibling plugin with the same layout. Not run against this plugin.
- Gemini CLI: `gemini extensions validate plugin` passes. Local install not tested.
- Untested: Claude app, ChatGPT, Codex, VS Code. Steps come from vendor docs and may change.

## Claude app
1. Customize, Plugins, Add, Add marketplace.
2. Paste `tejitpabari99/tejit-plugin`, confirm, Install.
3. Turn on Sync automatically.

## Claude Code
```
/plugin install tejit-plugin --marketplace tejitpabari99/tejit-plugin
```
Older versions:
```
/plugin marketplace add tejitpabari99/tejit-plugin
/plugin install tejit-plugin@tejit-plugin
```
Auto-update: `/plugin`, Marketplaces, `tejit-plugin`, Enable auto-update.

## ChatGPT Business or Enterprise
Admin, Plugins, import the GitHub repo `tejitpabari99/tejit-plugin`. Syncs daily.

## Codex
```
codex plugin marketplace add tejitpabari99/tejit-plugin
```

## GitHub Copilot CLI
```
copilot plugin marketplace add tejitpabari99/tejit-plugin
copilot plugin install tejit-plugin@tejit-plugin
```
Update: `copilot plugin update tejit-plugin`. VS Code: Add Marketplace in Agent Customizations.

## Gemini CLI
Needs a clone and a local install from `plugin/`:
```
git clone https://github.com/tejitpabari99/tejit-plugin
gemini extensions install ./tejit-plugin/plugin
```
No `--auto-update` for local folders. Update: `git pull`, then `gemini extensions update tejit-plugin`.

## Other tools
Build a ZIP ([releasing.md](releasing.md)) and upload it.

## After install
Run `start`. A GitHub connection is required; setup is not finished without it. Then add [AGENTS.md](../AGENTS.md) to your own instructions file.

## Updating
Auto-update or sync delivers new versions. Skills also check the repo for a newer version and print the update command.
