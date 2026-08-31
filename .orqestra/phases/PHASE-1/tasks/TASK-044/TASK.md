---
id: TASK-044
type: task
status: pending
updated: 2026-08-31
phase: PHASE-1
module: docs
stack: markdown
origin: feature
bug:
depends_on: []
serves: [PHASE-3/SC-1]
attempts: 0
---

## Goal

**Two statements in the specification are false, and one of them is a count TASK-033 already removed
everywhere else.**

| where | what it says | why it is wrong |
|---|---|---|
| §13:1922 | "all 20 templates" | `check-templates.py` reports **21**. TASK-033 removed every hard-coded skill count for exactly this reason and did not reach the template count |
| `D-029` `Constrains` | "established by the workflow, **or intake blocks** (D11)" | TASK-040 established by §8.2 decision that intake never blocks: §4.4.3 has no fitting `blocked_reason`, and a block has no artifact to live in since `BUG.md` is the only thing intake writes |

The first is the defect class TASK-033 closed for skills, surviving one section over. The second is dead
prose in an **active** decision — a clause describing a path that cannot be taken.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | §13 asserts no template count. `ls templates/` is the count, as §7.12 already says for skills |
| AC-2 | `D-029` no longer offers a block path intake cannot take. A decision's text is not normally rewritten — say whether this is a correction in place or a superseding decision, and why |
| AC-3 | No other count or completeness claim about templates, artifacts or skills survives anywhere in `REQUIREMENTS.md` — checked by **set-difference against the tree** where the claim is an enumeration, because no grep sees a missing row, and with number-words as well as digits |
| AC-4 | Nothing renumbered; ~90 files cite §-numbers |

## Out of Scope

`templates/` and `scripts/` — `plugin`. If a count lives there too, report it.

Re-opening whether intake should block. That was settled by human decision on TASK-040; this task makes
the decision file agree with it.
