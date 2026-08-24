---
id: TASK-004
type: design
status: done
updated: 2026-08-25
task: TASK-004
decisions: []
---

## Components

No new components — this task tests behaviour and repairs the skill where the tests expose a gap.

| test | criterion | evidence |
|---|---|---|
| init over an existing workspace | AC-1 | md5 of every file, HEAD, `git status` — all unchanged |
| `--force` with a written PRD | AC-2, AC-3 | PRD md5 identical; report distinguishes KEPT from replaced |
| init in a non-git directory | AC-4 | directory still empty afterwards |
| init with no remote and a `gh` stub that fails auth | AC-5 | both warnings present, init succeeds, workspace conforms |

## Interfaces

Unchanged.

## File Plan

| path | action | purpose |
|---|---|---|
| `skills/init/SKILL.md` | modify | Pre-announcement rule for `--force`, and the non-deletion rule |

## Decisions

- **`--force` announces before it writes, not after.** A report written after the write is a receipt,
  not a warning.
- **`--force` re-scaffolds generated files only.** It never removes `phases/`, `work/`, or the files in
  `decisions/`. Someone asking to re-scaffold config is not asking to discard a project — and that gap
  was open until this task.

## Test Strategy

Five runs across four fixtures, each verified by state comparison rather than by reading the report.
