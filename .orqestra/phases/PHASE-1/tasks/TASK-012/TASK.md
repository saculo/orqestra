---
id: TASK-012
type: task
status: pending
updated: 2026-08-26
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

**The task branch is created at preflight, before the first mutation of anything.**

§7.4 has preflight check out the *base* branch, then implement and qa modify the working tree and each
step commits its artifacts — and the branch is not created until `step-push`, step 5 of 7. So the
pipeline does its work on the base branch, which contradicts the "never work on the base branch" rule
the project ships in `templates/PROJECT.md`.

Found by running TASK-008: artifact commits had nowhere correct to land, and `git log` showed the
task's work sitting on local `master`. Rule 8 of `skills/task/SKILL.md` hedges it as "on the task branch
once one exists", which describes the bug rather than resolving it.

Consequences, all real rather than theoretical: source changes sit uncommitted on the base until push;
an interrupted run leaves them there; and a squash-merged PR leaves local base diverged, so the next
`git pull --ff-only` in preflight fails on a repo that did nothing wrong.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | §7.4 creates the task branch during preflight, after the tree and dependency checks pass and **before** any artifact or source write |
| AC-2 | §4.6's "delivery-pipeline artifact commits land on the task branch" is reachable — no step commits a task artifact while the base branch is checked out |
| AC-3 | `step-push`'s responsibilities are restated for a branch that already exists: it pushes and opens the PR, and its adoption rules still cover a resumed run |
| AC-4 | The spec states what preflight does when the base is behind its remote **or** when the base is ahead of it — the second has no defined outcome today and stopped TASK-008 at push |

## Out of Scope

Editing `skills/`. Plugin work follows as TASK-020 (D-019, D14).

Worktrees for bug reproduction — TASK-026 owns that.
