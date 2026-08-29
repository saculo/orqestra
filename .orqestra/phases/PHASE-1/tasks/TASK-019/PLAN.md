---
id: TASK-019
type: plan
status: done
updated: 2026-08-29
task: PHASE-1/TASK-019
---

## Approach

**Written as a backfill, not as a record of foresight.** This task was built by direct human
instruction with no plan and no design; the omission was caught at review on 2026-08-29 and closed at
the pipeline level by preflight check (c) (§7.4.3). This artifact reconstructs the approach against
the tree at `9e7dec4` — every area below was opened and read, not inferred — so the task carries the
artifact its stage requires. It did not guide the work. Nothing here is dated earlier than it is.

The goal in one sentence: **make the step skill and the expertise skills actually reach a dispatched
agent, so §5.0's triple — *(step skill, subagent, expertise skills)* — delivers all three layers
instead of one.**

The approach has three parts, and the ordering between them is the whole of the reasoning:

1. **Grant the capability.** Add `Skill` to `tools:` in all eight `agents/*.md`. Under D-024 that list
   is a true allowlist binding the whole subagent run, so this is necessary before anything else can
   work.
2. **Instruct the invocation.** Replace the unexecutable *"Load the module expertise skills named in
   your envelope"* bullet — present in all eight personas, executable by none — with a block naming
   the `Skill` tool and stating that `SKILL` and `EXPERTISE` are **names, not paths**.
3. **Detect the omission.** A `tools:` grant cannot compel use. Every skill dispatched with an
   envelope opens its `## Return` with `SKILLS:`, so a step that ran bare is visible in the return the
   orchestrator already reads rather than three steps later.

**The alternative considered and rejected: pass skill paths in `READ` and let the agent read them.**
Cheaper — no allowlist change, no new instruction. It fails on one verified fact:
`${CLAUDE_PLUGIN_ROOT}` expands **at invocation and not on `Read`**. A step skill opened as a file
therefore arrives with every `TEMPLATE:` line inside it pointing at a literal token, so the agent
cannot find the template it is required to copy (D16). This was confirmed by a harness probe before
adoption, not assumed — the probe table is in `D-025`.

Part 3 is what makes the choice honest rather than hopeful, and it is why the task does not stop at
part 1. Naming the layer that holds a guarantee, and saying so plainly when no layer holds it, is the
§7.0.1 discipline applied to this task's own mechanism.

## Affected Areas

All inside the `plugin` module's `paths` (`skills/`, `agents/`, `templates/`, `scripts/`,
`.claude-plugin/`). Nothing here requires touching `docs`.

| Area | Files opened | What is there |
|---|---|---|
| Personas | `agents/` — all eight: `agentic-engineer`, `analyst`, `architect`, `backend-engineer`, `devops-engineer`, `frontend-engineer`, `qa-engineer`, `reviewer` | Each carries a `tools:` frontmatter line and an identical `## Rules`-style bullet list. The expertise-load bullet is byte-identical across all eight, which is what makes a uniform replacement safe |
| Dispatch envelopes | `skills/close-phase/SKILL.md`, `skills/greenfield/step-phases.md`, `step-tasks.md`, `step-plan-design.md`, `skills/add-phase/step-define-phase.md`, `skills/bugfix/step-diagnose.md`, `skills/task/step-implement.md`, `step-qa.md`, `step-review.md` | Nine files holding ten `ROLE:` envelopes. §5.5 fixes which fields each must carry |
| Return contracts | `skills/implement/`, `qa/`, `plan/`, `design/`, `review-task/`, `review-phase/`, `create-tasks/`, `create-phases/`, `create-phase/` — the `## Return` fenced block in each | Nine skills are named as a `SKILL:` target by some envelope. `clarify/`, `create-task/` and `init/` also have return blocks but are never envelope-dispatched, so they are correctly out of scope |
| Registry | `.orqestra/modules.md` | The `plugin` row supplies `expertise: claude-expert, orqestra-conventions`. Read only — the expertise list must stay here and nowhere else |
| Conformance scripts | `scripts/check-templates.py` | The existing dev-only checker, and the pattern any new checker should follow: CPython 3 stdlib only, exits 0/1/2, no runtime dependency from the plugin (D-001, D-015) |

**Verified, not assumed:** `skills/pr-comments/` was opened and is genuinely out of scope — it is
invoked as a sub-workflow with a PR number, not dispatched with an envelope, and has no `## Return`
section at all.

## Risks

- **`tools:` grants a capability; nothing compels its use.** The central risk of the whole approach.
  Adding `Skill` makes the invocation possible and leaves it entirely to the agent's compliance. This
  is why part 3 exists, and it is the reason a passing artifact is not evidence the skills loaded.
- **A change to `agents/` cannot be verified live in the session that makes it.** Agent and skill
  definitions are read at session start, so the engineer editing a persona is still running the old
  one. Any claim of live verification must come from a *later* dispatch, which means the implement
  step structurally cannot prove its own change works.
- **`skills/bugfix/step-diagnose.md` has no step skill to name.** `skills/diagnose/` does not exist
  (TASK-024). Adding `SKILL:` there requires inventing a skill name, which would make a conformance
  check green by lying to it — the one outcome worse than the check being red.
- **§5.5's always-class is wrong for a dispatch with no single scope unit.** `create-phases` creates
  *all* phases, so it has no `TASK`/`PHASE`/`BUG` value to carry, yet §5.5 puts the scope field in the
  always class. §5.5 is `docs`, and D-019 puts docs first for anything that cites it.
- **The eight personas are byte-identical in the region being edited.** That is what makes the change
  safe, and it is also the risk: a replacement applied to seven of eight leaves one agent silently on
  the old text, and the artifacts would still look fine. Any check must assert 8 of 8, never "no
  occurrences remain".

## Open Questions

Both were live when this task was planned and both were settled by human decision on 2026-08-27 under
§8.2, after qa graded the task 4 of 6. Recorded here because the plan is what should have surfaced
them, and suppressing them is what turned them into failed criteria instead of scoped work.

1. **Can a live-dispatch probe be run from inside this module?** No — the expertise skills live in
   `.claude/skills/`, outside the `plugin` module's `paths`, and no agent in `agents/` holds a
   dispatch tool. Neither implement nor qa can run the probe AC-1 required. **Re-filed as TASK-031.**
2. **What happens to the two envelopes that cannot conform?** Neither is fixable here: one waits on
   `skills/diagnose/` (TASK-024), the other on a §5.5 correction in the `docs` module (D-019).
   **Re-filed as TASK-030.**
