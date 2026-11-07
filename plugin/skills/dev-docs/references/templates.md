# Doc templates

Copy a template, replace the `<...>` parts, delete what does not apply. Keep the sentences short.

## Folder index (`docs/<folder>/README.md`)

```markdown
# <Folder name>

<The question this folder answers.> <One clause on what it holds.>

**Audience:** <who>.

- [page-one.md](page-one.md): <what it covers, one line>.
- [page-two.md](page-two.md): <what it covers, one line>.
```

## Docs root index (`docs/README.md`)

```markdown
# Docs

| Path | Purpose | Audience |
|---|---|---|
| [mission.md](mission.md) | Governing mission and scope | Everyone |
| [architecture.md](architecture.md) | How the system fits together | Everyone |
| [concepts/](concepts/) | How should I think about this? | Users and contributors |
```

One row per folder or top-level file that exists.

## Mission (`docs/mission.md`)

Governs everything else. Say at the top that it wins when docs conflict.

```markdown
# <Project name>

## Mission and scope

<What the project is, in two or three sentences.>

### The problem
<Who has it, why current options fail.>

### What we are building
<The product in plain terms. What the user gets.>

### What it does
<The checks, features or outputs. Lists of allowed values live here and are mirrored elsewhere.>

### Boundaries
<What it does not do. One short subsection per boundary.>

### Principles
<Short rules that settle trade-offs.>
```

## Architecture (`docs/architecture.md`)

```markdown
# Architecture

High-level design: how the system fits together.

**Audience:** everyone.

<Two short paragraphs: the main flow, and the one rule that shapes the design.>

```
<client> --<call>--> <service> --<call>--> <dependency>
```

| Part | Job | By |
|---|---|---|
| <part> | <one line> | <what does the work> |

Where the code lives:

| Path | Holds |
|---|---|
| `<path>/` | <what> |

Details: [implementation/](implementation/), [concepts/](concepts/), [decisions/](decisions/).
```

## Concept (`docs/concepts/<topic>.md`)

```markdown
# <Topic>

<One sentence: what this page helps you understand.>

**Audience:** users and contributors.

<The idea, in plain words. Define each term once, in bold.>

- **<Case one>:** <result>.
- **<Case two>:** <result>.

**Boundary with other topics.** <What belongs here and what does not, with links.>
```

## Implementation (`docs/implementation/<component>.md`)

```markdown
# <Component>

<Stage or role.> Code: `<path/>`.

**Audience:** maintainers and coding agents.

## <Part one> (`<file>`)

<What it does, when it runs, inputs and outputs. Name the functions that matter.>

## <Part two> (`<file>`)

<The rules or decision table. Defaults live in reference/, link to them.>
```

## Reference (`docs/reference/<topic>.md`)

```markdown
# <Topic>

<What exactly is listed here. Who owns the underlying list, if another doc does.>

**Audience:** users.

| Name | Default | Meaning |
|---|---|---|
| `<NAME>` | `<value>` | <one line> |
```

Reference pages hold exact facts only. No reasoning; link to concepts or decisions for that.

## Decision (`docs/decisions/NNNN-short-title.md`)

```markdown
# NNNN. <Decision as a short statement>

**Audience:** contributors.

**Status:** accepted. <or: proposed, superseded by NNNN>

**Context.** <The problem and the forces, in two or three sentences.>

**Decision.** <What we do. Present tense.>

**Alternatives.** <What else was considered, and why not.>

**Consequences.** <What gets easier, what it costs.>
```

## Testing (`docs/testing/<topic>.md`)

```markdown
# <Topic>

**Audience:** contributors.

From `<dir>/`:

```bash
<exact commands>
```

<Whether it runs offline, what it needs.>

| Where | What |
|---|---|
| `<path>` | <what is tested> |
```

A pre-release checklist is a numbered list. One verifiable step each, with the command.

## Spec (`docs/specs/<behavior>.md`)

```markdown
# <Behavior>

<What the behavior promises.>

**Audience:** contributors and coding agents.

## Rules
1. <Normative rule, testable.>

## Acceptance criteria
- Given <state>, when <action>, then <result>.
```

If there are no specs yet, the folder README says so and says where the nearest rules live. Do not create empty spec files.

## Contract (`docs/contracts/README.md`)

```markdown
# <Interface> <version>

Source of truth for <what>. <Who> owns it. <Who> implements it.

| File | What it is |
|---|---|
| [x.schema.json](x.schema.json) | Machine-checked structure. |
| This file | Conventions, field meanings, and rules a schema cannot express. |

If this file and a schema disagree about structure, the schema wins. About a rule the schema cannot express, this file wins. Change them in the same commit.

## Versioning
<MAJOR.MINOR.PATCH rules. Version history with links to ADRs.>

## Conventions
<Indexing, units, ordering, encodings.>
```

## Agent files index (`docs/agent_files/README.md`)

```markdown
# Agent files

Branch-scoped agent artifacts, one folder per branch.

**Audience:** coding agents.

Put PRDs, task lists, reviews, plans and notes for a branch in `docs/agent_files/<branch-name-timestamp>/`. Replace `/` in the branch name with `-`. Create the folder once per branch and reuse it.

| Folder | Purpose |
|---|---|
| [<branch-timestamp>](<branch-timestamp>/README.md) | <what the branch did, one line>. |
```
