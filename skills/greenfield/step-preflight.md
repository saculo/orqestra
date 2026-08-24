# Step — Preflight

Four checks. Cheap, and each one prevents a failure that is expensive later.

| Check | On failure |
|---|---|
| `.orqestra/config.md` exists | **Stop.** Not an orqestra project — run `/orqestra:init` |
| `PRD.md` exists and is non-empty | **Stop.** Nothing to plan from |
| `modules.md` has at least one module | **Stop.** Every task routes by its module row (§5.1); `create-tasks` would block on the first task |
| Nothing parked | Report anything `blocked` or `awaiting-approval` via `orqestra:status`, and stop |

The module check earns its place: without it, planning runs all the way through clarify and phases
before `create-tasks` discovers there is nowhere to put a task. Failing in three seconds beats failing
after two gates.

## On success

```
✓ preflight · PRD 340 lines · 4 modules · nothing parked
```
