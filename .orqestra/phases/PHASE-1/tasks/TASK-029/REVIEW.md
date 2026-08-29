---
id: TASK-029
type: review
status: awaiting-approval
updated: 2026-08-30
task: TASK-029
verdict: passed
lenses: [correctness, design]
required: []
review_round: 2
---

## Verdict

F-1 is closed by the diff itself, not by a label: `git diff master...HEAD -- agents/` is now empty,
`agents/architect.md`'s last commit is `81d4139` on `master`, and this branch is rebased onto it, so the
file has left the branch's diff entirely and the PR carries `REQUIREMENTS.md` plus this task's own
`.orqestra/` artifacts and nothing else. That is exactly the resolution the floor asks for, and it
preserves the grant — the docs module's engineer keeps the `Edit` that `modules.md:14` requires of it.
F-2 is closed prescriptively at `REQUIREMENTS.md:949`. Everything I verified by hand in round 1 survives
the rebase; the spot-checks below hold. Nothing remains that is worth an attempt.

## Findings

| id | severity | file:line | finding |
|---|---|---|---|
| F-1 | minor | `IMPLEMENTATION.md:26` | **Closed as a major; re-recorded as minor for a residue.** `## Changes` no longer claims anything about `agents/`, `files_changed: 1` is now true of the diff, and the opening line correctly scopes itself to "this step". The record accounts for what the diff did. What is stale is C2's quoted `after:` text — it still reads "Omitted under `PHASE` and `PROJECT`", one revision behind the line it documents, which now reads "**Must be omitted** … carrying them there is a violation, not a harmless extra". The substance of C2 is recorded and the intent line is still accurate, so this is a transcription drift in a quotation, not an unrecorded change. Not worth an attempt; worth a line if the file is touched again. |
| F-3 | minor | `REQUIREMENTS.md:709`, `:1590`, `:1777` | Unchanged and re-judged as still minor. All three continue to pair the `api` module with `java-expertise, test-quality`, contradicting `§5.1:731` and the now-corrected example at `:872`. This is inside my module and my lens, but outside AC-3 as amended — TASK-015's F-3 named `:870` and scoped itself there — and it is pre-existing text this task neither introduced nor made worse. A reader hitting `:709` first still learns the wrong pairing, which is why it stays recorded rather than dropped. Fold into whichever task next opens §5.1 or §11; it does not justify an attempt. |

## What Would Change This Verdict

_n/a_

## Notes

- **F-2 from round 1 — verified closed, which is why it is no longer a finding.**
  `REQUIREMENTS.md:949` now reads "**Must be omitted** under `PHASE` and `PROJECT` — carrying them there
  is a violation, not a harmless extra". That is prescriptive enough that TASK-030 encodes a stated rule
  rather than picking a reading in `scripts/`, which is the one-way link F-4 existed to close. It does
  not touch the `TASK`/`BUG` side: that clause is still "mandatory **iff** the scope key is `TASK` or
  `BUG`", unchanged in force, and `QA.md`'s three negative fixtures (`TASK`-scoped with all four
  omitted, with only `EXPERTISE` dropped, `BUG`-scoped with all four omitted) all still resolve to
  *violation* under the new wording. The reason is stated with the rule, per house convention.
- **Floor, all four, re-run on the rebased diff.** (1) `PATHS`: the diff is `REQUIREMENTS.md` plus the
  task's own `.orqestra/` artifacts — no file outside the `docs` module remains. (2) The record: F-1
  above. (3) Coverage map: unchanged from round 1, and the rebase could only have disturbed it through
  `agents/architect.md`, which no criterion depends on. Spot-checked anyway and it holds — `:872` reads
  `java-expertise, spring-conventions` in the diff itself, the `^#{2,4} ` heading diff `master` vs `HEAD`
  is byte-identical so no `§N` citation breaks, and `.orqestra/config.md:2` still carries
  `project: orqestra`, which is AC-2's value source. (4) `D-027` is active and the amendment implements
  it exactly: scope is one of four keys, and the scope key alone decides the conditional class.
- **`QA.md:I-5` is now stale.** It records the branch as carrying an 11-line `agents/architect.md`
  change under commit `d2d1a41`. True when written, false now — the rebase moved it to `master`. qa was
  not re-dispatched and had no chance to update it, so this is an artifact of ordering rather than an
  error by qa. Flagging it because a later reader of `QA.md` alone would conclude the branch still
  breaches `PATHS` when it does not.
- **The grant was deliberately not reverted, and that was right.** Reverting removes `Edit` from the
  agent `modules.md:14` names as the `docs` engineer, which is what blocked implement twice (`2e6d260`,
  `29b98db`). Re-attribution onto `master` gets the floor what it wants without re-creating the
  circularity I flagged at the round-1 gate. Recording it here so the reasoning is on the record rather
  than only in `44f1fcc`'s message.
- Design fidelity is unchanged from round 1: C1–C5 land as `DESIGN.md` specified, amended in place, no
  `§5.5.2`, no renumbering, the named-steps clause gone with no replacement list. `deviation: none` is
  accurate.
- `check-envelopes.py` still exiting 1 remains expected and correctly recorded as tech debt (D-019,
  D14). Not a finding.
