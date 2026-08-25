---
id: D-018
type: decision
status: active
updated: 2026-08-25
amended: 2026-08-25          # rung 3 broadened — see **Amendment**
area: version-control
supersedes: —
superseded_by: —
---

# D-018 — Commits are scoped by the work that owns them, not typed by the kind of change

**When:** 2026-08-25 · PHASE-1 / TASK-009 · implement
**Decision:** `commit_style: scoped` replaces `commit_style: conventional`. Every commit is
`<scope>: <subject>`, where the scope is the **most specific scope that owns the change**:

The scope is chosen by a **ladder**, taken in order, that always terminates:

| | test | scope | example |
|---|---|---|---|
| 1 | A task owns the change — any commit made while that task is in flight, source or artifact | `TASK-NNN` | `TASK-008: add instance-mode heading guard` |
| 2 | Otherwise, a phase's planning owns it — `create-phases`, `create-tasks`, `clarify` | `PHASE-N` | `PHASE-2: plan phases — 5 phases, ordering rationale` |
| 3 | Otherwise — `init` scaffolding, workspace configuration, or repo-wide work no task covers | `orqestra` | `orqestra: initialize workspace` |

The subject line stays free prose. Only the prefix is constrained.

**Why:** The type prefix carried almost nothing. Nearly every commit this project makes is a `fix` or a
`chore`, and picking between them is guesswork at the moment of writing — a rule that resolves to a coin
flip is not a rule. The task id is the thing a reader actually needs: it leads to `TASK.md` for the goal
and acceptance criteria, `DESIGN.md` for why it was built that way, `REVIEW.md` for what was found, and
the phase success criterion the work serves. One prefix turns `git log --oneline` into an index into the
workspace.

`commit_style: conventional` also had a second defect: it named a convention without defining how to
pick within it. Three skills deferred to a setting whose semantics lived only in the reader's head.
`scoped` is defined where it is declared, in `templates/config.md`, and the selection rule is **total** —
every commit has exactly one correct scope, so no judgement is left at the moment of writing.

**Constrains:** Every skill that commits, from now on:

- Read `commit_style` from `config.md`. **Never hard-code a commit format** — `init` did, and that is
  why this convention had to be changed in two kinds of place instead of one.
- **Never emit a conventional-commit type prefix.** `feat(`, `fix(`, `chore(`, `docs(`, `test(` must not
  appear in any commit message a skill produces. Grepping `skills/` and `templates/` for those five
  strings must return nothing.
- A commit made while a task is in flight carries **that task's id**, artifact commits included (§4.6) —
  not the id of whatever produced the artifact.

**No history rewrite.** The convention applies from adoption forward. Rewriting the ~20 commits that
predate it would break every SHA already cited in artifacts and decisions.

## Amendment — 2026-08-25

**Rung 3 was too narrow, and the totality claim was false as written.** The original row read *"No phase
exists yet — `init` scaffolding, workspace-level configuration"*, which is a **precondition**, not a
fallback. The first commit to test it fell straight through: a repo-wide correction to the specification
and the plugin, owned by no task, made while PHASE-1 was very much in flight. No row matched, and the
rule that was advertised as leaving no judgement at the moment of writing required exactly that.

Rung 3 now reads *"otherwise"*. The ladder terminates by construction, which is what "total" has to mean
— a rule is only total if its last rung is unconditional. The three rungs are unchanged in what they
select; only the third stopped claiming a precondition it did not need.

Found by applying the decision rather than by reading it, which is the second time in this project a
plan that looked sound failed on first contact (compare D-019). Both times the defect was invisible
until someone had to pick.
