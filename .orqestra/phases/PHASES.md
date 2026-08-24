---
id: PHASES
type: phases
status: in-progress
updated: 2026-08-24
phase_count: 5
---

## Phases

| id | goal | criteria | status |
|---|---|---|---|
| PHASE-1 | The substrate: install, scaffold, and correctly report state | 6 | pending |
| PHASE-2 | Planning end to end: PRD → designed tasks, resumable | 6 | pending |
| PHASE-3 | The inner delivery loop, proven to converge | 7 | pending |
| PHASE-4 | The remote: branch, PR, comments, merge | 7 | pending |
| PHASE-5 | Lifecycle closure: add-phase, bugfix, close-phase | 7 | pending |

## Ordering Rationale

Each phase is deliverable given only what precedes it, and each is independently useful — you could
stop after any one and have something that works.

**PHASE-1 first because `status` is the state authority.** Every later phase calls it to decide where it
is, so a wrong stage derivation would surface as inexplicable misbehaviour in PHASE-2 rather than as a
clear failure here. Writing all 21 templates first is the same argument applied to schemas: a schema
with no template is one nobody has finished designing (D-003).

**PHASE-2 before PHASE-3 because planning exercises everything structural** — dispatch envelopes, the
return contract, gates, schemas, commits, state derivation — without touching git branches, `gh`, or CI.
If the envelope or the ≤10-line return is wrong, the cheapest possible place to find out is here, where
the only cost is a re-run. It is also where dogfooding starts: from PHASE-2 onward, orqestra plans its
own remaining work.

**PHASE-3 before PHASE-4 is the sharpest ordering decision.** The rework loop is the highest-risk
mechanism in the design that does not involve the network, and its specific danger is oscillation —
attempt 2 fixing what attempt 1 broke, forever. Proving it converges locally, where a bad run costs
nothing, must happen before adding branches and PRs that make every failure expensive to unwind.

**PHASE-4 fourth because its failure modes cannot be simulated honestly.** Every row of §7.4.2 — push
rejected, PR already open, CI red, merge conflict — needs a real remote to induce. Build it when it can
be tested, not before.

**PHASE-5 last because it is mostly composition.** `add-phase` reuses planning's tail, `bugfix` promotes
a bug into an ordinary task and reuses the whole delivery pipeline, `close-phase` reads artifacts that
by then exist. Little new machinery, which is exactly what belongs at the end — and its final criterion
is the real test of the whole tool: a phase planned and delivered by orqestra with no hand-editing.

**A note on what "pending" means here.** Much of the plugin source already exists as an untested draft.
The criteria are deliberately written as **observable behaviour**, not as "write skill X", so existing
source does not make any of them met. Nothing has been run. That is the honest state.
