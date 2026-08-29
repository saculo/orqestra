---
id: TASK-008
type: review
status: done
updated: 2026-08-29
task: TASK-008
verdict: passed
lenses: [correctness, design]
required: []
review_round: 1
---

## Verdict

Passed. All four acceptance criteria are met by the diff and each has a discriminating assertion
behind it — 13 of the 15 cases fail on pre-fix `master`, and the two that do not are the two that
were trivially true before, which `QA.md` says plainly rather than hiding. The design's actual
boundary — *catalogue interpretation lives in `parse_catalogue()`; the loops consume the row's facts
and never re-derive them from an artifact's name* — is the boundary the code holds, and the AC-4
static case enforces it on the AST of the whole script rather than on the deleted `FREEFORM`
constant, so it stays true wherever a name is reintroduced. The one recorded deviation is justified,
not merely declared. Two minor observations below; neither is worth an attempt.

## Findings

| id | severity | file:line | finding |
|---|---|---|---|
| F-1 | minor | `scripts/check-templates.py:70` | `freeform` is derived with `cells[3].lower().startswith("none")`. A headings cell that merely *opens* with the word — `none of the H2s are…`, `nonetheless…` — silently marks the row free-form and skips it **entirely**, which is the same class of unearned "checked" the task exists to remove. The sibling frontmatter parse at line 66 uses exact equality (`cells[2].lower() == "none"`); a whole-word or `none` + delimiter test here would match it. Not a defect today: `PRD.md` is the only row saying `none`, and `case_ac4_exemption_follows_catalogue` proves the flag follows the catalogue. |
| F-2 | nit | `scripts/check-templates.py:145` | `if row["headings"] and missing_h:` — `missing_h` is computed from `row["headings"]` on line 144, so it is empty whenever `row["headings"]` is, and the added conjunct can never change the branch. The equivalent guard in `main()` (line 202) *is* load-bearing, because `want != got` is true when `want` is empty and `got` is not; this one is not. Harmless, but it reads as if the two loops guard the same thing. |

## What Would Change This Verdict

_n/a_

## Notes

- **Floor, check 1 — module boundary: clean.** The diff is `scripts/check-templates.py`,
  `scripts/test-check-templates.py`, and the two `.orqestra/` artifacts. `scripts/` is in the
  `plugin` module's `paths`; `.orqestra/` deliberately belongs to no module (`modules.md`).
  `REQUIREMENTS.md` is untouched — the §4.8.1 catalogue is read-only `docs`-module input and D14 is
  respected, as `DESIGN.md` § Structure required.
- **Floor, check 2 — the record accounts for the diff.** Every hunk maps to a paragraph in
  `## Changes`. The one deviation (the AC-1 fix also landing in `check_instance()`, where the design
  scoped it to `main()`) is **justified, not merely declared**: `FREEFORM` was read by both loops, so
  AC-4 was unreachable without touching the second, and leaving its `not row["headings"]` skip in
  place would have left the exact defect AC-1 names alive there. Widening scope to *satisfy* the
  design's stated boundary is the right call, and the record says so.
- **Floor, check 3 — coverage map is honest.** Each `AC-N` resolves to a named case with a real
  assertion on exit code and output text, not on the script's internals: AC-1 breaks a frontmatter
  key in both directions and separately proves a stray `##` is *not* a failure; AC-2 asserts both the
  count and the finding naming `decisions/D-NNN-*.md`; AC-3 covers missing, unpermitted, undecodable
  and `--target`; AC-4 is behavioural (move the `none` declaration between rows and the checker
  follows) plus static. The `rows - checked == 1` assertion in `case_clean` derives its denominator
  by slicing §4.8.1 out of `REQUIREMENTS.md`, so the count cannot drift silently — that is the
  assertion that would have caught the original defect, and it is the strongest thing in the harness.
- **Floor, check 4 — no active decision is contradicted.** D-001 (no CLI in v1) holds: the script is
  dev-only and the docstring says so. D-003, D-016 and D16 are unaffected; nothing here is shipped
  runtime behaviour.
- The changed `check_instance()` behaviour has **no automated case** — `case_ac3_target_mode` exits at
  the parse guard and never reaches that loop, so the second loop's free-form and heading handling
  rests on the manual before/after diff in `QA.md`. That is a `tests`-lens observation and `tests` is
  not among my lenses; it is also not a floor gap, since no `AC-N` is about instance mode. Worth a
  case the next time that file is opened.
- `templates/DECISION.md` is now *counted* as checked, but only its frontmatter is compared — its
  declared body schema (`# D-NNN — <title>` then `**When**` `**Decision**` `**Why**` `**Constrains**`)
  is still not verified by anything. AC-1 asks for exactly this ("only the heading comparison is
  skipped"), so it is not a finding. Recorded because the residue is a smaller instance of the
  confidence gap this task closed, and a later reader should not assume the row is fully covered.
- The 88 → 113 figure in `IMPLEMENTATION.md`'s deviation row is 89 → 114 in fact, because
  `TASK-008/IMPLEMENTATION.md` was itself written between the two runs. Already found and explained by
  `QA.md`; not re-raised as a finding.
- `check-envelopes.py` exiting 1 on two envelopes owned by TASK-024/TASK-030, and the 19 pre-existing
  `--target` failures recorded as tech debt, are both outside this diff (D3, D14) and are not defects
  of this task.
