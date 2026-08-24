---
id: D-011
type: decision
status: active
updated: 2026-08-24
area: routing
supersedes: —
superseded_by: —
---

# D-011 — `task_type` is removed, not kept as a label

**When:** 2026-08-24 · bootstrap · modules.md review
**Decision:** The `task_type` field is deleted from `TASK.md`, from `modules.md`, and from the routing
table in `config.md`. `TASKS.md` and `status` show the **module** instead. `stack` survives as advisory
context only, and is explicitly not a routing input.
**Why:** Once the module row names the agent directly (D-004), nothing branched on `task_type` — and
Rule B (§4.4.1) says a field with no consumer is deleted, not kept for tidiness. Keeping it "as a
label" would have been the exact failure nit's ADR-0007 was written about: registries accumulating
fields nobody reads. The module name is also a better label than the type ever was — "api" and "worker"
say more than "backend" twice.
**Constrains:** Do not reintroduce a type or category field for routing. If a new dimension is genuinely
needed, add a column to `modules.md` and name its consumer before adding it. `stack` may be read for
context but never branched on.
