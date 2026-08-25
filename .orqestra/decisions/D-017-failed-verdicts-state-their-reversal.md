---
id: D-017
type: decision
status: active
updated: 2026-08-25
area: schemas
supersedes: —
superseded_by: —
---

# D-017 — A `failed` verdict must state what would reverse it, enforced by schema

**When:** 2026-08-25 · PHASE-1 / TASK-005 · deferred to PHASE-3
**Decision:** `REVIEW.md` gains a required heading `## What Would Change This Verdict`, carrying
`_none_` when the verdict is not `failed`. The orchestrator's contract check rejects an empty section on
a `failed` verdict.

**Why:** D-015 gave a `failed` review a re-review route, and that route is worthless without a stated
disagreement criterion. A re-review of *"this is wrong"* re-rolls the dice; a re-review of *"AC-3
requires at-least-once delivery and this publisher cannot provide it — if the publisher is actually
transactional, I am wrong"* is a question someone can answer.

D-015 added the requirement **as prose in one skill's body, enforced by nothing** — which is the exact
class of rule that decayed twice in a single session: the `D15` citation drift, and `init` composing
files instead of copying them. Both read fine and were checked by nothing. §4.4.5 and D12 say structure
is enforced by schema and contract check, not by asking nicely; this rule was asking nicely.

**Constrains:** PHASE-3 implements this. No new mechanism is needed — the `_none_` convention (§4.4.2)
already covers "not applicable":

- `${CLAUDE_PLUGIN_ROOT}/templates/REVIEW.md` gains the heading.
- The §4.8.1 catalogue row for `REVIEW.md` lists it, so `check-templates.py` verifies the template.
- `review-task` must fill it on `failed` — stating the fact that would reverse the verdict, not a
  restatement of the finding.

More generally: **a rule that only exists as prose is not a rule.** Where a constraint matters, put it
in the schema and let the check enforce it.
