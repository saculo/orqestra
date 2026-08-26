---
id: TASK-017
type: task
status: pending
updated: 2026-08-26
phase: PHASE-1
module: docs
stack: markdown
origin: feature
bug:
depends_on: []
serves: [PHASE-5/SC-1]
attempts: 0
---

## Goal

**Accepting an incomplete phase must not wedge the project.**

`close-phase` offers "Accept the phase as it stands", which leaves `PHASE_SUMMARY.md` with
`criteria_met: false`. `add-phase` requires the previous phase's summary to read `criteria_met: true`.
There is no `gap_accepted` field or equivalent. So a documented, legitimate outcome permanently blocks
all subsequent planning — the tool's own escape hatch is a trap.

`close-phase` also dispatches `create-tasks` "in gap mode". `create-tasks` defines no modes and no
gap-specific procedure, so the call names a mode that does not exist.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | `PHASE_SUMMARY.md` can express "criteria not met, accepted deliberately" distinctly from "criteria not met" — a decision recorded, not a flag flipped |
| AC-2 | `add-phase`'s precondition accepts a deliberately accepted gap and refuses an unaddressed one, and the §4.8.1 row carries whatever field that needs |
| AC-3 | Gap-task creation names a procedure that exists: either `create-tasks` gains the mode with its rules stated, or `close-phase` dispatches `create-task --mode add`, which already handles single tasks |
| AC-4 | An accepted gap is traceable — which criteria were unmet, and why accepting was right |

## Out of Scope

`skills/close-phase`, `skills/add-phase`, `skills/create-tasks` — `plugin`, TASK-025 (D-019).
