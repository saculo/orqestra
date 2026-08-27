---
id: TASK-015
type: pr
status: done
updated: 2026-08-27
task: TASK-015
branch: feat/TASK-015-envelope-delivers-its-layers
pr_number: 3
pr_url: https://github.com/saculo/orqestra/pull/3
pr_state: merged
---

## Summary

Amends §5.5 so the dispatch envelope delivers the layers it advertises. `EXPERTISE` is redefined as
skills the agent **invokes**, with the `Skill`-in-`tools:` precondition named rather than assumed
(D-024); `SKILL` names the step skill so a dispatched agent executes the procedure instead of relying
on its persona to duplicate it; `MODULE` and `PATHS` join the example and the prose, which is what lets
a reviewer check a diff against the module's `paths` deterministically (§5.2, D2).

Field presence is now mechanical: an obligation table with four classes — always, conditional on the
scope unit having a module, step-specific, and re-dispatch only — plus a closed-list rule making an
invented field as much a contract violation as an omitted one.

All five acceptance criteria verified. One `minor` deviation, declared: a clause in §7.8.2 linking the
resolved lens set back to §5.5. F-3 and F-4 remain open as minor, deferred by instruction; the `Skill`
grant is TASK-019's under D-019.

## Commits

| sha | subject |
|---|---|
| 5bc3ec5 | amend §5.5 so the envelope delivers the layers it advertises |
| 548d3c1 | qa — result passed, two minor issues |
| cf80ea7 | qa — correct the issue count to four |
| d137505 | review — changes-requested, F-1 and F-2 major |
| 39393f8 | rework — close AC-2, F-1 and F-2 |
| f53ea20 | qa round 2 — passed, 5 of 5 plus 3 regression checks |
| 18ca84a | review round 2 — passed, F-1 and F-2 closed |

## CI

No checks reported on the branch, at 2026-08-27T00:24+02:00. The repository configures no workflows,
so this is the expected state and not a pending run. The task's own `test_command`
(`python3 scripts/check-templates.py`) ran green at 20/20 in qa round 2.

Merged 2026-08-27T18:04:40Z as merge commit `31d415e`, verified with `gh pr view`.
