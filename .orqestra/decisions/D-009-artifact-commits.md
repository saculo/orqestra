---
id: D-009
type: decision
status: active
updated: 2026-08-24
area: version-control
supersedes: —
superseded_by: —
---

# D-009 — Every completed step commits its artifacts

**When:** 2026-08-24 · pre-project · spec
**Decision:** Planning steps commit `.orqestra/` paths on the current branch; delivery steps commit on the task branch so the record travels with the PR.
**Why:** Planning history becomes git history — `git log -- .orqestra/` shows how the design evolved, and a bad phase plan is undone with `git revert` rather than hand-editing Markdown. It also makes deleting an artifact a safe way to redo a step.
**Constrains:** Commit after the contract check passes, never before. A rejected gate does not revert its commit — the record of what was tried is the value.
