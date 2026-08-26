---
id: TASK-026
type: task
status: pending
updated: 2026-08-26
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: [TASK-020]
serves: [PHASE-5/SC-1]
attempts: 0
---

## Goal

**`bugfix` creates the dirty tree that later blocks its own fix.**

`step-reproduce` writes a failing automated test and updates `BUG.md`, then the workflow stops at design
and hands off to `/orqestra:task`. Task preflight blocks on any dirty tree — correctly, since a dirty
tree is a human's uncommitted work and touching it is the one mistake orqestra cannot undo.

Nothing defines a branch, commit, worktree, or cleanup owner for that reproduction test. So the normal
documented bugfix path produces a promoted task that cannot be delivered, and the only way out is a
human cleaning up by hand — the exact situation the workflow exists to avoid.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | A full `bugfix` run leaves a tree that task preflight accepts, verified end to end on a seeded bug |
| AC-2 | The reproduction test survives into the promoted task's delivery — it is the test that must fail against pre-fix code (§7.3.1), so discarding it is not an acceptable cleanup |
| AC-3 | Ownership is explicit: which branch or worktree the reproduction lives on, who commits it, and who cleans up if the bug is never promoted |
| AC-4 | An abandoned investigation leaves no stray branch, worktree, or uncommitted file |

## Out of Scope

Diagnosis quality and the promotion rules. Both are sound; this is about where the reproduction's
artifacts live.

Branch creation timing in the task pipeline — TASK-020, which this depends on.
