# Step — Handoff

```
✓ BUG-003 diagnosed → TASK-031 designed

  ROOT CAUSE  session TTL compared in local time, stored as UTC
  FIX         normalize at the store boundary · 3 files · api
  RISK        every existing session invalidates on deploy
  TESTS       SessionExpiryTest currently fails on main — qa will require it to
              fail against the pre-fix code

→ /orqestra:task TASK-031
```

The fix now goes through the **same pipeline as a feature** — implement, qa, review, push, PR comments,
merge. There is no separate fix path, and that is deliberate: a bug fix is the change most likely to
break something else, so it gets more scrutiny than a feature, not less.

**Do not implement the fix here.** Stop.
