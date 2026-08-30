# Step — Diagnose

Dispatch `analyst` to find the **root cause with evidence**, then **gate**.

## Dispatch

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
