---
id: TASK-005
type: task
status: pending
updated: 2026-08-24
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
depends_on: [TASK-001, TASK-002]
serves: [SC-4]
attempts: 0
---

## Goal

`/orqestra:status` reads a workspace and reports the correct stage for every task — including the two
cases where an artifact exists but the task has not advanced.

This is the highest-risk task in the phase. `status` is the state authority (§7.10): every orchestrator
calls it to decide where it is, so a wrong derivation surfaces later as inexplicable misbehaviour rather
than as a clear failure.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | Against a fixture tree containing a task at each of the eight stages in §4.3, `status` reports each one correctly |
| AC-2 | **Trap 1**: an `IMPLEMENTATION.md` with `status: changes-requested` reports the task as in rework at implement — never as `implemented` |
| AC-3 | **Trap 2**: a `QA.md` with `result: failed` leaves the task at `implemented`, and a `REVIEW.md` with `verdict: changes-requested` leaves it at `verified` — neither advances, and both report rework at **implement** |
| AC-4 | Any artifact with `status: blocked` makes the task report as `blocked`, with its `blocked_reason` as the headline, overriding every other derivation |
| AC-5 | A task with missing or malformed frontmatter reports as unknown and never as a guessed stage — an invented stage sends an orchestrator to the wrong step silently |

<!-- AC-3 amended 2026-08-25 by human decision at the QA gate. As written it claimed a
     rejected review leaves a task at `implemented`, conflating two traps that behave
     differently: when a review is rejected, qa has already passed, so the task genuinely
     IS `verified` and §4.3's stage table says so. `status` was correct; the criterion was
     loose. Amended to state each trap's resulting stage separately, and to require that
     both report rework at implement — the rework target, not the step that failed. -->

## Out of Scope

Output formatting and next-command selection — TASK-006.

Any state-derivation script. v1 stays codeless (D-001); if this task proves prompt-based derivation
unreliable, that is a finding to record against §12, not a fix to make here.
