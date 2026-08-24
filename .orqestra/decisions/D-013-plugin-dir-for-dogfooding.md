---
id: D-013
type: decision
status: active
updated: 2026-08-24
area: runtime
supersedes: —
superseded_by: —
---

# D-013 — `--plugin-dir` is the development and dogfooding mechanism

**When:** 2026-08-24 · bootstrap · dogfooding bootstrap
**Decision:** `claude --plugin-dir .` loads orqestra from its own working tree; `/reload-plugins` picks up edits in-session; `claude plugin validate .` checks structure. Marketplace packaging is deferred to PHASE-5.
**Why:** Dogfooding requires orqestra to be runnable in its own repository, but it cannot install itself from a marketplace before the marketplace work exists — a bootstrap deadlock. `--plugin-dir` dissolves it: the working tree is live, so a skill edited in a session is testable in that same session. It also removes marketplace packaging from PHASE-1, where it was scope nothing needed yet.
**Constrains:** Development and every dogfooding run use `--plugin-dir`, never an install. Do not add `marketplace.json` before PHASE-5 — no earlier phase needs it.
