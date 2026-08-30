#!/usr/bin/env python3
"""Behavioural test of check-envelopes.py against §5.5's obligation table.

Running the checker over the repo proves only that today's ten envelopes pass or fail.
It does not prove the checker would *notice* a violation that is not currently present —
which is the whole reason the check exists. These cases exercise each obligation class in
both directions: a conformant envelope produces no problem, and a violation produces one
naming the class it broke.

Usage: python3 scripts/test-check-envelopes.py
Exit:  0 all cases pass · 1 a case failed
"""

import importlib.util
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check-envelopes.py"
spec = importlib.util.spec_from_file_location("check_envelopes", SCRIPT)
ce = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ce)

# §5.5's always class, plus a scope field. Conformant on its own only under a scope that
# forbids the conditional class — PHASE or PROJECT (D-027).
SCOPED = ["ROLE", "STEP", "SKILL", "TASK", "READ", "TEMPLATE", "WRITE", "RETURN"]
# The conditional class: all four together, keyed to the scope field (§5.5, D-027).
CONDITIONAL = ["MODULE", "PATHS", "STACK", "EXPERTISE"]
# The minimum conformant dispatch under TASK or BUG, which mandate the conditional class.
BASE = SCOPED + CONDITIONAL


def scoped(key):
    """SCOPED with its scope field swapped for `key` — no conditional class."""
    return [f if f != "TASK" else key for f in SCOPED]


def case(name, step, fields, expect):
    """expect: [] for conformant, else substrings each of which must appear in a problem."""
    problems = ce.check(step, fields)
    if not expect:
        ok = not problems
    else:
        ok = all(any(e in p for p in problems) for e in expect) and len(problems) == len(expect)
    return ok, name, problems


CASES = [
    # --- always class -------------------------------------------------------
    ("minimum conformant dispatch", "implement", BASE, []),
    ("missing conditional class under TASK is caught", "implement",
     SCOPED, ["missing EXPERTISE, MODULE, PATHS, STACK — mandatory under TASK"]),
    ("missing SKILL is caught", "implement",
     [f for f in BASE if f != "SKILL"], ["missing SKILL — always class"]),
    ("missing WRITE is caught", "implement",
     [f for f in BASE if f != "WRITE"], ["missing WRITE — always class"]),
    ("missing RETURN is caught", "implement",
     [f for f in BASE if f != "RETURN"], ["missing RETURN — always class"]),

    # --- scope class: exactly one of TASK/PHASE/BUG/PROJECT -----------------
    ("PHASE is an accepted scope", "create-tasks", scoped("PHASE"), []),
    ("PROJECT is an accepted scope", "create-phases", scoped("PROJECT"), []),
    ("BUG is an accepted scope", "diagnose",
     [f if f != "TASK" else "BUG" for f in BASE], []),
    ("no scope field is caught", "create-phases",
     [f for f in BASE if f != "TASK"], ["0 scope fields"]),
    ("two scope fields are caught", "implement",
     BASE + ["PHASE"], ["2 scope fields"]),
    ("PROJECT alongside TASK is two scope fields", "implement",
     BASE + ["PROJECT"], ["2 scope fields"]),

    # --- conditional class: mandatory under TASK/BUG ------------------------
    ("partial conditional class is caught", "implement",
     SCOPED + ["MODULE", "PATHS"], ["missing EXPERTISE, STACK — mandatory under TASK"]),
    ("MODULE alone is caught", "implement",
     SCOPED + ["MODULE"], ["missing EXPERTISE, PATHS, STACK — mandatory under TASK"]),
    ("missing conditional class under BUG is caught", "diagnose",
     scoped("BUG"), ["missing EXPERTISE, MODULE, PATHS, STACK — mandatory under BUG"]),

    # --- conditional class: forbidden under PHASE/PROJECT -------------------
    ("conditional fields under PROJECT are caught", "create-phases",
     scoped("PROJECT") + CONDITIONAL,
     ["EXPERTISE, MODULE, PATHS, STACK must be omitted under PROJECT"]),
    ("conditional fields under PHASE are caught", "create-tasks",
     scoped("PHASE") + CONDITIONAL,
     ["EXPERTISE, MODULE, PATHS, STACK must be omitted under PHASE"]),
    ("a single conditional field under PROJECT is caught", "create-phases",
     scoped("PROJECT") + ["MODULE"], ["MODULE must be omitted under PROJECT"]),

    # --- step-specific: LENSES/ROUND on review, and on no other -------------
    ("review dispatch with LENSES and ROUND is conformant", "review",
     BASE + ["LENSES", "ROUND"], []),
    ("review dispatch missing ROUND is caught", "review",
     BASE + ["LENSES"], ["review dispatch missing LENSES/ROUND"]),
    ("review dispatch with neither is caught", "review",
     BASE, ["review dispatch missing LENSES/ROUND"]),
    ("LENSES outside a review dispatch is caught", "implement",
     BASE + ["LENSES"], ["LENSES outside a review dispatch"]),
    ("ROUND outside a review dispatch is caught", "qa",
     BASE + ["ROUND"], ["ROUND outside a review dispatch"]),

    # --- the list is closed -------------------------------------------------
    ("an invented field is caught", "implement",
     BASE + ["PRIORITY"], ["PRIORITY belongs to no class — the list is closed"]),
    ("REWORK is permitted on a re-dispatch", "implement", BASE + ["REWORK"], []),

    # --- duplicates ---------------------------------------------------------
    ("a duplicated field is caught", "implement",
     BASE + ["WRITE"], ["WRITE declared more than once"]),
]


def main():
    failures = []
    for name, step, fields, expect in CASES:
        ok, name, problems = case(name, step, fields, expect)
        if not ok:
            failures.append((name, expect, problems))

    print(f"\nchecked {len(CASES)} §5.5 obligation cases")
    if failures:
        print(f"✘ {len(failures)} failed\n")
        for name, expect, problems in failures:
            print(f"  {name}")
            print(f"      expected: {expect or 'no problems'}")
            print(f"      observed: {problems or 'no problems'}")
        print()
        return 1
    print("✔ the checker enforces every obligation class in both directions\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
