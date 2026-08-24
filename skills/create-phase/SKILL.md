---
name: create-phase
description: "Creates a single new phase in an orqestra-managed project, appending it after the existing phases with its own goal and numbered success criteria. Use when a workflow adds a phase to an existing project, or when the user says '/orqestra:create-phase'."
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion
---

> **Invocation**: dispatched by `orqestra:add-phase`, or `/orqestra:create-phase`.
> Interactive. **Class**: planning

# orqestra Create Phase

The singular counterpart to `create-phases`. One phase, **appended**.

Everything in `create-phases` applies — the same success-criteria discipline, the same *build only what
this phase needs now* rule. This skill exists for the append case, not to hold different rules.

## Inputs

| Read | Why |
|---|---|
| `PRD.md`, `CLARIFICATIONS.md` | The new phase must be derivable from the product |
| `phases/PHASES.md` | Existing phases — for numbering and to avoid overlap |
| The previous `PHASE_SUMMARY.md` | What was actually delivered, and what was left as debt |
| `PROJECT.md` | The stack as it now stands |
| `decisions/INDEX.md` | **Always read** (D4). Decisions taken in earlier phases constrain this one |

Reading the previous phase's summary matters: accepted gaps and carried tech debt are the most common
legitimate source of a next phase's criteria.

## Output

- **Writes**: `phases/PHASE-N/PHASE.md`, and appends a row to `PHASES.md`. **Nothing else** (D1, D2).
- **Template**: `${CLAUDE_PLUGIN_ROOT}/templates/PHASE.md`, copied literally (D16).

## Procedure

Run in order (D6):

1. `N = max(existing phase number) + 1`. **Never renumber existing phases** (D8) — their ids appear in
   commits, task frontmatter, and summary cross-references.
2. **Check the work is described in the PRD.** If it is not, stop and ask whether to update `PRD.md` and
   re-run `clarify` first. **Do not invent a phase the product never asked for** (D11) — this is the
   most likely place for scope to enter a project unnoticed, because by phase three the PRD is rarely
   reread.
3. Confirm the goal with the user if it was not given.
4. Write `SC-N` success criteria: observable, verifiable, checkable against actual behaviour by
   `review-phase`. Criteria restart at `SC-1` **within the phase** (D8) — they are phase-scoped, unlike
   task ids.
5. Check overlap. A criterion already met by an earlier phase is not a criterion — it is done.
6. Write `PHASE.md`, append to `PHASES.md`, verify against the schema, declare `SCHEMA: ok` (D12).

## Return

```
STATUS:  done | blocked
OUTCOME: PHASE-<N>: <goal>
CRITERIA: <SC-N: criterion>     one line each
BASIS:   <where in the PRD this comes from, or what debt it addresses>
SCHEMA:  ok
```

`BASIS` is the line that matters at the gate — it is how a human checks you did not invent the phase.

## When you cannot proceed

| Condition | `blocked_reason` |
|---|---|
| The work is not in the PRD and the user will not extend it | `contradictory-input` |
| The goal cannot be expressed as verifiable criteria | `criterion-unsatisfiable` |
| A settled `D-NNN` rules the phase out | `contradictory-input` |

## Rules

1. **Append only. Never renumber, never modify an existing phase** (D3, D5, D8).
2. **Never invent scope.** Every phase traces to the PRD or to recorded debt.
3. **Success criteria are observable behaviour**, always.
4. **Do not create tasks** (D3). That is `create-tasks`, after this gate.
5. Build only what this phase needs now.
