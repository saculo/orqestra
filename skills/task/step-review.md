# Step — Review

Dispatch the reviewer, then **gate the human**. This is the last point before anything reaches the
remote.

## Resolve lenses

From `config.md`, default `correctness,design`. Add `regression-risk` automatically when
`TASK.md.origin: bug` — for a fix, what it might break matters more than what it adds.

## Dispatch

```
ROLE:      reviewer
STEP:      review
TASK:      PHASE-1/TASK-007
LENSES:    correctness, design

READ:
  .orqestra/phases/PHASE-1/tasks/TASK-007/TASK.md
  .orqestra/phases/PHASE-1/tasks/TASK-007/DESIGN.md
  .orqestra/phases/PHASE-1/tasks/TASK-007/IMPLEMENTATION.md
  .orqestra/phases/PHASE-1/tasks/TASK-007/QA.md
  .orqestra/decisions/INDEX.md

TEMPLATE:  templates/REVIEW.md
WRITE:     .orqestra/phases/PHASE-1/tasks/TASK-007/REVIEW.md
RETURN:    at most 10 lines, per the skill's Return contract.
```

The reviewer reads the diff itself via `git diff`. Do not pass it.

## On return

Read `REVIEW.md` **frontmatter only** — `verdict`.

| `verdict` | Do |
|---|---|
| `passed` | Gate the human |
| `changes-requested` | Back to implement. `attempts++`. `REWORK: REVIEW.md — address F-2, F-5 only` |
| `failed` | `blocked`, `blocked_reason: design-invalid` — rework cannot save it; the design needs revisiting |

## The gate

Set `REVIEW.md` to `status: awaiting-approval` **first** — that is what lets `/orqestra:approve` resume
this gate in a new session, since an `AskUserQuestion` call does not survive one.

Then present the reviewer's return lines verbatim and ask:

```
▸ GATE · review · TASK-007

  VERDICT  passed
  Findings 3 minor, 0 blocking. Retry logic reads cleanly; the backoff cap is
  arbitrary but harmless. Tests cover all 4 acceptance criteria.

  [ Approve ]  [ Reject with reason ]  [ Accept findings as tech debt ]
```

| Choice | Effect |
|---|---|
| Approve | `REVIEW.md status: done` → continue to push |
| Reject with reason | Back to implement, `attempts++`, the comment in `REWORK` |
| Accept findings as tech debt | Findings move to `IMPLEMENTATION.md` `## Tech Debt`; continue to push |

**Never print the artifact.** You do not have its body, and the return lines are what the reviewer
wrote for exactly this moment.

**Never edit `REVIEW.md` to reflect a rejection.** Reject with the reasoning and let implement re-run.
