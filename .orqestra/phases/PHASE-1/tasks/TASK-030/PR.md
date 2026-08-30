---
id: TASK-030
type: pr
status: done
updated: 2026-08-30
task: TASK-030
branch: feat/TASK-030-every-envelope-conforms
pr_number: 8
pr_url: https://github.com/saculo/orqestra/pull/8
pr_state: open
---

## Summary

`check-envelopes.py` still asked whether a scope *unit* had a module, reaching into `TASK.md`/`BUG.md`
frontmatter and carrying step names as exceptions. TASK-029 replaced that rule in §5.5 with one keyed
off the **scope key** (D-027); this puts it in the checker. Scope is one of `TASK` `PHASE` `BUG`
`PROJECT`; the four module fields are required under `TASK`/`BUG` and **forbidden** under
`PHASE`/`PROJECT` — forbidden, because §5.5 calls carrying them "a violation, not a harmless extra".

`skills/greenfield/step-phases.md` gains `PROJECT: orqestra` and conforms without inventing a value.

The check still **exits 1**, on `skills/bugfix/step-diagnose.md` alone. That is the deliverable, not an
oversight: greening it needs a skip-list or a fabricated `SKILL`, which Out of Scope forbids and which
D-025 makes actively harmful since the value is invoked. TASK-033 then TASK-034 close it.

This task was **split** (§8.2) after plan found its dependency premise false — TASK-024 never touched
diagnose, and authoring the skill also makes §4.8.1:584 wrong, so the work spans two modules.

## Commits

| commit | subject |
|---|---|
| `9e45c42` | TASK-030: plan — blocked, needs-splitting |
| `9b3591f` | PHASE-1: split TASK-030 — the diagnose half becomes TASK-033 and TASK-034 |
| `ff7e3e8` | TASK-030: design — the conditional class becomes scope-keyed |
| `2c654ea` | TASK-030: design gate approved |
| `a1c5dac` | TASK-030: implement — the conditional class is keyed off the scope |
| `b951cb1` | TASK-030: qa — passed, 8 of 8 |
| `a2f0f16` | TASK-030: review — passed, 0 required, 0 advisory |
| `2ca3036` | TASK-030: review gate approved, and test_command says why it is red |

Eight commits. The blocked plan is kept: it records that the split was found before implement ran, not
after qa failed it — which is what TASK-019's AC-5 cost when the same class of defect was found late.

## CI

`gh pr checks 8` at 2026-08-30: **no checks reported**. The repository has no CI workflow, so this is
absence rather than pending. No review threads.

| command | result |
|---|---|
| `python3 scripts/test-check-envelopes.py` | 25 cases, 25 pass, exit 0 — was 19 |
| `python3 scripts/check-envelopes.py` | **exit 1**, one finding: `step-diagnose.md` missing `SKILL` — by design, TASK-034 |
| `python3 scripts/check-templates.py` | 21 of 22 catalogue rows, exit 0 |
| `python3 scripts/check-decisions.py` | 27 decisions, exit 0 |
| `python3 scripts/check-step-refs.py` | 40 references, exit 0 |
| `python3 scripts/test-check-templates.py` | 15 cases, exit 0 |
| `python3 scripts/test-check-step-refs.py` | 28 cases, exit 0 |

`config.md`'s `test_command` now chains `check-envelopes.py`, so **the whole suite exits 1** until
TASK-034 lands. A comment beside it names the envelope, names the tasks that close it, and instructs
its own deletion when the scan goes green.

The evidence that carries weight is the mutation run: eight mutants applied to a scratch copy of the
checker, **all killed**, including `exactly-one → at-least-one` on the scope key and the prohibition
turned into a no-op. Review then found those mutants asymmetric — `PHASE` and `TASK` are never
dropped — checked the gaps are covered by real cases, and noted qa had itself found and closed a path
its own mutants missed.
