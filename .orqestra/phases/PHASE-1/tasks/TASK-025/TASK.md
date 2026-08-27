---
id: TASK-025
type: task
status: pending
updated: 2026-08-26
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: [TASK-017]
serves: [PHASE-5/SC-1]
attempts: 0
---

## Goal

Two defects in task creation, both in skills.

**Split mode contains mutually exclusive rules.** Rule 6 says repoint anything depending on the original.
Rule 2 says never touch a task other than the one being split and its parts. Both cannot hold: either
dependencies stay pointed at a superseded task — which stalls delivery at the §7.4.1 dependency gate —
or the isolation rule (D3) is violated. Whichever an implementation picks, it violates a stated rule.

**Gap mode does not exist.** `close-phase` dispatches `create-tasks` "in gap mode"; `create-tasks`
defines no modes.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | Split mode's rules are consistent — repointing dependents is either permitted with its bound stated, or delegated to something that may do it |
| AC-2 | Splitting a task that two others depend on leaves no dependency pointing at the superseded id, verified against a fixture |
| AC-3 | Gap-task creation dispatches a procedure that exists, matching whatever TASK-017 settles in the spec |
| AC-4 | D3's isolation rule still means something afterwards — if an exception is added, it is named and bounded rather than softened |

## Out of Scope

§7.7 and the `PHASE_SUMMARY.md` schema — `docs`, TASK-017 (D-019).
