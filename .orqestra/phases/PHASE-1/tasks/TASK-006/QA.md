---
id: TASK-006
type: qa
status: done
updated: 2026-08-25
task: TASK-006
result: passed
test_command: python3 scripts/check-templates.py --target /tmp/next-fx/.orqestra
---

## Test Strategy

Three fixtures, expectations written first, every row graded.

## Results

```
fixture A — 8 tasks, titled, with a gate, a block, and an obstructing PR

  ⛔ TASK-008  audit log            api      designed    BLOCKED: contradictory-input → /orqestra:unblock
  ← TASK-007  remember-me          api      planned     design awaiting-approval → needs your decision
  ← TASK-002  login endpoint       api      pushed      PR #102 open ← waiting on you
  ✓ TASK-001  session store        api      delivered   PR #101 merged
    TASK-003  logout endpoint      api      designed    blocked by TASK-002
    TASK-004  session expiry job   worker   designed    blocked by TASK-002
    TASK-005  password reset       api      designed    ready
    TASK-006  login form           web      designed    ready

  → Next: merge PR #102 (unblocks TASK-003 and TASK-004)

fixture C — six equal candidates, nothing blocked or gated
  → Next: /orqestra:task TASK-003          (lowest id, D10)

empty states
  no .orqestra/       "No orqestra workspace here" → /orqestra:init
  no phases           reports the scaffold, notes planning never ran → fill PRD.md, then /orqestra:greenfield
```

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | `/tmp/uninit` — says so plainly, no error, no empty-project pretence | passed |
| AC-2 | initialized workspace, no phases — reports the scaffold and names greenfield | passed |
| AC-3 | fixture A — id, title, module, stage, and what holds each up; §4.3 stage names verbatim | passed |
| AC-4 | merge chosen over unblock (2 released vs 0); fixture C tie-break to lowest id | passed |
| AC-5 | fixture A — blocked, then gate, then obstructing PR, above everything; PR reported as obstruction, not progress | passed |

## Issues

**My expected answer for AC-4 was wrong, and finding out why was the finding.** I predicted
`/orqestra:unblock TASK-008` because blocked ranks first in the report. `status` named the merge, which
is correct: AC-4 asks for the action that unblocks the most work, and the block released nothing.

The instruction I misread said blocked is top "and nothing downstream matters" — which reads as *do the
blocked thing next*. `status` got it right; the skill did not require it to. Fixed by splitting the two
axes explicitly.

**AC-2 exceeded its criterion**: it noticed `PRD.md` held only a placeholder line and named that as the
real obstacle to `/orqestra:greenfield`, rather than reporting an empty project and stopping.
