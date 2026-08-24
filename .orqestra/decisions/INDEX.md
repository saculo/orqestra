---
id: DECISIONS
type: decisions-index
status: done
updated: 2026-08-24
count: 14
next_id: 15
---

## Decisions

| id | decision | area | status | summary |
|---|---|---|---|---|
| D-001 | No CLI in v1 | runtime | active | Skills + Markdown only; state derivation confined to `status` as a swap seam |
| D-002 | Artifacts are the state | state | active | No ledger file; stage derived from artifact presence + frontmatter |
| D-003 | Markdown schemas, not JSON Schema | schemas | active | Frontmatter keys, ordered headings, fixed columns; template + orchestrator enforce |
| D-004 | The module row is the whole routing key | routing | active | The row names the agent directly — no type enum in between |
| D-005 | Planning stops at design | workflow | active | Delivery is a separate per-task pipeline |
| D-006 | One file per decision + index | state | active | Index read every dispatch; detail opened on demand |
| D-007 | Step files named, never numbered | structure | active | Order lives in the SKILL.md index table |
| D-008 | Gates via AskUserQuestion | ux | active | Write `awaiting-approval` first so gates survive a session |
| D-009 | Every step commits its artifacts | version-control | active | Planning history becomes git history; revert works |
| D-010 | orqestra has two modules | routing | active | Modules are things that co-change — do not split by file type |
| D-011 | `task_type` is removed | routing | active | No consumer once the row names the agent; `stack` stays advisory only |
| D-012 | Skills are the commands | structure | active | No `commands/` dir — the skill folder name is the invocation name |
| D-013 | `--plugin-dir` for dogfooding | runtime | active | Loads the working tree live; marketplace packaging deferred to PHASE-5 |
| D-014 | Agents dispatch namespaced | routing | active | Registry stores `backend-engineer`; dispatch uses `orqestra:backend-engineer` |
