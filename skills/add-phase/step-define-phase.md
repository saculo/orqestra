# Step — Define Phase

Dispatch `create-phase` (singular), then gate.

## Check the PRD first

The new phase's criteria must be derivable from the PRD. **If the work was never described there,
stop and ask** whether to update `PRD.md` and re-run `/orqestra:clarify` first.

This is the most likely place for scope to enter a project unnoticed, because by phase three nobody
rereads the PRD, and a phase invented at this point looks exactly like a planned one afterwards (D11).

## Dispatch

```
ROLE:      analyst
STEP:      create-phase
READ:
  .orqestra/PRD.md
  .orqestra/CLARIFICATIONS.md
  .orqestra/phases/PHASES.md
  .orqestra/phases/PHASE-<prev>/PHASE_SUMMARY.md
  .orqestra/modules.md
  .orqestra/decisions/INDEX.md
TEMPLATE:  templates/PHASE.md
WRITE:     .orqestra/phases/PHASE-N/PHASE.md
RETURN:    at most 10 lines.
```

The previous `PHASE_SUMMARY.md` is in the read list deliberately: accepted gaps and carried tech debt
are the most common legitimate source of a next phase's criteria.

## The gate

```
▸ GATE · phase · PHASE-2 · Rate limiting

  SC-1  requests beyond the plan limit return 429 with a Retry-After header
  SC-2  limits are configurable per plan without a deploy
  SC-3  operators can see current usage per tenant

  Basis: PRD "Fair use" section; also closes the PHASE-1 debt item on
         unbounded /auth/token calls.

  [ Approve ]  [ Reject with reason ]
```

**`Basis` is the line to read carefully** — it is how you check the phase was not invented.

Approve → commit, continue to tasks.
