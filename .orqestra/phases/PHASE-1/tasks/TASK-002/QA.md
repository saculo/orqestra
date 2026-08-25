---
id: TASK-002
type: qa
status: done
updated: 2026-08-25
task: TASK-002
result: passed
test_command: claude plugin validate .
---

<!-- WRITTEN RETROACTIVELY on 2026-08-25. TASK-002 was verified ad hoc on 2026-08-24,
     immediately after the plugin first loaded, before artifact discipline was being
     applied to this project's own tasks. The work and its verification are real and are
     recorded in git history (commits a660327 and c2436d2); only this record is
     after-the-fact. `close-phase` caught the omission — the workspace reported TASK-002
     as `created` and SC-1 as having no evidence, which was accurate. -->

## Test Strategy

Structural validation, then a live session queried for what it can actually see.

## Results

```
$ claude plugin validate .
✘ skills/reject/SKILL.md — YAML frontmatter failed to parse
    "At runtime this skill loads with empty metadata (all frontmatter fields
     silently dropped)."
  → fixed (argument-hint was double-quoted), then:
✔ Validation passed          (also with --strict)

$ claude --plugin-dir . -p "list orqestra skills"
  22 skills, all namespaced /orqestra:<folder-name>

$ claude --plugin-dir . -p "list orqestra subagents"
  8 agents, all namespaced orqestra:<agent>   ← the finding behind D-014
```

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | `--plugin-dir .` loads with no plugin errors | passed |
| AC-2 | `plugin validate .` passes, including `--strict` | passed |
| AC-3 | live session lists all 22 skills as `/orqestra:<name>` | passed |
| AC-4 | every skill has a description; the 8 taking arguments declare `argument-hint` and read `$ARGUMENTS` | passed |
| AC-5 | live session lists all 8 agents | passed |

## Issues

**Three defects, all invisible to review:**

1. `skills/reject` had unparseable frontmatter — it would have loaded with **no description**, never
   triggered, and reported nothing.
2. Eight skills declared `argument-hint` but never read `$ARGUMENTS` — the handling had lived in the
   deleted `commands/` files.
3. Plugin agents are namespaced, so every envelope's bare `ROLE: backend-engineer` would have failed on
   the first real dispatch in PHASE-3 (D-014).

**Process note**: this task's criteria were verified on 2026-08-24; these artifacts were written on
2026-08-25 after `close-phase` reported the omission. The verification is not reconstructed — it is in
git history — but the record is.
