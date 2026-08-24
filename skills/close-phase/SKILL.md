---
name: close-phase
argument-hint: "<N>"
description: "Closes a completed orqestra phase — verifies every task is merged, dispatches review-phase to check the success criteria against actual behaviour, and gates the human on the milestone verdict. Use when the user says '/orqestra:close-phase <N>', asks whether a phase is done, or finishes the last task of a phase."
allowed-tools: Read, Glob, Grep, Skill, Task, AskUserQuestion, Bash
---

> **Arguments**: `/orqestra:close-phase <N>`
> **Class**: orchestrator+

# orqestra Close Phase

Decide whether a phase reached its milestone, and record it.

## Arguments

`$ARGUMENTS` is the phase number, e.g. `1`.

**When empty**: invoke `orqestra:status` and use the lowest-numbered phase whose status is not `done`; state which one you chose.

## Procedure

Run in order (D6):

### 1. Verify the phase is actually finished

Invoke `orqestra:status`. **Every task must be `delivered`** — `status: done` *and* `PR.md.pr_state:
merged`.

Anything short of that → stop and report what remains. A phase closed over an unmerged task certifies a
milestone whose code is not on the base branch, and the next phase then plans against a codebase that
does not exist.

### 2. Dispatch review-phase

```
ROLE:      orqestra:reviewer
STEP:      review-phase
PHASE:     PHASE-1
READ:
  .orqestra/phases/PHASE-1/PHASE.md
  .orqestra/phases/PHASE-1/tasks/*/TASK.md
  .orqestra/phases/PHASE-1/tasks/*/IMPLEMENTATION.md
  .orqestra/phases/PHASE-1/tasks/*/QA.md
  .orqestra/phases/PHASE-1/tasks/*/REVIEW.md
  .orqestra/decisions/INDEX.md
TEMPLATE:  ${CLAUDE_PLUGIN_ROOT}/templates/PHASE_SUMMARY.md
WRITE:     .orqestra/phases/PHASE-1/PHASE_SUMMARY.md
RETURN:    at most 10 lines.
```

### 3. Gate on the verdict

Read `PHASE_SUMMARY.md` **frontmatter only** — `criteria_met`.

**`criteria_met: true`:**

```
▸ GATE · phase close · PHASE-1

  CRITERIA  4 of 4 met
  DEBT      3 items carried forward
  KEY       Session expiry verified against real clocks, not mocks.
            TASK-006 deviated to a shared validator — noted, not a problem.

  [ Approve — close phase ]  [ Reject with reason ]
```

Approve → `PHASE.md status: done`, commit, report the next command.

**`criteria_met: false` — the phase does not advance.** Present the unmet criteria and ask:

```
▸ PHASE-1 · 3 of 4 criteria met

  SC-3  unmet — sessions do not expire; TTL is stored but never enforced

  [ Add tasks to close the gap ]  [ Accept the phase as it stands ]  [ Review again ]
```

| Choice | Effect |
|---|---|
| Add tasks | `create-tasks` in gap mode → new tasks for this phase → deliver them → close again |
| Accept as it stands | `PHASE.md status: done`, the unmet criteria recorded in the summary as accepted |
| Review again | Re-dispatch `review-phase` |

**Never invent gap tasks yourself** (D11). Whether an unmet criterion is worth more work is a product
decision, and it is the human's. Pre-empting it is the single most tempting overreach in this workflow —
the gap is visible, the fix looks obvious, and it is still not your call.

## Rules

1. **Never close a phase with unmerged tasks.**
2. **Never invent gap tasks.** Present the gap; the human decides.
3. **Never modify task artifacts** (D3, D5). They are done and frozen.
4. **Never write `PHASE_SUMMARY.md` yourself** (D1) — `review-phase` owns it. You gate on it.
5. `criteria_met: false` with "accept as it stands" is a legitimate outcome, recorded honestly. A phase
   closed with a known gap is fine; a phase closed pretending there is none is not.
