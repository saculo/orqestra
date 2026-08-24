---
id: TASK-004
type: implementation
status: done
updated: 2026-08-25
task: TASK-004
deviation: minor
files_changed: 1
---

## Changes

`skills/init/SKILL.md` — two rules the tests showed were missing:

1. **Announce before writing under `--force`.** The skill said only "refuse unless `--force`"; nothing
   required it to say what `--force` would destroy. The first run reported what it had replaced
   *afterwards*, which happened to be informative and is not a safeguard. The skill now specifies the
   list — what will be replaced, what will be kept — printed before any write, with confirmation where
   `AskUserQuestion` exists.

2. **`--force` must not delete planning state.** Nothing said so. `--force` re-scaffolds the generated
   files; `phases/`, `work/`, and the individual files under `decisions/` survive. A user asking to
   re-scaffold config is not asking to discard a project, and the gap between those two readings was
   entirely unwritten.

## Deviations

| severity | from design | what | why |
|---|---|---|---|
| minor | not planned | Added the non-deletion rule alongside the announcement rule | Found while writing the announcement: listing what `--force` keeps forced the question of what it is even allowed to remove, which nothing had specified |

## Tech Debt

_none_
