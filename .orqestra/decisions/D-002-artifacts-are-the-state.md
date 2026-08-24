---
id: D-002
type: decision
status: active
updated: 2026-08-24
area: state
supersedes: —
superseded_by: —
---

# D-002 — Artifacts are the state

**When:** 2026-08-24 · pre-project · spec
**Decision:** No `state.json`, no `STATE.md`, no ledger. Every artifact carries frontmatter with `status`; position is derived by globbing `.orqestra/` and reading it.
**Why:** A separate state file desyncs from the artifacts it describes. BMAD discovers progress by scanning output locations; that model has no second source of truth to reconcile.
**Constrains:** No task may introduce a file whose only job is recording status. Recovery is therefore file operations — deleting an artifact is how a step is redone (§8.1).
