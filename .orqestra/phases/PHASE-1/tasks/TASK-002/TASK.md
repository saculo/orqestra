---
id: TASK-002
type: task
status: done
updated: 2026-08-29
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
depends_on: []
serves: [SC-1]
attempts: 0
---

## Goal

orqestra loads as a Claude Code plugin from its own directory, validates structurally, and every skill
is reachable under the `/orqestra:` namespace.

This is what makes the tool runnable in its own repository, and therefore what makes every later
criterion in this phase testable at all.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | `claude --plugin-dir .` loads orqestra with no plugin errors in the `/plugin` Errors tab |
| AC-2 | `claude plugin validate .` passes; any warning it reports is either fixed or recorded with a reason |
| AC-3 | Every skill folder is invocable as `/orqestra:<folder-name>`, verified one by one rather than by inspecting files |
| AC-4 | Every skill carries a `description` written to trigger correctly, and each skill taking arguments carries an `argument-hint` and reads `$ARGUMENTS` |
| AC-5 | All 8 agents appear under Custom Agents in `/context`, and `/reload-plugins` picks up an edit to a skill without a restart |

## Out of Scope

Whether the skills themselves behave correctly — this proves loading and reachability, not the work.
`init` is TASK-003, `status` is TASK-005.

**Marketplace packaging.** `marketplace.json` and `/plugin install` are distribution, deferred to
PHASE-5. Development and dogfooding use `--plugin-dir`, which needs no marketplace (D-013).
