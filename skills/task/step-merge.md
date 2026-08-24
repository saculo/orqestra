# Step — Merge

The last gate. Report the PR's real state, let a human decide, record the outcome.

## Gather state

```bash
gh pr view <number> --json state,mergeable,reviewDecision
gh pr checks <number>
```

| Condition | Action |
|---|---|
| CI green, no conflicts | Gate the human |
| CI still pending | **Report and hold** — not a block. Present state, wait, re-check when asked |
| CI red | **block** `ci-red`, naming the failing jobs |
| Merge conflict with base | **block** `merge-conflict` — a human resolves; never auto-resolve |
| Unresolved review threads | Return to pr-comments — the loop is not finished |

**Pending CI is not a failure.** Blocking on it would turn every slow pipeline into a stopped task.
Report it and let the human decide whether to wait.

## The gate

Set `PR.md` to `status: awaiting-approval` first.

```
▸ GATE · merge · TASK-007

  PR #142  feat/TASK-007-password-reset → main
  CI       ✓ 4 checks passed
  Review   approved by 1
  Threads  all resolved

  [ Merged — confirm ]  [ Hold ]  [ Reject with reason ]
```

| Choice | Effect |
|---|---|
| Merged — confirm | Verify with `gh pr view --json state`, then record |
| Hold | Leave `pr_state: open`. The task stays at `pushed` and blocks its dependents |
| Reject with reason | Back to implement, `attempts++` |

`auto_merge: true` in `config.md` runs `gh pr merge` instead of asking. Default is `false`: merging is
a human decision, and it is the one action in the pipeline that is irreversible from orqestra's side.

## Record

Only after `gh` confirms the merge:

- `PR.md` → `pr_state: merged`, `status: done`
- `TASK.md` → `status: done`

**Never mark merged without verifying.** A task recorded as merged whose code is not on the base branch
breaks the dependency gate for every dependent task, silently — the exact failure §7.4.1 exists to
prevent, introduced by the step that was supposed to close it.

## Report

```
✓ TASK-007 delivered · PR #142 merged

→ Next: /orqestra:task TASK-008
```

Then stop. The next task is a new pipeline run, not a continuation of this one.
