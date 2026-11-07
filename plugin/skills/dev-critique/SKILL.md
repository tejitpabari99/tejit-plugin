---
name: dev-critique
description: Optional. Runs only when the user asks for it (never automatically, never mid-loop, never in auto mode). Use to get an independent "rubber duck" second opinion — a devil's-advocate critique of a plan, design, proposal, in-progress implementation, or test suite. Most useful right after design, before implementing. Spawns one critic agent that categorizes feedback into Blocking / Non-Blocking / Suggestions. Not a diff-only reviewer (see dev-review for that): works on ideas and partial work, not just finished code.
metadata:
  version: "0.1.0"
---

# dev-critique — Devil's-Advocate Second Opinion

Before anything else, follow `../_shared/update-check.md`.

## Overview

An outside, unbiased skeptic's pass over whatever the current state of work is — a plan, a
PRD, a partial implementation, a test suite, a proposal. Core principle: **optional, run only on
request, keep it cheap** — one critic agent, no verdict gate, no mandatory artifact.
It exists to catch problems the author is too close to see, while they're still cheap to
fix. No code changes — the critic never edits, it only reports.

Shared dispatch/output conventions (cold-agent pattern, mid-tier-model/medium-effort sub-agents, frontmatter spec,
"never comment on" list) live in `../_shared/dev-common.md`.

This is not `dev-review`. `dev-review` is a post-implementation, verdict-gated check
against a finished diff before it lands (bugs/security/architecture-fit, PASS/
NEEDS_CHANGES/BLOCK). `dev-critique` is a second opinion usable at any stage — including
before there's a diff at all — that categorizes feedback by how much it should change your
plan (Blocking/Non-Blocking/Suggestions) rather than gating landing.

## When to Use

**Optional, and only when the user asks.** It is not part of the automatic loop: no skill
runs it on its own, nothing waits for it, and auto mode never runs it. After design,
`dev-design` tells the user they can ask for it. Never run it without explicit approval.

- If the user asks: right after planning, before implementing — the highest-leverage
  moment, since a Blocking finding here costs a plan revision, not a rewrite.
- If the user asks: on partial progress, to course-correct before finishing something
  built on a bad premise.
- For any non-trivial task where the user wants a second opinion: proposals, PRDs,
  designs, in-progress code, tests.
- **Not for:** a final pre-land check on a finished diff (use `dev-review` — it's
  verdict-gated and covers bugs/security/architecture in one pass); re-running after every
  trivial edit (defeats the "cheap" part — use it at real decision points).

## Workflow

1. **Workspace guard.** Apply the Workspace guard in `../_shared/dev-common.md` before
   anything else — run in the worktree of the branch whose work is being critiqued.
2. **Gather the work to critique.** Whatever form it's in:
   - Plan/proposal/PRD → the plan text or file itself.
   - Partial or finished implementation → `git --no-pager diff` (staged/unstaged) or
     `git --no-pager diff main...HEAD`, plus the relevant surrounding files for context.
   - Tests → the test files plus what they're meant to cover.
3. **Spawn 1 sub-agent**, using
   `critique-agent-prompt-template.md`. Cold agent — give it the full work product, not a
   summary, plus what the work is trying to accomplish. It may not edit files or spawn
   further agents.
4. **Report directly to the human/orchestrating agent** — Blocking Issues, Non-Blocking
   Issues, Suggestions, in that order. If there are no Blocking issues, say so explicitly
   ("no blocking issues, safe to proceed") rather than leaving it ambiguous.
5. **Act on Blocking issues before continuing** the work being critiqued. Non-Blocking and
   Suggestions are the acting agent's call — note them, don't force a detour.
6. **No mandatory artifact.** This is meant to be lightweight and conversational. Only
   write a findings file if the human is tracking critique history across iterations
   — in that case, write
   `critique-<YYYY-MM-DD-HHMM>.md` into the branch folder (find/create it per
   `../_shared/dev-common.md`): sibling to `PRD.md`/`TASKS.md` if critiquing a
   sub-project, otherwise at that folder's root. Frontmatter per `../_shared/dev-common.md`
   (`status: done`, `summary:` the bucket counts).

## Verdict — not a gate, a triage

Unlike `dev-review`, there's no PASS/BLOCK computed by this skill. The critic returns three
buckets and the acting agent decides what to do:

| Bucket | Meaning | What happens next |
|---|---|---|
| Blocking | Must address for the work to succeed | Fix/revise before continuing |
| Non-Blocking | Should fix to improve quality, won't prevent success | Fix if cheap, else track it |
| Suggestions | Nice-to-have, not critical | Take or leave it |

## Output (when reporting inline)

```
## Critique — <what was reviewed>

### Blocking Issues
- <issue> — <impact> — <recommended fix>
(state explicitly if none: "No blocking issues — looks solid.")

### Non-Blocking Issues
- <issue> — <impact> — <recommended fix>

### Suggestions
- <suggestion>
```

## Common Mistakes

- Running it without the user asking. It is opt-in.
- Treating Suggestions as mandatory — only Blocking issues should stop forward progress.
- Using it as a substitute for `dev-review` before landing — it doesn't gate, and doesn't
  run the 3-persona bug/security/architecture pass `dev-review` does.
- Asking for critique without stating the goal — "what is this trying to accomplish" is
  required context; without it the critic can only nitpick surface details.
