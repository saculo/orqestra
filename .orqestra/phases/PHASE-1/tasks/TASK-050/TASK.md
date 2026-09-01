---
id: TASK-050
type: task
status: pending
updated: 2026-09-01
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: [TASK-048]
serves: [PHASE-4/SC-1]
attempts: 0
---

## Goal

**`pr-comments` edits arbitrary source with no dispatch, no module, no `PATHS`, and no recorded write
target — and it is the only workflow that writes source outside the delivery pipeline.**

`skills/pr-comments/step-resolve.md` says to route by module and apply fixes, and contains no `ROLE:`
envelope. The parent skill holds `Read, Write, Edit, Glob, Grep, Bash, Skill, Agent, AskUserQuestion`,
so it can execute those edits itself. `check-envelopes.py` validates envelopes that exist and never
asserts a step has one, so the step passes every check in the repository while being the least
constrained writer in it.

**Three distinct failures, not one.**

1. **No module agent, expertise or `PATHS`.** Every other source-writing step resolves its agent from
   the `modules.md` row and is bounded by `PATHS`. This one is bounded by nothing.
2. **One module per task is violated by construction.** A PR's comments can touch several modules;
   §5.2 and TASK.md's own rule say a task whose diff escapes its module is a review finding. Resolution
   as written has no way to honour that, because it is one undifferentiated step.
3. **The new diff is unreviewed.** The workflow treats these edits as already-reviewed because they
   answer review comments. That is false: a requested fix is a *new* diff, written after the review that
   requested it, and nothing looks at it before merge.

**Why it is not simply TASK-048.** That task gives every writing step an envelope, which fixes (1)'s
shape. It does not decide the *unit* of dispatch — one per module, with comment ids partitioned — nor
does it address (2) or (3), which are about ownership and verification rather than tool plumbing.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | Resolution dispatches one unit per module, with the comment ids for that module and `PATHS` from its `modules.md` row, so no dispatch can edit outside its module |
| AC-2 | A PR whose comments span two modules produces two dispatches, and the workflow says how a comment that matches no module row is handled — blocked, not guessed (D11) |
| AC-3 | The new diff is verified before merge: the existing QA run stays, plus a review of the post-resolution diff or a required external approval. "Already reviewed" is stated nowhere, because it is not true |
| AC-4 | `RESOLUTION.md` records the source commit SHA the fixes landed as, so what was resolved can be tied to what was written |
| AC-5 | The `pr-comments` skill's own `allowed-tools` no longer needs `Write`/`Edit` for source, since it no longer edits source |

## Out of Scope

**`gh` review-thread fetching.** TASK-022 — a different defect in the same workflow, and this task
should not touch `step-fetch.md`.

**The envelope mechanics themselves.** TASK-048 establishes that a writing step carries one; this task
decides what the units are and what verifies their output.

**Whether `pr-comments` should run inside the task pipeline at all.** It runs both standalone and as a
pipeline step, and that dual life is what makes the module question hard. Reworking it is a design
question, not this task's.
