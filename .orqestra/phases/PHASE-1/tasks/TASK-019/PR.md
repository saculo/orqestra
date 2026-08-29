---
id: TASK-019
type: pr
status: done
updated: 2026-08-29
task: PHASE-1/TASK-019
branch: feat/TASK-019-agents-invoke-their-skills
pr_number: 4
pr_url: https://github.com/saculo/orqestra/pull/4
pr_state: open
---

## Summary

Every agent's `tools:` allowlist omitted `Skill`, so no dispatched agent could invoke the step skill
carrying its procedure or the expertise skills carrying this project's conventions. Under D-024 that
list binds the whole subagent run, so §5.0's triple delivered one of its three layers. All eight
personas carried an instruction none could execute.

Four links, each existing because the one before it cannot be trusted alone: **grant** `Skill` in all
eight personas · **instruct** invocation by name, never by path · **supply** `SKILL:` in 9 of 10
dispatch envelopes · **detect** with `SKILLS:` opening every dispatched skill's `## Return`. The grant
alone is the defect restated; the instruction is not a guarantee, because `tools:` grants a
capability and cannot compel its use. Recorded as **D-025**.

The PR also carries `c227381`, which closes the route that let this task be built with no plan and no
design: preflight gains a fourth check that backfills `plan` → `design` → re-gate rather than
blocking, plus §7.4.3, §7.10.1, and the `status` reporting fix.

AC-2, AC-3, AC-4 and AC-6 verified. AC-1 and AC-5 were removed and re-filed as TASK-031 and TASK-030,
not dropped.

## Commits

| commit | subject |
|---|---|
| `b40d90d` | TASK-019: agents invoke their step and expertise skills |
| `c9fd23e` | TASK-019: make every envelope carry its mandatory fields, and check it |
| `6f59426` | TASK-019: stop the persona bullet expanding the token it describes |
| `5705eb6` | TASK-019: implement — record the work, and close two gaps it found |
| `44cb405` | TASK-019: qa — failed, 4 of 6 |
| `6631d38` | TASK-019: rework — SKILLS: first in every Return contract (I-3) |
| `e05fca9` | PHASE-1: split TASK-019's unreachable criteria into four tasks |
| `bcb7164` | TASK-019: qa round 2 — failed, 3 of 4 |
| `7a9febd` | TASK-019: rework — D-025 carries its Constrains (AC-4) |
| `f747fad` | TASK-019: qa round 3 — passed, 4 of 4 |
| `c227381` | orqestra: no task reaches implement without a plan and a design |
| `089f54f` | TASK-019: review — passed, 0 required |
| `9e7dec4` | TASK-019: review gate approved |
| `33124eb` | TASK-019: backfill plan and design |

Fourteen commits. The first three are the source change, committed by direct human instruction before
any pipeline artifact existed — the omission this task's own review caught, and which `c227381`
closes at the pipeline level.

## CI

`gh pr checks 4` at 2026-08-29: **no checks reported** on this branch. The repository has no CI
workflow, so this is absence rather than pending — nothing will arrive later.

The suite is run by hand and passed before push: `check-decisions.py` 25 decisions / 0 findings,
`check-templates.py` 20 templates conform, `test-check-envelopes.py` 19/19 — all exit 0.
`check-envelopes.py` exits 1 on two envelopes, both owned by TASK-024 and TASK-030 and left red
deliberately. `config.md`'s `test_command` is `check-templates.py` alone, which is the narrower of
the four.
