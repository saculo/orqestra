---
id: TASK-014
type: task
status: pending
updated: 2026-08-26
phase: PHASE-1
module: docs
stack: markdown
origin: feature
bug:
depends_on: []
serves: [SC-4]
attempts: 0
---

## Goal

**`status` is forbidden from reading the configuration it is required to read.**

`skills/status/SKILL.md` declares `config.md` an input, for gate modes and `require_merged_deps`. Its
Rules say "Read frontmatter, never bodies. **No exceptions.**" Both values live in Markdown body
sections of `config.md`, not its frontmatter. The rule and the input list contradict each other, and
whichever an implementation follows, the other is violated.

The frontmatter-only rule is right for *artifacts* — it is what keeps the state authority cheap and is
why bodies never enter an orchestrator's context. `config.md` is not an artifact in that sense: it is
configuration, it has no lifecycle, and no step derives a stage from it.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | §7.10 distinguishes reading **artifact** frontmatter from reading **configuration**, and permits the second explicitly |
| AC-2 | The reason is stated, not just the permission — frontmatter-only exists for context economy over many artifacts, which does not apply to one config file read once |
| AC-3 | The rule names exactly which files the exception covers, so it cannot be stretched to artifact bodies later |

## Out of Scope

`skills/status/SKILL.md` itself — `plugin`, and it follows this (D-019).
