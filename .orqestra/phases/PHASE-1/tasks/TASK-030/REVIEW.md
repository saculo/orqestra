---
id: TASK-030
type: review
status: awaiting-approval
updated: 2026-08-30
task: PHASE-1/TASK-030
verdict: passed
lenses: [correctness, design]
required: []
review_round: 1
---

## Verdict

The amended AC-1 and AC-2 are both met, the four floor checks pass, and the change is a faithful
implementation of D-027 rather than an interpretation of it: `check-envelopes.py:88-98` encodes
§5.5:949 clause for clause — `PROJECT` in the scope set, the conditional class keyed off the scope
key alone, and the prohibition under `PHASE`/`PROJECT` as a prohibition rather than a permission.
`skills/greenfield/step-phases.md:13` carries `PROJECT: orqestra`, a value read from
`.orqestra/config.md:2` `project:` and not invented, and the envelope learned nothing about the
checker. The one red in the suite is `skills/bugfix/step-diagnose.md` and it is the deliverable, not
a defect: under D-025 the `SKILL:` value is invoked, so a stub would be inventing a value with extra
steps — exactly what Out of Scope forbids. No allowlist, skip-list, or exemption marker exists
anywhere in `a1c5dac`; I confirmed that against the diff rather than against the claim.

## Findings

| id | severity | file:line | finding |
|---|---|---|---|

_none_

## What Would Change This Verdict

_n/a_

## Notes

**Floor check 1 — `.orqestra/config.md:33` is outside every module's `paths`, and the sanction
holds.** I verified the precedent rather than accepting it: `ac6af7d` (TASK-001, "template
conformance checker") set `test_command: python3 scripts/check-templates.py` on this same line and
shipped. `modules.md`'s registry comment states that `.orqestra/` belongs to no module *by design* —
it is workspace state, not source a task owns — so the §5.2 boundary has nothing to place this file
inside, and reading its absence as a violation would make AC-2 unsatisfiable by construction. AC-2
requires the edit, the edit is one line, and TASK.md's §8.2 amendment records the reasoning. Not a
finding. The other `.orqestra/` paths in the diff are step artifacts and the TASK-033/034 split,
which are workflow output, not module source.

**Floor check 3 — the mutation evidence is strong, and it survives being pushed on.** The eight
mutants are asymmetric in two places: `FORBIDS_CONDITIONAL` is mutated only by dropping `PROJECT`,
never `PHASE`, and `MANDATES_CONDITIONAL` only by dropping `BUG`, never `TASK`. Both gaps are covered
by cases that exist (`conditional fields under PHASE are caught`, `missing conditional class under
TASK is caught`), so the suite is not weaker than claimed — the mutant set is. More convincing than
the eight is what qa did *after* them: it identified that the prohibition branch is `if have:` and so
a partial forbidden set is a distinct path no mutant reached, then added `a single conditional field
under PROJECT is caught` and confirmed it dies under the prohibition-removed mutant. An agent grading
its own tests that finds a hole its own mutants missed is not selecting for the ways the change
happens to be right. I also confirmed independently that the design's "emit no conditional verdict
when the scope count is not one" decision is genuinely asserted, not merely crash-guarded:
`test-check-envelopes.py:42` compares `len(problems) == len(expect)`, so `no scope field is caught`
and `two scope fields are caught` assert *exactly one* problem. Mutants 1 and 3 kill by `KeyError`
from `scopes.pop()` rather than by an assertion, which is a weaker kill than the table implies, but
the count assertion covers the same ground properly.

**The repurposed case loses nothing — verified by construction, not by qa's word.** DESIGN.md's
`conformant with full conditional class` asserted `always + TASK + CONDITIONAL → []`. Under the
redefined `BASE = SCOPED + CONDITIONAL`, `minimum conformant dispatch` asserts the identical field
list and the identical expectation, so the original assertion survives verbatim under a different
name. The repurposed content is a new assertion (the `TASK`-side mirror of the `BUG` case), so the
edit is a net gain rather than a substitution. IMPLEMENTATION.md's deviation entry is accurate and
justified, not merely declared.

**I agree with qa's `## Issues` judgement, and its absence from the diff is correctly not a finding.**
Red-by-construction is the right trade: a skip-list is the same fabrication reached by a different
route, and it would silently outlive TASK-034 because nobody deletes an entry after the thing it hid
is fixed. The suggested comment beside `test_command` naming `step-diagnose.md` and TASK-034 is a good
idea and I would support it, but no `AC-N` asks for it and `config.md` is sanctioned here for the
`test_command` line only — adding unrequested prose to a file outside every module's `paths` widens
an out-of-paths edit past what licensed it. Referring it up rather than acting on it was the correct
call. It belongs to TASK-034 or to a human decision.

**Design fidelity.** `check()` keeps its signature, reads no file, and inspects no field value, as
`## Interfaces` required; the harness still imports and calls `check()` directly rather than growing
a subprocess scan. The `DELIBERATELY NOT CHECKED` docstring paragraph records the §5.5 row-4
`EXPERTISE` limit and its revisit condition beside the rule, which is what `## Decisions` asked for —
a reader who finds the checker disagreeing with row 4 finds the reason without rediscovering it.

**Not a finding, noted for the record:** the mutants were applied to a scratch copy and nothing in the
repo records them in runnable form, so the strongest evidence in `QA.md` is not reproducible from the
tree. That is the normal trade for hand-run mutation testing and no criterion asks otherwise.
IMPLEMENTATION.md's tech-debt entry (the harness docstring's "today's ten envelopes" count) is
correctly deferred under D3.
