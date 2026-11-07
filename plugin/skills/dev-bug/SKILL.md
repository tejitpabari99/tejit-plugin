---
name: dev-bug
description: Use for bugs and debugging. Triggers include "bug", "debug", "why is X happening", "not working", "this is broken". Two entries, both covered - a bug is listed, or debugging only (may find no bug). Reproduces first, explains in plain terms, finds the root cause from evidence, then fixes through dev-code with a regression test.
metadata:
  version: "0.1.0"
---

# dev-bug — Reproduce, Explain, Fix

Before anything else, follow `../_shared/update-check.md`.

Section names (Workspace guard, Test policy, Question rules, Plain explanation, Auto mode,
Review cadence, Handoff) are in `../_shared/dev-common.md`.

Entries: (a) the user lists a bug; (b) the user only wants it debugged and there may be no
bug. Same steps for both.

## Steps

1. **Workspace guard.** Apply it first. Show once: "Say `auto` any time to run all
   remaining stages without stopping." Follow Auto mode if on.
2. **Reproduce before any theory or fix.** Find an exact command or steps that show the
   problem. Write down observed versus expected. If you cannot reproduce it, say what you
   tried and the one missing fact needed (with a default, per Question rules), and ask for
   it; in auto mode stop and report instead. Do not guess a fix.
3. **Explain the bug plainly** (Plain explanation): what happens, what should happen, why,
   and one concrete example. No jargon.
4. **Find the root cause from evidence.** One hypothesis at a time:
   - Read the real error and the code on the failing path. Trace back to where the wrong
     value first appears.
   - Make a prediction ("if X is the cause, then Y will show"), test it with the smallest
     probe, keep or drop it. Put probe scripts inside the project, not a temp folder, and delete them before step 6.
   - Compare with similar code that works. Do not change several things at once.
   - After 3 failed hypotheses, stop and report what you know and the one thing you need.
5. **No bug found:** report the findings and stop. No code change.
6. **Bug found:** invoke `dev-code` in light mode with these instructions. No PRD or TASKS.
   - Write a regression test that fails first, for the reason you found, then the fix, then
     see it pass. The test is what keeps the bug from returning.
   - Run only that test and the tests it impacts (Test policy), never the whole suite.
7. **Handoff.** Write the Handoff section for the bug stage (Handoff). If `dev-ship`
   succeeds below it removes the section.
8. **Review and ship.** `dev-review` follows through `dev-code` (Review cadence). Then the
   ship question, "Ship?", via `dev-ship` (skipped when a PR is open or in auto mode). If
   the run stops here, print the "Continue here" message (skipped in auto mode).
