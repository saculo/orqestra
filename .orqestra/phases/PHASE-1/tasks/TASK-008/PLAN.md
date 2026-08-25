---
id: TASK-008
type: plan
status: done
updated: 2026-08-25
task: TASK-008
---

## Approach

Two independent defects in `parse_catalogue`/`main`, both from the same mistake: treating an absent
*heading list* as an absent *row*.

Fix the control flow so heading checks and frontmatter checks are independent, and give the
catalogue-unreadable path its own guard rather than letting an exception escape.

## Affected Areas

`scripts/check-templates.py` only — verified by reading it. `templates/DECISION.md` is the artifact that
proves the fix, and needs no change.

## Risks

- **The checked count will rise from 20 to 21**, which is the visible evidence the hole existed. Any
  regression that leaves it at 20 means the fix did not land.
- Hard-coding `DECISION.md` would make AC-2 pass while leaving AC-4 violated and the class of bug intact.

## Open Questions

_none_
