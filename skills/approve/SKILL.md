---
name: approve
argument-hint: "[comment]"
description: "Approves the orqestra step currently parked at a gate, records the approval, and resumes the workflow at the next step. Use when the user says '/orqestra:approve', or approves a gate in a session later than the one that parked it."
allowed-tools: Read, Write, Edit, Glob, Grep, Skill, Agent, Bash
disallowed-tools: NotebookEdit
---

> **Arguments**: `/orqestra:approve [comment]` · **Class**: control

# orqestra Approve

Resume the gate parked at `status: awaiting-approval`.

**This exists for one specific case: approving a gate in a *different session* from the one that parked
it.** Within a session, gates are answered directly through `AskUserQuestion` (§6.1) — an
`AskUserQuestion` call does not survive a session boundary, but `status: awaiting-approval` written to
the artifact does. That asymmetry is the whole reason this skill exists, and the reason gates write
their status to disk before asking.

## Procedure

1. Invoke `orqestra:status` to find the parked artifact. **Never glob `.orqestra/` yourself** (§7.10).
2. **Exactly one artifact should be parked.** More than one means two workflows are mid-flight, which
   D15 forbids — report both and stop rather than picking (D11).
3. Present what is being approved: the artifact's id, its step, and its stored return summary. The
   human may not have seen it — it was another session.
4. Set `status: done`, recording `$ARGUMENTS` as an approval note when given.
5. Commit (§4.6).
6. Resume the owning workflow at the next step, and say which one.

## Rules

1. **Never approve on the user's behalf.** Invoking this skill *is* the approval; do not also infer
   approval of anything else that happens to be pending.
2. **Never approve a `blocked` artifact.** Blocking is not a gate — fix the cause, then
   `/orqestra:unblock`.
3. Nothing else changes. Approval advances one step; it does not edit the artifact (§6.1).
