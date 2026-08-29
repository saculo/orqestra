#!/usr/bin/env python3
"""Behavioural test of check-templates.py against the §4.8.1 catalogue.

Running the checker over this repo proves only that today's templates pass. It does not
prove the checker would *notice* a template that is broken — which is the whole reason the
check exists, and exactly the defect TASK-008 closed: `decisions/D-NNN-*.md` was counted as
"checked" while nothing about it was ever examined.

Every case runs the real script as a subprocess against a throwaway copy of the repo
(REQUIREMENTS.md + templates/ + the script), so a case may break the catalogue or a template
without touching the working tree. Cases assert on exit code and on stdout/stderr text.

Usage: python3 scripts/test-check-templates.py [--verbose]
Exit:  0 all cases pass · 1 a case failed
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = Path(__file__).resolve().parent / "check-templates.py"

# The catalogue row and template that the coverage hole hid. Named here because the test
# must speak about a concrete artifact; the SCRIPT must not (AC-4), which case 9 asserts.
DECISION_ROW = "decisions/D-NNN-*.md"
DECISION_TPL = "DECISION.md"

results = []


def fixture(tmp):
    """An isolated copy of everything check-templates.py reads."""
    ws = Path(tmp) / "ws"
    (ws / "scripts").mkdir(parents=True)
    shutil.copy(ROOT / "REQUIREMENTS.md", ws / "REQUIREMENTS.md")
    shutil.copytree(ROOT / "templates", ws / "templates")
    shutil.copy(SCRIPT, ws / "scripts" / SCRIPT.name)
    return ws


def run(ws, *args):
    p = subprocess.run([sys.executable, str(ws / "scripts" / SCRIPT.name), *args],
                       cwd=ws, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def check(name, ok, detail=""):
    results.append((ok, name, detail))


def counted(out):
    m = re.search(r"checked (\d+) templates", out)
    return int(m.group(1)) if m else None


def catalogue_rows(ws):
    """The §4.8.1 rows, counted independently of the script under test.

    REQUIREMENTS.md holds other tables that name artifacts (§5.5's dispatch table among them),
    so the section must be sliced out first — counting `| \\`X.md\\` |` across the whole file
    over-counts and would make this assertion meaningless.
    """
    text = (ws / "REQUIREMENTS.md").read_text()
    m = re.search(r"#### 4\.8\.1 The catalogue\n(.*?)\n#### 4\.8\.2", text, re.S)
    assert m, "no §4.8.1 section in REQUIREMENTS.md"
    return [l.strip().strip("|").split("|")[0].strip().strip("`")
            for l in m.group(1).splitlines()
            if l.startswith("| `")]


def edit_row(ws, artifact, column, value):
    """Rewrite one cell of one §4.8.1 catalogue row. column: 2=frontmatter, 3=headings."""
    path = ws / "REQUIREMENTS.md"
    lines = path.read_text().splitlines(True)
    for i, line in enumerate(lines):
        if line.startswith(f"| `{artifact}` |"):
            cells = line.strip().strip("|").split("|")
            cells[column] = f" {value} "
            lines[i] = "|" + "|".join(cells) + "|\n"
            path.write_text("".join(lines))
            return
    raise AssertionError(f"no catalogue row for {artifact}")


def strip_frontmatter(path):
    path.write_text(path.read_text().split("---\n", 2)[2])


def drop_frontmatter_key(path, key):
    kept = [l for l in path.read_text().splitlines(True) if not l.startswith(f"{key}:")]
    path.write_text("".join(kept))


# --------------------------------------------------------------------------------------

def case_clean(ws):
    """The repo's own templates conform, and every catalogue row but the free-form one is counted."""
    code, out = run(ws)
    check("clean tree exits 0", code == 0, out)

    rows = len(catalogue_rows(ws))
    n = counted(out)
    # Exactly one row (PRD.md) is declared free-form, so every other row must be checked.
    check(f"every non-free-form catalogue row is counted ({n} of {rows} rows)",
          n is not None and rows - n == 1, out)


def case_ac1_frontmatter_still_checked(ws):
    """AC-1: a row declaring no `##` headings still has its frontmatter checked."""
    tpl = ws / "templates" / DECISION_TPL
    drop_frontmatter_key(tpl, "area")
    code, out = run(ws)
    check("AC-1 no-headings row: a missing frontmatter key fails",
          code == 1 and "frontmatter missing: area" in out, out)
    check("AC-1 the finding names the no-headings row", DECISION_ROW in out, out)


def case_ac1_extra_key(ws):
    """AC-1: frontmatter checking on a no-headings row runs in both directions."""
    tpl = ws / "templates" / DECISION_TPL
    lines = tpl.read_text().splitlines(True)
    lines.insert(1, "bogus_key: x\n")
    tpl.write_text("".join(lines))
    code, out = run(ws)
    check("AC-1 no-headings row: a key absent from the catalogue fails",
          code == 1 and "frontmatter not in catalogue: bogus_key" in out, out)


def case_ac1_heading_comparison_skipped(ws):
    """AC-1: ONLY the heading comparison is skipped — a stray `##` is not a failure there."""
    tpl = ws / "templates" / DECISION_TPL
    tpl.write_text(tpl.read_text() + "\n## A Heading The Catalogue Never Declared\n")
    code, out = run(ws)
    check("AC-1 no-headings row: the heading comparison is skipped, not the row",
          code == 0, out)


def case_ac2_counted(ws):
    """AC-2: the row appears in the checked count."""
    code, out = run(ws, "--verbose")
    check("AC-2 the decision row is reported as checked",
          code == 0 and f"✓ {DECISION_ROW}" in out, out)


def case_ac2_broken_frontmatter(ws):
    """AC-2: breaking its frontmatter makes the check fail. The negative control."""
    strip_frontmatter(ws / "templates" / DECISION_TPL)
    code, out = run(ws)
    check("AC-2 removing the frontmatter entirely fails, naming the row",
          code == 1 and "no YAML frontmatter" in out and DECISION_ROW in out, out)


def case_ac3_missing(ws):
    """AC-3: a missing catalogue exits 2 with a message, never a traceback."""
    (ws / "REQUIREMENTS.md").unlink()
    code, out = run(ws)
    check("AC-3 missing REQUIREMENTS.md exits 2",
          code == 2 and "could not read the catalogue" in out and "Traceback" not in out, out)


def case_ac3_unreadable(ws):
    """AC-3: unreadable covers permissions, not just absence."""
    if os.geteuid() == 0:
        check("AC-3 unpermitted REQUIREMENTS.md exits 2", True, "skipped: running as root")
        return
    (ws / "REQUIREMENTS.md").chmod(0o000)
    code, out = run(ws)
    (ws / "REQUIREMENTS.md").chmod(0o644)
    check("AC-3 unpermitted REQUIREMENTS.md exits 2",
          code == 2 and "could not read the catalogue" in out and "Traceback" not in out, out)


def case_ac3_undecodable(ws):
    """AC-3: a corrupt catalogue is unreadable too, and must not reach a traceback."""
    (ws / "REQUIREMENTS.md").write_bytes(b"\xff\xfe\x00 not utf-8")
    code, out = run(ws)
    check("AC-3 undecodable REQUIREMENTS.md exits 2",
          code == 2 and "could not read the catalogue" in out and "Traceback" not in out, out)


def case_ac3_target_mode(ws):
    """AC-3: the guard is in the parse, so --target mode inherits it."""
    (ws / "REQUIREMENTS.md").unlink()
    code, out = run(ws, "--target", str(ROOT / ".orqestra"))
    check("AC-3 --target mode also exits 2 on a missing catalogue",
          code == 2 and "could not read the catalogue" in out and "Traceback" not in out, out)


def case_ac4_exemption_follows_catalogue(ws):
    """AC-4: which artifact is exempt is a catalogue fact. Move it, and the checker follows."""
    edit_row(ws, "PRD.md", 3, "`## Goal`")
    edit_row(ws, "DESIGN.md", 3, "none — free-form for this test")
    code, out = run(ws, "--verbose")
    check("AC-4 the newly free-form row is skipped",
          "DESIGN.md: free-form, no schema — skipped" in out, out)
    check("AC-4 the no-longer-free-form row is checked and fails",
          code == 1 and re.search(r"^  PRD\.md$", out, re.M) is not None, out)


# Where an artifact name is legitimate: it maps a catalogue name onto a filesystem location,
# which the catalogue does not state and the script therefore cannot derive. `SPEC` names the
# catalogue file itself. Anything else restates the catalogue and is what AC-4 forbids.
NAME_TO_PATH = {"ALIASES", "INSTANCE_PATHS", "SPEC"}


def case_ac4_no_hardcoded_names(ws):
    """AC-4: no artifact name is restated in the script outside the name→path maps.

    Matched on the AST, not on line ranges, so it stays true as the file is reformatted — and
    so that a name reintroduced anywhere (a `FREEFORM` set, a conditional, a default argument)
    is caught wherever it is put.
    """
    import ast

    tree = ast.parse(SCRIPT.read_text())
    allowed = set()
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id in NAME_TO_PATH for t in node.targets):
            allowed.update(id(n) for n in ast.walk(node.value))
    # check_instance builds the same map incrementally into `targets` — a loop iterator of
    # (pattern, glob) pairs and a comprehension over a decisions glob. Same role, same licence.
    for node in ast.walk(tree):
        binds_targets = (
            (isinstance(node, (ast.Assign, ast.AugAssign))
             and any(isinstance(t, ast.Name) and t.id == "targets"
                     for t in (node.targets if isinstance(node, ast.Assign) else [node.target])))
            or (isinstance(node, ast.For) and isinstance(node.iter, ast.Tuple)))
        if binds_targets:
            allowed.update(id(n) for n in ast.walk(node))

    def is_message(s):
        # A sentence printed at a human. It cannot key a decision: nothing compares against it.
        return " " in s

    offenders = [f"line {n.lineno}: {n.value!r}"
                 for n in ast.walk(tree)
                 if isinstance(n, ast.Constant) and isinstance(n.value, str)
                 and n.value.endswith(".md") and id(n) not in allowed
                 and not is_message(n.value)]
    check("AC-4 no artifact name outside the name→path maps",
          not offenders, "; ".join(offenders))


CASES = [case_clean, case_ac1_frontmatter_still_checked, case_ac1_extra_key,
         case_ac1_heading_comparison_skipped, case_ac2_counted, case_ac2_broken_frontmatter,
         case_ac3_missing, case_ac3_unreadable, case_ac3_undecodable, case_ac3_target_mode,
         case_ac4_exemption_follows_catalogue, case_ac4_no_hardcoded_names]


def main():
    verbose = "--verbose" in sys.argv
    for c in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            c(fixture(tmp))

    failed = [r for r in results if not r[0]]
    for ok, name, detail in results:
        if not ok:
            print(f"  ✘ {name}")
            for line in detail.splitlines():
                print(f"      {line}")
        elif verbose:
            print(f"  ✓ {name}")

    print(f"\nran {len(results)} cases against {SCRIPT.name}")
    if failed:
        print(f"\n✘ {len(failed)} case(s) failed\n")
        return 1
    print("✔ all cases pass\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
