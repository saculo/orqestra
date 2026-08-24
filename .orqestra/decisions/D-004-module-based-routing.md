---
id: D-004
type: decision
status: active
updated: 2026-08-24
area: routing
supersedes: —
superseded_by: —
---

# D-004 — The module row is the whole routing key

**When:** 2026-08-24 · pre-project · spec
**Decision:** Every task names one `module` from `.orqestra/modules.md`. That row names the **agent
directly**, plus the stack and the expertise skills. There is no `task_type` enum and no second routing
table.
**Why:** A Spring service and a Celery worker are both "backend" while sharing nothing; `stack` alone
cannot tell Spring from Quarkus. And an enum of engineer types could not express `docs`, whose natural
owner is the architect — picking a type just to reach an agent was contortion. One key also removes a
class of contradiction: a task cannot claim one language while its module is another.
**Constrains:** Never set an agent, stack, or expertise independently of the module row. A task naming
a module not in the registry blocks (D11); so does a row naming an agent with no file in `agents/`.
