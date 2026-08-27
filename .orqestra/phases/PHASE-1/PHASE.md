---
id: PHASE-1
type: phase
status: pending
updated: 2026-08-26
phase: PHASE-1
criteria_count: 7
---

## Goal

The substrate works: orqestra installs, scaffolds a workspace, and can correctly say where a
project stands. Nothing orchestrates yet.

This phase exists because `status` is the state authority (§7.10) — every later phase calls it — and
because a schema without a template is an unfinished schema (D-003).

## Success Criteria

| id | criterion | verified by |
|---|---|---|
| SC-1 | `claude --plugin-dir .` loads orqestra, `claude plugin validate .` passes, and every skill is invocable as `/orqestra:<name>` | load the plugin in this repo; run `validate`; invoke each skill |
| SC-2 | `/orqestra:init` in an empty git repo produces the complete `.orqestra/` tree, confirms the stack interactively, and commits it as exactly one commit whose message is scoped per `config.md`'s `commit_style` — `orqestra: initialize workspace` under the default `scoped`, by rung 3 of §4.6 | run in a scratch repo; inspect the tree and `git log` |
| SC-3 | `/orqestra:init` refuses to run over an existing `.orqestra/` without `--force`, and never overwrites an existing `PRD.md` | run twice; run with a pre-existing PRD |
| SC-4 | `/orqestra:status` derives the correct stage for every row of the §4.3 table, **including both traps**: an `IMPLEMENTATION.md` with `status: changes-requested` reports `implemented`-in-rework, and a `QA.md` with `result: failed` does not advance the stage | a hand-built fixture tree covering all 8 stages plus both traps |
| SC-5 | Every artifact in the §4.8 catalogue has a template whose frontmatter keys and heading order match the catalogue exactly | a conformance check of `templates/` against §4.8, run as the project's first test |
| SC-6 | `/orqestra:status` on an uninitialized repo says so plainly and suggests `/orqestra:init` rather than erroring | run in a repo with no `.orqestra/` |
| SC-7 | **No orchestrator writes an artifact.** Every artifact in the §4.8 catalogue names a sole writer that holds `Write` and is reached by dispatch, and no skill writes an artifact D1 does not assign it — including `status` and `attempts` | a check over `skills/` frontmatter and write instructions against D1, run alongside the template conformance check |

<!-- SC-2 AMENDED 2026-08-25, by human decision (§8.2).

     It pinned the literal string `chore(orqestra):`. D-018 replaced that convention with
     `scoped`, and TASK-010/TASK-009 implemented it — which left this criterion
     unsatisfiable by the very code written to satisfy it. TASK-010 correctly refused to
     touch it: amending a success criterion is a phase-definition change and a human's
     call, not a task's.

     The amended wording names the CONFIG VALUE first and the literal second. That is the
     lesson from the breakage: a criterion that pins a format string silently expires the
     next time the format changes, and nothing points at the criterion when it does. The
     literal stays because a criterion must be checkable, but it is now labelled as an
     instance of the rule rather than as the rule itself, so the next convention change is
     a one-word edit with its reason already visible.

     TASK-003/QA.md is NOT amended. It records what an actual run produced under the old
     convention and is frozen (D5); rewriting it would falsify a verification that really
     happened. D-018: the convention applies from adoption forward. -->

<!-- SC-7 ADDED 2026-08-26, by human decision (§8.2).

     This one WIDENS the phase, which none of the mid-phase additions before it did. Said
     plainly because the phase's own notes claim otherwise about TASK-008, TASK-009, and
     TASK-010, and that claim should not quietly stop being true.

     The reason it is worth widening for: D1 is the oldest rule in the charter and nothing
     has ever verified it. Running the pipeline on TASK-008 found three skills writing
     artifacts they do not own, four instructions an orchestrator cannot execute, one
     artifact with two writers, and one D1 row naming an orchestrator as the sole writer of
     an artifact no agent is dispatched to write. All of it had been sitting in the
     specification since it was written, invisible, because a charter rule with no criterion
     is a rule nobody checks.

     It belongs in PHASE-1 rather than PHASE-3 because the writer assignments are substrate:
     D1 and the §4.8.1 written-by column, not pipeline behaviour. PHASE-3 exercises the loop;
     this is about who is permitted to hold the pen at all.

     "Verified by" names a CHECK rather than a run, deliberately. SC-5's conformance check
     became test_command and is the reason schema drift now surfaces at all; writer
     discipline earns the same treatment, because the failure mode is identical — a rule
     everyone believes is enforced, enforced nowhere. -->

## Scope

`init`, `status`, all artifact templates, the schema catalogue, `plugin.json`, and the conformance
check that becomes `test_command`.

The plugin source for these already exists as an untested draft. **This phase is about proving it
behaves**, not writing it from scratch — the criteria are behavioural for exactly that reason, so
existing source does not make them met.

## Out of Scope

Any orchestration. No workflow runs in this phase. Also: no state-derivation script (D-001) — if
SC-4 proves prompt-based derivation unreliable, that is a finding for §12, not a fix to make here.
