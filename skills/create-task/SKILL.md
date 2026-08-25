---
name: create-task
description: "Creates or splits a single orqestra task — used to add one task to an existing phase, to promote a diagnosed bug into a deliverable task, and to split an oversized task into ordered dependent parts. Use when the user says '/orqestra:create-task', when a bugfix workflow promotes a bug, or when a task must be split."
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion
disallowed-tools: Agent, Edit, NotebookEdit
---

> **Invocation**: dispatched by `orqestra:bugfix` (promotion), by `close-phase` (gap tasks),
> or `/orqestra:create-task`. **Class**: planning

# orqestra Create Task

The singular counterpart to `create-tasks`. Three jobs, same output shape.

| Mode | Trigger |
|---|---|
| **add** | One task added to an existing phase |
| **promote** | A diagnosed bug becomes a deliverable task |
| **split** | An oversized task becomes ordered dependent parts |

Everything in `create-tasks` §Sizing and §Rules applies here. This skill exists for the single-task
cases, not to hold different rules.

## Inputs

| Read | Why |
|---|---|
| `PHASE-N/PHASE.md` | The `SC-N` this task must serve |
| `PHASE-N/tasks/TASKS.md` | Existing tasks — for id allocation and dependency ordering |
| `modules.md` | The module registry — the task's routing key |
| `decisions/INDEX.md` | **Always read** (D4) |
| `work/BUG-NNN/DIAGNOSIS.md` | **promote mode only** — root cause and fix direction |
| The task being split | **split mode only** |

## Output

- **Writes**: one `TASK-NNN/TASK.md`, and updates `TASKS.md`. In split mode, two task files.
- **Template**: `${CLAUDE_PLUGIN_ROOT}/templates/TASK.md`, copied literally (D16).

Ids: `max(existing across all phases) + 1`, never reset, never reused (D8).

## Add mode

As `create-tasks`, for one task. It must cite an `SC-N`. A task serving no criterion is out of scope, or
the criteria are incomplete — say which (D11).

## Promote mode

A bug becomes an **ordinary task**:

```yaml
module: api               # where the fix lands — the row names who implements it
origin: bug
bug: BUG-001
serves: [SC-2]            # the criterion the bug violates
```

The module is **where the fix lands**, and its row names the agent — there is no "bugfix engineer"
(§7.3.1). `origin: bug` is what changes downstream: `review-task` adds the `regression-risk` lens, and
`qa` requires a test that fails against the pre-fix code.

Acceptance criteria come from the **diagnosis**, not the bug report: what must be true for the root
cause to be fixed, plus the reproduction now passing. Include the regression risk from `DIAGNOSIS.md`
under `## Out of Scope` where it bounds the fix.

## Split mode

```
TASK-007  (8 AC, spans the store and the API)
   ↓
TASK-007a  session store        AC-1..AC-4   depends_on: []
TASK-007b  session API surface  AC-5..AC-8   depends_on: [TASK-007a]
```

Rules, all checkable:

1. **Every `AC` from the original lands in exactly one part.** None dropped, none duplicated — this is
   what makes splitting safe rather than a quiet loss of requirements.
2. **Suffix, never renumber** (D8) — `TASK-007a`, `TASK-007b`. The original id appears in commits and
   dependency lists already.
3. **The original goes `superseded`**, never deleted, with a note recording the split and why.
4. **Parts carry `depends_on`** in the order the work must happen, so the dependency gate (§7.4.1)
   enforces the sequence rather than trusting anyone to remember it.
5. **Each part cites an `SC-N`.** A part serving none means the criterion was wrong, not the split.
6. **Anything depending on the original** is repointed — usually to the last part, but check which part
   it actually needed.

## Return

```
STATUS:  done | blocked
MODE:    add | promote | split
OUTCOME: <id: title (module) → SC-N>
DEPS:    <what it depends on, or none>
SPLIT:   <original → parts, and the AC distribution>   # split mode only
SCHEMA:  ok
```

## Rules

1. **One task per invocation** — except split mode, which produces exactly the parts of one original (D2).
2. **Never touch a task other than the one named** (D3). Split mode touches the original and its parts,
   nothing else.
3. **There is no bugfix module or bugfix agent.** Route by where the fix lands.
4. **Never drop an acceptance criterion** to make a task fit. Split instead.
5. Block rather than guess (D11).
