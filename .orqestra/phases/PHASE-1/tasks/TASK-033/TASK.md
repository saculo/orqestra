---
id: TASK-033
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

**The specification has no `diagnose` skill, and one row quietly says so.**

`skills/bugfix/step-diagnose.md` dispatches the analyst with `STEP: diagnose` and no `SKILL:`, because
there is no skill to name. That is the last envelope `check-envelopes.py` cannot pass, and it cannot be
fixed by inventing a value — under D-025 a `SKILL` value is **invoked**, so naming a skill that does not
exist is worse than omitting it.

Before the skill can be authored (TASK-034), the spec has to make room for it. Two places assume it is
absent:

| where | what it says today |
|---|---|
| §4.8.1:584 | `DIAGNOSIS.md`'s writer is **"`bugfix` diagnose"** — a workflow-plus-step, and the only catalogue row that names no skill. Every other row names one: `plan`, `design`, `qa`, `review-task` |
| §5.1.1 routing | the step→skill table has no `diagnose` row, so an orchestrator resolving that step finds nothing |

Found by TASK-030's plan, which blocked `needs-splitting` rather than crossing into `docs` to fix it.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | §4.8.1's `DIAGNOSIS.md` row names a skill, in the same form every other row uses |
| AC-2 | The step→skill routing table carries `diagnose`, so resolving that step yields a skill name rather than nothing |
| AC-3 | §7.3's `bugfix` walkthrough agrees with both, and no section is renumbered — citations across ~90 files depend on the numbers holding |

## Out of Scope

Authoring `skills/diagnose/SKILL.md` — that is TASK-034, which depends on this. Docs leads (D-019).

Making `check-envelopes.py` green. It stays red on `step-diagnose.md` until TASK-034 lands.
