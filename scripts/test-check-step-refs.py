#!/usr/bin/env python3
"""Behavioural test of check-step-refs.py against D-026.

Running the checker over the repo proves only that today's forty references resolve. It does
not prove the checker would *notice* a reference that does not — which is the whole reason
the check exists, and the exact failure TASK-024 was written to close. Nor does a green run
prove the checker is looking the right way round: a check that lists `step-*.md` files and
confirms they exist would also print a reassuring number while three dangling references sat
in the tree untouched.

So each case exercises one rule in both directions, and the last case is the one that matters
most: it deletes a shared step and requires BOTH skills that reference it to be named. That is
what a reference->filesystem walk catches and a filesystem->reference walk cannot.

Usage: python3 scripts/test-check-step-refs.py
Exit:  0 all cases pass · 1 a case failed
"""

import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check-step-refs.py"
spec = importlib.util.spec_from_file_location("check_step_refs", SCRIPT)
cs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cs)

FAILED, TOTAL = [], 0


def case(name, got, want):
    global TOTAL
    TOTAL += 1
    if got == want:
        print(f"  ✓ {name}")
    else:
        print(f"  ✘ {name}\n      expected {want}\n      got      {got}")
        FAILED.append(name)


def problems(span, row, skill, is_step_file=False):
    """The problem strings check() reports for one reference."""
    _, probs = cs.check(span, row, cs.SKILLS / skill, is_step_file)
    return [p.split(" —")[0] for p in probs]


def recognised(text):
    """The spans references() picks out of a body of markdown."""
    tmp = Path(tempfile.mkdtemp()) / "SKILL.md"
    tmp.write_text(text)
    try:
        return [span for _, span, _ in cs.references(tmp)]
    finally:
        shutil.rmtree(tmp.parent)


print("What counts as a reference — backticks are the discriminator")
case("a bare step filename in backticks",
     recognised("see `step-push.md` for git"), ["step-push.md"])
case("a plugin-relative path in backticks",
     recognised("`skills/task/step-push.md` owns git"), ["skills/task/step-push.md"])
case("a ${CLAUDE_PLUGIN_ROOT} path in backticks",
     recognised("| x | `${CLAUDE_PLUGIN_ROOT}/skills/greenfield/step-tasks.md` |"),
     ["${CLAUDE_PLUGIN_ROOT}/skills/greenfield/step-tasks.md"])

print("\nWhat must never be flagged — six categories from ## Interfaces")
case("unbackticked mention", recognised("step-push.md owns git"), [])
case("a glob, i.e. D-007 convention talk", recognised("`step-*.md` are named, never numbered"), [])
case("a placeholder in angle brackets", recognised("`step-<name>.md`"), [])
case("a non-step file", recognised("`SKILL.md` and `PLAN.md`"), [])
case("inside a fenced block",
     recognised("```\n`step-nonexistent.md`\n```"), [])
case("inside an HTML comment",
     recognised("<!-- `step-nonexistent.md` was the old name -->"), [])
case("two files in one span is not a reference",
     recognised("`step-push.md and step-merge.md`"), [])

print("\nExistence — the reference must resolve")
case("same-skill bare filename that exists",
     problems("step-push.md", False, "task"), [])
case("bare filename naming ANOTHER skill's file",
     problems("step-push.md", False, "qa"), ["missing"])
case("qualified path that exists",
     problems("${CLAUDE_PLUGIN_ROOT}/skills/greenfield/step-tasks.md", True, "add-phase"), [])
case("qualified path that does not exist",
     problems("${CLAUDE_PLUGIN_ROOT}/skills/greenfield/step-nope.md", True, "add-phase"),
     ["missing"])

print("\nShape — D-026's two forms, chosen by how the file is loaded")
case("${CLAUDE_PLUGIN_ROOT} inside a step file is inert",
     problems("${CLAUDE_PLUGIN_ROOT}/skills/greenfield/step-tasks.md", False, "task",
              is_step_file=True),
     ["shape"])
case("plugin-relative inside a step file is correct",
     problems("skills/greenfield/step-tasks.md", False, "task", is_step_file=True), [])
case("an index cell reaching another skill must be qualified",
     problems("skills/greenfield/step-tasks.md", True, "add-phase"), ["shape"])
case("the same path in PROSE is correct unqualified",
     problems("skills/greenfield/step-tasks.md", False, "add-phase"), [])

print("\nDirection — the check walks references to the filesystem, never the reverse")
# The trap D-026's last constraint names. A checker that globbed step-*.md and confirmed each
# file exists would pass a tree whose references dangle. Deleting a file that TWO skills
# reference must name BOTH of them: that is only possible walking outward from references.
tmp = Path(tempfile.mkdtemp())
try:
    copy = tmp / "repo"
    shutil.copytree(ROOT / "skills", copy / "skills")
    shutil.copytree(ROOT / "scripts", copy / "scripts")
    (copy / "skills" / "greenfield" / "step-plan-design.md").unlink()
    out = subprocess.run([sys.executable, str(copy / "scripts" / "check-step-refs.py")],
                         capture_output=True, text=True)
    text = out.stdout + out.stderr
    case("deleting a shared step is detected", out.returncode, 1)
    case("...and names add-phase, which references it", "add-phase/SKILL.md" in text, True)
    case("...and names bugfix, which also references it", "bugfix/SKILL.md" in text, True)

    # An orphan step file is not a finding: nothing points at it, so nothing can rot.
    (copy / "skills" / "task" / "step-orphan.md").write_text("# orphan\n")
    out = subprocess.run([sys.executable, str(copy / "scripts" / "check-step-refs.py")],
                         capture_output=True, text=True)
    case("an unreferenced step file is not a finding",
         "step-orphan" in (out.stdout + out.stderr), False)
finally:
    shutil.rmtree(tmp)

print("\nRobustness — the two ways the check refuses to answer")
# Exit 2, not 0. A checker that reports "clean" when it read nothing is the failure mode that
# makes the whole check worthless: the convention moves, the count silently goes to zero, and
# the green tick keeps printing. Both cases must be distinguishable from a clean run.
tmp = Path(tempfile.mkdtemp())
try:
    bare = tmp / "no-skills"
    (bare / "scripts").mkdir(parents=True)
    shutil.copy(SCRIPT, bare / "scripts" / SCRIPT.name)
    out = subprocess.run([sys.executable, str(bare / "scripts" / SCRIPT.name)],
                         capture_output=True, text=True)
    case("no skills/ directory exits 2", out.returncode, 2)
    case("...without a traceback", "Traceback" in (out.stdout + out.stderr), False)

    (bare / "skills" / "nothing").mkdir(parents=True)
    (bare / "skills" / "nothing" / "SKILL.md").write_text("# a skill that cites no step file\n")
    out = subprocess.run([sys.executable, str(bare / "scripts" / SCRIPT.name)],
                         capture_output=True, text=True)
    case("a skills/ holding zero references exits 2", out.returncode, 2)
finally:
    shutil.rmtree(tmp)

print("\nThe repository itself")
out = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
case("every reference in skills/ resolves", out.returncode, 0)

# The reported total is the number to read, because it is the one that silently goes to zero:
# a fix that DELETED a dangling reference would also turn this check green. Counted here by a
# scan written independently of references(), so agreement means something.
independent = sum(
    len(re.findall(r"`(?:\$\{CLAUDE_PLUGIN_ROOT\}/)?(?:[A-Za-z0-9._-]+/)*step-[a-z0-9-]+\.md`",
                   "\n".join(cs.preprocess(p.read_text()))))
    for p in sorted((ROOT / "skills").glob("*/*.md")))
reported = re.search(r"checked (\d+) step references", out.stdout)
case("the reported total matches an independent count",
     int(reported.group(1)) if reported else None, independent)
case("...and that total is not zero", independent > 0, True)

print()
if FAILED:
    print(f"✘ {len(FAILED)} of {TOTAL} cases failed: {', '.join(FAILED)}\n")
    sys.exit(1)
print(f"ran {TOTAL} cases against check-step-refs.py\n✔ all cases pass\n")
