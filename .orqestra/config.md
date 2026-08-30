---
project: orqestra
stack: markdown
version: 1
---

## Gates

| workflow | mode | gate after |
|---|---|---|
| greenfield | gated | phases, tasks, design |
| add-phase | gated | phase, tasks, design |
| bugfix | semi | diagnosis, design |
| task | gated | review, merge |
| pr-comments | semi | triage |
| close-phase | gated | summary |

## Rework

max_attempts: 3
require_merged_deps: true

## Delivery

branch_pattern: feat/{task_id}-{slug}
commit_style: scoped         # <scope>: <subject> — no conventional-commit type prefix (§4.6, D-018)
                             # scope = the most specific one that OWNS the change:
                             #   1. a task owns it (source or artifact, while in flight) → TASK-NNN
                             #   2. else a phase's planning owns it                      → PHASE-N
                             #   3. else — init, workspace config, repo-wide work        → orqestra
pr_draft: false
auto_merge: false
test_command: python3 scripts/check-templates.py && python3 scripts/test-check-envelopes.py && python3 scripts/check-envelopes.py
                             # check-envelopes.py exits 1 today, on skills/bugfix/step-diagnose.md
                             # alone: it needs a SKILL naming skills/diagnose/, which TASK-034 authors
                             # after TASK-033 makes room in the spec. The suite is red BY DESIGN until
                             # then — a skip-list would be the fabrication TASK-030's Out of Scope
                             # forbids, and would outlive the reason for it. DELETE THESE LINES when
                             # the scan goes green, so a second failure cannot hide inside a familiar
                             # one.

## Version control

no_commit: false
artifact_commit_scope: .orqestra/

## Routing

| step | skill | subagent |
|---|---|---|
| plan | plan | analyst |
| design | design | architect |
| implement | implement | from the module's task_type |
| qa | qa | qa-engineer |
| review | review-task | reviewer |
| pr-comments | pr-comments | from the module's task_type |

| task_type | subagent |
|---|---|
| backend | backend-engineer |
| frontend | frontend-engineer |
| devops | devops-engineer |
| agentic | agentic-engineer |
| qa | qa-engineer |

## Conventions

prd_path: REQUIREMENTS.md
review_lenses: correctness, design
