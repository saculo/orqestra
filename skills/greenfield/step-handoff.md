# Step — Handoff

Planning is finished. Report what exists and how to deliver it, then **stop**.

```
✓ PHASE-1 planned — 5 tasks designed

  TASK-001  session store        api     ready
  TASK-002  login endpoint       api     blocked by TASK-001
  TASK-003  logout endpoint      api     blocked by TASK-001
  TASK-004  session expiry job   worker  blocked by TASK-001
  TASK-005  login form           web     blocked by TASK-002

  Decisions recorded: D-001 (postgres), D-002 (no ORM), D-003 (flyway)

→ /orqestra:task TASK-001
```

Only tasks with no unmerged dependencies are `ready`. Name exactly one next command — the first ready
task in id order (D10).

## Do not continue

**Do not implement anything**, not even the first task, not even when asked to be helpful. The
planning/delivery split is the structure of the whole tool: delivery re-checks the design against HEAD
at preflight, runs qa, gates review, and opens a PR. Starting to build here skips all four.

If the user asks you to keep going, point at `/orqestra:task <ID>` and stop.
