# Coding-Agent Prompt Template (dev-code)

One sub-agent **per task** (in light mode, one agent for the whole request). Default
sequential (one task → verify → next); independent sub-projects may run in parallel only
with separate git worktrees. Dispatch/commit conventions in `../_shared/dev-common.md`. The agent implements
ONE task, test-first, verifies with the tests for its change only, makes ONE commit, and
**never touches `TASKS.md`** — the orchestrator owns Status.

---

## PROMPT (per task)

```
You are implementing ONE task from an approved plan. Implement ONLY this task — do not
start other tasks, refactor unrelated code, or add scope the task doesn't specify. Do NOT
edit TASKS.md (any file named TASKS.md) — the orchestrator tracks task status, not you.

First read `../_shared/dev-common.md` (relative to the skill folder; give the agent the resolved path) for the commit convention.

=== METHOD ===
- Test first: write a test that fails for the right reason, run it and watch it fail,
  write the minimum code to pass, run it and watch it pass, then tidy. A test that never
  failed proves nothing. Test cases are mandatory for every task.
- Evidence before claims: actually RUN the tests you created or that your change impacts
  and include the real command + output in your report. No "should work" / "looks
  correct". Do NOT run the whole test suite; that runs later, in the ship stage.
- When something fails: reproduce it, read the real error, form ONE hypothesis at a time
  and test it, fix the cause not the symptom. After 3 failed attempts, stop and report.

=== PROJECT & CONSTRAINTS ===
- Repo: <path>. Stack: <one line>.
- READ and OBEY the project AGENTS.md: <path/to/AGENTS.md>.
- Test command: tests for this change only, e.g. `cd backend && pytest -q tests/test_x.py`
  (name the specific files/tests; never the whole suite).
- Current branch: <branch>  (commit here, inside this git worktree; do NOT switch branches
  or touch main).

=== YOUR TASK (verbatim from TASKS.md; in light mode, the user's request) ===
<NN-name> / Task <N> — <short name>
<paste the task's full section text: what it is, what changes at a high level, done-when>
Sibling tasks already completed (commits) so you build on them: <list>
(Light mode only: if the repo has no CI workflow that runs tests on push/PR, also add one,
e.g. .github/workflows/ci.yml.)

=== GROUND YOURSELF (TASKS.md has no file list — find it yourself) ===
(Light mode: no PRD; skip to exploring the repo.)
The PRD is authoritative design context. Read it, especially "## Architecture" and
"## Decisions", to understand the intended shape:
<repo>/docs/agent_files/<branch-slug>-<YYYYMMDD-HHMM>/<NN-name>/PRD.md

Then explore the repo yourself (search and read tools) to find the actual files this task
touches — the task text names components/behaviors, not paths. Ground every edit in real,
currently-existing code; don't assume a file exists because the PRD implies it.

=== WHEN DONE ===
1. Ensure the working tree contains ONLY this task's changes (never TASKS.md).
2. Make EXACTLY ONE commit on the current branch:
   message: "<NN-name>: Task <N> — <short name>"
   attribution per ../_shared/dev-common.md.
3. Reply with: commit SHA; files changed; the exact test command + its real output; each
   done-when/acceptance criterion marked met/not-met; any deviations or new issues found
   (describe them — do NOT act on them).

If you cannot make the task pass (tests stay red, criterion unmet, blocker found): STOP,
do NOT commit broken code, and report the blocker with what you tried and what the
evidence showed.
```

---

## Orchestrator checklist (main thread, per task)

- [ ] Set this task's Status to `in-progress` in `TASKS.md` before dispatch.
- [ ] Branch is a feature branch (not `main`); working tree clean before dispatch; the
      worktree is on the latest default branch (pulled) with dependencies installed.
- [ ] Agent returned a real commit SHA; `git show --stat <sha>` matches the task's intent.
- [ ] Test output in the report is real and green and covers only the change's tests
      (spot-check; re-run those if doubtful; do not run the whole suite).
- [ ] A new test exists for the new behavior.
- [ ] `git show <sha>` does not touch `TASKS.md` — reject/re-dispatch if it does.
- [ ] Acceptance criteria met → set Status `done`. If not → set Status `blocked`, stop the
      run, record the blocker.
- [ ] Logged the task row for the `code-<timestamp>.md` artifact.
- [ ] After the last task of a sub-project: `dev-review` invoked (not per task); handoff
      written.

## Tips

- **Put completed-sibling commits in the prompt** so the agent builds on, not over, them.
- **One commit, one task, zero TASKS.md edits** — reject reports that violate any of these.
- **Stop-on-red is correct behavior**, not failure to push through.
- **Capture deviations/new issues** from each agent into the run artifact and route real
  scope changes back to the PRD via `dev-design`.
