---
name: dev-setup
description: Use to install the plugin's rules into your AI tool and prepare a repo. Triggers include "set up the plugin", "dev-setup", and the end of the start skill. Idempotent, safe to rerun any time to refresh the rules.
metadata:
  version: "0.2.0"
---

# dev-setup — Install Rules, Prepare Repo

Before anything else, follow `../_shared/update-check.md`.

Idempotent. Rerun it to refresh the rules after a plugin update. Asks no questions, except
that project-level install happens only if the user asks for it.

## Steps

1. **Rules file.** The text to install is `references/rules.md`. For each tool you can
   find on this machine (the instruction file or its folder exists), write it into that
   tool's global instruction file between these markers:
   ```
   <!-- tejit-plugin:start -->
   ...contents of references/rules.md...
   <!-- tejit-plugin:end -->
   ```
   On rerun, replace the block between the markers. Never touch text outside them. If the
   file exists without markers, append the block. If only one marker is present, report it
   and do not write that file. If the tool has a config-folder environment override, use it
   in place of the default path. Global by default; use the project's
   `AGENTS.md` only if the user asks.

   | Tool | Global instruction file | Source |
   |---|---|---|
   | Claude Code | `$CLAUDE_CONFIG_DIR/CLAUDE.md`, default `~/.claude/CLAUDE.md` | vendor docs |
   | Codex | `~/.codex/AGENTS.md` | vendor docs |
   | Gemini CLI | `~/.gemini/GEMINI.md` | vendor docs |
   | GitHub Copilot CLI | `~/.copilot/copilot-instructions.md` | unverified, check before relying on it |

2. **Repo ignore entries.** If the current directory is not in a git repo, skip this step.
   Otherwise make sure `.gitignore` has `.worktrees/`
   and `**/_next-context_.md`. If one was missing and you added it: on a feature branch,
   commit it (commit convention in `../_shared/dev-common.md`); on a default branch, leave it
   unstaged and tell the user.
3. **Agent setup.** Follow `references/agent-setup.md`: set up the session-start handoff
   pointer, the `next` command and the `continue` prompt hook in whatever way your tool supports.
4. **Report** what changed: files written or updated, files skipped (tool not found), the
   ignore entries added, and what your tool could not set up.
