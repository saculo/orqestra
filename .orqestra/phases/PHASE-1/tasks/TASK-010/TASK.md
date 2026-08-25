---
id: TASK-010
type: task
status: done
updated: 2026-08-25
phase: PHASE-1
module: docs
stack: markdown
origin: feature
depends_on: []
serves: [SC-2]
attempts: 0
---

## Goal

Correct §4.6 so it documents the task-scoped commit convention — **before** TASK-009 implements it.

This task comes first, and the ordering is the point. 13 of 17 commit sites in `skills/` say only
"Commit (§4.6)": they **cite** the specification rather than restating it. While §4.6 documents
`chore(orqestra):`, every one of them resolves to the old convention regardless of what any plugin-side
change does. Fix the citation target and most of them become correct without being touched.

§4.6 currently specifies the old format and shows three worked examples in it. A specification that
contradicts the tool is worse than one that omits the subject: the skills cite §4.6 by number, so a
reader following the citation would be told the wrong thing with full confidence.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | §4.6's convention block and all three examples show the task-id form as implemented by TASK-009 |
| AC-2 | The taskless cases (`init`, phase creation, task creation) are documented with the same rule TASK-009 implements — one rule, stated once |
| AC-3 | §3's `init` step, which names its commit message inline, matches |
| AC-4 | No `feat(`/`fix(`/`chore(`/`docs(`/`test(` example remains anywhere in the specification |

## Out of Scope

The implementation — `skills/` and `templates/config.md` are `plugin` and belong to TASK-009 (D14).

PHASE-1's own `SC-2`, which pins the literal string `chore(orqestra):`. Amending a success criterion is
a phase-definition change and a human decision (§8.2), not a task's to make.

<!-- CLOSED BY HAND 2026-08-25, outside the delivery pipeline, at the user's direction.

     Every acceptance criterion above is met and verifiable, but this task produced NO
     IMPLEMENTATION.md, QA.md, REVIEW.md, or PR — it was not run through `/orqestra:task`.
     `status: done` here records that the criteria are satisfied, not that the pipeline
     ran. Do not read this task as evidence the delivery loop works; nothing has exercised
     it end to end yet.

     Verification actually performed:
       AC-1..AC-3  §4.6 message-convention block, its four examples, and §3's init step
                   all show the scoped form.
       AC-4        `grep -nE '(feat|fix|chore|docs|test)\(' REQUIREMENTS.md` returns only
                   the line that PROHIBITS those prefixes, not an example of one. -->
