---
id: TASK-034
type: task
status: done
updated: 2026-08-30
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: [TASK-033]
serves: [PHASE-3/SC-1]
attempts: 1
---

## Goal

**The bugfix workflow's diagnose step has no procedure of its own.**

Every other dispatched step names a skill its agent invokes — `plan`, `design`, `implement`, `qa`,
`review-task`. `diagnose` names none, so a dispatched analyst runs on its persona plus whatever prose
the envelope carries. That is exactly the composition failure D-025 closed everywhere else: the triple
*(step skill, subagent, expertise skills)* delivering two of its three layers.

`skills/greenfield/step-phases.md` was the other envelope `check-envelopes.py` could not pass; TASK-030
fixed it. This is the last one.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | `skills/diagnose/SKILL.md` exists and carries a real procedure — inputs, output, procedure, return contract, rules — at the same altitude as `plan` and `qa`. A stub satisfies nothing: under D-025 the value is invoked |
| AC-2 | Its `## Return` block opens with `SKILLS:`, as every envelope-dispatched skill's does (D-025) |
| AC-3 | `skills/bugfix/step-diagnose.md` carries `SKILL: orqestra:diagnose`, and `python3 scripts/check-envelopes.py` **exits 0** — all ten envelopes conform |
| AC-4 | `python3 scripts/check-step-refs.py` still exits 0 — the new skill's references resolve in the shape its location dictates (D-026) |
| AC-5 | `agents/analyst.md`'s `description` names the steps it is actually dispatched at, not one of them |

<!-- AMENDED 2026-08-30, by human decision (§8.2), after plan raised it as an open question.

     AC-5 ADDED. agents/analyst.md's description says "Dispatched at the plan step". The
     analyst is dispatched at FIVE — create-phase, create-phases, create-tasks, diagnose,
     plan — so it is already false by four, and this task makes it five. In module, one
     line, and the same defect class as the `implement` skill's description corrected
     during TASK-019: a description is what the harness reads when selecting an agent, so
     a false one misroutes work rather than merely reading oddly.

     Checked across all eight personas before scoping this. analyst is the only genuine
     outlier. The engineers showing no dispatches are a measurement artifact — the example
     envelopes in skills/ demonstrate backend-engineer only — and are correctly described
     for the modules that route to them.

     NOT included, noted for a future task: `architect`'s description says design only,
     but modules.md also routes the `docs` module's implement step to it — the fact
     TASK-029 blocked twice on. 81d4139 added a persona note explaining the dual role; the
     description itself still understates it. Left out to keep this task's diff to its
     criteria, and recorded here so it is a decision rather than an oversight. -->

## Out of Scope

Changing `REQUIREMENTS.md` — TASK-033 lands the §4.8.1 and routing amendments first (D-019).

Rewriting what `step-diagnose.md` does. Its procedure is the subject; the envelope's shape is already
correct apart from the missing `SKILL`.
