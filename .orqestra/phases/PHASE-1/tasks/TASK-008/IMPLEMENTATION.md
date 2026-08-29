---
id: TASK-008
type: implementation
status: done
updated: 2026-08-29
task: TASK-008
deviation: minor
files_changed: 1
---

## Changes

All three changes land in `scripts/check-templates.py`, the existing conformance checker in the
`plugin` module's `scripts/` layer. No other file changed; `templates/DECISION.md` is the subject
under test and was not touched.

**`parse_catalogue()` — catalogue guard (AC-3).** `SPEC.read_text()` is wrapped in
`try/except (OSError, UnicodeDecodeError)`, printing `✘ could not read the catalogue at <path>: <err>`
to stderr and exiting **2**. `UnicodeDecodeError` is included alongside `OSError` because "unreadable"
covers a corrupt file as well as a missing or unpermitted one, and neither should reach a traceback.

**`parse_catalogue()` — derived free-form flag (AC-4).** Each parsed row now carries
`freeform`, computed as `cells[3].lower().startswith(FREEFORM_MARKER)` where `FREEFORM_MARKER = "none"`.
The module-level `FREEFORM = {"PRD.md"}` set is deleted. This is the boundary the design named: whether
a row is free-form is a fact the parsed row carries, derived from the catalogue's own "Required
headings" cell, and no loop downstream names an artifact.

The comment above `FREEFORM_MARKER` states the distinction the defect turned on, so it does not recur:
a headings cell opening with `none` declares **no schema at all** (`PRD.md`) and the row is skipped
entirely; a row declaring headings that are not `##` (`decisions/D-NNN-*.md` — an H1 plus bold labels)
**has a schema**, and only the `##` comparison has nothing to compare.

**`main()` template loop — headings absent ≠ row absent (AC-1, AC-2).** The `if not row["headings"]:
continue` guard is removed. Every non-free-form row is now counted and has its frontmatter checked; the
heading comparison is gated instead, at `if want and want != got:`. `decisions/D-NNN-*.md` therefore
resolves through the existing `ALIASES` entry to `templates/DECISION.md` and is checked for the first
time.

**`check_instance()` loop — the same two facts, consumed not re-derived.** `name in FREEFORM` becomes
`row["freeform"]`, and `not row["headings"]` is dropped from the skip condition and applied to the
heading comparison only (`if row["headings"] and missing_h:`). See `## Deviations`.

**Before/after evidence.** `python3 scripts/check-templates.py` reported `checked 20 templates` and now
reports `checked 21`, still `✔ all templates conform`. `--verbose` shows `✓ decisions/D-NNN-*.md` where
it previously showed nothing. (21, not 24: `templates/` holds 24 files, 22 of which are catalogue rows,
one of those free-form.)

## Deviations

| deviation | from design | what | why |
|---|---|---|---|
| minor | `## Components` scopes the AC-1 fix to the `main()` row loop | The same fix was applied to `check_instance()`'s loop | `FREEFORM` was read by both loops, so AC-4 could not be met without changing `check_instance()`. Leaving its `not row["headings"]` skip in place would have left the exact defect AC-1 names alive in the second loop, contradicting the design's own boundary that "the checking **loops**" consume the row's facts. Verified non-regressive: the failure list is byte-identical before and after; only the count rose, 88 → 113, as the 25 decision instances are now checked and all pass. |

## Tech Debt

- `check-templates.py --target .orqestra` exits 1 on **19 pre-existing artifacts**, all of them written
  before later schema changes landed: 10 `TASK.md` missing `bug`, 8 `DESIGN.md` missing `## Structure`
  (removed by D-020), and `TASK-001/REVIEW.md` missing `required`, `review_round` and
  `## What Would Change This Verdict` (added by D-017, D-022). Unchanged by this task and unrelated to
  it (D3). Backfilling those artifacts is a separate task; note that they are `.orqestra/` workspace
  state, which belongs to no module.
- The catalogue writes `bug` without the `?` conditional marker although §4.8.1's own convention makes
  it conditional on `origin: bug`. That is a `docs`-module row, out of scope here (D14), and is the
  root of 10 of the 19 failures above.
- `check_instance`'s exit 2 remains overloaded between "no workspace" and "catalogue unreadable" —
  explicitly out of scope per `TASK.md`, noted for TASK-003's review.
