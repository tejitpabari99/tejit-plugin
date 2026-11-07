---
name: brainstorm
description: Use before any creative or design work — a new feature, a bug-like change, a refactor, a product or business idea, a technical decision, a non-software project, or a vague brain-dump that needs sharpening. Interviews the human in rounds to turn a fuzzy idea into a decided design with a decision log, then stops for approval. Trigger phrases include "brainstorm", "grill me", "stress-test this", "poke holes in this", "help me think through", "what am I missing", or any request to build/change something that is not yet a decided design.
metadata:
  version: "0.1.0"
---

# Brainstorm

Before anything else, follow `../_shared/update-check.md`.

Turn an idea into a decided design. Interview the human until nothing important is left assumed.

Two rules make this work:

1. **Interview in rounds.** Not one question at a time. Not everything at once.
2. **Build nothing until the human says yes.**

<HARD-GATE>
No code, no scaffolding, no file writes into the project, no other
implementation skill — until you have said what you intend to do and
the human has explicitly approved it. A bigger task gets a bigger design.
The gate stays the same size.
</HARD-GATE>

Shared conventions (sub-agents, output folder, frontmatter) are in `../_shared/dev-common.md`.
Read it once. This file covers only what is unique to brainstorming.

If this is the first dev-loop skill of this piece of work, say once: "Say `auto` any time to
run all remaining stages without stopping." Follow **Auto mode** in `../_shared/dev-common.md`
if they do.

## 0. Workspace guard

Before anything else, follow **Workspace guard** in `../_shared/dev-common.md`. Do this
before reading the repo for Round 0. New work gets a fresh worktree off the latest default
branch. Continuing work stays in its worktree and pulls.

A quick answer (see size below) writes nothing, so it skips the guard.

## 1. Say the size of the task

Before your first question, say which size this is, in one sentence. The human can override you.

| Size | What it is | What it costs |
|---|---|---|
| **Quick answer** | A fact or "is it possible" question. The result is an answer, not something you keep. | State the question and how you would find out, in 2-3 sentences. One round at most. No document. |
| **Small change** | A clear change to something that already exists and that you can read. A flag, one endpoint, a copy change, one decision with little fallout. | One or two rounds. A short design in chat. No document. |
| **Full design** | A new project, a new part of a system, a restructure, a product direction, or anything whose pieces you cannot name yet. | Full interview. Written brief. |

**Small means you can read the thing today.** If it does not exist yet for you to read, it is not small. Familiarity does not count.

**Sizes only go up.** If you find hidden complexity mid-session, stop, say so, and pick the bigger size. Never go back down. When torn between two, pick the bigger one. Choosing the smaller label to skip work is the same doubt in disguise.

## 2. Look things up before asking

Never open with a question you could answer yourself.

- Read the real thing: the repo, the files, recent commits, the existing doc.
- **Finding facts is your job. Making decisions is theirs.** If a file, tool, search or sub-agent can settle a question, go settle it. Asking the human something you could have looked up wastes the one thing this skill spends.
- Send sub-agents for slow lookups (mechanics in `../_shared/dev-common.md`). Limits: at most 2 running at once, and a sub-agent may start one more at most (depth 2).
- **Do not wait on research.** Only the questions that depend on a lookup wait for it. Ask the rest now.

## 3. Round 0 — say the idea back

Start from a real moment, not an abstract goal. Ask for one concrete case: the last time the
problem bit them, or the picture of someone using the result.

Then write:

- **The idea in one paragraph, in your own words.** Not their sentence repeated. Your understanding.
- **What you are assuming.** Three to six bullets. These are the guesses you would otherwise build the interview on without anyone checking them.
- **Who or what it is for**, if that is not obvious.

Ask them to correct it before going further. A guess they can fix ("I think this is because X keeps biting you, right?") works better than an open question.

A well-run interview built on a misunderstood idea is the most expensive failure here. Round 0 is the guard against it. Skipping it is the bug.

## 4. Interview in rounds

Decisions depend on each other. Some can be asked right now. Others only make sense once an earlier answer is in.

A **round** is every question you can honestly ask now, without guessing the answers to the others. Put them all in one message. Then stop and wait.

### Round format

```
**Q1 — <short title>**

<The question. Offer concrete options where options exist; a real choice
beats an open prompt. Define any term you use.>

My take (default): <your recommended answer, and why, in one line>

---

**Q2 — <short title>**

...
```

End every round with: *"Answer by number, like 'Q1 yes, Q2 the second one, Q3 no because…'. Say `defaults` (or `all`) to accept every default."*

### Rules of the round

- **No question may depend on another question in the same round.** If Q3's answer would change how you word Q5, Q5 goes in the next round. This is why a round is safe to answer in one go.
- **Every question has a default.** A question with no default hands your thinking to the human. Say what you would pick and why. If your default argues against the question as worded, say so, so that agreeing means answering "no".
- **Plain words.** Short sentences. Define any term the first time. No jargon the human has not used.
- **A wide round means the task is too big.** If more than about seven questions are honestly askable now, say so and offer to split the task before continuing.
- **Never answer a decision question yourself.** Recommending is your job. Deciding is theirs.
- **Answers change what comes next.** Work out the new set of askable questions each round. Later rounds ask what earlier rounds could not.
- **No cap on rounds.** Some ideas need three questions, some fifty. If a session runs very long, the cause is usually size. Stop and split.
- **If they say "I don't understand" or "explain",** follow **Plain explanation** in `../_shared/dev-common.md`: new words, a concrete example, a different angle.

### Questions people skip

Work in at least one of each before you close.

- **Challenge the premise.** "Is this the right problem? What happens if we do nothing?"
- **The kill question.** "What would have to be true for this to be a bad idea?" and "What is the cheapest thing we could do to find out we are wrong?"
- **The cut pass.** Name the pieces you would drop. Ask which ones they would actually miss. Cut by default; make them argue things back in.
- **Goals, non-goals and anti-goals.** What must be true. What is out of scope. What would make it a failure even if it technically works. Write all three down; an unstated non-goal comes back as scope creep.
- **The failure question.** What happens when this breaks, and who notices?
- **The already-exists question.** What does part of this job today, and why is it not enough?
- **Reality check (product and business ideas).** Who wants this today? What do they do now instead? What is the narrowest version someone would use or pay for this week? Push for named people and real behaviour, not categories and hopes.
- **A cheap test (spike).** When one quick, throwaway try would answer a question faster than talking, offer it. A spike is thrown away unless the human decides otherwise, and keeping it is a new request that needs its own approval.

## 5. Pick angles by type of task

Not every task needs every angle. Pick the type, then spend your rounds on its angles. Add others if the answers call for them.

| Type of task | Angles to explore (3-5) |
|---|---|
| New feature | Who uses it and the real moment they need it; what they do today instead; the narrowest version worth shipping; what it touches that already exists; how we will know it works |
| Bug-like change | Exact steps and what they see vs what they expect; when it started or changed; what else depends on the broken behaviour; what must not break while fixing; the test that would have caught it |
| Refactor | Why now (what hurts today); what must stay exactly the same; where the boundaries should end up; how to move in safe steps; what we will not touch |
| Product or business idea | Who wants it today (named people); what they do instead and what it costs them; the narrowest paid or used version; why you, why now; the cheapest test of the riskiest guess |
| Technical decision | The options that are really on the table; what each costs to switch away from later; limits that rule options out (budget, skills, existing stack); what a wrong choice looks like in a year; the cheapest way to try the top two |
| Non-software project (talk, event, plan, renovation) | The outcome and who it is for; hard limits (time, money, people); the parts that cannot slip; what they have already; what success and failure look like on the day |

## 6. Design (Full design only)

When few useful questions remain:

- **Propose 2-3 approaches** with real trade-offs. Lead with your pick and say why. An approach that only exists to make another look good is padding. Cut it.
- **Present the design in sections**, each as long as its difficulty needs: a few sentences if simple, a few hundred words if tricky. After each section, ask if it lands before moving on.
- Cover: the shape of the thing, its parts and their edges, how data or control moves, what happens on failure, and how it will be checked.
- **Keep parts separable.** For each part: what it does, how it is used, what it needs. If someone cannot understand a part without reading its insides, or you cannot change its insides without breaking its users, the edge is wrong.
- **In an existing codebase:** follow the patterns already there. If existing code truly blocks this work, include a targeted fix in the design. Do not propose unrelated cleanup.

## 7. Close

An empty list of questions does not end the session. **The human saying "we agree on what this is" does.** Ask for that.

Then, by size:

- **Quick answer** — report the finding and a recommendation. Anything you built is throwaway; keeping it is a new request with its own size and approval.
- **Small change** — the short design and the decision log, in chat. Get an explicit yes. Then hand the coding to `dev-code` (light mode).
- **Full design** — write the brief, check it as a builder, then hand off.

In auto mode, take every default, skip the approval question, log each default taken in the
brief's Decision log as `auto default`, and move straight on. Stop only for a real blocker.

### The brief (Full design)

Write to `docs/agent_files/<branch-slug>-<YYYYMMDD-HHMM>/brainstorm.md`. Find or create the
branch folder per `../_shared/dev-common.md`. Aim for about 600-1,200 words (a soft target;
over is fine; never trim after writing). Frontmatter per `../_shared/dev-common.md`, then:

1. **TL;DR** — 2-4 sentences, first on the page: what was decided and why.
2. **Problem** — what we are solving, and for whom.
3. **Decision log** — one row per settled decision:

   | Decision | Alternative rejected | Why |
   |---|---|---|

   This is the part future readers use most. Every settled decision gets a row. Mark your own calls as yours, and only what the human said as theirs.
4. **Design** — the approach, its parts and their edges. Prose only where subtle; a table for anything listable.
5. **Goals, non-goals, anti-goals** — what it must do, what it will not do, and what would count as failure even if it works.
6. **Open risks** — what could still sink it, and the cheapest test for each.

**Builder check.** Before showing the brief, send a fresh sub-agent that knows nothing of this conversation. Give it the brief path and this job: "Read this as the person who must plan and build it. List every question you would need answered first. Do not suggest improvements." Sort what comes back:

- **Already answered** by the conversation or the project: add the answer to the brief.
- **Minor:** a sensible builder could settle it without changing what gets built. Settle it and mark it in the brief as your call.
- **Theirs:** only the human can answer, and the answer changes what gets built. Ask these in one message, most important first, each with a default.

That is the only question round the check produces. Update the brief, then fix inline anything
that contradicts itself, reads two ways, or has grown past one buildable unit. No second pass.
Without a sub-agent tool, read the brief yourself as that builder.

Then say: "Brief written to `<path>`. Calls I made myself: <short list>. Tell me what to change before we turn it into a design." Wait. In auto mode, do not wait.

**Handoff.** Once approved, write your section of `_next-context_.md` and end the stage
per **Handoff** in `../_shared/dev-common.md`. The next step is `dev-design`, which turns the
brief into PRDs. Do not jump to implementation.

## Anti-patterns

| Thought | Reality |
|---|---|
| "This is too simple to need a design." | Simple means a short design, not none. Two sentences, then approval. |
| "The design is obvious — I'll start while they read it." | The gate is their approval, not the length of the design. |
| "I'll ask them what the config currently says." | Facts are your job. Go look. |
| "I'll ask everything I can think of in one round." | A round is only what is askable now. Dependent questions wait. |
| "I'll skip the default, it's their call." | The decision is theirs. The default is yours and not optional. |
| "I'll use the technical word, they'll get it." | Plain words, defined on first use. |
| "No more questions, so we're done." | Done is when they say the understanding is shared. |
| "It grew, but I'm nearly finished — no need to re-size." | Hidden complexity moves the size up. Stop and say so. |
| "They approved the quick answer, so the follow-up is approved too." | Every task gets its own size and its own approval. |

## It's working if

- Round 0 surfaced at least one assumption they corrected.
- Each round is numbered, with a default per question, answerable by number or by `defaults`.
- No question needed another question in the same round answered first.
- Later rounds ask things the first round could not have.
- You looked facts up instead of asking for them.
- Background research never stalled a round.
- The questions fit the type of task (section 5).
- Question count is high; round count is low.
- It ended by asking, not by starting.
