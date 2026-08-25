---
id: TASK-002
type: design
status: done
updated: 2026-08-25
task: TASK-002
decisions: [D-012, D-013, D-014]
---

<!-- WRITTEN RETROACTIVELY on 2026-08-25. TASK-002 was verified ad hoc on 2026-08-24,
     immediately after the plugin first loaded, before artifact discipline was being
     applied to this project's own tasks. The work and its verification are real and are
     recorded in git history (commits a660327 and c2436d2); only this record is
     after-the-fact. `close-phase` caught the omission — the workspace reported TASK-002
     as `created` and SC-1 as having no evidence, which was accurate. -->

## Components

| component | serves | purpose |
|---|---|---|
| `.claude-plugin/plugin.json` | AC-1 | Manifest; its `name` is the skill namespace |
| `skills/<name>/SKILL.md` | AC-3, AC-4 | The folder name is the invocation name — no `commands/` layer (D-012) |
| `agents/*.md` | AC-5 | 8 personas, dispatched namespaced (D-014) |

## Interfaces

```
claude --plugin-dir .        load from the working tree, no install (D-013)
claude plugin validate .     structural validation
/reload-plugins              pick up edits in-session
```

## File Plan

| path | action | purpose |
|---|---|---|
| `.claude-plugin/plugin.json` | create | Manifest |
| `commands/` | delete | Redundant with `skills/` (D-012) |
| `skills/*/SKILL.md` | modify | Folder-name identity, `argument-hint`, `$ARGUMENTS` |

## Decisions

D-012 (skills are the commands), D-013 (`--plugin-dir` for dogfooding), D-014 (agents dispatch
namespaced) were all recorded from this task's findings.

## Test Strategy

`claude plugin validate .` for structure; a live `-p` session queried for its `orqestra:` skill and
agent lists for reachability.
