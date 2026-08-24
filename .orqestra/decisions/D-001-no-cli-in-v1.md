---
id: D-001
type: decision
status: active
updated: 2026-08-24
area: runtime
supersedes: —
superseded_by: —
---

# D-001 — No CLI in v1

**When:** 2026-08-24 · pre-project · spec
**Decision:** orqestra ships as skills, agents, commands, and Markdown. No CLI, no build step, no runtime dependency beyond `git` and `gh`.
**Why:** nit put its state machine in a Bun CLI and paid for it in install friction, version skew between plugin and CLI, and 26 JSON schemas that grew because a validator existed. BMAD and GSD both keep the workflow LLM-interpreted and use code only for config resolution and filesystem queries.
**Constrains:** No task may add a compiled or interpreted runtime. State derivation stays confined to the `status` skill so it can become `state.cjs` later without touching anything else (§7.10).
