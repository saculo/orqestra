---
id: TASK-048
type: task
status: pending
updated: 2026-09-01
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: [TASK-046]
serves: [SC-7]
attempts: 0
---

## Goal

**Every step is dispatched to a subagent. Today 8 of 27 step files are.**

A standing architectural rule, set by a human on 2026-09-01. It is not a refactor: it is what makes
writer discipline mechanically checkable for the first time.

| | step files |
|---|---|
| **dispatch** (8) | `define-phase` · `diagnose` · `phases` · `plan-design` · `tasks` · `implement` · `qa` · `review` |
| **inline** (19) | `preflight` ×3 · `handoff` ×3 · `push` · `merge` · `task/pr-comments` · `intake` · `reproduce` · `promote` · `clarify` · all six of `pr-comments` |

`close-phase` dispatches from `SKILL.md` rather than a step file, and counts as dispatching.

**Why this is the enforcement TASK-046 could not provide.** That task removes `disallowed-tools` from
six skills, because D-031 measured that the denial reaches dispatched subagents and overrides their
persona's `tools:`. That is necessary and it costs the only mechanism §4.4.5 cited as the guarantee
that no orchestrator patches an artifact. Prose is TASK-046's interim answer. **If no step runs inline,
the guarantee becomes checkable**: every step file carries exactly one `ROLE:` envelope with exactly one
`WRITE:` path, and an orchestrator with nothing to write in the first place cannot be the writer. That
is a `grep`, not a promise — and it is what `disallowed-tools` was believed to be and never was.

**The rule collides with three interactive sites, and the collision has a clean resolution.** A subagent
cannot reach the human, and three places depend on that reachability — two of them say so in the file:

| site | what depends on the human |
|---|---|
| `skills/greenfield/SKILL.md:67`, `skills/clarify/SKILL.md:8` | *"a subagent between the human and their own questions makes the conversation useless"* |
| `skills/bugfix/step-intake.md:22-35` | the module re-ask loop, steps 1-4 — *"a human is present at intake by construction"* |
| every gate | `AskUserQuestion` is held by the orchestrator |

**Split by capability instead of deleting them: the orchestrator asks, the subagent writes.** The
orchestrator is the only actor that can reach the human, so it keeps `AskUserQuestion` and keeps the
conversation. Every artifact write goes through a dispatch, with the conversation's *outcome* carried
in the envelope. Intake becomes: the orchestrator runs the re-ask loop, then dispatches `analyst` with
the settled `module:` in the envelope, and the analyst writes `BUG.md`. Clarify becomes two dispatches
around a conversation — the analyst returns the question list, the orchestrator asks, the analyst
writes `CLARIFICATIONS.md`. Neither property is given up.

**Not every inline step needs an agent, and saying so is part of the work.** `preflight`, `handoff`,
`push` and `merge` run `git`, `gh` and checks and write nothing an agent owns; `task/pr-comments`
delegates to a skill. The rule's purpose is that **no artifact is written outside a dispatch** — a step
that writes no artifact is a different case and the task must say which of the 19 are which, rather
than composing an envelope for a step with nothing to declare.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | Every step that writes an artifact carries a `ROLE:` envelope with exactly one `WRITE:` path — `intake`, `reproduce`, `promote`, `clarify` and the writing steps of `pr-comments` included |
| AC-2 | Every step that writes **nothing** is classified as such explicitly, with its reason, so the distinction is recorded rather than left as an absence someone later reads as an oversight |
| AC-3 | A checker enforces AC-1 and AC-2 over `skills/`, fails on a writing step with no envelope, and is added to the `test_command` chain. It goes green in this task rather than being added ahead of the conversion |
| AC-4 | The interactive sites still reach the human: `clarify`'s question loop and `intake`'s module re-ask loop each demonstrably run with the reporter, **verified by a run**, with the write performed by a dispatched agent |
| AC-5 | D-028 is reconciled — its `grep ROLE:` test currently classifies a direct `Skill:` invocation as neither dispatch nor inline, and `step-promote.md` sits in that gap today |

## Out of Scope

**`REQUIREMENTS.md`.** `docs` (D14). §4.8.1's `Written by` column changes meaning wholesale once every
writer is dispatched, and D-028 is the decision that governs that column — AC-5 reconciles the decision,
the catalogue rewrite is reported. Likely a `docs` task of its own; flagged, not assumed.

**Removing `disallowed-tools`.** TASK-046, which must land first — a dispatched writer under a denying
caller still holds no `Write` (D-031), so converting a step to a dispatch before that fixes nothing.

**`pr-comments`' source-editing defect.** TASK-050 covers it as its own subject: it needs per-module
dispatch, `PATHS` enforcement and a recorded commit SHA, not merely an envelope.

**Whether an orchestrator should hold `AskUserQuestion` at all.** This task assumes yes, because
nothing else can reach the human. If gates should instead be their own artifact, that is TASK-016 and
audit finding 5.
