# Step — Clarify

**Invoke `orqestra:clarify` directly. Never dispatch it as a subagent.**

It works through unknowns with the user one question at a time. A subagent between the human and their
own questions makes the conversation useless — the agent answers on their behalf, or relays badly.

## Skip when already done

`CLARIFICATIONS.md` exists with `open_count: 0` → skip. Re-asking answered questions is the fastest way
to make a workflow feel broken.

`open_count > 0` → re-invoke; it resumes on the open ones only.

## Invoke

```
Skill: orqestra:clarify
Args:  <prd-path>
```

## On return

Read `CLARIFICATIONS.md` frontmatter — `open_count`, `status`.

| Result | Do |
|---|---|
| `open_count: 0` | Commit, continue to phases |
| `open_count > 0` | Present them. Open questions do not block planning, but they will surface again at design — say so |
| `status: blocked` | Stop and report |

Not gated: the step is a conversation with the human throughout, so a gate at the end asks them to
approve what they just said.
