#!/usr/bin/env python3
"""check-vocabulary.py — the closed-vocabulary gate (SPEC INV-254).

UNARMED until the spec-format conversion delivery (INV-270); no default file, the document is named on
the command line.

THE LAW (FORMAT.md law 1, INV-254): every domain noun the document deals in holds exactly ONE glossary
entry, and a coined word is translated to a defined standard term before it enters the document. This
gate holds the mechanically-decidable half of that law:

  - ONE ENTRY PER TERM. A glossary term defined twice reds — a thing carries one definition, not two.
  - NO DEAD ENTRY. A glossary term no body line uses reds (the gates-plan red case: "a glossary entry
    no body line uses") — a closed vocabulary carries only nouns the body actually deals in.
  - NO BANNED COINAGE. A coined word from `guardrails/spec-coinages.json` appearing anywhere in the
    document reds, naming the coinage and its standard replacement.

NOT MECHANICALLY CHECKED (reported, never silently skipped): the converse direction — "every domain
noun USED in the body has an entry" — is undecidable, because no script can enumerate which nouns in
free prose are domain nouns as against ordinary English (INV-254's own glossary draws that line by
hand). The cold-reader panel (Area 5) catches an undefined domain noun a reader trips on; the coinage
list is the machine's growing net for the ones already known.

Usage:
  check-vocabulary.py <document.md> [<part.md> ...]
  VOCAB_COINAGES overrides the coinage-list path (the suite points it at a fixture list).
Exit 0 on a closed vocabulary (printing the reach line, INV-269); exit 1 naming each violation.
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

CHECK = "check-vocabulary"
COINAGES_PATH = os.environ.get("VOCAB_COINAGES", os.path.join(SCRIPT_DIR, "spec-coinages.json"))


def _body_text(doc):
    """The requirements body (everything from the first requirement on) — where a term is 'used'.
    The glossary's own definition lines are excluded, so a term is not counted as using itself."""
    if not doc.requirements:
        return ""
    start = doc.requirements[0].line_no - 1
    return "\n".join(doc.text.split("\n")[start:])


def _norm_words(s):
    """Lowercase words with separators (space, hyphen, dot) unified — so `project.layers` and
    `project layers` read as the same two words."""
    return re.findall(r"[a-z0-9]+", s.lower())


def _uses(body_words, term):
    """True when the term is used in the body. A used term has all its significant words present in
    the body (separators unified, case-folded): `project layers` is used by `project.layers`, and
    `founding-question set` by the body's `founding`, `question`, and `set`. A fully-orphaned entry —
    a term none of whose distinctive words appear — reds. The contiguous-phrase subtlety is the
    cold-reader panel's, not this lint's (INV-254)."""
    # No source behind the exact 3 (2026-08-07 census, row 15); an engineering default, not a
    # policy decision.
    words = [w for w in _norm_words(term) if len(w) >= 3] or _norm_words(term)
    return all(w in body_words for w in words)


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

    try:
        require_nonempty(CHECK, "the glossary terms", doc.glossary_terms)
    except VacuousInputError as e:
        print("%s: %s" % (CHECK, e))
        return 1

    coinages = {}
    if os.path.isfile(COINAGES_PATH):
        cfg = json.load(open(COINAGES_PATH, encoding="utf-8"))
        coinages = cfg.get("coinages", {})

    problems = []

    # ONE ENTRY PER TERM.
    seen = {}
    for term, _def, line_no in doc.glossary:
        key = term.lower()
        if key in seen:
            problems.append("the term `%s` holds two glossary entries (lines %d and %d) — a domain "
                            "noun is defined once (INV-254)." % (term, seen[key], line_no))
        else:
            seen[key] = line_no

    # NO DEAD ENTRY.
    body_words = set(_norm_words(_body_text(doc)))
    scanned = len(doc.glossary_terms)
    used = 0
    for term in doc.glossary_terms:
        if _uses(body_words, term):
            used += 1
        else:
            problems.append("the glossary defines `%s` but no body line uses it — a closed "
                            "vocabulary carries only nouns the body deals in (INV-254)." % term)

    # NO BANNED COINAGE.
    doc_low = text.lower()
    for coinage, replacement in sorted(coinages.items()):
        if re.search(r"\b%s\b" % re.escape(coinage.lower()), doc_low):
            problems.append("the document carries the coined word `%s` — translate it to the "
                            "standard term `%s` before it enters (INV-254)." % (coinage, replacement))

    if problems:
        print("%s: %d vocabulary violation(s) in %s:" % (CHECK, len(problems), where))
        for p in problems:
            print("  - %s" % p)
        return 1

    print(sf.green_reach(CHECK, [os.path.basename(p) for p in paths], used, scanned,
                         "every glossary term used in the body; no banned coinage present"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
