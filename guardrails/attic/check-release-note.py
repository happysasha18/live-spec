#!/usr/bin/env python3
"""check-release-note.py — a release note may offer the reader next-step choices, and the walk records
the offer-or-none decision (SPEC INV-228, ROADMAP 402).

PARKED 2026-08-18 in `guardrails/attic/`, with `release-note-fixtures/` beside it. By design it never
joined the push chain, and the publish walk has never handed it a real note, so the only records it has
ever read are its own three fixtures. Its suite still drives it here.

A GitHub changelog / release note is a human-facing surface the reader opens himself — the release-note
touchpoint the frame declares [INV-205]: asynchronous, person-opened, a human audience with no answer
needed. On such a surface an OFFER is afforded — appealing next steps the reader may take, phrased as
CHOICES and never instructions. The offers section is OPTIONAL, so a release with no worthwhile next
step owes none; but the offer-or-none decision must be RECORDED, so the walk never silently forgets to
consider it.

This checker reads one release-note record and reds when the offer-or-none decision is left unrecorded —
a record that neither offers a next step nor records "no offer". A record that offers, or records "none"
by name, passes. The record's regions are keyed by machine markers, so a human's wording stays free:

  <!-- release-note:offers -->  ... offer lines (choices) ...  <!-- /release-note:offers -->
  <!-- release-note:no-offer -->   the recorded "no offer" decision

An offers region carrying at least one offer line is an offer; the no-offer marker is a recorded none;
a record with neither leaves the decision unrecorded and reds.

This checker is NOT in the pre-push chain. The release note the publish walk produces is a process
artifact the walk records at runtime, and no committed release-note file exists in the tree for a push
gate to scan — the sibling of the far-tier report-shape check [INV-83]. The suite drives it over
fixtures to red-prove the shape; the publish walk drives it over the release note it prepares.

Usage:
  check-release-note.py --note FILE    validate one release-note record's offer-or-none decision.
"""
import argparse
import re
import sys

OFFERS = re.compile(
    r"<!--\s*release-note:offers\s*-->(.*?)<!--\s*/release-note:offers\s*-->", re.S)
NO_OFFER = re.compile(r"<!--\s*release-note:no-offer\s*-->")
# an offer line inside the offers region: a bullet naming a choice the reader may take. Offers are
# phrased as a list of choices, so a bullet is the shape; a region holding only prose or whitespace
# carries no recorded choice and reds (an offer is stated as a choice, not buried in a paragraph).
OFFER_LINE = re.compile(r"^\s*[-*]\s+\S", re.M)


def check_note(path):
    """Return a list of violation strings for one release-note record."""
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()

    m = OFFERS.search(text)
    has_offer = bool(m and OFFER_LINE.search(m.group(1)))
    records_none = bool(NO_OFFER.search(text))

    if has_offer or records_none:
        return []
    return [
        "INV-228: the release note leaves the offer-or-none decision unrecorded — it neither offers a "
        "next-step choice (a non-empty `<!-- release-note:offers -->` region) nor records `no offer` "
        "(a `<!-- release-note:no-offer -->` line). A release may owe no offer, but the decision is "
        "recorded, never silently skipped."
    ]


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--note", required=True)
    args = ap.parse_args(argv)

    violations = check_note(args.note)
    if violations:
        print("FAIL (release-note): the offer-or-none decision is unrecorded (SPEC INV-228):")
        for v in violations:
            print("  " + v)
        print("  Fix: offer the reader appealing next-step choices in a "
              "`<!-- release-note:offers -->` region, or record `<!-- release-note:no-offer -->` when "
              "this release has none. Choices, never instructions — the reader opens the note himself.")
        return 1

    print("OK (release-note): the offer-or-none decision is recorded — the note offers a next step or "
          "records none by name (INV-228).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
