---
id: TASK-005
type: qa
status: done
updated: 2026-08-25
task: TASK-005
result: failed
test_command: python3 scripts/check-templates.py --target /tmp/status-fx/.orqestra
---

## Test Strategy

13-task fixture generated from the real templates, schema-verified before use, with expected stages
written down before `status` was run once.

## Results

```
stage             expected      reported      
TASK-001 created  created       created       ✔
TASK-002          planned       planned       ✔
TASK-003          designed      designed      ✔
TASK-004          implemented   implemented   ✔
TASK-005          verified      verified      ✔
TASK-006          reviewed      reviewed      ✔
TASK-007          pushed        pushed        ✔  + "PR #42 open ← waiting on you"
TASK-008          delivered     delivered     ✔
TASK-009 TRAP1    designed      designed      ✔  + "implement: changes-requested → rework at implement"
TASK-010 TRAP2a   implemented   implemented   ✔  + "qa failed → rework at implement"
TASK-011 TRAP2b   verified      verified      ✔  + "review: changes-requested → rework at implement"
TASK-012 blocked  blocked       blocked       ✔  reason as headline, ranked first
TASK-013 malformed unknown      unknown       ✔  named both parse failures; refused to guess
```

Next command: `/orqestra:unblock TASK-012` — blocked correctly outranks the open PR.

Unprompted, `status` also caught a flaw in the fixture itself (TASK-007 and TASK-008 both carrying
`pr_number: 42`) and **declined to fix it**, noting it holds no `Write`.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | TASK-001..008, one per stage | passed |
| AC-2 | TASK-009 — reported `designed`, in rework at implement, never `implemented` | passed |
| AC-3 | TASK-010 and TASK-011 | **failed as written** — see Issues |
| AC-4 | TASK-012 — blocked, `design-invalid` as headline, ranked above everything | passed |
| AC-5 | TASK-013 — `unknown`, both parse errors named, no guessed stage | passed |

## Issues

**AC-3 is wrong, and `status` is right.** It says a `QA.md` with `result: failed` **or** a `REVIEW.md`
with `verdict: changes-requested` "does not advance the stage past `implemented`". The first half holds.
The second does not: when a review is rejected, qa has already passed, so the task genuinely *is*
`verified`, and §4.3's stage table says so. Reporting it as `implemented` would discard a fact the
workspace records.

The criterion conflates two traps that behave differently. `status` follows §4.3; the AC was written
from it loosely.

**Recommended amendment**: split AC-3 so each trap states its own resulting stage — `result: failed`
leaves the task at `implemented`, `verdict: changes-requested` leaves it at `verified`, and neither
advances. That is what the tool does and what §4.3 requires.

Marked `failed` rather than quietly passing, because a criterion is not met until it is amended — and
amending a criterion is a human decision (§8.1), not QA's.
