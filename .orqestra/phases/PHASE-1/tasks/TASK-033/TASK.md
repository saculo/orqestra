---
id: TASK-033
type: task
status: pending
updated: 2026-08-30
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

**The specification has no `diagnose` skill, and one row quietly says so.**

`skills/bugfix/step-diagnose.md` dispatches the analyst with `STEP: diagnose` and no `SKILL:`, because
there is no skill to name. That is the last envelope `check-envelopes.py` cannot pass, and it cannot be
fixed by inventing a value — under D-025 a `SKILL` value is **invoked**, so naming a skill that does not
exist is worse than omitting it.

Before the skill can be authored (TASK-034), the spec has to make room for it. Two places assume it is
absent:

| where | what it says today |
|---|---|
| §4.8.1:584 | `DIAGNOSIS.md`'s writer is **"`bugfix` diagnose"** — a workflow-plus-step, and the only catalogue row that names no skill. Every other row names one: `plan`, `design`, `qa`, `review-task` |
| §5.1.1 routing | the step→skill table has no `diagnose` row, so an orchestrator resolving that step finds nothing |

Found by TASK-030's plan, which blocked `needs-splitting` rather than crossing into `docs` to fix it.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | §4.8.1's `DIAGNOSIS.md` row names a skill, in the same form every other row uses |
| AC-2 | The step→skill routing table carries `diagnose`, so resolving that step yields a skill name rather than nothing |
| AC-3 | **Every** site that assumes `diagnose` has no skill agrees with the amendment — not only §7.3 — and no section is renumbered, since citations across ~90 files depend on the numbers holding |
| AC-4 | Neither site asserts a hard-coded skill **count**. A number that every new skill invalidates is a defect, not a fact |

<!-- AMENDED 2026-08-30, by human decision (§8.2), after plan found the inconsistency
     reaches five sites rather than two.

     AC-3 WIDENED from "§7.3 agrees" to "every site agrees". Plan found §2:118,
     §4.8.1:584, §5.1.1:777 and :786, §7.7:1447 and §7.12:1642-1651 all assume diagnose
     has no skill. §7.3:1196 needs no edit — it names step files, not skills, and already
     agrees. A partial amendment leaves §7.12 contradicting its own grid, and no criterion
     anywhere would have caught it.

     AC-4 ADDED. "22 skills." is asserted twice, 1500 lines apart, and TASK-034 makes it
     23. Rather than update the number — which forces a choice between a spec that
     briefly overstates the tree (against orqestra-conventions) and an edit TASK-034 may
     not make (against D-019) — the sites stop asserting a count at all. The count is
     derivable from the tree and every new skill invalidates it, so hard-coding it is the
     defect. Fixing the class dissolves the dilemma.

     templates/config.md needs NO diagnose row, reading accepted. Its routing table serves
     the delivery pipeline, where the subagent varies by module and must be resolved;
     diagnose is a planning-workflow step whose agent is hardcoded, and after TASK-034 its
     envelope carries `SKILL: orqestra:diagnose` literally, so no lookup occurs. If that
     reading is wrong, check-envelopes.py catches it in TASK-034 — a cheap failure against
     an existing check rather than a third task filed on speculation.

     ALSO CORRECTED, from plan: §4.8.1:583 (`BUG.md` | `bugfix` intake) has the identical
     workflow-plus-step shape and is TRUTHFUL — intake dispatches no subagent. The
     discriminator is `grep ROLE: skills/bugfix/`, which returns exactly one hit. Only
     :584 is wrong. -->

## Out of Scope

Authoring `skills/diagnose/SKILL.md` — that is TASK-034, which depends on this. Docs leads (D-019).

Making `check-envelopes.py` green. It stays red on `step-diagnose.md` until TASK-034 lands.
