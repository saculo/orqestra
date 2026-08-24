# Step — Implement

Dispatch the engineer. This step is thin by design: the routing table decides who, the envelope tells
them what, and you read one field back.

## Resolve the triple

**One lookup, from `TASK.md.module` into `modules.md`** (§5.1). The agent, stack, and expertise all come
from that single row — never from the task's prose, never from intuition (D9). The row names the agent
directly; there is no `task_type` enum in between (§5.1.1).

```
TASK-041  module: worker
  ↓  modules.md
  | worker | services/worker | backend-engineer | python | python-expertise, celery-conventions |
  ↓
  skill      implement
  subagent   orqestra:backend-engineer (the row names it; the plugin namespace is added)
  expertise  python-expertise, celery-conventions
  paths      services/worker           (the boundary the agent may not cross)
```

A module not in `modules.md`, or an `agent` with no file in `agents/`, is a **config error** — report
it, do not pick an agent yourself (D11).
A named expertise skill that is not installed: **warn once and dispatch without it**. A missing
conventions file degrades quality; a hard failure stops delivery. Name the module and the skill so the
gap is visible.

## Dispatch

```
ROLE:      orqestra:backend-engineer
STEP:      implement
TASK:      PHASE-1/TASK-041
MODULE:    worker
PATHS:     services/worker          # you may not write outside these (D2, D3)
STACK:     python
EXPERTISE: python-expertise, celery-conventions

READ:
  .orqestra/phases/PHASE-1/tasks/TASK-041/TASK.md
  .orqestra/phases/PHASE-1/tasks/TASK-041/PLAN.md
  .orqestra/phases/PHASE-1/tasks/TASK-041/DESIGN.md
  .orqestra/project/PROJECT.md
  .orqestra/modules.md
  .orqestra/decisions/INDEX.md

TEMPLATE:  templates/IMPLEMENTATION.md
WRITE:     .orqestra/phases/PHASE-1/tasks/TASK-041/IMPLEMENTATION.md
RETURN:    at most 10 lines, per the skill's Return contract.
```

**On rework**, add the line that makes rework different from redo:

```
REWORK:    QA.md — AC-3 and AC-7 failed. Fix only those.
REWORK:    REVIEW.md — address findings F-2, F-5 only.
```

Without it the agent re-does the whole task, which is how three attempts get spent on one defect.

## On return

Read `IMPLEMENTATION.md` **frontmatter only** — `status`, `deviation`, `files_changed`. Never the body.

| Frontmatter | Do |
|---|---|
| `status: done` | Contract check, commit artifacts, continue to qa |
| `status: blocked` | Stop. Report `blocked_reason` and what a human must decide |
| `deviation: major` | Treated as blocked — the design is wrong; do not continue to qa |

Contract check failure → re-dispatch **once**, naming the specific violations. Fail again → `blocked`,
`blocked_reason: contract`.

## Report

```
▸ PHASE-1 / TASK-041 · worker · implement · backend-engineer + python-expertise, celery-conventions
✓ implement · 7 files · deviation: minor
```
