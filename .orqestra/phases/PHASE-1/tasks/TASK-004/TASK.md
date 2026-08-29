---
id: TASK-004
type: task
status: done
updated: 2026-08-29
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
depends_on: [TASK-003]
serves: [SC-3]
attempts: 0
---

## Goal

`/orqestra:init` is safe to run twice. It never silently overwrites a workspace or a PRD, and it
reports environment gaps without failing on them.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | Running `/orqestra:init` where `.orqestra/` already exists refuses and changes nothing, naming `--force` as the override |
| AC-2 | `/orqestra:init --force` proceeds, and the report states plainly what it is about to replace before replacing it |
| AC-3 | An existing `PRD.md` is never overwritten, with or without `--force` |
| AC-4 | Running outside a git repository stops with an explanation, since artifact commits (§4.6) are load-bearing rather than optional |
| AC-5 | A missing git remote or unauthenticated `gh` produces a warning and a successful init — planning works without either; only delivery needs them |

## Out of Scope

The happy path (TASK-003). Migration of an existing workspace to a newer schema version — `--migrate`
is deferred until a schema version actually changes (§4.8.4).
