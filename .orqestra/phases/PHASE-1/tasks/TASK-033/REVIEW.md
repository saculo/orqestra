---
id: TASK-033
type: review
status: awaiting-approval
updated: 2026-08-30
task: TASK-033
verdict: passed
lenses: [correctness, design]
required: []
review_round: 1
---

## Verdict

**Passed.** All four amended criteria hold, and I verified the load-bearing ones independently rather
than reading qa's word for them: I ran the same set-difference myself and reproduce its result — §7.0's
class table is 23 tokens with `cls − ls skills/` = `{diagnose}` and `ls skills/ − cls` = **∅**, §7.12's
grid is set-identical to it, and `diagnose` is the sole spec-leads entry in each (D-019). No renumbering:
the diff touches no heading. The rework's class choice for `diagnose` is right, and right for a reason
stronger than its own argument — `agents/analyst.md` `tools: Skill, Read, Write, Glob, Grep` is exactly
`step`'s grant minus `Bash`, and `Bash` is correctly absent because reproduction is `step-reproduce.md`'s
job, run in the `bugfix` orchestrator which holds `Bash` (§7.0). Two minor findings, neither an AC
failure, neither worth an attempt: both are places where the new text asserts *content* that its
enumeration-level checks are structurally blind to.

## Findings

| id | severity | file:line | finding |
|---|---|---|---|
| F-1 | minor | `REQUIREMENTS.md:795` | The new justifying paragraph claims "a `BUG` carries `module:` too, so §5.5's conditional class is mandatory there as well". **`templates/BUG.md` has no `module:` field** — its frontmatter is `id type status updated bug severity`, and §4.8.1:583's own `BUG.md` row lists exactly `bug` `severity`. §7.3:1210 confirms the module is derived at *promote* ("module from the touched area"), not carried by the BUG. The paragraph's conclusion is sound and its premise is faithful to §5.5:957 (verbatim in `master`, so this task did not introduce the claim) — but §5.5:957, `templates/BUG.md` and §4.8.1:583 disagree with each other, and repeating the claim in a second place makes the disagreement harder to find, not easier. Not required: the honest fix is `templates/BUG.md` + the §4.8.1 row + the writer, three edits together (D-003), and `templates/` is the `plugin` module (D14). Filing it is the correct action, not rewording line 795 to hide it. |
| F-2 | minor | `REQUIREMENTS.md:1655` | Retitling the column `UTILITY / SETUP` "because `init` is `setup` class in §7.0" (IMPLEMENTATION R3) makes §7.12's columns read as the §7.0 class taxonomy — and on that reading the grid contradicts §7.0 twice, pre-existingly: `pr-comments` sits under **DELIVERY ORCHESTRATORS** while §7.0:1086 classes it `control`, and `close-phase` sits under **UTILITY** while §7.0:1079 classes it `orchestrator`. This is exactly the blind spot the round-2 method cannot see: the two lists are set-identical at 23 and still disagree on what a member *is*. Either the columns are a loose reading grouping (then the header should not have been derived from a class) or they are the taxonomy (then two cells are wrong). Cheap either way; not an AC failure, since AC-3 is about `diagnose`'s presence. |

## What Would Change This Verdict

_n/a_

## Notes

**Floor, all four.** Diff is `REQUIREMENTS.md` (in `PATHS`) plus this task's own artifacts and
`decisions/D-028` + `INDEX.md` — no file outside the module. `IMPLEMENTATION.md` accounts for every
hunk, including the three deviations (C7 §1.3, R1+R2 §7.0, R3 §7.12) it was not designed to touch, each
with a reason and not merely a declaration. `QA.md`'s coverage map has a real, locatable assertion
behind every AC — unusually so; I re-derived the AC-3 set-differences and the heading-count equality and
they hold. No contradiction of an active decision: §4.8.1:585 names `` `diagnose` `` bare and leaves
`` `bugfix` intake `` byte-identical, which is precisely D-028's discriminator; naming a skill the tree
does not yet have is D-019, not a D-025 violation, and Out of Scope keeps `check-envelopes.py` red until
TASK-034.

**On qa's N1 (§4.3:294 "twenty artifacts") — I agree it is out of scope.** AC-4's noun is a *skill*
count, and the amendment note scopes it the same way; §4.3:294 is unmodified by this branch and is not
one of AC-3's five sites. Leaving it is not a finding: widening a criterion at review is how a task
grows a sixth site it was never planned against. But qa is right that §4.3:294 ("twenty") contradicts
§4.8:553 ("Twenty-two", which I confirm is **correct** against 22 catalogue rows) and §13:1922 ("all 20
templates" against 21 conforming). **One follow-up task should take all three prose counts** — same
defect class, one edit.

**On the §7.12 trade — the rework made the right call.** Making the completeness claim true rather than
retracting it is stronger, because §7.12's job *is* to be the inventory and a hedged inventory has no
job. The objection that it commits the spec to a hand-maintained list forever is real but does not
favour the alternative: a prose count was *also* hand-maintained, and it went stale unnoticed twice.
What changed is that the claim is now falsifiable by a mechanical set-difference against `ls skills/`,
which a number never was. That makes **qa's N2 the thing that matters** — `scripts/check-skill-tables.py`
asserting set-equality between §7.0, §7.12 and the tree, allowing spec-leads entries. It is `plugin`
module, correctly not written here (D14), and F-2 shows the guard should compare *class agreement*, not
only membership. File it before the next skill lands, not after.

**For TASK-034, not this task.** `agents/analyst.md`'s `description:` still reads "produces PLAN.md …
Dispatched at the plan step" — a second step now dispatches it. `agents/` is outside this task's
`PATHS`; TASK-034 should widen that line when it authors `skills/diagnose/SKILL.md`, which must declare
`class: step` per §7.0:1081.
