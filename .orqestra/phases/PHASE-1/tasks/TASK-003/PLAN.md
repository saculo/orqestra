---
id: TASK-003
type: plan
status: done
updated: 2026-08-24
task: TASK-003
---

## Approach

Run `init` in a real empty repository and check what it produces against the catalogue. Not read the
skill and reason about it — **run it**, because every criterion here is about behaviour and the failure
mode is a file that reads correctly to a human while being wrong to the tool.

## Affected Areas

- `skills/init/SKILL.md` — whatever the run shows is wrong
- `scripts/check-templates.py` — AC-2 needs instance validation, and the checker only does templates
- Fixtures in `/tmp`, not committed

## Risks

- **AC-3 needs a human.** `AskUserQuestion` does not exist in a non-interactive session, so stack
  confirmation cannot be verified this way. The skill must at least degrade honestly.
- **The checker validates templates, not artifacts.** AC-2 asks about produced files. That gap is the
  reason a defect could ship unnoticed.

## Open Questions

_none_
