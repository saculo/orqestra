---
id: TASK-011
type: task
status: pending
updated: 2026-08-26
phase: PHASE-1
module: docs
stack: markdown
origin: feature
bug:
depends_on: []
serves: [SC-7, SC-5]
attempts: 0
---

## Goal

**No orchestrator writes an artifact. Every artifact is written by the skill that owns it, dispatched
with an agent.** The orchestrator decides which step runs, and nothing else.

D1 already says this for content and does not say it for state. Content writes were routed to owning
skills correctly; **status transitions were left wherever they were convenient** — and a `status` field
is not bookkeeping, it is the thing `orqestra:status` derives every stage from (§4.3, D2). It is the
most load-bearing content in the workspace, written by whoever happened to be holding the pen.

Two shapes of breakage, both found by running `/orqestra:task TASK-008` on 2026-08-26:

**Instructions that cannot execute.** Four sites tell an orchestrator to write while its
`disallowed-tools` denies `Write` and `Edit`:

| site | instruction |
|---|---|
| `skills/task/SKILL.md:81` | set the artifact `status: awaiting-approval` before gating |
| `skills/task/step-review.md:94` | set `REVIEW.md` to `awaiting-approval` |
| `skills/task/step-merge.md:25` | set `PR.md` to `awaiting-approval` |
| `skills/greenfield/SKILL.md:73` | set the artifact `status: awaiting-approval` |

Three of the four were hit in a single run. Each is silent: the orchestrator cannot comply, the gate is
presented anyway, and the artifact never reaches `awaiting-approval` — so `/orqestra:approve` finds
nothing parked and the gate does not survive a session boundary, which is the entire property D-008
exists to provide.

**Writes that violate D1 outright.** `approve` sets `status: done`; `reject` sets
`changes-requested` **and increments `attempts` in `TASK.md`**; `unblock` sets `status: in-progress,
attempts: 0`. All three hold `Write, Edit, Agent, Bash`. So `REVIEW.md` has `review-task` as its D1
sole writer plus three other skills mutating its frontmatter, and `TASK.md` has `create-tasks` as sole
writer plus `reject` editing it. D1 says "not 'usually' — exclusively," and it is not true today.

`PR.md` is the case that forced the question. D1 (§ line 1892) and §4.8.1 (§ line 579) both assign it to
`task` (`step-push.md`) — **an orchestrator named as a sole writer**, the only such row. `push`
dispatches nobody, because the design never gave it an agent: the branch name, PR number, and URL come
from `git` and `gh` calls the orchestrator itself makes. It is also double-written, since §7.5
(§ line 1254) has `pr-comments` updating it.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | Every row of D1's writer table names a skill that holds `Write`; **no orchestrator appears as a sole writer**. `PR.md` names a step skill with a dispatched agent, and §4.8.1's `PR.md` row agrees with D1 rather than contradicting it |
| AC-2 | `PR.md` has exactly one writer — §7.5's `pr-comments` update (§ line 1254) is removed or reassigned, so no artifact is written from two places |
| AC-3 | The four gate-write instructions are gone: grepping `skills/` for an orchestrator instructed to set `awaiting-approval` returns nothing, and D-008 states **which skill** performs that write and when |
| AC-4 | `approve`, `reject`, and `unblock` no longer edit artifacts they do not own under D1 — the spec states how a status transition and an `attempts` increment are performed by the owning skill instead |
| AC-5 | §7.0.1 states the rule as a general one with its reason, so a future step file cannot reintroduce the pattern by looking locally reasonable |

<!-- SERVES AMENDED 2026-08-26. Filed against SC-5 because §4.8.1's written-by column is
     catalogue content — a stretch, and said so at filing. SC-7 was added the same day and
     is what this task actually serves; SC-5 stays because AC-1 does edit a catalogue row. -->

## Out of Scope

**Changing any skill under `skills/`.** This is the `docs` module: `REQUIREMENTS.md` only (D14). The
plugin change is a separate task and a separate PR, and it must come second — the skills **cite** these
sections rather than restating them, so the specification has to be right before the implementation can
be (D-019, the same ordering that reversed TASK-009 and TASK-010).

**Writing the new push-step skill.** This task decides that `PR.md` needs a dispatched writer and says
so in D1; building it is plugin work.

**TASK-008.** It is parked at `push` with PR #2 open and its `PR.md` unwritten, which is what surfaced
this. It is not a dependency in either direction — `depends_on` means *merged before starting* (§7.4.1)
and TASK-008 has already run. Unparking it is a consequence of the plugin task that follows this one,
not of this one.

**The `attempts` location question.** Whether the rework counter belongs in `TASK.md` at all is a
design question worth asking, but moving it changes `status` derivation and the rework loop. If this
task concludes it should move, that is a `D-NNN` and a task, not an edit made in passing.
