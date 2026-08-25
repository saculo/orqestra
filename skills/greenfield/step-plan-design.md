# Step — Plan and Design

**Shared verbatim by `greenfield` and `add-phase`.** Referenced, never copied.

For every task in the phase, in dependency order: `plan`, then `design`. Both produce artifacts;
neither writes code.

## The loop

For each task whose stage is below `designed`:

### 1. Plan

```
ROLE:      orqestra:analyst
STEP:      plan
TASK:      PHASE-1/TASK-007
READ:
  .orqestra/phases/PHASE-1/tasks/TASK-007/TASK.md
  .orqestra/project/PROJECT.md
  .orqestra/decisions/INDEX.md
TEMPLATE:  ${CLAUDE_PLUGIN_ROOT}/templates/PLAN.md
WRITE:     .orqestra/phases/PHASE-1/tasks/TASK-007/PLAN.md
RETURN:    at most 10 lines.
```

Read `PLAN.md` frontmatter. `status: blocked` → stop this task, continue with the next one whose
dependencies allow it. **A blocked task does not block the whole step** — planning is the one place
where working around an obstruction is correct, because nothing has been built yet.

If the return reports open questions, surface them at the design gate rather than resolving them
yourself.

### 2. Design

```
ROLE:      orqestra:architect
STEP:      design
TASK:      PHASE-1/TASK-007
READ:
  .orqestra/phases/PHASE-1/tasks/TASK-007/TASK.md
  .orqestra/phases/PHASE-1/tasks/TASK-007/PLAN.md
  .orqestra/project/PROJECT.md
  .orqestra/decisions/INDEX.md
TEMPLATE:  ${CLAUDE_PLUGIN_ROOT}/templates/DESIGN.md
WRITE:     .orqestra/phases/PHASE-1/tasks/TASK-007/DESIGN.md
RETURN:    at most 10 lines.
```

`design` may also write `decisions/D-NNN-*.md` for choices that constrain future tasks. Regenerate
`decisions/INDEX.md` afterwards so the next dispatch sees them — **a decision recorded but not indexed
is invisible**, and the next agent will re-litigate it.

## The gate

Gate **once per phase, after every task is designed** — not once per task. A five-task phase would
otherwise stop five times to ask the same kind of question, and gate fatigue is how real review
attention gets spent on the wrong things.

Present each task's design return, then:

```
▸ GATE · design · PHASE-1  (5 tasks designed)

  TASK-004  session store       3 components · persistence layer · D-004 recorded
  TASK-005  login endpoint      2 components · api + service layers
  TASK-006  logout              1 component  · api layer
  TASK-007  password reset      3 components · api + service · risk: token expiry semantics
  TASK-008  login form          2 components · auth views + form state

  [ Approve all ]  [ Reject one with reason ]  [ Request alternative for one ]
```

Rejecting one task re-dispatches `design` for that task only, then re-gates.

## On completion

Every task at stage `designed`. Continue to handoff.

**Do not implement anything.** Not the first task, not a "quick" one, not to be helpful. The
planning/delivery split is the structure of the whole tool, and the moment planning starts building,
the phase loses the gate that was supposed to catch a bad design before it became code.
