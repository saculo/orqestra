---
id: TASK-036
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

**`check-step-refs.py` enforces two of D-026's three positions, and claims to enforce all of them.**

Carries **F-2** from TASK-024's review, recorded at `scripts/check-step-refs.py:129` and accepted as
advisory at the gate.

A `${CLAUDE_PLUGIN_ROOT}`-qualified step reference sitting in **prose** inside a `SKILL.md` passes
silently: the index-cell rule fires only when the reference is in a table row, and the step-file rule
only inside a `step-*.md`. Prose in a `SKILL.md` is the third position, and no rule covers it.

The docstring declares the limit at `:64–65`, so it is a chosen boundary rather than an oversight. What
makes it worth a task is the gap between that and what two other artifacts assert:

| where | what it claims |
|---|---|
| `D-026` third `**Constrains:**` bullet | the checker "enforces both the existence and the shape" |
| TASK-024 `QA.md`, AC-2 row | consistency is "machine-checked rather than a matter of taste" |

For over-qualified prose neither is true. The tree is correct today **by hand, not by check** — which
is the unearned confidence TASK-008 removed from `check-templates.py` one file over.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | A `${CLAUDE_PLUGIN_ROOT}`-qualified step reference in prose inside a `SKILL.md` is reported, naming the shape rule it breaks |
| AC-2 | The six never-flag categories still never flag — verified, not assumed. False positives are the failure this checker exists to avoid, and widening a rule is where they arrive |
| AC-3 | `test-check-step-refs.py` gains a case for the newly-covered position **and** a case proving the fix did not widen the two rules that already worked |
| AC-4 | `python3 scripts/check-step-refs.py` still exits 0 on the tree — the gap is a missing rule, not a hidden violation. If it does not, the finding is real and is reported rather than suppressed |

## Out of Scope

D-026's wording. The decision is right; the checker under-implements it.

The `agents/` and `templates/` directories. `check-step-refs.py` walks `skills/` only, which is
recorded tech debt and a separate question from which positions it checks inside that walk.
