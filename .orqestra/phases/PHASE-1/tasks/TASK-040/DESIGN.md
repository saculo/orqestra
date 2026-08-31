---
id: TASK-040
type: design
status: awaiting-approval
updated: 2026-08-31
task: TASK-040
decisions: []
---

## Components

Six components. D-029's `**Constrains:**` has four obligations; the column says which discharges
which. Obligation 4 — *"any future scope unit added to §5.5 states in §4.8 whether it carries
`module:`"* — binds future tasks, not this one, and has nothing to discharge here. Naming that is
part of the mapping, not an omission from it.

| # | component | responsible for | AC | D-029 obligation |
|---|---|---|---|---|
| C-1 | **The `BUG` frontmatter key** | `templates/BUG.md` carries `module:` — the schema half of "a bug names its module" | AC-1 | 1 (schema side) |
| C-2 | **`## Scope` stops carrying the module** | the template's `## Scope` guidance no longer asks for a module, so the fact lives in exactly one place | AC-3 | 2 |
| C-3 | **Intake's module-establishment procedure** | `step-intake.md` establishes the module before it writes, and never blocks — including every restatement of intake's contract elsewhere in the workflow | AC-2 | 1 (workflow side) |
| C-4 | **Reproduce reads instead of re-deriving** | `step-reproduce.md:7` loads expertise from the BUG's `module:`, not from the symptom | AC-4 | Why (settled in scope, §8.2) |
| C-5 | **Diagnose composes from the key, and the correction path** | `step-diagnose.md` states that `MODULE`/`PATHS`/`STACK`/`EXPERTISE` are read from `BUG.md`'s `module:`, and what happens when diagnosis finds the fix lands elsewhere | AC-4 | 3 |
| C-6 | **Promote carries the key** | `step-promote.md` states the produced task's `module:` is the BUG's, never re-derived from the symptom or the diagnosis | AC-4 | 3 |
| C-7 | **The stale `config.md` comment is deleted** | `.orqestra/config.md` stops describing a failure that is not the one occurring | AC-5 | — |

### C-3 — what intake does when the reporter cannot name a module

"Ask the human" is a direction. This is the procedure, and it must read as one to a fresh agent:

1. **The question is a closed choice, never free text.** Intake presents the `module` column of
   `.orqestra/modules.md`'s `## Modules` table as the options, each shown with that row's `paths`
   so the reporter can recognise their own surface. Intake already holds `AskUserQuestion`
   (`skills/bugfix/SKILL.md:5`). A registry of two rows answers most "unknown"s by being visible.
2. **If the reporter still cannot choose, intake derives a candidate.** It takes the concrete
   surface already gathered in the report — failing test path, stack frame, file path, the command
   run — and matches it against the `paths` column. This is the capability `step-reproduce.md:7`
   holds today, moved to the step that writes the file (C-4 removes it from reproduce).
3. **A derived candidate is offered back, never written silently.** Exactly one row matches → ask
   again with that row pre-selected and say what it matched on. Zero or more than one match → ask
   again over the candidate rows, or the full registry when none matched, stating what was tried.
4. **Intake does not write `BUG.md` until an answer exists, and does not block.** A human is
   present at intake by construction; the question is re-asked, not parked. If the human abandons
   it, the workflow ends having written nothing and reports that — no artifact, no
   `blocked_reason`. §4.4.3's list is closed and no value fits an incomplete input (§8.2
   amendment on `TASK.md`; D11, D7).
5. **Never write `module:` empty, and never fall back to `## Scope` prose** (D-029).

Rule 4's reason travels with it: the reason a block is unavailable is that `BUG.md` is the only
artifact intake produces and is the file that cannot be written. Without that reason the rule
looks arbitrary and the next reader will re-add the block.

C-3 also covers the two places intake's contract is restated: the report line in `step-intake.md`
and the one-sentence intake summary in `skills/bugfix/SKILL.md`. A contract stated in three places
and updated in one is the failure D-029 exists to end.

### C-5 — a module that turns out wrong at diagnosis

D-029 forbids a `MODULE:` that disagrees with the artifact it names. Three parts, and the step that
owns each:

- **Diagnose composes from the key.** `step-diagnose.md`'s envelope takes `MODULE:` from
  `work/BUG-NNN/BUG.md`'s `module:` and the other three fields from that one `modules.md` row.
  §5.5 (REQUIREMENTS.md:930-935) already says this in the spec; the step gains the rule beside the
  worked example, because the example alone is what let the convention go unchecked.
- **The analyst reports the disagreement; it does not fix it.** `DIAGNOSIS.md`'s `## Fix Direction`
  already means "where the fix belongs". When that is not the BUG's `module:`, the analyst states
  the difference explicitly. It cannot amend `BUG.md` — `agents/analyst.md:4` grants no `Edit`,
  `skills/diagnose/SKILL.md` disallows it, and D2 gives it one write path.
- **The amendment happens at the diagnosis gate, before promote.** The gate block carries a
  `MODULE` line whenever the two differ; approving the diagnosis approves the correction. On
  approval the BUG's `module:` is amended and any dispatch that named the old value is recomposed
  — never left standing. Promote then reads the amended key (§7.3, REQUIREMENTS.md:1213), so the
  task's `module:` and the bug's agree by construction rather than by luck.

**Stated plainly, per §7.0.1:** no actor in the `bugfix` workflow currently holds a tool that can
amend `BUG.md`. The orchestrator disallows `Write` and `Edit` (`skills/bugfix/SKILL.md:6`), the
analyst has no `Edit`, and `create-task` has none either. This is **pre-existing and identical for
all three writes to `BUG.md`** — intake's creation and reproduce's `## Reproduction` update have
the same gap today. This task states the rule at the step where the correction is decided and
changes no tool field; closing the capability gap is a separate task (see `## Decisions`).

## Interfaces

Every contract below was read, and both harnesses were run at design time.

- **§4.8.1 catalogue row** (`REQUIREMENTS.md:584`), already amended by TASK-037:
  `` | `BUG.md` | `bugfix` intake | `module` `bug` `severity` | `## Report` · `## Reproduction` · `## Expected vs Actual` · `## Scope` | ``
  The frontmatter contract is `COMMON` (`id type status updated`, `check-templates.py:27`) plus
  those three. `check-templates.py:192-197` compares key **sets in both directions** — a missing
  key and an extra key both fail — so `module` and nothing else may be added, and placement within
  the block is free. The **headings and their order are unchanged**: `## Scope` must survive C-2,
  which alters only its HTML-comment guidance.
- **`modules.md` `## Modules`** — columns `module | paths | agent | stack | expertise`. C-3's
  closed choice is the `module` column; C-3's derivation matches an observed surface against
  `paths`. Two rows today: `plugin` and `docs`.
- **The `BUG` dispatch envelope** (§5.5). No field changes. `check-envelopes.py` keys on the scope
  key and never reads frontmatter, so it neither gains nor loses coverage here; it exits 0 today
  (10 envelopes, verified) and must still.
- **`.orqestra/config.md:33`** — the `test_command` line itself is unchanged. Only the comment on
  lines 34-40 is removed.
- **`scripts/` is not touched.** Verified: `check-templates.py` reads the amended row from
  `REQUIREMENTS.md` and needs no edit; `check-envelopes.py` is out of scope by `TASK.md`.

## Structure

Four areas, one of which is read-only.

**The schema layer** — the artifact template. It carries the key and it stops carrying the module
in prose. Nothing else in this task may state where a bug's module lives.

**The workflow layer** — the `bugfix` step shards and the one summary sentence in its `SKILL.md`.
This is where every behavioural change lands. The boundary that matters: **once intake establishes
the module, no later step in this workflow may derive it from the symptom.** Reproduce, diagnose
and promote read the key; that is the whole of D-029's Constrains, and a step that re-derives is a
second source of truth however correct its answer.

**The harness** — read-only in this task. It is the evidence, not the deliverable. Do not add a
skip-list, do not touch the catalogue parser, do not widen `INSTANCE_PATHS`.

**The workspace config** — `.orqestra/config.md`, which belongs to **no** module
(`modules.md:45-47`), so editing it crosses no other module's boundary (OQ-3, settled §8.2). Only
the comment goes; the command stays.

**`REQUIREMENTS.md` is out of bounds** — `docs`, D14, and TASK-037 already landed the row. If the
spec is found wrong, report it; do not edit it.

**Order.** The schema key first, because every later edit cites the key it creates. Then intake,
the only step that establishes it. Then the three steps that read it, in workflow order —
reproduce, diagnose, promote — so each is written against a key that already exists in the
template. Then the `SKILL.md` summary sentence, which restates intake's contract and must match the
final wording rather than an intermediate one. `config.md` last: its claim becomes true only once
the templates go green, and deleting it earlier would be deleting a true comment.

## Decisions

**AC-2 is held by prose, and prose is the only layer available here. Say so; do not design as if
it were enforced.** `check-templates.py` reads keys with `line.startswith(f"{key}:")`, so a
`module:` with nothing after it passes. `check_instance` (`check-templates.py:119-128`) globs
`PHASE.md`, `TASKS.md`, `TASK.md`, `PLAN.md`, `DESIGN.md`, `IMPLEMENTATION.md`, `QA.md`,
`REVIEW.md`, `PR.md`, `PHASE_SUMMARY.md` and the decisions — **never `work/*/BUG.md`**. So no real
bug is checked at all, and even if one were, presence is not truth. **`step-intake.md`'s wording is
the entire enforcement of AC-2.** That is acceptable for this task, for a stated reason and not by
default: the alternatives are each a different task's work, and inventing one here is the
speculative scope this step forbids.

What would actually hold it, named so a future task can pick it up rather than rediscover it:

| layer | what it would catch | why not now |
|---|---|---|
| `work/*/BUG.md` added to `INSTANCE_PATHS` | a real bug missing the key entirely | no AC asks; `scripts/` is `plugin`, so it is a clean follow-up |
| a non-empty-value rule, instance mode only | `module:` written blank | template keys are deliberately empty placeholders, so this cannot be a template-mode rule — it is a new checker behaviour, not a schema edit |
| `check-envelopes.py` cross-checking `MODULE:` against the BUG's frontmatter | a dispatch disagreeing with its artifact | `check-envelopes.py` is out of scope by `TASK.md` |

The mitigation available *at this task's altitude* is placement, per `claude-expert`: put the rule
where the mistake would be made — in intake's gather step and again in its write step — and state
its reason, so it survives the case where a reporter is impatient.

**AC-5 is discharged by deleting, not correcting.** The comment's own last clause instructs
deletion "when the scan goes green", and it is green: `check-envelopes.py` was run at design and
reports `✔ all envelopes conform`. Correcting it in place would replace one stale claim with
another — the `BUG.md` window it would newly describe is closed by this very change, in the same
commit. A comment whose condition no longer exists is the thing that made this one wrong.

**Intake never blocks — recorded, not re-litigated.** Settled by human decision under §8.2 on
`TASK.md`. This makes D-029's *"or intake blocks (D11)"* dead prose in an active decision. **That
is a `docs` follow-up, not an edit made here** (D14, D9): D-029 is amended by the module that owns
decisions, in its own task. Recorded as an observation.

**No `D-030`.** The two durable-looking rulings are already recorded elsewhere: intake-never-blocks
is a §8.2 human decision on `TASK.md` awaiting a `docs` amendment to D-029, and the read-never-
re-derive rule *is* D-029. Filing D-030 would create a decision whose text contradicts an active
one — strictly worse than the amendment already identified. Two follow-ups to file, neither by this
task: **(a)** amend D-029's Constrains to drop "or intake blocks"; **(b)** the capability gap in
C-5 — nothing in the `bugfix` workflow holds a tool that can write or amend `BUG.md`, which is
pre-existing and touches intake, reproduce and the correction path alike.

## Test Strategy

There is no test runner; verification is behavioural — run the checks, read the artifacts (per
`claude-expert`). Every "today" figure below was **observed at design time**, not predicted.

**AC-1 — confirmed, not assumed.** Run both, explicitly, because the `test_command` chain contains
neither the second script nor an equivalent (R-3):
- `python3 scripts/check-templates.py` — today: exit 1, `checked 21 templates`, one failure,
  `BUG.md / frontmatter missing: module`. After: exit 0, `✔ all templates conform`, still 21.
- `python3 scripts/test-check-templates.py` — today: exit 1, `ran 15 cases`, `✘ 3 case(s) failed`.
  After: exit 0, 15 cases, 0 failed. The count of 3 matches `case_clean:104`,
  `case_ac1_heading_comparison_skipped:139`, `case_ac2_counted:146` — the only three of fifteen
  asserting `code == 0`, and the failure text names exactly the `BUG.md` key. That the other
  twelve still pass is asserted by the same run reporting zero failures; do not assert it
  separately.
- **Over-fix guard, free from the same run:** `check-templates.py:196` fails
  `frontmatter not in catalogue` on any key beyond `module`, so adding more than one key is caught
  without a second check.

**AC-2 — read-through of the three branches.** Give `step-intake.md` to a reader with no prior
context and a report naming no module. Each of C-3's branches (reporter chooses / derivation
matches exactly one row / nothing matches) must terminate in either a `BUG.md` with a non-empty
`module:` or an ended workflow that wrote nothing. **No branch may terminate in `blocked`.** Then:
`grep -rn "if known" skills/` returns nothing.

**AC-3 — the prose is silent and the heading survives.** `templates/BUG.md`'s `## Scope` comment
names no module; `grep -n module templates/BUG.md` hits the frontmatter only. Removing the `##
Scope` heading by accident is caught by `check-templates.py`'s ordered heading comparison
(`:199-210`), so AC-3 and AC-1 are checked by the same run.

**AC-4 — the chain, plus what the chain cannot see.**
- `python3 scripts/check-envelopes.py` exits 0 with `10 dispatch envelopes` — green today, so this
  is a no-regression check, and stating that is the point: it is not evidence that `MODULE:` now
  has a key behind it, because the checker never reads frontmatter.
- The full `config.md:33` chain exits 0.
- The actual AC-4 evidence is read-through: `step-diagnose.md` states `MODULE:` is read from the
  BUG's `module:`; `step-promote.md` states the task's `module:` is carried, never re-derived;
  `step-reproduce.md` no longer says "identify the module from the symptom".

**AC-5.** `.orqestra/config.md` makes no claim about any check being red; line 33 is byte-identical
to before; the chain exits 0, so the file describes reality.

**Whole-workspace no-regression.** `python3 scripts/check-templates.py --target .orqestra` exits 0.
Note what it proves: the workspace artifacts this task adds still conform. It proves **nothing**
about AC-2, because it never globs `work/*/BUG.md`.
