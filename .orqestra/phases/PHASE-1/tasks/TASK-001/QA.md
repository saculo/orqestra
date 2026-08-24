---
id: TASK-001
type: qa
status: done
updated: 2026-08-24
task: TASK-001
result: passed
test_command: python3 scripts/check-templates.py
---

## Test Strategy

Behavioural verification of each criterion by running the checker — against the live tree, against
deliberately broken templates, and against a fixture carrying the catalogue corrections that are out of
this task's reach.

## Results

```
$ python3 scripts/check-templates.py            # live tree
checked 20 templates against §4.8.1
✘ 2 template(s) do not conform                  exit 1

$ python3 scripts/check-templates.py            # fixture with TASK-007's corrections applied
checked 20 templates against §4.8.1
✔ all templates conform                         exit 0
```

Breakage detection, three classes, each restored afterwards:

| injected | reported |
|---|---|
| `## Notes` renamed to `## Remarks` | `headings missing: ## Notes` + `headings not in catalogue: ## Remarks` |
| `## Verdict`/`## Notes` reordered | `headings out of order: expected ## Verdict → ## Findings → ## Notes, found ## Notes → ## Findings → ## Verdict` |
| `reviewer_mood: cheerful` added | `frontmatter not in catalogue: reviewer_mood` |

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | live run — all 20 schema-bearing rows located and checked, missing template reported by path | passed |
| AC-2 | live run reports `frontmatter missing:` and `frontmatter not in catalogue:` by key name | passed |
| AC-3 | breakage tests 1 and 2 — missing, extra, and out-of-order all reported distinctly | passed |
| AC-4 | all three injected breakages reported with the specific violation | passed |
| AC-5 | exit 0 on the conforming fixture, 1 on the live tree, 2 on an unreadable catalogue; `test_command` recorded | passed (against amended AC-5) |

## Issues

**AC-5 was amended at this gate**, by human decision, after the original wording proved unsatisfiable
from inside this module. What follows is the finding that prompted it, kept because the reasoning
matters more than the outcome.

**AC-5 as originally written could not be satisfied from inside this task.** Its wording requires "zero on a clean tree",
and the live tree is not clean: two catalogue defects remain, both in `REQUIREMENTS.md`, which is the
`docs` module. D14 forbids this task from touching them.

The exit-code *behaviour* is proven correct (0 on the conforming fixture, 1 on the live tree, 2 when the
catalogue is unreadable). What is unproven is the live tree being green, and that is TASK-007's
deliverable.

**This is a planning defect, not an implementation one.** TASK-007 depends on TASK-001, but TASK-001's
AC-5 depends on TASK-007 — a circular dependency that only appeared when the work was actually done. It
needed a human decision (§8.1). **Resolved**: AC-5 amended to describe the checker's exit-code contract
rather than the live tree's state. TASK-001 closes; PHASE-1 SC-5 stays unmet until TASK-007 lands,
which is the honest position — the tree is genuinely not conformant yet.

**Two defects handed to TASK-007**, both in `REQUIREMENTS.md` §4.8.1:
1. `config.md` must be marked **no common frontmatter** — the checker already supports the marker.
2. The `TASK.md` row must include `bug`.
