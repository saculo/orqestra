---
id: TASK-051
type: task
status: pending
updated: 2026-09-01
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: []
serves: [PHASE-5/SC-1]
attempts: 0
---

## Goal

**`review-phase` must verify a phase "against actual behaviour" and cannot run anything.**

Its own description promises verification *"criterion by criterion against actual behaviour"*, and its
tool grant is `Bash(git diff:*), Bash(git log:*)` (`skills/review-phase/SKILL.md:4`). Those two commands
read history. Neither builds, runs a test, starts the system, or observes an output.

The dispatch compounds it. `close-phase`'s envelope (`skills/close-phase/SKILL.md:36-51`) passes
`PHASE.md`, the tasks' `TASK.md`/`IMPLEMENTATION.md`/`QA.md`/`REVIEW.md`, and `decisions/INDEX.md`.
**`PROJECT.md` is not in `READ`** — so the reviewer does not receive the project's test command, run
command, or conventions, and could not execute them even if it wanted to.

**So the phase verdict is a documentation roll-up wearing the words of a verification.** Every input is
an artifact written by an earlier step, most of them by agents whose work is what the phase verdict is
supposed to independently confirm. `criteria_met` is the most consequential boolean in the workspace —
`add-phase` gates on it — and it is currently derived entirely from other people's paperwork.

This is the same failure the project has already found twice: TASK-028 recorded a `qa-engineer` writing
its own `REVIEW.md` and *"vouching for the independence of the qa evidence — the one check it could not
make, being the same agent."* Here the reviewer is a different agent but has the same evidence.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | The `close-phase` dispatch passes `PROJECT.md` and the resolved config in `READ`, so the reviewer receives the project's test and run commands |
| AC-2 | `review-phase` can execute those commands — its `Bash` grant covers what `PROJECT.md`/`config.md` actually resolve to, rather than `git` alone |
| AC-3 | Each success criterion in `PHASE_SUMMARY.md` records the **command run, its exit status, and what was observed** — a criterion verified by reading an artifact is marked as such and does not count as behavioural verification |
| AC-4 | A criterion that cannot be executed is reported as unverifiable rather than silently graded from artifacts, so `criteria_met: true` never rests on paperwork alone |
| AC-5 | Verified by running `/orqestra:close-phase` against a phase and confirming the summary carries real command output |

## Out of Scope

**Widening `Bash` to unrestricted shell.** The narrow grant is deliberate. The answer is the *right*
commands, resolved from `PROJECT.md`, not an open shell — and if a constrained runner is needed, that is
this task's design question.

**`criteria_met` and the accepted-gap vocabulary.** TASK-017 and TASK-025.

**`review-task`, which has the identical `Bash(git diff:*), Bash(git log:*)` grant.** It reviews a diff
rather than a running system, so the grant may be correct there. If this task concludes otherwise, that
is a finding to report, not an edit to make (D3).
