# Step — Preflight

Three checks. All must pass.

## 1. orqestra-managed

`.orqestra/config.md` must exist. If not, this project was not built by orqestra, and v1 has no adoption
path (§1.3 principle 6). Say so plainly rather than offering a partial workaround — planning a phase
onto an unmapped codebase produces tasks that reference modules and conventions nobody recorded.

## 2. The previous phase is closed

Its `PHASE.md` is `status: done` **and** `PHASE_SUMMARY.md` has `criteria_met: true` (or an explicitly
accepted gap).

Not closed → **stop**. Run `/orqestra:close-phase <N>` first.

This matters more than it looks: planning a new phase over an unverified one builds on a milestone
nobody confirmed was reached. If it was not, the new phase inherits the gap silently and the gap
compounds — a criterion missed in PHASE-1 is found in PHASE-4, three phases of work later.

## 3. Nothing parked

Invoke `orqestra:status`. Anything `blocked` or `awaiting-approval` → report it and stop. A parked task
from the previous phase is not finished business to plan around.

## On success

```
✓ preflight · PHASE-1 closed (4/4 criteria) · nothing parked
```
