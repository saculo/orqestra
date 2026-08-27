---
id: TASK-015
type: task
status: pending
updated: 2026-08-26
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

**Fix the dispatch envelope so the layers it advertises actually arrive.**

Two defects, one contract.

**`EXPERTISE` passes names an agent cannot resolve.** §5.5 says "`EXPERTISE` names skills the agent
loads first", and all eight personas instruct the agent to load them "before starting". No agent holds
the `Skill` tool, so none can. Every agent has `Read`, so passing **paths** closes the gap with no tool
change and matches the envelope's own "paths, never contents" doctrine — the same argument that keeps
artifact bodies out of the orchestrator.

**Most envelopes omit required fields.** §5.5 fixes the field order, but the qa and review envelopes in
§7.4 omit `MODULE`, `PATHS`, and `STACK`, and the planning envelopes omit `EXPERTISE`. The reviewer is
required to check the diff against the module's `paths` (§5.2, D2) — with no `PATHS` in its envelope it
cannot do so deterministically, and in the TASK-008 run I had to add the field by hand for the check to
happen at all.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | §5.5 defines `EXPERTISE` as skills the agent **invokes**, and states the precondition that makes it possible: `Skill` must appear in the agent's `tools:`, which is the binding layer (D-024). The contract names its own requirement rather than assuming it |
| AC-2 | §5.5 states which fields are mandatory in **every** envelope and which are step-specific, so an omission is a contract violation rather than a judgement call |
| AC-3 | §5.5's own envelope example carries every field it declares mandatory — today it omits `MODULE` and `PATHS`, neither of which appears anywhere in `REQUIREMENTS.md` |
| AC-4 | The envelope names the **step skill**, so a dispatched agent executes the procedure rather than relying on its persona duplicating it |
| AC-5 | §5.5 records why the step skill is invoked rather than read: `${CLAUDE_PLUGIN_ROOT}` expands at invocation and **not** on `Read`, so a path-read skill carries dead `TEMPLATE:` references |

<!-- AMENDED 2026-08-26, by human decision, after the plan.

     AC-3 was mis-scoped BY ME at filing: it named §7.3/§7.4/§7.5, which contain step
     listings and no envelopes. The nine real envelopes are in `skills/` — `plugin`, so
     TASK-019's, not this task's (D14). AC-3 now covers the one envelope the spec actually
     contains, which turned out to be defective in the same way.

     AC-1 was reversed. It required EXPERTISE to pass PATHS, on the reasoning that agents
     hold `Read` but not `Skill`. The decision taken instead is to grant agents `Skill`,
     which makes names correct again — so the criterion now requires the spec to state the
     PRECONDITION rather than to work around its absence.

     AC-5 is new, from evidence this session: invoking a skill expands
     ${CLAUDE_PLUGIN_ROOT}; reading the file does not. That single fact is what rules out
     the cheap path-read fix, and it belongs in the spec so nobody re-derives it. -->

## Out of Scope

`agents/*.md` and `skills/` — `plugin`, delivered by TASK-019 (D14), which must come second (D-019).

Whether agents should hold `Skill` at all. This task makes the envelope work with the tools agents
have; granting `Skill` is a separate call TASK-019 can raise with evidence.
