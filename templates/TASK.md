---
id:
type: task
status: pending
updated:
phase:
module:                # THE routing key (D14). agent/stack/expertise all come from its row
stack:                 # advisory context, copied from the module row — never a routing input
origin: feature        # feature | bug
bug:                   # BUG-NNN backlink, when origin: bug
depends_on: []         # must be MERGED before this task starts (§7.4.1)
serves: []             # SC-N ids — a task serving none is out of scope
attempts: 0
---

## Goal
<!-- One coherent change a reviewer can hold in their head at once. -->

## Acceptance Criteria
<!-- Table: id | criterion
     Observable behaviour, checkable by qa against what the system actually does.
     "Works correctly" is not a criterion; "expired sessions return 401" is.
     Past ~5 criteria this is usually two tasks — split, never shrink (§7.6.1). -->

| id | criterion |
|---|---|

## Out of Scope
<!-- The boundary. Prevents scope creep at implement more reliably than the goal
     statement does. `_none_` if nothing needs excluding. -->
