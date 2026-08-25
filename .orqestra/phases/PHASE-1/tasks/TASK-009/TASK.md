---
id: TASK-009
type: task
status: done
updated: 2026-08-25
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
depends_on: [TASK-010]
serves: [SC-2]
attempts: 0
---

## Goal

**Commits are identified by the task that produced them, not by a conventional-commit type.**
`TASK-008: fix the checker coverage hole` rather than `fix(plugin): fix the checker coverage hole`.

The type prefix (`feat`/`fix`/`chore`/`docs`/`test`) carries almost nothing here: nearly every commit
this project makes is a `fix` or a `chore`, and the distinction is guesswork at the moment of writing.
The **task id** is the thing a reader actually needs — it leads to `TASK.md` for the goal and acceptance
criteria, `DESIGN.md` for why it was built that way, `REVIEW.md` for what was found, and the phase
success criterion the work serves. One prefix turns `git log` into an index into the workspace.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | Every commit the delivery pipeline makes for a task is prefixed `TASK-NNN: ` — source commits and artifact commits alike |
| AC-2 | Every artifact commit made while a task is in flight carries that task's id, so `git log --oneline` reads as a task history |
| AC-3 | Commits with no owning task — `init` scaffolding, phase and task creation — use a documented non-task prefix, and the rule for choosing between them is stated, not left to judgement |
| AC-4 | `config.md` records the convention explicitly in place of `commit_style: conventional`, and every skill that commits reads it from there rather than hard-coding a format |
| AC-5 | No skill emits a conventional-commit type prefix any more — verifiable by grepping `skills/` for `feat(`, `fix(`, `chore(`, `docs(`, `test(` |

<!-- DEPENDENCY REVERSED 2026-08-25, by human decision, after a pipeline run failed qa 3/5.
     TASK-009 originally had no dependency and TASK-010 depended on it. That was backwards.

     13 of 17 commit sites in `skills/` say only "Commit (§4.6)" — they DEFER to the
     specification rather than restating the format. So while §4.6 documents
     `chore(orqestra):`, those sites resolve to the old convention no matter what this
     task changes, and AC-1/AC-2/AC-4 are unsatisfiable from inside `plugin`.

     Once TASK-010 corrects §4.6, most of those 13 sites become correct with no further
     change — they were already deferring properly. The failure was never in the sites.

     The abandoned attempt (implement, qa 3/5, partial attempt 2) is on the local branch
     `feat/TASK-009-commits-identified-by-task-id`, commits 97567fa..f4f4513. Never pushed,
     no PR. -->

## Out of Scope

`REQUIREMENTS.md` §4.6, which documents the convention and carries three `chore(orqestra):` examples.
That is the `docs` module and therefore TASK-010 (D14).

Rewriting the history already committed. The convention applies from adoption forward; rewriting 20
commits would break every SHA already cited in artifacts and decisions.

<!-- CLOSED BY HAND 2026-08-25, outside the delivery pipeline, at the user's direction.

     Every acceptance criterion above is met and verifiable, but this task produced NO
     IMPLEMENTATION.md, QA.md, REVIEW.md, or PR — it was not run through `/orqestra:task`.
     `status: done` here records that the criteria are satisfied, not that the pipeline
     ran. Do not read this task as evidence the delivery loop works; nothing has exercised
     it end to end yet.

     Verification actually performed:
       AC-1..AC-3  `step-push.md` and `step-reply.md` name the `TASK-NNN:` form explicitly
                   while still deferring to `commit_style`; `init` documents rung 3.
       AC-4        `templates/config.md` and `.orqestra/config.md` carry `commit_style: scoped`
                   with the ladder written inline, where the value lives.
       AC-5        `grep -rnE '(feat|fix|chore|docs|test)\(' skills/ templates/` returns
                   nothing — D-018's own stated conformance test. -->
