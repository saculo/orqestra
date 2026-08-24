# Step — Reproduce

**No fix without a failing reproduction first.** This step either produces one or blocks.

## Procedure

1. Identify the module from the symptom, and load its expertise skills.
2. Follow the reported steps exactly, against the **current build**.
3. Reproduced → capture it as an **automated failing test** wherever possible. That test becomes qa's
   evidence later, and for an `origin: bug` task qa requires a test that fails against the pre-fix code
   (§7.3.1) — writing it now is the cheapest it will ever be.
4. Not reproduced → try the obvious variations: environment, data state, timing, version. Bound this;
   two or three attempts, not an open-ended hunt.
5. Still not reproduced → **block**, `blocked_reason: no-reproduction`. Ask the human for what is
   missing: exact version, data, logs, timing.

## Why this is absolute

A fix for an unreproduced bug cannot be verified. qa has nothing to check, review has nothing to judge
against, and the PR claims to fix something nobody can demonstrate was broken. The failure is silent —
it ships, and the bug is reported again in three weeks.

Update `BUG.md` `## Reproduction` with what actually worked, which is frequently not what was reported.

## Report

```
✓ reproduced · services/api/test/SessionExpiryTest.java:44 fails on main
```
