#!/usr/bin/env python3
"""check-one-name.py — the one-name-per-thing gate (SPEC INV-255).

UNARMED until the spec-format conversion delivery (INV-270); no default file, the document is named on
the command line.

THE LAW (FORMAT.md law 2, INV-255): one artifact carries one name everywhere in the document; an
artifact referenced under two names is a defect. A script cannot know from free prose that two nouns
denote one thing, so the known two-name pairs live in a data file `guardrails/one-name-aliases.json`:
each artifact has one canonical name and the aliases a draft might slip into. Any alias in the document
reds, pointing at the canonical name. The list grows as the cold-reader panel (Area 5) catches a new
two-name drift and adds the pair.

NOT MECHANICALLY CHECKED (reported): a two-name drift the alias file does not yet know is the panel's
catch, not this lint's — the machine holds the pairs already learned.

Usage:
  check-one-name.py <document.md> [<part.md> ...]
  ONE_NAME_ALIASES overrides the alias-list path (the suite points it at a fixture list).
Exit 0 when no known alias appears (printing the reach line, INV-269); exit 1 naming each alias found.
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

CHECK = "check-one-name"
ALIASES_PATH = os.environ.get("ONE_NAME_ALIASES", os.path.join(SCRIPT_DIR, "one-name-aliases.json"))


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

    cfg = {}
    if os.path.isfile(ALIASES_PATH):
        cfg = json.load(open(ALIASES_PATH, encoding="utf-8"))
    artifacts = cfg.get("artifacts", [])

    # The input set the gate expects non-empty: the alias groups it scans for. An empty alias file
    # would let the gate pass over nothing (INV-218).
    try:
        require_nonempty(CHECK, "the one-name alias groups", artifacts)
    except VacuousInputError as e:
        print("%s: %s" % (CHECK, e))
        return 1

    text_low = text.lower()
    problems = []
    scanned = 0
    for art in artifacts:
        canonical = art["canonical"]
        for alias in art.get("aliases", []):
            scanned += 1
            for m in re.finditer(r"\b%s\b" % re.escape(alias.lower()), text_low):
                line_no = text[: m.start()].count("\n") + 1
                problems.append("line %d references `%s` as `%s` — one artifact carries one name; "
                                "use `%s` (INV-255)." % (line_no, canonical, alias, canonical))

    if problems:
        print("%s: %d two-name violation(s) in %s:" % (CHECK, len(problems), where))
        for p in problems:
            print("  - %s" % p)
        return 1

    print(sf.green_reach(CHECK, [os.path.basename(p) for p in paths], 0, scanned,
                         "no known alias present across %d alias(es) of %d artifact(s)"
                         % (scanned, len(artifacts))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
