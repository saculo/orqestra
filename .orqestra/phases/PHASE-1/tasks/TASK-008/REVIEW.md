---
id: TASK-008
type: review
status: done
updated: 2026-08-26
task: TASK-008
verdict: passed
lenses: [correctness, design]
required: []
review_round: 1
---

## Verdict

Passed. All four criteria are met by the diff itself, not just by the report: `is_freeform()`
(`scripts/check-templates.py:34`) derives the exemption from the Required-headings cell and the
`FREEFORM` name set is gone (AC-4); the `try/except OSError` around `SPEC.read_text()`
(`scripts/check-templates.py:45`) exits 2 with a message on every unreadable shape (AC-3); and both
row loops now count a headings-less row and check its frontmatter, gating only the heading
comparison (`scripts/check-templates.py:142`, `:198`), which is what pulls `decisions/D-NNN-*.md`
into the count as the 21st template (AC-1, AC-2). The catalogue row for `DECISION.md` writes
`` `# D-NNN — <title>` `` — a single `#`, so `heads` is empty but `is_freeform` is correctly false,
which is precisely the distinction the design asked for. The diff touches one source file,
`scripts/check-templates.py`, inside module `plugin`'s `scripts/` path; the other two commits are
this task's own artifacts under `.orqestra/`.

## Findings

| id | severity | file:line | finding |
|---|---|---|---|

_none_

## What Would Change This Verdict

_n/a_

## Notes

- The `check_instance()` deviation was the right call and is correctly classified **minor**
  (`scripts/check-templates.py:130`). `DESIGN.md` `## Structure` states the rule in the plural —
  "the checking loops consume those facts" — so applying it to the second loop implements the design
  rather than departing from it; only the `## Components` table was narrower. Nothing in the
  interface, exit codes or scope moved, and leaving the identical `not row["headings"]` skip in
  `check_instance()` would have kept 24 `D-*.md` files outside a count the checker reports as
  complete — the exact defect this task exists to close. QA proved it independently (`--target`
  55 → 79, a `D-*.md` with `area:` deleted reported post-fix and invisible pre-fix), so it is not an
  unverified deviation.
- QA's `none`-exempts-frontmatter observation is correctly **not** a finding here, and belongs as
  tech debt in the `docs` module. `is_freeform` (`scripts/check-templates.py:34`) is behaving as
  `DESIGN.md` `## Decisions` specifies: a row that writes `none` is free-form, which is a different
  fact from a row that merely lists no `##` headings, and AC-1 is about the latter. The only row
  writing `none` today is `PRD.md`, whose template deliberately carries no frontmatter — checking it
  would produce a false failure. The latent risk is real but its fix is a distinct free-form marker
  in the §4.8.1 catalogue, which TASK-008's `## Out of Scope` excludes by name (D14). Worth carrying
  forward when the catalogue is next opened; it is recorded in `QA.md` `## Issues` but not in
  `IMPLEMENTATION.md` `## Tech Debt`, which is where a future reader would more likely look.
- `## Criteria Coverage` maps every AC plus the deviation, and each row cites an induced failure run
  against both the pre-fix and post-fix script — a differential that rules out probes which would
  have passed either way. AC-4 in particular was proved by moving the `none` exemption from `PRD.md`
  to `QA.md` in a throwaway catalogue and confirming the checker followed it, which is stronger than
  reading the diff for an absent constant. No criterion is claimed without evidence.
- Unchanged and correctly left alone: `ALIASES` and `INSTANCE_PATHS` still carry artifact names, but
  they map a catalogue row to a location on disk — a fact the catalogue does not state — so they are
  not the hard-coded exemptions AC-4 forbids. `check_instance()`'s overloaded exit 2 for a missing
  workspace (`scripts/check-templates.py:110`) is untouched, as the task directs.
