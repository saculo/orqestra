---
name: bugfix
argument-hint: "[description]"
description: "Investigates a bug in an orqestra-managed project — reproduces it, diagnoses the root cause with evidence, promotes it to a normal task, then plans and designs the fix. Stops at design; the fix is delivered by the standard task pipeline. Use when the user says '/orqestra:bugfix', reports a bug, or asks to investigate a defect."
allowed-tools: Read, Glob, Grep, Skill, Agent, AskUserQuestion, Bash
disallowed-tools: Write, Edit, NotebookEdit
---

> **Arguments**: `/orqestra:bugfix [description]` — interactive when omitted.
> **Class**: orchestrator+

# orqestra Bugfix

You investigate a bug and hand back a designed fix. **You do not fix it.**

Like every planning workflow, you stop at design (§1.1). The fix is delivered by
`/orqestra:task <ID>` — the same pipeline as a feature, with qa, review, PR, and PR comments.

## Arguments

`$ARGUMENTS` is an optional bug description.

**When empty**: gather the report interactively at intake.

## Steps

| step | file | dispatches | gate |
|---|---|---|---|
| intake | `step-intake.md` | — | no |
| reproduce | `step-reproduce.md` | the touched module's agent | no |
| diagnose | `step-diagnose.md` | `analyst` | **yes** |
| promote | `step-promote.md` | `create-task` | no |
| plan-design | `${CLAUDE_PLUGIN_ROOT}/skills/greenfield/step-plan-design.md` | `plan`, then `design` | **yes** |
| handoff | `step-handoff.md` | — | no |

`skills/greenfield/step-plan-design.md` is the **shared file** (D1) — referenced, not
copied.

## Intake

Write `work/BUG-NNN/BUG.md`: the report, reproduction steps as given, expected vs actual, and scope.
Id is `max(existing) + 1` (D8).

## Reproduce

**No fix without a failing reproduction first.** Establish one against the current build, as an
automated test where possible.

Cannot reproduce → **block**, `blocked_reason: no-reproduction`. Ask the human for more detail. Do not
proceed on a plausible theory — a fix for an unreproduced bug cannot be verified, and qa will have
nothing to check.

## Diagnose

Dispatch `analyst` to find the **root cause with evidence** — not the symptom, and not the first
plausible-looking line. `DIAGNOSIS.md` records `## Root Cause`, `## Evidence`, `## Fix Direction`,
`## Regression Risk`.

**Gate here.** The human confirms the diagnosis before any fix is designed — this is the cheapest point
to catch a wrong theory, and the most expensive one to skip.

## Promote

Invoke `create-task` to write a normal task under the current phase:

```yaml
module: api               # routing — where the fix lands; its row names the agent
origin: bug               # provenance
bug: BUG-001              # backlink
serves: [SC-N]            # the criterion the bug violates
```

**There is no bugfix module and no bugfix agent** (§7.3.1). Routing comes from where the fix lands: a bug
in the `api` module is implemented by whatever agent that row names, exactly as a feature there would
be.

`origin: bug` is what changes downstream: `review-task` adds the `regression-risk` lens, and `qa`
requires a test that **fails against the pre-fix code**.

If the bug reveals no phase criterion is violated, the criteria are incomplete — say so at the gate
rather than inventing a criterion (D11).

## Plan and design

The shared step, for the one promoted task.

## Handoff

```
✓ BUG-001 diagnosed → TASK-023 designed

  Root cause  session TTL compared against local time, not UTC
  Fix         normalize at the boundary; 3 files
  Risk        every existing session invalidates on deploy

→ /orqestra:task TASK-023
```

## Rules

1. **Never fix anything.** Stop at design (D3).
2. **Never skip reproduction.** No repro, no fix.
3. **Never diagnose past the first plausible cause.** Evidence, or block.
4. **Route by the module the fix lands in**, never by the fact that it is a bug.
5. Never write artifacts yourself — dispatch (D1).
