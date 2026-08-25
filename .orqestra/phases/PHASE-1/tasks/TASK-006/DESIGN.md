---
id: TASK-006
type: design
status: done
updated: 2026-08-25
task: TASK-006
decisions: []
---

## Components

Three fixtures:

| fixture | contains | proves |
|---|---|---|
| A | 8 titled tasks: 1 delivered, 1 pushed blocking two, 1 gated, 1 blocked, 2 ready | AC-3, AC-5, and leverage-based selection |
| C | A, mutated: PR merged, gate approved, block cleared — six equal candidates | AC-4 tie-break |
| empty | a git repo with no `.orqestra/`; an initialized workspace with no phases | AC-1, AC-2 |

## Interfaces

Unchanged; `status` stays read-only.

## File Plan

| path | action | purpose |
|---|---|---|
| `skills/status/SKILL.md` | modify | Separate the two ordering axes |

## Decisions

- **Row order and next-command are separate axes**, and the skill must say so. Row order answers *what
  needs attention*; the next command answers *what releases the most work*. They legitimately disagree.
- **Every high-attention row carries its own inline action**, so nothing needing a decision is invisible
  merely because it is not the single next command.

## Test Strategy

Grade every row of fixture A against pre-written expectations; confirm the tie-break on C; confirm both
empty states name the right next command.
