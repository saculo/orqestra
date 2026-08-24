---
id: TASK-003
type: task
status: pending
updated: 2026-08-24
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
depends_on: [TASK-001, TASK-002]
serves: [SC-2]
attempts: 0
---

## Goal

`/orqestra:init` turns an empty git repository into a working orqestra workspace, confirming the stack
with the user and committing the result.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | Running `/orqestra:init` in an empty git repository produces `config.md`, `modules.md`, `PRD.md`, `project/PROJECT.md`, `decisions/INDEX.md`, and empty `phases/` and `work/` directories |
| AC-2 | Every file it writes passes the TASK-001 conformance check against its template |
| AC-3 | The stack is auto-suggested from repo contents and **always confirmed** with the user via `AskUserQuestion` before being written |
| AC-4 | `modules.md` is seeded with one row whose `agent` names a real file in `agents/`, and the report explains that the registry is the thing to edit before real work |
| AC-5 | The whole scaffold lands as exactly one commit, `chore(orqestra): initialize workspace`, containing only `.orqestra/` paths |

## Out of Scope

Refusal and overwrite behaviour — that is TASK-004, deliberately split out so this task stays at five
criteria.

Scanning the codebase to populate `PROJECT.md`. v1 is greenfield-only (§1.3 principle 6); the layout
and conventions sections stay stubs until the first `design` fills them.
