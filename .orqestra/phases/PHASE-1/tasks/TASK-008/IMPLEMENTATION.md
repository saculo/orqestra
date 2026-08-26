---
id: TASK-008
type: implementation
status: done
updated: 2026-08-26
task: TASK-008
deviation: minor
files_changed: 1
---

## Changes

All in `scripts/check-templates.py`. Nothing under `templates/` changed — `templates/DECISION.md` is
the artifact that proves the fix, and it already conformed once it was actually examined.

**`parse_catalogue()` — the exit-2 guard (AC-3).** `SPEC.read_text()` is wrapped in `try/except OSError`,
printing `✘ cannot read the catalogue at <path>: <strerror>` to stderr and exiting 2. Covers both a
missing file and an unreadable one; the pre-existing "could not locate §4.8.1" guard already exited 2, so
the documented exit-code meanings are unchanged.

**`is_freeform()` — the exemption is read, not restated (AC-4).** The `FREEFORM = {"PRD.md"}` set is gone.
A row is free-form when its Required-headings cell starts with `none`, which is exactly what §4.8.1 says
about `PRD.md`. `parse_catalogue()` puts the result on the row as `"freeform"`; both checking loops read
that field and no longer see an artifact name. `ALIASES` and `INSTANCE_PATHS` keep their names — those map
a catalogue row to a location on disk, which the catalogue does not state, and are not exemptions.

**Both row loops — absent headings no longer mean an absent row (AC-1, AC-2).** In `main()` the
`if not row["headings"]: continue` skip is deleted; the row is counted and its frontmatter checked, and
only the heading comparison is now conditional (`if want and want != got`). `check_instance()` had the
identical `or not row["headings"]` skip in its guard, removed the same way, with its `missing_h` check
nested under `if row["headings"]`.

Verified: `python3 scripts/check-templates.py` reports **21** templates, up from 20, exit 0. Deleting
`area:` from a copy of `templates/DECISION.md` fails with `decisions/D-NNN-*.md — frontmatter missing:
area`, exit 1. A copied tree without `REQUIREMENTS.md`, and one with it `chmod 000`, both exit 2 with the
message and no traceback. `--target .orqestra` rises 54 → 78 artifacts (the 24 `D-*.md` files, all
conforming) with the same 19 pre-existing failures and no new ones.

## Deviations

| deviation | from design | what | why |
|---|---|---|---|
| minor | `## Components` names only the `main()` row loop for AC-1/AC-2 | Applied the same fix to `check_instance()`'s row loop | `## Structure` states the rule in the plural — "the checking loops consume those facts" — and `check_instance` carried the identical `not row["headings"]` skip. Leaving it would have kept 24 `D-*.md` files out of a count the checker reports as complete, which is the exact defect this task exists to close. |

## Tech Debt

- `--target .orqestra` reports 19 pre-existing non-conformances, none caused by this change: ten `TASK.md`
  missing `bug`, eight `DESIGN.md` missing `## Structure` (D-020), and `TASK-001/REVIEW.md` missing
  `required`, `review_round` and `## What Would Change This Verdict` (D-017, D-022). These are workspace
  artifacts written before those schema changes landed; `.orqestra/` belongs to no module and is not this
  task's to rewrite.
- `parse_catalogue`'s comment describes `bug?` as conditional, but the §4.8.1 row writes `bug` with no
  `?`, so the `optional` set is empty and every instance `TASK.md` is required to carry it. Fixing that
  is a catalogue edit — `docs` module, explicitly out of scope here (D14).
