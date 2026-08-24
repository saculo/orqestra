---
id: TASK-006
type: task
status: pending
updated: 2026-08-24
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
depends_on: [TASK-005]
serves: [SC-6]
attempts: 0
---

## Goal

`/orqestra:status` presents the derived state as a table a human can read at a glance, and names
exactly one next command.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | On an uninitialized repository, `status` says so plainly and suggests `/orqestra:init` rather than erroring or reporting an empty project |
| AC-2 | On an initialized workspace with no phases, it reports that and names `/orqestra:greenfield` as next |
| AC-3 | The task table renders one row per task with its id, title, module, derived stage, and what is holding it up, using the stage names from §4.3 **verbatim** |
| AC-4 | Exactly one next command is named; where several are possible, the one that unblocks the most work is chosen, and ties break to the lowest id (D10) |
| AC-5 | A blocked or awaiting-approval task is surfaced above everything else, and an unmerged PR is reported as an active obstruction rather than as progress |

## Out of Scope

Stage derivation itself (TASK-005). Any interactive behaviour — `status` is read-only and never
prompts.
