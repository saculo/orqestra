---
id: TASK-029
type: task
status: pending
updated: 2026-08-27
phase: PHASE-1
module: docs
stack: markdown
origin: feature
bug:
depends_on: []
serves: [PHASE-3/SC-1]
attempts: 0
---

## Goal

**§5.5's `always` class is wrong for a dispatch that has no scope unit.**

The obligation table requires "exactly one of `TASK` `PHASE` `BUG`" on every envelope. `create-phases`
creates *all* of a project's phases from the PRD: there is no single phase, task, or bug it operates on,
so no value can satisfy the rule. `skills/greenfield/step-phases.md` therefore cannot conform, and
`scripts/check-envelopes.py` reports it as a violation — correctly, against a rule that is itself wrong.

Found by TASK-019, which made the table executable. The defect is the same family as TASK-015's
deferred F-2 and F-4: the conditional class was written around `TASK.md`/`BUG.md` frontmatter and never
reached the dispatches that precede any scope unit existing.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | §5.5 states what a project-wide dispatch carries in place of a scope field, and the rule is decidable by looking at one thing — as every other row of the table is |
| AC-2 | `create-phases` conforms under the amended rule without inventing a value, and `scripts/check-envelopes.py` encodes the amendment |
| AC-3 | F-2 and F-4, deferred from TASK-015, are resolved or restated as still-open with a reason — the module condition reaches `close-phase`'s `PHASE`-scoped dispatch and `add-phase/step-define-phase.md`, or says why it need not |

## Out of Scope

`skills/` — the `plugin` module. TASK-030 applies this amendment; docs leads (D-019).
