---
id: TASK-033
type: qa
status: done
updated: 2026-08-30
task: TASK-033
result: failed
test_command: python3 scripts/check-templates.py && python3 scripts/check-decisions.py && python3 scripts/check-step-refs.py && python3 scripts/check-envelopes.py
---

## Test Strategy

There is no behaviour to execute — one commit, `f696c21`, `REQUIREMENTS.md` only. Verification is
therefore two things: the four repo checks as a regression baseline, and an **independent sweep of the
merged file** for the amendment's actual risk, which is a site the amendment silently falsified.

Test code was **not** written. The natural regression check for AC-4 is a `scripts/check-*.py`, and
`scripts/` is the `plugin` module — outside this task's `PATHS` (D14, D2). Stated rather than skipped.

**The sweep, and why these terms.** The engineer's own greps were anchored on the two forms already
known to be wrong: `bugfix. diagnose` and `\b[0-9]+ skills\b`. Both are list-based — they find sites
resembling the ones the plan already listed. A partial amendment survives exactly the greps derived
from the list, so I searched by *defect class* instead, on the merged file:

| what I searched | why that shape, not a list |
|---|---|
| `([0-9]+\|one…twelve\|twenty-*)[^.]{0,40}skills?\b` | a count is a **quantity near the noun**, in any notation. A digit-anchored grep cannot see `Twenty-two skills`. **This is what found F1.** |
| set-difference: every backticked token in §7.0's class table, and every token in §7.12's grid, against `ls skills/` | an **enumeration** asserts a count without writing one. No substring grep can catch a missing row; only comparing the list to the tree can. **This is what found F2 and F3.** |
| `names? no skill\|without a skill\|not a skill\|has none\|lacks\|omits.{0,15}SKILL\|last envelope\|cannot pass\|there is no` | the absence claim stated as prose rather than as a table cell. Returned 10 hits, all unrelated senses (`no state.json`, `no commands/ directory`, §9:2063 `No skill edits a done artifact`). Clean. |
| `grep -in diagnos` — all 15 hits read individually | confirms no *surviving* workflow-plus-step description and no second spelling |
| `grep -E '^#{1,6} '` diffed against `master`, and again on the numeric prefixes alone | AC-3's renumbering half, diffed rather than eyeballed |
| `grep -rn '^ROLE:' skills/bugfix/` | D-028's own discriminator, run against the tree rather than quoted |

`§1.3:69 "nit has 21 skills"` — **read, not assumed**. The line is `nit has 21 skills, 8 archetypes, a
Bun supervisor state machine, 26 JSON schemas…`; the subject is nit, a different frozen project, which
orqestra adding a skill does not falsify. Correctly kept.

## Results

| check | exit | note |
|---|---|---|
| `check-templates.py` | 0 | 21 templates conform |
| `check-decisions.py` | 0 | 28 decisions conform, D-028 included |
| `check-step-refs.py` | 0 | 40 step references resolve |
| `check-envelopes.py` | **1** | sole failure `skills/bugfix/step-diagnose.md:8 [diagnose] missing SKILL`. **Expected** — TASK-034's, per Out of Scope. `config.md`'s `test_command` exits 1 for this reason and this reason only |

Heading diff vs `master`: **identical**, 108 headings, text and order and numeric prefixes. Tree state:
`ls skills/` = 22 (`init` present, `diagnose` absent). Working tree carries only `REQUIREMENTS.md`
modified plus two pre-existing untracked `ORQESTRA_*.md`; nothing committed by me.

Three sweeps returned defects. Two of them are the failure mode this task was named as most at risk
of, and both live in **§7.0** — a section no artifact in the chain (plan, design, implementation)
mentions once.

## Criteria Coverage

| criterion | covered by | result |
|---|---|---|
| AC-1 | §4.8.1:585 reads `` \| `DIAGNOSIS.md` \| `diagnose` \| `` — one backticked token, the shape `plan`/`design`/`qa`/`review-task` use. `grep 'bugfix. diagnose'` returns nothing. §4.8.1:584's `` \| `BUG.md` \| `bugfix` intake \| `` **diffed byte-identical against `master`** — the adjacent-row slip did not happen. Truthful under D-028: `grep -rn '^ROLE:' skills/bugfix/` returns exactly one hit, `step-diagnose.md:8`, so `intake`/`reproduce`/`promote`/`handoff` dispatch nobody. I also applied D-028 to the column's other two workflow-plus-step cells — `push` and `pr-comments` — and neither `skills/task/step-push.md` nor `skills/pr-comments/` carries a `ROLE:`, so the amendment introduces no new contradiction there | **pass** |
| AC-2 | §5.1.1:786 `` \| diagnose \| `diagnose` \| `analyst` \| module's \| ``. The name is `diagnose` in all three amended sites and nowhere spelled otherwise — `grep -in diagnos` shows no `bugfix-diagnose`, no `root-cause`, no second variant. §5.1.1 is the single authoritative place; §4.8.1 and §7.7 restate it identically. The namespaced form is unambiguously derivable: §5.5:903 says `SKILL` is "namespaced like any other" and gives `STEP: review` → `SKILL: orqestra:review-task` (§5.1.1) as the worked example, so `orqestra:diagnose` is the only spelling TASK-034 can author. `analyst` matches `step-diagnose.md:8`'s `ROLE: orqestra:analyst` (D-014) | **pass** |
| AC-3 | Renumbering half **passes** (heading diff identical, above). "Every site agrees" half **fails** — §7.0's class table still enumerates 22 skills and `diagnose` is not among them. See F2. §7.3:1209 confirmed already true (names the step *file*) | **fail** |
| AC-4 | `grep -E '\b[0-9]+ skills\b'` returns only §1.3:69's nit fact — but the count survives in words at §7.0:1072. See F1 | **fail** |

## Issues

**F1 — AC-4: a hard-coded orqestra skill count survives, spelled as a number word.**

- **Where**: `REQUIREMENTS.md:1072`, §7.0 Skill anatomy, first line of the section.
- **Observed**: `Twenty-two skills have to be written consistently, by different hands, months apart.`
- **Expected**: no assertion of a count. AC-4 states the general rule — *"A number that every new skill
  invalidates is a defect, not a fact"* — and the engineer applied it correctly to §1.3:69, a site the
  design had also missed. The same reading reaches this one. TASK-034 makes the number 23.
- **Why it was missed**: every grep in the chain was digit-anchored. A number word is invisible to
  `\b[0-9]+ skills\b`, which is the whole reason a class-based sweep is not optional here.
- **Note**: §7.12's new closing line promises `No count is written here or in §2` — scoped to two
  sections, so it is not *literally* falsified by §7.0. The count is a defect on AC-4's own terms
  regardless, and a reader who takes §7.12's sentence as the document's policy is contradicted 590
  lines earlier.

**F2 — AC-3: §7.0's class table omits `diagnose`, and now contradicts three amended sites.**

- **Where**: `REQUIREMENTS.md:1076–1085`, the `Class · Skills · allowed-tools · disallowed-tools`
  table, introduced by `Every skill declares a class first, and the class fixes everything else`.
- **Observed**: the `Skills` column enumerates exactly 22 backticked skill names — 5 orchestrator,
  5 planning, 2 step, 2 step+build, 2 step+review, 1 query, 1 setup, 4 control — set-equal to
  `ls skills/`. `diagnose` appears nowhere in the section (`grep -c diagnose` over :1076–1086 = 0).
- **Expected**: `diagnose` carries a class, as every skill must. It is an exhaustive enumeration, so
  omitting the new skill is still an assertion that the step has none — the precise thing AC-3 widened
  to cover, and a form no substring grep can detect.
- **Contradicts, as merged**: §5.1.1:786 (routing row), §7.7:1463 (step-skills row), §7.12:1657 (grid).
  A `diagnose` that is a dispatched, template-writing step skill in three tables and absent from the
  fourth is a partial amendment.
- **Downstream cost — this is the SKILL-name risk repeating one column over**: TASK-034's AC-1 requires
  `skills/diagnose/SKILL.md` at the same altitude as `plan` and `qa`, and §7.0 obliges it to *declare a
  class first*. The spec sanctions no class for `diagnose`, so TASK-034 must either invent one — which
  is `plugin` inventing a `docs` fact, against D-019 — or block. Choosing between `step` (as `plan`,
  `design`) and `step+build` (as `qa`, if diagnosis needs `Bash` to investigate) is a specification
  decision and belongs in this commit.

**F3 — regression: §7.12's replacement sentence asserts a completeness that is false.**

- **Where**: `REQUIREMENTS.md:1659–1660`.
- **Observed**: `This grid is the whole inventory. The folder name is the invocation name (§2), so it
  is also the command list.` The grid does not contain `init`. Set-difference of grid tokens against
  `ls skills/`: grid-only `diagnose` (correct — the spec leads), tree-only **`init`**.
- **Expected**: either the grid lists `init`, or the sentence does not claim completeness. `init` is a
  skill and a command — §2:120 shows `skills/init/SKILL.md  #   → /orqestra:init`, and §7.0:1084 gives
  it its own `setup` class — so "the whole inventory" and "the command list" are both untrue as
  written.
- **Attribution, honestly**: the omission of `init` pre-dates this commit. What this commit did was
  replace a bare number with an **explicit** assertion of completeness, converting a stale count into a
  false claim, in the one section whose job is to be the inventory. Its own new text — `which is how
  this line came to say 22 twice, 1500 lines apart, while the tree said otherwise` — names the
  discrepancy and then does not resolve it. Lower severity than F1 and F2; fixing it is one token in
  the grid's `UTILITY` or a new `SETUP` cell.

**Not defects, checked and confirmed:**

- `check-envelopes.py` exit 1 on `step-diagnose.md` — TASK-034's, and the reason this task exists.
- §4.8.1:584 `` `bugfix` intake `` — byte-identical, and truthful under D-028.
- §1.3:69 `nit has 21 skills` — a fact about nit, correctly retained.
- §7.3:1209 `step-diagnose.md` — names a step file, already agrees, correctly untouched.
- `templates/config.md` having no `diagnose` row — the design's reading, `plugin` module either way.
