---
id: TASK-007
type: design
status: done
updated: 2026-08-24
task: TASK-007
decisions: []
---

## Components

Prose, not code. The edits, each traced to a criterion:

| edit | serves |
|---|---|
| §4.8.1 — `config.md` marked **no common frontmatter**; `TASK.md` row gains `bug` | AC-1 |
| §4.8 preamble — the exemption documented, with the reason | AC-1 |
| §7.12 — inventory rebuilt from the shipped tree; 15 → 22 | AC-2 |
| §1.4, §7.0 — stale skill counts corrected | AC-2 |
| §4.7.1 — `§11.6` citation reworded (a list item is not a section) | AC-3 |
| §5.4 — agent dispatch namespacing recorded where a reader looks for it (D-014) | AC-4 |
| §4.8.4 — the `init --migrate` claim removed; no such flag exists | AC-4 |

## Interfaces

None. The spec's interface is its section numbering, and **nothing is renumbered.**

## File Plan

| path | action | purpose |
|---|---|---|
| `REQUIREMENTS.md` | modify | Every edit above |

## Decisions

- **Correct in place, never renumber.** 22 skills cite this document by section number.
- **Where spec and plugin disagree, fix whichever is actually wrong** — not whichever is easier to
  reach. Both catalogue defects were spec-side; both `no_commit` defects are plugin-side and are
  therefore reported, not fixed.
- **The exemption is documented with its reason.** An unexplained exemption gets "fixed" back by the
  next reader.

## Test Strategy

`python3 scripts/check-templates.py` exits 0. The citation and count extractions re-run clean. Every
config key resolves to a consumer, or is recorded as debt with the module that owns it.
