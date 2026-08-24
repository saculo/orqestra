---
id: TASK-003
type: design
status: done
updated: 2026-08-24
task: TASK-003
decisions: []
---

## Components

| component | serves | purpose |
|---|---|---|
| `check_instance()` in the checker | AC-2 | Validate a real `.orqestra/` workspace, not just `templates/` |
| `INSTANCE_PATHS` + glob patterns | AC-2 | Map catalogue rows onto where artifacts actually land |
| Conditional-key support (`` `name?` ``) | AC-2 | A field required on the template but conditional on an instance |
| `skills/init/SKILL.md` corrections | AC-1, AC-3, AC-4 | Template fidelity, bare agent names, non-interactive honesty |

## Interfaces

```
python3 scripts/check-templates.py --target <workspace-dir>
```

Absent artifacts are **not** failures: a workspace legitimately contains only what its workflows have
produced so far. Only artifacts that exist and are wrong count.

## File Plan

| path | action | purpose |
|---|---|---|
| `scripts/check-templates.py` | modify | Instance mode, conditional keys |
| `skills/init/SKILL.md` | modify | The corrections the runs exposed |
| `skills/**/*.md` | modify | `${CLAUDE_PLUGIN_ROOT}` on every template path |

## Decisions

- **Instance mode is the same catalogue, applied to real files.** One parser, two targets — a second
  ruleset would be a second source of truth.
- **`${CLAUDE_PLUGIN_ROOT}` on every template reference.** Bare `templates/X.md` resolves against the
  *user's* project, which is not where the plugin's templates are.
- **Conditional keys are marked in the catalogue, not hard-coded** — the same shape as the
  no-common-frontmatter marker.

## Test Strategy

Three `init` runs in three fresh repos (Java, Java again after fixes, TypeScript), each checked with
`--target`. Verify the commit is single and scoped to `.orqestra/`. AC-3 verified only as far as
non-interactive sessions allow.
