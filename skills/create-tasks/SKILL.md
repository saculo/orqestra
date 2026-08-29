---
name: create-tasks
description: "Breaks one orqestra phase into single-PR tasks, each with a type, stack, dependencies, and acceptance criteria tracing to a phase success criterion. Writes TASKS.md and a TASK.md per task. Use when a planning workflow dispatches task creation for a phase, or when the user says '/orqestra:create-tasks <N>'."
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion
disallowed-tools: Agent, Edit, NotebookEdit
---

> **Invocation**: dispatched by a planning orchestrator, or `/orqestra:create-tasks <N>`. Interactive.
> **Class**: planning

# orqestra Create Tasks

Break one phase into tasks. **One task = one PR = one coherent change a reviewer can hold in their head
at once.**

## Inputs

| Read | Why |
|---|---|
| `PHASE-N/PHASE.md` | Goal and `SC-N` success criteria — every task must serve one |
| `modules.md` | **The module registry** — every task is assigned exactly one module (§5.1, §5.2) |
| `PROJECT.md` | Stack and layout |
| `decisions/INDEX.md` | **Always read.** Settled decisions constrain what tasks are possible |
| The codebase | What already exists. Tasks that rebuild it are waste |

## Output

- **Writes**: `TASKS.md` (index) and `TASK-NNN/TASK.md` per task.
- **Templates**: `${CLAUDE_PLUGIN_ROOT}/templates/TASKS.md`, `${CLAUDE_PLUGIN_ROOT}/templates/TASK.md`.

Task numbering is **continuous across phases** — `TASK-014` follows the last task of PHASE-1. It never
resets to `TASK-001`.

## Procedure

1. Read the phase's success criteria. **Every task must cite at least one `SC-N`.** A task serving none
   is either out of scope, or evidence the criteria are incomplete — say which, do not quietly keep it.
2. Decompose into coherent changes. For each task set:
   - `module` — **the routing key** (§5.1). Exactly one, from `modules.md`. The agent, stack, and
     expertise skills all come from its row, so none of them is ever set independently — one field
     cannot disagree with itself (D7, D9). A module not in the registry is a **block**, not an
     invention: adding one is a human's call.
   - `stack` — copied from the module row as advisory context. Never chosen.
   - **One task, one module** (§5.2, D13). Work spanning the API and the web app is two tasks with
     `depends_on` ordering them. The exception that proves it: a shared interface change is still two
     tasks — define the contract in the owning module, consume it in the other.
   - `depends_on` — real ordering only. **A dependency stalls delivery until the other task is merged**
     (§7.4.1), so an unnecessary one costs real time.
   - `serves` — the `SC-N` ids.
   - `origin: feature` (bugfix promotion sets `bug` instead).
3. Write acceptance criteria as `AC-N`: observable behaviour, checkable by qa against actual behaviour.
   "Works correctly" is not a criterion; "expired sessions return 401" is.
4. **Check size** — see below.
5. Write an explicit `## Out of Scope` per task. The boundary prevents scope creep at implement more
   reliably than the goal statement does.
6. Write `TASKS.md` with the dependency order, then each `TASK.md`.
7. Verify every artifact against its schema before returning.

## Sizing

**A task is as small as it can be and as big as it needs to be.** No points, no estimates. The test is
coherence: one change, one reviewer, one PR.

The practical signal is **acceptance criteria count**. Past roughly five `AC-N`, a task is usually two
tasks wearing one name — and the cost is concrete: one oversized PR, one review that misses things, and
a rework loop that churns because each attempt fixes some criteria and breaks others.

**When a task is too big, split it — never shrink the criteria.** Dropping an `AC` loses the
requirement; splitting keeps all of them and orders them:

```
TASK-007  (8 AC, spans the store and the API)
   ↓
TASK-007a  session store        AC-1..AC-4   depends_on: []
TASK-007b  session API surface  AC-5..AC-8   depends_on: [TASK-007a]
```

- **Every `AC` from the original lands in exactly one part.** None dropped, none duplicated.
- The parts carry `depends_on` in the order the work must happen, so the dependency gate enforces the
  sequence rather than trusting anyone to remember it.
- Each part still cites an `SC-N`. A part serving none means the criterion was wrong, not the split.

## Return

```
SKILLS:  <the SKILL and EXPERTISE names you invoked, or `none`>
STATUS:  done | blocked
OUTCOME: <n> tasks for PHASE-<N>
TASKS:   <id: title (module) → SC-N>   one line each
ORDER:   <the dependency chain>
SCHEMA:  ok
SPLIT:   <any task split, and why>   # omit if none
```

This is the tasks gate summary. A human approves the decomposition from these lines.

## When you cannot proceed

| Condition | `blocked_reason` |
|---|---|
| Phase success criteria are untestable or contradictory | `contradictory-input` |
| The phase cannot be delivered as scoped | `criterion-unsatisfiable` |

## Rules

1. **Every task cites an `SC-N`.** No orphan tasks.
2. **One task, one module** (§5.2, D14). A task needing two agents is two tasks.
3. **Never invent a module.** Not in `modules.md` → block (D11).
4. **Depend only on real ordering.** Every dependency is a delivery stall.
5. **Never invent scope the phase does not describe.** If something is missing, say so — do not add it.
6. Acceptance criteria are observable behaviour, always.
7. Ids are `max(existing) + 1`, global, never reset per phase (D8).
