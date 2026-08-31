---
id: TASK-045
type: task
status: pending
updated: 2026-08-31
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

**Four files still describe the plugin as it was before `diagnose` existed, or before D-011.**

Each was recorded as tech debt by the task that noticed it and left unfiled, which is why they are
collected here rather than found again one at a time.

| file | what it says | since |
|---|---|---|
| `templates/SKILL.template.md:24` | the `step` class is "plan, design" | TASK-034 added `diagnose` to it (§7.0:1081) |
| `templates/config.md` | no `diagnose` row in the step→skill table | TASK-033 sanctioned the skill, TASK-034 wrote it |
| `.orqestra/config.md:53,58-64` | `from the module's task_type`, plus a whole `task_type → subagent` table | **D-011 removed `task_type`** |
| `agents/analyst.md` — fixed; `agents/architect.md` | `description` says "Dispatched at the design step" | `modules.md` also routes the `docs` module's **implement** step to it — the fact TASK-029 blocked twice on |

The last one matters most: a description is what the harness reads when selecting an agent, and
TASK-034 corrected `analyst.md` for exactly this reason while leaving `architect.md`.

`.orqestra/config.md` is this workspace's own instance and belongs to **no module** (`modules.md:45-47`);
`templates/config.md` is the copy shipped to new projects. Both drifted from the spec, which
`REQUIREMENTS.md:777` is authoritative over — proven during TASK-033, since an instance can drift and
the spec cannot drift from an instance.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | `templates/SKILL.template.md`'s class table matches §7.0's, verified by comparison rather than by reading one of them |
| AC-2 | `templates/config.md`'s routing table matches §5.1.1's authoritative one, and carries `diagnose` |
| AC-3 | `.orqestra/config.md` carries no `task_type` — D-011 removed the field and nothing should branch on it |
| AC-4 | `agents/architect.md`'s `description` names the steps it is actually dispatched at, as `analyst.md`'s now does |
| AC-5 | All seven checkers and the `config.md` `test_command` chain exit 0 |

## Out of Scope

`REQUIREMENTS.md` — authoritative and correct here; these files move to meet it (D14, D-019).

Reconciling the two routing tables into one. Whether the spec should describe routing in two places is a
design question; this task makes the copies agree with their source.
