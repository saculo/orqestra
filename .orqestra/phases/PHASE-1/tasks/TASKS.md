---
id: TASKS-PHASE-1
type: tasks
status: in-progress
updated: 2026-08-27
phase: PHASE-1
task_count: 41
---

## Tasks

| id | title | module | depends_on | serves |
|---|---|---|---|---|
| TASK-001 | Artifact templates conform to the schema catalogue | plugin | — | SC-5 |
| TASK-002 | Plugin manifest and command wiring | plugin | — | SC-1 |
| TASK-003 | init scaffolds a complete workspace | plugin | TASK-001, TASK-002 | SC-2 |
| TASK-004 | init refuses to destroy existing work | plugin | TASK-003 | SC-3 |
| TASK-005 | status derives every task stage correctly | plugin | TASK-001, TASK-002 | SC-4 |
| TASK-006 | status reports what is next | plugin | TASK-005 | SC-6 |
| TASK-007 | Reconcile the specification with the shipped tree | docs | TASK-001 | SC-5 |
| TASK-008 | Fix the checker coverage hole and exit codes | plugin | — | SC-5 |
| TASK-010 | Specification records the commit convention | docs | — | SC-2 |
| TASK-009 | Commits are identified by task id, not commit type | plugin | TASK-010 | SC-2 |
| TASK-011 | Orchestrators must not write artifacts | docs | — | SC-7 |
| TASK-012 | Branch created at preflight, not at push | docs | — | PHASE-3/SC-1 |
| TASK-013 | `blocked_reason` and the status vocabulary in the catalogue | docs | — | SC-5 |
| TASK-014 | `status` may read configuration, not only frontmatter | docs | — | SC-4 |
| TASK-015 | The dispatch envelope delivers the layers it advertises | docs | — | PHASE-3/SC-1 |
| TASK-016 | A parked gate records enough to be resumed | docs | TASK-011 | SC-7 |
| TASK-017 | An accepted phase gap must not wedge planning | docs | — | PHASE-5/SC-1 |
| TASK-018 | `PROJECT.md` has an owner that populates it | docs | — | SC-5 |
| TASK-019 | Dispatched agents can reach their step and expertise skills | plugin | TASK-015 | PHASE-3/SC-1 |
| TASK-020 | Pipeline branches at preflight | plugin | TASK-012 | PHASE-3/SC-1 |
| TASK-021 | `init` produces a workspace `greenfield` can use | plugin | — | SC-2 |
| TASK-022 | PR review threads via a command that exists | plugin | — | PHASE-4/SC-1 |
| TASK-023 | Workspace mode enforces what template mode enforces | plugin | TASK-013 | SC-5 |
| TASK-024 | Every referenced step file exists | plugin | — | SC-1 |
| TASK-025 | Split mode and gap mode stop contradicting themselves | plugin | TASK-017 | PHASE-5/SC-1 |
| TASK-026 | `bugfix` leaves a tree its own task can be delivered from | plugin | TASK-020 | PHASE-5/SC-1 |
| TASK-027 | Skills implement writer discipline and gate state | plugin | TASK-011, TASK-016 | SC-7 |
| TASK-028 | Detect a write outside the dispatch contract | docs | TASK-011 | SC-7 |
| TASK-029 | §5.5's always-class reaches a scope-less dispatch | docs | — | PHASE-3/SC-1 |
| TASK-030 | Every envelope conforms, and the suite proves it | plugin | TASK-024, TASK-029 | PHASE-3/SC-1 |
| TASK-031 | Prove EXPERTISE changes what a dispatched agent does | plugin | — | PHASE-3/SC-1 |
| TASK-032 | qa needs a route for a failure implement cannot fix | docs | — | PHASE-3/SC-1 |
| TASK-033 | Specification makes room for a diagnose skill | docs | — | PHASE-3/SC-1 |
| TASK-034 | The diagnose step has a procedure of its own | plugin | TASK-033 | PHASE-3/SC-1 |
| TASK-035 | Routing names an agent that can do the work | plugin | — | PHASE-3/SC-1 |
| TASK-036 | The reference checker enforces D-026's third position | plugin | — | PHASE-3/SC-1 |
| TASK-037 | The spec and BUG.md agree about a bug's module | docs | — | PHASE-3/SC-1 |
| TASK-038 | The three skill enumerations are checked against each other | plugin | — | PHASE-3/SC-1 |
| TASK-039 | bugfix rule 3 agrees with its own step file | plugin | — | PHASE-3/SC-1 |
| TASK-040 | BUG.md carries the module the spec says it carries | plugin | TASK-037 | PHASE-3/SC-1 |
| TASK-041 | A recorded decision reaches the index | plugin | — | PHASE-3/SC-1 |

## Dependency Order

```
TASK-001  templates + conformance check ─┬─→ TASK-003 init scaffold ──→ TASK-004 init guards
TASK-002  manifest + commands ───────────┤
                                         ├─→ TASK-005 status derivation ──→ TASK-006 status reporting
                                         └─→ TASK-007 spec reconciliation
```

**Delivery order**: TASK-001, TASK-002, TASK-003, TASK-004, TASK-005, TASK-006, TASK-007, TASK-008,
TASK-010, TASK-009.

**TASK-010 before TASK-009** — reversed on 2026-08-25 after a pipeline run proved the original order
unsatisfiable. The skills **cite** §4.6 rather than restating it, so the specification has to be right
before the implementation can be (see D-019).

**Added mid-phase** (2026-08-25): TASK-008 from TASK-001's review findings; TASK-009 and TASK-010 from a
convention change requested during the phase. All three are `create-task --mode add`, and all cite an
existing success criterion — none of them widened the phase's goal.

Seven sequential PRs. TASK-001 and TASK-002 are genuinely independent and TASK-004, TASK-006, and
TASK-007 sit on separate branches of the graph — but v1 delivers one task at a time (D15), so the graph
buys ordering safety rather than speed.

**Every dependency here is real**, which matters because each one stalls delivery until the other task
is *merged* (§7.4.1), not merely done:

- **TASK-003 and TASK-005 both need TASK-001**, because both are verified against templates, and a
  fixture built from a non-conforming template proves nothing.
- **Both need TASK-002**, because their criteria are written as `/orqestra:init` and `/orqestra:status` —
  behaviour through the command, not a skill invoked by hand.
- **TASK-004 needs TASK-003**: you cannot test refusing to overwrite a workspace before one can be
  created.
- **TASK-006 needs TASK-005**: reporting a stage requires deriving it first.
- **TASK-007 needs TASK-001**: the reconciliation is driven by what the conformance check reports, not
  by re-reading the catalogue by eye.

## Notes on the decomposition

**TASK-003 and TASK-004 are one skill split in two.** Combining `init`'s happy path with its refusal
behaviour produced eight acceptance criteria — past the point where a task is two tasks wearing one name
(§7.6.1). Splitting kept every criterion; shrinking would have dropped the safety ones, which are the
ones that matter when someone runs `init` twice.

**TASK-007 is the phase's only `docs` task**, and it exists because of D14. TASK-001 makes templates
conform to the catalogue *as written*; where the catalogue itself is wrong, fixing it touches
`REQUIREMENTS.md` — a different module, therefore a different task, therefore a different PR reviewed by
whoever owns the spec. Its agent is `architect`, not an engineer.

**No task writes new skills.** The plugin source for `init`, `status`, the commands, and the templates
already exists as an untested draft. Every criterion here is written as observable behaviour precisely
so that existing source does not satisfy it — nothing has been run.

**Added 2026-08-26**: TASK-011, from running the delivery pipeline on TASK-008. Three of the four
unexecutable gate-write instructions were hit in that single run, and `PR.md` — the one D1 row naming
an orchestrator as sole writer — could not be written at all, which is why TASK-008 is parked at
`push` with PR #2 open. `docs` module, so `architect`, and the plugin change that follows it is a
separate task and a separate PR (D-019).

**Added 2026-08-26, from `ORQESTRA_AUDIT.md`**: TASK-012 through TASK-027. Sixteen tasks from an audit
of every shipped skill, step file, agent, template, the checker, and the manifest. Seven of its claims
were independently verified before filing; all seven held.

**`docs` before `plugin`, without exception** (D-019). Eight of these are specification tasks and eight
implement them. Every plugin task depends on its docs counterpart because the skills **cite** the spec
rather than restating it — the same ordering that had to be discovered the hard way when TASK-009 and
TASK-010 were reversed mid-phase after a pipeline run failed qa 3 of 5.

**Delivery order.** The docs tasks are independent of each other and can go in any order; the pairs are
what matter:

```
TASK-015 → TASK-019    envelope contract  → agents reach their skills   ← start here
TASK-012 → TASK-020    branch timing      → pipeline branches early
TASK-011 → TASK-027    writer discipline  → skills stop writing         (also needs TASK-016)
TASK-013 → TASK-023    schema vocabulary  → checker enforces it
TASK-017 → TASK-025    gap acceptance     → split and gap modes
TASK-020 → TASK-026    (branch timing)    → bugfix reproduction
```

TASK-021, TASK-022, TASK-024, TASK-018 and TASK-014 have no plugin/docs pairing and can run whenever.

**CRITERION GAP.** Seven of these serve criteria in phases that are not yet planned — written as
`PHASE-3/SC-1`, `PHASE-4/SC-1`, `PHASE-5/SC-1` rather than forced onto a PHASE-1 criterion that does not
fit. They are substrate defects found while delivering PHASE-1, but the behaviour they fix belongs to
later phases. Whether they stay here, move when those phases are planned, or justify more PHASE-1
criteria is a phase-definition decision (§8.2) and a human's call.
