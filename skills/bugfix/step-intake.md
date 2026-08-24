# Step — Intake

Capture the bug. `work/BUG-NNN/BUG.md`, id `max(existing) + 1` (D8).

## Gather

From arguments, or interactively via `AskUserQuestion`:

- **What happens**, in the reporter's words — do not translate it into a theory yet
- **Steps to reproduce**, exactly as given
- **Expected vs actual**
- **Severity** — `blocker` | `major` | `minor`
- **Where it surfaces** — which module, if known

## Write

`${CLAUDE_PLUGIN_ROOT}/templates/BUG.md`, copied literally (D16).

Record the report **as reported**. If the reporter's description is wrong about the cause — it often is —
that is for diagnosis to establish with evidence, not for intake to correct. A rewritten report loses the
symptom that was actually observed.

## Report

```
✓ BUG-003 recorded · major · surfaces in api

→ reproducing
```
