---
name: create-phases
description: "Breaks a clarified PRD into delivery phases, each a milestone with demonstrable value and numbered success criteria. Writes PHASES.md and a PHASE.md per phase. Use when a planning workflow dispatches phase creation, or when the user says '/orqestra:create-phases'."
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion
---

> **Invocation**: dispatched by `orqestra:greenfield`, or `/orqestra:create-phases`.
> Interactive. **Class**: planning

# orqestra Create Phases

Break the product into **delivery phases**. A phase is a milestone with demonstrable value — something
you could stop after and still have shipped something real.

## Inputs

| Read | Why |
|---|---|
| `PRD.md` | The product |
| `CLARIFICATIONS.md` | Resolved gaps and assumptions — treat as part of the PRD |
| `PROJECT.md` | Stack and constraints |
| `decisions/INDEX.md` | **Always read** (D4). Settled decisions constrain what phases are possible |

## Output

- **Writes**: `phases/PHASES.md` (index) and `phases/PHASE-N/PHASE.md` per phase. **Nothing else** (D1, D2).
- **Templates**: `templates/PHASES.md`, `templates/PHASE.md` — copied literally (D15).

## Procedure

Run in order (D6):

1. Read the PRD and clarifications together.
2. Identify milestones. **The governing rule: build only what this phase needs now.** No infrastructure
   "for later", no modules created ahead of the phase that uses them, no abstractions built before the
   second caller exists. This rule does more to keep phases small than any sizing heuristic.
3. For each phase write `SC-N` success criteria — **observable and verifiable**, because `review-phase`
   checks each one against actual behaviour at phase close. "Auth works" cannot be verified;
   "a user can register, log in, and log out; sessions expire after 24h" can.
4. Order the phases. Each must be deliverable given only what precedes it — a phase depending on a later
   one is misordered, not a dependency.
5. Write `PHASES.md` with the ordering rationale, then each `PHASE.md`.
6. Verify against the schema and declare `SCHEMA: ok` (D12).

## Sizing a phase

A phase is too big when its `SC-N` list stops describing one coherent milestone. Split on the seam where
the earlier half is independently shippable — never on an arbitrary count.

A phase with one success criterion is usually fine. A phase with twelve is two phases.

## Return

```
STATUS:  done | blocked
OUTCOME: <n> phases
PHASES:  <id: goal — <n> criteria>     one line each
ORDER:   <why this order, in one line>
SCHEMA:  ok
```

The phases gate summary. A human approves the decomposition and the ordering from these lines alone.

## When you cannot proceed

| Condition | `blocked_reason` |
|---|---|
| PRD too vague to derive milestones | `contradictory-input` — run `clarify` first |
| PRD requirements contradict each other | `contradictory-input` |
| A settled `D-NNN` rules out the described product | `contradictory-input` |

## Rules

1. **Never invent scope.** If the PRD does not describe it, it is not a phase. Say what is missing.
2. **Never renumber existing phases** (D8). New phases append. `create-phase` handles additions.
3. **Success criteria are observable behaviour**, always. Unverifiable criteria make phase close
   meaningless.
4. **Do not create tasks.** That is `create-tasks`, after this gate. Phases only (D3).
5. Block rather than guess (D11).
