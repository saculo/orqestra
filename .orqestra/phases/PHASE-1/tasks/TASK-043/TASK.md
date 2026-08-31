---
id: TASK-043
type: task
status: pending
updated: 2026-08-31
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: []
serves: [PHASE-3/SC-1]
attempts: 0
---

## Goal

**Nothing in the `bugfix` workflow can write `BUG.md`.**

`skills/bugfix/SKILL.md:6` declares `disallowed-tools: Write, Edit, NotebookEdit`, so the orchestrator
cannot write. And `step-intake.md` dispatches nobody — `grep '^ROLE:' skills/bugfix/` returns exactly
one hit, `orqestra:analyst` at **diagnose**. So intake has no actor with a tool that can produce the
artifact it exists to produce.

TASK-040 shipped an intake procedure that establishes the module and records it in frontmatter. That
procedure is **inert**: nothing can execute it. D-029's amendment path — *"the BUG's frontmatter is
amended and the dispatch recomposed"* — is stated and unexecutable for the same reason.

Found by TASK-040's implement and named again by its review as *"the `BUG.md` capability gap that makes
C-5's amendment path stated-but-unexecutable"*. Recorded as tech debt in two artifacts and filed here
because tech-debt prose is not a route anyone travels.

**Third instance of one pattern.** TASK-035 covers a registry naming an agent whose tools cannot
perform its step; TASK-041 covers a design step told to write a decision it cannot register; this covers
a workflow told to write an artifact it cannot write. All three surface only at dispatch, and all three
were found by running the pipeline rather than reading it.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | Some actor in the `bugfix` workflow can create `BUG.md`, and the skill that names the obligation is the one that holds the tool |
| AC-2 | The same actor, or a named other, can **amend** it — D-029 requires the frontmatter change when diagnosis finds the module wrong |
| AC-3 | Demonstrated by sequence rather than asserted: a walkthrough shows which step writes, with what tool, at what point |
| AC-4 | `check-envelopes.py`, `check-templates.py` and the `config.md` `test_command` chain still exit 0 |

## Out of Scope

Widening `skills/bugfix/SKILL.md`'s `allowed-tools` reflexively. D-024's two layers make an orchestrator
holding `Write` a real loss — §4.4.5 cites it as the guarantee that no orchestrator patches an artifact.
Dispatching a step that holds `Write` may be the better answer; the design chooses.

`REQUIREMENTS.md` — if §7.3's walkthrough carries the same assumption, report it (D14, D-019).
