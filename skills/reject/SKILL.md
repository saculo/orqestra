---
name: reject
argument-hint: ""<why>""
description: "Rejects the orqestra step currently parked at a gate, records the reason, and re-dispatches that step with the feedback as rework input. Use when the user says '/orqestra:reject', or rejects a gate in a session later than the one that parked it."
allowed-tools: Read, Write, Edit, Glob, Grep, Skill, Task, Bash
---

> **Arguments**: `/orqestra:reject "<why>"` — a reason is required · **Class**: orchestrator+

# orqestra Reject

Send the parked step back with feedback. The counterpart to `approve`, for the same cross-session case.

## Procedure

1. **Require a reason.** `$ARGUMENTS` empty → stop and ask. A rejection without one re-runs the step
   with no new information, which produces the same output and spends an attempt doing it.
2. Invoke `orqestra:status` to find the parked artifact.
3. Set `status: changes-requested`, increment `attempts` in `TASK.md`, and record the reason in the
   artifact.
4. **If `attempts` now exceeds `max_attempts`**: set `blocked`, `blocked_reason: max-attempts`, present
   every attempt and what each failed on, and **stop**. Do not re-dispatch (§8).
5. Otherwise re-dispatch the step with the reason in `REWORK`, per the owning workflow's rejection
   routing.
6. Commit (§4.6).

## Rules

1. **Never hand-edit the artifact to satisfy your own feedback** (§6.1). Reject with the reasoning and
   let the step re-run. This is the rule that decays fastest, because editing is quicker and looks like
   the same outcome — it is not: the fix goes unreviewed and unattributed.
2. **Rejection routes backwards**, never forwards. Rejecting a review reopens implement, not qa.
3. **A rejected gate keeps its commit** (§4.6). The record of what was tried is the value; the rework
   produces a new commit alongside it.
4. Be specific in what you record. "Not good enough" costs a full cycle that a named defect would not.
