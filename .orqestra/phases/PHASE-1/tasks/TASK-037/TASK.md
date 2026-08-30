---
id: TASK-037
type: task
status: pending
updated: 2026-08-30
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

**The specification says a `BUG` carries `module:`. It does not, and a checker now enforces the claim.**

Found by TASK-033's review (F-1), verified against `templates/BUG.md`, whose frontmatter is `id`,
`type`, `status`, `updated`, `bug`, `severity` — no `module:`.

The claim appears twice and has already been built on:

| where | what it says | shipped by |
|---|---|---|
| §5.5:957 | the four module fields are "mandatory **iff** the scope key is `TASK` or `BUG` — those units carry `module:` in their frontmatter" | TASK-029 |
| §5.1.1:795 | "a `BUG` carries `module:` too, so §5.5's conditional class is mandatory there as well" | TASK-033 |

`scripts/check-envelopes.py` encodes the first (TASK-030). So a `BUG`-scoped envelope **must** carry
`MODULE`/`PATHS`/`STACK`/`EXPERTISE`, and nothing can derive them: `skills/bugfix/step-diagnose.md`
supplies four values today with no frontmatter key behind them.

**Three steps passed this.** TASK-029 wrote it, TASK-030 encoded it, TASK-033 repeated it, and every
qa and review in between passed. A false premise stated once becomes a rule, then a check.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | The specification and `templates/BUG.md` agree about whether a bug carries a module — whichever way that is resolved, one of them changes and the other is verified against it |
| AC-2 | `skills/bugfix/step-diagnose.md`'s four module fields have a stated source: either a frontmatter key that exists, or a rule saying where else they come from for a `BUG` |
| AC-3 | Whatever `check-envelopes.py` enforces matches what the spec says after AC-1, verified by running it rather than by reading |
| AC-4 | No other place in `REQUIREMENTS.md` still asserts the version that turns out to be wrong — checked by search, and by set-difference where the claim is an enumeration |

## Out of Scope

Deciding by fiat. Both resolutions are defensible — a bug is diagnosed *against* a module, so
`module:` may belong in `BUG.md`; or a bug's module is genuinely resolved elsewhere and the spec
should say where. The design step chooses, with the reason recorded.

`skills/` and `scripts/` if AC-1 resolves toward the spec — docs leads (D-019). If it resolves toward
`templates/BUG.md`, that file is `plugin` and this task splits.
