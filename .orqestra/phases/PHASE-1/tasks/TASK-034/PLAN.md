---
id: TASK-034
type: plan
status: done
updated: 2026-08-30
task: TASK-034
---

## Approach

**Write `skills/diagnose/SKILL.md` as a single-file `step` skill modelled on `skills/plan/SKILL.md`,
then add the one missing `SKILL:` line to `skills/bugfix/step-diagnose.md`.** Nothing else changes.

Every value the skill must declare is already fixed by TASK-033's spec amendments and by artifacts on
disk, so this step is reconnaissance into what `diagnose` must say **differently** from `plan`, not a
choice of shape:

| what | fixed by | value |
|---|---|---|
| name / invocation | §5.1.1:786, §4.8.1:585 | `diagnose`, dispatched as `orqestra:diagnose` |
| class and tool fields | §7.0 class table (:1081) | `step` — `Read, Write, Glob, Grep` / `Agent, Edit, NotebookEdit, Bash` |
| subagent | §5.1.1:786 | `analyst`, module's expertise |
| reads / writes | §7.7 (:1463) | `BUG.md`, `PROJECT.md` → `DIAGNOSIS.md`, `templates/DIAGNOSIS.md` |
| headings | §4.8.1:585 | `## Root Cause` · `## Evidence` · `## Fix Direction` · `## Regression Risk` |

**Where it must differ from `plan` — the four things that make it a procedure rather than a copy:**

1. **The scope unit is a `BUG`, not a `TASK`.** There are no acceptance criteria to restate and no
   `depends_on`. `plan`'s three `blocked_reason` rows (`contradictory-input`, `needs-splitting`,
   `criterion-unsatisfiable`) are two-thirds inapplicable: nothing here has criteria to contradict or
   satisfy. The precondition is instead §7.3's hard rule — a *reproduction* must already exist in
   `BUG.md#Reproduction`. See `## Open Questions` for the vocabulary.
2. **The procedure is evidence-gated, not approach-choosing.** `plan` step 3 picks between defensible
   approaches; `diagnose` must instead *disprove* the first plausible cause. The bar is written twice
   already — `skills/bugfix/step-diagnose.md` ("the place the symptom became visible") and
   `skills/bugfix/SKILL.md` rule 3 ("Evidence, or block") — so the skill states the falsification
   procedure and cites, rather than restating, the rule.
3. **`root_cause_found: false` is a `done` outcome, not a block.** This has no analogue in `plan`.
   `templates/DIAGNOSIS.md` carries the key defaulted to `false`, and `step-diagnose.md`'s gate offers
   `[ Investigate further ]` — so an honest failure to find the cause returns `STATUS: done` with the
   frontmatter key false, and the human decides. A skill that mapped it to `blocked` would remove the
   gate branch the workflow already draws.
4. **The Return feeds a gate, so it is wider than `plan`'s.** §5.5.1 forbids the orchestrator reading
   the artifact body, yet `step-diagnose.md`'s gate block renders `ROOT CAUSE`, `EVIDENCE`, `DIRECTION`,
   `RISK`. Those four lines can only reach the human through the return text. `plan`'s `AREAS`/`RISKS`
   pair does not carry them. The Return must therefore open with `SKILLS:` (D-025, AC-2) and then carry
   one line per gate field plus the `root_cause_found` verdict — inside the 10-line ceiling.

Alternative considered and rejected: **sharding the procedure into `skills/diagnose/step-*.md`.** Every
other `step`-class skill (`plan`, `design`, `implement`, `qa`) is a single `SKILL.md` — verified by
listing `skills/*/*.md`: only orchestrators (`task`, `greenfield`, `add-phase`, `bugfix`, `pr-comments`)
hold step files. Sharding is the orchestrator context-economy lever, and `plan` fits in 87 lines;
`diagnose` has no more to say. **Confirmed, not assumed: `skills/diagnose/` needs `SKILL.md` and
nothing else.**

Alternative considered and rejected: **moving the "bar" and gate prose out of `step-diagnose.md` into
the new skill.** TASK-034's Out of Scope forbids rewriting what `step-diagnose.md` does, and the gate is
the orchestrator's to render. The skill cites the bar; it does not relocate it.

## Affected Areas

Read, in the `plugin` module (`skills/`, `templates/`, `scripts/`) — all inside `PATHS`:

- **`skills/bugfix/step-diagnose.md`** — 52 lines. The envelope at :7–23 carries `ROLE STEP BUG MODULE
  PATHS STACK EXPERTISE READ TEMPLATE WRITE RETURN`. Exactly one always-class field is absent: `SKILL`.
  §5.5 puts the scope field "immediately after `SKILL`", so the line belongs between `STEP:` and
  `BUG:` — insertion point, not an append. The rest of the file (`## The bar`, `## The gate`) is the
  input this skill must be consistent with and is out of scope to change.
- **`skills/bugfix/SKILL.md`** — the Steps table row `| diagnose | step-diagnose.md | analyst | yes |`
  and the `## Diagnose` section already name the four `DIAGNOSIS.md` headings and the gate rationale.
  Rules 3 and 5 are the ones the new skill must not contradict. No change needed here.
- **`skills/plan/SKILL.md`** — 87 lines, the nearest shape: same class, same `analyst`, same no-`Edit`,
  same section order (`Inputs`/`Output`/`Procedure`/`Return`/`When you cannot proceed`/`Rules`).
- **`templates/DIAGNOSIS.md`** — already conformant to §4.8.1:585; frontmatter `id type status updated
  bug root_cause_found task`. `task:` is filled later by `promote`, not by this step.
- **`templates/SKILL.template.md`** — the authoring contract (§7.0). Its class table lists the `step`
  class as "plan, design"; §7.0:1081 now says "`plan`, `design`, `diagnose`". A one-word divergence
  inside an HTML comment, not schema-bearing and touched by no AC. Recorded, not scheduled.
- **`scripts/check-envelopes.py`** — read in full. It globs `skills/*/*.md`, so a new
  `skills/diagnose/SKILL.md` containing no `ROLE:` line adds no envelope and cannot regress the count;
  the single fix that turns it green is the `SKILL:` line above (AC-3).
- **`scripts/check-step-refs.py`** — read in full. Its two shape rules bound AC-4 precisely: rule 1
  fires only on a line beginning `|` inside a `SKILL.md`, rule 2 only inside a `step-*.md`. So a
  reference to `skills/bugfix/step-diagnose.md` written in **prose** in the new `SKILL.md` takes the
  plain plugin-relative form, resolves from the repo root, and trips neither rule; the same string in a
  table row would require `${CLAUDE_PLUGIN_ROOT}` (D-026). Backticked spans are the only thing scanned.
- **`agents/analyst.md`** — holds `Skill` in `tools:` (D-025 satisfied), so `orqestra:diagnose` will be
  invocable. But its `description:` reads "produces PLAN.md — approach, affected areas, risks, and open
  questions. Dispatched at the plan step", which is now false for one of its two steps. See Risks.
- **`.claude/skills/orqestra/`** — nothing to do. `PROJECT.md`:29 records it as symlinks to whole
  directories, so a new `skills/diagnose/` is picked up with no second edit and no new link.

## Risks

- **`agents/analyst.md`'s `description` names only PLAN.md and the plan step.** Dispatch resolves
  `ROLE` explicitly, so nothing breaks mechanically — but D-025's whole point is that the persona is
  what runs when a layer is missing, and this persona instructs plan-shaped behaviour ("Open questions
  are a legitimate output") to an agent writing a diagnosis. No AC covers it, and widening it is a
  second file in the diff. Listed as an open question rather than assumed in.
- **Wording the falsification bar twice.** `step-diagnose.md` and `bugfix/SKILL.md` both state it; a
  third copy in `skills/diagnose/SKILL.md` is the exact failure the conventions name (a rule written
  twice disagrees with itself). The skill must carry the *procedure* for reaching evidence and cite
  §7.3 / the step file for the *bar*.
- **`root_cause_found: false` mapped to `blocked`.** The plausible-looking move, and it silently
  deletes the gate's `[ Investigate further ]` branch: a blocked artifact never reaches the gate at
  all. The skill has to say explicitly that this is a `done` outcome.
- **The Return exceeding 10 lines.** `SKILLS`+`STATUS`+four gate fields+`root_cause_found`+`SCHEMA`+
  `BLOCKED` is already at the ceiling; anything else added does not fit.
- **`check-envelopes.py` and `config.md`'s `test_command` exit 1 today.** That is this task's
  precondition, not a defect — but it means a green run cannot be used as a "nothing regressed"
  baseline before the change. Only the after-state is meaningful.

## Open Questions

1. **`blocked_reason` vocabulary — resolved, recorded so it is not re-derived.** §4.4.3 (:335) is a
   closed list; the skill declares from it and invents nothing. Of the work reasons, exactly two can
   arise inside `diagnose`: `no-reproduction` when `BUG.md#Reproduction` holds no established failing
   reproduction (the precondition §7.3 and `bugfix/SKILL.md` make hard — note the value is written by
   the *reproduce* step today, and diagnose's use is detecting the missing precondition, not
   re-running it), and `contradictory-input` when the bug report and the reproduction disagree about
   the observed behaviour. `root_cause_found: false` is **not** in this table — see Approach 3.
   Whether `no-reproduction` is the right value for a *precondition* failure as opposed to a
   *reproduction attempt* failure is the one judgement here; it is the only member of the closed list
   that fits, and inventing a new one would violate §4.4.3.
2. **`BUG.md` has no `module:` key, and §5.5 says it does — does that block this skill?** No, and the
   skill must **not** state where a bug's module comes from. §5.5 makes `MODULE`/`PATHS`/`STACK`/
   `EXPERTISE` the *orchestrator's* obligation; the dispatched skill consumes them from the envelope
   and never derives them. So `skills/diagnose/SKILL.md` can be written honestly today by citing §5.5
   for the `PATHS` boundary and saying nothing about provenance. The contradiction (§5.5:957 and
   §5.1.1:795 both assert a `BUG` carries `module:`; `templates/BUG.md` and §4.8.1:584 list only `bug`
   and `severity`) is **TASK-037's**, is not resolved here, and no wording in this skill should presume
   either outcome. If TASK-037 resolves it by adding `module:` to `BUG.md`, nothing in this skill needs
   to change — which is the test that this is the right seam.
3. **Should `agents/analyst.md`'s `description` be widened to cover the diagnose step?** A human call:
   it is honesty about a persona that now serves two steps, but it is outside every AC and adds a file
   to the diff. Defaulting to *no* unless design says otherwise; recorded so it is not discovered at
   review as an omission.
