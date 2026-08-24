---
id: TASK-001
type: task
status: pending
updated: 2026-08-24
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
depends_on: []
serves: [SC-5]
attempts: 0
---

## Goal

Every artifact in the §4.8 catalogue has a template that matches it exactly, and a conformance check
exists that proves it — mechanically, on demand.

This is first because a schema nobody can check is a schema that drifts, and because the check becomes
the project's `test_command`, which every later task needs (D-003).

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | Running the conformance check reports, for every row of the §4.8 catalogue, whether a template exists at `templates/<NAME>.md` |
| AC-2 | The check compares each template's frontmatter keys against the catalogue's required set and reports any missing or extra key by name |
| AC-3 | The check compares each template's `##` headings against the catalogue's required order and reports any missing, extra, or out-of-order heading |
| AC-4 | Deliberately breaking a template — removing a heading, adding an undeclared frontmatter key, reordering two headings — makes the check fail and name the specific violation |
| AC-5 | The check exits 0 when every template conforms, 1 on any violation, and 2 when the catalogue cannot be read; `config.md` records its invocation as `test_command` |

<!-- AC-5 amended 2026-08-24 by human decision at the QA gate. It originally required
     "zero on a clean tree", which conflated the checker with the tree it checks: the live
     tree cannot go green from inside this module, because the two remaining failures are
     catalogue defects owned by `docs` (TASK-007). That made TASK-001's completion depend
     on TASK-007 while TASK-007 depends on TASK-001 — a circular dependency that only
     surfaced once the work was done. AC-5 now describes the checker's exit-code contract,
     which is this task's actual deliverable and is proven. PHASE-1 SC-5 remains unmet
     until TASK-007 lands, which is correct: the tree really is not conformant yet. -->

## Out of Scope

Fixing the **catalogue** where it is wrong — the catalogue lives in `REQUIREMENTS.md`, which is the
`docs` module (TASK-007). This task makes templates conform to the catalogue as written, and reports
mismatches it cannot fix from this side.

Validating real artifacts produced by a workflow. This checks templates only; artifact validation at
runtime is the orchestrator's contract check (§4.4.5).
