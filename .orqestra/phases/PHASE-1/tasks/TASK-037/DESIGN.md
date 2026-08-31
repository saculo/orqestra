---
id: TASK-037
type: design
status: done
updated: 2026-08-31
task: TASK-037
decisions: [D-029]
---

## Components

Three, and the third is the one that makes this a design rather than a table cell.

| # | component | responsibility | serves |
|---|---|---|---|
| 1 | **The amended `BUG.md` catalogue row** (§4.8.1) | Declares `module` a frontmatter key of a bug, making §5.5:957 and §5.1.1:795 true statements rather than assertions with no schema behind them | AC-1 |
| 2 | **`D-029`** — a bug carries its module | Records *that* and *why* a bug's module is a frontmatter key, and what it binds — the artifact TASK-040 builds against | AC-2 |
| 3 | **The consistency pass across the four surfaces** | Reads §4.8.1 → §5.5:957 → §5.1.1:795 → §7.3/§7.3.1 as one workflow and reconciles the one line the amendment leaves stale (§7.3:1210, promote deriving the module "from the touched area"); then sweeps for any fifth site | AC-3, AC-4 |

Written already, at this step: `D-029` exists at `.orqestra/decisions/D-029-a-bug-carries-its-module.md`
(§4.7 names `design` among its writers). Component 2 is therefore not "write the decision" but **carry it
into `decisions/INDEX.md`** — which §4.7 says is regenerated from the files, not hand-edited, and must end
at `count: 29`, `next_id: 30`.

Not a component, deliberately: `templates/BUG.md`, `skills/bugfix/step-intake.md`,
`scripts/check-envelopes.py`, `.orqestra/config.md`. All outside `docs`'s `paths`; the first two are
TASK-040's, the last two need no edit at all (TASK.md Out of Scope).

## Interfaces

**The §4.8.1 row is a machine-read contract, not prose.** `scripts/check-templates.py::parse_catalogue`
tokenises the *Frontmatter additions* cell with `` re.findall(r"`([a-z_]+)\??`", cells[2]) `` — a key is
seen only if it is written as an inline-code token. The amended cell is:

```
| `BUG.md` | `bugfix` intake | `module` `bug` `severity` | ## Report · ## Reproduction · ## Expected vs Actual · ## Scope |
```

`module` first, mirroring `TASK.md`'s row where `module` precedes `origin`/`bug`. Order is not checked by
the script; it is checked by readers, and the two rows should read alike. The `Written by` cell is
untouched — it is correct under D-028 (`step-intake.md` contains no `ROLE:` envelope, which is D-028's own
test), and this task does not touch that column.

**`module?` is not an option.** In default mode `main()` compares `row["frontmatter"]` — which is
`COMMON + extra`, and `extra` includes optional keys — against the template's keys with no exemption
(`missing = [k for k in row["frontmatter"] if k not in fm_keys]`). `row["optional"]` is consulted only by
`check_instance`. So writing `module?` would not soften the check by one line, and it would misdescribe
the schema: a bug's module is not conditional on anything (D-029).

**The obligation TASK-040 builds against** is `D-029`'s `**Constrains:**`, not this design. It fixes four
things: the key is required and intake establishes it; `## Scope` stops carrying the module; diagnose and
promote *read* the key rather than re-deriving it; and the "does this unit carry `module:`?" test D-027
left open now has an answer. Nothing else about `templates/BUG.md` or `step-intake.md` is specified here.

**`REQUIREMENTS.md:957` and `:795` are read-only at this step.** Under resolution (a) both become true;
softening either would undo the fix. Likewise `D-027`: decision files are append-only (§4.7), its `Why`
becomes true with them, and `D-029` supersedes nothing.

## Structure

The change lands entirely in the `docs` module, in two surfaces of one specification:

- **The catalogue layer (§4.8).** The single source of truth for every artifact schema (D-003), and the
  only place a machine reads. Component 1 is one cell here.
- **The workflow narrative (§7.3).** Component 3's one reconciliation. §7.3:1210 today has promote taking
  the "module from the touched area"; once the BUG carries the key, the module is *carried forward* from
  the bug's frontmatter and confirmed against where the fix lands (§7.3.1 already states routing that
  way). This is an editorial reconciliation of one clause, not a rewrite of §7.3.

**Read but not written:** §5.5:957, §5.1.1:795, §5.1:739, §7.3.1's yaml block. Each is verified to hold
after the amendment and left alone. §5.1:739 ("Every **task** carries `module:`") is the set-difference
baseline for AC-4 and stays correct — it is not an exhaustive enumeration and is not falsified.

**No renumbering, no new subsection.** Every edit is inside an existing cell or clause; ~90 files cite by
number and §5.1.1 exists precisely because appending beats inserting.

**Nothing reaches out of `docs`.** `templates/`, `skills/`, `scripts/` and `.orqestra/config.md` are
`plugin` or unowned; a change there is TASK-040 or nothing (§5.2, D2, D14).

**Order.** The row first, because component 3 sweeps the amended text, not the old text. The index row for
`D-029` at any point. Nothing here depends on TASK-040, which is the whole reason the split works.

## Decisions

**Resolution (a), settled by human decision (§8.2) — make the specification true rather than soften it.**
The plan recommended (b) on a Rule B (§4.4.1) argument: a field whose only consumer is a check that does
not read it. That objection does not survive (a) as designed — the key's consumers are
`check-templates.py`, which proves it against §4.8.1, and `step-diagnose.md`, which after TASK-040 reads
it rather than re-deriving prose. §5.5:965's bar ("answered by something the orchestrator has already
read") is met more strongly by a frontmatter key than by a value the workflow re-derives at reproduce.
Recorded, with the reason and what it binds, as `D-029`.

**The convention this crosses, named.** `orqestra-conventions` makes a schema change **three edits always
together** — the §4.8 catalogue row, the `templates/` file, and the skill that writes it — because any one
alone leaves the schema broken (D-003). Here the three span two modules, and D14 forbids one task
touching both. The two rules cannot both be honoured. Chosen: **docs leads (D-019)**, TASK-040 follows,
and the schema is knowingly inconsistent for one merge window. Crossing D-003 is the cost; the alternative
is crossing D14, which would put a `plugin` edit in an `architect`'s hands with no `plugin` review.

**The window is symmetric, so the order was not chosen to dodge it.** Leading with `plugin` would fail the
same check from the other side — `frontmatter not in catalogue: module`. Either order is red for one
window; D-019 decided which.

**`python3 scripts/check-templates.py` goes RED at this merge, and that is the correct outcome.**
Verified against the script's actual behaviour, not predicted: default mode compares the catalogue's
frontmatter list against each template, `templates/BUG.md`'s keys are `id type status updated bug
severity`, so the amended row produces exactly one failure —

```
  BUG.md
      frontmatter missing: module
```

— and `main()` returns 1. Because `.orqestra/config.md`'s `test_command` chains with `&&`,
**`check-envelopes.py` will not run at all** during the window; its status is unchanged, but it must be
invoked directly to say so.

This red is left visible with its reason recorded, per TASK-030: a red check whose cause is written down
beats one made green by fabrication. No skip-list, no exemption marker, no `module?` — each of those would
be a lie in the schema that outlives the two days it bought. The reason is recorded here and in TASK-040's
Goal, which names the window explicitly. It is **not** recorded in `.orqestra/config.md` — that file is
outside `docs`'s `paths`, and its existing red-by-design note (lines 34-40) exists because that failure had
no closing task; this one has TASK-040, which depends on this task and closes it in the next merge.

**`D-027` is cited, not edited.** Its rule stands; its `Why` — `PHASE` and `PROJECT` omit the class
"because those units carry no `module:` in their frontmatter" — is true and stays true. `D-029` answers
the question D-027's `Constrains` left open rather than correcting anything (§4.7: append-only).

## Test Strategy

Markdown, so every criterion is proved by reading a stated place or running a stated command.

| criterion | proved by |
|---|---|
| AC-1 | §4.8.1's `BUG.md` row's third cell reads `` `module` `bug` `severity` ``. Then `python3 scripts/check-templates.py`: exit **1**, with **exactly one** failure — `BUG.md — frontmatter missing: module`. Any second failure is a regression this task introduced; a clean exit 0 means the row was not actually read (the token was not inline code) |
| AC-2 | `.orqestra/decisions/D-029-a-bug-carries-its-module.md` conforms to §4.8.1's decision row — `# D-NNN — <title>` then `**When**` `**Decision**` `**Why**` `**Constrains**` — and its `Constrains` names work TASK-040 can be checked against. `decisions/INDEX.md` carries the D-029 row with `count: 29`, `next_id: 30` |
| AC-3 | Read the four surfaces **as one workflow**, in order — §4.8.1's row → §5.5:957 → §5.1.1:795 → §7.3:1210 → §7.3.1 — and state per site whether it holds after the amendment. §5.5:957 and §5.1.1:795 must now read as true without edit; §7.3:1210 must no longer describe the module as first derived at promote. A pass recorded as "grepped, consistent" does not meet this criterion — the criterion says end to end, because this session has repeatedly shown a claim living in more places than the two obvious ones |
| AC-4 | Two axes, both required. **(i)** Search `REQUIREMENTS.md` and `README.md` for every surface form, not one: `` carries `module:` ``, `` carry no `module:` ``, `carries no`, `if known`, and `BUG` co-occurring with `module` — the phrasing that hid this contradiction was never identical twice. **(ii)** Set-difference §4.8.1's frontmatter cells against `templates/*.md` — which *is* `check-templates.py`'s output, so the red check doubles as AC-4's instrument: one expected delta (`BUG.md`, `module`), and any other delta is a live AC-4 finding. Record both axes' results, including the empty ones |
| regression | `python3 scripts/check-envelopes.py` run **directly**, since the `&&` chain short-circuits before it. Its result must be unchanged from HEAD (it exits 1 today on `skills/bugfix/step-diagnose.md`, per `config.md`) — this task must not move it in either direction |
