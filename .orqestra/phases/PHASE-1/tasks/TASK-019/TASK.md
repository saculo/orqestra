---
id: TASK-019
type: task
status: pending
updated: 2026-08-26
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: [TASK-015]
serves: [PHASE-3/SC-1]
attempts: 0
---

## Goal

**Dispatched agents cannot reach the step skill or the expertise skills the architecture is built on.**

Every agent's `tools:` allowlist omits `Skill`, and none declares a `skills:` preload. Under D-024 that
list is a true allowlist binding the whole subagent run. So the composition the design rests on —
*(step skill, subagent, expertise skills)* — delivers exactly one of its three layers.

All eight personas carry an instruction they cannot execute:

> "Load the module expertise skills named in your envelope **before** starting. They carry this
> project's conventions, which you cannot infer from the stack."

`agents/backend-engineer.md:17` goes further: "the expertise skills in your envelope are how you tell
them apart" — naming, as the mechanism that distinguishes two backend modules, something no agent can
reach.

**Confirmed empirically**: in the TASK-008 run on 2026-08-26, four agents were dispatched with
`EXPERTISE: claude-expert, orqestra-conventions`. None could load either. The artifacts were good, which
is precisely why this stayed invisible — the personas duplicate much of the step procedure and the
orchestrator's envelope carried the rest.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | A dispatched agent demonstrably receives the module's expertise content — verified by dispatching one with a probe convention that appears **only** in an expertise skill and confirming the output honours it |
| AC-2 | A dispatched agent receives the step procedure, rather than relying on its persona duplicating it |
| AC-3 | No persona instructs an action its `tools:` allowlist forbids — checked across all eight |
| AC-4 | The mechanism is stated with its reason, so the next agent added inherits it: either paths in `READ` (agents already hold `Read`) or a tool/preload grant, chosen explicitly and recorded |

## Out of Scope

§5.5's envelope contract — `docs`, TASK-015, which lands first (D-019).

Rewriting persona prose beyond the instructions that are actually unexecutable.
