---
id: TASK-027
type: task
status: pending
updated: 2026-08-26
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: [TASK-011, TASK-016]
serves: [SC-7]
attempts: 0
---

## Goal

Implement writer discipline and gate state in the skills: **no orchestrator writes an artifact**, and a
parked gate records enough to be resumed correctly.

This is the plugin half of TASK-011 and TASK-016, which fix the specification. It lands second because
the skills cite those sections rather than restating them (D-019).

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | No orchestrator skill instructs a write — the four known sites are gone, and a check over `skills/` confirms none remain, satisfying SC-7's verification |
| AC-2 | `PR.md` is written by a dispatched writer at push, and `pr-comments` no longer writes it |
| AC-3 | `approve`, `reject`, and `unblock` dispatch the owning skill instead of editing artifacts directly; their `allowed-tools` no longer need `Write` or `Edit` for artifacts they do not own |
| AC-4 | A gate parked in one session is correctly resumed by `/orqestra:approve` in a **new** session, verified by actually restarting — the property D-008 promises and does not currently deliver |
| AC-5 | TASK-008 is unparked: a `PR.md` exists for it, written by its legitimate writer |

## Out of Scope

§6.1, D1, and D-008 — `docs`, TASK-011 and TASK-016, both of which land first.
