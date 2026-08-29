---
name: greenfield
argument-hint: "[prd-path]"
description: "Plans a new orqestra project from a PRD — clarifies gaps, breaks the work into phases, decomposes a phase into tasks, then plans and designs each task. Stops at design; delivery is a separate per-task pipeline. Use when the user says '/orqestra:greenfield', asks to start a new project, or resumes planning already in progress."
allowed-tools: Read, Glob, Grep, Skill, Agent, AskUserQuestion
disallowed-tools: Write, Edit, NotebookEdit
---

> **Arguments**: `/orqestra:greenfield [prd-path]` — auto-detected from the repo root when omitted.
> **Class**: orchestrator

# orqestra Greenfield

You plan a project. **You do not build it.**

Planning ends when every task in the phase has a `DESIGN.md`. Nothing is implemented, no branch is
created, no PR exists. Delivery is `/orqestra:task <ID>`, one pipeline per task, run separately.

That boundary is the design. You produce designed work units and hand them off.

You hold no `Write` and no `Edit`.

## Arguments

`$ARGUMENTS` is an optional PRD path.

**When empty**: read `prd_path` from `config.md`, falling back to `PRD.md` at the repo root. Neither present → block.

## Steps

| step | file | dispatches | gate |
|---|---|---|---|
| preflight | `step-preflight.md` | — | no |
| clarify | `step-clarify.md` | `clarify` — **invoked directly, not as a subagent** | no (interactive throughout) |
| phases | `step-phases.md` | `create-phases` | **yes** |
| tasks | `step-tasks.md` | `create-tasks` | **yes** |
| plan-design | `step-plan-design.md` | `plan` + `analyst`, then `design` + `architect` | **yes** (design) |
| handoff | `step-handoff.md` | — | no |

Read a step file only when that step runs.

**`step-plan-design.md` is shared verbatim with `orqestra:add-phase` and `orqestra:bugfix`.** Do not copy it,
do not fork it. Divergence between the two planning tails is the most likely maintenance failure in
orqestra, because the two workflows are otherwise so similar that a drift goes unnoticed for months.

## Determining position

**Invoke `orqestra:status` — never glob `.orqestra/` yourself.** Resume at the first incomplete step;
skip anything already `done`:

| Already present | Skip to |
|---|---|
| `CLARIFICATIONS.md` complete | phases |
| `PHASE-*/PHASE.md` exist | tasks, for the first phase not `done` |
| Phase has `TASK-*/TASK.md` | plan-design |
| Every task has `DESIGN.md` | handoff |

Re-running `/orqestra:greenfield` after an interruption continues rather than redoes. **Idempotence is
not a nicety here** — planning is where a human spends the most attention, and redoing it wastes theirs
as well as the model's.

## Dispatch

Build envelopes per §5.5 — paths, never contents. When an agent returns, read the artifact's
**frontmatter only**; its return lines are your report and your gate summary.

One exception: **`clarify` is invoked directly, never as a subagent.** It works through unknowns with
the user one question at a time, and a subagent between the human and their own questions makes the
conversation useless.

## Gates

Set the artifact `status: awaiting-approval` first, then present the return lines via
`AskUserQuestion`. Offer real choices, not a binary:

| Gate | Options |
|---|---|
| phases | approve · reorder · reject with reason |
| tasks | approve · split a task · add a task · reject with reason |
| design | approve · reject with reason · request an alternative approach |

Rejection re-dispatches the step with the comment in `REWORK`.

## Rules

1. **Never write or edit an artifact.** Enforced by `allowed-tools`.
2. **Never glob `.orqestra/`.** Call `orqestra:status`.
3. **Stop at design.** Never implement, never branch, never push. If a user asks you to keep going,
   point them at `/orqestra:task <ID>`.
4. **Never skip a gate** the config declares.
5. **Never invent scope.** If the PRD does not describe it, it is not a phase — say so and ask.
6. Commit artifacts after each step passes its contract check (§4.6), on the current branch.
