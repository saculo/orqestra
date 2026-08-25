---
id: D-019
type: decision
status: active
updated: 2026-08-25
area: process
supersedes: —
superseded_by: —
---

# D-019 — Order a spec/plugin pair by whether the code reads the spec or cites it

**When:** 2026-08-25 · PHASE-1 / TASK-009 · pipeline run failed qa 3 of 5
**Decision:** When a change spans `docs` and `plugin` (D14, two tasks), the order is decided by **how
the implementation uses the specification**:

| the code… | order | why |
|---|---|---|
| **reads** the spec at run time | plugin first, docs reconciles after | The code parses whatever the spec says; a stale spec produces a visible failure the checker reports |
| **cites** the spec as its instruction | **docs first**, then plugin | The code inherits the spec's content. A stale spec is silently obeyed, and no plugin-side change can override it |

**Why:** This has now bitten twice, in opposite directions.

- **TASK-001 → TASK-007** (checker parses §4.8.1): plugin-first worked. The checker *read* the
  catalogue, so its two defects surfaced as reported failures and docs fixed them after.
- **TASK-009 → TASK-010** (skills cite §4.6): plugin-first was unsatisfiable. 13 of 17 commit sites say
  only "Commit (§4.6)" — they defer. While §4.6 documented the old convention, those sites resolved to
  it no matter what the plugin task changed, and three of five acceptance criteria could not be met from
  inside the module. Found by qa, not by review of the plan: commit `6ff876a` on
  `feat/TASK-009-commits-identified-by-task-id`.

Both times the plan looked sound. The difference is invisible until you ask which artifact is the source
of the behaviour.

**Constrains:** Before splitting a change across `docs` and `plugin`, grep the affected skills for
citations of the section being changed. **A skill that cites a section inherits it** — so the docs task
goes first and the plugin task depends on it. Only when the code parses the spec as data may the plugin
task lead.
