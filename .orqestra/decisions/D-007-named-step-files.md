---
id: D-007
type: decision
status: active
updated: 2026-08-24
area: structure
supersedes: —
superseded_by: —
---

# D-007 — Step files are named, never numbered

**When:** 2026-08-24 · pre-project · spec
**Decision:** Orchestrator shards are `step-preflight.md`, `step-push.md`. Order lives only in the step index table in `SKILL.md`.
**Why:** A numeric prefix encodes sequence in two places, so inserting a step means renaming every file after it and updating every cross-reference. This document hit exactly that problem with its own section numbers.
**Constrains:** Never add a numeric prefix to a step file. Reordering a workflow edits the index table only.
