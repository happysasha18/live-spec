#!/usr/bin/env python3
"""check-delta-record.py — the delta classifier (SPEC INV-260, INV-261, INV-262, INV-263).

UNARMED until the spec-format conversion delivery (INV-270). The old document, the new document, and
the delta record are named on the command line.

THE DELTA RECORD FILE FORMAT. A spec-touching delivery carries a delta record — a JSON file kept under
`docs/deltas/` (one per delivery, e.g. `docs/deltas/2026-07-22-row445.json`). Its shape:

    {
      "baseline": "<informational: the freeze the old set came from>",
      "codes": {
        "INV-300": "new",           # a code the body did not carry before
        "INV-4":   "sharpen",       # a code whose criterion text changed
        "INV-99":  "retire",        # a code the body no longer carries
        "INV-5":   "scenario-only"  # a code whose text is unchanged; only its cases/examples moved
      }
    }

Every touched code names exactly one of the four kinds (INV-260). The classifier diffs the old criteria
set against the new one and reds where the record and the diff disagree.

THE DIFF, under normalization (INV-261). Each criterion is keyed by its code and its criterion text;
the text is normalized — whitespace collapsed, italic `*` markers stripped, letters case-folded
OUTSIDE code anchors (specformat.normalize_criterion). A difference that survives normalization is a
text change; any other difference is none. Then:

  - a code in the OLD set and absent from the NEW with no `retire` declared reds (INV-261 c3);
  - a code in the NEW set and absent from the OLD with no `new` declared reds (INV-261 c4);
  - a code whose criterion text differs under normalization with no `sharpen` declared reds (INV-261 c5).

SHARPEN SURVIVAL (INV-262). A `sharpen` code is checked by a normalized full-sentence match: its own
new criterion line must no longer equal its old text (else nothing was sharpened), and its OLD sentence
must not survive that match ANYWHERE in the new document (else the old wording lingers). Either fault
reds.

GROWTH BUDGET (INV-263). The new-criteria budget is the byte sum of the declared new criteria. The
classifier measures the document's criterion-byte growth over the delivery, EXCLUDING declared-sharpen
byte deltas and glossary-addition bytes (glossary bytes are never criterion bytes, so they fall out by
construction), and reds when the measured growth exceeds the budget.

Usage:
  check-delta-record.py <old.md> <new.md> <record.json>
Exit 0 when the record and the diff agree within budget (printing the reach line, INV-269); exit 1
naming each disagreement. Stdlib only.
"""
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import specformat as sf  # noqa: E402
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402

CHECK = "check-delta-record"


def _code_texts(doc):
    """code -> list of {norm, raw, bytes} for each criterion carrying it.

    The NORMALIZED text is the criterion's SENTENCE — its body with the trailing code anchor stripped
    (specformat.normalize_criterion over c.body). The code is keyed separately, so the anchor is not
    part of the sentence a diff or a survival match reads: the same sentence under a different code
    survives, exactly as INV-262's full-sentence match intends. BYTES stay on the full criterion line
    (c.text), the ratchet-and-budget unit (INV-263/INV-264)."""
    out = {}
    for c in doc.criteria:
        entry = {"norm": sf.normalize_criterion(c.body), "raw": c.text, "bytes": sf.criterion_bytes(c.text)}
        for code in c.codes:
            out.setdefault(code, []).append(entry)
    return out


def _norm_set(doc):
    return {sf.normalize_criterion(c.body) for c in doc.criteria}


def _total_bytes(doc):
    return sum(sf.criterion_bytes(c.text) for c in doc.criteria)


def main(argv):
    if len(argv) != 4:
        print("%s: usage: %s <old.md> <new.md> <record.json>" % (CHECK, os.path.basename(argv[0])))
        return 2
    old_path, new_path, rec_path = argv[1], argv[2], argv[3]
    for p in (old_path, new_path, rec_path):
        if not os.path.isfile(p):
            print("%s: cannot read %s — the classifier stands on the old doc, the new doc, and the "
                  "delta record." % (CHECK, p))
            return 1
    with open(old_path, encoding="utf-8") as f:
        old = sf.parse(f.read())
    with open(new_path, encoding="utf-8") as f:
        new = sf.parse(f.read())
    with open(rec_path, encoding="utf-8") as f:
        record = json.load(f)
    declared = record.get("codes", {})

    old_ct, new_ct = _code_texts(old), _code_texts(new)
    old_codes, new_codes = set(old_ct), set(new_ct)

    try:
        require_nonempty(CHECK, "the new document's criteria", new.criteria)
    except VacuousInputError as e:
        print("%s: %s" % (CHECK, e))
        return 1

    problems = []

    def kind(code):
        return declared.get(code)

    # INV-261 c4: appeared codes must be declared `new`.
    for code in sorted(new_codes - old_codes, key=sf.code_sort_key):
        if kind(code) != "new":
            problems.append("`%s` is in the new criteria set and absent from the old, but the delta "
                            "record declares it %s, not `new` (INV-261)." % (code, kind(code) or "nothing"))

    # INV-261 c3: disappeared codes must be declared `retire`.
    for code in sorted(old_codes - new_codes, key=sf.code_sort_key):
        if kind(code) != "retire":
            problems.append("`%s` is in the old criteria set and absent from the new, but the delta "
                            "record declares it %s, not `retire` (INV-261)." % (code, kind(code) or "nothing"))

    # INV-261 c5: a code whose text changed under normalization must be declared `sharpen`.
    new_norm_all = _norm_set(new)
    for code in sorted(old_codes & new_codes, key=sf.code_sort_key):
        old_norms = {e["norm"] for e in old_ct[code]}
        new_norms = {e["norm"] for e in new_ct[code]}
        changed = old_norms != new_norms
        k = kind(code)
        if changed and k != "sharpen":
            problems.append("`%s`'s criterion text differs under normalization between old and new, "
                            "but the delta record declares it %s, not `sharpen` (INV-261)."
                            % (code, k or "nothing"))
        if k == "sharpen":
            # INV-262: the sharpened code's own line no longer equals its old text.
            if not changed:
                problems.append("`%s` is declared `sharpen` but its criterion text is unchanged under "
                                "normalization — nothing was sharpened (INV-262)." % code)
            # INV-262: the OLD sentence must not survive anywhere in the new document.
            survived = sorted(o for o in old_norms if o in new_norm_all)
            if survived:
                problems.append("`%s` is declared `sharpen` but its old sentence survives a normalized "
                                "full-sentence match in the new document — the old wording lingers "
                                "(INV-262)." % code)
        if k == "scenario-only" and changed:
            problems.append("`%s` is declared `scenario-only` but its criterion text changed under "
                            "normalization — a text change is a `sharpen`, not scenario-only (INV-261)." % code)

    # INV-263: the growth budget from declared-new criteria.
    new_declared = {c for c, v in declared.items() if v == "new"}
    sharpen_declared = {c for c, v in declared.items() if v == "sharpen"}

    budget = 0
    seen_new_lines = set()
    for code in sorted(new_declared, key=sf.code_sort_key):
        for e in new_ct.get(code, []):
            if e["norm"] in seen_new_lines:
                continue                     # a criterion carrying two new codes is counted once
            seen_new_lines.add(e["norm"])
            budget += e["bytes"]

    # Growth of criterion bytes, excluding declared-sharpen byte deltas.
    growth = _total_bytes(new) - _total_bytes(old)
    sharpen_delta = 0
    for code in sharpen_declared:
        old_b = sum(e["bytes"] for e in old_ct.get(code, []))
        new_b = sum(e["bytes"] for e in new_ct.get(code, []))
        sharpen_delta += (new_b - old_b)
    measured_growth = growth - sharpen_delta
    if measured_growth > budget:
        problems.append("the document's criterion-byte growth over the delivery is %d bytes "
                        "(sharpen deltas excluded), over the declared new-criteria budget of %d bytes "
                        "(INV-263)." % (measured_growth, budget))

    touched = len(new_codes ^ old_codes) + len(
        [c for c in (old_codes & new_codes) if {e["norm"] for e in old_ct[c]} != {e["norm"] for e in new_ct[c]}])

    if problems:
        print("%s: %d delta disagreement(s):" % (CHECK, len(problems)))
        for p in problems:
            print("  - %s" % p)
        return 1

    print(sf.green_reach(CHECK, [os.path.basename(old_path), os.path.basename(new_path),
                                 os.path.basename(rec_path)],
                         touched, len(new.criteria),
                         "%d touched code(s) reconciled with the record; growth %d B within budget %d B"
                         % (touched, measured_growth, budget)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
