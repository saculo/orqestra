---
id: TASK-024
type: task
status: pending
updated: 2026-08-26
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: []
serves: [SC-1]
attempts: 0
---

## Goal

**Three step files are referenced and do not exist.**

- `skills/add-phase/step-tasks.md`
- `skills/add-phase/step-plan-design.md`
- `skills/bugfix/step-plan-design.md`

`add-phase` and `bugfix` say these steps are shared from `greenfield`, but their step tables name
unqualified local filenames — so the orchestrator is told to read a file that is not there. Under D-007
the SKILL.md index table is what carries step order, which makes a wrong path in that table a
navigational dead end at exactly the moment the workflow needs to advance.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | Every step file named in every SKILL.md index table resolves to a file that exists — verified by a check over all 22 skills, not just these three |
| AC-2 | Sharing is expressed in a way that works: either the qualified path to `greenfield`'s file, or a real local file, chosen deliberately and consistently |
| AC-3 | The check from AC-1 is runnable and cheap enough to sit alongside `check-templates.py`, so a future rename cannot reintroduce this silently |

## Out of Scope

The content of the shared steps. This is about references resolving, not about what the steps say.
