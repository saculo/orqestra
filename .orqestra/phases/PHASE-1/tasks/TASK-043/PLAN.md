---
id: TASK-043
type: plan
status: done
updated: 2026-08-31
task: TASK-043
---

## Approach

**Give the `BUG.md` write path to a directly-invoked, non-orchestrator skill that holds `Write` — the
shape `clarify` already uses — rather than widening the orchestrator or composing a `ROLE:` envelope.**

The answer is already in the tree, and it is not a new pattern. `skills/greenfield/SKILL.md:5-6`
carries the *identical* tool fields to bugfix — `allowed-tools: Read, Glob, Grep, Skill, Agent,
AskUserQuestion` / `disallowed-tools: Write, Edit, NotebookEdit` — and greenfield still produces its
first artifact. It does it at `step-clarify`, and its step table (`SKILL.md:34`) records how:
`clarify` — **invoked directly, not as a subagent**. `skills/clarify/SKILL.md:4` holds
`allowed-tools: Read, Write, Glob, Grep, AskUserQuestion` with `disallowed-tools: Agent, Edit,
NotebookEdit`, and `SKILL.md:8-9` states the reason: *"the questions reach the human rather than an
agent."* Nothing in greenfield writes without invoking a `Write`-holding skill; the orchestrator
itself writes nothing anywhere.

That precedent fits intake exactly, on all three axes:

| Property | `clarify` | bugfix intake |
|---|---|---|
| Conversational, human present by construction | yes (`SKILL.md:51`) | yes — `step-intake.md:35`, and `AskUserQuestion` is in bugfix's `allowed-tools` |
| Produces exactly one artifact | `CLARIFICATIONS.md` | `BUG.md` (`step-intake.md:34`) |
| Must not be a subagent | greenfield `SKILL.md:68-69` | same reason — a subagent between the reporter and the module question makes step 1-4's re-ask loop useless |

`skills/init/SKILL.md:5` is the second half of the same precedent, and it is worth naming precisely
because it is easy to misread as licensing the opposite. init holds `Write` and writes directly — but
it also holds `disallowed-tools: Agent` and dispatches nobody. It is `Class: planning`, not an
orchestrator. So init licenses *a non-orchestrator skill holding `Write`*; it licenses nothing about
an orchestrator holding one.

`skills/bugfix/step-promote.md:7-10` shows bugfix already using this exact mechanism to produce an
artifact: `Skill: orqestra:create-task`, no `ROLE:`, and `skills/create-task/SKILL.md:4-5` holds
`Write` with `Agent` disallowed. Intake can use the same shape as promote. That is the strongest
evidence, because it means the fix adds no mechanism the workflow does not already run.

**Alternative rejected — widen `skills/bugfix/SKILL.md:6`.** TASK.md's Out of Scope forbids it
reflexively and the spec agrees: §4.4.5.3 cites the orchestrator's missing `Write`/`Edit` as the
guarantee that *"the orchestrator does not fix a malformed artifact itself"*, and §7.0.1 records
(lines 1131-1139) that orchestrators run in the main session where `disallowed-tools` clears at the
user's next message — so the loss is permanent while the protection was only ever per-turn. Trading a
real guarantee for a mechanism that already exists twice over is a bad trade.

**Alternative rejected — a `ROLE:` envelope dispatching a subagent at intake.** It would satisfy
`grep ROLE:` and D-028's test, but it puts a subagent between the reporter and the re-ask loop that
`step-intake.md:22-35` depends on, and `analyst`'s obligations (`agents/analyst.md:31`, one write path,
D2) do not fit an actor whose whole job is a conversation. Note this is also why the amendment sites
below cannot simply be handed to the analyst.

## Affected Areas

All inside `plugin` (`skills/`), except the two spec sections recorded under Open Questions.

**Verified — the defect, confirmed independently:**

- `skills/bugfix/SKILL.md:6` — `disallowed-tools: Write, Edit, NotebookEdit`. Line 110 states the rule
  it cannot honour: *"Never write artifacts yourself — dispatch (D1)"*, and nothing at intake does.
- `skills/bugfix/step-intake.md` — 57 lines, zero `ROLE:`. `## Write` (lines 39-48) names the template
  and the obligation; no actor holds a tool that can execute it. `grep '^ROLE:' skills/` returns 10
  hits across the plugin and exactly one is under `skills/bugfix/` — `step-diagnose.md:13`.
- `skills/bugfix/SKILL.md:39-46` (`## Intake`) restates the same inert obligation at the workflow level.

**Verified — a second write to `BUG.md` with the same gap, and a second dispatch gap:**

- `skills/bugfix/step-reproduce.md:25` — *"Update `BUG.md` `## Reproduction` with what actually worked"*.
  This is an amend of `BUG.md` and falls under AC-2. `step-reproduce.md` also contains **zero `ROLE:`**,
  while `SKILL.md:30`'s step table claims reproduce dispatches *"the touched module's agent"*. The step
  table and the step file disagree — a second instance of the TASK-043 pattern inside the same workflow,
  found by reading rather than asserted.

**Verified — the amendment site D-029 names:**

- `skills/bugfix/step-diagnose.md:59-74`. Lines 70-74 already state the gap plainly under §7.0.1
  discipline: *"no actor in this workflow currently holds a tool that can amend `BUG.md`"*, and defer
  closing it to a separate task — this one. Lines 63-68 are the procedure that becomes executable once
  a write path exists.
- `.orqestra/decisions/D-029...md:40-42` — the constraint being made executable. Not re-litigated (D9).

**Verified — the schema and its checkers:**

- `templates/BUG.md` — 27 lines. `module:` at line 6 with the D-029 comment; `status: in-progress` at
  line 4. **On the `status` question:** `in-progress` is the only default any actor sets, and nothing in
  `skills/bugfix/` moves it afterward — the workflow ends at handoff with the bug promoted, not closed.
  So the default implies the file is written **once, live, by whoever is holding the conversation**, and
  then mutated in place by later steps. That is an argument *for* the intake-writes-live shape and
  *against* an after-the-fact composer, and it is a second reason (beside D-029) that an amend path is
  structurally required rather than merely convenient.
- `scripts/check-envelopes.py:60-63` — an envelope *"starts at `ROLE:`"*. The script validates envelopes
  that exist; it never asserts a step has one. So AC-4 stays green whether or not an envelope is added —
  but any envelope added under `BUG` scope must carry `MODULE PATHS STACK EXPERTISE`
  (`check-envelopes.py:47`, `test-check-envelopes.py:76-77`).
- `scripts/check-templates.py:2,53` and `test-check-templates.py:77` — checks §4.8.1 columns 2
  (frontmatter) and 3 (headings) only. The **`Written by` cell is not machine-checked**, so a change
  there cannot be caught by AC-4's chain; only a reader catches it.

**Verified — the precedents:** `skills/clarify/SKILL.md` (whole file), `skills/init/SKILL.md:5-6,22`,
`skills/create-task/SKILL.md:4-8`, `skills/greenfield/SKILL.md:5,34,62-69,86`, `agents/analyst.md:4`
(`tools: Skill, Read, Write, Glob, Grep` — `Write` yes, `Edit` no, confirming the task's premise).

**Read but outside `plugin` — reported, not touched (D14, D-019):** `REQUIREMENTS.md:584` (§4.8.1's
`BUG.md` row, `Written by: bugfix intake`) and `REQUIREMENTS.md:1207-1220` (§7.3's walkthrough).

## Risks

1. **The precedent may never have been executed.** `clarify` is invoked by an orchestrator whose
   `disallowed-tools` removed `Write` *for the turn* (§7.0.1 line 1119: removed from the pool "until the
   user's next message"). Whether a nested `Skill` invocation re-grants `Write` inside that turn is
   **not documented anywhere I read**, and nothing in this repo has been run (PHASE-1 is a draft). If it
   does not re-grant, greenfield has the identical latent defect and this task's chosen approach fixes
   nothing. This is the one risk that can invalidate the whole approach, and AC-3's
   "demonstrated by sequence rather than asserted" is the criterion that will catch it — a walkthrough
   on paper will not.
2. **Amending `BUG.md` by whole-file `Write` loses the report.** `step-intake.md:45-48` requires the
   report be recorded *as reported* — *"A rewritten report loses the symptom that was actually
   observed."* An actor holding `Write` but no `Edit` must reproduce the reporter's prose verbatim to
   change one frontmatter key. That is the highest-fidelity-risk operation in the workflow, on the one
   field D-029 makes load-bearing.
3. **The analyst cannot be the amender, for a reason tooling does not fix.** `agents/analyst.md:31` and
   D2 bind it to exactly one `WRITE` path, which at diagnose is `DIAGNOSIS.md`. Adding `BUG.md` as a
   second write path is a D2 violation whether or not it holds `Edit` — `step-diagnose.md:62-63` already
   says so (*"it holds one write path (D2) and no `Edit`"*). So AC-2's actor is a separate question from
   AC-1's, not the same answer applied twice.
4. **Three writes to `BUG.md`, three steps, one file.** intake creates, reproduce amends
   `## Reproduction`, diagnose amends `module:`. Any solution that fixes only intake satisfies AC-1 and
   leaves AC-2 half-open, and the reproduce site is the one most likely to be missed because
   `SKILL.md:30` already claims that step dispatches.
5. **D-028's test does not classify a `Skill:` invocation.** D-028 says §4.8.1's `Written by` cell names
   a skill when the step *composes an envelope*, workflow-plus-step when it *runs inline*, and
   *"`grep ROLE:` is the test"*. A direct `Skill:` invocation is neither: it writes, but has no `ROLE:`.
   `step-promote.md` is already in this state today. Whatever this task does, it should not leave a
   third unclassified case without saying which side of D-028 it falls on.
6. **`SKILL.md:110` and `SKILL.md:30` become false or stay false.** Rule 5 says never write, always
   dispatch; the step table says reproduce dispatches. If the fix is "invoke a skill", both lines
   describe a mechanism the workflow does not use, and a rule that is false in its own file is worse
   than no rule (this is the failure this whole task is an instance of).

## Open Questions

1. **Does `Write` survive into a skill invoked by an orchestrator that disallowed it for the turn?**
   This must be answered by observation, not by reading — run `claude --plugin-dir .` (D-013) and drive
   `/orqestra:greenfield` to its clarify step. If `clarify` cannot write, this is a `plugin`-wide defect
   affecting greenfield, add-phase and bugfix alike, and TASK-043's scope is wrong. **Design should not
   start until this is checked**; it is one command, and it decides between two different fixes.
2. **Who amends at reproduce and at diagnose — the same actor as intake, or a named other?** AC-2 allows
   either. Risk 3 rules out the analyst; risk 2 makes whole-file `Write` uncomfortable but not
   impossible on a 27-line file. A human should say whether "the intake writer is re-invoked to amend"
   is acceptable, or whether an `Edit`-holding actor is wanted. I do not think this is design's to
   decide alone, because it trades a D2 principle against report fidelity.
3. **Does `skills/bugfix/step-reproduce.md`'s missing dispatch belong to this task or its own?**
   It writes `BUG.md` (line 25), so AC-2 covers that write. But the step *also* dispatches nobody while
   `SKILL.md:30` says it dispatches an agent to run a reproduction — that is a separate capability gap
   (running a build, writing a test) with no relation to `BUG.md`. Left unsplit, this task grows a
   second subject; left out, `SKILL.md:30` stays false. **My reading is that the `BUG.md` write is in
   scope and the reproduction dispatch is a fourth instance of the pattern deserving its own task**, but
   the boundary is a human's call.
4. **`REQUIREMENTS.md` carries the same assumption and is a different module.** Reporting, per TASK.md
   and D14:
   - `REQUIREMENTS.md:584` — §4.8.1's row reads `` `BUG.md` | `bugfix` intake ``. Under D-028 that cell
     is the "runs inline" form, which is *correct about today* and describes something that cannot
     execute. If intake becomes a skill invocation, this cell is wrong.
   - `REQUIREMENTS.md:1210-1211` — §7.3's walkthrough names **no writer** for either intake or
     reproduce: *"bug report from args or interactive → work/BUG-NNN/BUG.md"*. It carries exactly the
     assumption this task exists to break, so **yes, §7.3 has the same defect.** AC-3's walkthrough will
     contradict it.
   Per D-019, skills that *cite* a section inherit it and docs leads — and `step-diagnose.md:68` and
   `SKILL.md:77` both cite §7.3/§7.3.1. So this may need a `docs` task **before** the `plugin` change,
   not after. That sequencing is a human decision and I am flagging it rather than assuming.
