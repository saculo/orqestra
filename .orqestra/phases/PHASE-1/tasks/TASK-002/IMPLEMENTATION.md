---
id: TASK-002
type: implementation
status: done
updated: 2026-08-25
task: TASK-002
deviation: moderate
files_changed: 26
---

<!-- WRITTEN RETROACTIVELY on 2026-08-25. TASK-002 was verified ad hoc on 2026-08-24,
     immediately after the plugin first loaded, before artifact discipline was being
     applied to this project's own tasks. The work and its verification are real and are
     recorded in git history (commits a660327 and c2436d2); only this record is
     after-the-fact. `close-phase` caught the omission — the workspace reported TASK-002
     as `created` and SC-1 as having no evidence, which was accurate. -->

## Changes

- `.claude-plugin/plugin.json` — manifest; `name: orqestra` becomes the skill namespace.
- **`commands/` deleted** (12 files). Claude Code namespaces plugin skills from the manifest, so
  `skills/task/` *is* `/orqestra:task`; the docs state `commands/` is the legacy flat form. A parallel
  command file per skill described every invocation twice (D-012).
- **`approve`, `reject`, `unblock` created as skills.** Deleting `commands/` exposed that they had
  existed *only* as commands — §8.2's recovery protocol had documented entry points with nothing behind
  them.
- Skill folders renamed to their invocation names (`orchestrate-task` → `task`), `argument-hint` added,
  `$ARGUMENTS` handling written into the 8 skills that take arguments.

## Deviations

| severity | from design | what | why |
|---|---|---|---|
| moderate | not planned | Deleted `commands/` entirely | Verified against the Claude Code docs rather than memory; the layer was redundant and drift-prone |
| moderate | not planned | Created three missing skills | The deletion exposed commands with no implementation |

## Tech Debt

_none_
