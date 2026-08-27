---
id: TASK-020
type: task
status: pending
updated: 2026-08-26
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: [TASK-012]
serves: [PHASE-3/SC-1]
attempts: 0
---

## Goal

Implement TASK-012 in the pipeline: **create the task branch at preflight**, before any artifact or
source write, and adjust `step-push` to a branch that already exists.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | `step-preflight.md` creates the branch after its checks pass; a run interrupted after implement leaves the base branch untouched — verified by inspecting `git status` on the base after an interrupted run |
| AC-2 | Every artifact commit from implement, qa, and review lands on the task branch, so the task's `.orqestra/` record travels with its PR |
| AC-3 | `step-push.md` pushes and opens the PR without creating the branch, and its adoption rules still cover a resumed run and an already-open PR |
| AC-4 | A base branch ahead of its remote has a defined outcome instead of stopping the run — this is what parked TASK-008 at push |

## Out of Scope

§7.4 and §4.6 — `docs`, TASK-012, which lands first (D-019).
