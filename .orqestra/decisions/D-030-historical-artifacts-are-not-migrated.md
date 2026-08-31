---
id: D-030
type: decision
status: active
updated: 2026-08-31
area: schemas
supersedes: —
superseded_by: —
---

# D-030 — Historical artifacts are not migrated to a later schema

**When:** 2026-08-31 · PHASE-1 · found by `check-templates.py --target .orqestra` reporting 19 failures
**Decision:** an artifact that conformed when it was written is not amended to satisfy a rule added
afterwards. `check-templates.py --target .orqestra` is a **diagnostic with known noise**, not a gate, and
the noise is the record of when each rule arrived.

**Why:** all 19 failures are one shape — an artifact judged by a rule that did not exist when it was
written:

| failing | count | rule arrived at |
|---|---|---|
| `TASK.md` missing `bug:` | 10, TASK-001…010 | `1ba7049` |
| `DESIGN.md` missing `## Structure` | 8 | `6ee08b5` |
| `TASK-001/REVIEW.md` missing `required`, `review_round`, `## What Would Change This Verdict` | 1 | D-022, §8.1 |

Backfilling them would mean writing a `## Structure` section for a design nobody designed that way, and
a `## What Would Change This Verdict` for a review nobody wrote. The artifact would conform and stop
being a record. **These files are evidence of what was decided and when** — that is the whole reason
they are committed rather than derived, and the value of the deep scan is smaller than the value of the
history it would overwrite.

**What this costs, stated rather than discovered later.** `--target .orqestra` has 19 standing failures,
so a twentieth would hide among them. That is the "second failure inside a familiar one" this phase has
already been bitten by three times — `config.md`'s stale comment, `test-check-templates.py`'s unrecorded
red, and the pre-existing `--target` drift itself. The cost is accepted because the scan is **not** in
`config.md`'s `test_command` and gates nothing; a red there stops no work. If it is ever wired in, this
decision has to be revisited first, not worked around.

**Constrains:**

- Never amend a committed artifact to satisfy a schema rule added after it was written. If a rule must
  reach backwards, that is a migration with its own task, its own review, and a reason recorded — not a
  quiet edit while passing.
- `--target .orqestra` may not be added to `config.md`'s `test_command` while this decision stands. Its
  19 known failures would make the suite permanently red, which is how a checker stops being read.
- A NEW artifact must conform. This decision exempts history, never present work: `check-templates.py`
  without `--target` gates the templates, and every task's own artifacts are checked at its contract
  check (§4.6).
- Anyone reading `--target .orqestra` output compares it against the 19 recorded here. A count that is
  not 19 means something changed and is worth reading — that is the only detection this decision leaves,
  and it is deliberately weak.
