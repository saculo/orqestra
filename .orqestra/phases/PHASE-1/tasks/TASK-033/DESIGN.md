---
id: TASK-033
type: design
status: awaiting-approval
updated: 2026-08-30
task: TASK-033
decisions: [D-028]
---

## Components

Six amendments to `REQUIREMENTS.md`, all in one commit. Two of them (C1, C2) are the criteria; the
other four exist because a statement elsewhere in the same document becomes false the moment C1 and
C2 land. **This is not a §4.8 schema change** — `DIAGNOSIS.md` keeps its frontmatter keys and its four
headings, `templates/DIAGNOSIS.md` is untouched, and no skill changes shape. D-003's three-edits rule
does not apply; the §4.8.1 column being corrected says *who writes* the artifact, not what it is.

| # | component | responsibility | serves |
|---|---|---|---|
| C1 | §4.8.1 `DIAGNOSIS.md` writer cell | names the skill `` `diagnose` `` bare, in the form `plan`/`design`/`qa`/`review-task` use | AC-1, AC-3 |
| C2 | §5.1.1 routing table `diagnose` row | resolving step `diagnose` yields a skill, a subagent, and an expertise source | AC-2, AC-3 |
| C3 | §5.1.1 fixed-role paragraph (:786) | the sentence that counts the fixed-role rows and explains why, restated so a seventh row does not falsify it and so a reader is not told `diagnose` is a task-pipeline step | AC-3 |
| C4 | §7.7 step-skills table `diagnose` row | the reads/writes/template row every dispatched artifact-writing step has | AC-3 |
| C5 | §2 repo-tree comment (:118) | states what the `skills/` line is there to state — the folder name is the invocation name — without a count | AC-4 |
| C6 | §7.12 inventory grid and its closing line | `diagnose` appears under `STEP SKILLS`; the closing line asserts completeness and the command-list identity, not a number | AC-3, AC-4 |

**Deliberately absent, and each absence is a decision, not an oversight:**

- **§4.8.1:583 (`BUG.md` | `` `bugfix` intake ``) is not touched.** It has C1's shape and is truthful:
  `grep ROLE: skills/bugfix/` returns exactly one hit, `step-diagnose.md`. `intake`, `reproduce`,
  `promote` and `handoff` dispatch nobody, so §5.5 never reaches them and there is no skill to name.
  D-028 states the discriminator so this row is protected from a later "consistency" fix.
- **§7.3:1196–1206 is not touched.** It names step *files*, and `step-diagnose.md → DIAGNOSIS.md
  [GATE: diagnosis]` is already true. AC-3 asks that every site *agree*; this one does. Editing it to
  name a skill would make it the only walkthrough of six that mixes files and skills.
- **`templates/config.md` and `.orqestra/config.md` are not touched** — `plugin` and workspace state
  respectively, outside `docs` (D14, D-010). Q1 is answered: no `diagnose` row is needed there.
- **No new subsection.** §5.1.1's existing table admits `diagnose` without strain. A §5.1.2 holding one
  row would split one rule across two places.
- **Nothing is renumbered** (AC-3). Every edit is a row appended to an existing table, a cell rewritten
  in place, or a sentence rewritten in place. No heading moves.

## Interfaces

**The skill's name is `diagnose`, invoked as `orqestra:diagnose`. `REQUIREMENTS.md` is where that is
authoritative** — C1's cell and C2's row are the sanction, and TASK-034 authors `skills/diagnose/`
against them, because under D-012 the folder name *is* the invocation name. TASK-034's AC-3 reaches
exit 0 only if `skills/bugfix/step-diagnose.md` gains exactly `SKILL: orqestra:diagnose`. No other
spelling is sanctioned by this design, here or anywhere.

§5.5's always-class row is satisfiable by that value the moment the skill exists: `SKILL` is
unconditional (§5.5:947), and `step-diagnose.md` already supplies `ROLE` `STEP` `BUG` `MODULE` `PATHS`
`STACK` `EXPERTISE` `READ` `TEMPLATE` `WRITE` `RETURN`. `SKILL` is its only gap.

**C1 — the cell.** The `Written by` value becomes `` `diagnose` ``: backticked, bare, no workflow
prefix, matching every other dispatched row in the column. Frontmatter and `Sections` cells unchanged.

**C2 — the row.** Column order is fixed by the table: `step · skill · subagent · expertise`.

```
| diagnose | `diagnose` | `analyst` | module's |
```

`analyst` is the registry name, unnamespaced, exactly as `architect` and `qa-engineer` appear in the
rows above; dispatch namespaces it to `orqestra:analyst` (D-014), which is what `step-diagnose.md:8`
already carries. `module's` is correct and correct for a *different reason* than the rows above it:
the module reaches `diagnose` through a `BUG`, not a `TASK`, and §5.5:949 makes the conditional class
mandatory under `BUG` as well (D-027). Place the row **last**, after `pr-comments` — the six rows
above are the task pipeline in order, and appending keeps that reading intact.

**C3 — the paragraph.** Two obligations, and the second is the one a partial edit misses:

1. Stop counting. "The other four" must not become "the other five"; a count in prose is falsified by
   the next row exactly as "22 skills" was. Name the property instead of the quantity — the rows that
   vary by module are `implement` and `pr-comments`, and *every other row* is a fixed role.
2. Say why `diagnose` is in a table about the steps of a task at all: it is the one row that is not a
   task-pipeline step. It runs in the `bugfix` workflow against a `BUG.md`, and it is listed here
   because the module's expertise reaches it the same way — a `BUG` carries `module:` too (§5.5,
   D-027). Without that clause a reader concludes the task pipeline has seven steps.

**C4 — the §7.7 row.** Columns are `Skill · Reads · Writes · Template`.

```
| `diagnose` | `BUG.md`, `PROJECT.md` | `DIAGNOSIS.md` | `templates/DIAGNOSIS.md` |
```

Verified against `step-diagnose.md`'s `READ` list and `TEMPLATE` line; `templates/DIAGNOSIS.md` exists.
Plugin-relative in prose, per D-026 — no `${CLAUDE_PLUGIN_ROOT}`, matching the six rows above it.
Place it after `review-phase`; the table's inclusion rule, read from its members, is *step skills that
write an artifact from a template*, and `diagnose` meets it.

**C5 — the tree comment.** The count is the only part that goes; the clause carrying the information
stays. Sanctioned wording:

```
├── skills/                    # one directory per skill — the folder name IS the invocation name
```

**C6 — the grid and its closing line.** `diagnose` joins the `STEP SKILLS` column (it is
envelope-dispatched and writes from a template; the other three columns are orchestrators, planning
skills and utilities). The closing line currently opens `22 skills.` — a bare deletion leaves the
sentence starting mid-thought. What that number was doing was asserting *this grid is all of them*, so
say that, and say why no number appears. Sanctioned wording:

```
This grid is the whole inventory. The folder name is the invocation name (§2), so it is also the
command list. No count is written here or in §2: `ls skills/` is the count, and a number stated in
prose is falsified by the next skill added — which is how this line came to say 22 twice, 1500 lines
apart, while the tree said otherwise.
```

## Structure

One file, `REQUIREMENTS.md`, inside the `docs` module (§5.2, D2). `README.md` is in `paths` and is
**not** affected — it makes no skill-count or `diagnose` claim.

The six edits land in three layers of the document, and the ordering constraint runs between them
rather than within them:

- **The catalogue and routing layer** (§4.8.1, §5.1.1) is where the amendment is *made*. C1 and C2 are
  the authoritative statements; everything else describes them.
- **The prose that reads off those tables** (§5.1.1's paragraph, §7.7, §7.12's grid) is *derived*. C3,
  C4 and C6 have no independent content — each is false the instant C1/C2 land and true again only
  when it matches them. They must move in the same commit; a reviewer checks them *against* C1 and C2,
  not against this design.
- **The counts** (§2, §7.12's closing line) are a different defect that this task happens to sit on
  top of. C5 and C6's closing line remove a class of statement, and they are correct independently of
  whether `diagnose` exists.

Nothing outside `REQUIREMENTS.md` may be reached into. In particular the spec must not be edited to
match `.orqestra/config.md` or `templates/config.md`: **`REQUIREMENTS.md:777` is the authoritative
routing table and the other two are instances of it.** This is provable rather than asserted —
`.orqestra/config.md` still carries `task_type` wording that D-011 removed, so an instance demonstrably
drifts while the spec cannot drift from one. That drift is pre-existing and belongs to nobody's task
here.

The commit lands before TASK-034 (D-019: code that cites a section inherits it, so docs leads).
`check-envelopes.py` stays red on `step-diagnose.md` throughout this task, by design.

## Decisions

- **D-028 — a §4.8.1 `Written by` cell names a skill exactly when the step composes a dispatch
  envelope.** Recorded as a decision rather than kept local because it governs every future row added
  to that column and, immediately, protects :583 from being "fixed" into C1's shape. `grep ROLE:` on
  the workflow's `step-*.md` is the test.
- **The skill is named `diagnose`, not `bugfix-diagnose` or `root-cause`** (local to this amendment;
  D-012 supplies the reason it is also the folder name). `bugfix-diagnose` would be the only hyphenated
  compound in the inventory and would make C1's cell read unlike every sibling. `root-cause` renames
  the step, which §7.3 and the `status` stage names cite as `diagnose`.
- **The two count sites stop asserting a count rather than counting to 23** (§8.2 human decision).
  Updating the number forces a choice between a spec that briefly overstates the tree and an edit
  TASK-034 may not make (D-019); removing the class dissolves the dilemma. Both replacements keep what
  the sentence was communicating — the invocation-name identity in §2, the completeness claim in §7.12
  — and §7.12's states the reason, so the number does not creep back.
- **`diagnose` is appended to §5.1.1's table rather than given a subsection.** The table's selection
  rule — steps whose subagent is fixed in every module — admits it (`analyst`, always). A §5.1.2 for
  one row would put one rule in two places, which is the failure `orqestra-conventions` names.
- **Not a §4.8 schema change**, so D-003's template-and-skill companions are not required. Stated
  explicitly because a reviewer seeing "§4.8.1" in the edit list will reach for that rule.

## Test Strategy

No test runner; verification is a reader with `grep` against the document as merged.

| criterion | what proves it |
|---|---|
| AC-1 | The §4.8.1 `DIAGNOSIS.md` row's `Written by` cell is `` `diagnose` `` — one backticked token, no workflow word. Compare it side by side with the `plan`, `design`, `qa`, `review-task` rows: the four cells are the same shape. `grep -n 'bugfix. diagnose' REQUIREMENTS.md` returns nothing |
| AC-2 | Read §5.1.1's table as an orchestrator would: look up the row whose `step` is `diagnose`, and get `diagnose` / `analyst` / module's. Cross-check `analyst` against `skills/bugfix/step-diagnose.md:8`'s `ROLE: orqestra:analyst` — the row and the live envelope name the same agent |
| AC-3 | `grep -n 'diagnose' REQUIREMENTS.md` — every hit is either one of the five amended sites or §7.3's step-*file* names, and nothing else in the document implies the step has no skill. Independently: `grep -n '^## \|^### \|^#### ' REQUIREMENTS.md` against the same command on `HEAD~1` produces an identical list, proving no renumbering. And §7.12's grid must contain `diagnose` — the section whose job is to be the inventory is the one a partial amendment leaves contradicting itself |
| AC-4 | `grep -nE '\b2[0-9] skills\b' REQUIREMENTS.md` returns nothing. Then read both replacement sentences aloud: §2's still says the folder name is the invocation name, §7.12's still says the grid is complete and is the command list. A bare deletion that leaves either sentence limp fails this criterion even though the grep passes |
| downstream | TASK-034 is the real check on the name: `SKILL: orqestra:diagnose` in `step-diagnose.md` and `python3 scripts/check-envelopes.py` at exit 0 succeed only if the name sanctioned above is the one authored. If it is not, that is this design's failure surfacing there |
