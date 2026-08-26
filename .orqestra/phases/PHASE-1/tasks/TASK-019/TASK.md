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
| AC-4 | All eight agents hold `Skill` in `tools:`, and the choice is recorded as a `D-NNN` — the durable allowlist changed, so the next agent added inherits the reason, not just the line |
| AC-5 | Every envelope in `skills/` carries the fields §5.5 declares mandatory — the nine real dispatches, which is where TASK-015's AC-3 stops and this one starts |
| AC-6 | No persona instructs the agent to **read** a step skill as a file: `${CLAUDE_PLUGIN_ROOT}` expands only at invocation, so a path-read skill's `TEMPLATE:` lines are dead references |

<!-- AMENDED 2026-08-26, by human decision taken during TASK-015's planning.

     AC-4 was open — "either paths in READ or a tool/preload grant, chosen explicitly".
     It is now chosen: agents get `Skill`. The deciding evidence is that
     ${CLAUDE_PLUGIN_ROOT} expands at invocation and not on Read, so the cheap path-read
     option leaves every TEMPLATE: line inside a step skill unresolvable.

     AC-5 absorbs what TASK-015's AC-3 turned out not to cover: the nine envelopes live in
     `skills/`, which is this module. AC-6 records the read-vs-invoke hazard as a check. -->

## Out of Scope

§5.5's envelope contract — `docs`, TASK-015, which lands first (D-019).

Rewriting persona prose beyond the instructions that are actually unexecutable.
