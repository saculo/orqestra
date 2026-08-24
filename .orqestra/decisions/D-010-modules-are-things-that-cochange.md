---
id: D-010
type: decision
status: active
updated: 2026-08-24
area: routing
supersedes: —
superseded_by: —
---

# D-010 — orqestra itself has two modules, not five

**When:** 2026-08-24 · bootstrap · modules.md
**Decision:** The plugin is one module (`skills/`, `agents/`, `commands/`, `templates/`, `.claude-plugin/`); docs is the other.
**Why:** nit split `cli/` and `.claude/` and found every task crossed between them. Splitting templates from skills here would do the same: 'make init produce a valid workspace' touches skills/init and two templates, and D14 would force it into two tasks — shipping a schema without the skill that writes it.
**Constrains:** Split a module only where a change to one genuinely does not imply a change to the other. Adding a CLI (§12) would justify a third module; splitting the plugin by file type would not.
