---
name: clarify
description: "Interactively closes gaps in a PRD before planning — unknowns, ambiguities, risks, and unstated assumptions — and writes CLARIFICATIONS.md with resolved answers, recorded assumptions, and anything still open. Use when a planning workflow reaches the clarify step, or when the user says '/orqestra:clarify'."
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion
disallowed-tools: Agent, Edit, NotebookEdit
---

> **Invocation**: invoked **directly** by `orqestra:greenfield` — never as a subagent, so
> the questions reach the human rather than an agent. **Class**: planning

# orqestra Clarify

Close the gaps in the PRD before anyone plans against it.

You are the one skill that talks to the user at length. Everything downstream — phases, tasks, designs —
inherits whatever ambiguity survives this step, and it gets more expensive to fix at every stage.

## Inputs

| Read | Why |
|---|---|
| `PRD.md` | The product as written |
| `PROJECT.md` | Stack and constraints already fixed |
| `decisions/INDEX.md` | **Always read** (D4). A settled decision is not a question — do not re-ask it |

## Output

- **Writes**: `.orqestra/CLARIFICATIONS.md`. **Nothing else** (D1, D2) — in particular, **never edit
  `PRD.md`.** The PRD is the human's document; your output records what it left open.
- **May write**: `decisions/D-NNN-*.md` when an answer settles something that constrains future work.
- **Template**: `${CLAUDE_PLUGIN_ROOT}/templates/CLARIFICATIONS.md`, copied literally (D16).

## Procedure

Run in order (D6):

1. Read the PRD end to end before asking anything.
2. Collect gaps into four kinds, and **classify before asking** — the kind determines whether it is a
   question at all:

   | Kind | Handling |
   |---|---|
   | **Unknown** — needed to plan, not stated | Ask |
   | **Ambiguity** — stated two ways | Ask, offering the readings |
   | **Assumption** — you can proceed on a default | Record it, do not ask |
   | **Risk** — knowable only later | Record it, do not ask |

   Most apparent gaps are assumptions. Asking about all of them is how clarification becomes an
   interrogation and the human stops reading the questions.

3. Ask via `AskUserQuestion`, **one topic at a time**, offering concrete options where real ones exist.
   Never present a wall of questions.
4. Record each answer against its question. An answer that changes what is buildable **and constrains
   future tasks** also becomes a `decisions/D-NNN-*.md` — regenerate `INDEX.md` afterward.
5. Anything still unresolved goes under `## Open`, honestly. An open question recorded is cheaper than
   the block it prevents at design.
6. Write `CLARIFICATIONS.md`, verify against the schema, declare `SCHEMA: ok` (D12).

## Question discipline

- **Ask only what changes the plan.** If both answers produce the same phases and tasks, it is not a
  clarification, it is curiosity.
- **Offer options.** "What should happen when a session expires?" with three concrete behaviours beats
  an open prompt.
- **Never ask what the PRD already answers.** Read it properly first.
- **Never re-ask a settled `D-NNN`** (D9).

## Return

```
STATUS:  done | blocked
OUTCOME: <n> resolved, <n> assumed, <n> open
KEY:     <the 2–3 answers that most changed the shape of the work>
OPEN:    <what remains unresolved, or none>
SCHEMA:  ok
```

## When you cannot proceed

| Condition | `blocked_reason` |
|---|---|
| PRD is missing or empty | `contradictory-input` |
| The user cannot answer a question that blocks all planning | `contradictory-input` |

## Rules

1. **Never edit `PRD.md`** (D1). Record, do not rewrite.
2. **Never answer your own questions** to move faster. An assumption is recorded as an assumption, in
   `## Assumptions`, where a human can see and reject it.
3. **Never create phases or tasks** (D3). Clarify only.
4. Skip entirely when `CLARIFICATIONS.md` exists with every question answered — re-asking answered
   questions is the fastest way to make a workflow feel broken.
