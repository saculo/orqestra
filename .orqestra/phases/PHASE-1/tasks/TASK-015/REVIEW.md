---
id: TASK-015
type: review
status: done
updated: 2026-08-27
task: TASK-015
verdict: changes-requested
lenses: [correctness, design]
required: [F-1, F-2]
review_round: 1
---

## Verdict

The amendment lands all five design components in §5.5 with no renumbering, no collateral edit, and
no unrecorded deviation — AC-1, AC-3, AC-4 and AC-5 are met on the text as written, and the diff stays
inside the `docs` module's `paths`. AC-2 is not: §5.5 now says two contradictory things about whether
every dispatch carries every field (line 860 against the table at 936–941), and the table declares no
class for step-specific fields, so applying it to a `review` dispatch returns no verdict on `LENSES:`
and `ROUND:` — the two omissions land on exactly the clause AC-2 was written to close ("which are
step-specific … so an omission is a contract violation rather than a judgement call"). Both are
single-line corrections inside the section already open for edit.

## Findings

| id | severity | file:line | finding |
|---|---|---|---|
| F-1 | major | REQUIREMENTS.md:860 | §5.5's opening sentence — "same fields, same order, every dispatch, every workflow" — was true before this change and is false after it. The new table (939) makes `MODULE` `PATHS` `STACK` `EXPERTISE` legitimately absent from `create-phases`/`create-tasks` envelopes and calls that "conformant, not an exception". A reader who stops at the opening line concludes all twelve fields are always required; one who reaches the table concludes otherwise. D9 resolves it in the table's favour, but needing D9 to resolve a contradiction four lines wide is the judgement call AC-2 exists to remove. The **order** half of the sentence survives; the "same fields" half must yield to the table. |
| F-2 | major | REQUIREMENTS.md:936-941 | The table's classes are always / scope / conditional-on-module / re-dispatch-only. None of them is the step-specific class AC-2 names, and DESIGN.md C4 promised ("always mandatory, conditionally mandatory … or step-specific"). The consequence is live, not theoretical: `skills/task/step-review.md:17` carries `LENSES:` and `ROUND:`, `grep 'LENSES' REQUIREMENTS.md` returns 0 hits, and §7.8.2 (1436) describes lenses as selectable without ever putting them in the envelope. Applying the table to a review dispatch therefore yields verdicts on the fields it lacks and **no verdict at all** on two fields it carries — an undeclared field is neither permitted nor forbidden. Either add a step-specific class, or state that the field list is closed and an unlisted field is a violation. |
| F-3 | minor | REQUIREMENTS.md:870 | `MODULE: api` with `EXPERTISE: java-expertise, test-quality` contradicts §5.1's `api` row (731), which gives `java-expertise, spring-conventions` — against the rule §5.5 itself states at 931, that `MODULE` "resolved `ROLE`, `STACK`, `EXPERTISE`, and `PATHS` from one `modules.md` row". `ROLE`, `STACK` and `PATHS` all match the row; only `expertise` diverges. The pairing is pre-existing (709, 1521, 1708 pair it the same way, so the registry row is the outlier), which is why this is not a major — but adding `MODULE:` is what made it checkable, and the section now fails its own stated rule in its own example. |
| F-4 | minor | REQUIREMENTS.md:939 | The condition reads "the scope unit has a module — its `TASK.md`/`BUG.md` frontmatter carries `module:`", and excuses `create-phases`/`create-tasks` by name. A `PHASE`-scoped dispatch made *after* its tasks have modules — `close-phase`'s `review-phase` — is reached by neither clause. The right answer is derivable (`templates/PHASE.md` frontmatter has no `module:` key) but only from a file §5.5 never names, so the condition is not decidable "by looking at exactly one thing" as the sentence at 934 claims. Naming `PHASE.md` alongside the other two closes it. |

## What Would Change This Verdict

_n/a_

## Notes

- Floor checks all clear. Diff is `REQUIREMENTS.md` (inside `PATHS`) plus this task's own
  `IMPLEMENTATION.md`; `IMPLEMENTATION.md` records `deviation: none` and the diff bears that out
  against DESIGN.md's five components; nothing contradicts an active `D-NNN` — D-024 is cited
  correctly at 921 as the binding layer, and D-004/D2/D4/D16 all check out against their targets.
- `QA.md`'s coverage map is the strongest part of this task's record: every AC maps to an assertion
  re-derived from the file rather than from `IMPLEMENTATION.md`, the renumbering hazard is checked by
  checksum rather than by reading, and the obligation table was *exercised* against all nine `skills/`
  envelopes instead of read. F-1 through F-4 correspond to its I-3, I-4, I-1 and I-2; qa declined to
  grade them and that was correct. I differ from qa only on severity, on the two that sit on AC-2.
- `ORQESTRA_AUDIT.md` is untracked at the repo root and is not in this task's commit, so it is not
  attributed here — but it is outside `PATHS` and someone should decide whether it belongs in the
  tree at all.
- The `agents/architect.md` `Edit` gap recorded as tech debt is real and worth raising in TASK-019
  alongside the `Skill` grant: rewriting 2031 lines through `Write` to change 33 worked here and git
  proves it, but the next amendment to this file is a larger gamble on the same mechanism.
