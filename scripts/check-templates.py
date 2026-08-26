#!/usr/bin/env python3
"""Conformance check against the §4.8.1 catalogue in REQUIREMENTS.md.

Two modes:
  (default)          check templates/ — the schemas themselves
  --target <dir>     check a real .orqestra/ workspace — the artifacts a workflow produced

The second mode is what catches a skill that composed a file from scratch instead of copying
its template (D16). Such a file reads correctly to a human and is invisible to `status`,
which derives every task stage from frontmatter — so nothing else would report it.

The catalogue is the single source of truth (D-003). This script parses it and proves
every artifact template matches — frontmatter keys, headings, and heading ORDER.

Dev-only. Not shipped behaviour: the plugin has no runtime dependency on it (D-001, D-015).

Usage:  python3 scripts/check-templates.py [--verbose] [--target <workspace-dir>]
Exit:   0 clean · 1 conformance failure · 2 the catalogue itself could not be read
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEC = ROOT / "REQUIREMENTS.md"
TPL = ROOT / "templates"

# Common frontmatter, implied on every artifact (§4.4.4)
COMMON = ["id", "type", "status", "updated"]

# Catalogue names that do not map 1:1 onto a template filename
ALIASES = {"decisions/INDEX.md": "DECISIONS_INDEX.md", "decisions/D-NNN-*.md": "DECISION.md"}

# A row exempts itself from the schema by writing `none` in its Required-headings column
# (§4.8.1). Read the exemption off the row; never hard-code the artifact name — a name in the
# script and a rule in the catalogue drift apart, and the catalogue is the source of truth (D-003).
def is_freeform(headings_cell):
    return headings_cell.strip().lower().startswith("none")

# A catalogue row may exempt itself from the common frontmatter (§4.4.4) by saying so in
# its Frontmatter column. config.md is the expected case: it is configuration, not project
# state, so `status` and `updated` would be noise on it.
EXEMPT_MARKER = "no common frontmatter"


def parse_catalogue():
    try:
        text = SPEC.read_text()
    except OSError as exc:
        print(f"✘ cannot read the catalogue at {SPEC}: {exc.strerror}", file=sys.stderr)
        sys.exit(2)
    m = re.search(r"#### 4\.8\.1 The catalogue\n(.*?)\n#### 4\.8\.2", text, re.S)
    if not m:
        print("✘ could not locate §4.8.1 in REQUIREMENTS.md", file=sys.stderr)
        sys.exit(2)
    rows = []
    for line in m.group(1).splitlines():
        if not line.startswith("|") or line.startswith("|---") or "Artifact |" in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        name = re.sub(r"`", "", cells[0])
        # A key written `name?` is CONDITIONAL — present only when some other field makes it
        # meaningful (e.g. `bug?` only when `origin: bug`). Required on the template, optional
        # on an instance: the template documents the field, an artifact need not carry it.
        extra = [] if cells[2].lower() == "none" else re.findall(r"`([a-z_]+)\??`", cells[2])
        optional = set(re.findall(r"`([a-z_]+)\?`", cells[2]))
        base = [] if EXEMPT_MARKER in cells[2].lower() else COMMON
        heads = re.findall(r"`(##[^`]+)`", cells[3])
        rows.append({"name": name, "frontmatter": base + extra, "optional": optional,
                     "headings": heads, "freeform": is_freeform(cells[3])})
    return rows


def read_template(path):
    text = path.read_text()
    fm_keys, headings = [], []
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            k = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):", line)
            if k:
                fm_keys.append(k.group(1))
        body = text[m.end():]
    else:
        body = text
    # ignore headings inside fenced code blocks and HTML comments
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    for line in body.splitlines():
        if line.startswith("## "):
            headings.append(line.rstrip())
    return fm_keys, headings, bool(m)


# Where each catalogue row lands inside a real .orqestra/ workspace
INSTANCE_PATHS = {
    "config.md": "config.md",
    "modules.md": "modules.md",
    "PROJECT.md": "project/PROJECT.md",
    "PRD.md": "PRD.md",
    "CLARIFICATIONS.md": "CLARIFICATIONS.md",
    "decisions/INDEX.md": "decisions/INDEX.md",
    "PHASES.md": "phases/PHASES.md",
}


def check_instance(target, rows, verbose):
    """Check the artifacts a real workspace contains. Absent artifacts are not failures —
    a workspace legitimately has only what its workflows have produced so far."""
    ws = pathlib.Path(target)
    if not ws.exists():
        print(f"✘ no workspace at {ws}", file=sys.stderr)
        return 2
    by_name = {r["name"]: r for r in rows}
    failures, checked = [], 0

    targets = [(n, ws / p) for n, p in INSTANCE_PATHS.items()]
    targets += [(f"decisions/D-NNN-*.md", f) for f in sorted(ws.glob("decisions/D-*.md"))]
    for pat, sub in (("PHASE.md", "phases/*/PHASE.md"), ("TASKS.md", "phases/*/tasks/TASKS.md"),
                     ("TASK.md", "phases/*/tasks/*/TASK.md"), ("PLAN.md", "phases/*/tasks/*/PLAN.md"),
                     ("DESIGN.md", "phases/*/tasks/*/DESIGN.md"),
                     ("IMPLEMENTATION.md", "phases/*/tasks/*/IMPLEMENTATION.md"),
                     ("QA.md", "phases/*/tasks/*/QA.md"), ("REVIEW.md", "phases/*/tasks/*/REVIEW.md"),
                     ("PR.md", "phases/*/tasks/*/PR.md"),
                     ("PHASE_SUMMARY.md", "phases/*/PHASE_SUMMARY.md")):
        targets += [(pat, f) for f in sorted(ws.glob(sub))]

    for name, path in targets:
        row = by_name.get(name)
        if row is None or not path.exists() or row["freeform"]:
            continue
        checked += 1
        fm_keys, headings, has_fm = read_template(path)
        problems = []
        if not has_fm:
            problems.append("no YAML frontmatter — file was composed rather than copied from its template (D16)")
        else:
            missing = [k for k in row["frontmatter"]
                       if k not in fm_keys and k not in row.get("optional", ())]
            if missing:
                problems.append(f"frontmatter missing: {', '.join(missing)}")
        if row["headings"]:
            missing_h = [h for h in row["headings"] if h not in headings]
            if missing_h:
                problems.append(f"headings missing: {', '.join(missing_h)}")
        if problems:
            failures.append((str(path.relative_to(ws)), problems))
        elif verbose:
            print(f"  ✓ {path.relative_to(ws)}")

    print(f"\nchecked {checked} artifacts in {ws} against §4.8.1")
    if failures:
        print(f"\n✘ {len(failures)} artifact(s) do not conform:\n")
        for name, problems in failures:
            print(f"  {name}")
            for p in problems:
                print(f"      {p}")
        print()
        return 1
    print("✔ all artifacts conform\n")
    return 0


def main():
    verbose = "--verbose" in sys.argv
    rows = parse_catalogue()
    if "--target" in sys.argv:
        return check_instance(sys.argv[sys.argv.index("--target") + 1], rows, verbose)
    failures, checked = [], 0

    for row in rows:
        name = row["name"]
        fname = ALIASES.get(name, name)
        path = TPL / fname
        problems = []

        if not path.exists():
            failures.append((name, [f"no template at templates/{fname}"]))
            continue
        if row["freeform"]:
            if verbose:
                print(f"  · {name}: catalogue declares no schema — skipped")
            continue

        checked += 1
        fm_keys, headings, has_fm = read_template(path)

        if not has_fm:
            problems.append("no YAML frontmatter")
        else:
            missing = [k for k in row["frontmatter"] if k not in fm_keys]
            extra = [k for k in fm_keys if k not in row["frontmatter"]]
            if missing:
                problems.append(f"frontmatter missing: {', '.join(missing)}")
            if extra:
                problems.append(f"frontmatter not in catalogue: {', '.join(extra)}")

        # A row with no `##` headings — DECISION.md is an H1 plus bold labels — has nothing to
        # compare, but its FRONTMATTER is still a schema. Skipping the whole row here is what let
        # DECISION.md sit outside the checked count while the script reported success.
        want, got = row["headings"], headings
        if want and want != got:
            missing = [h for h in want if h not in got]
            extra = [h for h in got if h not in want]
            if missing:
                problems.append(f"headings missing: {', '.join(missing)}")
            if extra:
                problems.append(f"headings not in catalogue: {', '.join(extra)}")
            if not missing and not extra:
                problems.append(f"headings out of order: expected {' → '.join(want)}, found {' → '.join(got)}")

        if problems:
            failures.append((name, problems))
        elif verbose:
            print(f"  ✓ {name}")

    print(f"\nchecked {checked} templates against §4.8.1")
    if failures:
        print(f"\n✘ {len(failures)} template(s) do not conform:\n")
        for name, problems in failures:
            print(f"  {name}")
            for p in problems:
                print(f"      {p}")
        print()
        return 1
    print("✔ all templates conform\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
