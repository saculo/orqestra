---
id: TASK-040
type: plan
status: done
updated: 2026-08-31
task: TASK-040
---

## Approach

Close the schema window TASK-037 opened by landing the two edits it could not: the `templates/`
file and the skills that write and read it (`orqestra-conventions`: a schema change is three
edits, always together; docs led under D-019).

**1. `templates/BUG.md` gains `module:`** (AC-1). §4.8.1:584 already reads
`` | `BUG.md` | `bugfix` intake | `module` `bug` `severity` | ... ``; the template carries
`id type status updated bug severity` and so fails `frontmatter missing: module`. The checker
compares key *sets*, not order (`check-templates.py:192-197`), so placement is free and is
design's call, not this plan's.

**2. `## Scope` stops carrying the module** (AC-3). `templates/BUG.md:22` currently instructs
"which module the symptom surfaces in". D-029's `Constrains` is flat on this, and D9 puts a
decision above a criterion written before it — so AC-3's disjunct *"or the prose stops carrying
the module"* is the branch that is taken, and taking it satisfies AC-3's other branch vacuously.
This resolves TASK-037 review finding F-1: **D-029 governs, AC-3 is satisfied by it, not in
tension with it.**

**3. `step-intake.md` establishes rather than invites** (AC-2). `step-intake.md:13` reads
"**Where it surfaces** — which module, if known"; the word must go. What *establishing* can
mean concretely, from the files as they stand:

- **Closed choice, not free text.** Intake already gathers via `AskUserQuestion` (`SKILL.md:5`
  grants it). `modules.md` `## Modules` is a closed registry of the project's modules, so the
  question becomes "which of these rows", not "name a module". This alone converts most
  "unknown" answers into an answer.
- **Derivation from the symptom surface.** `step-reproduce.md:7` already does exactly this —
  "Identify the module from the symptom" — by matching what the reporter observed (failing test
  path, stack frame, command run) against the `paths` column. The capability exists in the
  workflow; it is only in the wrong step. Intake writes `BUG.md`, so the derivation has to
  happen *before* the write, not two steps later.
- **Only then, block.** If neither a human choice nor a path match yields a row, the bug is not
  creatable (D-029). See OQ-1 — no value on §4.4.3's closed `blocked_reason` list fits, and
  inventing one is forbidden (D11).

Because intake takes the derivation over, `step-reproduce.md:7` must stop re-deriving and read
the key instead. D-029's `Constrains` names only diagnose and promote, but its `Why` names
`reproduce` as part of the same re-derivation problem, and leaving it is the "rule written in
two places" the decision exists to prevent.

**4. `step-diagnose.md` and `step-promote.md` read the key** (AC-4). Neither file states today
where `MODULE:` comes from — `step-diagnose.md:12-15` is a worked example with no rule behind
it, which is precisely the "unchecked convention" TASK.md describes. Both gain the rule: compose
`MODULE`/`PATHS`/`STACK`/`EXPERTISE` from the BUG's `module:` via its `modules.md` row, never
from the symptom; when diagnosis finds the fix lands elsewhere, amend the BUG's frontmatter and
recompose the dispatch. `step-diagnose.md:16-20` already `READ`s both `BUG.md` and `modules.md`,
so the inputs are in place and no envelope field changes.

**5. `.orqestra/config.md:34-40`** (AC-5): the comment describes `check-envelopes.py` red on
`step-diagnose.md`, which TASK-034 closed, while the chain is red for the `BUG.md` window this
task closes. Its own text says "DELETE THESE LINES when the scan goes green". Deleting is the
action its instruction names; correcting it in place would restate a rule that no longer has a
condition.

**Alternatives considered.** *Declare `module` optional on the §4.8.1 row* — rejected: the row
landed non-optional under TASK-037 and is out of scope here, and D-029 forbids a bug without a
module regardless. *Let reproduce supply the module and have intake write `BUG.md` without it* —
rejected: D-029 says a bug whose module is unknown is not creatable, and a template key written
empty by design is exactly the unchecked-convention failure this task closes (see R-3).

## Affected Areas

Every file below was opened and read.

| file | what is there now | why it is touched |
|---|---|---|
| `templates/BUG.md:1-8` | frontmatter `id type status updated bug severity` — no `module` | AC-1; the failing key |
| `templates/BUG.md:21-22` | `## Scope` comment names the module | AC-3 / D-029 |
| `skills/bugfix/step-intake.md:13` | "which module, **if known**" | AC-2; the word D-029 removes |
| `skills/bugfix/step-intake.md:15-21` | `## Write` — copies the template literally (D16) | must establish before the write |
| `skills/bugfix/step-intake.md:26` | report line `surfaces in api` | display of the same fact |
| `skills/bugfix/step-reproduce.md:7` | "Identify the module from the symptom" | re-derivation D-029's `Why` names |
| `skills/bugfix/step-diagnose.md:5-24` | example dispatch; `MODULE: api` with no stated source | AC-4; the convention gains a schema |
| `skills/bugfix/step-promote.md:12-20` | `module: api  # where the fix lands` on the produced task | D-029: read, never re-derive |
| `skills/bugfix/SKILL.md:41` | intake summary — "the report, reproduction steps, expected vs actual, and scope" | the scope sentence is where the module used to live |
| `.orqestra/config.md:33-40` | `test_command` + the stale "red BY DESIGN" comment | AC-5 |

**Not touched, verified:** `scripts/check-templates.py` needs no change — `COMMON` (line 27) plus
the row's keys is already the contract, and it reads the amended row from `REQUIREMENTS.md`.
`scripts/check-envelopes.py` is out of scope by TASK.md; its line 47 comment
(`# the scope unit carries a module: (D-027)`) becomes true when this lands, as TASK.md predicts.
`REQUIREMENTS.md` is `docs` (D14) — §4.8.1:584 was checked and is already correct.

**The 3 failing assertions in `test-check-templates.py`, read case by case.** The file runs 12
cases producing 15 `check(...)` assertions. Exactly three assert a zero exit against an
otherwise-clean fixture, and each fails today only because `BUG.md` fails in that same fixture:

- `case_clean:104` — `"clean tree exits 0"` (`code == 0`)
- `case_ac1_heading_comparison_skipped:139` — `code == 0` after adding a stray heading
- `case_ac2_counted:146` — `code == 0 and "✓ decisions/D-NNN-*.md" in out`

The other twelve assert `code == 1` with a named message, or `code == 2` on an unreadable
catalogue, and are indifferent to a second failing template. So adding `module:` to
`templates/BUG.md` closes all three and touches none of the twelve — this is **known from the
cases, not hoped**. It also matches the 3-of-15 count in the dispatch, which is independent
corroboration. I hold no `Bash`, so this is read, not executed; whoever implements must run both
scripts.

**`.orqestra/work/` is empty** — no `BUG.md` instance exists (`Glob .orqestra/work/**` returns
nothing). This is a schema change, not a migration. Nothing is invalidated.

**`.orqestra/` belongs to no module** — confirmed against `modules.md:45-47`, not assumed:
"*`.orqestra/` deliberately belongs to NO module*". The `plugin` row's `paths` are
`skills/, agents/, templates/, scripts/, .claude-plugin/` and do not include it. See OQ-3.

## Risks

- **R-1 — `module:` present but empty satisfies the checker.** `check-templates.py` reads keys
  by `line.startswith(f"{key}:")`; a bug written with `module:` and nothing after it passes both
  template and instance checks. The schema constrains presence, not truth, so AC-2's "cannot be
  created without one" rests entirely on `step-intake.md`'s wording. That instruction is the only
  thing holding it — worth stating plainly rather than implying the checker covers it (§7.0.1).
- **R-2 — instance mode never sees a `BUG.md`.** `check_instance` (`check-templates.py:119-128`)
  globs `PHASE.md`, `TASKS.md`, `TASK.md`, `PLAN.md`, `DESIGN.md`, `IMPLEMENTATION.md`, `QA.md`,
  `REVIEW.md`, `PR.md`, `PHASE_SUMMARY.md` and the decisions — **not** `work/*/BUG.md` or
  `DIAGNOSIS.md`. So `--target .orqestra` will never catch a real bug missing its module. No AC
  asks for this and I am not proposing it as scope; it is the gap that makes R-1 matter.
- **R-3 — the AC-1 harness is not in the `test_command` chain.** `config.md:33` runs
  `check-templates.py && test-check-envelopes.py && check-envelopes.py`. `test-check-templates.py`
  (and `check-decisions.py`, `check-step-refs.py`, `test-check-step-refs.py`) are absent. AC-1
  demands `test-check-templates.py` exit 0 and AC-4 demands the chain exit 0 — these are two
  different runs, and passing the chain does not evidence AC-1. Run it explicitly.
- **R-4 — an amended `BUG.md` after diagnose has no schema trace.** D-029 allows the module to be
  corrected when diagnosis finds the fix lands elsewhere. Nothing records that it changed, and the
  already-composed diagnose envelope named the old one. Small today (no bugs exist), but it is the
  one path where the key and a dispatch can disagree.
- **R-5 — the worked examples name modules this repo does not have** (`api`, `java`,
  `spring-conventions` in `step-diagnose.md`, `step-promote.md`, `SKILL.md`). They are
  illustrative and correct as illustrations; a reader mapping them onto `modules.md` finds no
  match. Not a defect, but the reason to state the *rule* next to the example rather than trusting
  the example to carry it.

## Open Questions

- **OQ-1 — AC-2's block has no `blocked_reason` that fits, and this is the task's hard edge.**
  §4.4.3's closed work list is `contradictory-input` · `criterion-unsatisfiable` ·
  `no-reproduction` · `design-invalid` · `max-attempts` · `contract` · `needs-splitting`. Read
  against "the reporter cannot name the module": `contradictory-input` needs a conflict, and an
  incomplete input is not a contradiction; `no-reproduction` is `reproduce`'s and means the
  symptom would not reproduce; `contract` is defined by §4.4.5 as an artifact that failed its
  schema twice after re-dispatch, which is not this. **No value fits**, and inventing one is
  forbidden (D11, D7). A human must choose: (a) reuse `contract` and accept the stretch, (b) add
  a value to §4.4.3 — a `REQUIREMENTS.md` edit, therefore `docs`, therefore a different task
  (D14, and this task's Out of Scope forbids it), or (c) rule that intake never blocks because a
  human is present at intake by construction, and an unanswerable module question ends the
  workflow without an artifact. **My reading is that (c) is closest to how intake actually runs**
  — but it is a decision, not an inference, and I will not make it here.
- **OQ-2 — if intake does block, what artifact carries the `blocked_reason`?** `BUG.md` is the
  only artifact intake produces, and it is precisely the file that cannot be written. Writing it
  with an empty `module:` to hold `status: blocked` would pass the checker (R-1) and violate
  D-029's "may not create a bug without one". This is why OQ-1 is not merely a naming question.
- **OQ-3 — AC-5 edits `.orqestra/config.md`, which is outside this task's `PATHS`.** The AC's
  own HTML comment says "config.md is `plugin`"; `modules.md:45-47` says `.orqestra/` belongs to
  **no** module. The premise is wrong, though the conclusion likely survives: because it is in no
  module, editing it crosses into no other module's paths, so D14 is not violated and the §8.2
  human decision that folded AC-5 here stands. Confirm rather than assume — it decides whether
  the implementer may touch the file at all, and my dispatch `PATHS` do not list it.
- **OQ-4 — is `step-reproduce.md:7` in scope?** No AC names it and D-029's `Constrains` lists
  only diagnose and promote, yet its `Why` names `reproduce` as one of the four re-derivers.
  Approach item 3 includes it. If a human disagrees, it is a follow-up in the same module and the
  task still closes master; if left, the workflow both establishes and re-derives the module,
  which is the state D-029 exists to end.
