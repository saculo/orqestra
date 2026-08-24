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
commit_style: conventional
pr_draft: false
auto_merge: false
test_command: (none yet — see PHASE-1 SC-5, the eval harness)

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
