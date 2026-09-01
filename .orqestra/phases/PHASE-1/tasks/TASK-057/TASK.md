---
id: TASK-057
type: task
status: pending
updated: 2026-09-01
phase: PHASE-1
module: docs
stack: markdown
origin: feature
bug:
depends_on: []
serves: [SC-7]
attempts: 0
---

## Goal

**Three skills must write more than one artifact, and D2 permits exactly one. Every one of them is
either violating its envelope or not doing its job.**

D2: *"A dispatch declares exactly one `WRITE:` path. Any write outside it is a contract violation."*
The rule is good and TASK-028 exists to enforce it. But it is not satisfiable as written by:

| skill | must write | declared |
|---|---|---|
| `design` | `DESIGN.md` **+ decision files + `INDEX.md`** | one `WRITE:` — `DESIGN.md` |
| `clarify` | `CLARIFICATIONS.md` **+ decision files + `INDEX.md`** | one artifact |
| `create-tasks` | `TASKS.md` **+ one `TASK.md` per task** | one artifact |

So each faces the same forced choice: exceed the envelope, or leave the secondary artifact unwritten.
`create-tasks` cannot avoid it — a phase of eight tasks is nine files by definition.

**TASK-041 is one instance of this and does not name the pattern.** It fixes the decision-index path
specifically, and its AC-3 asks whether the index is regenerated or hand-edited. That is the right
question for decisions and it does not reach `create-tasks`, whose secondary writes are not an index at
all. Fixing the instance without deciding the rule leaves the next compound writer to rediscover it.

**The available answers are genuinely different, and choosing is the work.**

1. **A declared write *set*.** D2 becomes "exactly one declared set", envelopes carry several `WRITE:`
   lines, and TASK-028's check compares against the set. Simple; weakens the one-owner property.
2. **One dispatch per artifact, plus a deterministic generator.** Indexes are *derived*, never written
   by an agent — regenerated from the files by a script. Keeps D2 intact, is idempotent and retryable,
   and matches §4.7's existing claim that the index is regenerated. Costs more dispatches.
3. **An explicit transaction.** A compound step declares its write set up front and is validated as a
   unit. Most expressive, most machinery.

Option 2 is the only one that also fixes the reliability problem underneath: an index maintained by
edit drifts silently, which is exactly the failure TASK-041 was filed for.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | D2 states what a step that must produce several artifacts does, so `design`, `clarify` and `create-tasks` are describable without violating it |
| AC-2 | The choice between a declared write set, per-artifact dispatch with generated indexes, and an explicit transaction is made and recorded as a decision with its reason (D-NNN) |
| AC-3 | Whatever is chosen covers **`create-tasks`**, whose secondary writes are N task files rather than an index — the case that rules out any answer built only for indexes |
| AC-4 | §5.5's envelope contract and D2 agree with each other afterwards, and TASK-028's out-of-contract check remains statable against the result |
| AC-5 | §4.7's "the index is regenerated" is either honoured or corrected, rather than left as a claim no writer implements |

## Out of Scope

**`skills/`.** `docs` (D14); the skills cite D2 and §5.5 rather than restating them, so docs leads
(D-019). Every plugin change is a follow-on task.

**TASK-041.** It stays the decision-index instance and lands on whatever this decides. This task must
not pre-empt its AC-1 by naming the registering actor.

**Building the index generator.** If option 2 is chosen, the generator is plugin work and its own task.
