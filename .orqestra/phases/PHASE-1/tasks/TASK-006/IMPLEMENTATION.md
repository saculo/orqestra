---
id: TASK-006
type: implementation
status: done
updated: 2026-08-25
task: TASK-006
deviation: minor
files_changed: 1
---

## Changes

`skills/status/SKILL.md` — **separated the two ordering axes**, which were written as one list and read
as one rule.

The old text said "Blocked tasks first. Anything blocked is the top of the report — **nothing downstream
matters**", then separately "pick the one that unblocks the most". Those contradict: if nothing
downstream matters, a downstream merge cannot be the next command.

`status` resolved it correctly anyway — blocked reported first, `merge PR #102 (unblocks TASK-003 and
TASK-004)` named as next, and an inline `→ /orqestra:unblock` on the blocked row so the decision is not
lost. But **I misread the same instruction while writing this task's expected answers**, predicting
`/orqestra:unblock TASK-008`. A rule that its own author misreads is not a clear rule.

Now stated as two sections: **row order — by attention**, **the one next command — by leverage**, with
the worked example showing them disagreeing and why that is correct.

## Deviations

| severity | from design | what | why |
|---|---|---|---|
| minor | not planned | Documented that high-attention rows carry inline actions | It is what makes the two axes safe to disagree — without it, a blocked task could be silently dropped from view by a leverage-based next command |

## Tech Debt

_none_
