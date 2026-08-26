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
| AC-1 | §5.5 defines `EXPERTISE` as **paths** to skill files, with the reason: an agent's `tools:` allowlist is what decides what it can reach, and `Skill` is not in it (D-024) |
| AC-2 | §5.5 states which fields are mandatory in **every** envelope and which are step-specific, so an omission is a contract violation rather than a judgement call |
| AC-3 | Every envelope example in §7.3, §7.4, and §7.5 carries the mandatory fields — no example contradicts the contract it illustrates |
| AC-4 | The envelope names the **step skill's path** too, so a dispatched agent can read the procedure it is executing rather than relying on its persona duplicating it |

## Out of Scope

`agents/*.md` and `skills/` — `plugin`, delivered by TASK-019 (D14), which must come second (D-019).

Whether agents should hold `Skill` at all. This task makes the envelope work with the tools agents
have; granting `Skill` is a separate call TASK-019 can raise with evidence.
