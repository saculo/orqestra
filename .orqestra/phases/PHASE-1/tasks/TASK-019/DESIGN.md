---
id: TASK-019
type: design
status: done
updated: 2026-08-29
task: PHASE-1/TASK-019
decisions: [D-025]
---

<!-- BACKFILL, written 2026-08-29 against the tree at 9e7dec4. This task was built with no plan and
     no design; the omission was found at review and closed at the pipeline level by preflight
     check (c) (§7.4.3). This artifact did not guide the work. It is written at design altitude
     anyway — describing the shape the change should have, not the shape it happens to have — so
     that it can be disagreed with. Where the built thing and the designed thing differ, the
     difference is named rather than smoothed over. -->

## Components

Four components, each named with the criterion it serves. The interesting property is that they form
a chain in which **each one exists because the one before it cannot be trusted alone.**

| # | Component | Responsible for | Serves |
|---|---|---|---|
| 1 | **Capability grant** | Every persona in `agents/` holding `Skill` in its `tools:` allowlist, so a dispatched agent *can* invoke a skill at all | AC-4 (grant half); prerequisite for AC-2 |
| 2 | **Invocation instruction** | A single uniform persona rule telling the agent to invoke `SKILL` then every `EXPERTISE` skill before anything else, and stating these are **names, not paths** | AC-2, AC-3, AC-6 |
| 3 | **Envelope completeness** | Every dispatch envelope naming the step skill it expects invoked, in a `SKILL:` field | AC-2 |
| 4 | **Detection line** | Every envelope-dispatched skill opening its `## Return` with `SKILLS:` — the names actually invoked, or `none` | AC-4 (the grant is not evidence of a load) |
| 5 | **Decision record** | `D-025` carrying the choice, the rejected alternative with the fact that kills it, and a `**Constrains:**` register binding future tasks | AC-4 (record half) |

**Component 1 alone is the defect restated, not fixed.** A grant with no instruction changes nothing
an agent does. **Components 1+2 are still not enough**, because a `tools:` line grants a capability
and cannot compel its use — which is why component 4 is not optional polish but the only thing that
makes the mechanism observable. Component 3 exists because component 2 instructs invoking a field
that some envelope has to supply.

**One thing in the tree traces to no live criterion.** `scripts/check-envelopes.py` was built for
AC-5, which was removed from this task on 2026-08-27 and re-filed as TASK-030. A design written today
would not include it — by rule 2 it would be cut. It is recorded here as **inherited scope**, not as
a designed component, so that a reviewer sees it deliberately.

## Interfaces

Three contracts, all in Markdown, all already existing in the codebase and being extended rather than
invented.

**1 · Persona frontmatter — `agents/*.md`**

```
tools: Skill, Read, Write, Edit, Glob, Grep, Bash
```

A comma-separated allowlist. Under D-024 this is the **durable** allowlist binding the whole subagent
run, unlike a skill's `allowed-tools`, which only pre-approves for one turn. `Skill` leads the list in
every persona, so the eight lines stay diffable against each other. The per-persona remainder is
unchanged: `analyst` and `architect` gain no `Edit` and no `Bash`.

**2 · Dispatch envelope — the `ROLE:` block in `skills/*/step-*.md` and orchestrator `SKILL.md` files**

```
ROLE:      orqestra:qa-engineer
STEP:      qa
SKILL:     orqestra:qa                 ← the field this task adds
EXPERTISE: java-expertise, spring-conventions
```

`SKILL` and `EXPERTISE` carry **skill names**, never filesystem paths, and a step skill is never
routed through `READ`. This is the load-bearing part of the contract: `${CLAUDE_PLUGIN_ROOT}` expands
at invocation and **not** on `Read`, so a step skill opened as a file arrives with every `TEMPLATE:`
line inside it pointing at a literal token. The `EXPERTISE` value is resolved from the task's
`modules.md` row (§5.1) and from nowhere else.

**3 · Return contract — the fenced block under `## Return` in every envelope-dispatched skill**

```
SKILLS:   <the SKILL and EXPERTISE names you invoked, or `none`>
STATUS:   done | blocked
...
```

`SKILLS:` is the **first** line, not merely present. The ordinal is the contract because all eight
personas instruct *"Your first `RETURN` line names what you loaded"*, and a skill whose return block
disagrees with the persona dispatching into it is the drift this task exists to end.

## Structure

The change lands entirely inside the `plugin` module (`skills/`, `agents/`, `scripts/`). No `docs`
edit is required, which matters: §5.5 is `docs`, and D-019 puts the spec first for anything that
cites it — so this design deliberately touches nothing that would drag `REQUIREMENTS.md` into scope.

Three layers, and **the order they come together is not cosmetic:**

1. **The persona layer** (`agents/`) must gain the capability *before* the instruction to use it means
   anything. Granting and instructing in separate tasks would ship a persona telling an agent to do
   something its allowlist forbids — the exact defect AC-3 forbids, reintroduced in the other
   direction.
2. **The orchestration layer** (the dispatch envelopes inside `skills/*/`) supplies the value the
   persona instruction consumes. A persona instructing "invoke `SKILL`" against an envelope with no
   `SKILL` field is an instruction with nothing to act on.
3. **The step-skill layer** (each dispatched skill's `## Return`) closes the loop by reporting what
   layer 1 actually did. It depends on nothing and can land in any order relative to the others.

**What must not reach into what.** The expertise list lives in the `modules.md` row and nowhere else
— never hardcoded into a persona and never into a step skill. That is what keeps expertise
project-owned and dynamic: a project adds `spring-conventions` to its module row and the next dispatch
loads it, with no plugin change and no new agent. A persona that names its own expertise skills has
made the plugin the owner of a project's conventions, which is backwards.

**Uniformity is a structural property here, not tidiness.** The eight personas are byte-identical in
the edited region. Any verification must assert **8 of 8 present**, never "no occurrences of the old
text remain" — the two differ exactly in the case that matters, a replacement applied to seven.

## Decisions

- **`D-025` — agents hold `Skill`, and the triple is composed by invocation.** Recorded as a decision
  file rather than a local note because it constrains every future persona and every future step
  skill. Its `**Constrains:**` register carries four forward obligations: names never paths; every new
  `agents/*.md` holds `Skill`; the grant is not evidence of a load, so `SKILLS:` stays the first
  `## Return` line; the expertise list lives in the `modules.md` row alone.
- **Detection over enforcement, stated as such.** No layer available here can *compel* an agent to
  invoke a skill. Rather than pretend the instruction is a guarantee, the design names the gap and
  adds observability — §7.0.1's discipline applied to this task's own mechanism (D-025).
- **Local to this task: `skills/pr-comments/` is excluded.** It is invoked as a sub-workflow with a PR
  number, not dispatched with an envelope, and has no `## Return` section. It constrains nothing
  future, so it stays here rather than in a decision file.

## Test Strategy

Every criterion is checked by something that can fail. Presence alone is not evidence.

| Criterion | What proves it |
|---|---|
| **AC-2** — a dispatched agent receives the step procedure | A **live dispatch**, not a grep: an agent following instructions that exist only in its step skill and not in its persona. The honest limit is that this is the agent's own report; an independent probe needs a dispatching layer, which no agent holds (TASK-031) |
| **AC-3** — no persona instructs what its `tools:` forbids | Read all eight `tools:` lines against their own prose. `analyst` and `architect` hold neither `Edit` nor `Bash`; assert neither is instructed. **Also check the newly-delivered layer**: the step skill an analyst now actually loads must not instruct a forbidden action either — `plan` and `design` declare `disallowed-tools: Agent, Edit, NotebookEdit, Bash`, which agrees rather than conflicts |
| **AC-4** — grant half | Assert `Skill` in **8 of 8** `tools:` lines. Uniformity is the property; a 7-of-8 result is the failure mode |
| **AC-4** — record half | A conformance check that `D-025` carries `**Constrains:**`, **plus a negative control**: delete the line, confirm the checker reports it and exits 1, restore it, confirm exit 0. A check that has never been seen to fail proves nothing. The content bar is separate and human-judged: is each constraint a forward obligation naming the failure it prevents, or a restatement of the `**Why:**` above it? |
| **AC-6** — no persona instructs a path-read of a step skill | Grep `agents/` for `CLAUDE_PLUGIN_ROOT` and for skill-path shapes; both must be zero. Behavioural confirmation is stronger: an invoked step skill returns its template path **expanded** while the same token in a plain envelope line stays literal |

**The invariant that spans criteria**, and the one worth checking as a set rather than per file: the
nine skills named as a `SKILL:` target must each open their `## Return` with `SKILLS:`, and the skills
never dispatched with an envelope — `clarify`, `create-task`, `init` — must not be dragged in. Nine of
nine, three correctly absent.
