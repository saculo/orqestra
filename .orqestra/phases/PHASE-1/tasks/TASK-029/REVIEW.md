---
id: TASK-029
type: review
status: awaiting-approval
updated: 2026-08-30
task: TASK-029
verdict: changes-requested
lenses: [correctness, design]
required: [F-1]
review_round: 1
---

## Verdict

The specification change itself is correct, well-evidenced and faithful to `DESIGN.md` — I re-derived
every criterion by hand against the real envelopes and all four hold. The task is returned for one
reason only: `git diff master...HEAD` carries `agents/architect.md`, a `plugin`-module file outside the
`docs` module's `PATHS`, and `IMPLEMENTATION.md` states the opposite. §5.5:925 fixes the severity for me
— "`review-task` flags any changed file that falls outside as a `major` finding (§5.2, §7.8.1, D2)" —
and that check keys off the diff, not off the commit scope the change was filed under.

## Findings

| id | severity | file:line | finding |
|---|---|---|---|
| F-1 | major | `agents/architect.md:4` | `tools:` gains `Edit` and `Bash`, plus 9 lines of prose at `:29-37`. `agents/` is the `plugin` module (`modules.md:14`); this task's `PATHS` are `REQUIREMENTS.md, README.md`. Filing it under an `orqestra:` commit scope (`d2d1a41`) does not move it out of the branch's diff, and the branch's diff is the PR. The three harms the floor guards are all live: the change is attributed to TASK-029's PR, it was reviewed under `docs` lenses by a reviewer carrying `orqestra-conventions` rather than `claude-expert`, and it is a permission expansion — the one class of `plugin` change that most wants its own review. Compounding it, `IMPLEMENTATION.md:8` records `files_changed: 1` and `:11` asserts "Nothing under `skills/`, `scripts/` or `agents/` was touched", so the artifact does not account for what the diff did (floor check 2). **The content is not wrong** — I verified `skills/design/SKILL.md:5` does declare `disallowed-tools: Agent, Edit, NotebookEdit, Bash`, so the D-024 two-layer argument holds. Resolution is attribution, not code: take `agents/architect.md` off this branch and land it under its own `plugin`-module task, leaving TASK-029 carrying `REQUIREMENTS.md` only. See `## Notes` — the removal has a loop-ordering consequence a human should settle at this gate. |
| F-2 | minor | `REQUIREMENTS.md:949` | "Omitted under `PHASE` and `PROJECT`" does not say whether omission is *required* or merely *not required*, so a `PHASE`-scoped envelope carrying `MODULE` is a violation under one reading and conformant under the other. Recorded by qa as I-1 and correctly not gated: no envelope hits the case today, and read against the row's `conditional` obligation and §5.5:958 ("an omission is a contract violation rather than a judgement call") the prescriptive reading is the plain one. It is still worth one clause, because TASK-030 must encode a reading in `scripts/`, and the spec deciding it there rather than here is the one-way link F-4 existed to close. Not worth an attempt on its own; fold it in if F-1 reopens the file. |
| F-3 | minor | `REQUIREMENTS.md:709`, `:1590`, `:1777` | C4 fixed the `api`/`java-expertise, test-quality` pairing at `:872` where F-3 pointed, but three further occurrences remain and now contradict both `§5.1:731` and the freshly-corrected example. Outside AC-3's reach as amended (TASK-015's F-3 named `:870` and scoped itself there), inside this module and this lens. Same disposition as F-2. |

## What Would Change This Verdict

_n/a_

## Notes

- **Floor check 3 — the coverage map is a real assertion, not a claim.** qa's harness was not committed
  (correctly: `scripts/` is `plugin`, D14), so the evidence reaches me as narrative. For a spec change
  the rule is short enough to apply by hand, and I did, independently of `QA.md`: the scope lines of all
  ten envelopes read from `HEAD` (`close-phase/SKILL.md:41` and `add-phase/step-define-phase.md:19` are
  `PHASE`-scoped and omit the four; `task/step-implement.md:35-36`, `step-qa.md:12-13`,
  `step-review.md:17,20` are `TASK`-scoped and carry all four; `greenfield/step-phases.md` carries no
  scope line); `.orqestra/config.md:2` carries `project: orqestra`; `REQUIREMENTS.md:872` now matches
  `:731` byte for byte; and the `^#{2,4} ` heading diff `master` vs `HEAD` is identical, so no `§N`
  citation breaks. Every claim I could check, checked out. AC-1, AC-2, AC-3 (F-3 and F-4) each have real
  evidence behind them.
- **The circularity behind F-1, for the human at this gate.** Reverting `agents/architect.md` removes
  `Edit` from the architect, who `modules.md:14` names as the `docs` module's engineer — which is what
  blocked implement twice (`2e6d260`, `29b98db`). Rework that removes the grant disables the agent the
  rework loop must dispatch. That is why F-1's resolution is written as re-attribution rather than
  deletion, and why the cleanest close may be a human ratifying the grant as its own `plugin` task
  (landed on `master` ahead of this branch) rather than an implement attempt. I flag rather than choose
  (D11): which of the two is orchestration, not code, and it is not mine to decide.
- **Design fidelity is clean.** C1–C5 land exactly as `DESIGN.md` specified: amended in place, no
  §5.5.2, no renumbering, the named-steps clause gone with no replacement list (which is what actually
  closes F-4 rather than re-deferring it), and D-027's `Constrains` line filled. `deviation: none` is
  accurate for the `REQUIREMENTS.md` edit.
- `QA.md:8` records `test_command: python3 scripts/check-templates.py`, which exercises none of this
  task's criteria — the real proof is the hand-execution in `## Results`. Harmless here, but the field
  reads as if the criteria were machine-checked when they were not. Outside my lenses.
- `check-envelopes.py` still exiting 1 is expected and correctly recorded as tech debt (D-019, D14).
  Not a finding.
