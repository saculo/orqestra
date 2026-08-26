---
id: TASK-015
type: review
status: done
updated: 2026-08-27
task: TASK-015
verdict: passed
lenses: [correctness, design]
required: []
review_round: 1
---

## Verdict

F-1 and F-2 are both genuinely closed, and nothing AC-1, AC-3, AC-4 or AC-5 rests on moved. The opening
sentence at 858–862 no longer asserts "same fields" — it keeps the order half in bold and hands the
field question to the table, which is now the only thing that answers it; and the table at 934–946 gains
the fourth, step-specific class (`LENSES` `ROUND`, mandatory on `review` and permitted on no other, each
with meaning, consumer and position stated) plus a closing **The list is closed** paragraph grounded in
Rule B, so every field any real envelope carries now resolves to exactly one row and an unlisted field is
a stated violation rather than silence. I re-derived that last claim independently: extracting field
names from all nine dispatch blocks in `skills/` yields fifteen names, every one of them declared. The
rework diff is three hunks, two inside §5.5 and one in §7.8.2 recorded as a `minor` deviation, all inside
the `docs` module's `paths`. F-3 and F-4 remain open below, unchanged and still `minor`; they were left
open by instruction and are not counted against this round.

## Findings

| id | severity | file:line | finding |
|---|---|---|---|
| F-3 | minor | REQUIREMENTS.md:870 | Carried forward, unchanged and deliberately deferred. `MODULE: api` with `EXPERTISE: java-expertise, test-quality` contradicts §5.1's `api` row (731), which gives `java-expertise, spring-conventions` — against the rule §5.5 itself states at 926, that `MODULE` "resolved `ROLE`, `STACK`, `EXPERTISE`, and `PATHS` from one `modules.md` row". `ROLE`, `STACK` and `PATHS` all match the row; only `expertise` diverges. The pairing is pre-existing elsewhere in the file, which is why it is not a major. |
| F-4 | minor | REQUIREMENTS.md:942 | Carried forward, unchanged and deliberately deferred. The module condition reads "the scope unit has a module — its `TASK.md`/`BUG.md` frontmatter carries `module:`", and excuses `create-phases`/`create-tasks` by name. `close-phase`'s `PHASE`-scoped `review-phase` is reached by neither clause, and `QA.md` I-1's mechanical run widens this by one: `add-phase`'s `create-phase` is hit by the same gap. Naming `templates/PHASE.md` — whose frontmatter has no `module:` key — closes both at once. |

## What Would Change This Verdict

_n/a_

## Notes

- Floor clear. Diff touches `REQUIREMENTS.md` plus this task's own `IMPLEMENTATION.md` and `QA.md` —
  nothing outside `PATHS`. The one deviation from `DESIGN.md`'s "§5.5's body is the entire write
  surface" (the §7.8.2 clause at 1445–1446) is recorded as `minor` with its reasoning, and is the right
  call: declaring `LENSES` in §5.5 while the section that owns lenses stayed silent would have left the
  same one-way link that let the field exist in `skills/` unnoticed by the spec. No active `D-NNN` is
  contradicted; D-024 remains correctly cited at 921 as the binding layer, and the new row's citations
  to §7.8.2 and §8.1 both resolve to text that says what the row claims.
- `QA.md`'s coverage map is complete against all five criteria plus three regression checks, and it did
  the thing that matters most here: it re-verified AC-1, AC-3, AC-4 and AC-5 from the file at `HEAD`
  rather than assuming the rework left them alone, and it caught the F-2 fix by *executing* the table
  over both branches (`permitted` on `review`, `VIOLATION-not-permitted` elsewhere) instead of reading
  it. Its I-1 and I-2 correctly decline to grade the two deferred findings.
- The table's "Both sit immediately after the scope field" matches `skills/task/step-review.md:17-18`,
  which is where the real envelope puts them — so the order claim is checkable and true, even though
  §5.5's own example is an `implement` dispatch and correctly shows neither field.
- Tech debt stands as recorded and belongs to TASK-019: nine `skills/` envelopes now short only
  `SKILL` plus the module four, `skills/task/SKILL.md:64`'s inline restatement, and the missing `Edit`
  in `agents/architect.md` that forced a second whole-file `Write` of a 2093-line file. It verified
  clean twice; a third round on the same mechanism is a gamble worth retiring first.
- `ORQESTRA_AUDIT.md` is still untracked at the repo root and still not in any commit here, so it is
  not attributed to this task — but someone should decide whether it belongs in the tree.
