---
id: TASK-007
type: task
status: pending
updated: 2026-08-24
phase: PHASE-1
module: docs
stack: markdown
origin: feature
depends_on: [TASK-001]
serves: [SC-5]
attempts: 0
---

## Goal

`REQUIREMENTS.md` describes the tree that actually exists. Its catalogue, counts, and cross-references
match what ships.

The specification is cited by number from roughly ninety files, so a stale catalogue row or a wrong
count is not cosmetic — it is a citation that sends a reader somewhere wrong.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | Every row of the §4.8 catalogue corresponds to a shipped template, and every shipped artifact template has a catalogue row — verified by the TASK-001 check, with any mismatch resolved on whichever side is wrong |
| AC-2 | Every count stated in prose matches reality: the skill inventory in §7.12, the artifact count in §4.8, and the agent list in §5.4 |
| AC-3 | Every `§n.n` and `D-n` citation in the specification resolves to a section that exists |
| AC-4 | Any rule the specification states that no shipped skill implements is either implemented or removed from the specification — a rule nothing enforces is worse than no rule, because it is trusted |

## Out of Scope

Changing any behaviour. This task edits `REQUIREMENTS.md` only; where reconciliation requires a
template or skill to change, that is a `plugin` task and gets created separately (D14 — one task, one
module).

Rewriting the specification's structure or renumbering sections. Renumbering breaks every citation
across the plugin (D-007's reasoning applied to sections).
