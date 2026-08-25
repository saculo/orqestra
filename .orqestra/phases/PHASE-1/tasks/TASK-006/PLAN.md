---
id: TASK-006
type: plan
status: done
updated: 2026-08-25
task: TASK-006
---

## Approach

A second fixture, richer than TASK-005's: real titles, real dependencies, a parked gate, and an open PR
that actually obstructs two tasks. TASK-005's fixture had empty index files, so no titles existed and
AC-3 could not have been tested against it.

Expected answers written before running, again — that method caught a wrong stage last time, and this
time it caught a wrong expectation of mine.

## Affected Areas

`skills/status/SKILL.md`, and `/tmp/next-fx` plus two empty-state fixtures. Not committed.

## Risks

- **Reporting order and next-command selection are different questions.** A fixture that does not
  separate them will pass while the tool conflates them.
- Empty states are the paths nobody tests and every new user hits first.

## Open Questions

_none_
