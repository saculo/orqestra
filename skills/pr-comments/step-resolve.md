# Step — Resolve

Fix the `accept` comments. **In lowest-number order** (D10), one at a time.

## Routing

With `--task`: route by the task's module row — same agent, same expertise, same `PATHS` boundary as
implement used (§5.1).

Standalone: infer the module from the file's location in `modules.md`, and **say which you inferred**.
An inference stated is checkable; an inference hidden is a silent misroute.

## Scope

**Fix only what the comment names.** A comment about a null check is not license to refactor the method.
Adjacent problems you notice go in the reply as an observation, not into the diff (D3).

Each fix stays inside its module's `paths` (D14). A comment asking for a change in another module is a
`discuss` — it belongs to a different task.

## Why these fixes skip the rework loop

They do not re-enter implement → qa → review, and they do not increment `attempts`.

They have already been reviewed — by the PR reviewers, looking at this exact diff, which is a stronger
check than re-running `review-task` against feedback those same reviewers wrote. Re-running review here
would ask the same question twice and spend an attempt doing it.

## Report

```
✓ resolve · 4 fixes applied · api
```
