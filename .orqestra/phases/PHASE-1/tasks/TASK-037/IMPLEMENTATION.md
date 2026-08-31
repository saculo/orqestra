---
id: TASK-037
type: implementation
status: done
updated: 2026-08-31
task: TASK-037
deviation: none
files_changed: 2
---

## Changes

**Component 1 — §4.8.1's `BUG.md` row (AC-1).** `REQUIREMENTS.md:584`, third cell, now reads
`` `module` `bug` `severity` ``. `module` leads, mirroring the `TASK.md` row where `module` precedes
`origin`/`bug`; the tokens are inline code, which is what `check-templates.py::parse_catalogue` reads
(`` re.findall(r"`([a-z_]+)\??`", cells[2]) ``). The `Written by` cell is untouched — correct under
D-028. **`module?` was not written**: the optional marker is consulted only by `check_instance`, so it
would not soften the default-mode check by one line, and it would misdescribe a key that is required
rather than conditional (D-029).

**Component 2 — `decisions/INDEX.md` (AC-2).** The D-029 row was appended and the frontmatter moved to
`count: 29`, `next_id: 30`. `D-029` itself was written at the design step (§4.7 names `design` among the
decision writers); this closes the index that `check-decisions.py` had been failing on since.
`.orqestra/` belongs to no module — the same precedent as `config.md` in TASK-030. The structural gap is
TASK-041's; this closes the instance, not the class.

**Component 3 — the four-surface consistency pass (AC-3), read end to end as one workflow, not grepped.**

| surface | after the amendment |
|---|---|
| §4.8.1:584 | amended. `BUG.md` declares `module` |
| §5.5:957 | **holds unedited.** "those units carry `module:` in their frontmatter" is now true of `BUG` as it was of `TASK`; the warrant no longer outruns the schema. Softening it would undo the fix |
| §5.1.1:795 | **holds unedited.** "a `BUG` carries `module:` too, so §5.5's conditional class is mandatory there as well" — the lookup it describes is now backed by a key |
| §7.3:1210 | **reconciled**, the one stale clause. Promote took the "module from the touched area"; it now takes the module **carried from `BUG-NNN`'s frontmatter**. Nothing else in §7.3 changed |
| §7.3.1:1221 | **holds unedited.** "routing comes from *where the fix lands*" stays the rule — the bug's `module:` *is* where the fix lands, and D-029 says diagnosis amends the frontmatter rather than composing a `MODULE:` that disagrees with it. The yaml block already shows `module:` on the promoted task |

**AC-4, both axes, including the empty ones.** (i) Search over `REQUIREMENTS.md` for every surface form,
because the phrasing was never identical twice: `` carr* `module:` `` → three hits (739, 795, 957), all
true after the change; `carries no` / `carry no` → the §5.5 `PHASE`/`PROJECT` clause only, still correct
(D-027); `if known` → **zero hits** in `docs`, it lives in `skills/bugfix/step-intake.md`, TASK-040's;
`BUG` co-occurring with `module` → 584, 794-795, 957, no fourth site. §5.1:739 ("Every **task** carries
`module:`") is the set-difference baseline and stays correct — it is not an exhaustive enumeration and a
bug carrying the key does not falsify it. `README.md` is in `PATHS` but **does not exist** in the repo,
so it has nothing to sweep. (ii) Set-difference of §4.8.1's frontmatter cells against `templates/*.md`
*is* `check-templates.py`'s output: exactly one delta, `BUG.md — frontmatter missing: module`, the
expected one. No other delta, so no live AC-4 finding.

**Verification.**

| command | exit | result |
|---|---|---|
| `python3 scripts/check-decisions.py` | **0** | 29 decisions conform. Was red before this change ("no row for D-029"); this is what fixed it |
| `python3 scripts/check-templates.py` | **1** | **Expected, and correct.** Exactly one finding — `BUG.md — frontmatter missing: module` — and nothing else |
| `python3 scripts/test-check-envelopes.py` | 0 | 25 obligation cases |
| `python3 scripts/check-envelopes.py` | **0** | 10 envelopes conform. Run **directly**, because `config.md`'s `test_command` chains with `&&` and short-circuits at the templates red |
| `python3 scripts/check-step-refs.py` | 0 | 42 step references resolve |

Re-run after the rework edit, each **directly**: `check-decisions.py` **0** (29 decisions),
`check-envelopes.py` **0** (10 envelopes), `check-step-refs.py` **0** (42 references),
`check-templates.py` **1** — still **exactly one** non-conforming template and **exactly one** finding
line, `BUG.md — frontmatter missing: module`. Nothing new hides behind it. Only `REQUIREMENTS.md` was
touched in this attempt (`git diff --stat`: 1 file, +10 −7).

**Rework, attempt 1 — QA Issue 1, the one defect behind AC-3 and AC-4.** `REQUIREMENTS.md:930` was the
only sentence in the specification saying where the envelope's `MODULE` value comes from, and it named
the task alone (*"`MODULE` is the task's `module:`"*) while §5.5:957 obliges `MODULE` under `BUG` too
and D-029 has `step-diagnose` read `BUG-NNN`'s frontmatter. A `BUG` dispatch is composed **before**
promote, so under :930 as written a conformant `BUG` envelope's `MODULE` had no defined source. It now
reads *"`MODULE` is the **scope unit's** `module:` — the task's under `TASK:`, the bug's under `BUG:` —
the single key that resolved `ROLE`, `STACK`, `EXPERTISE`, and `PATHS` from one `modules.md` row"*, with
a following clause keeping what the sentence was communicating and extending it: the value is **read
from the unit's frontmatter, never derived by the dispatching agent** — a `BUG` dispatch has no task to
read from, and `step-diagnose` takes `BUG-NNN/BUG.md`'s own `module:` (§7.3, D-029). `§5.1.1` was added
to the citation list beside `§5.1`, D-004, because :795 is the clause that says the lookup is identical
for a `BUG`. The paragraph was re-wrapped to the file's column width; nothing else in it changed. AC-1
and AC-2's edits (§4.8.1:584, `decisions/INDEX.md`) were **not** touched, and §5.5:957, §5.1.1:795 and
§7.3:1210 still stand as recorded above.

**The second sweep, run with terms chosen not to assume the first sweep's phrasing** — the first used
`` carr* `module:` ``, which anchors on one surface form and could not reach :930, because :930 says
"carry the **row**". Nil results are listed, so a reader can tell a search from an assumption.

| searched in `REQUIREMENTS.md` | returned |
|---|---|
| `` `MODULE` `` (the envelope field itself, not the frontmatter key) | **2** — 930 (fixed) and 957 (the obligation table). No third site. This is the search that would have caught it first time |
| `` the task's ``, `` from the task `` | 6 — 673, 805, 1489 are the review/PR module-boundary rule (a *task's* diff, correct as written); 1270, 1389 are routing-table prose about task-pipeline steps; 931 is the amended clause |
| `` `PATHS` `` | 4 — 930, 932, 935 (this paragraph) and 957. `PATHS` is sourced by the same sentence as `MODULE` and is now covered by the same fix |
| `modules.md row`, `routing row`, `the row` | 9 — 553, 753-755, 767, 836, 897, 949 are §5.1/§5.3/§5.5 prose about the row naming the agent; none states a *source* for `MODULE` |
| `re-deriv`, `infer` (case-insensitive) | **5, none about a module** — 60, 283, 1560, 2057 are about artifact shape and stage derivation; 1172 is resumability. Nothing re-derives a module in the spec; that behaviour lives in `skills/`, TASK-040's |
| `touched`, `symptom` | **zero hits.** §7.3:1210's "module from the touched area" was already removed by the AC-3 edit; nothing reintroduced it |
| every `module` line co-occurring with `bug`/`scope unit`/`unknown`/`prose`/`establish` | 574, 584, 794-795, 931, 935, 957, 1224 — the catalogue rows, §5.1.1's identical-lookup clause, the amended sentence, the obligation table, and §7.3.1's "where the fix lands". All seven agree after the change |

§5.5's prose was **read end to end, lines 900-975, not grepped** — the envelope field paragraphs, the
scope field paragraph, the obligation table and the closed-list rule. That read is what confirms :930
and :957 are now the same rule stated once each rather than two rules that disagree.

**The templates red is expected and its closing task is TASK-040**, which carries `module` into
`templates/BUG.md` and `skills/bugfix/step-intake.md` — both `plugin`, both outside this module's
`paths` (§5.2, D2, D14). A schema change is three edits always together (D-003), the three span two
modules, and docs leads (D-019); the window is one merge and it is symmetric — leading with `plugin`
would fail the same check from the other side with `frontmatter not in catalogue: module`. Per TASK-030,
a red check whose cause is recorded beats one made green by fabrication. No skip-list, no exemption
marker, no `module?`.

## Deviations

| deviation | from design | what | why |
|---|---|---|---|
| _none_ | — | — | — |

## Tech Debt

- **`scripts/test-check-templates.py` exits 1, 3 of 15 cases — recorded here because it was recorded
  nowhere until qa ran it.** All three assert against the real repository tree and quote the same
  `BUG.md — frontmatter missing: module` output, so all three are the **one expected window** and all
  three self-close the moment `templates/BUG.md` gains the key. It is not a second failure hiding behind
  the familiar one. It is absent from `config.md`'s `test_command`, which is why no one had run it —
  `plugin`, outside this module's `paths` (§5.2, D2), so **not fixed here**. **TASK-040** closes it
  alongside `check-templates.py`; its AC-1 currently names only the checker and should name this test
  too, so the window is described completely rather than partially.
- **`.orqestra/config.md`'s `test_command` comment is stale** — it describes a window **TASK-034**
  already closed. `plugin`, outside this module's `paths`, so **not fixed here**. Folded into
  **TASK-040 as AC-5**; recorded so the record does not depend on that fold surviving.
- **`.orqestra/config.md:34-36` is now stale**, and it is not this task's to fix (out of `docs`'s
  `paths`, TASK.md Out of Scope). It says `check-envelopes.py` "exits 1 today, on
  `skills/bugfix/step-diagnose.md` alone… red BY DESIGN"; run directly it now exits **0**, so that note
  outlived its cause. The design's regression row repeated the same stale claim. Nothing regressed —
  this task moved neither the checker nor the envelope — but the note will mislead the next reader who
  trusts it instead of running the command. Whoever next edits `config.md` (a `plugin` change) should
  drop it and leave the templates red, with TASK-040 named, in its place.
