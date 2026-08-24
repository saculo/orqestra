---
id: PHASE-4
type: phase
status: pending
updated: 2026-08-24
phase: PHASE-4
criteria_count: 7
---

## Goal

Delivery reaches the remote: a reviewed task becomes a merged PR, with every review comment
accounted for and every git failure mode behaving as specified.

## Success Criteria

| id | criterion | verified by |
|---|---|---|
| SC-1 | A reviewed task produces a branch matching `branch_pattern`, a commit carrying both source and `.orqestra/` artifacts, and an open PR whose body derives from `TASK.md` and `IMPLEMENTATION.md` | a full run to an open PR on a real remote |
| SC-2 | Re-running `/orqestra:task` after the PR exists **adopts** the existing branch and PR and never opens a second | interrupt after push; re-run; count PRs |
| SC-3 | Every row of the §7.4.2 failure table produces its defined outcome — dirty tree, branch conflict, push rejected, PR already open, `gh` unauthenticated, CI red, CI pending, merge conflict | deliberately induce all 8 conditions, one at a time |
| SC-4 | The dependency gate blocks a task whose dependency's PR is open but unmerged, **before any work is done**, naming which dependency and its stage | attempt a dependent task while its dependency's PR is open |
| SC-5 | `pr-comments` gives every comment a row and a recorded outcome; every `reject` carries drafted reasoning; no `discuss` thread is auto-resolved | a PR seeded with accept-, reject-, and discuss-worthy comments, plus bot noise |
| SC-6 | The pr-comments loop terminates — it re-checks for new comments and blocks after three non-converging passes rather than looping indefinitely | add comments during the run; then add faster than they resolve |
| SC-7 | The merge gate reports CI honestly — pending holds rather than blocks, red blocks with the failing job names — and `pr_state: merged` is only recorded after `gh` confirms it | run against green, pending, and red CI |

## Scope

`step-push`, `step-pr-comments`, `step-merge`, the whole `pr-comments` sub-workflow and its 6 step
files, and the failure-mode table.

## Out of Scope

Non-GitHub forges. Auto-merge stays off by default — merging is the one irreversible action and
remains a human decision.
