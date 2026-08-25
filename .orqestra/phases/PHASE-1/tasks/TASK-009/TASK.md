---
id: TASK-009
type: task
status: pending
updated: 2026-08-25
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
depends_on: []
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

## Out of Scope

`REQUIREMENTS.md` §4.6, which documents the convention and carries three `chore(orqestra):` examples.
That is the `docs` module and therefore TASK-010 (D14).

Rewriting the history already committed. The convention applies from adoption forward; rewriting 20
commits would break every SHA already cited in artifacts and decisions.
