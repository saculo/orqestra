---
id: TASK-029
type: implementation
status: blocked
updated: 2026-08-30
task: TASK-029
deviation: none
files_changed: 0
---

## Changes

_none_ — `REQUIREMENTS.md` is **unmodified** and the working tree is clean of this task. The block
is unchanged in effect but its **cause is now identified**, which the previous run did not do.

**The grant landed in a file the harness does not load.** `agents/architect.md:4` does read
`tools: Skill, Read, Write, Edit, Glob, Grep, Bash` — commit d2d1a41 is real and correct. But the
tool set this session actually holds is `Skill, Read, Write, Glob, Grep`: no `Edit`, no `Bash`.
`Edit` returns `No such tool available: Edit. Edit is disabled for this session, in subagents as
well as here.` The reason is visible in the tree: the plugin's **skills** are installed at
`.claude/skills/orqestra/`, and there is **no installed copy of `agents/` anywhere** — both
`.claude/agents/*.md` and `.claude/**/agents/*.md` glob to zero files. So `agents/architect.md`'s
body reaches the subagent as its persona while its `tools:` allowlist — the one layer that binds
for a whole subagent run (§7.0.1, D-024) — is never read. **Editing `agents/architect.md` again
cannot fix this.** What a human must do is install or sync the plugin's `agents/` directory to
wherever the harness loads subagent definitions from, then re-dispatch; the fix is in the
installation, not in the repository.

**Why `Write` was not used instead.** The envelope forbids it and the ban is right.
`REQUIREMENTS.md` is 122,615 bytes / 2147 lines; a whole-file `Write` means re-emitting ~31k tokens
of prose verbatim, at or over the output ceiling. Truncation is one failure mode, silent drift in
reproduced prose is the worse one — this file is cited by number from ~90 other files, so a
paraphrased paragraph corrupts citations without failing any check. Stopping before the first byte
is the clean stop the BUDGET clause asks for.

**The four edits, settled to copy-paste text, so the retry is four string replacements.**

**C1 — the scope row, `:940`.**

- before: `` | the scope — exactly one of `TASK` `PHASE` `BUG` | always | the unit of work the step operates on | ``
- after: `` | the scope — exactly one of `TASK` `PHASE` `BUG` `PROJECT` | always | which unit of work the step operates on. `PROJECT` is the dispatch composed before any scope unit exists; its value is the project name from `.orqestra/config.md` `project:` (D-027) | ``
- intent: the key, not a judgement, answers the row — and a dispatch operating on every phase now
  has a value it can truthfully carry.

**C2 — the conditional row, `:941`.**

- before: `` | `MODULE` `PATHS` `STACK` `EXPERTISE` | conditional | mandatory **iff** the scope unit has a module — its `TASK.md`/`BUG.md` frontmatter carries `module:`. `create-phases` and `create-tasks` run before any task has one and omit all four; that is conformant, not an exception | ``
- after: `` | `MODULE` `PATHS` `STACK` `EXPERTISE` | conditional | mandatory **iff** the scope key is `TASK` or `BUG` — those units carry `module:` in their frontmatter. Omitted under `PHASE` and `PROJECT`: `templates/PHASE.md` carries no `module:`, and a `PROJECT` dispatch has no scope unit at all. The scope key decides, never a list of step names (D-027) | ``
- intent: one lookup answers both rows, and **the named-steps clause goes** — naming steps is
  precisely defect F-4, and no replacement list appears.

**C3** — one paragraph inserted between *"Paths, never contents"* (`:930-932`) and *"Which fields
are mandatory"* (`:934`): what the scope field is, and why `PROJECT` exists — a project-wide
dispatch has no unit to name, and a rule no envelope can satisfy is a broken rule (house
convention: every rule states its reason). No renumbering; `§5.5.1` and after are untouched.

**C4 — F-3, `:872`.** `EXPERTISE: java-expertise, test-quality` →
`EXPERTISE: java-expertise, spring-conventions`, matching §5.1's `api` row at `:731` character for
character. Both lines re-read this run and confirmed.

**The risk the envelope named, re-checked against the real envelope lines this run.** The four
module fields stay MANDATORY for every `TASK`- and `BUG`-scoped envelope, because under C2 the key
decides and `TASK`/`BUG` sit on the mandatory side:

| envelope | scope line | the four fields, verified |
|---|---|---|
| `skills/task/step-implement.md` | `:35` `TASK: PHASE-1/TASK-041` | `:36-39` `MODULE: worker`, `PATHS: services/worker`, `STACK: python`, `EXPERTISE: python-expertise, celery-conventions` — still required |
| `skills/task/step-qa.md` | `:12` `TASK: PHASE-1/TASK-007` | `:13-16` `MODULE: api`, `PATHS: services/api`, `STACK: java`, `EXPERTISE: java-expertise, spring-conventions` — still required |
| `skills/task/step-review.md` | `:17` `TASK: PHASE-1/TASK-007` | `:20-23` `MODULE: api`, `PATHS: services/api`, `STACK: java`, `EXPERTISE: java-expertise, spring-conventions` — still required |

The widening reaches only the `PHASE`/`PROJECT` side, where no envelope carries the four fields
today. No currently-caught omission becomes legal.

**Out of scope, untouched as instructed.** Nothing under `skills/`, `scripts/` or `agents/` was
modified. `check-envelopes.py` will still exit 1 on `greenfield/step-phases.md`; TASK-030 owns the
checker and the ten envelope edits (D-019). **C5** — `decisions/D-027-project-is-a-scope-value.md`
— already exists, `status: active`, `Constrains` filled; cited, not rewritten (D9).

**Verification commands not run.** `check-templates.py`, `check-decisions.py` and
`check-step-refs.py` need `Bash`, which this session does not hold. With zero files changed there
is nothing to regress: all three were at 0 before this task and the tree is byte-identical.

## Deviations

| deviation | from design | what | why |
|---|---|---|---|
| _none_ | — | — | — |

## Tech Debt

The `docs` module is **unbuildable by any subagent until the plugin's `agents/` directory is
installed.** `REQUIREMENTS.md` is 122,615 bytes, so every `docs` task needs `Edit` regardless of
how small its change is — the file's size decides, not the edit's. Two consecutive runs have now
blocked here. Worth a preflight check in `skills/task/`: a dispatch whose engineer lacks `Edit`
for a module whose `paths` contain a file over some size should fail at compose time, not after a
full subagent run. Not fixed — `skills/` is the `plugin` module (D3, D14).
