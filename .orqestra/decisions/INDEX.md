---
id: DECISIONS
type: decisions-index
status: done
updated: 2026-08-31
count: 30
next_id: 31
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
| D-015 | A `failed` review is a gate | workflow | active | `changes-requested` loops to implement; `failed` asks a human, re-review allowed once |
| D-016 | Rework routes to the owner | workflow | active | Findings carry `owner`; rework goes to who fixes it, not who found it. **Due PHASE-3** |
| D-017 | `failed` states its reversal | schemas | active | `## What Would Change This Verdict`, schema-enforced. **Delivered** — heading added to `REVIEW.md` alongside D-022 |
| D-018 | Commits scoped by owning work | process | active | `TASK-NNN:` / `PHASE-N:` / `orqestra:` — most specific scope that owns the change |
| D-019 | Spec-first when skills cite it | process | active | Code that *cites* a section inherits it, so docs leads; code that *reads* it may follow |
| D-020 | Design states structure, not files | schemas | active | `## File Plan` removed; the architect sets boundaries, the engineer picks paths |
| D-021 | `PROJECT.md` records what is expensive to find | schemas | active | Cost-to-retrieve test; `## Testing`/`## Git and GitHub`/`## Traps` added, git rules ship pre-written |
| D-022 | Severity is the only grade | schemas | active | `required` column dropped; `required: [F-N]` in frontmatter is what the rework loop reads |
| D-023 | Review has a floor | workflow | active | Four contract checks run whatever the lenses; fixes qa grading its own coverage |
| D-024 | Tool fields enforce at two layers | structure | active | `allowed-tools` only pre-approves; `agents/` `tools:` is the durable allowlist; orchestrators bind for one turn |
| D-025 | Agents hold `Skill`; the triple composes by invocation | structure | active | `Skill` in every `agents/` `tools:`; `SKILL`/`EXPERTISE` invoked not read; `SKILLS:` in every return |
| D-026 | Reference shape follows how the file is loaded | structure | active | Index cells carry `${CLAUDE_PLUGIN_ROOT}`; prose and `step-*.md` use plugin-relative — the variable is inert under `Read` |
| D-027 | `PROJECT` is the fourth scope value | structure | active | Scope is one of `TASK` `PHASE` `BUG` `PROJECT`; the scope key alone decides whether `MODULE`/`PATHS`/`STACK`/`EXPERTISE` are mandatory |
| D-028 | A catalogue writer cell names a skill iff the step dispatches | schemas | active | §4.8.1's `Written by` names a skill when the step composes an envelope, workflow-plus-step when it runs inline; `grep ROLE:` is the test |
| D-029 | A `BUG` carries `module:` in its frontmatter | schemas | active | §4.8.1 lists `module` on `BUG.md`; intake establishes it, `## Scope` stops carrying it, diagnose and promote read it |
| D-030 | Historical artifacts are not migrated | schemas | active | An artifact that conformed when written is not amended for a later rule; `--target .orqestra` is a diagnostic with 19 known failures, never a gate |
