---
id: D-031
type: decision
status: active
updated: 2026-08-31
area: structure
supersedes: —
superseded_by: —
---

# D-031 — What a skill's tool fields actually do, probed

**When:** 2026-08-31 · PHASE-1 · probed live while planning TASK-043
**Decision:** orqestra records the measured behaviour of skill-level `allowed-tools` and
`disallowed-tools`, because D-024 documented the fields from Claude Code's own docs and three
consequences follow that D-024 does not state.

**Why:** TASK-043's plan proposed giving `BUG.md`'s write path to a directly-invoked
`Write`-holding skill, and flagged that nobody knew whether that works. It was probed in the main
session rather than reasoned about. Four results:

| probe | result |
|---|---|
| Invoke `orqestra:status` (`disallowed-tools: Write, Edit, NotebookEdit`), then `Write` | **`Write` removed.** Error: *"disabled for this session, in subagents as well as here"* |
| Then **dispatch a subagent** whose persona declares `tools: … Write, Edit …` and have it try `Write` | **removed there too**, and `Edit` with it. `Bash` survives |
| Then invoke `orqestra:create-task` (`allowed-tools: … Write …`), then `Write` | **still removed.** `allowed-tools` does not restore |
| Then write a file with a **`Bash` heredoc** | **succeeds** |
| `create-task` also declares `disallowed-tools: Agent` | `Agent` removed the same way |

**Three consequences, none of them in D-024.**

**1. The removal reaches subagents, and overrides their persona's `tools:`.** Not read off the error
string — dispatched and measured. `agents/agentic-engineer.md` declares `Write` and `Edit`; a subagent
dispatched under a `status`-restricted parent held **neither**, while `Bash` survived. So D-024's
"`agents/*.md` `tools:` is a true allowlist for the whole subagent run" is a **ceiling, not a floor**:
the persona cannot grant what the caller removed. So an orchestrator that
invokes a `Write`-denying skill cannot dispatch an agent that writes, for the rest of the turn —
and `skills/task/SKILL.md` rule 2 *requires* calling `orqestra:status`. Every `/orqestra:task` run
invokes it at preflight and then dispatches `implement`, which must write `IMPLEMENTATION.md`. The
pipeline has not broken on this because a human message falls between every step and clears the
restriction; an unattended run is a different matter.

**2. `allowed-tools` cannot undo `disallowed-tools`.** D-024 says `allowed-tools` "never
restricts"; it also never *grants*. So the shape TASK-043's plan proposed — an orchestrator that
denies `Write` invoking a skill that allows it — **cannot work**. `greenfield` has the same shape:
it denies `Write` and invokes `clarify`, `create-tasks` and `create-task`, all of which must write.

**3. `Bash` routes around the whole mechanism.** §4.4.5 cites an orchestrator's lack of `Write` as
the guarantee that no orchestrator patches an artifact. `bugfix` and `task` both hold `Bash`. The
guarantee is not weak, as D-024 concluded — for any orchestrator holding `Bash` it is **absent**.

**Constrains:**

- Never rely on a skill's `allowed-tools` to obtain a tool an earlier skill removed. It does not
  grant; only the user's next message restores the pool.
- A step that must write is **dispatched**, never invoked, when its caller denies `Write`.
  `agents/*.md` `tools:` is a true allowlist for the subagent run (D-024) — but see the first
  consequence: the caller's removal reaches the subagent too, so the caller must not have denied it.
- Never state that removing `Write` prevents an orchestrator from writing while that orchestrator
  holds `Bash`. Say what the layer actually holds (§7.0.1), or remove `Bash` and mean it.
- Any claim about tool behaviour in this project is probed before it is written down. D-024 was
  correct and incomplete because it was read rather than run; this decision exists because
  TASK-043's plan refused to guess.
