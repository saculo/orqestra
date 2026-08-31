# Step — Promote

Turn the diagnosed bug into an ordinary task. Invoke `create-task` in **promote mode**.

## Invoke

```
Skill: orqestra:create-task
Args:  --mode promote --bug BUG-003 --phase PHASE-2
```

## The task it produces

```yaml
module: api               # CARRIED from the BUG's `module:` — never re-derived (D-029)
stack: java               # advisory, copied from the module row
origin: bug
bug: BUG-003
serves: [SC-2]            # the criterion the bug violates
```

**The task's `module:` is the BUG's `module:`, read from its frontmatter** — never re-derived from
the symptom or from the diagnosis (D-029). When diagnosis found the fix lands elsewhere, the BUG was
amended at the diagnosis gate, so reading the key here is already reading the corrected value.

**There is no bugfix agent** (§7.3.1). The module row names who implements it, and a bug in `api` is
implemented by exactly the agent a feature there would be. `origin: bug` is what changes downstream:
`review-task` adds the `regression-risk` lens, and `qa` requires a test that fails against the pre-fix
code.

Acceptance criteria come from the **diagnosis**, not the report: what must be true for the root cause to
be fixed, plus the reproduction now passing.

## When no criterion is violated

If the bug violates no phase success criterion, the criteria are incomplete. **Say so at the next gate —
do not invent one** (D11).

## Report

```
✓ BUG-003 → TASK-031 (module: api, origin: bug, serves SC-2)
```
