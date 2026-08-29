#!/usr/bin/env python3
"""Conformance check for `.orqestra/decisions/` against templates/DECISION.md.

`check-templates.py` cannot catch this. A decision file's schema is carried in **bold
field lines** — `**When:**`, `**Decision:**`, `**Why:**`, `**Constrains:**` — not in `##`
headings, and the heading check therefore passes a decision that is missing all four.

`**Constrains:**` is the field the template calls "the one that earns this file": a fresh
agent reads a decision for exactly one reason, to know what it must do differently. A
decision without it is a note, and the next agent inherits the line without the reason —
which is precisely what a `D-NNN` is required for.

Also checks the index: every decision has a row, and `count`/`next_id` match the table.

Dev-only. Not shipped behaviour (D-001).

Usage:  python3 scripts/check-decisions.py [--target <workspace-dir>]
Exit:   0 clean · 1 conformance failure · 2 the template itself could not be read
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "DECISION.md"


def required_fields(template_text):
    """The bold field labels the template declares, in order."""
    body = template_text.split("---", 2)[-1]
    return [m.group(1) for m in re.finditer(r"^\*\*([A-Za-z ]+):\*\*", body, re.M)]


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.split("#")[0].strip()
    return out


def check(decisions_dir, fields):
    findings = []
    files = sorted(p for p in decisions_dir.glob("D-*.md"))
    index = decisions_dir / "INDEX.md"

    for path in files:
        text = path.read_text()
        for field in fields:
            if not re.search(r"^\*\*%s:\*\*" % re.escape(field), text, re.M):
                findings.append((path.name, "missing **%s:** — required by templates/DECISION.md" % field))
        fm = frontmatter(text)
        if fm.get("type") != "decision":
            findings.append((path.name, "frontmatter type is %r, expected 'decision'" % fm.get("type")))
        stem_id = path.name.split("-")[0] + "-" + path.name.split("-")[1]
        if fm.get("id") != stem_id:
            findings.append((path.name, "frontmatter id %r does not match filename %r" % (fm.get("id"), stem_id)))

    if index.exists():
        itext = index.read_text()
        rows = re.findall(r"^\| (D-\d+) \|", itext, re.M)
        for path in files:
            did = path.name.split("-")[0] + "-" + path.name.split("-")[1]
            if did not in rows:
                findings.append(("INDEX.md", "no row for %s" % did))
        for did in rows:
            if not any(p.name.startswith(did + "-") for p in files):
                findings.append(("INDEX.md", "row %s has no decision file" % did))
        ifm = frontmatter(itext)
        if ifm.get("count") != str(len(rows)):
            findings.append(("INDEX.md", "count is %s, table has %d rows" % (ifm.get("count"), len(rows))))
        expected_next = max((int(r.split("-")[1]) for r in rows), default=0) + 1
        if ifm.get("next_id") != str(expected_next):
            findings.append(("INDEX.md", "next_id is %s, expected %d" % (ifm.get("next_id"), expected_next)))
    else:
        findings.append(("INDEX.md", "missing"))

    return len(files), findings


def main():
    target = ROOT / ".orqestra"
    if "--target" in sys.argv:
        target = pathlib.Path(sys.argv[sys.argv.index("--target") + 1])
    decisions = target / "decisions"

    if not TEMPLATE.exists():
        print("cannot read %s" % TEMPLATE, file=sys.stderr)
        return 2
    fields = required_fields(TEMPLATE.read_text())
    if not fields:
        print("no bold field labels found in %s" % TEMPLATE, file=sys.stderr)
        return 2
    if not decisions.is_dir():
        print("no decisions directory at %s" % decisions, file=sys.stderr)
        return 2

    total, findings = check(decisions, fields)
    print("\nchecked %d decisions against templates/DECISION.md (%s)"
          % (total, ", ".join("**%s:**" % f for f in fields)))
    if not findings:
        print("✔ all decisions conform\n")
        return 0
    print("✘ %d finding(s):\n" % len(findings))
    for name, msg in findings:
        print("  %s\n      %s" % (name, msg))
    print()
    return 1


if __name__ == "__main__":
    sys.exit(main())
