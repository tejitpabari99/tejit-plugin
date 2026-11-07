---
name: dev-code
description: Use for ALL coding work, with or without a PRD. With an approved design+tasks folder (PRD.md + TASKS.md from dev-design/dev-tasks), executes the tasks via coding sub-agents in dependency order, one commit per task, with the orchestrator tracking each task Status in TASKS.md. With no PRD (plain request such as "add X", "fix Y", "change Z", "implement this", "write the code"), runs in light mode where the request itself is the task. Always test-first, runs only the tests for the change, then invokes dev-review and offers dev-ship. Triggers include "implement this", "code this out", "build the tasks", "implement SP3 / task 5 only", "add a feature", "make this change".
metadata:
  version: "0.1.0"
---

# dev-code — Execute PRD+TASKS into Code

Before anything else, follow `../_shared/update-check.md`.

## Overview

All code changes go through this skill, with or without a PRD. It **orchestrates coding
sub-agents** — the main thread plans order, dispatches agents, verifies their evidence,
tracks each task's Status (full mode), and never writes code itself. Core principle:
**one verified commit per task, in dependency order, test-first.**

Two modes:
- **Full mode** — an approved folder with `PRD.md` + `TASKS.md` exists. Each coding agent
  grounds itself in the PRD's Architecture/Decisions and explores the repo itself for the
  actual files (`TASKS.md` carries no code or file lists, see `dev-tasks`).
- **Light mode** — no PRD or TASKS. The guidance the user gave is the task. See below.

Shared conventions live in `../_shared/dev-common.md`; this file uses its section names
(Workspace guard, Test policy, CI default, Question rules, Plain explanation, Auto mode,
Handoff, Review cadence) rather than restating them.

**Method every task agent follows** (written out in the agent prompt):
- Test first: write a test that fails for the right reason, watch it fail, write the
  minimum code to pass, watch it pass, then tidy.
- Evidence before claims: run the tests for this change and paste the real command and
  output. No "should work".
- When something fails: reproduce it, read the actual error, form one hypothesis at a
  time and test it, fix the cause rather than the symptom. After 3 failed attempts, stop
  and report instead of guessing further.

## When to Use

- Any request to write or change code: a feature, a fix, a refactor, "implement this".
- A folder with `PRD.md` + `TASKS.md` exists and the human wants it built (full mode).
- "Implement the whole branch folder", a single sub-project, or a single task.
- **Not for:** designing/decomposing (`dev-design`) or generating tasks (`dev-tasks`).
  In full mode, a sub-project whose PRD still has `[OPEN]` items waits (see the gate).

## Input & Scope Modes

Full mode input is a **folder path**:
- **Branch folder** (`…/agent_files/<branch-slug>-<timestamp>/`) → all sub-projects, order
  from `README.md`.
- **Single sub-project folder** (`…/<NN-name>/`) → that one's tasks, in `TASKS.md` table order.
- **"only SP&lt;N&gt;" / "only task N"** → just that sub-project/task.

Light mode input is the request itself. No folder is needed.

**Fix-only** (used by `dev-ship` for test or CI failures): light mode with the failure as
the task, but no CI default and no Finish steps 2-5. Make the fix test-first, commit, and
return to the caller. The caller owns review rounds and the ship step, so their 3-round
caps do not reset.

## Light mode

Used when there is no PRD or `TASKS.md`. The user's guidance is the single task.
- No PRD, no `TASKS.md`, no Status tracking, no settled-design gate.
- If the request is too vague to act on, ask per Question rules (with a default); never
  ask for facts you can find in the repo.
- Dispatch one coding agent with the request as the task. Same method: test first, tests
  for this change only, one commit.
- **CI default:** if the repo has no CI workflow that runs the tests on push/PR, include
  wiring one in (e.g. `.github/workflows/ci.yml`) as part of the work (not in fix-only).
- Then `dev-review` (one review covers everything), then the ship question, same as full
  mode (see Finish).
- The artifact and handoff still apply; the branch folder is created per the Output
  convention.

## Preconditions (main thread, before dispatching)

1. **Workspace guard:** apply the Workspace guard in `../_shared/dev-common.md` first. It
   pulls and creates a worktree off the latest default branch for new work, or continues
   in the existing worktree with `git pull --ff-only`. Install dependencies before running
   anything. Do the rest of the run there.
2. **Auto check:** if the first message contains `auto` (see Auto mode), turn it on and
   print its explanation first, before any work. **Auto reminder:** at the first dev-code command of this piece of work, show once: "Say
   `auto` any time to run all remaining stages without stopping." Follow Auto mode if on.
3. **Read context:** project `AGENTS.md`, `README.md` index, each target `PRD.md` (esp.
   Architecture, Decisions, Manual steps, Risks / Open Questions), and `TASKS.md`. **Read
   `TASKS.md` once and hold it** — you own it for the rest of the run; sub-agents never
   read it to make decisions, only you dispatch from it. (Full mode only.)
4. **Settled-design gate (full mode only):** target `TASKS.md` missing → stop, send to
   `dev-tasks`. Target PRD's Risks / Open Questions has any `[OPEN]` item → stop, list
   them, route to the human. Do not implement unsettled design. In auto mode, OPEN items
   take the recommended default and are logged in the PRD as
   `[RESOLVED: auto default - <choice>]` instead of stopping.
5. **Git safety:** working tree clean, ignoring `docs/agent_files/` (bookkeeping edits to
   `TASKS.md` and artifacts are committed at stage end, see Finish).
6. **Order (full mode):** execution order = `TASKS.md`'s tracking table (`Depends on`
   column) within each sub-project, sub-projects ordered by the README's phases/deps.
7. **Resume (full mode):** the tracking table's `Status` column is the resume source — skip
   tasks already `done`; cross-check against `git log` if anything looks stale.
8. **Status:** no narration while working. If asked "status", answer in at most five
   lines from the `TASKS.md` Status column.

## Execution Loop (everything via agents — nothing coded on the main thread)

For each task, in order (sequential by default):

1. **Mark it `in-progress`** (full mode). Main thread edits `TASKS.md`'s tracking table —
   only the Status cell for this task — before dispatching. This is bookkeeping, not code.
2. **Dispatch one coding agent** (a sub-agent) using
   `code-agent-prompt-template.md`: repo path, the task text verbatim (from `TASKS.md`, or
   the user's request in light mode), the PRD path with instruction to read its
   Architecture + Decisions (full mode), and the mandate to explore the repo itself to
   find the files, then implement test-first. **Tell it explicitly: do not edit
   `TASKS.md`.**
3. **The agent** implements ONLY that task, test-first, runs **only the tests it created
   or that the change impacts** (Test policy: never the whole suite), makes **exactly one
   commit** (message/trailer per `../_shared/dev-common.md`). It reports: commit SHA,
   files changed, the test command + real output, acceptance criteria met, deviations.
4. **Orchestrator verifies** before advancing: commit exists, tests actually passed
   (spot-check the diff/output, don't trust prose alone). There is no per-task review;
   review happens per sub-project (see Finish).
5. **Flip Status** (full mode). Success + criteria met → main thread sets `done`. Failure
   (impl fails, tests red, criteria unmet) → main thread sets `blocked`, **stops the run**
   (don't pile broken commits or skip ahead), diagnoses (reproduce, read the error, one
   hypothesis at a time) or reports the blocker to the human, and records it in the
   artifact.

**Parallelism:** tasks with shared files or sequential deps stay serial. Independent
sub-projects in the same phase MAY run in parallel — each gets its own git worktree
nested under `<repo>/.worktrees/<sub-project-branch>`, branched from the feature
worktree's branch (install dependencies there first) and merged back into it per
sub-project (not into main).

**Commits:** one per task by default; combine only when genuinely inseparable (say so in
the artifact). Never mix unrelated changes.

**Scope discipline:** agents implement only what the task specifies. New issues/ideas
discovered mid-task go into the artifact's follow-ups (and back to the PRD via
`dev-design`), never silent scope creep.

## Finish

1. **Write the artifact** `code-<YYYY-MM-DD-HHMM>.md` in the target folder. Multiple runs
   → multiple artifacts (history). Commit the artifact and any `TASKS.md`/PRD changes
   (`docs: code artifacts`, per `../_shared/dev-common.md`). Do not run the full test
   suite here; that is `dev-ship`'s job.
2. **Review** per Review cadence in `../_shared/dev-common.md`: invoke `dev-review`
   automatically once when a sub-project's tasks are all done (never per task). When all
   sub-projects are finished, a full review of the whole branch diff runs automatically,
   without asking. One sub-project, or light mode: one review covers both. `dev-review`
   writes its file and returns here with no message; this run continues.
3. **Fix loop:** `dev-review` returning NEEDS_CHANGES comes back here with the must-fix
   list as the next task (light-mode style, one agent), then re-review. Max 3 rounds,
   then stop and report. BLOCK or a PRD gap goes to `dev-design`.
4. **Handoff (mandatory, never skip, both modes):** write the Handoff section (stage,
   done, next, open decisions, `Mode: auto` if on) to `_next-context_.md` per
   `../_shared/dev-common.md` at the end of each sub-project and before the ship ask. The
   stage is not finished until the file exists. Print "Continue here" (with the `read
   <path> and continue` block) whenever the run stops; not mid-loop, not in auto mode.
5. **Ship ask** once the final review passes: invoke `dev-ship`. If no PR is open for the
   branch, ask exactly one yes/no, "Ship?". If a PR is already open, ship directly. In
   auto mode never ask. Ask nothing else about push, PR, title or base branch. If
   `dev-ship` succeeds it removes the Handoff section (no stale section may remain); skip any further handoff message.
   If the answer is no or it stops, print the "Continue here" message.

### Artifact format (`code-<timestamp>.md`)

```
# Code Run — <date time> — <scope: all sub-projects | SP3 | SP3/Task 5>
Branch: <branch>   Base: <default branch>   Mode: full | light

## Tasks completed
| Sub-project | Task | Status | Commit | Files | Tests |
|---|---|---|---|---|---|
| 01-... | Task 1 — ... | done | <sha> | a.py, b.py | 12 passed |
| ...    | ...          | blocked | — | — | 1 failed (see below) |

## Deviations from the PRD/TASKS
- <task> — <what changed and why>

## Follow-ups / new issues discovered
- <issue> → <where it should go: PRD update, new task, bug>

## Still requires you (from PRD Manual steps + this run)
- <human-only step>
```

## Common Mistakes

- **Coding on the main thread.** Orchestrate only; all code is written by agents.
- **Implementing past the gate (full mode).** Missing TASKS or `[OPEN]` PRD items = stop
  (auto mode takes defaults and logs them).
- **Running the whole test suite.** Only tests for the change; the full suite is `dev-ship`.
- **Reviewing per task.** Review is per sub-project, plus one full review at the end.
- **Trusting "tests pass" without evidence.** Verify the diff + real test output.
- **Letting a coding agent edit `TASKS.md`.** Status is main-thread-only; a sub-agent
  editing it (even the description) breaks the tracking contract.
- **Barreling past a failure.** Stop, mark `blocked`, diagnose, report.
- **Giant catch-all commits.** One task per commit unless genuinely inseparable.
- **Scope creep.** Build the task; route new ideas to the artifact/PRD.
- **Committing to `main`, or working outside the feature worktree.** Apply the Workspace
  guard first.
- **Skipping dev-code because "it is small".** All coding goes through here; use light mode.
- **Skipping the handoff.** No `_next-context_.md` or "Continue here" = the stage is not
  finished, in light mode too (Finish step 4).
- **Skipping the artifact.** The run log is the deliverable that closes the loop.
