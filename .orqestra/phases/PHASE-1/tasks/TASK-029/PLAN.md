---
id: TASK-029
type: plan
status: done
updated: 2026-08-30
task: TASK-029
---

## Approach

Amend §5.5's obligation table in place — two rows, no new section, no renumbering. The scope row
(`REQUIREMENTS.md:940`) and the conditional row (`:941`) are both wrong in the same way: each was
written around a scope unit that already exists and carries `module:` in its own frontmatter, and
neither reaches a dispatch composed before that unit exists. `create-phases` is the extreme case —
it has no scope unit at all — and `close-phase`/`add-phase` are the milder one, conformant in
practice but excused by no clause. One amendment fixes both families.

Amending rows beats appending a §5.5.2: nothing is renumbered either way (§5.5.1 already exists, so
a new subsection would be §5.5.2 and safe), but a second place stating the obligation is a second
place to disagree with the table, and the conventions' "never restate a rule you can cite" applies
inside the file as much as across it. The table is already declared "the only thing that answers"
the field question at :861-862; the fix belongs in the table.

Alternatives considered and rejected:

- **Add a fourth scope value `PROJECT:`.** Rejected. There is exactly one project, so the field
  would carry a constant — a field with no consumer, which is precisely what Rule B (§4.4.1)
  forbids and what removed `task_type` (D-011).
- **Excuse `create-phases` by name**, as the conditional row already excuses `create-phases` and
  `create-tasks`. Rejected: naming steps by name is exactly the defect F-4 records — the list went
  stale the moment `close-phase` and `add-phase` were written, and it would go stale again.
- **Make the whole scope class conditional on judgement** ("when a unit of work applies").
  Rejected against AC-1: a rule needing judgement is what made the table unexecutable.

The decidability requirement in AC-1 is the real constraint, and the candidate that satisfies it
without naming steps is **the dispatch's own `READ` list**: the orchestrator has already read the
scope unit's file to route the dispatch, so "does `READ` name a `.orqestra/phases/**` scope-unit
artifact" is one thing, mechanically checkable, and the orchestrator has it in hand. Verified
against the real envelopes: `greenfield/step-tasks.md:17` carries `PHASE: PHASE-1` and reads a
`PHASE.md`; `greenfield/step-phases.md:16-21` reads only `PRD.md`, `CLARIFICATIONS.md`,
`PROJECT.md`, `modules.md`, `INDEX.md` — no scope unit, hence no scope field. Selecting the exact
discriminator and its wording is design's call; this plan records that a discriminator meeting AC-1
exists and that the two named alternatives do not meet it.

For the conditional row (F-4), the fix TASK-015's reviewer already identified holds up on
inspection: state the condition against the scope unit's frontmatter generically rather than
listing `TASK.md`/`BUG.md`, and name `templates/PHASE.md` as the case with no `module:` key.
Verified: `templates/PHASE.md` frontmatter carries `id` and `type: phase` only — no `module:`.
That closes `close-phase` and `add-phase` by the rule rather than by enumeration.

Scope of the edit: `REQUIREMENTS.md` only. This is **not** a §4.8 three-edit schema change (D-003)
— the envelope is a prose contract, not an artifact schema, and has no catalogue row and no
`templates/` file. It is a D-019 spec-first change: docs states the rule here, `plugin` applies it
in `skills/` and `scripts/` under TASK-030.

## Affected Areas

Inside the `docs` module (`REQUIREMENTS.md`, `README.md`):

| file | what is there |
|---|---|
| `REQUIREMENTS.md:934-952` | The obligation table and its closing paragraph. Row `:940` is the scope class; row `:941` is the conditional class carrying F-4's defect. Both are the edit surface. |
| `REQUIREMENTS.md:870` | The example envelope's `EXPERTISE: java-expertise, test-quality`, which F-3 records as contradicting §5.1's `api` row (`:731`, `java-expertise, spring-conventions`). Inside this module and cheap to correct alongside. |
| `REQUIREMENTS.md:957-975` | §5.5.1 already exists. Any appended subsection would be §5.5.2; nothing renumbers. |
| `README.md` | **Does not exist in the repository.** The module row lists the path, but there is no file, so no README work is implied. Verified by attempted read. |

Read for evidence, outside this module and **not to be edited here**:

- `skills/greenfield/step-phases.md:12-25` — the non-conformant envelope. No scope field.
- `skills/greenfield/step-tasks.md:17` — `PHASE: PHASE-1`, the contrasting conformant case.
- `skills/close-phase/SKILL.md:38-41` and `skills/add-phase/step-define-phase.md:16-19` — both
  `PHASE`-scoped, both omitting `MODULE`/`PATHS`/`STACK`/`EXPERTISE`. Already conformant in
  behaviour; unreached by the rule's current wording. This is F-4, confirmed as real.
- `templates/PHASE.md:2-3` — no `module:` key.
- `scripts/check-envelopes.py:13-14,31,69` — the checker's docstring paraphrases the table and
  `SCOPE = ["TASK","PHASE","BUG"]` enforces exactly-one. It will keep failing `step-phases.md`
  until TASK-030 lands.
- `.orqestra/phases/PHASE-1/tasks/TASK-015/REVIEW.md:29-32` — the deferred findings table.

## Risks

- **AC-2's second clause lands outside this module.** `scripts/check-envelopes.py` is `plugin`
  (`modules.md:13`); this task is `docs`. Read literally, AC-2 makes TASK-029 a D14 violation.
  It is not a split: TASK-030 already exists, `depends_on: [TASK-024, TASK-029]`, its AC-1 is
  "`check-envelopes.py` exits 0 — all ten envelopes conform", and its Out of Scope names
  "Changing §5.5" as TASK-029's. The checker edit is already owned. AC-2 overreaches into work a
  downstream task holds; the boundary is not ambiguous, only the criterion's wording is. Treating
  AC-2's first clause as this task's and the second as TASK-030's keeps both tasks whole.
  Consequence if unamended: qa cannot pass AC-2 without an out-of-module edit that review must
  flag as `major` (§7.8.1, D2).
- **AC-3 names F-2, but F-2 is closed.** `TASK-015/REVIEW.md:15` states "F-1 and F-2 are both
  genuinely closed"; `:24` states "F-3 and F-4 remain open". The findings table at `:29-32`
  contains F-3 and F-4 only. AC-3's own description — "the module condition reaches `close-phase`'s
  `PHASE`-scoped dispatch and `add-phase/step-define-phase.md`" — is verbatim F-4. So AC-3 covers
  F-3 and F-4; "F-2" is a transcription slip. Acting on the id rather than the description would
  produce a criterion with nothing to satisfy.
- **The two rows are coupled and must move together.** If the scope row becomes omittable for a
  project-wide dispatch but the conditional row still keys off "the scope unit has a module", a
  dispatch with no scope unit has no defined answer for `MODULE`/`PATHS`/`STACK`/`EXPERTISE`
  either. `create-phases` omits all four today (`step-phases.md:12-25`) and must stay conformant.
  Amending one row alone re-opens the defect one level down.
- **A rule stated only in prose will drift from the checker.** `check-envelopes.py:13-14` already
  paraphrases the table in its docstring; the amendment creates a second paraphrase that TASK-030
  must chase. Precision in the row's wording is what keeps that mechanical.
- **Every conforming envelope must survive the amendment.** Nine of ten envelopes conform under the
  current scope rule. A rewording that widens omission too far turns a currently-caught omission
  into a legal one, silently. TASK-030's AC-1 is the check, but it runs after this task merges.

## Open Questions

1. **Is AC-2's "and `scripts/check-envelopes.py` encodes the amendment" struck from this task, as
   TASK-030's AC-1?** Recommended: yes — the evidence above is one-directional. This plan proceeds
   on that reading; a human should confirm it so qa grades AC-2 on the first clause only. If the
   answer is no, TASK-029 is `needs-splitting` and TASK-030 loses its reason to exist.
2. **Does AC-3 mean F-3 and F-4?** Recommended: yes, per `TASK-015/REVIEW.md:15,24,29-32`. Confirm
   whether F-3 (the `:870` example-envelope `EXPERTISE` mismatch) is to be fixed here or restated
   as still-open — it is in-module and small, but it is a different defect from F-4 and AC-3's
   description does not mention it.
3. **May the amendment change the shape of an envelope that conforms today** — e.g. requiring a
   new marker line on project-wide dispatches — or must it only widen the rule so `step-phases.md`
   conforms unchanged? This decides whether TASK-030 is a one-file checker change or ten envelope
   edits, and design cannot choose the discriminator without knowing.
