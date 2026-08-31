---
id: TASK-034
type: review
status: done
updated: 2026-08-31
task: TASK-034
verdict: passed
lenses: [correctness, design]
required: []
review_round: 2
---

## Verdict

F-1 is repaired, and repaired at the end this review said it had to be: the false citation is gone
from `skills/diagnose/SKILL.md` rather than papered over by editing the authority it misquoted. Both
`:57` and rule 1 at `:128` now cite `skills/bugfix/step-diagnose.md`'s `## The bar`, which says what
they claim — `:31` there reads "`root_cause_found: false` is an honest and useful outcome", the exact
disposition this skill's outcome contract row two encodes. The two lines agree with each other and
neither restates the bar. No third stale reference survives: `grep -nE 'bugfix|rule [0-9]|SKILL\.md'`
over the file returns `:57` and `:128` and nothing else. `required` is empty; F-2 remains advisory.

## Findings

| id | severity | file:line | finding |
|---|---|---|---|
| F-2 | minor | `skills/diagnose/SKILL.md:91` | Unchanged from round 1, correctly — it was never in `required`. "On `done`, nine:" heads a fenced block of eight lines (`SKILLS`, `STATUS`, `ROOT_CAUSE_FOUND`, `ROOT CAUSE`, `EVIDENCE`, `DIRECTION`, `RISK`, `SCHEMA`). Inherited from `DESIGN.md`, so not a deviation; the literal block governs and the ceiling is "at most 10", so nothing breaks. Still worth a line whenever this file is next opened, because a stated count that disagrees with the block beneath it invites a fresh agent to pad a ninth line |

## What Would Change This Verdict

_n/a_

## Notes

**Check 1 — the new citation points at authority that agrees.** `skills/bugfix/step-diagnose.md`'s
`## The bar` (`:26–32`) states "Root cause, not symptom. Evidence, not plausibility", that the first
plausible line is where the symptom became visible rather than where it came from, and that
`root_cause_found: false` is "an honest and useful outcome". That sanctions the falsification bar step
4 claims to meet and the honest-no-cause result — with one boundary worth naming: `## The bar` says
nothing about *gate-reaching*, which is a property of `skills/diagnose/SKILL.md`'s own contract at
`:79–86` plus the `[ Investigate further ]` branch in the gate exemplar at `step-diagnose.md:47`. The
repair respects that boundary rather than overreaching it. `:57` says explicitly "What follows when
nothing survives is this skill's own: the outcome contract below", and `:130` attributes the
disposition locally — "`root_cause_found: false` per the outcome contract — never a block". Neither
line claims the cited authority governs more than it does.

**Check 2 — `:57` and `:128` agree, and the disagreement was resolved rather than moved.** Round 1's
finding had two halves: `:57` claimed to defer while `:128` restated the bar verbatim with a swapped
ending. Now `:57` defers and hands off to the local contract; rule 1's body defers to the same section
and points at step 4 as where the bar is met, keeping only the local disposition. Rule 1's imperative
title ("Never diagnose past the first plausible cause") still paraphrases the bar's `:30`, but a rule
heading naming its subject above a body that defers is not the restatement the convention forbids —
the substance is cited once and stated nowhere.

**Check 3 — nothing else cites contrary authority.** The whole-file grep is the check, not a spot look
at the two edited lines. `skills/bugfix/SKILL.md` and "rule 3" appear nowhere in the file. Every other
citation in it resolves to something that agrees: `§5.5`, `§7.3.1`, `§5.5.1`, `§4.4.3`, `§7.0`, `§5.2`,
`D3`, `D-015`. The `**block**` at `:48` is the no-reproduction case from `## When you cannot proceed`,
a different branch from the one F-1 concerned, and consistent with rows three and four of the contract.

**Leaving `skills/bugfix/SKILL.md` alone is coherent, per the human decision (§8.2), and I do not
re-raise it.** The repair removed the *assertion this task made* — that rule 3 is the bar this step
meets. With that assertion gone, no line in this diff contradicts anything, and rule 3's "Evidence, or
**block**" is left as what it already was on `master`: an outlier against its own step file at
`step-diagnose.md:30`. `IMPLEMENTATION.md:119` records it under `## Tech Debt` with the file, line,
and reason, which is the right disposition for a defect this work did not cause.

**Round-1 conclusions spot-checked, and they hold.** The change is two prose lines in one file, so it
could only have disturbed the procedure or AC-4. Step 4 still states a falsification *test* and still
needs no `Bash`; the outcome contract table at `:79–86` and the return blocks are untouched, so
orchestrator-legibility is unaffected. AC-4 gained a second step-file reference at `:128` — backticked,
plugin-relative, no `${CLAUDE_PLUGIN_ROOT}` — which is the D-026 shape, and `IMPLEMENTATION.md` records
that the reference count went from one to two rather than letting the count drift silently. Floor
re-run on the new diff: both files are `skills/diagnose/SKILL.md` and the task's own
`IMPLEMENTATION.md`, the latter being workspace state belonging to no module; the implementation note
accounts for both lines and justifies them; no `D-NNN` is contradicted. Per rule 2 I did not re-run the
suite — the checker results at `IMPLEMENTATION.md:99–105` are qa's and implement's artifact, and I
have no `tests` lens and no reason to doubt them.
