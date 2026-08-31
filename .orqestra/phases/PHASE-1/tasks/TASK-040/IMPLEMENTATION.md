---
id: TASK-040
type: implementation
status: done
updated: 2026-08-31
task: TASK-040
deviation: minor
files_changed: 7
---

## Changes

**C-1 — the `BUG` frontmatter key** (AC-1). `templates/BUG.md` gains `module:` between `updated:`
and `bug:`, commented as the routing key per `templates/TASK.md`'s convention. Placement is free —
`check-templates.py:192-197` compares key sets, not order.

**C-2 — `## Scope` stops carrying the module** (AC-3). The same file's `## Scope` guidance now reads
"who and what is affected — users, data, environments, blast radius" and states that the module is
`module:` in the frontmatter *and only there* (D-029). The heading itself is untouched.

**C-3 — intake establishes the module** (AC-2). `skills/bugfix/step-intake.md` rewritten: the gather
bullet no longer offers "if known", and a new `## Establish the module` section holds the five-rule
procedure — closed choice over `modules.md`'s `module` column shown with each row's `paths`,
derivation from the observed surface against `paths`, a derived candidate offered back rather than
written silently, **re-ask and never block** (with its reason: `BUG.md` is intake's only artifact so
a `blocked_reason` has nowhere to live; §4.4.3's list is closed; D11, D7), and never write `module:`
empty or fall back to `## Scope`. `## Write` repeats the two rules at the point of the write, and the
report line shows `module: api` instead of `surfaces in api`. `skills/bugfix/SKILL.md`'s intake
summary and Rule 4 — the two other places intake's contract is restated — now match.

**C-4 — reproduce reads instead of re-deriving** (AC-4). `skills/bugfix/step-reproduce.md:7` now
reads `module:` from `BUG.md` and loads that row's expertise, with the negative rule beside it.

**C-5 — diagnose composes from the key** (AC-4). `skills/bugfix/step-diagnose.md` states above the
worked example that `MODULE` comes from the BUG's `module:` and the other three from that one
`modules.md` row, and that the example illustrates while the rule governs. A new `## When the fix
lands in another module` section holds the correction path: the analyst states the difference and
cannot fix it (D2, no `Edit`); the gate block carries a `MODULE` line when the two differ; on
approval the key is amended and any dispatch naming the old value is recomposed. It also states
plainly (§7.0.1) that no actor in the workflow holds a tool that can amend `BUG.md` — pre-existing
and identical for every write to it.

**C-6 — promote carries the key** (AC-4). `skills/bugfix/step-promote.md` states the produced task's
`module:` is the BUG's, read from frontmatter, never re-derived from the symptom or the diagnosis,
and that a diagnosis-time correction was already applied at the gate.

**C-7 — the stale comment is deleted** (AC-5). `.orqestra/config.md` lines 34-40 removed, as their own
text instructed once the scan went green. Line 33 (`test_command`) is byte-identical. The file
belongs to no module (`modules.md:45-47`), so this crossed no boundary.

**Verification — every check run directly, not through the `&&` chain.** Baseline captured first.

| check | before | after |
|---|---|---|
| `python3 scripts/check-templates.py` | **exit 1** — `BUG.md / frontmatter missing: module` | **exit 0** — `checked 21 templates`, `✔ all templates conform` |
| `python3 scripts/test-check-templates.py` | **exit 1** — `ran 15 cases`, `✘ 3 case(s) failed` | **exit 0** — 15 cases, `✔ all cases pass` |
| `python3 scripts/check-envelopes.py` | exit 0 | exit 0 |
| `python3 scripts/test-check-envelopes.py` | exit 0 | exit 0 |
| `python3 scripts/check-step-refs.py` | exit 0 | exit 0 |
| `python3 scripts/test-check-step-refs.py` | exit 0 | exit 0 |
| `python3 scripts/check-decisions.py` | exit 0 | exit 0 |

**The three failing cases closed are the three PLAN named** — confirmed by reading the failure
output, not assumed: `clean tree exits 0`, `AC-1 no-headings row: the heading comparison is skipped,
not the row`, `AC-2 the decision row is reported as checked`. The other twelve still pass, asserted
by the same run reporting zero failures.

**`test_command` chain: passes end to end**, exit 0
(`check-templates.py && test-check-envelopes.py && check-envelopes.py`).

**Read-through evidence (AC-2, AC-3, AC-4).** `grep -rn "if known" skills/` → 0 hits.
`grep -n module templates/BUG.md` → the frontmatter key and the `## Scope` comment's pointer *to*
that key, nothing else. Every branch of C-3 terminates in a `BUG.md` with a non-empty `module:` or a
workflow that ended having written nothing; none terminates in `blocked`.

**`scripts/` was not touched.** AC-2 is held by `step-intake.md`'s wording alone, as the design
states; no checker was widened.

## Deviations

| deviation | from design | what | why |
|---|---|---|---|
| minor | `## Test Strategy` — "`check-templates.py --target .orqestra` exits 0" | It exits **1**, and did so identically before this change (verified by `git stash`: byte-identical output before and after, zero mentions of `BUG`). Failures are pre-existing schema drift in `TASK-001/REVIEW.md` (`frontmatter missing: required, review_round`; `headings missing: ## What Would Change This Verdict`) and `TASK-009/DESIGN.md` (`headings missing: ## Structure`). | The design asserted a baseline that was never green. Nothing built here changed it, and fixing those artifacts is other tasks' work (D3). Recorded rather than silently dropped, because the design named this run as no-regression evidence and a reader would otherwise expect a 0. |
| minor | `## Components` prose says "Six components" while its table lists C-1…C-7 | Built all seven, per the table and the dispatch. | The count sentence disagrees with its own table; the table is the specification. No scope question — C-7 is the AC-5 work the table, `TASK.md` and the dispatch all name. |

## Tech Debt

- **AC-2 rests entirely on prose, and the checker cannot catch a violation.** `module:` written
  empty passes `check-templates.py` (`line.startswith(f"{key}:")`), and `check_instance` never globs
  `work/*/BUG.md`, so no real bug is checked at all. The design names this and the three layers that
  would close it (add `work/*/BUG.md` to `INSTANCE_PATHS`; a non-empty-value rule in instance mode
  only; `check-envelopes.py` cross-checking `MODULE:` against the BUG's frontmatter). Each is a
  separate task in `plugin`; none was in scope here.
- **D-029's `Constrains` still says "or intake blocks (D11)"**, which the §8.2 human decision on
  `TASK.md` made dead prose. Amending it is a `docs` edit (D14, D9) and was not made here.
- **No actor in the `bugfix` workflow holds a tool that can write or amend `BUG.md`.** The
  orchestrator disallows `Write`/`Edit` (`skills/bugfix/SKILL.md:6`) and the analyst has no `Edit`.
  Pre-existing, and identical for intake's creation, reproduce's `## Reproduction` update, and the
  new correction path. The rule is stated at the step that decides the correction; closing the
  capability gap is a separate task.
- **`check-templates.py --target .orqestra` is red on two pre-existing artifacts** — see Deviations.
  Not this task's module boundary problem, but it means that run cannot serve as a clean workspace
  no-regression signal until those two artifacts are brought to schema.
- **The worked examples name modules this repo does not have** (`api`, `java`,
  `spring-conventions`). Correct as illustrations; `step-diagnose.md` now says so explicitly so a
  reader does not try to match them against `modules.md`. Left as-is (D3).
