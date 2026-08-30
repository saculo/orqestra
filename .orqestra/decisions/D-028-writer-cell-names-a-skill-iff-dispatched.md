---
id: D-028
type: decision
status: active
updated: 2026-08-30
area: schemas
supersedes:
superseded_by:
---

# D-028 — A §4.8.1 "Written by" cell names a skill exactly when the step is envelope-dispatched

**When:** 2026-08-30 · PHASE-1/TASK-033 · design
**Decision:** The `Written by` column of the §4.8.1 catalogue has one discriminator, and it is
**whether the step composes a dispatch envelope**. A step that dispatches a subagent is a step that
has a `SKILL:` (§5.5 makes `SKILL` an always-class field), so its row names that skill bare and alone
— `` `plan` ``, `` `design` ``, `` `qa` ``, `` `diagnose` ``. A step that runs inline in the
orchestrator's own turn composes no envelope and therefore has no skill to name; its row names the
**workflow plus the step** — `` `bugfix` intake ``. The test is mechanical: `grep ROLE:` the
workflow's `step-*.md` files. A `ROLE:` line means a dispatch, means a skill, means a skill name in
the cell.
**Why:** Both forms already appear in the column, and without a stated rule the two are
indistinguishable — which is how §4.8.1:584 came to describe `DIAGNOSIS.md`'s writer as
`` `bugfix` diagnose `` while §5.5 simultaneously required that same step to carry a `SKILL:`. The
spec disagreed with itself in the one table whose job is to say who writes what. A rule keyed on
"does it dispatch" is answered by looking at the step file, so a reviewer never has to reason about
intent; and it makes the column's shape carry information rather than noise — the reader learns from
the cell alone whether a subagent produced the artifact.
**Constrains:** Every future row added to §4.8.1 picks its `Written by` form by this test, not by
resemblance to a neighbouring row. Any "consistency" edit that rewrites `` `bugfix` intake `` into a
skill name is a regression and must be rejected: `intake`, `reproduce`, `promote` and `handoff`
dispatch nobody, and naming a skill that does not exist is worse than naming none (D-025 — a `SKILL`
value is invoked). Conversely, promoting an inline step to a dispatched one obliges the same commit
to author its skill and amend its catalogue cell, because the envelope's always-class row (§5.5) is
unsatisfiable otherwise.
