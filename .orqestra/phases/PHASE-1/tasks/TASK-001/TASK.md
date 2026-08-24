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
| AC-5 | The check exits non-zero on any failure and zero on a clean tree, and `config.md` records its invocation as `test_command` |

## Out of Scope

Fixing the **catalogue** where it is wrong — the catalogue lives in `REQUIREMENTS.md`, which is the
`docs` module (TASK-007). This task makes templates conform to the catalogue as written, and reports
mismatches it cannot fix from this side.

Validating real artifacts produced by a workflow. This checks templates only; artifact validation at
runtime is the orchestrator's contract check (§4.4.5).
