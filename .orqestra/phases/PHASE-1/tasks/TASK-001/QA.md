---
id: TASK-001
type: qa
status: done
updated: 2026-08-24
task: TASK-001
result: failed
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
| AC-5 | exit 1 on the live tree, exit 0 on the conforming fixture; `test_command` recorded | **failed** — see Issues |

## Issues

**AC-5 cannot be fully satisfied from inside this task.** Its wording requires "zero on a clean tree",
and the live tree is not clean: two catalogue defects remain, both in `REQUIREMENTS.md`, which is the
`docs` module. D14 forbids this task from touching them.

The exit-code *behaviour* is proven correct (0 on the conforming fixture, 1 on the live tree, 2 when the
catalogue is unreadable). What is unproven is the live tree being green, and that is TASK-007's
deliverable.

**This is a planning defect, not an implementation one.** TASK-007 depends on TASK-001, but TASK-001's
AC-5 depends on TASK-007 — a circular dependency that only appeared when the work was actually done. It
needs a human decision (§8.1): amend AC-5 to describe the checker's behaviour rather than the live
tree's state, or accept TASK-001 as blocked until TASK-007 lands.
