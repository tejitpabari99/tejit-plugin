---
name: dev-ship
description: Use to ship a finished branch. Triggers include "ship", "push", "open PR", "ship it". Runs ALL test suites, pushes, opens or updates the pull request, and watches CI until it passes or fails. Never merges.
metadata:
  version: "0.1.0"
---

# dev-ship — Test, Push, PR, CI

Before anything else, follow `../_shared/update-check.md`.

Section names below (Workspace guard, Test policy, CI default, Question rules, Auto mode,
Review cadence, Handoff) are in `../_shared/dev-common.md`. Never merge. Never force push.

## Steps

1. **Ship gate.** `gh pr view --json number,url,state` for the current branch. Only
   `state` OPEN counts as an open PR; merged or closed counts as no PR.
   - Open PR exists: ship directly, no question.
   - No open PR: if the user directly asked to ship (said "ship", "push", "open PR"), that
     is the yes. Otherwise ask exactly one yes/no, "Ship?" (default yes). Auto mode never asks. No other
     question about push, PR, title or base branch. A "no" ends the skill; keep the Handoff.
2. **Workspace guard.** Apply it. Then `git pull --ff-only` if the branch has an upstream.
3. **Run ALL test suites** in the repo. Find the commands in the project rules, the CI
   workflow, and package files (`package.json`, `pyproject.toml`, `Makefile`, and so on).
   This is the only skill that runs the whole suite (Test policy). On failure, fix through
   `dev-code` fix-only, then rerun. Max 3 rounds, then stop and report.
   If no CI workflow runs the tests, warn once at the end; do not add one (CI default).
4. **Push.** `git push -u origin <branch>`.
   - No PR: `gh pr create --base <default-branch> --title <title> --body-file <file>`, body
     filled from `pr-template.md`.
   - PR exists: regenerate the body from `pr-template.md`, `gh pr edit <n> --body-file <file>`,
     then push.
5. **Watch CI.** Dispatch a CI monitor sub-agent. It runs this as a background command, so
   no model turn is spent per check, then ends its turn and reports when the command exits:
   ```
   timeout 1800 gh pr checks <n> --watch --interval 300
   ```
   It re-checks every 5 minutes for at most 30 minutes. By exit status:
   - `0`: all checks passed. The agent closes; report the PR URL.
   - `124` (timeout): still pending after 30 minutes. Report pending and stop.
   - other non-zero: a check failed (or none exist; see below). Get the run ID from
     `gh pr checks <n> --json link`, then the logs with `gh run view <run-id> --log-failed`.
     Fix through `dev-code` fix-only, go back to step 3. Max 3 CI rounds, then stop and
     report.
   - No checks reported: right after a push they may not have started. If a workflow file
     exists, retry every 60 seconds for 5 minutes before concluding none are configured.
     If still none, warn, finish.
6. **Handoff.** On success remove this section of `_next-context_.md` (Handoff). On a stop,
   write what failed and what is next, then end with the "Continue here" message (skipped in
   auto mode).
