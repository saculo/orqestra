---
name: add-phase
argument-hint: "[goal]"
description: "Adds a new phase to an orqestra-managed project — defines the phase and its success criteria, breaks it into tasks, then plans and designs each. Stops at design; delivery is the per-task pipeline. Use when the user says '/orqestra:add-phase', asks to start the next phase, or wants to extend a project orqestra already manages."
allowed-tools: Read, Glob, Grep, Skill, Agent, AskUserQuestion
disallowed-tools: Write, Edit, NotebookEdit
---

> **Arguments**: `/orqestra:add-phase [goal]` — interactive when omitted.
> **Class**: orchestrator

# orqestra Add Phase

Plan the next phase of a project orqestra already manages. Identical to greenfield from the phase
boundary onward — it joins the machine at a different point, it is not a different machine.

## Arguments

`$ARGUMENTS` is an optional goal for the new phase.

**When empty**: ask for it interactively via `AskUserQuestion` before anything else.

## Steps

| step | file | dispatches | gate |
|---|---|---|---|
| preflight | `step-preflight.md` | — | no |
| define-phase | `step-define-phase.md` | `create-phase` | **yes** |
| tasks | `${CLAUDE_PLUGIN_ROOT}/skills/greenfield/step-tasks.md` | `create-tasks` | **yes** |
| plan-design | `${CLAUDE_PLUGIN_ROOT}/skills/greenfield/step-plan-design.md` | `plan`, then `design` | **yes** |
| handoff | `step-handoff.md` | — | no |

`skills/greenfield/step-plan-design.md` and `skills/greenfield/step-tasks.md` are the **shared files** (D1) —
referenced, never copied. Two planning tails that drift apart is the likeliest maintenance failure in
orqestra, precisely because the workflows are similar enough that nobody notices.

## Preflight

Three checks, all must pass:

1. **orqestra-managed** — `.orqestra/config.md` exists. If not, this project was not built by orqestra
   and v1 has no adoption path (§1.3 principle 6). Say so plainly.
2. **The previous phase is closed** — its `PHASE.md` is `status: done` and `PHASE_SUMMARY.md` has
   `criteria_met: true`.

   Not closed → **stop**. Run `/orqestra:close-phase <N>` first. Planning a new phase over an unverified
   one builds on a milestone nobody confirmed was reached — and if it was not, the new phase inherits
   the gap silently.

3. **Nothing is parked** — no task is `blocked` or `awaiting-approval`. Invoke `orqestra:status`; report
   anything outstanding and stop.

## Define the phase

Invoke `create-phase` (singular). It **appends** — new `PHASE-N` at `max(existing) + 1`, and **never
renumbers finished phases** (D8), because their ids appear in commits, task frontmatter, and
`PHASE_SUMMARY.md` cross-references.

The new phase's `SC-N` criteria must be derivable from the PRD. If the work was never described there:
say so, and ask whether to update `PRD.md` and re-run `clarify` first. **Do not invent a phase the
product never asked for** (D11).

Task numbering also continues — `TASK-024` follows PHASE-1's last task (D8).

## Tasks, plan, design

The shared steps. Same gates, same rules.

## Handoff

```
✓ PHASE-2 planned — 4 tasks designed

  TASK-024  rate limiter        backend   → SC-1
  TASK-025  quota storage       backend   → SC-1, SC-2   depends_on: TASK-024
  TASK-026  quota admin API     backend   → SC-2         depends_on: TASK-025
  TASK-027  usage dashboard     frontend  → SC-3         depends_on: TASK-026

→ /orqestra:task TASK-024
```

## Rules

1. **Never renumber existing phases or tasks** (D8).
2. **Never plan over an unclosed phase.** Preflight stops it.
3. **Stop at design** (D3). Delivery is `/orqestra:task <ID>`.
4. **Never touch a previous phase's artifacts** (D3, D5). They are done and frozen.
5. Never write artifacts yourself — dispatch (D1).
