---
id: TASK-030
type: design
status: awaiting-approval
updated: 2026-08-30
task: PHASE-1/TASK-030
decisions: []
---

## Components

| # | component | responsibility | serves |
|---|---|---|---|
| C1 | the amended obligation rule in `check-envelopes.py` | `PROJECT` joins the scope set, so exactly-one-of is four-way; the conditional class becomes scope-keyed — `MODULE` `PATHS` `STACK` `EXPERTISE` all required under `TASK`/`BUG`, all forbidden under `PHASE`/`PROJECT`. Its docstring's four-class summary is part of the component, not commentary: it is a second copy of the rule and goes stale in the same edit | AC-1 |
| C2 | the `PROJECT` scope field on the `create-phases` dispatch | `skills/greenfield/step-phases.md`'s envelope names the unit it operates on. Value is the project name from `.orqestra/config.md` `project:` — `orqestra` for this repo (D-027). Nothing else is added: the envelope already carries all seven always-class fields and correctly carries no conditional ones | AC-1 |
| C3 | the behavioural harness in `test-check-envelopes.py` | Proves C1 rejects what it must and accepts what it must, in both directions, for violations not present in the tree. Changing the rule changes what its 19 cases assert, so it moves with C1 in the same commit — a harness asserting the superseded rule is worse than none | AC-1 |
| C4 | the widened `test_command` | `.orqestra/config.md` runs C1 and C3 as part of the suite, so a non-conformant envelope fails a run rather than waiting to be noticed | AC-2 |

No fifth component. `skills/diagnose/` is TASK-034's; `REQUIREMENTS.md` §5.5 is already amended and is `docs` (D-019, D14).

## Interfaces

**`check(step, fields) -> [str]` keeps its signature and its inputs.** `fields` is the ordered list of
field *names*; the scope key is already in it, so the scope-keyed rule needs no new argument, no
envelope values, and no file read. Any design that reaches for `modules.md` or for field values has
left this task.

The problem strings are the contract C3 asserts against — they are interface, not prose. Three change
shape:

| condition | message |
|---|---|
| scope count `n != 1` | unchanged: `{n} scope fields; exactly one of TASK/PHASE/BUG/PROJECT required` — the set widens, the wording does not |
| scope is `TASK`/`BUG`, conditional members missing | names the missing members and the scope key that made them mandatory (e.g. `missing MODULE, PATHS — mandatory under TASK`). This *replaces* the `partial conditional class — missing …` message: under the amended rule a partial set and an empty set are the same violation, so one message covers both |
| scope is `PHASE`/`PROJECT`, any conditional member present | names the present members and the scope key that forbids them (e.g. `MODULE, PATHS must be omitted under PROJECT`) |

**When the scope count is not exactly one, report the scope problem and emit no conditional-class
verdict.** With no scope key, or two, the class is undecidable; a derived second complaint is noise
that also makes every one-problem test case ambiguous.

The envelope field format is unchanged — `PROJECT:` is a `^[A-Z]+:` line like any other and the
existing parser already yields it. It sits immediately after `SKILL:`, in the scope position §5.5
fixes for all four values.

## Structure

The change lands in two places inside the `plugin` module and one sanctioned place outside it.

**`scripts/` holds the rule and its proof, and they are one unit.** The checker and its harness must
change in the same commit; a green harness asserting the pre-D-027 rule is a false witness. The harness
imports the checker by path and calls `check()` directly — it must not grow a subprocess run over the
repo, because a repo scan proves only what today's tree happens to contain, which is the gap the
harness exists to close.

**`skills/greenfield/` holds the envelope.** One line added to an existing dispatch block. The step
file is data to the checker and must not learn anything about it — no marker, no exemption comment.

**`.orqestra/config.md` is outside every module's `paths` by design.** TASK-001 set this same
`test_command` line and shipped; TASK.md records the precedent as sanctioned (§8.2), so review reads it
as licensed rather than as an out-of-paths `major` finding (§7.8.1, D2). `templates/config.md`'s
`test_command` stays empty — it seeds other projects, which have no `scripts/`.

**Order:** C1 and C3 together, then C2 (the envelope can only be verified against the amended rule),
then C4 last — widening the suite before the rule is amended reports failures this task caused.

**`check-envelopes.py` will exit 1 on `skills/bugfix/step-diagnose.md` after this ships**, because its
`SKILL:` names a skill nobody has authored. That is the correct result and the suite is expected to go
red on it until TASK-033 and TASK-034 land. Nothing here may suppress it — no allowlist, no
known-failures set, no `SKILL:` value invented to clear it. A suppression is the same fabrication
TASK.md's Out of Scope forbids, reached by a different route, and it would silently outlive TASK-034.

## Decisions

**`EXPERTISE` stays mandatory under `TASK`/`BUG`, and the checker does not try to decide §5.5 row 4.**
The row omits `EXPERTISE` when the module's `expertise` cell is empty — a fact that lives in
`modules.md`, not in the envelope, so no checker reading only the envelope can tell a conformant
omission from a forgotten field. Three answers were available and this one is the least bad:

- *Drop `EXPERTISE` to permitted-but-not-required under `TASK`/`BUG`.* Rejected. A missing `EXPERTISE`
  is precisely the silent degradation the checker's own docstring names — the dispatch does not fail,
  it runs on the bare persona and returns plausible work following none of this project's conventions
  (§5.5, D-025). Making the one field that fails invisibly the one field unchecked guts the tool.
- *Cross-check `MODULE`'s value against `modules.md`.* Rejected as scope. It needs field *values* and a
  workspace read, changing `check()`'s inputs and coupling a `skills/`-shaped checker to `.orqestra/`.
  No `AC-N` asks for it.
- *Require all four, and say so.* Chosen. Both rows of `modules.md` carry a non-empty `expertise` cell,
  and the checker is dev-only (D-001) — it globs `skills/` relative to its own repo root and never runs
  against a consuming project. So the false positive it can produce cannot occur in the only tree it
  can run in.

The limit is recorded in the docstring beside the rule, as the condition under which this would need
revisiting: **the first module registered with an empty `expertise` cell**. A reader who finds the
checker disagreeing with §5.5 row 4 must find the reason there, not rediscover it.

No `D-NNN` file. This constrains one script's rule, not future tasks; the durable choice — the scope
key alone decides the conditional class — is already **D-027**, which this design implements rather
than extends.

## Test Strategy

The suite is `python3 scripts/check-templates.py`, then `test-check-envelopes.py`, then
`check-envelopes.py`. **The harness runs before the repo scan**: the scan is expected to exit 1 on
`step-diagnose.md`, and an `&&` chain in the other order would hide the harness result behind a known
red.

**AC-1, the envelope.** `check-envelopes.py --verbose` lists `skills/greenfield/step-phases.md` as
conformant, and the run's only failure is `skills/bugfix/step-diagnose.md` with `missing SKILL`. Any
other failure, or that file passing, means something was fabricated.

**AC-1, the rule.** The harness carries the proof. Its `BASE` constant is the pre-amendment minimum —
always class plus `TASK`, no conditional fields — and under the amended rule that is *no longer
conformant*. Redefining `BASE` to include the conditional four is the single edit that repairs every
case built on it.

*Cases that must change:*

| case | why |
|---|---|
| `minimum conformant dispatch` | `TASK` with no conditional class is now a violation — repaired by the `BASE` change |
| `missing SKILL` / `missing WRITE` / `missing RETURN` | each asserts exactly one problem; unrepaired `BASE` adds a second |
| `BUG is an accepted scope` | must carry the conditional four to stay conformant |
| `PHASE is an accepted scope` | must use a scope-only base, *without* the conditional four — it passes today only by accident and must now pass on purpose |
| `partial conditional class is caught`, `MODULE alone is caught` | the expected substring moves to the replacement message |
| `LENSES outside…`, `ROUND outside…`, `an invented field…`, `REWORK is permitted…`, `a duplicated field…` | all built on `BASE`; repaired by the `BASE` change, expectations unchanged |

*Cases that must NOT change:* `no scope field is caught` and `two scope fields are caught`. These are
the regression guards. A checker that accepts `PROJECT` but stopped rejecting a missing or doubled
scope key would satisfy every other case here and leave the rule hollow — if either case is edited to
accommodate the new rule rather than repaired by the `BASE` change, the change is wrong. Likewise the
step-specific and closed-list cases keep their expectations exactly.

*New cases — the `PROJECT` path, positive and negative:*

| case | asserts |
|---|---|
| `PROJECT is an accepted scope` | scope-only base with `PROJECT` → no problems |
| `conditional fields under PROJECT are caught` | scope-only base plus the four → one problem naming them and `PROJECT`. **The negative half of AC-1**: without it, "must be omitted" is a sentence in §5.5 that nothing enforces |
| `conditional fields under PHASE are caught` | the same prohibition on the other omitting scope — `PHASE` regressed silently once already |
| `missing conditional class under BUG is caught` | mandatory-under-`BUG` fails when absent, not just when partial |
| `PROJECT alongside TASK is two scope fields` | widening the set did not turn exactly-one into at-least-one |

**AC-2.** Running `test_command` as written in `.orqestra/config.md` executes all three scripts; the
run reports the harness green and the repo scan red on `step-diagnose.md` alone. Temporarily deleting a
required field from any conformant envelope turns the scan red on that file too — which is what "a
non-conformant envelope fails the suite" means, and is the only way to observe it while the diagnose
envelope is legitimately red.
