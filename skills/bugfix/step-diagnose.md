# Step — Diagnose

Dispatch `analyst` to find the **root cause with evidence**, then **gate**.

## Dispatch

`MODULE` is read from `work/BUG-NNN/BUG.md`'s `module:`, and `PATHS` `STACK` `EXPERTISE` come from
that one `modules.md` row (§5.5). **Never derive any of the four from the symptom** — intake
established the module and D-029 forbids a `MODULE:` that disagrees with the artifact it names.
The example below is an illustration; the rule above is what governs.

```
ROLE:      orqestra:analyst
STEP:      diagnose
SKILL:     orqestra:diagnose
BUG:       BUG-003
MODULE:    api
PATHS:     services/api
STACK:     java
EXPERTISE: java-expertise, spring-conventions
READ:
  .orqestra/work/BUG-003/BUG.md
  .orqestra/project/PROJECT.md
  .orqestra/modules.md
  .orqestra/decisions/INDEX.md
TEMPLATE:  ${CLAUDE_PLUGIN_ROOT}/templates/DIAGNOSIS.md
WRITE:     .orqestra/work/BUG-003/DIAGNOSIS.md
RETURN:    at most 10 lines.
```

## The bar

**Root cause, not symptom. Evidence, not plausibility.**

The first plausible-looking line is usually not the cause — it is the place the symptom became visible.
`root_cause_found: false` is an honest and useful outcome; a confident wrong diagnosis costs a designed
fix, an implementation, and a review before anyone notices.

## The gate

```
▸ GATE · diagnosis · BUG-003

  ROOT CAUSE  session TTL is compared against System.currentTimeMillis() in local
              time, while it is stored as UTC — sessions expire early or late by
              the UTC offset.
  EVIDENCE    SessionExpiryTest fails only when TZ != UTC; passes under TZ=UTC.
              Introduced in TASK-004 (commit a3f21c8).
  DIRECTION   normalize at the store boundary; 3 files in api
  RISK        every existing session invalidates on deploy

  [ Approve — design the fix ]  [ Reject with reason ]  [ Investigate further ]
```

This is the cheapest point to catch a wrong theory and the most expensive one to skip.

Approve → commit, continue to promote.

## When the fix lands in another module

`## Fix Direction` may put the fix somewhere other than the BUG's `module:`. The analyst **states
that difference and does not fix it** — it holds one write path (D2) and no `Edit`.

Carry a `MODULE` line in the gate block whenever the two differ, naming the old value and the new:
approving the diagnosis approves the correction. On approval, amend the BUG's `module:` and
**recompose any dispatch that named the old value** — never leave a `MODULE:` standing against an
artifact that now says something else (D-029). Promote then reads the amended key (§7.3), so the
task's `module:` and the bug's agree by construction rather than by luck.

**Stated plainly (§7.0.1): no actor in this workflow currently holds a tool that can amend
`BUG.md`.** The orchestrator disallows `Write` and `Edit` (`skills/bugfix/SKILL.md:6`) and the
analyst has no `Edit`. That gap is pre-existing and identical for every write to `BUG.md`,
including intake's; closing it is a separate task. The rule is stated here because this is where
the correction is decided.
