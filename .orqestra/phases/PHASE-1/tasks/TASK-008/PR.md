---
id: TASK-008
type: pr
status: done
updated: 2026-08-29
task: TASK-008
branch: feat/TASK-008-conformance-checker-coverage
pr_number: 5
pr_url: https://github.com/saculo/orqestra/pull/5
pr_state: merged
---

## Summary

`scripts/check-templates.py` reported *"checked 20 templates"* while one of them had never been
examined. `templates/DECISION.md` was the file: its §4.8.1 catalogue row declares an H1 plus bold
labels rather than `##` headings, and the row loop read "no headings to check" as "nothing to check",
skipping the row entirely — frontmatter included.

A row declaring no `##` headings now still has its frontmatter checked; only the heading comparison is
skipped (AC-1, AC-2). An unreadable `REQUIREMENTS.md` exits 2 with a message rather than a traceback
(AC-3). `FREEFORM` is derived from the catalogue's own "none" declaration instead of a hard-coded
`{"PRD.md"}` (AC-4). Coverage is now **21 of 22 catalogue rows**, `PRD.md` alone skipped as the one
genuinely free-form row.

One minor deviation, recorded and justified: the design scoped the fix to `main()`'s row loop, but
`check_instance()` read `FREEFORM` too, so AC-4 was unsatisfiable without touching it. Both loops
changed; the instance-mode failure section is byte-identical before and after, only the count rising
89 → 114 as the 25 decision instances came into scope.

Review passed, 0 required, 2 advisory findings left unactioned.

## Commits

| commit | subject |
|---|---|
| `9a988d2` | TASK-008: implement — close the checker's coverage hole |
| `f30eada` | TASK-008: qa — passed, 4 of 4 |
| `aededea` | TASK-008: review — passed, 0 required |
| `9291c77` | TASK-008: review gate approved |

Four commits, one per pipeline step, each committed after its artifact passed its contract check
(§4.6). The source change is confined to `9a988d2`; `f30eada` adds the test harness.

## CI

`gh pr checks 5` at 2026-08-29: **no checks reported**. Merged as `ffe59d1`. The repository has no CI workflow, so this is
absence rather than pending — nothing will arrive later.

The suite was run by hand before push and is recorded in `QA.md`:

| command | result |
|---|---|
| `python3 scripts/test-check-templates.py` | 15 cases, 15 pass — **13 of the 15 fail on pre-fix `master`** |
| `python3 scripts/check-templates.py` | 21 of 22 catalogue rows checked, all conform, exit 0 |
| `python3 scripts/check-decisions.py` | 25 decisions, 0 findings, exit 0 |
| `python3 scripts/test-check-envelopes.py` | 19 obligation cases, 19 pass, exit 0 |
| `python3 scripts/check-envelopes.py` | exit 1 on two envelopes — both **TASK-024** and **TASK-030**, pre-existing and out of scope |

The 13-of-15 figure is the one that carries weight: it is what distinguishes a suite that discriminates
from one that would pass whatever the code did — the same defect class this task removes.
