# Step — QA

Dispatch `qa-engineer` with the task's stack expertise. Ungated: a failure routes back to implement
without asking a human, because the finding is objective and the fix is mechanical.

## Dispatch

```
ROLE:      orqestra:qa-engineer
STEP:      qa
TASK:      PHASE-1/TASK-007
STACK:     java
EXPERTISE: java-expertise, test-quality

READ:
  .orqestra/phases/PHASE-1/tasks/TASK-007/TASK.md
  .orqestra/phases/PHASE-1/tasks/TASK-007/DESIGN.md
  .orqestra/phases/PHASE-1/tasks/TASK-007/IMPLEMENTATION.md
  .orqestra/project/PROJECT.md
  .orqestra/decisions/INDEX.md

TEMPLATE:  ${CLAUDE_PLUGIN_ROOT}/templates/QA.md
WRITE:     .orqestra/phases/PHASE-1/tasks/TASK-007/QA.md
RETURN:    at most 10 lines, per the skill's Return contract.
```

The qa skill resolves its own expertise from the task's `stack` — QA in a Java project needs the Java
skills, not a generic testing stance.

## On return

Read `QA.md` **frontmatter only** — `result`, `status`.

| Frontmatter | Do |
|---|---|
| `result: passed` | Commit artifacts, continue to review |
| `result: failed` | Back to implement. `attempts++`. `REWORK: QA.md — <failing AC-N>` |
| `status: blocked` | Stop. Report the reason |

**`result: failed` is not a block.** It is the loop working: a defect found before review, fixed, and
re-verified. Only report it as a problem when `attempts` reaches `max_attempts`.

At `attempts > max_attempts` → `blocked`, `blocked_reason: max-attempts`. Present every attempt and
what each one failed on, then stop. **Do not retry** — a loop that has failed three times on the same
criterion fails a fourth time the same way, and the cause is upstream of implement.

## Report

```
▸ PHASE-1 / TASK-007 · qa · qa-engineer + java-expertise
✗ qa · 2 of 9 criteria failed → returning to implement (attempt 2 of 3)
```
