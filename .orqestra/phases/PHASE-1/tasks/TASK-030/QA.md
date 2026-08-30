---
id: TASK-030
type: qa
status: done
updated: 2026-08-30
task: PHASE-1/TASK-030
result: passed
test_command: python3 scripts/check-templates.py && python3 scripts/test-check-envelopes.py && python3 scripts/check-envelopes.py
---

## Test Strategy

Verified behaviourally, never by reading `check-envelopes.py` and reasoning that the rule looks right.
Three lines of evidence, graded against TASK.md's **amended** AC-1 (the `step-diagnose.md` half is
TASK-033/034's, per the §8.2 HTML comment), and against D-027.

**1. The repo scan, observed.** `python3 scripts/check-envelopes.py --verbose` run against the working
tree. Read the finding list in full to confirm nothing was suppressed — the one failure mode this task
was most at risk of. There is no allowlist, no known-failures set, no skip constant, and no marker in
any step file; `git show a1c5dac -- scripts/check-envelopes.py` adds none. `skills/greenfield/
step-phases.md:13` is listed **conformant**, carrying `PROJECT: orqestra` in the scope position — a
value read from `.orqestra/config.md` `project:`, not invented.

**2. Mutation testing of the checker, which is what proves the harness bites.** A harness that passes
is not evidence; a harness that *fails when the rule is broken* is. Eight mutants were applied to a
scratch copy of `check-envelopes.py` (the repo copy was never modified) and the harness re-run against
each. Every mutant was killed:

| mutant | killed by |
|---|---|
| `if len(scopes) != 1:` → `if False:` | harness aborts — `check()` raises on the empty-scope path |
| exactly-one → at-least-one (`< 1`) | `two scope fields are caught`, `PROJECT alongside TASK…` |
| exactly-one → at-most-one (`> 1`) | `no scope field is caught` (raises) — exit 1 |
| prohibition branch → `if False:` | both `conditional fields under PHASE/PROJECT are caught` |
| `FORBIDS_CONDITIONAL` loses `PROJECT` | `conditional fields under PROJECT are caught` |
| mandate reverted to the old partial-only rule (`have and have != …`) | `missing conditional class under TASK/BUG is caught` |
| `MANDATES_CONDITIONAL` loses `BUG` | `missing conditional class under BUG is caught` |
| `PROJECT` dropped from `SCOPE` | three cases, including `PROJECT is an accepted scope` |

The two regression guards named in DESIGN.md as must-not-change — `no scope field is caught` and
`two scope fields are caught` — are textually unedited in `a1c5dac` and their expectations
(`0 scope fields` / `2 scope fields`) are unchanged. They were repaired by the `BASE` redefinition
exactly as the design required, not accommodated. Mutants 1–3 confirm they still bite.

**3. End-to-end prohibition, at file level rather than at `check()`.** A copy of `skills/` was made in
the scratchpad and `MODULE`/`PATHS`/`STACK`/`EXPERTISE` injected into the `PROJECT`-scoped envelope in
`step-phases.md`. The scan went from 1 to 2 non-conformant, the new one reading
`EXPERTISE, MODULE, PATHS, STACK must be omitted under PROJECT`. §5.5's "must be omitted" is encoded as
a **prohibition**, not a permission — the parser yields `PROJECT:` and the forbidding branch fires on a
real file, not only on a synthetic field list.

**Test added (1).** `a single conditional field under PROJECT is caught` — the prohibition branch is
`if have:`, so a *partial* forbidden set is a distinct path from the full four, and no case exercised
it. Confirmed it fails under the prohibition-removed mutant. Strengthening only; nothing was weakened
and no expectation was relaxed to make anything pass.

## Results

```
python3 scripts/check-templates.py        21 templates      ✔ all conform            exit 0
python3 scripts/test-check-envelopes.py   25 cases          ✔ all pass               exit 0
python3 scripts/check-envelopes.py        10 envelopes      ✘ 1 non-conformant       exit 1
                                          skills/bugfix/step-diagnose.md:8 [diagnose]
                                              missing SKILL — always class
SUITE                                                                                exit 1
```

24 harness cases before this step, 25 after. The suite exits 1, **by construction and as designed** —
see `## Issues`. The single scan finding is `step-diagnose.md` and nothing else: re-read against the
pre-task state, this is down from two, the second having been `step-phases.md` itself.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 — `step-phases.md` conforms under §5.5 as amended by D-027 | `check-envelopes.py --verbose` lists it `✔` at line 13 with `PROJECT: orqestra`, a value read from `config.md` `project:` | passed |
| AC-1 — the checker encodes the amended rule (`PROJECT` in scope, class keyed off the scope key) | `PROJECT is an accepted scope`, `PROJECT alongside TASK is two scope fields`; mutant "`PROJECT` dropped from `SCOPE`" kills 3 cases | passed |
| AC-1 — the four module fields **must be omitted** under `PHASE` and `PROJECT` (prohibition, not permission) | `conditional fields under PROJECT are caught`, `…under PHASE are caught`, new `a single conditional field under PROJECT is caught`; plus the file-level injection into `step-phases.md` producing `must be omitted under PROJECT`; mutants 4–5 kill them | passed |
| AC-1 — the four stay **mandatory** under `TASK` and `BUG` | `missing conditional class under TASK is caught`, `…under BUG is caught`, `partial conditional class is caught`, `MODULE alone is caught`; mutants 6–7 kill them | passed |
| AC-1 — exactly-one-of scope survives the widening | `no scope field is caught`, `two scope fields are caught` (both unedited); mutants 1–3 kill them | passed |
| AC-1 — nothing invented to make it pass | no allowlist / skip-list / known-failures set / exemption marker anywhere in `a1c5dac`; the scan still reports `step-diagnose.md`, the one envelope that cannot conform | passed |
| AC-2 — both scripts in `config.md`'s `test_command` | `test_command` runs all three scripts in the design's order (harness before scan, so the harness result is not hidden behind a known red); executed as written | passed |
| AC-2 — a non-conformant envelope fails the suite | injecting a violation into a previously-conformant envelope turned the scan red on that file (evidence 3); `step-diagnose.md` fails the suite today rather than waiting to be noticed | passed |

Deviation review (`IMPLEMENTATION.md`, minor): the DESIGN case `conformant with full conditional class`
became byte-identical to `minimum conformant dispatch` once `BASE` absorbed the conditional four, and
was repurposed to `missing conditional class under TASK is caught`. **No coverage was lost.** What the
original asserted — a `TASK` envelope carrying all four is conformant — is asserted verbatim by
`minimum conformant dispatch`, since `BASE = SCOPED + CONDITIONAL`. The repurposing is a net gain: it
adds the `TASK`-side negative that mutant 6 kills, and leaving a duplicate would have been a case that
could never fail independently. Correct call.

## Issues

No defects. One judgement call is referred up, as asked.

**The suite is red by construction until TASK-034 lands, and I think that is the right trade — but it
needs a visible expiry, not a note in a commit message.**

The trade is right on the merits. AC-2 asked for exactly this: a non-conformant envelope should fail
the suite rather than wait to be noticed. The alternative is worse in a way this phase has already been
burned by — the only way to keep the suite green is to skip-list `step-diagnose.md`, and a suppression
is the same fabrication TASK.md's Out of Scope forbids, reached by a different route. Worse, it would
silently outlive TASK-034: nobody removes an allowlist entry after the thing it hid gets fixed. A red
line in every run is a debt that keeps announcing itself; a skip-list is a debt that disappears.

The cost is real, though, and it is the disease this phase has been treating. Every `qa` from here runs
a `test_command` that exits 1, and each one has to re-derive that one specific failure is expected.
That is precisely how a team learns to read `exit 1` as "the usual" — and the run *after* the one where
a second envelope breaks looks identical at a glance. The failure mode is not that the red is ignored;
it is that a **new** red hides inside the old one.

What makes it survivable: the finding list is itemised per file, so a second failure changes the count
line (`✘ 1 non-conformant`) visibly, and the harness runs *first* in the `&&` chain, so the part that
tests the rule reports green on its own. Those are real mitigations and they were designed in.

What I would ask for — and it is a suggestion for the humans, not a finding against this task, since no
`AC-N` asks for it: **give the known red an owner and a deadline in a place a reader of a failing run
will see.** One line in `.orqestra/config.md` beside `test_command` naming `step-diagnose.md`, TASK-034,
and "delete this line when the scan goes green" costs nothing and converts "the suite is always red"
into "the suite is red for exactly one reason, and here is who owns it". If TASK-034 slips, that line
is what makes the slip visible instead of normal. Deliberately not changed here — `config.md` edits are
sanctioned for AC-2's `test_command` only, and inventing an out-of-scope edit at qa is its own defect.
