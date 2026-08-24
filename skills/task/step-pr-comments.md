# Step — PR Comments

Hand off to the `pr-comments` sub-workflow against `PR.md`'s number, and loop until no unresolved
threads remain.

## Invoke

```
Skill: orqestra:pr-comments
Args:  <pr_number>  --task PHASE-1/TASK-007
```

`--task` matters: it tells the sub-workflow to write `COMMENTS.md` and `RESOLUTION.md` into the **task
directory** rather than `work/PR-NNN/`, and to route fixes by the task's module row. Without it the
sub-workflow behaves as a standalone run on an unrelated PR.

The sub-workflow owns its own loop — triage, resolve, verify, reply, re-check. Do not re-implement it
here; a second copy of that logic is a second copy that will drift.

## On return

| Result | Do |
|---|---|
| No unresolved threads | Continue to merge |
| Threads remain, all `discuss` | Stop and present them — they need a human, not a fix |
| Fixes were pushed | Continue to merge; CI will re-run on the new commits |
| Sub-workflow blocked | Propagate the block unchanged |

**Fixes pushed here do not re-enter the rework loop.** They are already reviewed — by the PR
reviewers, which is a stronger check than re-running `review-task` against feedback that came from
humans looking at the same diff. Re-running review here would ask the same question twice and burn an
attempt doing it.

## When there are no comments

A PR with no review comments passes straight through. Do not wait for comments to appear, and do not
prompt for them — a clean PR is the expected case, not a suspicious one.

## Report

```
✓ pr-comments · 4 comments · 3 fixed, 1 rejected with reply · all threads resolved
```
