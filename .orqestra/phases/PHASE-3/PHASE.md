---
id: PHASE-3
type: phase
status: pending
updated: 2026-08-24
phase: PHASE-3
criteria_count: 7
---

## Goal

One designed task goes to review-passed quality locally, and the rework loop provably converges
instead of oscillating.

## Success Criteria

| id | criterion | verified by |
|---|---|---|
| SC-1 | `/orqestra:task <ID>` takes a task from `designed` to a `passed` review, dispatching implement, qa, and review with the module's expertise loaded at each | a full local run on a real task from PHASE-2's output |
| SC-2 | A qa failure returns to implement with **only the failing criteria** in `REWORK`, and the second attempt fixes them without re-doing the rest of the task | seed an implementation that fails 2 of 6 criteria; diff attempt 1 against attempt 2 |
| SC-3 | A `changes-requested` review returns to implement citing specific `F-N` findings, and converges to `passed` within `max_attempts` | seed a defect a reviewer will catch; run the loop |
| SC-4 | Rework exceeding `max_attempts` blocks with `blocked_reason: max-attempts` and **does not attempt a fourth time** | seed an unsatisfiable criterion; count dispatches |
| SC-5 | A diff touching a file outside the task's module `paths` produces a `major` review finding | implement a task that deliberately edits another module |
| SC-6 | Preflight detects a design invalidated by a merged task, refreshes it via `design`, and **re-gates** the refreshed design | design task B, deliver task A so it invalidates B's assumptions, then run B |
| SC-7 | An `origin: bug` task is reviewed with the `regression-risk` lens and its qa requires a test that fails against the pre-fix code | run a bug-derived task through the pipeline |

## Scope

`task` steps preflight, implement, qa, review; the `implement`, `qa`, and `review-task`
skills; the rework loop; the `attempts` budget; module `PATHS` enforcement.

## Out of Scope

Anything touching the remote — no branches, no pushes, no PRs. That is PHASE-4, deliberately: prove
the loop terminates before adding state that is expensive to unwind.
