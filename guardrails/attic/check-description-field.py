#!/usr/bin/env python3
"""check-description-field.py — the Formal-index non-empty description-field gate (SPEC INV-239, M-421).

BLOCKING when armed; a self-declared DORMANT no-op until then.

PARKED 2026-08-18 in `guardrails/attic/`, with its arming switch `description-field.json` beside it. Its
switch has stood at `armed: false` its whole life, so every run it has ever made printed "OK (dormant)"
and no run could red. The back-describe landing that would have armed it never came; the row-445
conversion removed the description column it was built to read. Returning the pair is one move.

WHERE IT LIVES. This gate RIDES THE SUITE (gate b) and takes NO push-gate letter, the same placement
check-far-tier.py and check-board.py's own suite test take: its enforcement is a suite test
(tests/test_description_field.py) that runs it against the REAL tree and asserts the expected result,
so a real violation reds the suite and gate b blocks the push. It is NOT wired into the pre-push chain
directly, so the letter-counting meta-guards (INV-210 CI mirror, INV-212 every-gate-can-fail) need not
see it — a suite-riding check carries no gate letter, and its known-red proof is the red-first test the
suite runs, not a gate-red-proofs.json entry.

THE LAW behind it (E-35, INV-239). Every reference to an internal item carries a pair — its stable
code beside a plain one-sentence description — and that description's one home is a dedicated field
the Formal index gains, written once there and read by every reference [base rule 4]. This gate is
that field's mechanical net, pinned to a PRESENCE check: it asserts every registered code in the
Formal index carries a non-empty description field and reds a code whose field is empty, naming the
code. It judges presence ALONE — whether the description reads well, or semantically matches the
item, is the human sampling net below [INV-41], never the machine's, because a semantic match on a
translated, reformulated sentence is undecidable and no gate can rule on it.

DORMANT UNTIL ARMED (folded finding N5, INV-217). The existing code set carries no rich descriptions
yet — the back-describe migration that gives every already-registered code its plain-description line
is a future his-gated landing [INV-217]. Until that landing the description field stands empty for the
whole tree, so an armed gate would red everything. The gate therefore ships DORMANT and reads its
arming state from `guardrails/attic/description-field.json`: with `armed: false` it prints an OK-dormant line
and exits 0; the migration flips it to true in the same landing that back-describes the code set, and
only then does the gate enforce. This is the sibling of the index-prose gate's vacuous-pass guard
[INV-218]: a check that would red the whole tree before its subject exists is turned off by name, not
left to false-red.

THE DESCRIPTION FIELD's SHAPE. The field is a dedicated `Description` column the Formal-index table
gains — `| Anchor | One line | Description | Section |`. The terse `One line` map stays the machine
handle's home; the `Description` column is the human-clear one-sentence line the pair law owns. Before
the migration the column is absent, which is exactly why the armed gate would red the whole tree and
why it ships dormant.

Usage:
  check-description-field.py
    Reads guardrails/attic/description-field.json (the arming switch) and PRODUCT_SPEC.md's Formal index.
    DESCRIPTION_FIELD_CONFIG overrides the config path; DESCRIPTION_FIELD_SPEC overrides the spec path
    (the suite points both at fixtures, so the real config is never flipped).
Exit 0 when dormant, or when armed and every registered code carries a non-empty description; exit 1
when armed and a code's field is empty (or the field/section is missing). Stdlib only.
"""
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GUARDRAILS_DIR = os.path.dirname(SCRIPT_DIR)   # the script sits in guardrails/attic/ since 2026-08-18
REPO_ROOT = os.path.dirname(GUARDRAILS_DIR)
sys.path.insert(0, GUARDRAILS_DIR)
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402

# The arming switch travelled with the gate, so returning the pair is one move.
CONFIG_PATH = os.environ.get("DESCRIPTION_FIELD_CONFIG",
                             os.path.join(SCRIPT_DIR, "description-field.json"))
SPEC_PATH = os.environ.get("DESCRIPTION_FIELD_SPEC", os.path.join(REPO_ROOT, "PRODUCT_SPEC.md"))
CHECK = "check-description-field"

INDEX_ANCHOR = re.compile(r"^[A-Z]+-[0-9]+(?:\.\.[A-Z]*-?[0-9]+)?$")

# Words that fill a field without naming anything — the same placeholder family the earned-message
# gate refuses. A description that says only this is empty in spirit.
PLACEHOLDER = re.compile(
    r"^\s*(?:tbd|todo|n/?a|none|-+|\.+|<[^>]*>|placeholder|fixme)\s*\.?\s*$", re.IGNORECASE)

# A plain word: a run of at least two letters. The presence floor is the SAME the deposit lint
# (check-deposit-description.py) uses — at least two plain words — so both presence nets read one
# floor. It stays presence-only: a single character or a lone digit is not a description, whether or
# not the words that do stand there describe the code (the semantic read is the human net, INV-41).
WORD = re.compile(r"[A-Za-z]{2,}")
MIN_WORDS = 2


def _is_present(text):
    """True when a description field carries a minimal real description — past the placeholder set and
    at least MIN_WORDS plain words. Presence only, never a correctness check."""
    if not text or PLACEHOLDER.match(text):
        return False
    return len(WORD.findall(text)) >= MIN_WORDS


def _armed():
    """(armed, note): read the arming switch. A missing or malformed config is treated as DORMANT and
    never as a false red — the gate's dormancy is the safe default until the migration writes it."""
    if not os.path.isfile(CONFIG_PATH):
        return False, "no config at %s — treated as dormant" % CONFIG_PATH
    try:
        cfg = json.load(open(CONFIG_PATH, encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        return False, "config unreadable (%s) — treated as dormant" % e
    return bool(cfg.get("armed", False)), cfg.get("reason", "")


def _table_cells(row):
    """A markdown table row's cells, trimmed, outer pipes dropped."""
    return [c.strip() for c in row.strip().strip("|").split("|")]


def _index_rows(spec):
    """(header_cells_lower, [(anchor, raw_cells)]) for the Formal index, or (None, []) if absent.

    Rows carry their RAW cell list, never a header→cell dict: a short row (one that omits its
    description cell) must stay short so the caller reds it, and a dict-zip would silently drop the
    missing cell and slide the Section text into the description slot (the false pass this parser was
    corrected to catch)."""
    if "## Formal index" not in spec:
        return None, []
    index = spec.split("## Formal index", 1)[1]
    header = None
    rows = []
    for line in index.splitlines():
        s = line.strip()
        if not (s.startswith("|") and s.endswith("|")):
            continue
        cells = _table_cells(line)
        if header is None:
            if cells and cells[0].lower() == "anchor":
                header = [c.lower() for c in cells]
            continue
        if set("".join(cells)) <= set("-: "):  # the |---|---| separator row
            continue
        anchor = cells[0]
        if not INDEX_ANCHOR.match(anchor):
            continue
        rows.append((anchor, cells))
    return header, rows


def main():
    armed, note = _armed()
    if not armed:
        print("check-description-field: OK (dormant) — the gate arms in the back-describe migration "
              "landing (INV-217, folded finding N5); it stands down until then. %s" % note)
        return 0

    if not os.path.isfile(SPEC_PATH):
        print("check-description-field: cannot read %s — the gate stands on the spec file." % SPEC_PATH)
        return 1
    with open(SPEC_PATH, encoding="utf-8") as f:
        spec = f.read()

    header, rows = _index_rows(spec)
    if header is None:
        print("check-description-field: %s carries no `## Formal index` section — the gate cannot read "
              "the description fields (SPEC INV-239)." % SPEC_PATH)
        return 1

    # The expected-non-empty input set: the registered codes. A zero-anchor index reds by name rather
    # than passing over nothing (the vacuous-pass guard, INV-218).
    try:
        require_nonempty(CHECK, "the Formal-index registered codes", [a for a, _ in rows])
    except VacuousInputError as e:
        print("check-description-field: %s" % e)
        return 1

    if "description" not in header:
        print("check-description-field: the Formal index carries no `Description` field, so every "
              "registered code stands with no description (the field the back-describe migration adds, "
              "SPEC INV-239/E-35). Add the description field, or keep the gate dormant until the "
              "migration lands (guardrails/description-field.json).")
        return 1

    # The description field is located by its HEADER column index. A row with fewer cells than the
    # header OMITS a cell — and an omitted description cell is a missing description, red exactly like
    # an empty one. This short-row guard is what stops the misalignment a header→cell zip would hide,
    # where a short row slides the Section text into the description slot and false-passes.
    desc_idx = header.index("description")
    empty = []
    for anchor, cells in rows:
        if len(cells) < len(header):
            empty.append(anchor)          # short row: a cell is omitted, the description among them
            continue
        if not _is_present(cells[desc_idx]):
            empty.append(anchor)

    if empty:
        print("check-description-field: %d registered code(s) carry an empty or missing description "
              "field — the field is the description's one home and a bare code never stands alone "
              "before a reader (SPEC INV-239/E-35): %s" % (len(empty), ", ".join(empty)))
        print("  Fix: give each named code its plain one-sentence description in the Formal index's "
              "Description field (to the quality bar, read by the human sampling net INV-41).")
        return 1

    print("check-description-field: OK (armed; %d registered codes, each carrying a non-empty "
          "description field)." % len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
