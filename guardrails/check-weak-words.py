#!/usr/bin/env python3
"""check-weak-words.py — the weak-word gate (SPEC INV-256).

UNARMED until the spec-format conversion delivery (INV-270); no default file, the document is named on
the command line.

THE LAW (FORMAT.md law 5, INV-256): a relational word — proportional, larger, sufficient, fast, and
their kind — opens a slot the criterion must fill where the word stands: the reference point, the
measure, or the reason. A weak word standing with an unfilled slot and no `[GAP]` line reds.

The seeded list lives in `guardrails/weak-words.json`, seeded from the ISO 29148 and INCOSE vague-term
lists plus the project's own additions. A criterion's weak word is EXCUSED when the criterion carries a
reference cue from the same file (a number, a comparison, a measure, `than`, `at least`, …) or a
`[GAP]` line — a plausibly-filled slot. A weak word with neither reds, naming the word and the
criterion. The close read — is the filled slot the RIGHT reference — is the cold-reader panel's, not
this lint's (Area 5); this gate holds the mechanical floor.

Usage:
  check-weak-words.py <document.md> [<part.md> ...]
  WEAK_WORDS overrides the list path (the suite points it at a fixture list).
Exit 0 when no weak word stands unfilled (printing the reach line, INV-269); exit 1 naming each.
Stdlib only.
"""
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import specformat as sf  # noqa: E402
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402

CHECK = "check-weak-words"
WORDS_PATH = os.environ.get("WEAK_WORDS", os.path.join(SCRIPT_DIR, "weak-words.json"))


def _has_reference(crit, cues):
    """True when the criterion carries a filled-slot signal: a digit, a reference cue, or a GAP line."""
    text = crit.body.lower()
    if re.search(r"\d", text):
        return True
    if any(cue.lower() in text for cue in cues):
        return True
    if crit.gap_lines:
        return True
    return False


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

    cfg = {}
    if os.path.isfile(WORDS_PATH):
        cfg = json.load(open(WORDS_PATH, encoding="utf-8"))
    weak = cfg.get("weak_words", [])
    cues = cfg.get("reference_cues", [])

    try:
        require_nonempty(CHECK, "the document's criteria", doc.criteria)
    except VacuousInputError as e:
        print("%s: %s" % (CHECK, e))
        return 1
    try:
        require_nonempty(CHECK, "the weak-word list", weak)
    except VacuousInputError as e:
        print("%s: %s" % (CHECK, e))
        return 1

    patterns = [(w, re.compile(r"\b%s\b" % re.escape(w.lower()))) for w in weak]
    problems = []
    scanned = 0
    for crit in doc.criteria:
        scanned += 1
        body_low = crit.body.lower()
        hits = [w for (w, rx) in patterns if rx.search(body_low)]
        if hits and not _has_reference(crit, cues):
            problems.append("Requirement %d criterion %d (line %d) uses the weak word(s) %s with no "
                            "reference point, measure, or reason nearby and no [GAP] line — fill the "
                            "slot where the word stands, or record the hole (INV-256)."
                            % (crit.req_num, crit.number, crit.line_no, ", ".join(sorted(set(hits)))))

    if problems:
        print("%s: %d weak-word violation(s) in %s:" % (CHECK, len(problems), where))
        for p in problems:
            print("  - %s" % p)
        return 1

    print(sf.green_reach(CHECK, [os.path.basename(p) for p in paths], scanned, scanned,
                         "no weak word stands with an unfilled slot"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
