#!/usr/bin/env python3
"""check-size-ratchet.py — the bytes-per-criterion ratchet gate (SPEC INV-264, INV-265).

UNARMED until the spec-format conversion delivery (INV-270). The document is named on the command line;
the recorded bound lives in `guardrails/spec-ratchet.json`.

THE LAW (INV-264). The spec document records a bytes-per-criterion bound — the byte count of its
criterion lines alone (glossary and preamble bytes excluded) divided by the count of criteria in its
body. A delivery may lower the bound or leave it; a delivery whose new bytes-per-criterion is ABOVE the
recorded bound reds. Raising the bound is a change to Requirement 280, run through the pipeline; no
delivery raises it on its own (INV-265). The ratchet governs PRODUCT_SPEC.md alone.

THE UNSEEDED STATE. The initial bound is the value measured at the migration-end freeze, recorded by
the freeze actor (INV-264 criterion 3). Before that freeze the spec is not yet in the requirements
format, so `bytes_per_criterion` is null: the gate reads it as "not yet seeded" and PASSES with the
config's stated reason rather than red-ing on an absent bound. This gate never writes the config —
seeding and lowering the recorded bound are the freeze actor's step, not a side effect of a check.

Usage:
  check-size-ratchet.py <document.md> [<part.md> ...]
  RATCHET_CONFIG overrides the config path (the suite points it at a fixture bound).
Exit 0 when the bound is unseeded, or the new bytes-per-criterion is at or below it (printing the reach
line, INV-269); exit 1 when it is above. Stdlib only.
"""
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import specformat as sf  # noqa: E402
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402

CHECK = "check-size-ratchet"
CONFIG_PATH = os.environ.get("RATCHET_CONFIG", os.path.join(SCRIPT_DIR, "spec-ratchet.json"))


def bytes_per_criterion(doc):
    """The byte count of the document's criterion lines alone, divided by the count of criteria."""
    crits = doc.criteria
    total = sum(sf.criterion_bytes(c.text) for c in crits)
    return total, len(crits)


def main(argv):
    if len(argv) < 2:
        print("%s: usage: %s <document.md> [<part.md> ...]" % (CHECK, os.path.basename(argv[0])))
        return 2
    # The document may arrive as a core plus its parts (specformat's parts map). The ratchet measures
    # the whole document, so it reads the concatenation; with no parts this is the single file.
    paths = sf.spec_paths(argv[1:])
    missing = [p for p in paths if not os.path.isfile(p)]
    if missing:
        print("%s: cannot read %s — the gate stands on the document file."
              % (CHECK, ", ".join(missing)))
        return 1
    names = [os.path.basename(p) for p in paths]
    _read, text = sf.read_document(paths, expand=False)
    doc = sf.parse(text)

    try:
        crits = require_nonempty(CHECK, "the document's criteria", doc.criteria)
    except VacuousInputError as e:
        print("%s: %s" % (CHECK, e))
        return 1

    total_bytes, count = bytes_per_criterion(doc)
    bpc = total_bytes / count

    if not os.path.isfile(CONFIG_PATH):
        print("%s: no ratchet config at %s — the gate cannot read the recorded bound (INV-264)."
              % (CHECK, CONFIG_PATH))
        return 1
    cfg = json.load(open(CONFIG_PATH, encoding="utf-8"))
    bound = cfg.get("bytes_per_criterion", None)

    if bound is None:
        print("%s: OK (bound not yet seeded) — measured %.1f bytes/criterion over %d criteria in %s. "
              "%s. reach: files=[%s, %s]; scanned %d criteria."
              % (CHECK, bpc, count, ", ".join(names),
                 cfg.get("reason", "the bound is seeded at the migration-end freeze (INV-264)"),
                 ", ".join(names), os.path.basename(CONFIG_PATH), count))
        return 0

    if bpc > bound:
        print("%s: the document's bytes-per-criterion is %.1f, above the recorded bound of %.1f — the "
              "ratchet moves only down; a delivery may not raise it (INV-264/INV-265). Tighten the "
              "prose or, to raise the bound, change Requirement 4 through the pipeline."
              % (CHECK, bpc, bound))
        return 1

    note = "at or below the recorded bound %.1f" % bound
    if bpc < bound:
        note += " — the freeze actor lowers the recorded bound to %.1f at freeze (INV-264 c7)" % bpc
    print(sf.green_reach(CHECK, names + [os.path.basename(CONFIG_PATH)],
                         count, count,
                         "%.1f bytes/criterion %s" % (bpc, note)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
