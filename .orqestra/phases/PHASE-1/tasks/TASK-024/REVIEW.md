---
id: TASK-024
type: review
status: awaiting-approval
updated: 2026-08-30
task: TASK-024
verdict: passed
lenses: [correctness, design]
required: []
review_round: 1
---

## Verdict

**Passed.** All four floor checks hold and both lenses are satisfied: the diff stays inside
`plugin`'s paths, `IMPLEMENTATION.md` accounts for every file in it, every `AC-N` in `QA.md`'s
coverage map has a real assertion behind it, and the shipped references obey D-026 in the shape
their location dictates. The three findings below are all `minor` — each is an imprecision in a
durable artifact or a documented limit of the checker, none is a defect in what the tree now does,
and none is worth one of three rework attempts.

## Findings

| id | severity | file:line | finding |
|---|---|---|---|
| F-1 | minor | `.orqestra/decisions/D-026-reference-shape-follows-loading.md:47` | The `**Constrains:**` bullet "Never put `${CLAUDE_PLUGIN_ROOT}` inside a `step-*.md`" is written unqualified, but the tree this decision ships in contains ten such tokens in step files — `skills/task/step-review.md:32`, `skills/task/step-implement.md:49`, `skills/greenfield/step-plan-design.md:27,55`, and six more, all `TEMPLATE:` lines D-025 already names as arriving literal. D-026's table and `**Why:**` reason only about cross-skill *references*, so the intended scope is clear from context, but the operative bullet is the line a future engineer will apply. As written it either condemns ten lines this task did not touch and did not record as known-open, or it teaches the reader that D-026 is approximate. Scope the bullet to step-file references, or name the `TEMPLATE:` lines as a known-open case owned elsewhere. |
| F-2 | minor | `scripts/check-step-refs.py:129` | The checker enforces two of D-026's three positions. A `${CLAUDE_PLUGIN_ROOT}`-qualified step reference sitting in **prose** inside a `SKILL.md` passes silently, because rule 1 fires only when `row` is true and rule 2 only inside a step file. The docstring declares this at :64–65, so it is a chosen limit rather than an oversight — but D-026's third `**Constrains:**` bullet says the checker "enforces both the existence and the shape", and `QA.md`'s AC-2 row claims consistency is "machine-checked rather than a matter of taste". For over-qualified prose it is not; the tree is correct today by hand, not by check. |
| F-3 | minor | `.orqestra/phases/PHASE-1/tasks/TASK-024/IMPLEMENTATION.md:87` | The build-continuity deviation records the authorship split accurately and names the affected files, but justifies it only as "nothing was re-derived — the design was already approved and unchanged". That answers whether the *output* changed; it does not address the convention it crosses. `claude-expert`'s Conventions section is explicit that an orchestrator holding `Write` collapses the separation "and it collapses quietly", and here the orchestrator wrote production corrections, the test harness, and the artifact grading them. The deviation is honest and I found no divergence from the design in what it produced — but it should name the convention it breaks, not only the design it preserved. |

## What Would Change This Verdict

_n/a_

## Notes

**Floor, check by check.**

1. *Paths.* Nine non-artifact files, all under `skills/` and `scripts/`. The remaining diff is this
   task's own `.orqestra/` artifacts plus `D-026` and its `INDEX.md` row, written by the design step.
   Nothing outside `plugin`'s `PATHS`.
2. *Unrecorded deviation.* `files_changed: 8` matches the diff exactly (6 in `skills/`, 2 in
   `scripts/`). The nine corrected references reconcile against `IMPLEMENTATION.md`'s table once you
   count `add-phase/SKILL.md`'s prose line as carrying two spans: 4 + 2 + 2 + 1 = 9, the same nine
   the pre-fix run reports. The two stale ownership lines are recorded. One divergence sits in prose
   rather than in the Deviations table: `DESIGN.md`'s Test Strategy specifies that "each case runs
   the real script as a subprocess against a throwaway copy", and the harness instead imports
   `check()` and `references()` via `importlib` for the unit-level cases, keeping `subprocess` for
   the direction and repository cases. `IMPLEMENTATION.md:64` states this plainly and cites
   `test-check-envelopes.py`'s precedent, so it is declared, just not tabled. Not a finding — the
   assertions it produces are on real checker behaviour, not on a stub.
3. *Every AC-N has a real assertion.* Checked case by case against `scripts/test-check-step-refs.py`,
   since qa both wrote the additions and graded them. AC-1 rests on `:86` (bare filename naming
   another skill → `missing`), `:90` (qualified path that does not exist), `:119–121` (deleting the
   shared step names **both** referencing skills) and `:156` (the repository itself). AC-2 rests on
   the four shape cases at `:95–104`, which exercise both rules in both directions. AC-3 rests on
   the exit-2 pair at `:143–150` and the total-vs-independent-count assertion at `:166`. These are
   assertions on the checker's own output and exit codes, not restatements of it. The three
   discrimination probes qa ran — the `git archive master` tree at 9 findings, the inverted straw man
   failing 10 of 23, and the orphan case — are the right probes and I have no reason to doubt them.
   One wording slip: `QA.md:38` says "3 new cases, 23 → 28"; the qa commit adds five `case()` calls,
   covering three test concerns. The 23 → 28 figures are the accurate ones and I confirmed both.
4. *No code contradicts an active `D-NNN`.* The shipped shapes obey D-026: the three index cells at
   `add-phase/SKILL.md:29,30` and `bugfix/SKILL.md:33` carry `${CLAUDE_PLUGIN_ROOT}`, and every
   corrected prose site is plugin-relative. The one contradiction I found is in D-026's own text,
   recorded as F-1.

**The 40-before-40-after argument, judged rather than counted.** The count is right — I reproduced
it independently on both revisions with a `git grep -o` over D-026's pattern: 40 on `master`, 40 on
`HEAD`. The argument that an unchanged total proves rewriting rather than deletion is weaker than
`IMPLEMENTATION.md:31` states, because a total is a sum: a deletion paired with an addition anywhere
else in `skills/` preserves it. What actually closes the gap is that the deletion set is visible —
the diff touches six files, every hunk rewrites a span in place, and none removes one. The count is
a necessary guard against the silent-zero failure, not sufficient evidence on its own, and
`test-check-step-refs.py:166` is the right place for it to live permanently.

**Design fidelity beyond the floor.** All five components in `DESIGN.md` are present and behave as
specified; the resolution table, the closed exclusion list, the two-shape finding model, and the
0/1/2 exit contract are implemented as written, including the deliberate choice to substitute `ROOT`
rather than expand the environment variable. Writing the checker first and watching it fail on the
unfixed tree is the ordering the design called load-bearing, and it was followed and evidenced.

**Two non-blocking observations on the checker, outside both lenses.** `preprocess` toggles its fence
state on any line whose first non-space characters are three backticks, so an odd number of inline
triple-backtick mentions in one file would desync the rest of it; none exists today. And shape rule 1
keys on "the line begins with `|`", which is every table in a `SKILL.md`, not only the step index —
a non-index table citing another skill's step file plugin-relative would be flagged. Neither is
reachable in the current tree.

**Explicitly out of scope and not counted against this task**, per the review envelope:
`check-envelopes.py`'s two findings and the absent `skills/diagnose/` (both TASK-030), and the
755-vs-644 mode inconsistency carried forward from TASK-019.
