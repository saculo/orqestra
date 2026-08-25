---
id: TASK-009
type: design
status: done
updated: 2026-08-25
task: TASK-009
decisions: [D-018]
---

## Components

**One rule, three scopes, chosen by specificity.**

```
<scope>: <subject>

TASK-008: fix the conformance checker coverage hole
PHASE-1:  create tasks — 7 tasks, dependency order recorded
orqestra: initialize workspace
```

| scope | when | example |
|---|---|---|
| `TASK-NNN` | A task owns the change — any commit made while that task is in flight, source or artifact | `TASK-008: add instance-mode heading guard` |
| `PHASE-N` | Planning work owned by a phase but by no single task — `create-phases`, `create-tasks`, `clarify` | `PHASE-2: plan phases — 5 phases, ordering rationale` |
| `orqestra` | No phase exists yet — `init` scaffolding, workspace-level configuration | `orqestra: initialize workspace` |

**The selection rule is "most specific scope that owns the change", and it is total** — every commit has
exactly one correct scope, so there is no judgement left at the moment of writing. That is the property
`commit_style: conventional` lacked: it named a convention without defining how to pick within it.

## Interfaces

`config.md` gains a value whose meaning is written down where the value lives:

```
commit_style: scoped     # <scope>: <subject>, scope = TASK-NNN | PHASE-N | orqestra
                         # most specific scope that owns the change (§4.6)
```

## File Plan

| path | action | purpose |
|---|---|---|
| `templates/config.md` | modify | `commit_style: scoped`, with the scopes named inline |
| `skills/init/SKILL.md` | modify | `orqestra: initialize workspace` |
| `skills/task/step-push.md` | modify | Show the `TASK-NNN:` form explicitly rather than only deferring |
| `skills/pr-comments/step-reply.md` | modify | Same, for follow-up commits on a task branch |
| `.orqestra/decisions/D-018-*.md` | create | The convention constrains all future commits |

## Decisions

- **D-018** — commits are scoped by the work that owns them, not typed by the kind of change.
- **The subject line stays free prose.** Only the prefix is constrained; over-specifying the subject
  would trade one guess (which type?) for another (which phrasing?).
- **No history rewrite.** The convention applies from adoption forward; SHAs already cited in artifacts
  and decisions must keep resolving.

## Test Strategy

- `grep -rEn '(feat|fix|chore|docs|test)\(' skills/ templates/` returns nothing (AC-5).
- Every skill that commits either shows the scoped form or defers to `commit_style`, and
  `commit_style`'s meaning is stated where it is declared (AC-4).
- The three scopes each have a worked example in the shipped text (AC-3).
