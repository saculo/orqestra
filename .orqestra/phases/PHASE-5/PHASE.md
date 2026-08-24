---
id: PHASE-5
type: phase
status: pending
updated: 2026-08-24
phase: PHASE-5
criteria_count: 7
---

## Goal

The lifecycle closes: phases can be verified and closed, new phases added, and bugs taken from
report to merged fix — all reusing the machinery the earlier phases proved.

## Success Criteria

| id | criterion | verified by |
|---|---|---|
| SC-1 | `/orqestra:close-phase <N>` refuses while any task is unmerged, then verifies each `SC-N` against **actual behaviour** with recorded evidence | close a phase with an open PR, then with all merged |
| SC-2 | A phase with an unmet criterion does **not** advance, and `close-phase` presents the gap without proposing gap tasks | close a phase deliberately missing one criterion |
| SC-3 | `/orqestra:add-phase` refuses over an unclosed previous phase, and on success appends without renumbering any existing phase or resetting task ids | attempt over an open phase; then append and inspect ids |
| SC-4 | `/orqestra:add-phase` refuses to invent a phase the PRD never described, and asks whether to update the PRD first | request a phase absent from the PRD |
| SC-5 | `/orqestra:bugfix` takes a report through reproduction, diagnosis, and promotion to a task with `origin: bug` and `task_type` from the touched module — **never `task_type: bugfix`** | a real bug in orqestra itself |
| SC-6 | A bug that cannot be reproduced blocks with `no-reproduction` and does not proceed to diagnosis | report a bug with insufficient detail |
| SC-7 | A full second phase runs end to end — add-phase → per-task delivery → close-phase — with no hand-editing of any artifact | PHASE-6 of orqestra itself, planned and delivered by orqestra |

## Scope

`add-phase`, `bugfix` and their step files, `create-phase`, `create-task`,
`close-phase`, `review-phase`, and a README.

Little new mechanism — these are compositions of what PHASE-1 to PHASE-4 proved. That is why they are
last.

## Out of Scope

Brownfield adoption, parallel delivery, ADRs, phase learning records, size-adaptive pipelines,
parallel research fan-out, punch lists (§10, §11) — all deferred past v1.0 with their triggers
recorded.
