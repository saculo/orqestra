<!--
  orqestra — skill authoring template
  ===================================
  Copy this file to skills/<skill-name>/SKILL.md and fill every ▢ blank.
  Delete every HTML comment before shipping.

  The FOLDER NAME is the invocation name: skills/init/ → /orqestra:init. There is no
  separate commands/ file — plugin skills ARE the slash commands, already namespaced.
  Add `argument-hint:` to the frontmatter when the skill takes arguments, and read them
  from $ARGUMENTS in the body.

  Pick the skill's CLASS first — it fixes allowed-tools, whether the skill may write,
  and whether it may dispatch. Everything else follows from the class.

  ┌────────────────┬──────────────────────────────────────────────┬────────────────────────────────────┐
  │ class          │ examples                                     │ allowed-tools                      │
  ├────────────────┼──────────────────────────────────────────────┼────────────────────────────────────┤
  │ orchestrator   │ orchestrate-greenfield, orchestrate-add-phase│ Read, Glob, Grep, Skill, Task,     │
  │                │ orchestrate-bugfix                           │ AskUserQuestion                    │
  │ orchestrator+  │ orchestrate-task, pr-comments                │ …the above, plus Bash (git, gh)    │
  │ planning       │ create-phases, create-phase, create-tasks,    │ Read, Write, Glob, Grep,           │
  │                │ create-task, clarify                         │ AskUserQuestion                    │
  │ step           │ plan, design                                 │ Read, Write, Glob, Grep            │
  │ step+build     │ implement, qa                                │ Read, Write, Edit, Glob, Grep, Bash│
  │ step+review    │ review-task, review-phase                    │ Read, Write, Glob, Grep, Bash      │
  │ query          │ status                                       │ Read, Glob, Grep                   │
  └────────────────┴──────────────────────────────────────────────┴────────────────────────────────────┘

  Two hard rules, both structural rather than aspirational:
    • An orchestrator NEVER holds Write or Edit. It reads state, dispatches, and gates.
    • A step skill NEVER holds Task. It does its own work; it does not sub-dispatch.
-->

---
name: ▢skill-name          # the FOLDER name; Claude Code prefixes the plugin namespace → /orqestra:▢skill-name
description: "▢One sentence: what it does, what it produces, and when to use it. Include the literal trigger phrases a user might type — this string is the only thing the model sees when deciding whether to load the skill."
allowed-tools: ▢per the class table above
---

> **Invocation**: ▢`/orqestra:<name>` · or: dispatched by ▢<orchestrator> at the ▢<step> step.
> **Class**: ▢orchestrator | planning | step | query

# ▢Skill Title

▢One paragraph. What you are, and the single thing you are responsible for.
▢State the boundary explicitly — what this skill must NOT do, especially where an adjacent
▢skill would plausibly claim the work.

## Inputs

<!-- Paths only. The dispatch envelope (§5.3) hands you paths; you read them yourself. -->

| Read | Why |
|---|---|
| ▢`.orqestra/…` | ▢ |
| `.orqestra/decisions/INDEX.md` | Settled decisions. **Always read.** Open a `D-NNN-*.md` only when a row touches your work. **Never re-litigate.** |

▢**When present**: `REWORK` in the envelope — the finding ids (`F-N`) or gate comment you must
▢address. Read the named artifact, fix exactly what it names, and do not re-do the rest.

## Output

<!-- Step and planning skills only. Orchestrators write nothing. -->

- **Writes**: ▢`.orqestra/…/ARTIFACT.md` — exactly one artifact.
- **Template**: `templates/▢ARTIFACT.md` — copy it, fill it, **change nothing structural**.
- **Schema**: §4.8 catalogue. Ordered headings, closed vocabularies, `_none_` for empty sections.

## Procedure

<!-- Numbered, imperative, testable. One action per step. This is the body of the skill. -->

1. ▢
2. ▢
3. Write the artifact from the template.
4. Verify your own output against the schema before returning: frontmatter keys present, values in
   vocabulary, headings present and in order, no undeclared headings, no blank required section.

## Return

<!-- What you hand back to the orchestrator. This is NOT the artifact. -->

Return **at most 10 lines**, and nothing else:

```
STATUS:  done | blocked
OUTCOME: ▢one line — what you produced or decided
▢KEY:    ▢2–4 lines of the detail a human needs at a gate
BLOCKED: <reason from §4.4.3> — <what a human must decide>   # only when STATUS: blocked
```

The orchestrator reads your artifact's **frontmatter only**, never its body. Your return text is what
reaches the human at a gate — so write it for a person, not for a log.

## When you cannot proceed

▢List the conditions that make this step impossible, each mapped to a `blocked_reason` (§4.4.3).
▢Emit a blocked return instead of guessing. Guessing produces work that is thrown away one step later.

| Condition | `blocked_reason` |
|---|---|
| ▢ | ▢ |

## Rules

1. ▢The non-obvious constraint that this skill gets wrong when written casually.
2. Stay inside your artifact. Do not write, fix, or tidy anything another step owns.
3. Do not invent scope. If the input is insufficient, block — do not fill the gap with plausible work.

<!--
  ─────────────────────────────────────────────────────────────────────────────
  ORCHESTRATORS ONLY — everything below replaces "Output"/"Procedure" above.
  ─────────────────────────────────────────────────────────────────────────────

  ## Steps

  Shard when the skill exceeds ~150 lines or has more than 4 steps. One file per step,
  loaded only when that step runs — this is the main context-economy lever.

      skills/<name>/
        SKILL.md              entry: state discovery, step index, rules
        step-<name>.md        named, never numbered — order lives in the index table


  | # | step | dispatches | gate |
  |---|---|---|---|
  | 01 | ▢ | ▢skill + agent + expertise | ▢yes/no |

  ## Dispatch

  Build the envelope per §5.3. Resolve the triple from config.md's routing table —
  never from the task's prose, never from intuition.

  ## Rules

  1. Never write an artifact. Enforced by allowed-tools.
  2. Determine position by invoking `orqestra:status` — never glob .orqestra/ yourself (§7.10).
  3. Never skip a gate the config declares.
  4. Never advance past `blocked`.
  5. One task at a time, in dependency order.
-->
