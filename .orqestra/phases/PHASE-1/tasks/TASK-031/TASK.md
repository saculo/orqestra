---
id: TASK-031
type: task
status: pending
updated: 2026-08-27
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

**Nothing can run the probe that proves a dispatched agent honours its expertise.**

Carries TASK-019's AC-1, which that task could not meet. The criterion asks for a probe convention that
appears **only** in an expertise skill, with the dispatched agent's **output honouring it** — not
quoting it. Quoting proves the text arrived; honouring proves it was used, and only the second is worth
a criterion.

It cannot run from inside the pipeline. A dispatched agent holds no `Agent` tool, so it cannot dispatch
the probe subject; and the probe's fixture lives outside any module's `PATHS`. TASK-019 verified AC-2
and AC-4 by other means — a branch-only string in the agent's own system prompt — but AC-1 needs a
layer that can dispatch.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | A probe convention exists in a fixture expertise skill and **nowhere else** in the repository, verified by grep |
| AC-2 | Dispatching an agent with that skill in `EXPERTISE` produces output that honours the convention; dispatching without it produces output that does not. Both directions run, because only the contrast proves the skill did the work |
| AC-3 | The probe is repeatable by a human from one documented command, and its result is recorded — a probe that only ever ran once verifies nothing about the next change |

## Out of Scope

A general eval harness for every skill. This proves one mechanism — that `EXPERTISE` reaches and
changes a dispatched agent. SC-1's broader verification is separate work.
