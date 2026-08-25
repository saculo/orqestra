---
id: D-024
type: decision
status: active
updated: 2026-08-25
area: structure
supersedes: —
superseded_by: —
---

# D-024 — `allowed-tools` never enforced; the guarantee lives in `agents/`, and lasts one turn in a skill

**When:** 2026-08-25 · PHASE-1 · found while auditing `review-task`'s "you hold no `Edit`" claim
**Decision:** orqestra states which layer carries every tool guarantee, and stops calling a guarantee
structural without naming the field that holds it (§7.0.1).

| Layer | Field | Binds? | For how long |
|---|---|---|---|
| Dispatched subagent | `agents/*.md` `tools:` | **yes**, true allowlist | whole subagent run |
| Dispatched subagent | `agents/*.md` `disallowedTools:` | **yes**, denylist | whole subagent run |
| Skill | `disallowed-tools:` | **yes**, removed from pool | until the user's next message |
| Skill | `allowed-tools:` | **no** — pre-approval only | never restricts |

**Why:** §7.0 said the two hard rules were *"enforced by the tool list rather than by instruction, which
is the point"*, and §4.4.5 cited that as its guarantee that no orchestrator ever patches an artifact.
Claude Code's documentation says the opposite of `allowed-tools`: it lists tools callable *without a
permission prompt*, and *"does not restrict which tools are available: every tool remains callable."*
Twenty-two skills, `templates/SKILL.template.md`, and this project's own `claude-expert` skill all
taught the false version. The error's direction is what made it expensive: **it claimed a guarantee that
did not exist, so nobody built the one that would have.**

**What the correction buys, and what it costs.** Every step skill runs inside a dispatched subagent, and
`agents/*.md` `tools:` *is* a real allowlist — so "a step skill never dispatches" and "the reviewer
holds no `Edit`" were true all along, just for a different reason than stated. The loss is at the top:
**orchestrators run in the main session**, so their only mechanism is `disallowed-tools`, which clears
at the user's next message — and an orchestrator gates for user input by design. The rule that most
needed enforcing is the one least enforceable, and that is now written down rather than assumed away.

**Two further defects surfaced from the same audit:**

- **The subagent tool is `Agent`, not `Task`.** Every orchestrator pre-approved a tool under its former
  name, so every real dispatch would have prompted. Renamed throughout.
- **`approve`, `reject`, `unblock` declared `Class: orchestrator+` while holding `Write` and `Edit`** —
  the exact combination §4.4.5 relied on being impossible. They are now the `control` class. Their real
  constraint is **scope, not tools**: one frontmatter field, one artifact, on a human's instruction. No
  tool list expresses that, so it is a stated rule and a named exception.

**Constrains:**

- Never describe a tool restriction as structural without naming the field and the layer. `allowed-tools`
  is never that field.
- A guarantee that must survive a gate cannot live in a skill. Put it in `agents/*.md`, or accept that
  it is behavioural and label it so.
- Skill frontmatter uses `disallowed-tools` (kebab); agent frontmatter uses `disallowedTools` (camel). A
  camelCase key in a `SKILL.md` is silently ignored — no error, no effect.
- `Bash` cannot be narrowed in `agents/*.md`, only in a skill's `allowed-tools` via `Bash(cmd:*)`. Where
  an agent needs `Bash` at all (`reviewer`, the engineers, `qa-engineer`), everything else it might run
  is governed by prose, and that prose must say so plainly rather than implying a tool-level guarantee.
- Durable session-wide enforcement needs a `PreToolUse` hook or a `settings.json` deny rule. Deferred as
  optional hardening (§7.0.1), on the same reasoning as the `git checkout -b` hook in §7.4.2.
