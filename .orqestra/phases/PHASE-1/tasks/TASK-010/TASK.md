---
id: TASK-010
type: task
status: pending
updated: 2026-08-25
phase: PHASE-1
module: docs
stack: markdown
origin: feature
depends_on: [TASK-009]
serves: [SC-2]
attempts: 0
---

## Goal

Make `REQUIREMENTS.md` describe the commit convention that TASK-009 actually implements.

§4.6 currently specifies the old format and shows three worked examples in it. A specification that
contradicts the tool is worse than one that omits the subject: the skills cite §4.6 by number, so a
reader following the citation would be told the wrong thing with full confidence.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | §4.6's convention block and all three examples show the task-id form as implemented by TASK-009 |
| AC-2 | The taskless cases (`init`, phase creation, task creation) are documented with the same rule TASK-009 implements — one rule, stated once |
| AC-3 | §3's `init` step, which names its commit message inline, matches |
| AC-4 | No `feat(`/`fix(`/`chore(`/`docs(`/`test(` example remains anywhere in the specification |

## Out of Scope

The implementation — `skills/` and `templates/config.md` are `plugin` and belong to TASK-009 (D14).

PHASE-1's own `SC-2`, which pins the literal string `chore(orqestra):`. Amending a success criterion is
a phase-definition change and a human decision (§8.2), not a task's to make.
