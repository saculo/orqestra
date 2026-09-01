---
id: TASK-046
type: task
status: pending
updated: 2026-09-01
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: []
serves: [SC-7]
attempts: 0
---

## Goal

**An orchestrator that denies `Write` cannot cause a write by any route inside its own turn — dispatch
included. Six skills deny it.**

D-031 probed the tool fields live rather than reading them. Three measured results, none of them in
D-024:

| probe | result |
|---|---|
| Invoke a skill declaring `disallowed-tools: Write`, then `Write` | removed, *"for this session, in subagents as well as here"* |
| Then dispatch a subagent whose persona declares `tools: … Write, Edit …` | **removed there too.** `Bash` survives |
| Then invoke a skill whose `allowed-tools` lists `Write` | **still removed.** `allowed-tools` never grants |

`add-phase`, `bugfix`, `close-phase`, `greenfield`, `task` and `status` all declare
`disallowed-tools: Write, Edit, NotebookEdit`. Only the user's next message restores the pool. So every
one of these workflows appears to run today **only because a human message falls between every step**.

`skills/task/SKILL.md:108` rule 2 requires calling `orqestra:status` at preflight. `status` denies
`Write` — and it is the case worth stating plainly, because it is the least intuitive: a **read-only**
skill that denies a tool it never uses disables that tool for the orchestrator that called it, and for
every agent that orchestrator then dispatches. `task` invokes `status`, then dispatches `implement`,
which must write `IMPLEMENTATION.md`.

**The mechanism is at once too strong and too weak.** Too strong: it does not stop the orchestrator
writing, it stops everything downstream in the turn from writing. Too weak: `bugfix`, `task` and
`close-phase` hold `Bash`, and a heredoc writes fine — for those three the §4.4.5 guarantee is not
weak, it is **absent**.

**Why this is not TASK-011, TASK-027, or TASK-043.** All three name symptoms of it and all three chose
a remedy the probe has since disproved. TASK-011 lists four sites where an orchestrator is told to
write while its `disallowed-tools` denies it, and routes the fix to dispatch; TASK-027 AC-1 implements
that; TASK-043 chose "invoke a `Write`-holding skill from the `bugfix` orchestrator" and flagged as its
own Risk 1 that the approach dies if `Write` does not survive. It does not survive. Dispatch is not
sufficient and invocation is not sufficient. This task establishes the premise those three rest on, so
it lands first — it is not their duplicate, it is what makes their remedies executable.

**The remedy, decided by a human on 2026-09-01 and not to be re-opened at design.** The six skills
drop `disallowed-tools: Write, Edit, NotebookEdit`. Narrowing `allowed-tools` instead was rejected as
documentation shaped like a control; stripping `Bash` was rejected as needing its own investigation,
since those three use it for `git` and `gh`.

**What replaces the guarantee — amended 2026-09-01, same day.** This task was filed saying prose was
the only available answer, on the argument that no skill-level tooling can enforce writer discipline:
`allowed-tools` never restricts and `Bash` routes around any denial. A human then set a standing
architectural rule — **every step is dispatched to a subagent** — which makes a *mechanical* answer
available after all. If no step runs inline, a checker can assert that every step file carries exactly
one `ROLE:` envelope with exactly one `WRITE:` path, which is the property `disallowed-tools` was
believed to provide and never did. That checker ships with **TASK-048**, alongside the conversion of
the 19 step files that do not dispatch today — it cannot be green before them. So prose is this task's
interim answer and TASK-048 is the enforcement, and the prose must say so rather than presenting
itself as the end state.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | No skill under `skills/` denies `Write`, `Edit` or `NotebookEdit` to a caller that must reach a writer — grepping the frontmatter of `add-phase`, `bugfix`, `close-phase`, `greenfield`, `task` and `status` returns no such field |
| AC-2 | **Demonstrated by run, not asserted.** One turn, no intervening human message: a workflow calls `orqestra:status` and then reaches a writer, and the artifact exists on disk afterwards. This defect was invisible to reading; a walkthrough on paper does not satisfy this |
| AC-3 | Every affected orchestrator states the never-write obligation as a rule, **says it is a rule rather than a tooling guarantee**, and names TASK-048 as where enforcement lands — so no later reader re-adds `disallowed-tools` believing it enforces something, and nobody mistakes the interim answer for the final one |
| AC-4 | `REQUIREMENTS.md` §4.4.5 and §7.0.1 are **reported, not touched** — §4.4.5 cites the missing `Write`/`Edit` as the guarantee that an orchestrator does not patch an artifact, and that claim is now false in both directions |
| AC-5 | `check-envelopes.py`, `check-templates.py` and the `config.md` `test_command` chain still exit 0 |

## Out of Scope

**`REQUIREMENTS.md`.** `docs` module (D14), and the skills *cite* §4.4.5 rather than restating it, so
docs leads (D-019). AC-4 reports it; TASK-011 owns the correction. Whether that ordering makes TASK-011
a dependency of this task rather than a consequence of it is a sequencing call a human should make —
flagged, not assumed.

**Converting the 19 inline step files to dispatches, and the checker that enforces it.** TASK-048.
This task only makes the tool pool reach a dispatched writer; it does not change who is dispatched.

**Removing `Bash` from `bugfix`, `task` and `close-phase`.** It would close the heredoc route and it is
the only thing that would, but those three use `Bash` for `git` and `gh`. Its own investigation.

**Re-planning TASK-043, TASK-011, TASK-016, TASK-027 or TASK-028.** All five rest on the disproved
assumption and all five need revisiting once this lands, but a task does not edit another task (D3).
TASK-043's `PLAN.md` in particular is invalidated at its Approach, not merely amended.

**Amending SC-7.** Its wording — *"names a sole writer that holds `Write` and is reached by dispatch"* —
treats dispatch as sufficient to confer `Write`, which the probe disproves. Amending a success criterion
is a phase-definition change and a human's call (§8.2). Reported here so it is not lost.

**`skills/bugfix/step-reproduce.md` and `SKILL.md:30` disagreeing about whether reproduce dispatches.**
TASK-043's Open Question 3; a separate capability gap with no bearing on the tool pool.
