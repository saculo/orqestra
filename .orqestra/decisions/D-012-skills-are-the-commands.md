---
id: D-012
type: decision
status: active
updated: 2026-08-24
area: structure
supersedes: —
superseded_by: —
---

# D-012 — Plugin skills are the commands — no `commands/` directory

**When:** 2026-08-24 · bootstrap · plugin layout review
**Decision:** orqestra ships `skills/` only. Claude Code namespaces plugin skills from `plugin.json`'s `name`, so `skills/task/` is `/orqestra:task`. Arguments come from `$ARGUMENTS` with `argument-hint` in frontmatter. The `commands/` directory and its 12 files are deleted.
**Why:** The Claude Code docs state that `commands/` is the legacy flat form and that new plugins should use `skills/`. Keeping both meant every invocation was described twice — once in the command, once in the skill it called — which is the same duplication this project removed from §7.7 and from the two planning tails. A second description is a second thing to drift.
**Constrains:** Never add a `commands/` directory. A skill's FOLDER NAME is its invocation name, so renaming a folder renames the command — check every reference before doing it.
