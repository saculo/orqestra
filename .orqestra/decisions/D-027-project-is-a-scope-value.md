---
id: D-027
type: decision
status: active
updated: 2026-08-30
area: structure
supersedes:
superseded_by:
---

# D-027 — `PROJECT` is the fourth scope value, and the scope key decides the module class

**When:** 2026-08-30 · PHASE-1/TASK-029 · design
**Decision:** §5.5's scope field carries **exactly one of `TASK` `PHASE` `BUG` `PROJECT`**. `PROJECT:`
marks a dispatch composed before any scope unit exists and carries the project name from
`.orqestra/config.md`. The conditional class (`MODULE` `PATHS` `STACK` `EXPERTISE`) is decided by
**which scope key is present** — mandatory under `TASK` and `BUG`, omitted under `PHASE` and
`PROJECT`, because those units carry no `module:` in their frontmatter.
**Why:** `create-phases` operates on no task, phase, or bug, so no value of the three-value field could
be true; the rule, not the envelope, was wrong. A fourth value keeps one lookup answering both rows —
read the scope key, know the class — instead of a second discriminator (a `READ`-list scan, a step
name) that a reader has to reason about. The Rule B (§4.4.1) objection to a constant-valued field does
not apply: the scope key already has a consumer, since it is what the conditional row keys off; this
extends that consumer rather than inventing an unread field.
**Constrains:** Every future dispatch composed before a scope unit exists carries `PROJECT:` in the
scope position and omits `MODULE` `PATHS` `STACK` `EXPERTISE`; it may not invent a `TASK`/`PHASE`/`BUG`
value to satisfy the row. Every future envelope check decides the module class from the scope key
alone, never from a list of step names. Any new scope unit type must state in §4.8 whether its
frontmatter carries `module:`, because that is what places it on one side of this rule.
