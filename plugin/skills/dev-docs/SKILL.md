---
name: dev-docs
description: Use when writing, organizing or updating project documentation - creating a docs/ folder, adding a doc page, recording a decision (ADR), writing a mission, architecture or reference page, or keeping docs in step with a code change. Sets the folder structure, the writing style, the index rule and the rule to update docs in the same change as the code.
metadata:
  version: "0.1.0"
---

# dev-docs - Write and keep project docs

Before anything else, follow `../_shared/update-check.md`.

Docs are part of the change. A change is not done until its docs are right.

## 1. Pick the structure

- **Technical project** (code, APIs, pipelines, infra): use the full structure below.
- **Non-technical project** (research, writing, ops, planning): one `docs/` folder is enough. Flat pages, one `docs/README.md` index. Still apply sections 3 to 5.
- Only create a folder when it has something to hold. An empty folder is noise. Add it with its first doc.

## 2. Full structure (technical project)

| Path | Question it answers | Audience |
|---|---|---|
| `docs/mission.md` | What is this for, and what is out of scope? Wins over all other docs. | Everyone |
| `docs/architecture.md` | How does the system fit together? | Everyone |
| `docs/concepts/` | How should I think about this? Behavior that crosses components. | Users and contributors |
| `docs/implementation/` | How is this implemented? Private details. | Maintainers and coding agents |
| `docs/reference/` | What exactly is supported? Precise, lookup-oriented facts. | Users |
| `docs/decisions/` | Why is it like this? Numbered ADRs. | Contributors |
| `docs/testing/` | How do I test it, and what do I verify before a release? | Contributors |
| `docs/specs/` | What behavior is promised? Normative rules with acceptance criteria. | Contributors and coding agents |
| `docs/examples/` | How do I call it? Runnable public-API usage. | Users |
| `docs/contracts/` | What is the machine-readable interface? Schemas plus a README of rules a schema cannot express. | Producers, consumers, coding agents |
| `docs/agent_files/<branch-timestamp>/` | What did agents produce on this branch? PRDs, tasks, reviews, notes. | Coding agents |

Rules for the structure:
- Every folder has a `README.md` index (see section 4). `docs/README.md` indexes the whole tree with the same table.
- `mission.md` wins when docs conflict. Agents read it before any work and do not build outside its scope without approval.
- A contract's schema wins on structure. Its README wins on rules a schema cannot express. Change both in the same commit.
- `agent_files/`: one folder per branch, named `<branch-name>-<YYYYMMDD-HHMM>` with `/` replaced by `-`. Create it once per branch and reuse it. Index every folder in `agent_files/README.md` with one line each.
- Put each fact in one place. Other docs link to the owner instead of repeating it.

## 3. Writing style

- Short sentences. Plain words. Prefer "use" over "utilize".
- One idea per doc. If a page grows a second topic, split it and index both.
- Line 1 is the title. Line 3 says what the page is for, in one sentence. Line 5 is `**Audience:** <who>.`
- Say what the page is for before the detail. A reader should know in ten seconds whether to keep reading.
- Name the code a page describes: `Code: \`path/to/module/\``. Link to other docs with relative links.
- Use tables for lookups (settings, codes, stages), bullets for parallel items, short paragraphs for reasoning.
- Bold a term once, where it is defined. Contrast with "X, not Y" when a term is easy to misread.
- Give exact values: defaults, limits, names, codes. No "usually" or "some" when a number exists.
- Examples are fictional and generic. Never paste real user data or secrets into docs.
- No history in the body ("we used to..."). History belongs in an ADR or a changelog.

Templates for each page type are in `references/templates.md`.

## 4. Indexes

Every folder `README.md` has: title, one line stating the folder's question, the `**Audience:**` line, then one entry per file:

```
- [file.md](file.md): what it covers, in one line.
```

Folders of numbered or dated items (decisions, agent_files) use a table with one row per item. The index and the files must match: no file without a line, no line without a file.

## 5. Decisions (ADRs)

Numbered `NNNN-short-title.md`, never renumbered. Sections, in order: Status, Context, Decision, Alternatives, Consequences. Keep each to a few sentences. A decision that changes an earlier one gets a new ADR; mark the old one `superseded by NNNN`. Add every ADR to `docs/decisions/README.md`.

## 6. Keep docs current (every change)

In the same change as the code, every time:
1. Find the docs the change touches: reference, implementation, concepts, testing, examples, contracts.
2. Update them. A stale doc is fixed in place, not appended to or left with a "note: now different".
3. New decision, or a reversal of one: write a new ADR.
4. New doc: add it to its folder index (and `docs/README.md` if it is a new folder).
5. Changed interface or schema: update the contract and its version history.
6. Removed feature: delete its docs and index lines. Do not leave dead pages.
7. Where practical, add a test that fails when docs drift from code (for example, settings listed in a reference page versus settings in code).

Before finishing: grep the docs for the old name, flag or path, and check every relative link resolves.

## 7. Add "Where docs go" to AGENTS.md

When you create or reorganize `docs/`, add this section to the project's `AGENTS.md` (tool-neutral instructions file), trimmed to the folders that exist:

```markdown
## Where docs go

| Path | Purpose | Audience |
|---|---|---|
| `docs/mission.md` | Governing mission and scope. Wins over other docs. | Everyone |
| `docs/architecture.md` | How the system fits together | Everyone |
| `docs/concepts/` | How should I think about this? | Users and contributors |
| `docs/implementation/` | How is this implemented? | Maintainers and coding agents |
| `docs/reference/` | What exactly is supported? | Users |
| `docs/decisions/` | Why is it like this? (ADRs) | Contributors |
| `docs/testing/` | How to test, what to verify before release | Contributors |
| `docs/specs/` | Normative behavior with acceptance criteria | Contributors and coding agents |
| `docs/examples/` | Runnable usage examples | Users |
| `docs/contracts/` | Machine-readable interface contracts | Producers, consumers, coding agents |
| `docs/agent_files/` | Branch-scoped agent artifacts, one folder per branch | Coding agents |

Update docs in the same change as the code. New decision: new ADR. New doc: add it to the index.
```

For a non-technical project, a single row for `docs/` is enough.
