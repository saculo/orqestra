---
name: unblock
argument-hint: "<ID>"
description: "Clears a blocked orqestra artifact after its cause has been addressed, resetting it to in-progress and recording the human intervention. Use when the user says '/orqestra:unblock', or after fixing whatever caused a task to block."
allowed-tools: Read, Write, Edit, Glob, Grep, Skill, Agent, Bash
disallowed-tools: NotebookEdit
---

> **Arguments**: `/orqestra:unblock <ID>` · **Class**: control

# orqestra Unblock

The sanctioned way out of a `blocked` state (§8.1).

**A blocked task re-dispatched unchanged blocks again on the same step.** This is the rule people break
every time, because unblocking feels like progress. It is not — it is the *record* that progress was
made somewhere else.

## Procedure

1. Read the artifact named in `$ARGUMENTS` and show its recorded `blocked_reason` and explanation.
2. **Ask what was addressed.** Do not accept "it's fine now" — ask what changed, because the answer is
   what gets recorded and what a reader needs next month.
3. Check the answer against the reason. Some blocks cannot be cleared by unblocking at all:

   | `blocked_reason` | What must have changed first |
   |---|---|
   | `deps-unmerged` | The dependency's PR is merged — verify with `gh`, do not take it on trust |
   | `contract` | The schema violation is understood; re-running alone will repeat it |
   | `max-attempts` | The **cause** changed — the task, the design, or the criteria. Not just a wish to retry |
   | `needs-splitting` | The task was actually split (`/orqestra:create-task --mode split`) |
   | `criterion-unsatisfiable` | The criterion was rewritten — this is a `TASK.md` change, not a re-run |
   | `no-reproduction` | A reproduction now exists |
   | `merge-conflict`, `ci-red`, `dirty-tree` | The real-world condition is resolved |

   If nothing changed, **say so and stop**. Unblocking here burns another cycle to arrive at the same
   block.
4. Set `status: in-progress`, `attempts: 0`.
5. **Append a line to the artifact** recording that a human intervened, when, and why. An unblock with
   no record is indistinguishable from a bug next week.
6. Commit (§4.6), then name the command that resumes the workflow.

## Rules

1. **Fix the cause first.** Always.
2. **Never unblock to "see if it works this time."** Nothing is non-deterministic enough for that to be
   a strategy.
3. **Never clear `deps-unmerged` without verifying the merge.** Believing it is exactly the failure the
   dependency gate exists to prevent (§7.4.1).
4. Resetting `attempts` is legitimate only because the inputs genuinely changed. If they did not, do not
   reset it.
