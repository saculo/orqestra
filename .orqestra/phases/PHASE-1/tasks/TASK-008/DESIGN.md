---
id: TASK-008
type: design
status: done
updated: 2026-08-26
task: TASK-008
decisions: []
---

## Components

| component | serves | change |
|---|---|---|
| `main()` row loop | AC-1, AC-2 | Skip the *heading comparison* when a row declares none; never skip the row |
| `parse_catalogue()` | AC-3 | Guard a missing/unreadable `REQUIREMENTS.md` with an explicit exit 2 |
| `FREEFORM` | AC-4 | Derive from the catalogue's "none" declaration instead of a hard-coded name |

## Interfaces

Unchanged. Exit codes keep their documented meaning: 0 conforms · 1 violations · 2 catalogue unreadable.

## Structure

One area: the conformance checker in the `plugin` module's `scripts/` layer — `scripts/check-templates.py`,
an existing file being extended. Nothing else in the module changes; `templates/` is the subject under
test, not a participant.

The §4.8.1 catalogue in `REQUIREMENTS.md` is read-only input here. It belongs to the `docs` module and is
out of scope (D14) — the defect is in how the checker reads the catalogue, not in what the catalogue says.

The boundary that carries the fix: **all catalogue interpretation lives in the parsing component.** Whether
a row is free-form, and whether it declares headings, are facts the parsed row carries; the checking loops
consume those facts and may never re-derive them from an artifact's name. That is the rule AC-4 is asking
for, and hard-coding a name anywhere downstream violates it even if the criteria pass.

Order: the parse-side guard and the derived free-form flag come first, because the loop change reads the
row shape they produce.

## Decisions

- **Absent headings and absent rows are different things.** The row is still checked; only the heading
  comparison is skipped. This is the actual defect, stated as a rule so it does not recur.
- **No artifact name is hard-coded.** Every exemption is read from its catalogue row, which is what
  `DESIGN.md` claimed in TASK-001 and what F-3 showed was not true.

## Test Strategy

The checked count must rise 20 → 21. Break `templates/DECISION.md`'s frontmatter and confirm a failure
naming it. Move `REQUIREMENTS.md` aside and confirm exit 2 with a message, not a traceback.
