---
name: pr-comments
argument-hint: "<pr-number> [--task PHASE-N/TASK-NNN]"
description: "Triages and resolves review comments on a GitHub pull request — fetches every thread, classifies each as accept, reject, or discuss, applies fixes, verifies, replies, and resolves threads, looping until nothing is unresolved. Runs as a step of the task pipeline and standalone. Use when the user says '/orqestra:pr-comments <PR>', asks to address PR feedback, or the task pipeline reaches its pr-comments step."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, Task, AskUserQuestion
---

> **Arguments**: `/orqestra:pr-comments <pr-number> [--task PHASE-N/TASK-NNN]`
> With `--task`, artifacts go in the task directory and fixes route by the task's module row.
> Without it, artifacts go to `work/PR-NNN/`. **Class**: orchestrator+

# orqestra PR Comments

Resolve every review comment on a PR, and **account for every one** — including the ones you do not act
on.

The rule that shapes this skill: **never silently ignore a comment.** Every thread gets a row, a
verdict, and a recorded outcome. A reviewer who cannot see what happened to their feedback stops giving
it.

## Steps

| step | file | gate |
|---|---|---|
| fetch | `step-fetch.md` | no |
| triage | `step-triage.md` | per config (`semi` default) |
| resolve | `step-resolve.md` | no |
| verify | `step-verify.md` | no |
| reply | `step-reply.md` | no |
| recheck | `step-recheck.md` | no — loops to triage when new comments arrived |

## Fetch

```bash
gh pr view <n> --json reviews,comments,reviewThreads
gh api repos/{owner}/{repo}/pulls/<n>/comments
```

Collect **every** thread — human and bot, resolved and unresolved. Already-resolved threads are recorded
and skipped, not re-litigated.

`gh auth status` failing → **block** `gh-auth`.

## Triage

Write `COMMENTS.md`: one row per comment, in the fixed column order (§4.8.2).

| # | thread | file:line | summary | verdict | action |
|---|---|---|---|---|---|
| 1 | t_abc | `Foo.java:42` | null check missing | `accept` | add guard + test |
| 2 | t_def | `Bar.ts:11` | rename to `x` | `discuss` | conflicts with project convention |
| 3 | t_ghi | `Baz.go:88` | use a map here | `reject` | n≤3; O(n) is correct here |

| verdict | Meaning |
|---|---|
| `accept` | Valid — will be fixed |
| `reject` | Not correct here. **Requires drafted reasoning** for the human to send |
| `discuss` | Needs a human decision, not a code change |

**Bot comments** (CodeRabbit and similar) are triaged like any other — but a bot thread of many
low-signal comments may be batch-rejected with **one** drafted reply rather than one per comment.

Gate per config: `semi` stops here so a human sees the verdicts before any code changes.

## Resolve

Fix `accept` comments in **lowest-number order** (D10), one at a time. Route by the task's module row
where `--task` was given; otherwise infer the module from the file's location and say so.

**Fixes here do not re-enter the rework loop.** They are already reviewed — by the PR reviewers, on the
same diff. Re-running `review-task` would ask the same question twice and burn an attempt.

## Verify

Re-run the test suite from `PROJECT.md`. **Nothing regressed** is the bar, not "the fix works". A green
suite is required before replying — a reply announcing a fix that broke something else is worse than no
reply.

## Reply

1. Commit the fixes (`config.md` `commit_style`) and push to the task branch.
2. Reply to each thread: what changed and where, or the drafted reasoning for a rejection.
3. Resolve the threads you addressed. **Never resolve a `discuss` thread** — it is waiting on a human.
4. Write `RESOLUTION.md`: verdict, action taken, commit, thread resolved.

## Recheck

Re-fetch. New comments since the run started → loop to triage with only the new ones. None → done.

The loop terminates when a full pass adds no new threads. If it runs three times without converging,
**block** and report — a PR generating comments faster than they are resolved needs a conversation, not
another pass.

## Rules

1. **Every comment gets a row and an outcome** (D2). No silent drops.
2. **A `reject` always carries drafted reasoning.** Rejecting without explaining is how review
   relationships break.
3. **Never resolve a thread you did not address.**
4. **Never force-push** to a branch under review. It destroys the reviewers' context.
5. Verify before replying, always.
6. Block rather than guess at an ambiguous comment — that is what `discuss` is for (D11).
