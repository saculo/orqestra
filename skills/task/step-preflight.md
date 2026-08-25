# Step — Preflight

Three checks, in order. **All must pass before any work happens.** Nothing is written, no branch is
created, so a failure here costs nothing to unwind — which is the entire reason this step exists.

## (a) Dependencies

For each id in `TASK.md.depends_on`, read that task's `TASK.md` and `PR.md` frontmatter:

- `TASK.md.status: done` **and** `PR.md.pr_state: merged` → satisfied.
- Anything else → **block**, `blocked_reason: deps-unmerged`.

**`done` is not enough — it must be merged.** A task marked done whose PR is still open has its code
on a branch, not on the base. A dependent task would branch from a tree missing the very thing it
depends on, and the conflict surfaces at push, after implement, qa, and review have all been paid for.

Report which dependencies are unsatisfied and their current stage:

```
⛔ TASK-007 blocked · deps-unmerged
   TASK-004 is at stage `pushed` (PR #139 open, not merged).
   → merge #139, then: /orqestra:task TASK-007
```

`require_merged_deps: false` in `config.md` relaxes this to `status: done`. Off by default.

## (b) Working tree

| Check | Command | On failure |
|---|---|---|
| Tree is clean | `git status --porcelain` | **block** `dirty-tree` — never stash, never commit someone else's work |
| On the base branch | `git branch --show-current` | check out the base; if that fails, **block** `branch-conflict` |
| Base current with origin | `git rev-list --count @..@{u}` | `git pull --ff-only`; fails → **block** `branch-conflict` |

A dirty tree is always a human's uncommitted work. Touching it is the one mistake that loses something
orqestra cannot recreate.

## (c) Design freshness

`DESIGN.md` was written during planning, possibly before several tasks merged. Check whether it still
holds against current HEAD:

1. Do the areas and boundaries in `## Structure` still exist as the design describes them?
2. Do the interfaces in `## Interfaces` still match the real code?
3. Has a merged task since changed something the design assumes?
4. Do any `decisions/` rows added since the design was written contradict it?

**Holds** → continue to implement.

**Stale** → dispatch `design` with the existing `DESIGN.md` as the starting point and a note of what
HEAD invalidated. It refreshes rather than rewrites. Then **re-gate the design** — a human approved the
old one, and they have not seen this.

Judgement call: prefer refreshing when genuinely uncertain. A stale design costs a rework cycle at
review; an unnecessary refresh costs one dispatch.

## On success

Report one line and continue. Preflight is silent when everything is fine — it earns attention only
when it stops something.

```
✓ preflight · deps merged · tree clean · design holds
```
