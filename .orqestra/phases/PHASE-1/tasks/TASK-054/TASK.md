---
id: TASK-054
type: task
status: pending
updated: 2026-09-01
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: [TASK-020]
serves: [PHASE-4/SC-1]
attempts: 0
---

## Goal

**Preflight's base-branch check fails on the state this repository is in right now, and PR adoption can
open a second PR for a branch that already has one.**

`skills/task/step-preflight.md:27-36` checks *base current with origin* using
`git rev-list --count @..@{u}`. Three defects in one line:

1. **`@{u}` is undefined when the branch has no upstream** — which is the normal state of a freshly
   created local task branch, and the state of `feat/TASK-043-bugfix-can-write-bug` as this is written.
   The command errors rather than reporting a count.
2. **It counts one direction only.** A base that has diverged — local commits *and* remote commits —
   passes an ahead-only count, and the `git pull --ff-only` that follows then fails for a reason the
   check said would not happen.
3. **Nothing defines what the base branch is.** No `base_branch` is configured or discovered, and no
   step verifies it against the remote's default.

**Push has the matching pair.** Rejection rebases onto the base rather than onto the remote task branch
(`step-push.md:21-27`), so a non-fast-forward against an existing `origin/<task-branch>` is still
non-fast-forward after the retry — the one rebase attempt is spent achieving nothing. And PR adoption
queries only open PRs (`step-push.md:29-39`), so a closed or merged PR for the same branch is invisible
and a second PR gets opened. `skills/task/SKILL.md:100-101` calls that *"the one failure that is
genuinely hard to undo."*

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | `base_branch` is established at `init` and verified against the remote's default, so no step infers it |
| AC-2 | The currency check fetches first and compares both directions — `git rev-list --left-right --count base...origin/base` — and distinguishes behind, ahead, and diverged, with a stated action for each |
| AC-3 | A branch with no upstream is a defined case with a defined outcome, not an error from an unset `@{u}` |
| AC-4 | Push rejection rebases against `origin/<task-branch>` when the branch exists remotely, so the single retry can actually succeed |
| AC-5 | PR adoption queries `--state all --head <branch>` and defines what happens for a closed and for a merged match — never silently opening a second PR |

## Out of Scope

**When the branch is created.** TASK-012 and TASK-020; this task assumes the branch exists at preflight
and fixes what is done *with* it. Hence `depends_on: [TASK-020]`.

**`gh` review-thread fetching.** TASK-022.

**Merge-queue, protected-branch or fork workflows.** Out of scope for v1 (§12); the checks here assume
a single remote and a direct push.
