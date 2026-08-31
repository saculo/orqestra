---
id: TASK-040
type: review
status: done
updated: 2026-08-31
task: TASK-040
verdict: passed
lenses: [correctness, design]
required: []
review_round: 1
---

## Verdict

**Passed.** All five acceptance criteria are met against their amended text, the floor is clean, and
the four `Constrains` of D-029 are each discharged by a named component. The sharpest question here
was whether master went green because the defect is fixed or because the checks do not look: for
AC-1 it is the former, and qa proved it adversarially rather than asserting it — the extra-key probe
(`foo:` → exit 1, `frontmatter not in catalogue`) shows `check-templates.py:192-197` compares key
sets in both directions, so the green run genuinely detects both a missing `module` and an
over-fix. For AC-2 it is neither: no check looks, and the diff says so in four places rather than
letting a green suite imply otherwise. Three minor findings, none required.

## Findings

| id | severity | file:line | finding |
|---|---|---|---|
| F-1 | minor | `.orqestra/phases/PHASE-1/tasks/TASK-040/IMPLEMENTATION.md:83` | The recorded deviation names `TASK-001/REVIEW.md` and `TASK-009/DESIGN.md` as the `--target .orqestra` failures. **Nineteen** artifacts fail, across `TASK-001`…`TASK-010` (qa's I-2, independently confirmed). The material claim — pre-existing, untouched by this change — holds and was verified by worktree diff, so this is not an unrecorded deviation and does not fail floor check 2. It is a wrong figure in a shipped artifact of the exact kind a follow-up inherits as a scope estimate, which is why it is a finding rather than a note; it is minor because `QA.md` ships the correction alongside it. |
| F-2 | minor | `skills/bugfix/step-intake.md:50-56` | `## Report` shows only the success line. Step 4 at `:34-35` creates a second terminal branch — the human abandons the question, the workflow ends having written nothing "and says so" — and that branch has no prescribed shape. A fresh agent reaching it has to invent the output, which is the failure the report blocks exist to prevent. Does not breach AC-2, which asks only that intake not block, and it does not. |
| F-3 | minor | `skills/bugfix/step-diagnose.md:64` vs `:41-53` | "Carry a `MODULE` line in the gate block whenever the two differ, naming the old value and the new" is stated eleven lines below the gate block it governs, in a section `## The gate` does not point at, and the block itself shows no such line and no rendering of one. The block at `:41-53` is the artifact an agent copies; per `claude-expert`, the rule belongs where the mistake would be made. AC-4 is satisfied without it — the correction path is stated, and stating it is what D-029's third obligation asks. |

## What Would Change This Verdict

_n/a_

## Notes

**Floor check 1 — `.orqestra/config.md` holds, and not for the reason first given.** The file is
outside this task's `PATHS` and belongs to **no** module (`modules.md:45-47`), so the edit crosses no
other module's boundary, is attributed to no other module's reviewers, and the §8.2 human decision
that folded AC-5 here stands. Recording explicitly that this conclusion survives a false premise: the
original AC-5 comment justified it with *"config.md is `plugin`"*, which is wrong, and the later
amendment comment corrects it in terms. I reached the same conclusion from `modules.md` directly
rather than inheriting it. The remaining diff files are the pipeline's own artifacts under this
task's directory and the seven source files, all inside `PATHS`.

**The design lens on AC-2 — the call is right, and §7.0.1 is the reason.** The orchestrator's framing
was *say so and detect instead*. §7.0.1's actual standard is narrower: name which of the four layers
binds, and where none does, state it plainly rather than paper it over; its own worked example — the
orchestrator's `Write`/`Edit`, "the weakest guarantee in the system and now labelled as such" — ships
with **no** detection at all, and its hardening is explicitly optional and deferred *"once there is a
run to test it against"*. This task did strictly more than that precedent: it names the gap in
`DESIGN.md`'s `## Decisions`, in `IMPLEMENTATION.md`'s tech debt, in `QA.md`'s I-1, and — the one
that matters, because it is the only one a future editor of the step will read — inline at
`step-intake.md:36-37`: *"An empty value passes `check-templates.py`; this instruction is the only
thing that catches it."* It also enumerates three concrete layers with a reason each is not now, and
applies the mitigation available at this altitude by stating the rule at both the gather step and
the write step. So the answer to *is there detection, or only a statement?* is: only a statement —
and that is the correct outcome here, because each detection layer is a `scripts/` change no AC asks
for, and building one would be the speculative scope the step forbids. This is not the project
talking itself into an unenforced guarantee; the guarantee is disclaimed in the same breath it is
stated, which is the opposite failure mode.

**D-029's four `Constrains`, against the seven components.** (1) *Every `BUG.md` carries `module:`;
intake may not create without one nor fall back to `## Scope`* — C-1 (`templates/BUG.md:6-7`) holds
the schema side and is machine-detected; C-3 (`step-intake.md:16-37`) holds the workflow side and is
prose-only, honestly labelled. (2) *`## Scope` stops carrying the module* — C-2
(`templates/BUG.md:23-26`), genuinely discharged: `grep -n module templates/BUG.md` hits the key and
a pointer *to* the key, and the two `## Scope` mentions in `skills/bugfix/` both say it does not name
the module. This is silence, not merely absence of contradiction. (3) *Diagnose and promote read,
never re-derive; amend the BUG when the fix lands elsewhere* — C-5 (`step-diagnose.md:7-10`, `:59-74`)
and C-6 (`step-promote.md:15`, `:22-24`), with C-4 (`step-reproduce.md:7-9`) covering reproduce, which
D-029's *Why* names among the four re-derivers though its `Constrains` does not. (4) *Future scope
units state whether they carry `module:`* — binds future tasks; nothing to discharge here, and the
design saying so is a correct reading rather than an omission. **Only apparently discharged: none.**
The nearest candidate is (3)'s amendment path, which is stated but cannot be executed — no actor in
the `bugfix` workflow holds a tool that can amend `BUG.md`. That gap is pre-existing, identical for
intake's own creation, and disclosed under §7.0.1 at `step-diagnose.md:70-74`; stating the rule
without the capability is the right split, since the rule is what a future task implements against.

**D-029 now contradicts shipped behaviour, sanctioned.** `step-intake.md:31-35` forbids what D-029's
first `Constrains` bullet permits — *"or intake blocks (D11)"*. Floor check 4 does not fire: the
contradiction was settled by human decision under §8.2 on `TASK.md`, with a reason I find sound (no
value in §4.4.3's closed list fits an incomplete input, and a `blocked` `BUG.md` would need the very
`module:` that is missing, passing the checker while violating D-029 in one stroke). D-029 lives in
`docs`; amending it here would breach D14. Correctly left, and recorded by both `IMPLEMENTATION.md`
and `QA.md` (I-4). Per D9 I cite rather than re-litigate.

**The follow-ups exist only as prose.** `DESIGN.md` says the three enforcement layers are named "so a
future task can pick it up rather than rediscover it" — but nothing routes anyone to them. Five
items now live as tech-debt prose: the three detection layers, the D-029 amendment, and the
`BUG.md` capability gap. Outside this task's ACs and outside anything rework could fix, so a note:
worth `create-task` entries before the phase closes, or the rediscovery the design set out to
prevent happens anyway.

**On the rest of the diff being green for the weaker reason.** Checked and clear. AC-3's heading
survival is caught by `check-templates.py`'s ordered heading comparison; AC-5 is verified by numstat,
an md5 on line 33, and a grep, all real. AC-4 is the one where a green run could have misled, and
`QA.md` refuses the inference in terms — `check-envelopes.py` "keys on the scope key and never reads
frontmatter", so exit 0 is a no-regression signal and not evidence. The evidence offered instead is
the trace `step-diagnose.md:7` → `templates/BUG.md:6` → §4.8.1:584, which closes. The three
`test-check-templates.py` cases that flipped are the three asserting `code == 0`; both artifacts read
the failure text rather than counting, which is the right discipline.

**`templates/BUG.md:7` says "a bug without one is not creatable"** — an impossibility phrasing for
something nothing makes impossible. Not a finding: it quotes D-029's own wording (cite, do not
re-argue), and the reader who follows the workflow meets the honest version at
`step-intake.md:36-37`. Noted because if the template comment is ever read on its own, it is the
shape §7.0.1 was written to correct.
