---
id: TASK-005
type: plan
status: done
updated: 2026-08-25
task: TASK-005
---

## Approach

Build a fixture workspace containing a task at **every** stage plus each trap, then run `status` against
it and grade the output against answers written down in advance.

Writing the expected answers first is the whole method. `status` output is plausible-looking prose; read
without a key, a wrong stage looks exactly like a right one.

## Affected Areas

- `skills/status/SKILL.md` — whatever the grading exposes
- `/tmp/status-fx` — 13-task fixture, not committed

## Risks

- **A fixture built carelessly grades the wrong thing.** Artifacts must conform to their schemas, or a
  derivation failure and a malformed-input failure become indistinguishable.
- **The spec may disagree with itself.** §4.3's stage table and TASK-005's own AC-3 were written at
  different times.

## Open Questions

_none_
