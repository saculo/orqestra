# Step — Intake

Capture the bug. `work/BUG-NNN/BUG.md`, id `max(existing) + 1` (D8).

## Gather

From arguments, or interactively via `AskUserQuestion`:

- **What happens**, in the reporter's words — do not translate it into a theory yet
- **Steps to reproduce**, exactly as given
- **Expected vs actual**
- **Severity** — `blocker` | `major` | `minor`
- **Which module** — established here, by the procedure below. Never optional, and never left to
  whatever the reporter happens to know (D-029)

## Establish the module

`module:` is the BUG's routing key: every later step reads it, and `MODULE` `PATHS` `STACK`
`EXPERTISE` on the diagnose dispatch all resolve from its `modules.md` row. A bug whose module is
unknown is not creatable (D-029), so intake settles it **before** it writes anything.

1. **Ask as a closed choice, never free text.** Present the `module` column of
   `.orqestra/modules.md`'s `## Modules` table as the options, each shown with that row's `paths`
   so the reporter recognises their own surface. A visible registry answers most "I don't know"s.
2. **If the reporter still cannot choose, derive a candidate.** Match the concrete surface already
   in the report — failing test path, stack frame, file path, the command that was run — against
   the `paths` column.
3. **Offer a derived candidate back; never write it silently.** Exactly one row matched → ask
   again with that row pre-selected, saying what it matched on. Zero or several matched → ask again
   over the candidate rows, or the whole registry when none matched, saying what was tried.
4. **Re-ask; do not block.** Repeat steps 1–3 until an answer exists. **No branch of this step ends
   in `blocked`** — a human is present at intake by construction, and `BUG.md` is the only artifact
   intake produces, so a `blocked_reason` would have no file to live in and §4.4.3's closed list has
   no value that fits an incomplete input (D11, D7). If the human abandons the question, the
   workflow ends having written **nothing** and says so.
5. **Never write `module:` empty, and never fall back to `## Scope` prose** (D-029). An empty value
   passes `check-templates.py`; this instruction is the only thing that catches it.

## Write

`${CLAUDE_PLUGIN_ROOT}/templates/BUG.md`, copied literally (D16).

`module:` carries the row established above. **`## Scope` records who and what is affected and does
not name the module** — the fact lives in the frontmatter and only there (D-029).

Record the report **as reported**. If the reporter's description is wrong about the cause — it often is —
that is for diagnosis to establish with evidence, not for intake to correct. A rewritten report loses the
symptom that was actually observed.

## Report

```
✓ BUG-003 recorded · major · module: api

→ reproducing
```
