---
id: TASK-005
type: implementation
status: done
updated: 2026-08-25
task: TASK-005
deviation: minor
files_changed: 1
---

## Changes

`skills/status/SKILL.md` — one real defect and one clarification:

1. **`status` named the step that failed, not the step that re-runs.** It reported "rework at qa" and
   "rework at review". The rework loop always returns to **implement**, whatever failed (§8) — qa does
   not re-run qa, and a rejected review does not re-run review. A reader acting on "rework at review"
   would expect the wrong thing to happen next. Now both facts are reported and kept distinct:
   `qa failed → rework at implement`.

2. **Trap 1's stage was under-specified.** The skill said `IMPLEMENTATION.md` with
   `changes-requested` is "in rework at implement, *not* implemented" without saying what the stage
   *is*. It is `designed`: the chain stops **before** a non-`done` artifact. Now stated.

3. **Trap 2 clarified in the same place.** A failing artifact does not advance the stage, but everything
   before it still counts — a rejected review leaves the task `verified`, because qa genuinely passed.
   Reporting it as `implemented` would discard real information.

## Deviations

| severity | from design | what | why |
|---|---|---|---|
| minor | not planned | Clarified both traps' resulting stage, not just the rework wording | Grading showed the skill never said what stage a trap *produces*, only what it is not. `status` got it right; the instruction did not require it to |

## Tech Debt

_none_
