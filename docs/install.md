# Install

Install and update, tool by tool.

**Audience:** developers.

Marketplace: `tejitpabari99/thepass`. Plugin: `thepass`.

## Tested
- Claude Code and GitHub Copilot CLI: installs worked for a sibling plugin with the same layout. Not run against this plugin.
- Gemini CLI: `gemini extensions validate plugin` passes. Local install not tested.
- Untested: Claude app, ChatGPT, Codex, VS Code. Steps come from vendor docs and may change.

## Claude app
1. Customize, Plugins, Add, Add marketplace.
2. Paste `tejitpabari99/thepass`, confirm, Install.
3. Turn on Sync automatically.

## Claude Code
```
/plugin install thepass --marketplace tejitpabari99/thepass
```
Older versions:
```
/plugin marketplace add tejitpabari99/thepass
/plugin install thepass@thepass
```
Auto-update: `/plugin`, Marketplaces, `thepass`, Enable auto-update.

## ChatGPT Business or Enterprise
Admin, Plugins, import the GitHub repo `tejitpabari99/thepass`. Syncs daily.

## Codex
```
codex plugin marketplace add tejitpabari99/thepass
```

## GitHub Copilot CLI
```
copilot plugin marketplace add tejitpabari99/thepass
copilot plugin install thepass@thepass
```
Update: `copilot plugin update thepass`. VS Code: Add Marketplace in Agent Customizations.

## Gemini CLI
Needs a clone and a local install from `plugin/`:
```
git clone https://github.com/tejitpabari99/thepass
gemini extensions install ./thepass/plugin
```
No `--auto-update` for local folders. Update: `git pull`, then `gemini extensions update thepass`.

## Other tools
Build a ZIP ([releasing.md](releasing.md)) and upload it.

## After install
Run `start`. A GitHub connection is required; setup is not finished without it. `start` then runs `dev-setup`, which installs the rules into your tool's global instructions file. To rerun setup later, say "run dev-setup".

## Updating
Auto-update or sync delivers new versions. Skills also check the repo for a newer version and print the update command.
