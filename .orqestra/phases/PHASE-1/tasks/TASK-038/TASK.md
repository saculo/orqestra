---
id: TASK-038
type: task
status: pending
updated: 2026-08-30
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: []
serves: [PHASE-3/SC-1]
attempts: 0
---

## Goal

**Three places enumerate the skills, and nothing checks they agree.**

Carries **F-2** from TASK-033's review and **N2** from its qa.

`REQUIREMENTS.md` now lists every skill three times: §5.1.1's step→skill routing table, §7.0's class
table, and §7.12's grid. TASK-033 made all three agree with the tree — verified by set-difference
against `ls skills/`, which is the check no pattern can perform, because no grep can see a missing row.

**Set membership is not agreement of content**, and that is the gap the method still has. Review found
a live instance: §7.12's grid and §7.0's class table are set-identical, yet `pr-comments` and
`close-phase` sit in columns §7.0 classes differently. Both lists are "complete"; they disagree anyway.

§7.12 also now claims outright that its grid **is** the whole inventory. That claim is true today
because TASK-033 made it true by hand. It goes silently false the next time a skill is added — the same
defect class as the hard-coded count TASK-033 removed, one level up.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | A skill present in the tree but missing from any of the three enumerations is reported, naming which one |
| AC-2 | A skill whose **class or role disagrees between two enumerations** is reported — set membership alone is not the check |
| AC-3 | The check fails against a tree with a deliberately introduced disagreement, and passes against HEAD. A check only ever seen passing proves nothing |
| AC-4 | It runs beside the other checkers in `scripts/`, CPython 3 stdlib only, and a behavioural harness covers both directions |

## Out of Scope

Changing `REQUIREMENTS.md`. This task detects disagreement; if the check finds a real one, that is a
`docs` finding to report, not a value to edit (D14, D-019).

Removing any of the three enumerations. Whether the spec should list skills three times is a design
question for someone else; this task makes the duplication safe rather than arguing about it.
