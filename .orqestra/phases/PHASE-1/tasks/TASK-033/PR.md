---
id: TASK-033
type: pr
status: done
updated: 2026-08-30
task: TASK-033
branch: feat/TASK-033-spec-makes-room-for-diagnose
pr_number: 9
pr_url: https://github.com/saculo/orqestra/pull/9
pr_state: open
---

## Summary

`skills/bugfix/step-diagnose.md` dispatches with no `SKILL:` because there was no skill to name — the
last envelope `check-envelopes.py` cannot pass. This makes room for one.

**D-028** is the durable part: a §4.8.1 `Written by` cell names a skill **iff** the step composes a
dispatch envelope, tested by `grep ROLE:`. That protects `:583` (`BUG.md` | `bugfix` intake), which is
truthful because intake dispatches nothing, while condemning `:584`. Correcting the instance without
the rule would have implied `:583` was wrong too.

The name is fixed once — `diagnose` / `orqestra:diagnose`, `step` class — so TASK-034 has no room to
author a different one and fail a check with nothing to point at.

Three hard-coded skill counts are removed rather than incremented, and §7.12 now names `ls skills/` as
the count and explains why prose cannot hold one.

## Commits

| commit | subject |
|---|---|
| `7b75d75` | TASK-033: plan — the row was written around an absence, in five places |
| `6329fac` | TASK-033: amend AC-3, add AC-4, by human decision (§8.2) |
| `74be275` | TASK-033: design — a writer cell names a skill iff the step dispatches |
| `b93fdb1` | TASK-033: design gate approved |
| `f696c21` | TASK-033: implement — the spec sanctions a diagnose skill, and counts nothing |
| `143065b` | TASK-033: qa — failed, 2 of 4 |
| `5ce1077` | TASK-033: rework — the count in words, diagnose's class, and a true inventory |
| `740536c` | TASK-033: qa round 2 — passed, 4 of 4 |
| `a5a9d7a` | TASK-033: review — passed, 0 required, 2 advisory |
| `9a7bfe6` | TASK-033: review gate approved, and F-1/F-2 filed |

Ten commits, `attempts: 1 of 3`. The failed qa is kept: it is the record of a defect that two thorough
sweeps missed, and the reason the method changed.

## CI

`gh pr checks 9` at 2026-08-30: **no checks reported**. The repository has no CI workflow, so this is
absence rather than pending. No review threads.

| command | result |
|---|---|
| `python3 scripts/check-templates.py` | 21 of 22 catalogue rows, exit 0 |
| `python3 scripts/check-decisions.py` | 28 decisions, exit 0 |
| `python3 scripts/check-step-refs.py` | 40 references, exit 0 |
| `python3 scripts/check-envelopes.py` | **exit 1**, sole hit `step-diagnose.md` — TASK-034's, by design |

No test was added: `scripts/` is the `plugin` module and this task is `docs` (D14). Verification was
therefore a **set-difference against `ls skills/`**, run in both directions — §7.0's class table,
§7.12's grid and the tree are set-identical at 23, with `diagnose` the sole entry present in the spec
and absent from the tree, which is docs leading (D-019). Headings 108/108 identical to master.

That method exists because this task **failed qa 2 of 4**. "Twenty-two skills" was spelled in words and
survived two digit-anchored sweeps, including the orchestrator's. The rework's conclusion is the
durable lesson: no grep can see a missing row, so an enumeration is checked by set-difference, never by
a pattern. Both earlier sweeps searched for what was present; every defect was an absence.
