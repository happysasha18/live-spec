#!/usr/bin/env python3
"""check-doc-findings-bound.py — gate aa: no live document carries more findings than its record.

THE LAW (the owner's word, 2026-07-28 evening): a document repaired to zero stays at zero, on every
push, with no exception. A document still carrying findings never carries more than it did. The
direction of the count is down and never up.

WHAT IT READS. `guardrails/rule-census.json` holds one entry per live document with the count recorded
when it was last measured. `scripts/rule-census.py` measures the live set the same way for both, so the
record and the measure can never drift apart in method.

THE THREE VERDICTS.

  (a) measured == recorded, and recorded is 0  -> pass, and the document is named as held clean.
  (b) measured  < recorded                     -> pass, and the gate prints the re-seed command, so the
      lower number becomes the new ceiling rather than leaving headroom the next edit can spend.
  (c) measured  > recorded                     -> RED. A document recorded at 0 reds on its first
      finding, which is the uncompromising half of the law.

A live document missing from the record also reds: a new document is measured and recorded before it
can pass, so nothing enters the tree unmeasured.

WHY IT SITS AT THE PUSH. The census is a report and reports do not refuse anything. Between the morning
of 2026-07-28 and that evening one page rose from 107 findings to 112 with nothing noticing. This gate
is what noticing looks like.

Usage:
  check-doc-findings-bound.py                    push mode: the repository's own record and live set.
  check-doc-findings-bound.py --record FILE      read the record from FILE (fixtures).
  check-doc-findings-bound.py --root DIR         measure the live set under DIR (fixtures).
Exit 0 when every document sits at or under its record; exit 1 naming each document that rose.
Stdlib only.
"""
import argparse
import importlib.util
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
CENSUS = os.path.join(REPO_ROOT, "scripts", "rule-census.py")
RECORD = os.path.join(REPO_ROOT, "guardrails", "rule-census.json")

CHECK = "doc-findings-bound"


def load_census():
    """The census module itself, so the gate and the report measure by one definition."""
    spec = importlib.util.spec_from_file_location("rule_census", CENSUS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", default=RECORD)
    ap.add_argument("--root", default=REPO_ROOT)
    args = ap.parse_args(argv)

    try:
        with open(args.record, encoding="utf-8") as f:
            recorded = json.load(f)["files"]
    except (OSError, ValueError, KeyError) as e:
        print("FAIL (%s): cannot read the record %s (%s) — the record is this gate's whole ground, "
              "and a gate with no ground passes on everything." % (CHECK, args.record, e))
        return 1

    census = load_census()
    cap, cap_rule = census.load_word_cap()
    files = census.live_files(args.root)
    if not files:
        print("FAIL (%s): the live set came out empty, so this gate would pass on nothing." % CHECK)
        return 1

    rose, fell, held, unrecorded = [], [], [], []
    for rel in files:
        reading = census.measure(rel, cap, root=args.root)
        if "unread" in reading:
            print("FAIL (%s): %s refused to be read (%s)." % (CHECK, rel, reading["unread"]))
            return 1
        total = reading["total"]
        if rel not in recorded:
            unrecorded.append((rel, total))
            continue
        bound = recorded[rel]["total"]
        if total > bound:
            rose.append((rel, bound, total, reading))
        elif total < bound:
            fell.append((rel, bound, total))
        elif bound == 0:
            held.append(rel)

    for rel in held:
        print("  held clean: %s" % rel)
    for rel, bound, total in fell:
        print("  fell: %s — recorded %d, measured %d" % (rel, bound, total))
    if fell:
        print("  Lower the ceiling to what the text now measures:")
        print("    python3 scripts/rule-census.py --json guardrails/rule-census.json")

    if not rose and not unrecorded:
        print("OK (%s): %d live documents, %d held at zero, none above its record (cap %d, rule %s)."
              % (CHECK, len(files), len(held), cap, cap_rule))
        return 0

    for rel, total in unrecorded:
        print("FAIL (%s): %s is live and carries no entry in the record. Measure it into the record "
              "before it ships: python3 scripts/rule-census.py --json guardrails/rule-census.json"
              % (CHECK, rel))
    for rel, bound, total, reading in rose:
        if bound == 0:
            print("FAIL (%s): %s was repaired to zero and now carries %d finding(s). A cleared document "
                  "stays cleared." % (CHECK, rel, total))
        else:
            print("FAIL (%s): %s rose from %d to %d findings." % (CHECK, rel, bound, total))
        print("    long %d (longest sentence %d words), style %d, register %d"
              % (reading["long"], reading["longest"], reading["style"], reading["register"]))
    print("  Fix: repair the text, or read `python3 scripts/rule-census.py %s` to see each finding."
          % (rose[0][0] if rose else ""))
    return 1


if __name__ == "__main__":
    sys.exit(main())
