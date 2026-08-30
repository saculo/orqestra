---
id: TASK-035
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

**`modules.md` can name an agent that structurally cannot do the work it is sent, and nothing notices
until dispatch.**

TASK-029 blocked twice on exactly this. `modules.md` routes the `docs` module to `architect` — a
deliberate choice, recorded in the registry's own comment, because editing a specification is design
reasoning and no engineer persona fits it. But `agents/architect.md` granted `tools: Skill, Read,
Write, Glob, Grep`, no `Edit` and no `Bash`, while every engineer persona has both. The docs module's
designated engineer could not edit the only file the module contains, nor run the verification its step
requires. Cleared by `81d4139`, after two dispatches were spent discovering it.

The routing was right and the grant had never followed it. Nothing connects the two.

This is TASK-019's AC-3 one level up. That task checked each persona against **its own prose**;
nothing checks the **registry's routing** against the target agent's `tools:`. `check-envelopes.py`
validates envelope shape and never asks whether the named `ROLE` holds what its `STEP` requires — so a
config error surfaces as a mid-run block rather than as a finding, after a branch exists and dispatches
have been paid for.

`docs` is the only module that trips it today, because it is the only row naming a non-engineer. That
is a reason it stayed hidden, not a reason it is narrow (§5.1.1 exists so a module *can* name any
agent).

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | Every agent named in `modules.md` exists in `agents/`, and a row naming a file that is absent is reported — not discovered at dispatch |
| AC-2 | An agent routed to a step whose skill requires a tool the agent's `tools:` omits is reported, naming the module, the step, the agent and the missing tool |
| AC-3 | The check is runnable and cheap enough to sit beside the other checkers in `scripts/`, and a behavioural harness proves it catches a violation that is not currently present |
| AC-4 | The check fails against the pre-`81d4139` tree — where `docs` → `architect` held no `Edit` — and passes against HEAD. A check that has only ever been seen passing proves nothing |

## Out of Scope

Changing any `modules.md` row or any agent's `tools:`. This task detects the mismatch; deciding which
side is wrong is a human's.

Inventing a step→tools table if the specification already implies one. If it does not, say so — that
is a `docs` dependency (D-019), not a value to fabricate here.
