---
id: TASK-008
type: qa
status: done
updated: 2026-08-29
task: TASK-008
result: passed
test_command: python3 scripts/test-check-templates.py
---

## Test Strategy

This module has no test framework (`PROJECT.md` § Commands: `test` is **none yet**). Its standing
convention is a `scripts/test-<script>.py` behavioural harness — `scripts/test-check-envelopes.py` is
the precedent — so `scripts/test-check-templates.py` was added in the same shape: self-contained, run
by hand, exit 0 clean / 1 a case failed.

Every case runs the real `check-templates.py` as a **subprocess** against a throwaway copy of
`REQUIREMENTS.md` + `templates/` + the script, and asserts on exit code and output text. Nothing runs
against the working tree, so a case may break the catalogue or a template freely. `git status` after
the run confirms the tree is untouched.

The criteria here are all negative controls, and that is the point of the task: a checker that counts a
file it would pass regardless is the exact defect being removed. So each case was also run against
**pre-fix `master`** (`git show master:scripts/check-templates.py` into an identical fixture). A case
that passes both ways proves nothing about the fix. **13 of 15 cases fail against `master`**; the two
that do not are `clean tree exits 0` and `AC-1 heading comparison skipped`, both trivially true before.

AC-4 is asserted on the **AST of the whole script**, not on the `FREEFORM` constant and not on line
ranges — a name moved out of a constant and into a conditional still fails it. `ALIASES`,
`INSTANCE_PATHS`, `SPEC` and the `targets` map in `check_instance` are exempted by AST node identity:
they map a catalogue name onto a filesystem location, which the catalogue does not state. This is
discriminating, not decorative — it catches `master`'s `FREEFORM = {"PRD.md"}` at line 33.

The `IMPLEMENTATION.md` deviation (`check_instance` changed as well as `main`) was verified
independently rather than taken on the record: both revisions were run over `.orqestra/` and their
failure sections diffed.

## Results

| command | outcome |
|---|---|
| `python3 scripts/test-check-templates.py` | **exit 0** — 15 cases, 15 pass, 0 fail (15 added) |
| same, against pre-fix `master`'s script | **exit 1** — 13 of 15 fail, as required |
| `python3 scripts/check-templates.py` | exit 0 — `checked 21 templates`, all conform |
| `python3 scripts/check-templates.py --verbose` | `✓ decisions/D-NNN-*.md`; `· PRD.md: free-form … skipped` |
| `python3 scripts/test-check-envelopes.py` | exit 0 — 19 cases (untouched, no regression) |
| `python3 scripts/check-decisions.py` | exit 0 — 25 decisions conform (untouched) |
| `git status --short` | only `scripts/test-check-templates.py`, plus two pre-existing untracked files |

**Coverage denominator.** 22 catalogue rows, of which 21 are checked and 1 (`PRD.md`, the only row
declaring `none`) is skipped. Not 24: `templates/` holds 24 files, but `EXPERTISE.template.md` and
`SKILL.template.md` are skill-authoring scaffolds with no catalogue row and correctly have none. The
test derives 22 by slicing §4.8.1 out of `REQUIREMENTS.md` itself and asserts `rows - checked == 1`, so
the count cannot silently drift. Pre-fix the same fixture reports **20 of 22**.

**Deviation verified.** `--target .orqestra`, master vs branch: `checked 89` → `checked 114` (the 25
`decisions/D-*.md` instances, now checked, all pass). `diff` of the two failure sections: **identical**.
The claim in `IMPLEMENTATION.md` reads 88 → 113 because `TASK-008/IMPLEMENTATION.md` itself was written
between the two runs. Non-regressive, confirmed independently.

Both modes still exit 1 on pre-existing artifacts — 19 in `--target` mode, unchanged from master and
recorded as tech debt; `check-envelopes.py` on two envelopes owned by TASK-024/TASK-030. Both are
outside this task (D3, D14) and neither was touched.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 — a row declaring no `##` headings still has its frontmatter checked; only the heading comparison is skipped | `case_ac1_frontmatter_still_checked` (drop `area` → `frontmatter missing: area`, exit 1), `case_ac1_extra_key` (add `bogus_key` → `frontmatter not in catalogue`, exit 1), `case_ac1_heading_comparison_skipped` (append an undeclared `## …` → exit 0). All three fail on pre-fix code except the last | **pass** |
| AC-2 — `templates/DECISION.md` appears in the checked count, and breaking its frontmatter makes the check fail | `case_ac2_counted` (`--verbose` prints `✓ decisions/D-NNN-*.md`; count 20 → 21), `case_ac2_broken_frontmatter` (strip the frontmatter → exit 1, `no YAML frontmatter`, finding names the row). Pre-fix: the same stripped template passes with exit 0 — the defect, reproduced | **pass** |
| AC-3 — a missing or unreadable `REQUIREMENTS.md` exits **2** with a clear message, never a traceback | `case_ac3_missing`, `case_ac3_unreadable` (mode 000), `case_ac3_undecodable` (invalid UTF-8), `case_ac3_target_mode`. Each asserts exit 2, `could not read the catalogue at <path>: <err>` on stderr, and no `Traceback`. Also verified by hand against a directory in place of the file. Pre-fix all four traceback and exit 1 | **pass** |
| AC-4 — exemptions are read from the catalogue rather than restated in the script — no hard-coded artifact names | Behavioural: `case_ac4_exemption_follows_catalogue` moves the `none` declaration from `PRD.md`'s row to `DESIGN.md`'s and the checker follows — `DESIGN.md` is skipped, `PRD.md` is checked and fails. Static: `case_ac4_no_hardcoded_names` walks the whole script's AST for any `.md` literal outside the name→path maps. Pre-fix, the behavioural case skips *neither* row correctly and the static case flags `FREEFORM = {"PRD.md"}` | **pass** |

## Issues

_none_

One observation, not a defect: `ALIASES`, `INSTANCE_PATHS` and `check_instance`'s `targets` list still
name artifacts literally. They are name→path mappings — the catalogue states no filesystem location, so
these cannot be derived from it — they are not exemptions, and they are unchanged from `master`. AC-4's
subject is the exemption logic, and no artifact name reaches a branch anywhere in the script. Recorded
so a later reader does not mistake the grep hit for an unclosed criterion.
