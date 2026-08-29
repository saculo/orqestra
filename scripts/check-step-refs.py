#!/usr/bin/env python3
"""Conformance check that every step-file reference in skills/ resolves, and is written in
the shape D-026 dictates for where it sits.

A step file named in a SKILL.md index table is a navigation instruction: D-007 puts step
*order* in that table, so a wrong path there is a dead end at exactly the moment a workflow
needs to advance. Three such rows were dangling before TASK-024 — `add-phase`'s `tasks` and
`plan-design` rows and `bugfix`'s `plan-design` row named local filenames for files that live
in `greenfield` — and nothing noticed, because nothing looked.

The check walks REFERENCES → filesystem, never the reverse. Listing `skills/*/step-*.md` and
looking for a row that names each one inverts it: every one of those three broken rows would
have passed, because the files they should have named do exist. An orphan step file that
nothing references is a different defect and is deliberately NOT reported here.

WHAT COUNTS AS A REFERENCE

An inline-code span (single backticks) whose *entire* content matches:

    (${CLAUDE_PLUGIN_ROOT}/)?(<dir>/)*step-<name>.md

Backticks are the whole discriminator. House style code-spans every filename, so requiring
them turns "is this sentence talking about a file?" — the judgement call that makes scanning
prose dangerous — into a lexical test. The cost is a real reference written without backticks
going unchecked: a false negative, fixed by adding backticks. A false positive would be worse,
because a checker that cries wolf gets ignored, which is the failure this check exists to
remove.

The exclusion list is closed:

    an unbackticked occurrence in a sentence   prose about a file, not a path
    `step-*.md`, `step-<name>.md`              names the naming CONVENTION (D-007), not a
                                               file; `*`, `<`, `>` cannot match the pattern
    `SKILL.md`, `templates/DESIGN.md`          other reference classes; this check is step files
    anything inside a ``` fence                examples and transcripts name files that need
                                               not exist
    anything inside an HTML comment            same, plus design rationale
    anything outside skills/                   agents/, templates/, .orqestra/ are not scanned
    a step-*.md nothing references             an orphan; inverting this check is the risk above

RESOLUTION

    starts ${CLAUDE_PLUGIN_ROOT}/   the plugin root
    contains / , no variable        the plugin root
    no /                            the directory of the skill whose file contains it

The variable is SUBSTITUTED, not expanded: `${CLAUDE_PLUGIN_ROOT}` is a runtime mechanism this
script cannot observe, and ROOT derived from __file__ is the same root by construction.

FINDINGS

    missing   the resolved path does not exist                                    (AC-1)
    shape     it resolves, but is written wrong for where it sits (D-026)         (AC-2)

Two shape rules, and only two, chosen so they cannot overlap — index tables live in a SKILL.md
(D-007), so the first rule is scoped to SKILL.md and the second to step files:

  1. a reference in a SKILL.md table row (line begins `|`) that contains `/` must carry
     ${CLAUDE_PLUGIN_ROOT} — the cell is handed straight to Read, and the variable expands at
     skill invocation (D-025), so it arrives absolute.
  2. a reference anywhere in a step-*.md must NOT carry ${CLAUDE_PLUGIN_ROOT} — a step file is
     loaded BY Read, where the token arrives literal and the path is inert (D-025).

Prose in a SKILL.md is a citation rather than a Read argument, so it takes the plain
plugin-relative form and neither rule fires on it.

NOT CHECKED, deliberately: whether a shared step file's *content* suits every workflow that
references it. `skills/greenfield/step-tasks.md` gates on the first phase not `done` and
mentions PHASE-1; whether that is right for `add-phase`, which references it, is the step's
content and out of scope here.

Dev-only. Not shipped behaviour: the plugin has no runtime dependency on it (D-001, D-015).

Usage:  python3 scripts/check-step-refs.py [--verbose]
Exit:   0 clean · 1 a finding · 2 skills/ could not be read, or held no references at all
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

VAR = "${CLAUDE_PLUGIN_ROOT}/"

# An inline-code span. Anchored `match` against REF below means only a span that is ENTIRELY a
# step path counts — `see step-push.md and step-merge.md` in one span would not.
SPAN = re.compile(r"`([^`\n]+)`")
REF = re.compile(r"^(?:\$\{CLAUDE_PLUGIN_ROOT\}/)?(?:[A-Za-z0-9._-]+/)*step-[a-z0-9-]+\.md$")


def preprocess(text):
    """Lines with fenced blocks and HTML comments blanked, line numbers preserved.

    Both regions name files that need not exist — examples, handoff transcripts, rationale —
    so a reference inside one is not a reference. Blanking rather than deleting keeps every
    finding's line number true to the file on disk."""
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    out, fenced = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else line)
    return out


def references(path):
    """Yield (line_no, span, is_table_row) for every step reference in one file."""
    for line_no, line in enumerate(preprocess(path.read_text()), 1):
        row = line.lstrip().startswith("|")
        for m in SPAN.finditer(line):
            span = m.group(1)
            if REF.match(span):
                yield line_no, span, row


def check(span, row, skill_dir, is_step_file):
    """Resolve one reference and return (target_path, [problems])."""
    qualified = span.startswith(VAR)
    rest = span[len(VAR):] if qualified else span
    target = (ROOT / rest) if (qualified or "/" in rest) else (skill_dir / rest)

    problems = []
    if not target.exists():
        problems.append(f"missing — no file at {target.relative_to(ROOT)}")
    if is_step_file and qualified:
        problems.append("shape — ${CLAUDE_PLUGIN_ROOT} is inert inside a step file, which is "
                        "loaded by Read; use the plugin-relative form (D-025, D-026)")
    if not is_step_file and row and "/" in span and not qualified:
        problems.append("shape — an index-table cell reaching another skill must carry "
                        "${CLAUDE_PLUGIN_ROOT}; it is read as a path (D-026)")
    return target, problems


def main():
    verbose = "--verbose" in sys.argv
    if not SKILLS.is_dir():
        print(f"✘ no skills/ directory at {SKILLS}\n", file=sys.stderr)
        return 2

    total, failures = 0, []
    for path in sorted(SKILLS.glob("*/*.md")):
        rel = path.relative_to(ROOT)
        is_step_file = path.name.startswith("step-")
        try:
            found = list(references(path))
        except OSError as e:
            print(f"✘ could not read {rel}: {e}\n", file=sys.stderr)
            return 2
        except UnicodeDecodeError:
            print(f"✘ could not read {rel}: not valid UTF-8\n", file=sys.stderr)
            return 2
        for line_no, span, row in found:
            total += 1
            where = f"{rel}:{line_no}"
            _, problems = check(span, row, path.parent, is_step_file)
            if problems:
                failures.append((where, span, problems))
            elif verbose:
                print(f"  ✔ {where}  `{span}`")

    if not total:
        print("✘ no step references found — are step files still cited in backticks?\n",
              file=sys.stderr)
        return 2

    print(f"\nchecked {total} step references against D-026")
    if failures:
        print(f"✘ {len(failures)} unresolved or misshapen\n")
        for where, span, problems in failures:
            print(f"  {where}  `{span}`")
            for p in problems:
                print(f"      {p}")
        print()
        return 1
    print("✔ every step reference resolves, in the shape its location dictates\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
