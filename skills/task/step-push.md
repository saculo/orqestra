# Step — Push

The only step in orqestra that touches the remote. Branch, commit, push, open the PR, record `PR.md`.

## Procedure

1. **Resolve the branch name** from `config.md`'s `branch_pattern`, e.g.
   `feat/TASK-007-password-reset`.

2. **Branch, adopting where one exists:**

   | Condition | Action |
   |---|---|
   | Branch does not exist | `git checkout -b <branch>` |
   | Exists, belongs to **this** task | **Adopt it** — a resumed run, not a collision |
   | Exists, belongs to another task | **block** `branch-conflict` |

3. **Commit** the source changes and this task's `.orqestra/` artifacts together, using
   `config.md`'s `commit_style`. From here the task's record travels with its PR and merges with it.

4. **Push**. On rejection (non-fast-forward): rebase onto the base **once**, retry. Fails again →
   **block** `push-rejected`. One retry is the entire automatic recovery budget.

5. **Open the PR** — but check first:

   ```bash
   gh pr list --head <branch> --json number,state
   ```

   | Condition | Action |
   |---|---|
   | No PR | `gh pr create` |
   | PR already open for this branch | **Adopt it** — update `PR.md`, do **not** create a second |
   | `gh auth status` fails | **block** `gh-auth` |

   **Never open a second PR for a task.** It is the one failure in the pipeline that is genuinely hard
   to undo, and a resumed run is far more likely than a genuine collision.

   Body: generate from `TASK.md` (goal, acceptance criteria) and `IMPLEMENTATION.md` (changes,
   deviations). Honor `pr_draft`. If the repo has a PR template, follow it.

6. **Write `PR.md`** — `branch`, `pr_number`, `pr_url`, `pr_state: open`, plus `## Summary`,
   `## Commits`, `## CI`.

   This is the one artifact an orchestrator writes, and it exists only because no subagent was
   dispatched to produce it. Everything in it comes from `git` and `gh` output, never from judgement.

## Failure summary

| Condition | Detected by | Action |
|---|---|---|
| Dirty tree | `git status --porcelain` | `blocked: dirty-tree` |
| Branch belongs to another task | branch name vs `TASK.md.id` | `blocked: branch-conflict` |
| Push rejected | `git push` exit | rebase once, retry; then `blocked: push-rejected` |
| PR already open | `gh pr list --head` | adopt it |
| `gh` unauthenticated | `gh auth status` | `blocked: gh-auth` |

## Report

```
✓ push · feat/TASK-007-password-reset · PR #142 opened
```
