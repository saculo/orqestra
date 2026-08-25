---
id: TASK-009
type: plan
status: done
updated: 2026-08-25
task: TASK-009
---

## Approach

The convention is emitted in exactly five places, and only one of them is a real decision — what
prefix a commit uses when **no task owns it**.

Everything else follows once that rule exists: three skills already defer to `config.md`'s
`commit_style` rather than hard-coding a format, so changing the setting and its documented meaning
carries them. Only `init` hard-codes its message inline.

## Affected Areas

Verified by grepping `skills/` and `templates/` for commit formats and `commit_style`:

| file | what it does today |
|---|---|
| `templates/config.md` | `commit_style: conventional` — the single declaration |
| `skills/init/SKILL.md` | hard-codes `chore(orqestra): initialize workspace` |
| `skills/task/step-push.md` | defers to `commit_style` |
| `skills/pr-comments/SKILL.md`, `step-reply.md` | defer to `commit_style` |

Artifact commits (§4.6) are made by the orchestrators, which cite the convention rather than restating
it — so they need no change if the convention itself is stated in one place.

## Risks

- **`commit_style: conventional` is a value with no defined meaning in this repo.** Nothing says what
  "conventional" expands to; three skills defer to a setting whose semantics live only in the reader's
  head. Replacing the value is an opportunity to fix that, and leaving it vague would reproduce the
  defect under a new name.
- **The taskless case is the whole difficulty.** `init` runs before any phase exists; `create-phases`
  runs before any task exists. A rule that only covers task commits leaves the two most common early
  commits undefined.

## Open Questions

_none_ — the taskless rule is settled in `DESIGN.md` rather than deferred, since AC-3 requires it
stated rather than left to judgement.
