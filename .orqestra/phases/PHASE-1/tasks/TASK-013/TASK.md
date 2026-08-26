---
id: TASK-013
type: task
status: pending
updated: 2026-08-26
phase: PHASE-1
module: docs
stack: markdown
origin: feature
bug:
depends_on: []
serves: [SC-5]
attempts: 0
---

## Goal

**A blocked artifact must be able to conform to its own schema.** Today it cannot.

Every workflow can block, `orqestra:status` reports `blocked_reason` as the headline, and skills set it
throughout. **No artifact template declares the field** — it appears only in `templates/SKILL.template.md`,
which is a meta-template for authoring skills, not an artifact. So a correctly blocked artifact violates
the §4.8.1 catalogue, and the conformance check that TASK-008 just sharpened would flag it.

A second vocabulary conflict rides along: the global `status` vocabulary excludes `active`, while every
`decisions/D-NNN-*.md` uses `status: active` and the catalogue's own DECISION row expects it.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | The §4.8.1 catalogue declares `blocked_reason` for every artifact type a workflow can block, and states whether it is required always or only when `status: blocked` |
| AC-2 | The `status` vocabulary is stated once, in one place, and includes every value the shipped artifacts actually use — `active` among them |
| AC-3 | `blocked_reason` values are a closed vocabulary listing the reasons the spec already names: `deps-unmerged`, `dirty-tree`, `branch-conflict`, `contract`, `max-attempts`, `design-invalid`, `push-rejected`, `gh-auth` |
| AC-4 | A blocked artifact built to the amended catalogue passes `check-templates.py --target`, verified against a hand-built fixture |

## Out of Scope

Changing `templates/*.md` or the checker — `plugin` module, TASK-023 (D14, D-019).
