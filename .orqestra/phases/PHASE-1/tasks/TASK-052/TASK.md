---
id: TASK-052
type: task
status: pending
updated: 2026-09-01
phase: PHASE-1
module: docs
stack: markdown
origin: feature
bug:
depends_on: []
serves: [PHASE-3/SC-1]
attempts: 0
---

## Goal

**`max_attempts: 3` permits four attempts, and one step file contradicts itself about it two lines
apart.**

The guard is `attempts > max_attempts` (`skills/task/step-qa.md:46`, `skills/reject/SKILL.md:22`
*"exceeds"*, `REQUIREMENTS.md:1680` *"exceeds"*). With the default of 3, attempts 1, 2 and 3 all pass
it; blocking happens after the **fourth** failure.

That is not obviously wrong on its own — it depends what `attempts` counts. Every other statement in
the tree says it is wrong:

| site | says |
|---|---|
| `templates/config.md:22`, `.orqestra/config.md:20` | `max_attempts: 3` |
| `REQUIREMENTS.md:1021` | *"rework cycles per step before escalating to the human"* |
| `skills/task/SKILL.md:43` | *"Past `max_attempts` (default 3) the task blocks"* |
| `skills/task/step-qa.md:44` | *"Only report it as a problem when `attempts` **reaches** `max_attempts`"* |
| `skills/task/step-qa.md:46` | *"At `attempts` **> `max_attempts`** → `blocked`"* |

**Lines 44 and 46 of the same file give different thresholds.** Whichever is intended, one of them is
executed and the other is read by the next person to change this code.

**The real defect is that there is no transition function.** `attempts` is incremented in at least four
places — `reject`, and the sites TASK-011 and TASK-028 each list separately — and compared in two, and
no section defines whether the initial execution counts as an attempt. A budget with no single
definition is a budget that differs per call site, which is what the tree shows.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | §6 or §8 defines `attempts` precisely: whether the initial execution counts, what increments it, and when. One definition, cited by everything that reads it |
| AC-2 | One comparison is stated and used everywhere — `>=` or `>` — and `max_attempts: 3` demonstrably permits three, matching its own config comment |
| AC-3 | `step-qa.md:44` and `:46` agree, and every other `attempts` site is checked against the definition rather than left to match by luck |
| AC-4 | The boundary is stated for 0, N-1, N and N+1, so a test can be written against it rather than against a reading of the prose |

## Out of Scope

**`skills/`.** `docs` (D14); the skills cite §6/§8 rather than restating them, so docs leads (D-019).

**Moving `attempts` out of `TASK.md`.** TASK-011 and TASK-016 both carved this out for the same reason —
it changes stage derivation — and it stays carved out here.

**Which sites increment it.** TASK-011 owns that table and TASK-028 explicitly declines to extend it
(D3). This task defines the *semantics*; those tasks assign the *sites*.
