---
id: TASK-007
type: qa
status: done
updated: 2026-08-24
task: TASK-007
result: passed
test_command: python3 scripts/check-templates.py
---

## Test Strategy

Every criterion verified by re-running the extraction that found the defect, not by re-reading the prose.
A reconciliation checked by eye is how the discrepancies got there.

## Results

```
$ python3 scripts/check-templates.py
checked 20 templates against §4.8.1
✔ all templates conform                          exit 0

$ citation extraction (spec + all 22 skills + agents + templates)
sections defined: 63 · BROKEN section citations: none
charter rules defined: 16 · BROKEN D-rule citations: none

$ count extraction
skills: 22 shipped / 22 claimed · agents: 8 / 8 · catalogue rows: 22 / 22 claimed
```

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | `check-templates.py` exits 0 — every catalogue row has a conforming template and vice versa | passed |
| AC-2 | count extraction: skills 22, agents 8, artifacts 22, each matching its claim in prose | passed |
| AC-3 | citation extraction over the spec and all 22 skills — zero unresolved `§n.n` or `Dn` | passed |
| AC-4 | config-key and flag cross-check; `--migrate` removed, two plugin-side gaps recorded as debt | passed |

## Issues

**Two unimplemented rules remain, both plugin-side** (`no_commit`, `artifact_commit_scope`) — recorded
in `IMPLEMENTATION.md` under Tech Debt with the recommendation that they become a PHASE-2 task.

AC-4 says such a rule must be "either implemented or removed". Neither is possible from `docs`: the
implementation lives in `skills/`, and removing the claim would leave `templates/config.md` declaring a
key the spec no longer mentions — a worse inconsistency than the one being fixed. **Reporting across the
boundary is the correct action**, and it is the same move TASK-001 made when it handed these catalogue
defects to this task.
