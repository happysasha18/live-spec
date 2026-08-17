#!/usr/bin/env python3
"""check-index-prose.py — a Formal-index code is carried in its home prose (SPEC INV-218). Retired
from gate x at the row-445 conversion, superseded by check-index-generated.py; this script still
ships for its fixture red-proofs.

PARKED 2026-08-18 in `guardrails/attic/`. On the real tree it exits 1 and always will: PRODUCT_SPEC.md
has carried no `## Formal index` section since the row-445 conversion, so the section this gate parses
is gone. Its fixture red-proofs still run from here. Moving it back is one `git mv` plus the two path
lines below.

The first named instance of the vacuous-pass law (SPEC INV-218, ROADMAP 384). The Formal index
promises code → home: every anchor in the index is defined somewhere in the spec's prose. Today
`tests/test_traceability.py::test_spec_index_unique_anchors` checks uniqueness alone, so an index
row pointing at an EMPTY home — an anchor the prose never carries — passes. That is exactly the
defect the drafter's self-catch hit: minted codes absent from the prose, a scan comparing zero
against zero and reporting clean.

This gate declares its input set with the shared shape `guardrails/nonempty_input.py`: the
Formal-index anchors are expected non-empty, so an index that parses to zero anchors (the parser
broke, the section moved, the header was renamed) REDS BY NAME rather than passing over nothing.
Then, for each index anchor, it demands the prose body carries it — a range citation in the prose
(`T-1..T-7`) counting for its members, since the index states such a state group as one range.
An index anchor whose home prose never carries it reds, naming the anchor.

The gate reads PRODUCT_SPEC.md by default; `INDEX_PROSE_SPEC` overrides the path (the red-proof
points it at a fixture whose index is empty, and at one whose index anchor has no home). Kin of
the traceability suite's index checks, promoted to a push gate so the vacuous-pass never slips
back in between commits.
"""
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GUARDRAILS_DIR = os.path.dirname(SCRIPT_DIR)   # the script sits in guardrails/attic/ since 2026-08-18
REPO_ROOT = os.path.dirname(GUARDRAILS_DIR)
sys.path.insert(0, GUARDRAILS_DIR)
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402

SPEC_PATH = os.environ.get("INDEX_PROSE_SPEC", os.path.join(REPO_ROOT, "PRODUCT_SPEC.md"))
CHECK = "check-index-prose"

ANCHOR = r"[A-Z]+-[0-9]+"
INDEX_ANCHOR = r"[A-Z]+-[0-9]+(?:\.\.[A-Z]*-?[0-9]+)?"


def expand(anchor):
    """T-1..T-7 -> [T-1 ... T-7]; a plain anchor passes through."""
    m = re.match(r"([A-Z]+)-(\d+)\.\.(?:[A-Z]+-)?(\d+)$", anchor)
    if m:
        prefix, lo, hi = m.group(1), int(m.group(2)), int(m.group(3))
        return ["%s-%d" % (prefix, i) for i in range(lo, hi + 1)]
    return [anchor]


def main():
    if not os.path.isfile(SPEC_PATH):
        print("index-prose: cannot read %s — the gate stands on the spec file." % SPEC_PATH)
        return 1
    with open(SPEC_PATH, encoding="utf-8") as f:
        spec = f.read()

    if "## Formal index" not in spec:
        print("index-prose: %s carries no `## Formal index` section — the gate cannot read the "
              "index anchors (a vacuous pass, SPEC INV-218). The section moved or the header was "
              "renamed." % SPEC_PATH)
        return 1
    body, index = spec.split("## Formal index", 1)

    # The expected-non-empty input set: the Formal-index anchors, ranges expanded.
    raw = re.findall(r"^\| (%s) \|" % INDEX_ANCHOR, index, re.M)
    anchors = set()
    for a in raw:
        anchors.update(expand(a))
    try:
        require_nonempty(CHECK, "the Formal-index anchors", anchors)
    except VacuousInputError as e:
        print("index-prose: %s" % e)
        return 1

    # The home set: every anchor named literally in the prose body, plus every member of a range
    # citation the body carries (the index states some state groups as one range).
    carried = set(re.findall(ANCHOR, body))
    for rng in re.findall(r"%s\.\.[A-Z]*-?[0-9]+" % ANCHOR, body):
        carried.update(expand(rng))

    homeless = sorted(a for a in anchors if a not in carried)
    if homeless:
        print("index-prose: %d Formal-index anchor(s) whose home prose never carries them — the "
              "index promises code → home, and these point at an empty home (SPEC INV-218): %s"
              % (len(homeless), ", ".join(homeless)))
        return 1

    print("index-prose: OK (%d Formal-index anchors, each carried in its home prose)." % len(anchors))
    return 0


if __name__ == "__main__":
    sys.exit(main())
