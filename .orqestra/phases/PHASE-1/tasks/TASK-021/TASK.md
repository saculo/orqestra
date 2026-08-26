---
id: TASK-021
type: task
status: pending
updated: 2026-08-26
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: []
serves: [SC-2]
attempts: 0
---

## Goal

**Fix `init` so the documented happy path works.** Three defects, all in one skill.

**The PRD pointer.** `init` creates `.orqestra/PRD.md` and tells the user to edit it. `greenfield`
defaults to `PRD.md` in the repository root unless `prd_path` is set, and `templates/config.md` contains
no `prd_path`. So `init → edit .orqestra/PRD.md → greenfield` — the path the tool documents — blocks
immediately on a fresh install.

**`--force` hides retained decisions.** It preserves individual `decisions/D-NNN-*.md` files but writes
a fresh empty `decisions/INDEX.md`. Every dispatch reads the index first and opens a decision file only
when a row points at it (D-006), so preserved decisions become unreachable — present on disk, absent
from every context that matters.

**`--force` replaces `modules.md`** while retaining tasks whose `module` values reference the old
registry, leaving tasks routed to modules that no longer exist.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | A fresh `init` followed immediately by `greenfield` finds the PRD with no hand-editing of `config.md` |
| AC-2 | `init --force` leaves `decisions/INDEX.md` listing every retained decision file — verified by forcing over a workspace holding several |
| AC-3 | `init --force` either preserves `modules.md` or reports every retained task whose `module` no longer resolves; it never silently orphans routing |
| AC-4 | The existing SC-3 guarantees still hold: no `.orqestra/` overwrite without `--force`, and `PRD.md` never overwritten |

## Out of Scope

Everything `init` already does correctly. This is three defects, not a rewrite.
