#!/usr/bin/env python3
"""check-no-history.py — the no-history / provenance gate (SPEC INV-253).

UNARMED until the spec-format conversion delivery (INV-270); no default file, the document is named on
the command line.

THE LAW (FORMAT.md law 6, INV-253): the spec states today's behaviour only. Dates, provenance, and the
reasons behind past choices live in `JOURNAL.md`, not in the spec. A dated note or a provenance
sentence in the spec BODY is a defect and moves to the journal.

This gate reds the body (the requirements, from the first requirement on — the preamble and glossary
are exempt, as the preamble may state what the codes are and the glossary may define `journal` in
terms of the history it holds) on:

  - a DATE: an ISO date (2026-07-22), a month-name-and-number (July 2026), or a bare four-digit year.
  - a RECORDED-WORD phrase: "his word", "he said", "on his OK", "her word", and their kin — a decision
    attributed to a person's recorded say, which belongs in the journal.
  - a HISTORY phrase: "back in <year>", "as of <year>", "used to be", "formerly", "previously renamed",
    "flipped on", "(v… , <year>)" — a sentence narrating a past state rather than today's.

Deliberately NOT flagged: "supersede(d)", which the attic requirement uses for today's behaviour, and
"history" / "past choices", which the glossary may name when defining the journal. The precise reason
behind a requirement is a cold-reader / journal concern; this gate catches the mechanical date and
attribution markers.

Usage:
  check-no-history.py <document.md> [<part.md> ...]
Exit 0 when the body carries no date or provenance marker (printing the reach line, INV-269); exit 1
naming each. Stdlib only.
"""
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import specformat as sf  # noqa: E402
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402

CHECK = "check-no-history"

MONTHS = ("January|February|March|April|May|June|July|August|September|October|November|December")
PATTERNS = [
    ("date", re.compile(r"\b(?:19|20)\d\d-\d\d-\d\d\b")),
    ("date", re.compile(r"\b(?:%s)\s+\d" % MONTHS)),
    ("date", re.compile(r"\b\d{1,2}\s+(?:%s)\b" % MONTHS)),
    ("year", re.compile(r"\b(?:19|20)\d\d\b")),
    ("recorded-word", re.compile(r"\b(?:his|her|their)\s+word\b", re.I)),
    ("recorded-word", re.compile(r"\bhe\s+said\b|\bshe\s+said\b", re.I)),
    ("recorded-word", re.compile(r"\bon\s+(?:his|her|their)\s+ok\b", re.I)),
    ("history", re.compile(r"\bback in (?:19|20)\d\d\b", re.I)),
    ("history", re.compile(r"\bas of (?:19|20)\d\d\b", re.I)),
    ("history", re.compile(r"\bused to be\b", re.I)),
    ("history", re.compile(r"\bformerly\b", re.I)),
    ("history", re.compile(r"\bflipped on\b", re.I)),
]


def _body_lines(doc):
    """(1-based line number, text) for each body line — from the first requirement to the end."""
    if not doc.requirements:
        return []
    start = doc.requirements[0].line_no - 1
    lines = doc.text.split("\n")
    return [(i + 1, lines[i]) for i in range(start, len(lines))]


def main(argv):
    if len(argv) < 2:
        print("%s: usage: %s <document.md> [<part.md> ...]" % (CHECK, os.path.basename(argv[0])))
        return 2
    # The document may arrive as a core plus its parts (specformat's parts map). The gate
    # reads the concatenation as ONE document, so a rule that spans core and part is seen once; with
    # no parts this is the single file, byte for byte.
    paths = sf.spec_paths(argv[1:])
    missing = [p for p in paths if not os.path.isfile(p)]
    if missing:
        print("%s: cannot read %s — the gate stands on the document file."
              % (CHECK, ", ".join(missing)))
        return 1
    where = ", ".join(paths)   # what a fault line names: the file, or the files
    _read, text = sf.read_document(paths, expand=False)
    doc = sf.parse(text)

    body = _body_lines(doc)
    try:
        require_nonempty(CHECK, "the document's body lines", body)
    except VacuousInputError as e:
        print("%s: %s" % (CHECK, e))
        return 1

    problems = []
    for line_no, raw in body:
        # A code anchor like [INV-253] must not read as a "year"; blank bracketed groups first.
        s = re.sub(r"\[[^\]]*\]", " ", raw)
        for kind, rx in PATTERNS:
            m = rx.search(s)
            if m:
                problems.append("line %d carries a %s marker (`%s`) — the spec states today's "
                                "behaviour; dates, provenance, and past-choice reasons live in "
                                "JOURNAL.md (INV-253): %s"
                                % (line_no, kind, m.group(0).strip(), raw.strip()))
                break

    if problems:
        print("%s: %d history/provenance marker(s) in %s:" % (CHECK, len(problems), where))
        for p in problems:
            print("  - %s" % p)
        return 1

    print(sf.green_reach(CHECK, [os.path.basename(p) for p in paths], 0, len(body),
                         "no date or provenance marker in the body"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
