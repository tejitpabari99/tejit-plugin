---
name: dev-review
description: Invoked automatically by dev-code once per finished sub-project, and once more over the whole branch diff when all sub-projects are done (one review if there is only one sub-project or light mode); also usable when pointed at any diff. Independent review of the diff before it lands. Spawns 3 parallel reviewer personas (bugs/correctness, security, architecture-fit) against the diff + PRD, synthesizes one verdict, and writes a single review artifact. Feeds back into dev-code (fix loop) or dev-design (PRD gap) so the design→tasks→code→review loop can continue.
metadata:
  version: "0.1.0"
---

# dev-review — Multi-Persona Code Review

Before anything else, follow `../_shared/update-check.md`.

## Overview

Independent review stage that `dev-code` invokes automatically, before a sub-project (or
the whole branch) is considered done. Scopes follow Review cadence in
`../_shared/dev-common.md`: once per sub-project (never per task), then one full review of
the whole branch diff at the end, without asking or waiting. One sub-project, or light
mode: one review covers both. Core principle: **cheap but not shallow** — 3 parallel reviewer personas
with distinct blind spots, not one generic pass and not the full 7-specialist fanout. No
code changes, no test runs — read the diff, write one findings file, hand back a
routing decision.

Shared dispatch/output conventions (cold-agent pattern, commit format, frontmatter spec) live in
`../_shared/dev-common.md`. **Model override:** all reviewer sub-agents in this skill run on
your strongest available model, overriding the shared mid-tier default.

**Bar for feedback: high-confidence only.** Confidence framing and the "never comment on"
list are shared across this pipeline — see `../_shared/dev-common.md`. Each persona
reports only what it's confident is a real problem in its lane; if unsure, it stays
silent rather than padding the findings list.

## When to Use

- `dev-code` just finished a sub-project, or all sub-projects (it calls this for you); or
  a human points at a diff/commit range and wants a second pair of eyes before merge.
- Re-running after a fix loop to confirm must-fix items are resolved.
- **Not for:** reviewing a PRD before implementation exists (that's a design discussion,
  not a code review); fixing issues found here (route back to `dev-code`); running tests of any kind
  (`dev-code` runs the tests for its change, `dev-ship` runs the full suite — this is a
  *read* of the diff).

## Workflow

1. **Workspace guard.** Apply the Workspace guard in `../_shared/dev-common.md` before
   anything else — run in the worktree of the branch under review.
2. **Locate inputs.** Diff = `git diff` against the default branch (sub-project review:
   the commits of that sub-project; full review: the whole branch) or the exact commit
   range given. If a `PRD.md`/`TASKS.md` exists for this work (from `dev-design`/
   `dev-tasks`), read them — especially the PRD's `## Architecture` and `## Decisions`
   sections. Read the project `AGENTS.md` if present.
3. **Spawn 3 reviewer personas in parallel**, one sub-agent each (your strongest
   available model), using `review-agent-prompt-template.md`. Each is cold — give full diff, relevant PRD
   excerpts, and its persona brief. None of them may edit files or spawn further agents.
4. **Synthesize.** Dedupe overlapping findings (keep the higher severity, note if >1
   persona flagged it). Order by severity. Compute the overall verdict (rules below).
5. **Write one artifact**: `review-<YYYY-MM-DD-HHMM>.md` in the branch folder (find/create
   it per `../_shared/dev-common.md`) — the sub-project folder, sibling to `PRD.md`/
   `TASKS.md`, if this diff belongs to one; otherwise the branch folder's root. Multiple
   runs → multiple timestamped files (history of the fix loop).
6. **Report** verdict, must-fix findings, and the recommended next step — don't just leave
   the file sitting there. Commit the artifact (`docs: review artifacts`).
7. **Handoff.** Write the Handoff section for this stage (verdict, next step) per
   `../_shared/dev-common.md`. When `dev-code` invoked this review, write the file and
   return with no message; `dev-code` prints "Continue here" only when the run actually
   stops. When a human invoked it directly, end with that message (skipped in auto mode).

## Personas — exactly 3, no more

| Persona | Focus |
|---|---|
| Bug Hunter | Correctness: logic errors, edge cases, error handling, state/data bugs |
| Security | Injection, authz/authn gaps, secret leakage, unsafe input/output handling |
| Architect | Fit vs PRD intent, over-engineering vs YAGNI, coupling, code reuse, simplicity |

Skip test-coverage and style/conformance personas by default — `dev-code` is already
test-first, and style nits aren't worth a dedicated agent. If the repo has a
`.github/repo-profile.md` and the human specifically wants conformance checked, fold it
into the Architect persona's brief instead of adding a 4th agent.

## Verdict rules

1. Any persona reports a **blocking** issue (exploitable security hole, data loss, broken
   core behavior, silent incorrect output) → **BLOCK**.
2. Otherwise, any persona has **must-fix** findings → **NEEDS_CHANGES**.
3. Only nits/observations, nothing must-fix → **PASS**.

## Output

`review-<timestamp>.md` (frontmatter per `../_shared/dev-common.md`):

```
---
status: done
summary: <verdict — e.g. "NEEDS_CHANGES — 2 must-fix">
date: <YYYY-MM-DD>
---
# Review — <date time> — <scope: sub-project name | full branch>
Diff: <base>...<head>   Personas: Bug Hunter, Security, Architect

## Verdict: PASS | NEEDS_CHANGES | BLOCK

## Must-fix
- [Persona] file:line — issue → why it matters
...

## Notes (non-blocking)
- [Persona] file:line — observation
(omit this section if empty)

## Next step
<see routing below>
```

## Next step routing

- **PASS** → next sub-project if any remain; otherwise the full-branch review; after the
  full review passes, `dev-ship` (it asks "Ship?" only if no PR is open; auto mode never
  asks).
- **NEEDS_CHANGES** → back to `dev-code` with the must-fix list as its next task; re-run
  `dev-review` on the follow-up diff. Max 3 rounds, then stop and report.
- **BLOCK**, or a finding reveals the PRD itself is wrong/incomplete → route to
  `dev-design` to amend the PRD (record it as an Open Question), then `dev-tasks`, then
  `dev-code` again. In auto mode, BLOCK is a real blocker: stop and report.

## Common Mistakes

- Spinning up more than 3 personas for a normal-sized diff — that's the expensive
  7-specialist pattern this skill deliberately avoids.
- Reviewing the diff without reading the PRD — findings that aren't grounded in the
  intended design read as opinion, not review.
- Treating style nits as must-fix (they're notes, not blockers).
- Reporting anything on the shared "never comment on" list as a low-priority note instead
  of staying silent — see `../_shared/dev-common.md`.
- Writing the artifact and stopping — always end with a routing decision, not just a file.
