---
id: PHASE-2
type: phase
status: pending
updated: 2026-08-24
phase: PHASE-2
criteria_count: 6
---

## Goal

The planning layer works end to end: a PRD becomes phases, tasks, plans, and designs, with a human
gating each boundary — and it resumes correctly when interrupted.

## Success Criteria

| id | criterion | verified by |
|---|---|---|
| SC-1 | `/orqestra:greenfield` on a real PRD produces `PHASES.md`, per-phase `PHASE.md`, `TASKS.md`, per-task `TASK.md`, `PLAN.md`, and `DESIGN.md`, stopping at the phases, tasks, and design gates | a full run against a small real PRD |
| SC-2 | Interrupting the run at any point and re-invoking `/orqestra:greenfield` resumes at the next incomplete step and **redoes nothing already `done`** | interrupt at each of the 6 steps in turn; diff the tree before and after resume |
| SC-3 | Every artifact produced passes its schema contract check; a deliberately malformed one is re-dispatched once with the violation named, then blocks with `blocked_reason: contract` | inject a missing heading and a bad enum value into a step's output |
| SC-4 | A decision written by `design` appears in `decisions/INDEX.md` and is present in the next dispatch's context, and no later step re-litigates it | plant a decision mid-phase; inspect subsequent envelopes and outputs |
| SC-5 | A task naming a module absent from `modules.md` **blocks** rather than inventing one or picking an engineer | run `create-tasks` against a phase needing an unregistered module |
| SC-6 | `clarify` reaches the human directly — its questions are answered by the user, never by a subagent — and re-running with `open_count: 0` skips instead of re-asking | run with an incomplete PRD, then re-run |

## Scope

`greenfield` and its 6 step files, `clarify`, `create-phases`, `create-tasks`, `plan`,
`design`, the dispatch envelope (§5.5), gates via `AskUserQuestion`, artifact commits, and the
decisions directory.

**Dogfooding starts here.** Once SC-1 passes, PHASE-3 through PHASE-5 are planned by orqestra itself,
and this file stops being hand-written.

## Out of Scope

Implementation of anything planned. No branches, no PRs. Delivery is PHASE-3.
