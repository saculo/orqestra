---
id: D-008
type: decision
status: active
updated: 2026-08-24
area: ux
supersedes: —
superseded_by: —
---

# D-008 — Gates are asked via AskUserQuestion

**When:** 2026-08-24 · pre-project · spec
**Decision:** A gate sets the artifact `awaiting-approval`, then asks via `AskUserQuestion` with real options. `/orqestra:approve` and `/orqestra:reject` exist for resuming a gate in a new session.
**Why:** Gates are the most frequent interaction — dozens per phase — so they must be one keystroke, and they can offer more than a binary (split a task, accept findings as debt). A tool call does not survive a session boundary, which is why the status is still written to disk.
**Constrains:** Every gate writes `status: awaiting-approval` BEFORE asking. A gate that only asks is unresumable.
