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
plus a seventh site the merged-file sweep found (see `## Deviations`).

| # | § / line | what it says now |
|---|---|---|
| C1 | §4.8.1:584 | `DIAGNOSIS.md`'s `Written by` cell is `` `diagnose` `` — one backticked token, the shape `plan`/`design`/`qa`/`review-task` use (AC-1) |
| C2 | §5.1.1:785 | routing row `\| diagnose \| \`diagnose\` \| \`analyst\` \| module's \|`, appended **after** `pr-comments` so the six rows above still read as the task pipeline in order (AC-2) |
| C3 | §5.1.1:787–795 | the fixed-role paragraph stops counting ("Every other row is a fixed role", was "The other four") and gains a second paragraph saying `diagnose` is the one row that is *not* a task-pipeline step, and why the module's expertise still reaches it — a `BUG` carries `module:`, so §5.5's conditional class is mandatory there too |
| C4 | §7.7:1462 | step-skills row `\| \`diagnose\` \| \`BUG.md\`, \`PROJECT.md\` \| \`DIAGNOSIS.md\` \| \`templates/DIAGNOSIS.md\` \|`, plugin-relative per D-026, after `review-phase` |
| C5 | §2:118 | tree comment is now `# one directory per skill — the folder name IS the invocation name`; the count went, the clause that carried the information stayed (AC-4) |
| C6 | §7.12:1656, 1661–1665 | `diagnose` joins the `STEP SKILLS` column of the grid (column-aligned at the same offset as the six above it); the closing line no longer opens with a number — it asserts completeness and the command-list identity, and states *why* no count is written, so the number does not creep back (AC-3, AC-4) |
| C7 | §1.3:69–71 | **not in the design.** See `## Deviations` |

**The sweep the envelope required, and what it returned.** Three of the six components carry no
independent content, so I did not stop at the checklist. Against the *merged* file:

| grep | result |
|---|---|
| `bugfix. diagnose` | **no hits** — nothing still describes the step as workflow-plus-step |
| `\b[0-9]+ skills\b` | one hit, §1.3:69 `nit has 21 skills`. **Correctly kept**: a fact about a different, frozen project, which orqestra adding a skill does not falsify. Every assertion of *orqestra's own* count is gone |
| `diagnose` (all 10 hits) | each is an amended site, §7.3:1208's step **filename** (`step-diagnose.md`, untouched and already true), or ordinary prose (§1:25, §3:42, §7.4:1243, §12:1833). Nothing implies the step has no skill |
| `no skill\|without a skill` | one hit, §9:2062 "No skill edits a done artifact" — unrelated sense |
| `^#{1,4} ` diffed against `HEAD` | **identical**. No section renumbered (AC-3) |

**:583 is protected and I checked it.** `| \`BUG.md\` | \`bugfix\` intake |` survives byte-identical.
Under D-028 it is truthful — `grep ROLE: skills/bugfix/` still returns exactly one hit,
`step-diagnose.md:8`, so `intake` dispatches nobody and has no skill to name. **My amendment states
no rule about that column**: C1 rewrote a single cell and added no prose generalising it, so nothing
I wrote condemns :583. The discriminator lives in D-028 alone, which is where a later "consistency"
fix will find it.

**Verification** (`git status` shows `REQUIREMENTS.md` as the only modified file; the two untracked
`ORQESTRA_*.md` files pre-date this task and are not mine):

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
| minor | design lists six components; §1.3:69–71 is in none of them | Added C7: §1.3's nit comparison said "orqestra has **22 skills**, no archetypes…". Rewrote to "a comparable number of skills and none of the rest — no archetypes, no state machine, no schemas, and one rework rule", plus "The simplification is not a smaller skill count; it is the machinery underneath them." | The required post-merge sweep returned it. It is AC-4's exact defect class — a hard-coded orqestra skill count that TASK-034 falsifies — and the design's own §7.12 wording promises "No count is written here or in §2", which would have been the third such promise broken by a count 1580 lines earlier. The plan's grep found two count sites; there were three. Leaving it is the partial amendment the task names as its likely failure. The rewrite keeps what the sentence communicated and arguably sharpens it: the original invited reading 22-vs-21 as the simplification, which was never the claim |

## Tech Debt

- **`.orqestra/config.md`'s routing table still carries `from the module's task_type` and a
  `task_type → subagent` table that D-011 removed.** Found while confirming which routing table is
  authoritative. Pre-existing, workspace state rather than a deliverable, and outside `docs` — noted,
  not fixed (D3, D14).
- **`templates/config.md`'s routing table has no `diagnose` row.** The design answers Q1 that it needs
  none, because `step-diagnose.md` will carry `SKILL: orqestra:diagnose` literally and no lookup
  occurs. If that reading is wrong, `check-envelopes.py` surfaces it in TASK-034 — a cheap failure
  against an existing check. `plugin` module either way.
- **§7.7's table has no stated inclusion rule.** I added `diagnose` on the design's reading — *step
  skills that write an artifact from a template*. If the intended rule is *steps of the delivery
  pipeline*, then `review-phase` above it does not belong either. Pre-existing ambiguity; not resolved
  here.
