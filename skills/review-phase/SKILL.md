---
name: review-phase
description: "Verifies a completed orqestra phase criterion by criterion against actual behaviour and aggregates deviations, tech debt, and review findings across its tasks into PHASE_SUMMARY.md with a criteria-met verdict. Use when close-phase runs, or when the user says '/orqestra:review-phase <N>'."
allowed-tools: Read, Write, Glob, Grep, Bash(git diff:*), Bash(git log:*)
disallowed-tools: Agent, Edit, NotebookEdit
---

> **Invocation**: dispatched by `orqestra:close-phase`, or `/orqestra:review-phase <N>`. Runs as the
> `reviewer` subagent. **Gated.** **Class**: step+review

# orqestra Review — Phase

Decide whether the phase actually delivered its milestone.

Not whether the tasks are done — `status` already knows that. Whether the **success criteria hold in
observable behaviour**. Those are different questions, and the gap between them is exactly what this
step exists to find: five merged tasks can leave `SC-3` unmet, and nothing else in the workflow would
notice.

## Inputs

| Read | Why |
|---|---|
| `PHASE-N/PHASE.md` | The `SC-N` criteria — the standard |
| Every `TASK-*/TASK.md` in the phase | What was delivered, and which `SC-N` each served |
| Every `IMPLEMENTATION.md` | Deviations and tech debt |
| Every `QA.md` | Criteria coverage and results |
| Every `REVIEW.md` | Findings, including advisory ones accepted as debt |
| `decisions/INDEX.md` | **Always read** (D4). Decisions taken during the phase |
| The running system | **Verify behaviour, not paperwork** |

## Output

- **Writes**: `PHASE-N/PHASE_SUMMARY.md`. **Nothing else** (D1, D2).
- **Template**: `${CLAUDE_PLUGIN_ROOT}/templates/PHASE_SUMMARY.md`, copied literally (D16).

## Procedure

Run in order (D6):

1. List every `SC-N` from `PHASE.md`.
2. For each, find the tasks that claimed to serve it (`TASK.md.serves`).
3. **Verify it against actual behaviour.** Run it, exercise it, read the tests that prove it. A
   criterion marked met because every task touching it merged is not verified — that is the failure mode
   this step exists to catch.
4. Record `met: yes|no` per criterion **with evidence**: what you ran, what you observed. "Tasks
   complete" is not evidence.
5. Aggregate across the phase, each item **tagged with the task it came from**:
   - deviations from `IMPLEMENTATION.md`
   - tech debt from `IMPLEMENTATION.md` and accepted review findings
   - unresolved advisory findings from `REVIEW.md`
6. Set `criteria_met`: `true` only if **every** criterion is met. One unmet criterion makes it `false` —
   there is no partial credit, because a phase is a milestone or it is not.
7. Write `PHASE_SUMMARY.md`, verify against the schema, declare `SCHEMA: ok` (D12).

## Return

```
STATUS:   done
SKILLS:   <the SKILL and EXPERTISE names you invoked, or `none`>
CRITERIA: <n> of <m> met
UNMET:    <SC-N: what is missing>          one line each; omit when all met
DEBT:     <n> items carried forward
KEY:      <the 2–3 things a human most needs to know about this phase>
SCHEMA:   ok
```

## Rules

1. **Verify behaviour, never paperwork.** A criterion is met when you observed it holding.
2. **Never invent gap tasks.** An unmet criterion is reported; whether to add tasks or accept the phase
   as it stands is the human's decision at the gate. Proposing tasks is not your job, and doing it
   pre-empts a choice that is theirs (D11).
3. **Never modify a task's artifacts** (D3, D5). They are done and frozen. You read them.
4. **No partial credit.** `criteria_met: true` requires every criterion.
5. Tag every aggregated item with its source task. An untagged finding cannot be acted on.
