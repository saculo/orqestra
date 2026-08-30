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
| AC-2 | `create-phases` conforms under the amended rule without inventing a **scope-unit** value |
| AC-3 | F-3 and F-4, deferred from TASK-015, are resolved or restated as still-open with a reason — the module condition reaches `close-phase`'s `PHASE`-scoped dispatch and `add-phase/step-define-phase.md`, or says why it need not |

<!-- AMENDED 2026-08-30, by human decision (§8.2), after plan surfaced two defects in the
     criteria themselves.

     AC-2: the clause "and `scripts/check-envelopes.py` encodes the amendment" is STRUCK.
     `scripts/` is the `plugin` module and this task is `docs`. TASK-030 already carries that
     work — depends_on: [TASK-024, TASK-029], AC-1 is the checker exiting 0, and its Out of
     Scope reads "Changing §5.5 ... that is TASK-029's". The evidence is one-directional:
     AC-2 overreached. This is NOT needs-splitting, and striking the clause is what keeps
     TASK-030's reason to exist intact.

     "without inventing a value" is narrowed to "without inventing a SCOPE-UNIT value". The
     human chose the marker-line route (below), so a new FIELD is permitted; what stays
     forbidden is putting a fake TASK/PHASE/BUG value on a dispatch that has no such unit,
     which was the original intent.

     AC-3: F-2 -> F-3. TASK-015's REVIEW.md:15 records F-1 and F-2 as closed and :24 records
     F-3 and F-4 as open. AC-3's own description is verbatim F-4, so the pair it means is
     F-3 and F-4. Graded against F-2 it would have been unsatisfiable by construction.

     DESIGN DIRECTION, decided here rather than left to the architect: the amendment MAY
     introduce a marker line on project-wide dispatches rather than only widening the rule.
     That makes the shape self-describing and the rule decidable by looking at one line, at
     the cost of making TASK-030 ten envelope edits plus the checker rather than one file. -->

## Out of Scope

`skills/` — the `plugin` module. TASK-030 applies this amendment; docs leads (D-019).
