---
id: D-014
type: decision
status: active
updated: 2026-08-24
area: routing
supersedes: —
superseded_by: —
---

# D-014 — Agents dispatch under the plugin namespace

**When:** 2026-08-24 · PHASE-1 / TASK-002 verification
**Decision:** `modules.md` stores the bare agent name (`backend-engineer`); every dispatch envelope and
`Task` call uses the namespaced type (`orqestra:backend-engineer`).
**Why:** Found by running it. Claude Code namespaces plugin agents exactly as it namespaces plugin
skills, so a dispatch to the bare name would not resolve. Every envelope in the spec and the step files
had the bare name, so the first real dispatch of PHASE-3 would have failed — a defect that no amount of
re-reading found, and that one `-p` invocation surfaced immediately.
**Constrains:** Every envelope's `ROLE` is `orqestra:<agent>`. Keep the registry bare so it stays
readable and so the namespace lives in exactly one place — the dispatch.
