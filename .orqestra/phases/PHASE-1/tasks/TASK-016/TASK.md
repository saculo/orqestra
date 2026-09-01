---
id: TASK-016
type: task
status: pending
updated: 2026-09-01
phase: PHASE-1
module: docs
stack: markdown
origin: feature
bug:
depends_on: [TASK-046, TASK-011]
serves: [SC-7]
attempts: 0
---

## Goal

**A parked gate must record enough to be resumed correctly in a new session.**

`approve` sets the parked artifact to `status: done` and resumes. That is not sufficient, because gates
differ in what approval *means*:

- merge approval must verify GitHub state, then update `PR.md.pr_state` **and** `TASK.md.status`
- phase approval must update `PHASE.md`, not only `PHASE_SUMMARY.md`
- accepting a `failed` review must record the findings as tech debt (§8.1)
- accepting a phase gap needs a durable marker — see TASK-017

No artifact stores the owning workflow, the gate kind, the choice set, or the return summary that
`approve` claims to recover. So a cross-session `/orqestra:approve` can apply the wrong transition, and
it has no way to know it did.

TASK-011 establishes **who** may write these transitions. This task establishes **what must be recorded**
for the write to be correct. They are separable and both are needed.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | A parked artifact records the workflow, the gate, and the choices offered — enough that a new session reconstructs the gate without the original `AskUserQuestion` |
| AC-2 | §6.1 defines each gate's approval transition explicitly, per gate, rather than as one global "set `done`" |
| AC-3 | The fields are added to the §4.8.1 catalogue for every artifact that can park, so a parked artifact still conforms (with TASK-013's `blocked_reason` work) |
| AC-4 | `reject` and `unblock` transitions are defined the same way, including where `attempts` is incremented and by whom |
| AC-5 | A gate covering **several** artifacts is representable — the greenfield design gate covers every task at once, and `approve` expects exactly one parked artifact. Either a gate gets a record of its own, or parking is defined for the many-artifact case; arbitrarily parking one is not an answer (audit finding 5) |
| AC-6 | A gate with **no** `TASK.md` is representable — phase, task-decomposition, phase-close and PR-triage gates have no task owner, and `reject` increments `attempts` in a `TASK.md` unconditionally. A phase gate must not invent a task owner to hold its retry count (audit finding 11) |

## Out of Scope

`skills/approve`, `skills/reject`, `skills/unblock` — `plugin`, TASK-027 (D-019).

Moving `attempts` out of `TASK.md`. Same carve-out TASK-011 made: it changes stage derivation, so it is
a `D-NNN` if this task concludes it should move.

**Defining an approval transition before TASK-046 lands.** Every transition here is a write performed
by some actor, and D-031 measured that an orchestrator's `disallowed-tools` removes `Write` from its
dispatched agents as well as itself. Until that clears, "the owning skill writes it" names an actor
that cannot. Hence `depends_on: [TASK-046]`.

<!-- WIDENED BY AUDIT 2026-09-01. Findings 5 and 11 became AC-5 and AC-6 rather than a
     note, because both change what the task must produce rather than adding context.
     The audit proposes a dedicated gate record (id, owning workflow, step, scope, target
     artifacts, summary, choices, approval note, resume action) and typed approve/reject
     handlers. That is one candidate answer to AC-5 and AC-6, not the required one — the
     alternative is extending the parked artifact, and choosing is this task's work. -->
