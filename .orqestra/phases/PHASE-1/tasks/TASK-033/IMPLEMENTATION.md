---
id: TASK-033
type: implementation
status: done
updated: 2026-08-30
task: TASK-033
deviation: minor
files_changed: 1
---

## Changes

`REQUIREMENTS.md` is the only file changed. `README.md` is in `PATHS` but does not exist in the
repository, so nothing there could assert a count. The design's six components landed as written,
plus a seventh site the first sweep found and three more the rework fixed.

### Original amendments (attempt 1, commit `f696c21`) — all still in place

| # | § / line | what it says now |
|---|---|---|
| C1 | §4.8.1:585 | `DIAGNOSIS.md`'s `Written by` cell is `` `diagnose` `` — one backticked token, the shape `plan`/`design`/`qa`/`review-task` use (AC-1) |
| C2 | §5.1.1:786 | routing row `\| diagnose \| \`diagnose\` \| \`analyst\` \| module's \|`, appended **after** `pr-comments` so the six rows above still read as the task pipeline in order (AC-2) |
| C3 | §5.1.1:788–796 | the fixed-role paragraph stops counting ("Every other row is a fixed role"), and a second paragraph says `diagnose` is the one row that is *not* a task-pipeline step, and why the module's expertise still reaches it |
| C4 | §7.7:1463 | step-skills row `\| \`diagnose\` \| \`BUG.md\`, \`PROJECT.md\` \| \`DIAGNOSIS.md\` \| \`templates/DIAGNOSIS.md\` \|`, plugin-relative per D-026 |
| C5 | §2:119 | tree comment is now `# one directory per skill — the folder name IS the invocation name`; the count went, the clause that carried the information stayed (AC-4) |
| C6 | §7.12:1657, 1660–1664 | `diagnose` joins the `STEP SKILLS` column of the grid; the closing line no longer opens with a number and states *why* no count is written (AC-3, AC-4) |
| C7 | §1.3:69–71 | the nit comparison no longer asserts orqestra's own skill count — a deviation from the design, recorded below and unchanged by this rework |

`§4.8.1`'s `` | `BUG.md` | `bugfix` intake | `` row is **byte-identical to `master`** (line 583 there,
584 here — the row's text `diff`s clean; only its line number moved). Truthful under D-028:
`grep -rn '^ROLE:' skills/bugfix/` returns exactly one hit, `step-diagnose.md:8`, so `intake`
dispatches nobody and has no skill to name.

### Rework (attempt 1 of 3) — the three items QA raised, and nothing else

| # | § / line | what changed | why |
|---|---|---|---|
| R1 · AC-4 | §7.0:1072 | `Twenty-two skills have to be written consistently` → `Every skill has to be written consistently`. The sentence keeps exactly what it communicated — many hands, months apart, hence a template — and stops asserting a quantity | The count spelled in words. Same defect as C5 and C7, same fix: keep the meaning, drop the number. TASK-034 makes it 23 |
| R2 · AC-3 | §7.0:1081 | the `step` class row is now `` `plan`, `design`, `diagnose` `` | **`step` is the class the step's own behaviour dictates.** `diagnose` is *dispatched to* the `analyst` subagent, so it never dispatches itself — that rules out `orchestrator`. It writes `DIAGNOSIS.md` from a template, so it needs `Write` — that rules out `query`. It amends no existing file, so it must not hold `Edit` — that rules out `step+build`, whose `Edit` exists for `implement` and `qa` writing code. It renders no verdict on someone else's work, which is what `step+review` names. What is left is exactly `plan` and `design`: read the repo, reason, write one artifact. `step`'s `disallowed-tools` includes `Bash`, and that is correct here — reproducing the bug is `step-reproduce.md`'s job, a different step, and diagnosis reasons over what reproduction already established |
| R3 · regression | §7.12:1657, 1655 | `init` added to the grid, in the column whose header becomes `UTILITY / SETUP` | **I made the grid complete rather than weakening the claim.** The claim is the more useful of the two: §7.12 exists to *be* the inventory, and "the folder name is the invocation name, so it is also the command list" is the sentence that makes the grid worth reading. Weakening it to "a selection of skills" would leave the section with no job. `init` is a real skill and a real command (§2:120, §7.0:1085 `setup`), so its absence was the bug, not the sentence. `UTILITY / SETUP` because `init` is `setup` class in §7.0 and the header now says so instead of quietly absorbing it |

**The sweep, run by defect class rather than by list.** The lesson of both failures is that a search
anchored on one surface form finds only that form. Every term below was run against the **working
tree** file, and the nil results are reported because a nil result is the evidence:

| shape searched | pattern | returned |
|---|---|---|
| count, digits | `\b(2[0-9]\|1[0-9]\|[0-9])\b[^.]{0,40}\bskills?\b` | 9 hits. §1.3:69 `nit has 21 skills` — **correctly kept**, a fact about a different, frozen project. §12:1820 `8 subagents` — a subagent count, unaffected by a new skill. §13:1922 `all 20 templates` — a *template* count, stale already and not a skill count (see Tech Debt). The other 6 are heading numbers (`### 7.0`, `### 5.3`) and `at most 10 lines` |
| count, number-words | `\b(one…twenty-nine\|thirty\|dozen)\b[^.]{0,40}\bskills?\b` | 11 hits, **all `one`** in its ordinary sense — "one review skill, many stances", "one directory per skill", "exactly one skill permitted to write it". No surviving quantity. **This shape is what QA used to find F1**, and it is now clean |
| quantifier near the noun | `\b(all\|every\|each\|the whole\|both\|none\|no)\b[^.]{0,25}\bskills?\b` and the mirror | 7 hits, all distributive rather than numeric — "every skill declares a class", "every skill cites these by number". `all 20 templates` again |
| completeness assertions | `whole inventory\|complete (list\|inventory\|set)\|exhaustive\|every skill\|the full (list\|set)\|entire (list\|inventory)\|all of them` | 7 hits. §7.12:1660 `whole inventory` — the R3 site, now true. §2:139 "exactly one copy of every skill, agent, and template" — about *file layout*, not membership. The rest are §7.0:1072/1075 and §9:2010, distributive |
| **enumerations**, not prose | set-difference: every skill-name token in the file against `ls skills/` + `diagnose`, line by line, flagging any line naming ≥3 | 34 candidate lines. Two are **exhaustive** and both now cover all 23: §7.0's class table (:1077–1086) and §7.12's grid (:1649–1658) — `missing: NONE` for each. §7.7's table (:1456–1463) is not exhaustive by construction (it lists step skills only) and already carries `diagnose` from C4. The remaining 31 are prose naming two or three skills as examples |

No substring grep can see a missing row, which is why the enumeration check is a set-difference
against the tree and not a pattern. It is the check that would have caught F2 and F3 the first time.

**Verification.** `git status`: `REQUIREMENTS.md` the only modified file (the two untracked
`ORQESTRA_*.md` pre-date this task). `git diff --stat`: 4 insertions, 4 deletions — line-neutral.
Headings `diff`ed against `master`: **identical**, text and order and numeric prefixes, so nothing is
renumbered (AC-3).

| script | exit | note |
|---|---|---|
| `check-templates.py` | 0 | 21 templates conform |
| `check-decisions.py` | 0 | 28 decisions conform |
| `check-step-refs.py` | 0 | 40 step references resolve |
| `check-envelopes.py` | **1** | **expected.** Sole failure is `skills/bugfix/step-diagnose.md:8 [diagnose] missing SKILL`. TASK-034's, per this task's Out of Scope |

Not committed (D1).

## Deviations

| deviation | from design | what | why |
|---|---|---|---|
| minor | design lists six components; §1.3:69–71 is in none of them | C7: §1.3's nit comparison said "orqestra has **22 skills**, no archetypes…". Rewrote to "a comparable number of skills and none of the rest", plus "The simplification is not a smaller skill count; it is the machinery underneath them." | The post-merge sweep returned it. AC-4's exact defect class — a hard-coded orqestra skill count TASK-034 falsifies. Kept from attempt 1, unchanged |
| minor | design lists six components; §7.0 is in none of them | R1 and R2: §7.0:1072's number-word count removed, and `diagnose` given the `step` class in §7.0's table | QA found both. §7.0 is a seventh site the design's five-site survey missed entirely — its class table is an exhaustive enumeration, so omitting `diagnose` asserted the step has no class, which is AC-3's defect in a form no substring grep sees. The class choice is derived in `## Changes` R2 from what the step does; it invents nothing, and it is what TASK-034 must declare in `skills/diagnose/SKILL.md` |
| minor | `init`'s absence from §7.12's grid pre-dates this task | R3: added `init`, and the column header now reads `UTILITY / SETUP` | Attempt 1 replaced a stale number with an explicit completeness claim, which converted a visible defect into an invisible one. Fixing the grid rather than retracting the claim, because §7.12's job *is* to be the inventory |

## Tech Debt

- **§13:1922 says "all 20 templates"** while `check-templates.py` reports 21. A template count, not a
  skill count, so outside AC-4 as written; the sentence is a historical argument about build ordering
  rather than a live reference. Same decay class as the skill counts this task removed, and worth the
  same treatment — noted, not fixed (D3).
- **`.orqestra/config.md`'s routing table still carries `from the module's task_type`** and a
  `task_type → subagent` table that D-011 removed. Pre-existing workspace state, outside `docs` (D3, D14).
- **`templates/config.md`'s routing table has no `diagnose` row.** The design answers that it needs
  none, because `step-diagnose.md` will carry `SKILL: orqestra:diagnose` literally and no lookup
  occurs. If that reading is wrong, `check-envelopes.py` surfaces it in TASK-034. `plugin` module either way.
- **§7.7's table has no stated inclusion rule.** `diagnose` was added on the design's reading — *step
  skills that write an artifact from a template*. If the intended rule is *steps of the delivery
  pipeline*, `review-phase` above it does not belong either. Pre-existing ambiguity; not resolved here.
