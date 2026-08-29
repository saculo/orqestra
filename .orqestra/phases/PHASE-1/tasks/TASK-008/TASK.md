---
id: TASK-008
type: task
status: done
updated: 2026-08-25
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
depends_on: []
serves: [SC-5]
attempts: 0
---

## Goal

Close the coverage hole and the exit-code gap that TASK-001's review found in the conformance checker.

A checker that reports "20 templates checked" while one of them was never examined is worse than no
checker: it produces confidence that is not earned, and every later task leaned on that number.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | A catalogue row declaring no `##` headings still has its **frontmatter** checked; only the heading comparison is skipped |
| AC-2 | `templates/DECISION.md` appears in the checked count, and breaking its frontmatter makes the check fail |
| AC-3 | A missing or unreadable `REQUIREMENTS.md` exits **2** with a clear message, never a traceback |
| AC-4 | Exemptions are read from the catalogue rather than restated in the script — no hard-coded artifact names |

## Out of Scope

The §4.8.1 catalogue itself. It accurately describes `DECISION.md` as an H1 plus bold labels; the defect
is the checker treating "no headings to check" as "nothing to check" (`docs` vs `plugin`, D14).

`check_instance`'s overloaded exit 2 for a missing workspace — a separate finding, noted for TASK-003's
review, not this task.
