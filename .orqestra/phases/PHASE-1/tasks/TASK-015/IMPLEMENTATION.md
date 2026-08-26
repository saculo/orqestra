---
id: TASK-015
type: implementation
status: done
updated: 2026-08-26
task: TASK-015
deviation: none
files_changed: 1
---

## Changes

All five components landed in `REQUIREMENTS.md` §5.5, between its heading and §5.5.1. No other file
was touched, and no heading was added, moved, or renumbered — §5.5 is still line 856, §5.5.1 moved
from 896 to 950 without changing its number, and every section after it shifted by exactly the same
+54 lines, which is the check that no text outside §5.5's body changed.

**C1 — `EXPERTISE` rewritten (AC-1).** The old sentence *"`EXPERTISE` names skills the agent loads
first"* is gone. `EXPERTISE` now names bare, un-namespaced project skills (§5.3) that the agent
**invokes**, and the paragraph states the precondition in its own text: `Skill` must appear in the
dispatched agent's `agents/*.md` `tools:`, the only layer that binds for a whole subagent run (§7.0.1,
D-024). It names the failure when the precondition is unmet — `SKILL` and `EXPERTISE` both inert, the
dispatch degrading silently to the bare persona rather than failing.

**C2 — `SKILL` introduced (AC-4).** A new field between `STEP` and the scope, defined as the
namespaced plugin step skill the agent invokes. The paragraph separates it from `STEP` using the case
that proves one field cannot serve both — `STEP: review` runs `SKILL: orqestra:review-task` (§5.1.1) —
and names its consumer (the dispatched agent) and its reason (D4: a procedure not named in the
envelope is one the agent has to invent).

**C3 — the invocation rationale (AC-5).** One paragraph records the expansion asymmetry:
`${CLAUDE_PLUGIN_ROOT}` expands when a skill is *invoked* and stays a literal string on `Read`, so a
step skill obtained by reading hands the agent a `TEMPLATE:` path it cannot open — which makes D16
unfollowable. That is why `SKILL` carries a name rather than a path. The same paragraph explains why
the envelope's own `TEMPLATE:` line may carry the prefix (the orchestrator composes it from inside an
invoked skill), and the line itself was corrected from the bare, unresolvable
`templates/IMPLEMENTATION.md`.

**C4 — the field table (AC-2).** Three obligation classes in a table after the example: always
mandatory; the scope field (exactly one of `TASK`/`PHASE`/`BUG`); conditional on the scope unit having
a module, which is decidable from `TASK.md`/`BUG.md` frontmatter the orchestrator has already read;
plus `EXPERTISE`'s additional empty-cell condition and `REWORK`'s re-dispatch-only class. The
closing sentence states the consequence AC-2 asks for — an omission is a contract violation, rejected
as a missing `WRITE:` is (D2). `MODULE` and `PATHS` are *defined* in their own paragraph, not merely
listed: `MODULE` as the routing key that resolved the whole row (§5.1, D-004), `PATHS` as the boundary
`review-task` checks the diff against (§5.2, §7.8.1, D2), each with its consumer named (Rule B).

**C5 — the example corrected (AC-3).** It now carries `SKILL`, `MODULE`, and `PATHS` in the fixed
order, with values consistent with §5.1's `api` row and §5's own `TASK-007` example. `MODULE:` and
`PATHS:` previously appeared nowhere in `REQUIREMENTS.md`.

## Deviations

| deviation | from design | what | why |
|---|---|---|---|

_none_

## Tech Debt

- **Nine envelopes in `skills/` are non-conformant as of this merge**, plus `skills/task/SKILL.md:64`,
  which restates §5.5's field list inline and now disagrees with it. That is the intended sequencing,
  not an oversight: `skills/` and `agents/` are the `plugin` module and TASK-019's work (D14), and the
  spec leads when a skill cites it (D-019). Until TASK-019 merges the gap is a live inconsistency
  rather than a pending one.
- **`agents/architect.md` grants no `Edit`.** The `docs` module routes `implement` to `architect`
  (§5.1.1), so amending a 2031-line `REQUIREMENTS.md` had to be done by rewriting the whole file
  through `Write`. It was verified byte-stable by heading count and by every post-§5.5 anchor shifting
  by exactly +54 lines, but the mechanism contradicts D16's own reasoning about reproducing structure
  from context and scales badly with the file. The fix is one word in `agents/architect.md` `tools:` —
  TASK-019's file, and worth raising there alongside the `Skill` grant this amendment presupposes.
