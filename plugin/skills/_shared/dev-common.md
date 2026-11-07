# dev-* shared conventions

Referenced by the `dev-*` pipeline skills (design, tasks, code, review, critique,
security-review) instead of each restating it. Not a skill itself (no `SKILL.md` here).

## Dispatching sub-agents

- Every dispatched agent is **cold** — it has no memory of this conversation. Give it
  everything it needs inline: paths, decisions, exact deliverable, house format/example to
  read. Point at a real example file rather than describing a format abstractly.
- Spawn one sub-agent per unit of work (sub-project / PRD / task /
  persona). Dispatch independent units together so they run in parallel.
- **Sub-agent model: a mid-tier model, medium reasoning effort.** Never dispatch a sub-agent on a smaller model.
- A cold agent may not spawn further agents unless its calling skill explicitly says so.

## Commit convention (dev-code and any skill that commits)

One commit per unit of work. Message: `"<NN-name>: Task N — <short name>"`, body as
needed. Light mode (no sub-project or task number): `"<type>: <short summary>"` (e.g.
`fix: handle empty input`). Every stage also commits its own `docs/agent_files/` changes
(PRD, TASKS, artifacts) at stage end, as `"docs: <stage> artifacts"`, so they reach the PR
and worktrees stay removable. `_next-context_.md` is git-ignored and never committed. Follow your tool's commit attribution convention, if any. Never combine unrelated changes into one commit.

## Workspace guard (every dev-loop skill runs this first — before reading/writing anything else; `dev-cleanup` and `dev-setup` do not)

Confirm both, in the target repo:
1. **Not on a default branch:** `git rev-parse --abbrev-ref HEAD` is not `main`/`master`/
   the repo's actual default branch.
2. **Inside a linked worktree, not the primary checkout:**
   `git rev-parse --git-dir` differs from `git rev-parse --git-common-dir`.

If both pass and the request continues this branch's work, stay in this worktree and run
`git pull --ff-only` if the branch has an upstream. A new, unrelated task inside an old
worktree is new work: use the new-work path below.

If the primary checkout is on a non-default branch (work already started there): stop if
the tree is dirty and tell the human. Otherwise `git switch <default-branch>`, then
`git worktree add ".worktrees/$branch" "$branch"`, and continue in that worktree. Tell the
human you moved it.

`dev-review`, `dev-critique`, `dev-security-review` and `dev-ship` never create branches.
If they start on the default branch, stop and name the branch needed.

Otherwise (on the default branch, or the request is new work), always pull, then make a
worktree off the latest default branch (never off the current HEAD or current branch):
```
branch=<descriptive kebab-case name for the work, e.g. feat/<topic>>
git fetch origin
# keep the primary checkout clean: local-only exclude, no commit (run before cd)
ex="$(git rev-parse --path-format=absolute --git-common-dir)/info/exclude"
mkdir -p "$(dirname "$ex")"
grep -qxF '.worktrees/' "$ex" 2>/dev/null || printf '.worktrees/\n' >> "$ex"
git worktree add ".worktrees/$branch" -b "$branch" origin/<default-branch>
cd ".worktrees/$branch"
# .gitignore edit and its commit happen ONLY here, inside the new worktree
grep -qxF '.worktrees/' .gitignore || printf '.worktrees/\n' >> .gitignore
grep -qxF '**/_next-context_.md' .gitignore || printf '**/_next-context_.md\n' >> .gitignore
# if .gitignore changed: git add .gitignore && git commit -m "chore: ignore .worktrees/ and handoff file"
#   (on the new branch, per the commit convention above)
```
The `info/exclude` line stops the primary checkout showing `?? .worktrees/`. Never edit
`.gitignore` in the primary checkout.
Then install the project's dependencies inside the worktree before running anything.
Exception: `dev-code` parallel sub-project worktrees branch from the feature branch (see
`dev-code`), not from the default branch.

Do all further work — reads, writes, sub-agent dispatch — inside that worktree from then
on. Never commit to main. Read-only skills (`dev-review`, `dev-critique`,
`dev-security-review`) apply this guard too — they still write artifacts, and should run
in the worktree of the branch under review, not the primary checkout.

## Test policy

- Test cases are mandatory. `dev-tasks` always plans test coverage (a dedicated test task
  or explicit tests in each task's Done-when). `dev-code` writes tests first: a test that
  fails for the right reason, then the code that makes it pass.
- Run only the specific tests created or impacted by the change in `dev-code` and `dev-bug`.
  `dev-review` runs no tests. Never run the whole suite there.
- The full test suite runs only in `dev-ship`.
- Before saying work is done, run the relevant tests and read the output. Report what you
  saw, not what you expect.

## CI default

Every repo should run its tests on push and pull request. If it has no CI workflow that
does, `dev-tasks` adds a task to wire one in (e.g. `.github/workflows/ci.yml`), and
`dev-code` light mode does the same. That way CI already exists when the branch is pushed.
`dev-ship` only warns if none exists; it does not add one.

## Question rules

- Plain language. Define any term you use.
- Every question gives a default. One word, `defaults`, accepts all defaults.
- Never ask about push or PR. The only exception is the single "Ship?" question in
  `dev-ship`.
- Never ask for facts you can find yourself (code, config, git state, docs).

## Plain explanation

Explain so the user never has to say "I don't understand". Short sentences, everyday
words, one concrete example. If they say "I don't understand" or "explain", explain again
in plain words with a concrete example and a different angle. Never repeat the same
wording.

## Auto mode

The word `auto` anywhere in the request, or in any later message, turns it on: "auto: add
X", "auto", "run auto", "do this on auto", "add X, on auto". Exception: the word plainly
means something else (e.g. "auto-save feature"). When on, run every remaining loop stage
without stopping, through `dev-ship`, then give one final output.

- The 2-3 line explanation below prints immediately, as the very first output, before any
  work. Explain in plain lines: auto takes the recommended default for every
  open decision, logs each one (PRD Open Questions as `[RESOLVED: auto default - <choice>]`,
  otherwise in `_next-context_.md`), asks nothing more, and ships at the end. It stops only
  for a real blocker: `dev-review` BLOCK, 3 failed fix rounds, CI still failing after 3
  rounds, or missing access.
- `stop auto` turns it off.
- Persist as `Mode: auto` in the handoff section so it survives `/clear`.
- Auto never runs `dev-critique`.
- Across sub-projects: code, review, next sub-project, and so on, then the full review,
  then ship.
- Reminder, shown once at the start of the dev loop (the first loop skill of a piece of
  work) and at the first `dev-code` command: "Say `auto` any time to run all remaining
  stages without stopping."

## Review cadence

- `dev-code` invokes `dev-review` automatically once per sub-project, never per task.
- When all sub-projects are finished, a full review of the whole branch diff runs
  automatically, without asking or waiting. With one sub-project, or in light mode, one
  review covers both.
- Fix loop: NEEDS_CHANGES goes back to `dev-code`, then re-review. Max 3 rounds, then stop
  and report. BLOCK or a PRD gap goes to `dev-design`.
- After the final review passes, ask the ship question per `dev-ship`: if no PR is open
  for the branch, ask exactly one yes/no, "Ship?". If a PR is open, ship directly. Auto
  mode never asks. `dev-ship` never merges.

## Handoff

A short file so work survives `/clear` and parallel sessions:
`docs/agent_files/<folder>/_next-context_.md` (the branch folder with its mandatory timestamp, see Output convention).

- One `## <sub-project>` section per parallel session. A writer replaces only its own
  section. Each section holds: stage, what is done, what is next, open decisions,
  `Mode: auto` if on.
- Writing it is a numbered, unskippable Finish step of every stage that stops (design,
  tasks, code in both modes, review, bug), and at the end of each sub-project. A stage is
  not finished until the file is written and the "Continue here" message is shown (auto
  mode: file only). Orchestrators may write this file directly.
- End every stage with exactly:
  ```
  Continue here: type continue
  Fresh context: /clear, then continue
  ```
  followed by a code block holding `read <absolute path> and continue`. In auto mode, write
  the file but skip the message.
- Remove your section when the work is done. After `dev-ship` succeeded, no stale section
  may remain: remove it. Delete the file when no sections remain.
- Keep `**/_next-context_.md` in `.gitignore` (the Workspace guard adds it).
- On plain `continue`: look for the file under `docs/agent_files/*/` of the current branch.
  If none, search other worktrees (`git worktree list --porcelain`), since the file is
  git-ignored and lives only in the worktree that wrote it. One section resumes. Several
  sections: ask which.

## Output convention — one folder per branch

Every file any pipeline skill writes goes under one folder, created once per branch:
```
<repo>/docs/agent_files/<branch-slug>-<YYYYMMDD-HHMM>/
```
`<branch-slug>` = the current branch name with `/` replaced by `-`. The timestamp is
mandatory: never create a folder without it. Create it with `date +%Y%m%d-%H%M`, once,
when the folder is first created; it never changes on later runs.

**Find before creating:** `ls -d docs/agent_files/<branch-slug>-* 2>/dev/null` — if one or
more already exist for this branch, reuse the newest; never create a second folder for the
same branch.

Layout inside it:
```
docs/agent_files/<branch-slug>-<YYYYMMDD-HHMM>/
  README.md                          # index, written/updated last
  _next-context_.md                  # handoff, one section per session (git-ignored)
  brainstorm.md                      # brainstorm brief (skill: brainstorm), if any
  critique-<YYYY-MM-DD-HHMM>.md      # critique of the whole-branch work, if not a sub-project
  <NN-kebab-name>/                   # one folder per sub-project
    PRD.md
    TASKS.md
    code-<YYYY-MM-DD-HHMM>.md
    review-<YYYY-MM-DD-HHMM>.md
    security-review-<YYYY-MM-DD-HHMM>.md
    critique-<YYYY-MM-DD-HHMM>.md
```
`<FILE>` for a sub-project is `PRD`, `TASKS`, or a timestamped artifact (`code-<timestamp>.md`,
`review-<timestamp>.md`, `security-review-<timestamp>.md`, `critique-<timestamp>.md`).

No other location: never write to `docs/brainstorms/`, a `tasks/<YYYY-MM-DD>/` folder, "the
repo's local convention", the repo root, or a scratch fallback.

## Frontmatter (every generated pipeline doc)

Every generated PRD.md / TASKS.md / brainstorm brief / review / critique / security-review
artifact opens with:
```yaml
---
status: draft | approved | in-progress | done
summary: <one line>
date: <YYYY-MM-DD>
---
```
For a point-in-time report (review, critique, security-review), `status` is `done` once
written and `summary` is the one-line verdict (e.g. `NEEDS_CHANGES — 2 must-fix`,
`Blocking: 1, Non-Blocking: 2`) rather than a design-doc gist.

## Feedback bar — "never comment on" list

Reviewer/critic personas (dev-review, dev-critique, dev-security-review, and any future
persona-style skill) never report: style, formatting, or naming conventions;
grammar/spelling; "consider doing X" suggestions that aren't bugs; minor refactors that
don't affect correctness/design; missing docs/comments that don't cause real
misunderstanding; general "best practices" with no concrete harm named.

## Confidence framing — "silence is better than noise"

A finding should feel like discovering a $20 bill in your jeans after doing laundry — a
genuine, useful surprise, not noise to wade through. If a persona isn't confident
something is a real problem, it leaves it out rather than padding the list. A report with
zero findings is a valid, useful outcome — never pad to look thorough.

## Length discipline (generated docs)

Skills give a word **aim** (e.g. "aim for ~800–1,500 words"), not a limit — it's a soft
target that shapes the first draft. Going over is fine when the content needs it. Write
tight on the first draft: tables/bullets over prose, each fact stated once, evidence as a
short tag (`[verified: grep '...' → 0 matches]`) not a sentence. Never count words or edit
a finished draft just to cut length — no post-draft trim pass, and don't report a word
count.
