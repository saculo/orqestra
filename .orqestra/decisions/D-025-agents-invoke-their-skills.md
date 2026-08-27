---
id: D-025
type: decision
status: active
updated: 2026-08-27
area: structure
supersedes: —
superseded_by: —
---

# D-025 — Agents hold `Skill`, and the triple is composed by invocation

**When:** 2026-08-27 · PHASE-1 · found by tracing what an implement step actually calls
**Decision:** every agent in `agents/` holds `Skill` in `tools:`, and the dispatched agent invokes its
`SKILL` and `EXPERTISE` before doing anything else. That invocation is how §5.0's triple —
*(step skill, subagent, expertise skills)* — is composed at dispatch.

**Why:** the triple is the central mechanism of the design and only one of its three layers was
arriving. No agent held `Skill`, so no dispatched agent could invoke the step skill that carries its
procedure, or the expertise skills that carry the project's conventions. What ran was the persona alone,
plus whatever prose the orchestrator put in the envelope.

It failed silently, which is why it survived so long. All eight personas instructed a load they could
not perform; the artifacts came out good because the personas duplicate much of the step procedure. The
cost surfaced on 2026-08-27, when a dispatched `qa-engineer` committed and wrote another step's
`REVIEW.md` — both forbidden by `skills/qa/SKILL.md`, a file it never loaded. The same prohibition,
placed inline in the next envelope, was obeyed.

**Verified before adoption, not assumed.** A subagent was dispatched to probe the harness:

| question | result |
|---|---|
| Is `Skill` available to a subagent? | yes |
| Does `Skill("orqestra:implement")` load the body? | yes — quoted back from the returned text |
| Does `Skill("orqestra-conventions")` load a bare, non-namespaced expertise skill? | yes |
| Does `${CLAUDE_PLUGIN_ROOT}` expand for a subagent? | **yes**, to a real absolute path, never literal |

The last row is what rules out the cheap alternative. Passing skill *paths* in `READ` and letting the
agent read them leaves every `TEMPLATE:` line inside a step skill unresolvable, because
`${CLAUDE_PLUGIN_ROOT}` expands **at invocation and not on `Read`**. Names invoked, never paths read.

**Why the expertise list stays in `modules.md`.** No agent frontmatter field preloads skills — the
fields are `name`, `description`, `tools`, `disallowedTools`. So composition can only happen at
dispatch, through the envelope, which is what makes it dynamic: a project adds `spring-conventions` to
its module row and the next dispatch loads it, with no change to the plugin and no new agent.

**The instruction is not a structural guarantee, so it is made observable instead.** `tools:` grants the
capability; it cannot compel the agent to use it. Every step skill's `RETURN` therefore opens with
`SKILLS:` — the names actually invoked, or `none`. A step that ran bare is then visible in the return
the orchestrator already reads, rather than three steps later. This is the §7.0.1 discipline applied to
itself: name the layer that holds the guarantee, and when no layer holds it, say so and detect instead.
