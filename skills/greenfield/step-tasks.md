# Step — Tasks

**Shared verbatim with `orqestra:add-phase`** (D1) — referenced, never copied.

Dispatch `create-tasks` for the first phase whose status is not `done`, then gate.

## Skip when already done

The phase already has `TASK-*/TASK.md` → skip to plan-design.

## Dispatch

```
ROLE:      analyst
STEP:      create-tasks
PHASE:     PHASE-1
READ:
  .orqestra/phases/PHASE-1/PHASE.md
  .orqestra/modules.md
  .orqestra/project/PROJECT.md
  .orqestra/decisions/INDEX.md
TEMPLATE:  templates/TASKS.md, templates/TASK.md
WRITE:     .orqestra/phases/PHASE-1/tasks/
RETURN:    at most 10 lines.
```

## The gate

```
▸ GATE · tasks · PHASE-1 · 5 tasks

  TASK-001  session store        api     → SC-1
  TASK-002  login endpoint       api     → SC-1, SC-2   depends_on: TASK-001
  TASK-003  logout endpoint      api     → SC-2         depends_on: TASK-001
  TASK-004  session expiry job   worker  → SC-3         depends_on: TASK-001
  TASK-005  login form           web     → SC-4         depends_on: TASK-002

  [ Approve ]  [ Split a task ]  [ Add a task ]  [ Reject with reason ]
```

**Split a task** invokes `create-task` in split mode (§7.6.1) and re-gates. **Add a task** invokes it in
add mode.

Read the dependency chain out loud before approving: **every dependency stalls delivery until the other
task is merged** (§7.4.1). A chain five deep means five sequential PRs, and that is the moment to notice
it — not at the third preflight block.

Approve → commit, continue to plan-design.
