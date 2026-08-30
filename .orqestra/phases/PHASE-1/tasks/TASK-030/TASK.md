---
id: TASK-030
type: task
status: pending
updated: 2026-08-27
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: [TASK-024, TASK-029]
serves: [PHASE-3/SC-1]
attempts: 0
---

## Goal

**Every dispatch envelope conforms to §5.5, and the checker proves it.**

Carries TASK-019's AC-5, which that task could not meet: 8 of 10 envelopes conform, and the two that do
not are both blocked outside its module.

| envelope | blocked on |
|---|---|
| `skills/bugfix/step-diagnose.md` | `STEP: diagnose` names no skill — `skills/diagnose/` does not exist. **Re-filed: TASK-033 then TASK-034** |
| `skills/greenfield/step-phases.md` | no scope unit exists for a project-wide dispatch (TASK-029) |

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | `skills/greenfield/step-phases.md` conforms under §5.5 as amended by D-027, and `check-envelopes.py` encodes that rule — including that the four module fields **must be omitted** under `PHASE` and `PROJECT`. Nothing invented to make it pass |
| AC-2 | `check-envelopes.py` **and** `test-check-envelopes.py` are added to `config.md`'s `test_command`, so a non-conformant envelope fails the suite rather than waiting to be noticed |

<!-- AMENDED 2026-08-30, by human decision (§8.2), after plan blocked needs-splitting.

     TASK-030 SPLIT. AC-1 bundled two unrelated changes and only one was deliverable.

     `step-phases.md` needed a PROJECT scope field, which TASK-029 delivered. That half
     stays here and is what AC-1 now means.

     `step-diagnose.md` needed a `SKILL:` naming a skill that does not exist. TASK.md's
     table claimed TASK-024 unblocked it; that premise was FALSE — TASK-024 was about
     step-file references and never touched diagnose. Worse, authoring `skills/diagnose/`
     makes REQUIREMENTS.md §4.8.1:584 wrong: it names DIAGNOSIS.md's writer as "`bugfix`
     diagnose", the only catalogue row naming a workflow-plus-step rather than a skill, and
     §5.1.1's step->skill routing has no diagnose line. Both are `docs`, so the work spans
     two modules (D14) and docs leads (D-019).

     Re-filed as TASK-033 (docs, the amendments) and TASK-034 (plugin, the skill), the
     latter depending on the former. `check-envelopes.py` stays red on step-diagnose.md
     until both land — deliberately, since a value fabricated to turn it green is exactly
     what this task's Out of Scope forbids.

     AC-2 widened to include `test-check-envelopes.py`. The checker alone would leave the
     behavioural harness unrun, and that harness is what proves the checker still catches
     violations after this task changes it.

     `.orqestra/config.md` belongs to no module, so AC-2 edits outside PATHS. Confirmed
     permitted: TASK-001 set the same line and shipped. Recorded here because the precedent
     was never written down, so review sees it as sanctioned rather than as a finding. -->

## Out of Scope

Changing §5.5. If an envelope cannot conform, the rule is wrong and that is TASK-029's, not a value
fabricated here to turn the check green.
