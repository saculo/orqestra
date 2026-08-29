---
id: TASK-030
type: task
status: pending
updated: 2026-08-27
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: [TASK-024, TASK-029]
serves: [PHASE-3/SC-1]
attempts: 0
---

## Goal

**Every dispatch envelope conforms to §5.5, and the checker proves it.**

Carries TASK-019's AC-5, which that task could not meet: 8 of 10 envelopes conform, and the two that do
not are both blocked outside its module.

| envelope | blocked on |
|---|---|
| `skills/bugfix/step-diagnose.md` | `STEP: diagnose` names no skill — `skills/diagnose/` does not exist (TASK-024) |
| `skills/greenfield/step-phases.md` | no scope unit exists for a project-wide dispatch (TASK-029) |

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | `python3 scripts/check-envelopes.py` exits 0 — all ten envelopes conform, with nothing invented to make it pass |
| AC-2 | `check-envelopes.py` is added to `config.md`'s `test_command`, so a non-conformant envelope fails the suite rather than waiting to be noticed |

## Out of Scope

Changing §5.5. If an envelope cannot conform, the rule is wrong and that is TASK-029's, not a value
fabricated here to turn the check green.
