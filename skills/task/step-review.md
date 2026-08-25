# Step — Review

Dispatch the reviewer, then **gate the human**. This is the last point before anything reaches the
remote.

## Resolve lenses

From `config.md`, default `correctness,design`. Add `regression-risk` automatically when
`TASK.md.origin: bug` — for a fix, what it might break matters more than what it adds.

## Dispatch

```
ROLE:      orqestra:reviewer
STEP:      review
TASK:      PHASE-1/TASK-007
LENSES:    correctness, design
ROUND:     1

READ:
  .orqestra/phases/PHASE-1/tasks/TASK-007/TASK.md
  .orqestra/phases/PHASE-1/tasks/TASK-007/DESIGN.md
  .orqestra/phases/PHASE-1/tasks/TASK-007/IMPLEMENTATION.md
  .orqestra/phases/PHASE-1/tasks/TASK-007/QA.md
  .orqestra/decisions/INDEX.md

TEMPLATE:  ${CLAUDE_PLUGIN_ROOT}/templates/REVIEW.md
WRITE:     .orqestra/phases/PHASE-1/tasks/TASK-007/REVIEW.md
RETURN:    at most 10 lines, per the skill's Return contract.
```

The reviewer reads the diff itself via `git diff`. Do not pass it.

`ROUND` is `1` for a first review and `2` only when re-dispatching a disputed `failed` (§8.1). The
reviewer writes it to `REVIEW.md.review_round`, which is what makes the once-only budget survive a
session boundary rather than living in this orchestrator's memory.

## On return

Read `REVIEW.md` **frontmatter only** — `verdict`, `required`, `review_round`.

`required` is the list of `F-N` ids the rework loop must address (§7.8.3). It is in frontmatter
precisely so this step never has to open the body to build a `REWORK` line.

| `verdict` | Do |
|---|---|
| `passed` | Gate the human |
| `changes-requested` | **Loop back to implement.** `attempts++`. `REWORK: REVIEW.md — address <required> only`, naming the ids verbatim from the frontmatter list |
| `failed` | **Neither loop nor block — gate the human with two routes.** See below |

A `changes-requested` verdict with an empty `required` is a contract failure, not an empty rework:
**block** rather than dispatching an implement step with nothing to fix.

**`changes-requested` always returns to implement**, never to review, never to qa. One place work is
redone (§8).

### When the verdict is `failed`

`failed` means the reviewer believes rework cannot save this. **Do not send it to implement** — that
burns attempts on a problem implement cannot solve. **Do not block it automatically either**, because a
`failed` verdict can itself be wrong: a stale design, missing context, a lens the task never claimed.

Present the reviewer's reasoning and offer two routes:

```
▸ GATE · review FAILED · TASK-007

  VERDICT  failed
  The retry wrapper cannot satisfy AC-3: the criterion requires at-least-once
  delivery, and the design's fire-and-forget publisher cannot provide it
  whatever the implementation does. This is a design problem, not a code one.

  [ Ask for a re-review ]  [ Revisit the design ]  [ Accept and continue ]  [ Abandon the task ]
```

| choice | effect |
|---|---|
| Ask for a re-review | Re-dispatch `review-task` with why the verdict is disputed, and `ROUND: 2` in the envelope. **`attempts` is not incremented** — no implementation work is being redone. **Offer this choice only when `review_round: 1`** |
| Revisit the design | `blocked`, `blocked_reason: design-invalid`. Recovery is a human's (§8.2) |
| Accept and continue | Findings move to `## Tech Debt`; continue to push. Legitimate, and recorded |
| Abandon the task | `status: superseded`, with the reason |

**Never re-review a third time.** Two independent `failed` verdicts are evidence, not noise — at that
point the disagreement is about the task, not the code, and only a human can settle it.

**The budget is `review_round`, not your memory** (§8.1). When the returning `REVIEW.md` already reads
`review_round: 2`, do not offer the re-review choice at all — present both verdicts and the remaining
three routes. `attempts` deliberately does not move here, and the re-review overwrote the same path, so
this field is the only thing that survives a session boundary and tells you which round you are in. The
superseded first review is recoverable from its artifact commit (§4.6).

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
