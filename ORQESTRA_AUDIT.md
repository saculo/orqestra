# Orqestra workflow audit — 2026-09-01

Snapshot reviewed: commit `7c8041a` on branch `orqestra/audit-backlog` — named
`feat/TASK-043-bugfix-can-write-bug` when this audit was written.

This is a fresh audit of the current repository. It replaces the deleted audit files; it is not a
copy of their findings. The focus is whether the documented workflows can execute, resume after an
interruption, preserve their invariants, and report truthful state.

## Executive summary

The architecture is thoughtful, and the static contract checks have improved, but the tool is not yet
safe to run end to end. The largest problem is not an edge case: several orchestrators permanently
remove `Write`/`Edit` from the current session and all subagents, then attempt to dispatch writers or
mutate gate state. The repository's own D-031 proves this runtime behavior.

The next most important defects are pipeline-state defects. Source work happens before the task branch
exists; review rework can resume while treating stale QA/review artifacts as current; phase acceptance
has no persistent representation; and the generic approval/rejection commands do not know the
side-effects required by each kind of gate.

Recommended order: fix findings 1–6 before adding workflow features, then fix delivery integration and
schema enforcement, then improve developer checks and usability.

## Critical pipeline and business-logic defects

### 1. Nested skills remove the tools that later steps require

**Evidence:** `greenfield`, `add-phase`, `bugfix`, `task`, `close-phase`, and `status` declare
`disallowed-tools: Write, Edit, NotebookEdit`; for example `skills/task/SKILL.md:5-6` and
`skills/status/SKILL.md:4-5`. D-031 records that invoking such a skill removes those tools for the
session and its subagents, and a downstream `allowed-tools` declaration cannot restore them
(`.orqestra/decisions/D-031-skill-tool-fields-probed.md:20-31`). The workflows nevertheless dispatch
writers, set gate status, or write `PR.md` (`skills/task/SKILL.md:87-94`,
`skills/task/step-push.md:43-49`).

**Failure:** A same-turn workflow can reach a writer that has no `Write`, or an orchestrator can reach
a gate that it cannot persist. It may appear to work only when a new human message restores the tool
pool. `approve` and `reject` are also affected: each invokes read-only `status` before trying to edit
state (`skills/approve/SKILL.md:23-31`, `skills/reject/SKILL.md:19-27`).

**Fix:** Remove persistent `Write`/`Edit` denial from any skill that invokes another skill or agent in
the same workflow. Keep the restriction as a behavioral rule and enforce artifact ownership in the
dispatch contract/checker. If hard isolation is required, execute every writer in a fresh process or
session whose tool pool is independent; do not rely on a nested `allowed-tools` field to restore it.
Add a runtime integration test for `orchestrator -> status -> writer -> gate mutation`.

### 2. Bug intake and reproduction have no executable writer

**Evidence:** `bugfix` denies `Write`/`Edit` (`skills/bugfix/SKILL.md:5-6`). Intake is not dispatched,
but directly writes `BUG.md` (`skills/bugfix/step-intake.md:37-48`). Reproduce is described as a module
agent dispatch in the step table, but `step-reproduce.md` contains no dispatch envelope. It must create
a failing test and edit `BUG.md` (`skills/bugfix/step-reproduce.md:8-25`).

**Failure:** The workflow cannot create its first state artifact. Even after fixing intake, reproduce
has no actor with a declared source boundary or artifact write target. A failing test would also dirty
the shared base working tree before promotion, and the later task preflight rejects any dirty tree.

**Fix:** Make intake a dedicated writer (ANALYST!!) step or allow the orchestrator to write only `BUG.md`. Dispatch
reproduction explicitly with `ROLE/SKILL/BUG/MODULE/PATHS/READ/WRITE/RETURN`. Decide ownership of the
failing test: preferably create the task branch before reproduction and commit the test there; an
alternative is to save a patch as a bug artifact and apply it after task branch creation. Do not leave
a failing source change unowned on the base branch.

### 3. The task branch is created after implementation, QA, and review

**Evidence:** preflight requires the base branch and says no branch is created
(`skills/task/step-preflight.md:3-4,27-36`). The branch is created only in push
(`skills/task/step-push.md:7-20`), after implement, QA, and review. Yet the generated project rules say
never work on the base branch (`templates/PROJECT.md:72-73`), and the task skill says artifacts are
committed on the task branch only "once one exists" (`skills/task/SKILL.md:118-119`).

**Failure:** Source edits are made on the base branch. Artifact commits either cannot happen after each
step or pollute the base branch. After an interruption, a clean-tree preflight cannot distinguish
uncommitted task work from human work, while committed work changes the base used by later tasks.

**Fix:** Resolve and create/adopt the task branch during preflight, immediately after dependency/base
checks and before planning backfill or implementation. Record the branch-to-task association in
`TASK.md` or a branch metadata artifact. Commit each validated step on that branch. Push remains the
first remote operation, not the first branch operation.

### 4. Rework resume can skip QA and review for changed code

**Evidence:** status derives the stage solely from currently `done` artifacts
(`skills/status/SKILL.md:35-61`). A rejected review loops to implement, but the previous passed `QA.md`
and review artifact remain on disk (`skills/task/step-review.md:50-60,99-118`). Merge rejection also
returns to implement (`skills/task/step-merge.md:39-45`).

**Failure:** If the run stops after re-implementation, status sees the old passed QA and may derive
`verified`; it then resumes at review and skips QA of the changed code. After a merge-gate rejection,
old QA and review can both remain valid-looking, allowing resume at push and skipping both. Artifact
presence does not prove that an artifact evaluated the current implementation generation.

**Fix:** Add a monotonic `revision`/`attempt` identifier or source commit SHA to IMPLEMENTATION, QA,
REVIEW, and PR artifacts. Status advances only when adjacent artifacts reference the same current
revision. On any route back to implement, explicitly supersede/invalidate all downstream artifacts.
Test interruption after each rework boundary, not only uninterrupted loops.

### 5. Cross-session gates are not modeled strongly enough

**Evidence:** every gate parks an ordinary output artifact at `awaiting-approval`; `approve` then finds
exactly one parked artifact, sets it to `done`, and resumes a generic "next step"
(`skills/approve/SKILL.md:21-31`). The greenfield design gate covers every task after all designs are
created, but there is no single phase-level design-gate artifact. Merge approval requires live GitHub
verification and updates both PR and task (`skills/task/step-merge.md:47-55`), while generic approval
only changes the parked artifact.

**Failure:** Multiple DESIGN files cannot represent one design gate without either parking several
artifacts (which `approve` rejects) or arbitrarily parking one. Generic approval cannot safely perform
gate-specific side effects such as verifying a merge, closing a phase, or selecting a rejection route.
The promised "stored return summary" is not a schema field, so a later session may not have the text
it is required to present.

**Fix:** Add a dedicated `GATE.md` (or equivalent gate record) with unique id, owning workflow, step,
scope, target artifacts, summary, allowed choices, approval note, and resume action. `approve/reject`
should dispatch to a typed gate handler, not mutate arbitrary artifacts generically. Make one active
gate per workflow explicit; do not infer it by globally scanning output statuses.

### 6. Closing a phase with an accepted gap wedges the next phase

**Evidence:** close-phase allows `criteria_met: false` to be accepted and marks `PHASE.md` done
(`skills/close-phase/SKILL.md:73-99`). Add-phase requires `criteria_met: true` or an "explicitly
accepted gap" (`skills/add-phase/step-preflight.md:10-17`), but `PHASE_SUMMARY.md` has no accepted-gap
field and `criteria_met` is only true/false (`templates/PHASE_SUMMARY.md:1-8`). Close-phase also calls
`create-tasks` in "gap mode" (`skills/close-phase/SKILL.md:83-86`), while `create-tasks` defines no
such mode (`skills/create-tasks/SKILL.md`).

**Failure:** Honest acceptance leaves `criteria_met: false`, so the next phase has no machine-readable
way to distinguish an accepted gap from an unclosed phase. Choosing "Add tasks" invokes a nonexistent
behavior.

**Fix:** Add an explicit closure disposition such as `closure: met | accepted-gap` plus acceptance
note/date, and make add-phase consume it. Define gap mode as a real skill argument and contract: input
unmet SC ids, append tasks to the same phase, preserve existing tasks, and re-open phase status. Or
remove the option until implemented.

## High-severity technical and flow defects

### 7. PR comment fetching starts with an unsupported `gh` field

**Evidence:** both fetch instructions use `gh pr view --json ... reviewThreads`
(`skills/pr-comments/SKILL.md:40-43`, `skills/pr-comments/step-fetch.md:4-7`). Local `gh 2.94.0` lists
`comments` and `reviews`, but not `reviewThreads`; the command exits before the REST fallback runs.

**Fix:** Fetch review threads through `gh api graphql` with pagination, including thread id, resolved
state, comments, path, and line. Use REST only for review comments that GraphQL did not return. Add a
fixture-backed parser test and a smoke test that checks the installed CLI's accepted JSON fields.

### 8. PR-comment resolution edits source without a dispatched owner

**Evidence:** `step-resolve.md` says to route by module and fix comments, but supplies no dispatch
envelope (`skills/pr-comments/step-resolve.md:1-25`). The parent skill itself holds broad Write/Edit and
Bash access. Static envelope checks therefore see nothing to validate.

**Failure:** The orchestrator can directly modify arbitrary source without the module agent,
expertise, PATHS enforcement, or a recorded write target. Standalone comments touching different
modules also violate the one-module ownership model. The claim that these edits were "already
reviewed" is inaccurate: the requested fix creates a new diff.

**Fix:** Dispatch one resolution unit per module with explicit PATHS and comment ids. Run the normal QA
suite after the batch (already required), then perform a lightweight review of the new diff or require
the external reviewer/CI to approve it before merge. Persist the source commit SHA in RESOLUTION.md.

### 9. Review-phase cannot verify the running system with its declared tools and inputs

**Evidence:** review-phase requires exercising actual behavior (`skills/review-phase/SKILL.md:25-30,
40-55`) but its Bash allowlist permits only `git diff` and `git log` (`skills/review-phase/SKILL.md:4`).
The close-phase envelope does not pass PROJECT.md, so the reviewer does not receive project test/run
commands (`skills/close-phase/SKILL.md:36-51`).

**Failure:** It can aggregate paperwork but cannot execute the behavior it must use as evidence. The
phase verdict can become a documentation roll-up masquerading as system verification.

**Fix:** Include PROJECT.md and relevant runtime/test configuration in READ. Allow the exact project
commands resolved from PROJECT.md/config, preferably through a constrained test runner rather than
unrestricted shell. Require each SC row to record command, exit status, and observation.

### 10. Attempt limits are off by one

**Evidence:** the default is 3, examples say not to attempt a fourth, but QA and reject block only when
`attempts > max_attempts` (`skills/task/step-qa.md:44-48`, `skills/reject/SKILL.md:20-24`).

**Failure:** attempts 1, 2, and 3 all pass the guard; blocking occurs after the fourth failure.

**Fix:** Define whether `attempts` counts initial execution or rework executions, then use one
transition function everywhere. With the present wording, increment and block when
`attempts >= max_attempts` before another implement dispatch. Add boundary tests for 0, N-1, N, N+1.

### 11. Generic rejection assumes every gate owns a TASK.md

**Evidence:** reject always increments `attempts` in `TASK.md` (`skills/reject/SKILL.md:19-24`), but
phases, task decomposition, phase close, and PR triage can all be gated without a task owner.

**Failure:** rejecting a phase-level gate either edits an unrelated task, has no target, or cannot
record a retry budget. The rejection route is also gate-specific, so a generic "re-dispatch the step"
is insufficient.

**Fix:** Put retry count and rejection route on the proposed gate record. Task gates may mirror the
count into TASK.md for reporting, but phase/project gates must not invent a task owner.

### 12. Planning backfill is retroactive and can legitimize unreviewed code

**Evidence:** task explicitly says that when IMPLEMENTATION/QA/REVIEW exist past a planning gap,
preflight backfills plan and design but does not re-run implement (`skills/task/SKILL.md:65-69`).

**Failure:** A design written after the code can rationalize the existing implementation. Once the
gap is filled, existing downstream artifacts can advance the task even though implementation was not
performed against the approved design.

**Fix:** Backfill may recover documentation, but it must mark implementation and every later artifact
stale. After the design gate, require implement reconciliation against the new design, followed by
fresh QA and review. If preserving manual work is desired, add an explicit adoption step that produces
a diff and deviations rather than silently treating it as compliant.

### 13. Branch/base synchronization and PR adoption are incomplete

**Evidence:** preflight uses `git rev-list --count @..@{u}` but does not define how the base branch or
upstream is discovered (`skills/task/step-preflight.md:27-36`). The current task branch has no upstream,
which demonstrates that this command can fail in normal local state. Push rejection rebases onto the
base rather than the remote task branch (`skills/task/step-push.md:21-27`). PR adoption queries only the
default open set (`skills/task/step-push.md:29-39`).

**Failure:** local-ahead/diverged base state can pass an ahead-only count; missing upstream is not
mapped cleanly; a non-fast-forward against an existing remote task branch remains non-fast-forward
after rebasing only onto base; and a closed PR can be missed, allowing a second PR for the same branch.

**Fix:** Configure `base_branch` during init and verify it against the remote default. Fetch first,
then use `git rev-list --left-right --count base...origin/base`. For an adopted task branch, fetch and
rebase/merge against `origin/<task-branch>` according to policy. Query `gh pr list --state all --head`
and define reopen/new-PR behavior for closed or merged matches.

## Schema, state, and validation inconsistencies

### 14. Required runtime state is absent from artifact schemas

**Evidence:** workflows write/read `blocked_reason`, but the catalogue and templates do not add it to
parkable artifacts (`REQUIREMENTS.md:559-587`, `templates/TASK.md`). Decisions use `status: active`
(`templates/DECISION.md:4`) although the global status vocabulary excludes `active`
(`REQUIREMENTS.md:319-335`). Accepted phase gaps and stored gate summaries likewise have no schema.

**Failure:** A correctly blocked or approved artifact cannot be both fully expressive and conformant.
Status may depend on fields that validators consider undeclared, while invalid enum values can remain
undetected.

**Fix:** Model common optional state explicitly: `blocked_reason?`, `blocked_detail?`, and a gate
reference on artifacts that can park. Either add `active` to the status vocabulary for decisions or
give decisions a separate vocabulary. Add the accepted-gap closure fields described in finding 6.
Make every field name its consumer.

### 15. `status` promises frontmatter-only reads but needs configuration body values

**Evidence:** status says it reads frontmatter only, while it consumes gate modes and
`require_merged_deps` from config (`skills/status/SKILL.md:21-32`). Those values live under body
headings in the config template, not YAML frontmatter (`templates/config.md:1-40`).

**Failure:** Literal compliance prevents status from reading the values it claims to use. Ignoring the
rule makes its context contract false and inconsistent with other orchestrators.

**Fix:** Exempt config.md explicitly from the frontmatter-only rule, or move machine-consumed config
into YAML/frontmatter/a structured config file. Prefer one parser and one typed configuration model.

### 16. The checks validate examples, not composed runtime dispatches

**Evidence:** `check-envelopes.py` scans static uppercase fields starting at literal `ROLE:` blocks and
checks field presence/classes only (`scripts/check-envelopes.py:45-109`). It does not validate field
order, values, referenced role/skill/template existence, module lookup, PATHS, WRITE ownership, or the
actual prompt composed during a workflow. `step-resolve.md` passes because it contains no envelope.

**Failure:** "all envelopes conform" can be true while an executable dispatch is missing or malformed.

**Fix:** Represent envelopes as structured data and render them, rather than composing prose at
runtime. Validate the rendered envelope immediately before dispatch. Extend dev checks to verify
referenced files, role/skill existence, one WRITE owner, module/PATHS consistency, and exact order.

### 17. Workspace template validation is weaker than template validation

**Evidence:** `check-templates.py --target` checks only missing frontmatter keys and missing headings
(`scripts/check-templates.py:130-160`). It does not reject extra keys/headings, wrong order, invalid
enum values, empty required sections, table columns, or id/reference mismatches. The current workspace
scan is knowingly red with 19 historical failures, so it is excluded from the gate by D-030.

**Failure:** drift in produced artifacts can pass; meanwhile a permanent red baseline makes genuine
new failures easy to normalize as historical noise.

**Fix:** Use the same strict checks in template and instance modes, with explicit migrations or a
machine-readable grandfather list keyed by path and exact known violation. A new or changed violation
must fail. Add value, section-content, table-shape, and id-chain checks.

### 18. The configured test chain omits most repository checks

**Evidence:** `.orqestra/config.md:33` runs three commands only. It omits the template checker test
harness, decision checker, step-reference checker, and step-reference test harness. The repository
contains seven relevant checker/test commands.

**Failure:** regressions in omitted controls can merge while the configured suite is green. Chaining
with `&&` also hides later results after the first failure.

**Fix:** Add one `scripts/check-all.py` runner that executes every check, reports all results, and exits
nonzero if any fail. Keep the historical workspace scan separate but explicit until migrated.

## Lower-severity usability and consistency problems

### 19. Fresh init and greenfield disagree about the default PRD path

**Evidence:** init creates `.orqestra/PRD.md`, while greenfield falls back to repository-root `PRD.md`
unless `prd_path` is configured (`skills/greenfield/SKILL.md:23-27`). The distributed config template
has no `prd_path` (`templates/config.md`). The dogfood workspace has a manually added value, which
masks the consumer-project failure.

**Fix:** Put `prd_path: .orqestra/PRD.md` in the generated configuration and have init/greenfield read
the same single source. Add an empty-repository integration test: init, edit seeded PRD, greenfield.

### 20. The promised PROJECT.md enrichment has no design write contract

**Evidence:** init creates an honest PROJECT.md stub and says layout, conventions, testing, and traps
are filled by the first design (`skills/init/SKILL.md:115-129`). The PROJECT template and catalogue
also assign that ownership to design (`templates/PROJECT.md:23-25`, `REQUIREMENTS.md:566`). However,
design's output contract lists DESIGN.md and optional decision files only
(`skills/design/SKILL.md:37-42`), while its dispatch envelope has a single DESIGN.md WRITE target
(`skills/greenfield/step-plan-design.md:41-57`).

**Failure:** PROJECT.md remains a stub, or the first design agent edits outside its declared write
boundary. Later agents trust a globally loaded file whose promised discovery step never happened.

**Fix:** Add a dedicated project-discovery/enrichment dispatch during the first design with PROJECT.md
as its sole output, or explicitly model a validated multi-target transaction. Do not hide a second
artifact owner behind the DESIGN.md dispatch.

### 21. Multi-artifact writers conflict with the one-WRITE-path contract

**Evidence:** design and clarify may write decision files and regenerate the decisions index in
addition to their main artifact, while dispatch envelopes expose one WRITE target and generic agent
rules require one artifact. `create-tasks` similarly writes an index plus many task files.

**Failure:** either the writer violates its envelope, or required secondary artifacts/index updates do
not occur. Tool restrictions also make index regeneration via edit unreliable.

**Fix:** Make compound operations explicit transactions with a declared write set, or split them into
one dispatch per artifact followed by a deterministic index generator. The latter is easier to audit
and retry idempotently.

## Proposed implementation roadmap

1. **Runtime viability:** complete the tool-field correction, make bug intake/reproduce dispatchable,
   and add same-turn integration tests.
2. **State generations:** create task branches before work; add revision/commit correlation; invalidate
   downstream artifacts on rework.
3. **Typed gates:** add a gate artifact and gate-specific handlers; repair phase accepted-gap and gap
   task flows.
4. **GitHub delivery:** replace review-thread fetching, harden base/branch/PR adoption, and dispatch PR
   comment fixes by module.
5. **Contract consolidation:** correct schema vocabularies, make config machine-readable, strengthen
   runtime envelope and artifact validation.
6. **Fresh-project path:** align PRD defaults and give PROJECT.md a real owner.

## Verification performed

- `claude plugin validate .` — passed.
- Python compilation of all checker and checker-test scripts — passed.
- `scripts/test-check-templates.py` — 15 cases passed.
- `scripts/test-check-envelopes.py` — 25 obligation cases passed.
- `scripts/test-check-step-refs.py` — 28 cases passed.
- `scripts/check-envelopes.py` — 10 static envelopes passed.
- `scripts/check-step-refs.py` — 43 references passed.
- `scripts/check-decisions.py --target .orqestra` — 31 decisions passed.
- `scripts/check-templates.py --target .orqestra` — failed on 19 known historical artifacts, as
  documented by D-030.

These results show that the present static examples and narrow schemas are mostly internally
consistent. They do not contradict the runtime and state-machine failures above; several findings are
specifically outside what those checks inspect.


**VERY IMPORTANT!!! EVERY STEP HAVE TO BE DISPATCHED TO SUBAGENT FROM ORQESTRA!!!!!**