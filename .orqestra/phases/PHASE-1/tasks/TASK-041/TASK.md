---
id: TASK-041
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

**The design step writes a decision it cannot register, and leaves the repository red.**

`skills/design/SKILL.md` says design *"also writes: a `decisions/D-NNN-*.md` file for any choice that
constrains future tasks (§4.7)"*. It does not say who adds that decision's row to
`decisions/INDEX.md` — and design **cannot**: line 5 declares `disallowed-tools: Agent, Edit,
NotebookEdit, Bash`, so the architect can `Write` a new file but not `Edit` the index.

Observed on TASK-037, not theorised: the design step wrote `D-029`, `check-decisions.py` reported
`no row for D-029` and exited 1, and the repository was red **before implement ran**. `config.md`'s
`test_command` chains with `&&`, so a red check there stops the checks behind it from running at all.

It has worked until now because implement has happened to notice. Nothing obliges it to, and nothing
tells a reader whose job it is.

**Same family as TASK-035.** That task covers a registry naming an agent whose tools cannot perform its
step; this one covers a step whose own skill asks for work its tools forbid. Both surface only at
dispatch, and both were found by running the pipeline rather than by reading it.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | Whoever must register a decision's `INDEX.md` row is stated in the skill that has the tools to do it, so the obligation sits with a step that can discharge it |
| AC-2 | A design step that records a decision no longer leaves `check-decisions.py` red — demonstrated by the sequence, not asserted |
| AC-3 | §4.7 says the index is *regenerated* rather than hand-edited; whatever this task lands agrees with that, or says why regeneration is not what happens today |
| AC-4 | `check-decisions.py`, `check-templates.py` and `check-envelopes.py` exit 0 at the end |

## Out of Scope

`agents/architect.md`'s `tools:`. Granting the architect `Edit` at design would let it edit code while
designing, which `skills/design/SKILL.md` removes deliberately (D-024's two layers). The fix belongs in
whose *obligation* it is, not in widening a tool grant.

`REQUIREMENTS.md` §4.7 itself, unless AC-3 finds it wrong — that is `docs` (D14, D-019). Report rather
than cross.

**WIDENED BY AUDIT 2026-09-01 — finding 21.** This task fixes one instance of a general problem, and
should say which it is fixing. `design` and `clarify` both write a decision file *and* regenerate
`INDEX.md` alongside their main artifact, while the envelope exposes one `WRITE:` path and D2 permits
one; `create-tasks` writes `TASKS.md` plus many `TASK.md` files. So either these writers exceed their
envelope or the index update does not happen. Whether the answer is a declared write *set*, an explicit
transaction, or one dispatch per artifact followed by a deterministic index generator is a design
question larger than this task. Fixing the decision path without naming the pattern leaves
`create-tasks` in the same state.
