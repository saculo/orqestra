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

_none_ — nothing was written. `REQUIREMENTS.md` is **unmodified**; the working tree is clean of
this task. The block is a tool-capability block, not a design block: D-027 is sound, DESIGN.md is
implementable as written, and every input needed to make the five component edits was read.

**Why nothing was written.** This session has `Edit` disabled — `Edit` returns
`No such tool available: Edit. Edit is disabled for this session, in subagents as well as here.`
The only mutation tool available is `Write`, which is **whole-file only** and cannot patch. Making
C1–C4 therefore requires emitting all 2147 lines of `REQUIREMENTS.md` in one `Write` call. The file
measures ~45k tokens for lines 1–1012 alone, so a full round-trip is ~95k output tokens — above the
per-response output ceiling. The call cannot complete; it would truncate, and a truncated
`REQUIREMENTS.md` is the one outcome the envelope's BUDGET clause names as unacceptable
("stop cleanly rather than leaving REQUIREMENTS.md half-edited"). Stopping before the first byte is
that clean stop.

**The work, fully specified, so the retry is mechanical.** All four in-file edits were located and
their exact text settled against the real envelopes. A retry with `Edit` enabled is four
string replacements and no further reading.

**C1 — the scope row, `REQUIREMENTS.md:940`.**

- before: `| the scope — exactly one of `TASK` `PHASE` `BUG` | always | the unit of work the step operates on |`
- after: the same row admitting `PROJECT` as the fourth key, with the condition restated as *which
  scope key the dispatch carries* — `PROJECT` for a dispatch composed before any scope unit exists,
  valued with the project name from `.orqestra/config.md` `project:` (D-027).

**C2 — the conditional row, `REQUIREMENTS.md:941`.**

- before: `| `MODULE` `PATHS` `STACK` `EXPERTISE` | conditional | mandatory **iff** the scope unit has a module — its `TASK.md`/`BUG.md` frontmatter carries `module:`. `create-phases` and `create-tasks` run before any task has one and omit all four; that is conformant, not an exception |`
- after: the condition keyed off the scope key alone — mandatory under `TASK` and `BUG`, omitted
  under `PHASE` and `PROJECT`, because `templates/PHASE.md` frontmatter carries no `module:` and a
  `PROJECT` dispatch has no scope unit at all. **The named-steps clause goes**; naming steps is
  precisely the defect F-4 records, and no replacement list appears (D-027, DESIGN.md C2).

**C3 — the scope-field rationale paragraph**, one short paragraph inserted between the *"Paths,
never contents"* paragraph (`:930-932`) and *"Which fields are mandatory"* (`:934`): what the scope
field is, and why `PROJECT` exists — a project-wide dispatch has no unit to name, and a rule no
envelope can satisfy is a broken rule (house convention: every rule states its reason).

**C4 — the F-3 fix, `REQUIREMENTS.md:872`.** `EXPERTISE: java-expertise, test-quality` →
`EXPERTISE: java-expertise, spring-conventions`, matching §5.1's `api` row at `:731` character for
character. Confirmed by reading both lines.

**C5 — `decisions/D-027-project-is-a-scope-value.md`** already exists, `status: active`, with its
`Constrains` line filled. Cited above, not rewritten (D9).

**The risk the envelope named, verified against the real files before stopping.** Under C2 the four
module fields stay MANDATORY for every `TASK`- and `BUG`-scoped envelope, because the key is what
decides and those keys sit on the mandatory side. Checked by reading the actual envelope lines:

| envelope | scope line | the four fields |
|---|---|---|
| `skills/task/step-implement.md` | `:35` `TASK: PHASE-1/TASK-041` | `:36-39` `MODULE: worker`, `PATHS: services/worker`, `STACK: python`, `EXPERTISE: python-expertise, celery-conventions` — all four present, all four still required |
| `skills/task/step-qa.md` | `:12` `TASK: PHASE-1/TASK-007` | `:13-16` `MODULE: api`, `PATHS: services/api`, `STACK: java`, `EXPERTISE: java-expertise, spring-conventions` — all four present, all four still required |
| `skills/task/step-review.md` | `:17` `TASK: PHASE-1/TASK-007` | `:20-23` `MODULE: api`, `PATHS: services/api`, `STACK: java`, `EXPERTISE: java-expertise, spring-conventions` — all four present, all four still required |

The same read confirms the other side: `close-phase/SKILL.md:41` (`PHASE: PHASE-1`),
`add-phase/step-define-phase.md:19` (`PHASE: PHASE-<N>`) and `greenfield/step-tasks.md:17`
(`PHASE: PHASE-1`) carry no `MODULE`/`PATHS`/`STACK`/`EXPERTISE` and become conformant unchanged —
that is F-4 — while `bugfix/step-diagnose.md:10-14` (`BUG: BUG-003`) carries all four and keeps
having to. No currently-caught omission becomes legal.

**Verification commands not run.** `check-templates.py`, `check-decisions.py` and
`check-step-refs.py` were not executed: no `Bash` tool is available in this session either, and with
zero files changed there is nothing for them to regress. They were at 0 before this task and the
tree is byte-identical to that state. `check-envelopes.py` still exits 1 on
`greenfield/step-phases.md`, unchanged and expected — TASK-030 owns it (D-019).

## Deviations

| deviation | from design | what | why |
|---|---|---|---|
| _none_ | — | — | — |

## Tech Debt

_none_ — nothing was built, so nothing was shortcut. Noted for whoever retries: this session had
neither `Edit` nor `Bash`, so any `docs`-module task touching `REQUIREMENTS.md` is unexecutable
under that tool set, regardless of how small the edit is. The file's size, not the edit's, is what
decides.
