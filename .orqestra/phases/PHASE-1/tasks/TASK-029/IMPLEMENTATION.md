---
id: TASK-029
type: implementation
status: done
updated: 2026-08-30
task: TASK-029
deviation: none
files_changed: 1
---

## Changes

One file changed: `REQUIREMENTS.md`, +11 −3, all four amendments inside §5.5's body. Nothing under
`skills/`, `scripts/` or `agents/` was touched, and no section was renumbered — `§5.5.1` and everything
after it are byte-identical, so no `§N` citation in any of the ~90 citing files breaks.

**C1 — the scope row of §5.5's obligation table.**

- before: `| the scope — exactly one of `TASK` `PHASE` `BUG` | always | the unit of work the step operates on |`
- after: `| the scope — exactly one of `TASK` `PHASE` `BUG` `PROJECT` | always | which unit of work the step operates on. `PROJECT` is the dispatch composed before any scope unit exists; its value is the project name from `.orqestra/config.md` `project:` (D-027) |`
- intent: a dispatch composed before any phase, task or bug exists now has a value it can truthfully
  carry, instead of satisfying the row by inventing a unit. Serves AC-1, AC-2.

**C2 — the conditional row (`MODULE` `PATHS` `STACK` `EXPERTISE`).**

- before: `| ... | conditional | mandatory **iff** the scope unit has a module — its `TASK.md`/`BUG.md` frontmatter carries `module:`. `create-phases` and `create-tasks` run before any task has one and omit all four; that is conformant, not an exception |`
- after: `| ... | conditional | mandatory **iff** the scope key is `TASK` or `BUG` — those units carry `module:` in their frontmatter. Omitted under `PHASE` and `PROJECT`: `templates/PHASE.md` carries no `module:`, and a `PROJECT` dispatch has no scope unit at all. The scope key decides, never a list of step names (D-027) |`
- intent: one lookup — read the scope key, know the class. The named-steps clause is **gone** and no
  replacement list appears; naming steps in the rule is precisely defect F-4. Serves AC-2, AC-3.

**C3 — the scope-field paragraph**, inserted between *"Paths, never contents"* and *"Which fields are
mandatory"*: what the scope field is, and why `PROJECT` exists — `create-phases` runs when the project
has no phase, task or bug to name, and a rule no conformant envelope can satisfy is a broken rule, not
a strict one. Reason stated with the rule, per house convention. Serves AC-1.

**C4 — §5.5's example envelope, the `EXPERTISE` line.** `java-expertise, test-quality` →
`java-expertise, spring-conventions`, now matching §5.1's `api` row character for character. Serves
AC-3 (F-3).

**C5** — `decisions/D-027-project-is-a-scope-value.md` already existed from the design step,
`status: active`, `Constrains` filled. Cited, not rewritten (D9). Not counted in `files_changed`.

**The risk the design named — widening the conditional row too far — re-verified this run.** The four
module fields remain MANDATORY for every `TASK`- and `BUG`-scoped envelope, because under C2 the scope
key decides and `TASK`/`BUG` sit on the mandatory side. The three `TASK`-scoped envelopes, re-read after
the edit:

| envelope | scope line | the four fields |
|---|---|---|
| `skills/task/step-implement.md` | `:35` `TASK: PHASE-1/TASK-041` | `:36-39` `MODULE: worker`, `PATHS: services/worker`, `STACK: python`, `EXPERTISE: python-expertise, celery-conventions` — still required |
| `skills/task/step-qa.md` | `:12` `TASK: PHASE-1/TASK-007` | `:13-16` `MODULE: api`, `PATHS: services/api`, `STACK: java`, `EXPERTISE: java-expertise, spring-conventions` — still required |
| `skills/task/step-review.md` | `:17` `TASK: PHASE-1/TASK-007` | `:20-23` `MODULE: api`, `PATHS: services/api`, `STACK: java`, `EXPERTISE: java-expertise, spring-conventions` — still required |

The widening reaches only the `PHASE`/`PROJECT` side, where no envelope carries the four fields today.
No currently-caught omission becomes legal.

**Verification.** `python3 scripts/check-templates.py` — 21 templates, all conform, exit 0.
`python3 scripts/check-decisions.py` — 27 decisions, all conform, exit 0. `python3
scripts/check-step-refs.py` — 40 references, all resolve, exit 0. `check-envelopes.py` was deliberately
not run to a passing state: it still enforces `SCOPE = ["TASK","PHASE","BUG"]` and will keep exiting 1
on `greenfield/step-phases.md`. That is expected, not a regression — TASK-030 owns the checker and the
ten envelope edits (D-019: `docs` states the rule, `plugin` applies it).

## Deviations

| deviation | from design | what | why |
|---|---|---|---|
| _none_ | — | — | — |

## Tech Debt

The spec now says `PROJECT` is a legal scope key while `scripts/check-envelopes.py` and all ten real
envelopes still say otherwise — the repository is intentionally inconsistent between this task merging
and TASK-030 landing. Anyone reading `check-envelopes.py`'s output in that window sees a failure that
is by design; TASK-030 closes it, and nothing here should be "fixed" first (D3, D14).
