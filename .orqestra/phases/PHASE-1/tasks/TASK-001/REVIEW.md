---
id: TASK-001
type: review
status: done
updated: 2026-08-25
task: TASK-001
verdict: passed
lenses: [correctness, design]
---

## Verdict

Passed. The checker does what AC-1..AC-5 (as amended) ask and what DESIGN.md specified: `parse_catalogue()`,
`read_template()` and `main()` are all present with the designed responsibilities, the catalogue is parsed
at run time rather than restated, and the three violation classes required by AC-3/AC-4 — missing heading,
extra heading, wrong order — are reported distinctly and by name (`scripts/check-templates.py:193-202`).
The exit-code contract of AC-5 holds on its primary paths. Three defects remain, none of them rework for
this task: two are cosmetic-to-narrow, and the third has its root cause in the `docs` module, which D14
puts out of this task's reach — the same disposition the two catalogue defects already received.

## Findings

| id | severity | file:line | finding | required |
|---|---|---|---|---|
| F-1 | major | `scripts/check-templates.py:175-178` | The "catalogue declares no headings" exemption skips the row *entirely*, so frontmatter is never compared either. `decisions/D-NNN-*.md` declares required keys (`area` `supersedes` `superseded_by` + common) and `templates/DECISION.md` is consequently never checked against them — a declared schema the conformance gate cannot see. Not required here: the row is unparseable only because the catalogue writes its headings as `# D-NNN — <title>` plus bold labels rather than `##`, which is a catalogue defect in `REQUIREMENTS.md` §4.8.1 and belongs with the other two handed to TASK-007 (D14). Once the row is corrected the skip stops firing on its own; the frontmatter/heading skips should be split at the same time. | no |
| F-2 | minor | `scripts/check-templates.py:42` | AC-5 says exit 2 "when the catalogue cannot be read", but only a *missing §4.8.1 section* produces it. An absent or unreadable `REQUIREMENTS.md` raises `FileNotFoundError` from `SPEC.read_text()` and exits 1 with a traceback — precisely the conflation DESIGN.md:27-28 separates exit 2 to avoid ("the rules are unreadable" reported as "the templates are wrong"). Narrow in practice: `SPEC` is derived from `__file__`, so cwd cannot trigger it. | no |
| F-3 | nit | `scripts/check-templates.py:34,171` | `FREEFORM = {"PRD.md"}` hard-codes a name the catalogue already expresses — the PRD row declares `none` for both frontmatter and headings, so the "no headings" skip would cover it. This is the one place the implementation restates the catalogue instead of reading it, against DESIGN.md:41 ("each expressed *in the catalogue* rather than hard-coded"). Harmless today; it becomes a second source of truth if another row is ever declared free-form. | no |

## Notes

- Outside the lenses and outside this diff: the `--target` instance-check mode (`scripts/check-templates.py:87-152`)
  was added later by TASK-003, not by `ac6af7d`. It is reviewed with that task, but one thing is worth
  passing along — `check_instance` returns 2 for a missing workspace (`scripts/check-templates.py:104-105`),
  which overloads the exit code DESIGN.md:24 reserves for "the catalogue could not be read".
- The module boundary is clean. `ac6af7d` touches `scripts/check-templates.py` inside `plugin`'s PATHS;
  the `.orqestra/` files in the commit are workspace state and out of review scope per the task brief.
  The `modules.md` correction that gave `scripts/` a home is declared as a deviation
  (`IMPLEMENTATION.md:24`) and is the right call — the deliverable had no module to live in otherwise.
- Both TASK-007 debts recorded at `IMPLEMENTATION.md:28-33` now appear satisfied in the catalogue at HEAD:
  the `config.md` row carries the **no common frontmatter** marker and the `TASK.md` row includes `bug`.
  Worth confirming when TASK-007 closes, so the debt is not carried twice.
