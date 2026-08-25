---
project:
stack:
version: 1
---

## Gates
<!-- mode: gated (stop at every listed gate) | semi (only those listed) | auto (never stop)
     Gates are presented via AskUserQuestion, not by waiting for a typed command. -->

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
require_merged_deps: true    # a dependency must be MERGED, not merely done (§7.4.1)

## Delivery

branch_pattern: feat/{task_id}-{slug}
commit_style: conventional
pr_draft: false
auto_merge: false            # merging is a human decision — the one irreversible action
test_command:

## Version control

no_commit: false             # true disables artifact commits entirely (§4.6)
artifact_commit_scope: .orqestra/

## Routing
<!-- The module registry (modules.md) is the routing key: it names the agent and the
     expertise for every task. This table only fixes the steps whose role is the same
     in every module. There is no task_type table — see §5.1.1. -->

| step | skill | subagent |
|---|---|---|
| plan | plan | analyst |
| design | design | architect |
| implement | implement | **the module's `agent`** |
| qa | qa | qa-engineer |
| review | review-task | reviewer |
| pr-comments | pr-comments | **the module's `agent`** |

## Conventions
<!-- Project-wide. Module-specific conventions belong in that module's expertise skills (§5.3) —
     a module may name several. -->

review_lenses: correctness, design
