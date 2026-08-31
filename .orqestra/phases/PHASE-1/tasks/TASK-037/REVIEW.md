---
id: TASK-037
type: review
status: done
updated: 2026-08-31
task: TASK-037
verdict: passed
lenses: [correctness, design]
required: []
review_round: 1
---

## Verdict

**Passed.** The four amended criteria are met by the diff, and the two things this review had to judge
deliberately both come out defensible. The known-red `check-templates.py` is not a defect shipped: it is
the *accurate* report of a schema whose three edits (D-003) span two modules that D14 forbids one task
from crossing — the collision was named at design, resolved by D-019 with the human gate at `550a361`,
the window is symmetric (leading with `plugin` fails the same check as `frontmatter not in catalogue:
module`), it is closed by a task that already exists and already depends on this one, and **no `BUG.md`
instance exists anywhere in the repository** (`templates/BUG.md` is the only one), so the inconsistent
schema misroutes nothing during the window — it only makes visible a gap that was already there and
unchecked. That is TASK-030's precedent applied correctly: a red left visible with its cause recorded,
with no skip-list, no exemption marker, and no `module?` softening. The `decisions/INDEX.md` edit is
inside `.orqestra/`, which `modules.md` places in **no** module by construction ("workspace state that
workflows write as they run"), so it is not an out-of-paths change; it closes an instance a design step
structurally cannot close, and the class is filed as TASK-041. The single finding below is `minor` and
belongs to TASK-040's own design step.

## Findings

| id | severity | file:line | finding |
|---|---|---|---|
| F-1 | minor | `.orqestra/phases/PHASE-1/tasks/TASK-040/TASK.md:44` | TASK-040's AC-3 is **disjunctive** where D-029 is not. It permits "whatever intake writes in one is consistent with the other, **or** the prose stops carrying the module"; D-029's second constraint (`D-029-a-bug-carries-its-module.md:38`) says flatly "`## Scope` in `templates/BUG.md` **stops** carrying the module. A rule written in two places is one that will disagree with itself." The first branch of that `or` is an outcome the decision forbids, and it is precisely the two-places state D-029 exists to end. The binding still holds — a decision outranks a task AC and TASK-040's implementer reads `INDEX.md` — so this is advisory, not an attempt: TASK-040's design step should drop the branch rather than TASK-037 reworking anything. |

## What Would Change This Verdict

_n/a_

## Notes

**The floor, all four checks.**

1. *Paths.* `REQUIREMENTS.md` is in `docs`'s `paths`. Everything else in the diff is under `.orqestra/`,
   which `modules.md` assigns to no module deliberately. `README.md` is in `paths` and does not exist.
   No out-of-paths file. **Not a finding**, and the reasoning is worth recording: reading the floor
   strictly enough to flag `.orqestra/` would make every task in this project a violation of it, which
   is the reading `modules.md` wrote its comment to pre-empt.
2. *`IMPLEMENTATION.md` accounts for the diff.* `deviation: none`, `files_changed: 2`, and both are
   right — `D-029` itself was written at the design step (`74f788c`, and §4.7 names `design` among the
   decision writers), so it is not an unrecorded implement-step change. The rework at `3209fbf` is
   recorded in its own section with the before/after text. Nothing in the diff is unaccounted for.
3. *Coverage map.* Below.
4. *Decision contradictions.* Below.

**Does `:930`'s generalisation overreach onto `PHASE`/`PROJECT`? No — and this is the right shape.**
`:930-931` enumerates the two carriers explicitly ("the task's under `TASK:`, the bug's under `BUG:`")
rather than asserting that every scope unit has a `module:`. `§5.5:957` is untouched and still reads
"**Must be omitted** under `PHASE` and `PROJECT` — carrying them there is a violation". D-027 is cited,
not contradicted. The generalisation is in the *sourcing rule* ("read from the unit's frontmatter, never
derived by the dispatching agent"), which is vacuously satisfied by units that carry no such key, not in
the *obligation*, which stays keyed on the scope value. Had it generalised the obligation, that would
have been a `blocker`; it did not.

**qa's method: evidence, not ceremony — with one honest limit.** The three sweeps are genuinely different
instruments, not the same one repeated: round 1 anchored on `` carr.* `module:` ``, the rework anchored on
`MODULE` / "the task's" / "the row" / `re-deriv|infer`, and round 2 read named line ranges in full
(`:707`, `:877`, `:239`, `:1210-1247`, `§5.5.1`, `:1466`, `:1598`, `:403`, `:1767`). The third sweep's
selection principle is stated and correct — both earlier sweeps were **rule-shaped** greps and could not
reach a constraint stated in a narrative or an example, which is exactly the surface class that hid this
contradiction in the first place. Round 2 was also right to distrust round 1's own red: it re-read
`check-templates.py`'s full output rather than the rework's claim about it, because round 1 had caught a
second red hiding behind the familiar one. The limit worth naming: AC-3 and AC-4 rest on *readings*,
which are not independently reproducible the way an exit code is. I spot-verified the load-bearing ones
myself — `:584`, `:930-936`, `:957`, `:795`, `:739`, `:707` — and each holds as QA.md describes. AC-1 and
AC-2 have machine assertions behind them (`check-templates.py` parsing the row and naming `module` as the
one delta; `check-decisions.py` exit 0 over 29). qa added no test files, correctly: `scripts/` is
`plugin`, outside this module's `paths`. So the coverage map is real, and the criteria as amended are
proved rather than asserted.

**qa failing this task at round 1 was correct, and the defect was real.** `:930` as written named the task
as `MODULE`'s only source while `§5.5:957` obliges `MODULE` under `BUG` and a `BUG` dispatch is composed
before promote — a conformant envelope with no defined source for a mandatory field. AC-3's whole point is
internal consistency, so that was a genuine AC-3/AC-4 failure and not a stylistic one. The repair
generalised rather than special-cased, which is the better fix.

**D-029 binds TASK-040 adequately.** Four forward obligations, each checkable, and it does explain the
asymmetry the task most needed explained: `PHASE` and `PROJECT` omit `module:` not because they are large
units but because they **route no module-scoped work**, and the stated test — "whether the unit routes one
module's work" — answers D-027's open question for the next scope unit as well as for this one. That is a
decision doing what `**Constrains:**` is for rather than restating its own `Why`. Only F-1 is loose, and
it is loose in TASK-040's text, not in D-029's.

**§5:717 — I agree with qa that it is out of scope, and it needs a task.** `:717` says the orchestrator
"reads the routing table in `config.md`" while `:209`, `:727` and `:930` all make `.orqestra/modules.md`
the registry. It is a real defect and it is inside `docs`'s `paths`. But AC-4 hunts *"the version that
turns out to be wrong"*, and that version is "a bug does not carry `module:`" — not "the registry lives in
`config.md`". `git log -L 717,717` puts it in `a660327`, the initial workspace commit; this diff neither
introduced it nor touched it. Charging it here would be reviewing the file rather than the change.
Recording it here because nothing else does: TASK-041 covers the INDEX gap, not this, so `:717` is
currently an observed defect with **no task filed against it**, and it will evaporate when this branch
merges unless someone files one.

**`.orqestra/config.md:34-40` is stale and correctly not fixed here.** It claims `check-envelopes.py` is
"red BY DESIGN" on `step-diagnose.md`; run directly it exits 0 (TASK-034 closed that), while a *different*
check is now red. The comment has become the thing it was written to prevent — a familiar red masking an
unfamiliar one. `plugin`, outside `docs`'s `paths`, and already folded into TASK-040 as AC-5 by human
decision, with the record duplicated in `IMPLEMENTATION.md`'s Tech Debt so it survives if that fold does
not. Right disposition.

**`scripts/test-check-templates.py`'s 3-of-15 red** is the same window and self-closes with it; it is
absent from `config.md`'s `test_command`, which is why nobody had run it. Recorded as tech debt against
TASK-040. The observation that TASK-040's AC-1 currently names only the checker and should name this test
too is correct and worth carrying into TASK-040's design — noted rather than filed, since it is one
sentence in a task not yet started.
