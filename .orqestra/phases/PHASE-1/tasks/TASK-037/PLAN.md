---
id: TASK-037
type: plan
status: done
updated: 2026-08-31
task: TASK-037
---

## Approach

**The finding: the obligation is right, the warrant under it is false.** §5.5:957 and §5.1.1:795 do not
merely assert that a `BUG` carries `module:` — they offer that as the *reason* the conditional class is
mandatory under `BUG`. The reason is false. The rule it justifies is not: `check-envelopes.py` keys on
the **scope key**, never on frontmatter (line 90, `scope = scopes.pop()`), so nothing in the enforcement
path reads `BUG.md` at all. This reframing is what makes AC-1 satisfiable without disturbing D-027,
whose settled rule — the scope key alone decides the class — is cited, not re-opened (D9).

**Where `api` comes from in `skills/bugfix/step-diagnose.md:12`, traced.** A human types it, and the
workflow re-derives it; no frontmatter key is involved at any point:

| where | what happens to the module | form |
|---|---|---|
| `skills/bugfix/step-intake.md:13` | gathered from args or `AskUserQuestion` — "**Where it surfaces** — which module, **if known**" | human input, optional |
| `templates/BUG.md:21` | written to `## Scope` — "which module the symptom surfaces in" | body prose |
| `skills/bugfix/step-intake.md:26` | echoed in the report line — `surfaces in api` | display |
| `skills/bugfix/step-reproduce.md:7` | "Identify the module from the symptom, and load its expertise skills" | re-derived by the orchestrator |
| `skills/bugfix/step-diagnose.md:12` | composed into `MODULE:`; `PATHS`/`STACK`/`EXPERTISE` then come from that row in `modules.md` (§5.1, D-004) | envelope |
| `skills/bugfix/step-promote.md:15`, §7.3:1210 | **first** becomes a frontmatter key — `module: api`, "where the fix lands", on the `TASK`, not the `BUG` | frontmatter |

So resolution **(b)** is available and the source is concrete: the reporter states it at intake, it
lives in `BUG.md` `## Scope`, the workflow confirms it from the symptom at reproduce, and it becomes a
`module:` key only at promote — on the task the bug becomes. §7.3.1:1221 already says this in the words
the spec needs ("routing comes from *where the fix lands*"), which is why (b) needs no new concept.

**Recommendation, for `design` to accept or overturn — it makes the call, not this plan (TASK.md Out of
Scope).** (b), because the spec's own rigor bar rules against (a) more than it rules for it: §5.5:965
requires every condition to be "answered by something the orchestrator has already read to route the
dispatch", and the orchestrator has already read the module at reproduce. Adding `module:` to `BUG.md`
would add a frontmatter field whose only consumer is a check that does not read it — precisely the Rule
B (§4.4.1) failure that removed `task_type` (D-011). (a) remains defensible if design judges that a
diagnosed bug's module should be machine-readable before promotion; if it chooses (a), **this task
splits and docs leads (D-019)** — see Risks for the three edits and their modules.

## Affected Areas

Inside `docs` (`REQUIREMENTS.md`, `README.md`) — the only files this task may edit:

| file:line | what is there | in scope |
|---|---|---|
| `REQUIREMENTS.md:957` | §5.5 conditional row — "mandatory **iff** the scope key is `TASK` or `BUG` — those units carry `module:` in their frontmatter" | yes, under both (a) and (b) |
| `REQUIREMENTS.md:795` | §5.1.1 — "a `BUG` carries `module:` too, so §5.5's conditional class is mandatory there as well" | yes, under both |
| `REQUIREMENTS.md:584` | §4.8.1 `BUG.md` row, frontmatter-additions cell `bug severity` | **only under (a)**; it matches `templates/BUG.md` exactly today |
| `REQUIREMENTS.md:739` | §5.1 — "Every **task** carries `module:`" | correct as written; the set-difference baseline for AC-4 |
| `REQUIREMENTS.md:1221-1232` | §7.3.1 — routing comes from where the fix lands; `module:` shown on the promoted task | correct; the anchor (b) cites |
| `REQUIREMENTS.md:1210` | §7.3 — promote takes "module from the touched area" | correct; consistent with (b) |
| `README.md` | grepped for the claim — no occurrence | no |

Read and verified, **outside** this task's paths (read-only reconnaissance, no edit planned):
`templates/BUG.md` (frontmatter is `id type status updated bug severity`; `## Scope` holds the module as
prose), `skills/bugfix/step-intake.md`, `step-reproduce.md`, `step-diagnose.md`, `step-promote.md`,
`scripts/check-envelopes.py`, `.orqestra/decisions/D-027-project-is-a-scope-value.md`.

**Is the check enforcing something unsatisfiable? No — it is met, and met honestly.**
`step-diagnose.md:8-23` carries all seven `ALWAYS` fields, exactly one scope key (`BUG:`), and all four
conditional fields; it is the only `BUG`-scoped envelope in `skills/` (`grep '^BUG:'`, one hit). It
therefore passes `check(...)` today. The rule is satisfiable and satisfied; what is unchecked is not the
envelope but the **provenance** of the four values — nothing verifies that `api` came from anywhere.
That is the gap AC-2 names, and it is a documentation gap, not a broken check.

**§4.8.1:584 under D-028.** D-028 governs the `Written by` column only. That cell reads `` `bugfix`
intake `` — workflow-plus-step, the form D-028 prescribes for a step that writes inline rather than
dispatching, and `step-intake.md` contains no `ROLE:` envelope (`grep ROLE:` is D-028's own test, and it
is empty there). **The cell is correct and out of scope.** The frontmatter-additions cell is a different
column that D-028 does not govern; it is in scope for this contradiction only under (a).

## Risks

- **Under (a) this task cannot complete alone.** `orqestra-conventions` makes a schema change three
  edits always together (D-003): §4.8.1:584 (`docs`), `templates/BUG.md` (`plugin`), and the skill that
  writes it, `skills/bugfix/step-intake.md` (`plugin`) — verified as the writer; nothing else copies
  that template. Two of three are outside `PATHS`, so (a) is `needs-splitting`, docs first (D-019).
  Shipping only the §4.8.1 row would leave the schema broken in the exact way D-003 exists to prevent.
- **Under (a), `step-intake.md`'s "if known" becomes a contradiction.** A mandatory frontmatter key
  cannot be sourced from an optional interactive answer, and `## Scope` in `templates/BUG.md` would then
  duplicate a frontmatter field — the "rule written in two places" failure `orqestra-conventions` warns
  about. Design must resolve both if it chooses (a); neither is visible from `REQUIREMENTS.md` alone.
- **Under (b), a plugin tail remains and AC-3 will surface it.** `scripts/check-envelopes.py:16-19`
  restates the false warrant in its docstring ("those units carry no `module:` in their frontmatter"),
  as does the line 47 comment. The code stays correct; the comment becomes wrong. `scripts/` is
  `plugin`, so under (b) too this is a follow-up — small, but it is the same restatement-drift that
  produced this contradiction.
- **The premise is older than TASK-029 and reached a decision file.** `TASK-015/DESIGN.md:52` already
  asserted "`TASK.md`/`BUG.md` frontmatter carries `module:`"; TASK-029 hardened it, TASK-030 encoded
  it, TASK-033 repeated it. `D-027`'s own **Why** (line 18) and **Constrains** (line 28-29, "must state
  in §4.8 whether its frontmatter carries `module:`") carry the false clause. A `REQUIREMENTS.md` fix
  that leaves D-027 reading the old warrant recreates the drift on the next task that cites it.
- **AC-4's set-difference has a second axis.** Beyond grepping the phrase, the enumeration to diff is
  §4.8.1's per-artifact frontmatter cells against the actual `templates/*.md` files — a row/template
  mismatch of this kind is by construction invisible to a grep for the claim's wording.

## Open Questions

1. **(a) or (b)?** `design` decides and records the reason (TASK.md Out of Scope). This plan recommends
   (b) and traces the module's real source; it does not decide. If (a), design must also return
   `needs-splitting` and name the `plugin` follower.
2. **Does correcting the warrant require a new decision, or amend D-027?** D-027's *rule* stands
   untouched under (b), but its Why and Constrains state the false reason. A decision file's text is not
   normally rewritten; the clean route is a corrective `D-029` that supersedes nothing and restates the
   warrant. `.orqestra/decisions/` belongs to no module, and `design` writes decisions — so this is
   answerable at design, but a human should confirm that a factually-wrong **Why** is corrected by a new
   decision rather than by editing D-027 in place.
3. **Should the module become mandatory at intake regardless of (a)/(b)?** Today it is "if known", so a
   `BUG` can exist with no module at all, and `step-diagnose.md` would then have nothing to put in
   `MODULE:` — an envelope the checker rejects. Neither resolution addresses this by itself. It may be
   the real defect behind the contradiction, and it lands in `plugin`.
