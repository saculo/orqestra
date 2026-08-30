#!/usr/bin/env python3
"""Conformance check of every dispatch envelope in skills/ against §5.5's obligation table.

§5.5 states which fields a dispatch must carry and makes the condition for each one decidable
by looking at exactly one thing. That is what makes an omission a contract violation rather
than a judgement call — but only if something checks, and until now nothing did. A dispatch
missing EXPERTISE degrades silently: the agent runs on its persona alone and the artifact
still looks right (D-025).

Four obligation classes, mirroring the table:

  always        ROLE STEP SKILL READ TEMPLATE WRITE RETURN
  scope         exactly one of TASK PHASE BUG PROJECT
  conditional   MODULE PATHS STACK EXPERTISE — keyed to the scope field, all four together:
                mandatory under TASK and BUG, forbidden under PHASE and PROJECT, because
                those units carry no module: in their frontmatter (D-027). Forbidden, not
                merely unnecessary — §5.5 calls a present one "a violation, not a harmless
                extra". With no scope key, or two, the class is undecidable and no
                conditional verdict is emitted; the scope problem is the whole report.
  step-specific LENSES ROUND — on a review dispatch and no other

The list is closed: a field in no class is a violation the same way an omission is.

DELIBERATELY NOT CHECKED: §5.5 row 4 also omits EXPERTISE when the module row's expertise
cell is empty. That fact lives in .orqestra/modules.md, not in the envelope, so no check
reading only the envelope can tell a conformant omission from a forgotten field. Requiring
all four under TASK/BUG is the least bad of three answers: dropping EXPERTISE to optional
would leave unchecked the one field that fails invisibly, and cross-checking modules.md
would need field values and a workspace read, coupling a skills/-shaped checker to
.orqestra/. Both modules.md rows carry a non-empty expertise cell today, and this script is
dev-only — it globs skills/ relative to its own repo root and never runs against a consuming
project — so the false positive cannot occur in the only tree it can run in. Revisit when,
and only when, a module is registered with an empty expertise cell.

Dev-only. Not shipped behaviour: the plugin has no runtime dependency on it (D-001, D-015).

Usage:  python3 scripts/check-envelopes.py [--verbose]
Exit:   0 clean · 1 a non-conformant envelope · 2 skills/ could not be read
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

ALWAYS = ["ROLE", "STEP", "SKILL", "READ", "TEMPLATE", "WRITE", "RETURN"]
SCOPE = ["TASK", "PHASE", "BUG", "PROJECT"]
MANDATES_CONDITIONAL = {"TASK", "BUG"}     # the scope unit carries a module: (D-027)
FORBIDS_CONDITIONAL = {"PHASE", "PROJECT"}  # it does not — the four must be omitted
CONDITIONAL = ["MODULE", "PATHS", "STACK", "EXPERTISE"]
STEP_SPECIFIC = ["LENSES", "ROUND"]
OPTIONAL = ["REWORK"]
KNOWN = set(ALWAYS + SCOPE + CONDITIONAL + STEP_SPECIFIC + OPTIONAL)

FIELD = re.compile(r"^([A-Z]+):\s*(.*)$")


def envelopes(path):
    """Yield (line_no, step, [field names]) for each envelope in one file.

    An envelope starts at ROLE: and ends at the fence that closes its block."""
    lines = path.read_text().split("\n")
    for i, line in enumerate(lines):
        if not line.startswith("ROLE:"):
            continue
        fields, step = [], ""
        for nxt in lines[i:]:
            m = FIELD.match(nxt)
            if m:
                fields.append(m.group(1))
                if m.group(1) == "STEP":
                    step = m.group(2).strip()
            elif nxt.startswith("```"):
                break
        yield i + 1, step, fields


def check(step, fields):
    present, problems = set(fields), []

    for f in ALWAYS:
        if f not in present:
            problems.append(f"missing {f} — always class")

    scopes = present & set(SCOPE)
    if len(scopes) != 1:
        problems.append(f"{len(scopes)} scope fields; exactly one of {'/'.join(SCOPE)} required")
    else:
        # The scope key alone decides the conditional class (D-027). With no scope key, or
        # two, the class is undecidable — reporting a derived second problem would be noise.
        scope = scopes.pop()
        have = present & set(CONDITIONAL)
        if scope in MANDATES_CONDITIONAL and have != set(CONDITIONAL):
            missing = ", ".join(sorted(set(CONDITIONAL) - have))
            problems.append(f"missing {missing} — mandatory under {scope}")
        if scope in FORBIDS_CONDITIONAL and have:
            problems.append(f"{', '.join(sorted(have))} must be omitted under {scope}")

    lenses = present & set(STEP_SPECIFIC)
    if step == "review" and lenses != set(STEP_SPECIFIC):
        problems.append("review dispatch missing LENSES/ROUND")
    if step != "review" and lenses:
        problems.append(f"{', '.join(sorted(lenses))} outside a review dispatch")

    for f in sorted(present - KNOWN):
        problems.append(f"{f} belongs to no class — the list is closed")

    dupes = {f for f in fields if fields.count(f) > 1}
    for f in sorted(dupes):
        problems.append(f"{f} declared more than once")

    return problems


def main():
    verbose = "--verbose" in sys.argv
    if not SKILLS.is_dir():
        print(f"✘ no skills/ directory at {SKILLS}\n", file=sys.stderr)
        return 2

    total, failures = 0, []
    for path in sorted(SKILLS.glob("*/*.md")):
        for line_no, step, fields in envelopes(path):
            total += 1
            rel = f"{path.relative_to(ROOT)}:{line_no}"
            problems = check(step, fields)
            if problems:
                failures.append((rel, step, problems))
            elif verbose:
                print(f"  ✔ {rel}  [{step or '—'}]")

    if not total:
        print("✘ no envelopes found — is the ROLE: convention still in use?\n", file=sys.stderr)
        return 2

    print(f"\nchecked {total} dispatch envelopes against §5.5")
    if failures:
        print(f"✘ {len(failures)} non-conformant\n")
        for rel, step, problems in failures:
            print(f"  {rel}  [{step or '—'}]")
            for p in problems:
                print(f"      {p}")
        print()
        return 1
    print("✔ all envelopes conform\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
