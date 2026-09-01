---
id: TASK-053
type: task
status: pending
updated: 2026-09-01
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

**Preflight backfills a design for code that already exists, and then lets that code advance as though
it had been built against the design.**

`skills/task/SKILL.md:65-69` states it plainly: a task arrives as `created` with an
`IMPLEMENTATION.md` already on disk, and *"Preflight backfills the planning; it does not re-run
implement."*

The entry path is deliberate and correct — *"it is not an error to point `/orqestra:task` at an
unplanned task, and it must not be, because the alternative is a human running `plan` and `design` by
hand and no step verifying they did."* The consequence is what is unhandled.

**A design written after the code can only rationalize it.** The architect reads a tree that already
contains the implementation, and the cheapest design consistent with what it finds is the one it
writes. Then the gap is closed, `status` walks an unbroken chain, and the existing `QA.md` and
`REVIEW.md` advance the task — none of which evaluated the code against the design that now claims to
have governed it.

**This is the inverse of TASK-049 and shares its root.** There, an artifact is stale because the source
moved underneath it. Here, an artifact is *born* stale because it was written after the thing it
describes. Both are the same missing invariant: **nothing records what an artifact was written
against.** They are filed separately because the remedies differ — TASK-049 needs a generation marker,
this needs a reconciliation step — but a solution to one should not contradict the other.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | §7.4.3 states that backfilled `PLAN.md` and `DESIGN.md` mark `IMPLEMENTATION.md` and every later artifact stale, rather than completing a chain that then advances |
| AC-2 | After the design gate, the spec requires implement to **reconcile** the existing code against the approved design and record the differences, followed by fresh QA and review |
| AC-3 | The reconciliation is distinguishable from a normal implement in the artifact, so a reader can tell that code preceded its design — the fact that makes the review worth reading |
| AC-4 | Preserving manual work stays possible: the outcome of reconciliation may be "the code already matches", but it is a **recorded finding**, not an assumption |
| AC-5 | Consistent with TASK-049's mechanism, whichever it chooses — the two must not define competing notions of a stale artifact |

## Out of Scope

**`skills/task/step-preflight.md`.** `plugin` (D14), lands second (D-019).

**Forbidding the unplanned entry path.** It exists for a stated reason and removing it would push
planning back into unverified hand-work. This task makes its consequence visible, not the path illegal.

**TASK-008's own history.** It ran before several of these rules existed and is not migrated (D-030).
