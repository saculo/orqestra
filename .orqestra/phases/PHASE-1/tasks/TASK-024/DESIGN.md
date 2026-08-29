---
id: TASK-024
type: design
status: done
updated: 2026-08-29
task: TASK-024
decisions: [D-026]
---

## Components

| # | component | responsible for | serves |
|---|---|---|---|
| 1 | **The reference-shape convention** | One rule that decides how any reference to a step file is written, keyed on how the *containing* file is loaded. Recorded as D-026; it is what makes AC-2's "deliberately and consistently" checkable rather than a matter of taste. | AC-2 |
| 2 | **The three broken index rows** | `add-phase`'s `tasks` and `plan-design` rows and `bugfix`'s `plan-design` row name `greenfield`'s real files under the convention. | AC-1, AC-2 |
| 3 | **The six prose references** | The prose that names a step file living in another skill is made true under the same convention — `add-phase/SKILL.md:33`, `bugfix/SKILL.md:36`, `qa/SKILL.md:35`, `implement/SKILL.md:46,103`, `task/step-preflight.md:59`, and `greenfield/step-plan-design.md:3`'s claim about who shares it. | AC-1, AC-2 |
| 4 | **The reference checker** | Collects every step reference across `skills/`, resolves each, and fails when the target does not exist or the shape is wrong. Its input is the set of references; the filesystem is consulted only to answer "does this exist". | AC-1, AC-3 |
| 5 | **The checker's test harness** | Proves the checker *notices* — including the two failure modes PLAN named: an inverted check that reads files instead of references, and a pattern that matches only the bare shape. | AC-3 |

Component 3 exists because the human answer to PLAN's Q1 is the wide reading. It is not extra
surface: leaving those lines alone would force the checker to carry a prose exemption, and an
exemption is exactly where a false negative hides.

## Interfaces

### What counts as a step reference

A **step reference** is an inline-code span (single backticks) in a Markdown file under `skills/`,
outside fenced code blocks and outside HTML comments, whose *entire* span content matches:

```
(\$\{CLAUDE_PLUGIN_ROOT\}/)?([A-Za-z0-9._-]+/)*step-[a-z0-9-]+\.md
```

Backticks are the whole discriminator, and they are safe to lean on: house style already
code-spans every filename, and every one of the 39 existing occurrences is backticked. Requiring
them turns "is this prose talking about a file?" — the judgement call that makes prose matching
dangerous — into a lexical test.

**The checker must NOT flag any of these.** The list is closed and belongs in the script's docstring,
because a checker that cries wolf gets ignored, which is the failure this task exists to remove:

| not a reference | why |
|---|---|
| an unbackticked occurrence in a sentence | it is prose about a file, not a path |
| a span containing `*`, `<`, `>` (`step-*.md`, `step-<name>.md`) | naming the *convention* (D-007), not a file |
| a span naming a non-`step-` file (`SKILL.md`, `templates/DESIGN.md`, `config.md`) | other reference classes; this task is step files |
| anything inside a ``` fence or an HTML comment | examples and handoff transcripts name files that need not exist |
| anything outside `skills/` | `agents/`, `templates/`, `.orqestra/` are not scanned |
| a `step-*.md` file that nothing references | an orphan is a different check — inverting this one is the named risk |

Stripping fences and comments is the same preprocessing `check-templates.py` already does before
reading headings; reuse the approach, not the code.

### Resolution

| the span | resolved against |
|---|---|
| starts `${CLAUDE_PLUGIN_ROOT}/` | the plugin root — the checker substitutes its own `ROOT`, never the environment |
| contains `/`, no variable | the plugin root |
| no `/` | the directory of the skill whose file contains it |

The checker substitutes rather than expands because `${CLAUDE_PLUGIN_ROOT}` is a *runtime* mechanism
it cannot observe (PLAN's fifth risk); `ROOT` derived from `__file__` is the same root by
construction.

### Findings

Two kinds, both reported as `skills/<skill>/<file>:<line>` plus the span text:

- **missing** — the resolved path does not exist. This is AC-1.
- **shape** — the reference resolves but is written in the wrong form for where it sits. Two rules
  only: a reference on a table row (the line begins with `|`) that contains `/` must carry the
  variable; a reference anywhere inside a `step-*.md` must not. This is AC-2's consistency, and
  without it the next person picks a shape at random.

### CLI contract

Matches the existing four exactly (PLAN's approach section): CPython 3, stdlib only, `ROOT` from
`__file__`, `--verbose`, findings collected then printed, and a docstring stating why the check
exists and that it is dev-only with no runtime dependency from the plugin (D-001, D-015).

| exit | condition |
|---|---|
| 0 | every reference resolves and conforms |
| 1 | at least one finding |
| 2 | `skills/` unreadable, **or zero references found** — as in `check-envelopes.py`, finding nothing means the convention moved, not that the tree is clean |

## Structure

Everything lands in two areas of the `plugin` module, and in this order.

**`skills/` — the references themselves.** Two layers, and the convention differs between them
because the loading mechanism differs (D-026):

- A `SKILL.md` body is loaded by *invocation*, so `${CLAUDE_PLUGIN_ROOT}` is expanded before the
  agent sees it (D-025). A step-index `file` cell is consumed directly as a `Read` argument, so a
  cross-skill cell carries the variable and arrives absolute. Same-skill cells stay bare — twenty
  rows are already correct and the variable would be noise on them.
- A `step-*.md` is loaded by `Read`, where the variable arrives **literal** (D-025). A qualified
  path there is inert text. Cross-skill references in a step file are therefore plugin-relative,
  which is why `task/step-preflight.md:59` is already the right shape and stays as it is.
- Prose in a `SKILL.md` that cites another skill's step file is plugin-relative too. It is a
  citation, not a `Read` argument, and `${CLAUDE_PLUGIN_ROOT}/skills/task/step-push.md owns git`
  buys nothing over `skills/task/step-push.md owns git` and costs the sentence.

Nothing in `agents/`, `templates/`, or `.claude-plugin/` is touched. No `REQUIREMENTS.md` row is
needed — `check-envelopes.py` and `check-decisions.py` have none — which is what keeps the whole
change inside one module (D2).

**`scripts/` — the checker and its twin.** The checker is a peer of the existing four, not a layer
above them: it imports nothing from them and shares no helper module. Four small scripts that each
read a different source of truth are easier to keep honest than one framework, and there is no
package here to import from.

**Order, and it is load-bearing.** Write the checker and its harness *before* correcting any
reference, and observe it exit 1 naming exactly the three broken rows on today's tree. A checker
first seen on a green tree is a checker nobody has watched fail, and the inverted implementation —
glob `skills/*/step-*.md`, look for a row — passes today's tree silently. Then correct the
references; then the same command exits 0.

## Decisions

**D-026 — a cross-skill reference's shape follows how its file is loaded.** Recorded as a decision
file: it binds every future step file and every future skill, not just this task.

**The prose is corrected, not exempted (PLAN Q1, human-answered).** The alternative — a checker that
skips prose — makes the three most-cited cross-skill references permanently unverified, and an
exemption clause is where the next broken reference will live. Six edits once is cheaper than a
standing blind spot.

**Backticks are required for a match.** This is the decision that makes the wide reading safe. An
unbackticked `step-push.md` in a sentence is not a reference and is not flagged. The cost is a real
reference written without backticks going unchecked; that is a false *negative*, recoverable by
adding backticks, whereas a false positive trains people to ignore the check (the TASK-008 argument
about unearned confidence, applied to noise instead of coverage).

**Pattern forms are excluded by the presence of `*`, `<`, or `>` in the span.** D-007's subject
matter is the naming convention itself, and text about it will keep appearing in `skills/`.
Excluding on a character class rather than on context means no judgement call at the call site.

**`greenfield/step-plan-design.md:3` is corrected to name `bugfix` (PLAN Q3, human-answered).** That
line is a factual claim about *who references the file* — it is metadata about the sharing, not the
step's content, so TASK.md's out-of-scope line does not reach it. Leaving it would ship a file whose
first sentence contradicts the reference this task adds.

**Orphan step files are explicitly out of scope.** AC-1 is about references resolving. A file with
no reference is a different defect with a different fix, and conflating them is what produces the
inverted checker.

**`greenfield/step-tasks.md`'s phase selection is not touched.** It gates on the first phase not
`done` and mentions `PHASE-1`; whether that is right for `add-phase` is the step's *content*, which
TASK.md excludes. Flagged in the harness's docstring, not fixed.

**`.orqestra/project/PROJECT.md` stays stale.** It calls `check-templates.py` "the only automated
check" and was already wrong before this task. It belongs to no module and is not editable from
`plugin`'s paths.

## Test Strategy

A `test-check-*.py` twin (PLAN Q2, human-answered), following `test-check-templates.py`: each case
runs the real script as a subprocess against a throwaway copy of `skills/` plus the script, so a case
can break an input without touching the working tree. Cases assert on exit code and on output text.

| case | proves |
|---|---|
| clean tree exits 0, and the reported reference count matches a count taken independently in the test | AC-1 — the checker is looking at something. A checker that matches nothing also exits 0 |
| delete a step file that a **bare same-skill** row names → exit 1 naming that `file:line` | AC-1, the ordinary path |
| delete `greenfield/step-plan-design.md` → exit 1 naming **`add-phase`'s and `bugfix`'s rows** | The named two-shape risk. A regex matching only the bare form skips exactly the rows this task adds, and this case is the only thing that catches it |
| rewrite an index cell to `step-nope.md` → exit 1 | AC-1 from the reference side |
| add an unreferenced `step-orphan.md` → still exit 0 | The inversion guard. An implementation that globs files fails here |
| fixture prose containing `step-*.md`, `step-<name>.md`, an unbackticked `step-push.md`, a fenced example naming `step-imaginary.md`, and an HTML comment naming another → exit 0 | The no-false-positive contract, one case per excluded form |
| a `step-*.md` containing a `${CLAUDE_PLUGIN_ROOT}`-qualified reference → exit 1, shape finding | AC-2 — the variable is inert under `Read` (D-025) |
| a table row containing a bare `skills/x/step-y.md` → exit 1, shape finding | AC-2 the other way |
| remove `skills/` → exit 2, no traceback; a `skills/` with no references → exit 2 | AC-3 robustness, matching `check-envelopes.py` |

AC-2 and AC-3 are additionally proven on the real tree, not only on fixtures: after the edits,
`python3 scripts/check-<name>.py --verbose` exits 0 and lists the three formerly-broken references
as checked, and `python3 scripts/test-check-<name>.py` exits 0. Both must be recorded in QA with
their actual output — the reference count is the number to read, because it is the one that silently
goes to zero.
