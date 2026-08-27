# Step — Phases

Dispatch `create-phases`, then gate.

## Skip when already done

`phases/PHASE-*/PHASE.md` exist → skip to tasks. Never regenerate phases over existing ones — task
directories hang off those ids (D8).

## Dispatch

```
ROLE:      orqestra:analyst
STEP:      create-phases
SKILL:      orqestra:create-phases
READ:
  .orqestra/PRD.md
  .orqestra/CLARIFICATIONS.md
  .orqestra/project/PROJECT.md
  .orqestra/modules.md
  .orqestra/decisions/INDEX.md
TEMPLATE:  ${CLAUDE_PLUGIN_ROOT}/templates/PHASES.md, ${CLAUDE_PLUGIN_ROOT}/templates/PHASE.md
WRITE:     .orqestra/phases/PHASES.md and .orqestra/phases/PHASE-N/PHASE.md
RETURN:    at most 10 lines.
```

## The gate

```
▸ GATE · phases · 3 phases planned

  PHASE-1  Authentication      4 criteria
  PHASE-2  Rate limiting       3 criteria
  PHASE-3  Admin console       5 criteria

  Order: auth first — everything else assumes an identity to attach limits and
  permissions to.

  [ Approve ]  [ Reorder ]  [ Reject with reason ]
```

**Reorder** re-dispatches with the requested order and re-gates. **Reject** re-dispatches with the
reason in `REWORK`.

Approve → commit, continue to tasks for PHASE-1.
