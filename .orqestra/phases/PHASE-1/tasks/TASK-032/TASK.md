---
id: TASK-032
type: task
status: pending
updated: 2026-08-27
phase: PHASE-1
module: docs
stack: markdown
origin: feature
bug:
depends_on: []
serves: [PHASE-3/SC-1]
attempts: 0
---

## Goal

**qa can fail on a criterion implement cannot fix, and the pipeline has nowhere to send it.**

`step-qa.md` routes every `result: failed` back to implement with `attempts++`, on the assumption that
a qa failure is always a code defect. It is not always. TASK-019 failed qa on two criteria that were
**structurally** unreachable from its module: one needed a skill that does not exist and a specification
amendment (D14, D-019), the other needed a layer that can dispatch, which no dispatched agent is.

Looping implement on those spends three attempts on work it cannot perform, and the task then blocks
with `blocked_reason: max-attempts` — a diagnosis that is actively wrong, and that points a human at
the engineer rather than at the scope.

**Review already solves this.** §8.1 gives a `failed` verdict its own route: neither loop nor block,
but gate the human with named options, because a `failed` verdict can itself be about the task rather
than the code. qa needs the same escape, and for the same reason.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | The specification states what happens when qa fails a criterion the implement step cannot satisfy, distinguishing it from an ordinary defect by a condition a reader can apply — not by judgement |
| AC-2 | That route does not increment `attempts`, on the same reasoning §8.1 gives for a disputed review: no implementation work is being redone |
| AC-3 | The human is offered named options, as the review gate is, and at least one of them splits the unmet criteria into a task where they can be met — the resolution TASK-019 actually took |
| AC-4 | `blocked_reason: max-attempts` cannot be reached by a failure of this kind, since it names the wrong cause |

## Out of Scope

`skills/` — the `plugin` module, and a separate task under D-019.

Whether qa should grade an out-of-module criterion as failed at all. TASK-019's qa held that ownership
elsewhere explains why a criterion is open but does not make it met, and that reading is correct: the
fix is a route for the failure, not a softer grade.
