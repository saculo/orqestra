---
id: TASK-056
type: task
status: pending
updated: 2026-09-01
phase: PHASE-1
module: plugin
stack: markdown
origin: feature
bug:
depends_on: [TASK-048]
serves: [PHASE-3/SC-1]
attempts: 0
---

## Goal

**"All envelopes conform" is true of the examples in the step files. Nothing checks the envelope that
is actually dispatched.**

`check-envelopes.py` finds literal `ROLE:` blocks in `skills/` and checks field presence by obligation
class (`scripts/check-envelopes.py:45-109`). What it does not check:

| unchecked | consequence |
|---|---|
| field **order** | §5.5 fixes an order; a reordered envelope passes |
| field **values** | `ROLE: orqestra:nonexistent-agent` passes |
| referenced agent, skill or template **exists** | a dispatch to a deleted persona passes |
| `MODULE` against `modules.md`, and `PATHS` against that row | a dispatch can claim a module it does not match |
| exactly one `WRITE:` owner, against D1 | D2's core rule is unchecked at the point it is declared |
| **the composed prompt** | the envelope the orchestrator builds at runtime is never inspected at all |

The last row is the subject. Envelopes are **prose assembled at dispatch time** from a template in a
step file plus values the orchestrator substitutes. The checker sees the template. Nothing sees the
substitution — so a step whose example is perfect can dispatch an envelope with an empty `MODULE`, a
`PATHS` that resolves to nothing, or a `WRITE:` pointing at the wrong task directory, and every check
in the repository stays green.

**TASK-030 delivered the static half and is done.** It verified the ten envelopes in the tree conform to
§5.5. This is the half it did not cover, and it is not a defect in that task — a done task is not
reopened (D-030, D3). TASK-048 adds envelopes to nineteen more step files, which multiplies the surface
this leaves unchecked, which is why it depends on it rather than racing it.

**The structural fix is bigger than a checker.** If an envelope were structured data rendered through
one function, the rendered result could be validated immediately before dispatch, and the static check
would become redundant rather than partial. That is a design decision — prose assembly is what the whole
plugin does today — and this task should make it deliberately rather than bolting a second grep onto the
existing one.

## Acceptance Criteria

| id | criterion |
|---|---|
| AC-1 | The envelope an orchestrator actually dispatches is validated before the dispatch, not only the example in the step file |
| AC-2 | Validation covers what the static check omits: field order, `ROLE`/`SKILL`/`TEMPLATE` resolving to files that exist, `MODULE` present in `modules.md`, `PATHS` matching that row, and exactly one `WRITE:` path |
| AC-3 | The `WRITE:` path is checked against D1's writer table, so a dispatch declaring a path the agent does not own fails at dispatch rather than after the write |
| AC-4 | A deliberate decision is recorded on whether envelopes become structured data rendered through one function, or stay prose with a runtime check — with the reason, since it governs every future step file (D-NNN) |
| AC-5 | The static checker and the runtime validation do not disagree: a step file that passes one passes the other, or the difference is stated |

## Out of Scope

**Adding envelopes to the steps that lack them.** TASK-048. This task validates envelopes; that one
creates them. Hence `depends_on: [TASK-048]` — validating nineteen absent envelopes is not useful.

**Detecting an out-of-contract write after the fact.** TASK-028 — that checks what a step *did*, this
checks what it was *told*. Both are needed and neither substitutes for the other.

**`REQUIREMENTS.md` §5.5.** `docs` (D14). If validation requires the section to state an order it only
implies, report it.
