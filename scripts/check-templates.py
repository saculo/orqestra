#!/usr/bin/env python3
"""Conformance check: templates/ against the §4.8.1 catalogue in REQUIREMENTS.md.

The catalogue is the single source of truth (D-003). This script parses it and proves
every artifact template matches — frontmatter keys, headings, and heading ORDER.

Dev-only. Not shipped behaviour: the plugin has no runtime dependency on it (D-001, D-015).

Usage:  python3 scripts/check-templates.py [--verbose]
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

# Rows the catalogue declares as having no schema
FREEFORM = {"PRD.md"}

# A catalogue row may exempt itself from the common frontmatter (§4.4.4) by saying so in
# its Frontmatter column. config.md is the expected case: it is configuration, not project
# state, so `status` and `updated` would be noise on it.
EXEMPT_MARKER = "no common frontmatter"


def parse_catalogue():
    text = SPEC.read_text()
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
        extra = [] if cells[2].lower() == "none" else re.findall(r"`([a-z_]+)`", cells[2])
        base = [] if EXEMPT_MARKER in cells[2].lower() else COMMON
        heads = re.findall(r"`(##[^`]+)`", cells[3])
        rows.append({"name": name, "frontmatter": base + extra, "headings": heads})
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


def main():
    verbose = "--verbose" in sys.argv
    rows = parse_catalogue()
    failures, checked = [], 0

    for row in rows:
        name = row["name"]
        fname = ALIASES.get(name, name)
        path = TPL / fname
        problems = []

        if not path.exists():
            failures.append((name, [f"no template at templates/{fname}"]))
            continue
        if name in FREEFORM:
            if verbose:
                print(f"  · {name}: free-form, no schema — skipped")
            continue
        if not row["headings"]:
            if verbose:
                print(f"  · {name}: catalogue declares no headings — skipped")
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

        want, got = row["headings"], headings
        if want != got:
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
