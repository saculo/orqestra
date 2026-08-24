---
id: D-005
type: decision
status: active
updated: 2026-08-24
area: workflow
supersedes: —
superseded_by: —
---

# D-005 — Planning stops at design; delivery is a separate per-task pipeline

**When:** 2026-08-24 · pre-project · spec
**Decision:** greenfield, add-phase, and bugfix all end when every task has a `DESIGN.md`. `/orqestra:task <ID>` then takes one task to a merged PR.
**Why:** Separating them makes delivery independently resumable per task, lets a human review a whole phase of designs at once, and keeps the two orchestrator kinds small enough to shard cleanly.
**Constrains:** No planning workflow may implement, branch, or push. The delivery pipeline re-checks design freshness at preflight, because designs are written before the tasks ahead of them merge.
