"""Every row identifier in TEST_MATRIX.md and every row number in the ROADMAP system is unique
across the whole tree, archive included (found 2026-08-19, a same-day merge collision).

Two independent packages each picked their own "next free" TEST_MATRIX id and ROADMAP row number
off the same shared ancestor, and the merge landed both: `M-547` and `M-548` each named two
unrelated rows in TEST_MATRIX.md, and ROADMAP row `625` named one live row and one already-rotated
archive row. Nothing textual conflicted — every line differs, so git merged clean — and
`guardrails/check-matrix-reference.py` (gate d) passed at "540 of 540 rows scanned", because it
checks the body against the generated Reference table, never that a row's own id is claimed once.
No script anywhere held this law; it is stated here for the first time.

This is a TEST under `tests/`, not a new push gate: the coordinator's word (2026-08-19) is that a
duplicate id is real but rare enough, and cheap enough to repair by hand once caught, that the
"one generated device home" gate af now demands (SPEC INV-210/INV-212: a manifest entry, a red
proof, a CI-mirror step) is not owed for it. This test rides the ordinary suite instead.

Red proven 2026-08-19: planting a second `| M-1 |` row in TEST_MATRIX.md made
`test_every_matrix_id_is_unique` fail, naming `M-1` and both its line numbers; removing the plant
passed it again. The same proof ran for a planted second `| 1 |` ROADMAP row.
"""
import glob
import os
import re
import sys
import unittest

from conftest import ROOT

sys.path.insert(0, os.path.join(ROOT, "guardrails"))
import specformat as sf  # noqa: E402

MATRIX = os.path.join(ROOT, "TEST_MATRIX.md")
PLAN = os.path.join(ROOT, "PLAN.md")
# The queue was a table of its own until 2026-08-27; the retired file rests in the attic and its
# rows are read from there, so the archives keep being checked against the body they left.
ROADMAP = os.path.join(ROOT, "attic", "ROADMAP.md")
ARCHIVE_GLOB = os.path.join(ROOT, "docs", "queue-archive", "rotated-ROADMAP-*.md")

MATRIX_ROW_RE = re.compile(r"(?m)^\|\s*(M-\d+)\s*\|")
PLAN_ID_RE = re.compile(r"(?m)^###\s+.*\u2014\s*id:\s*([A-Za-z][A-Za-z0-9-]*)\s*$")
ROADMAP_ROW_RE = re.compile(r"(?m)^\|\s*(\d+)\s*\|")


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _matrix_ids(text):
    """(id, 1-based line number) for every body row TEST_MATRIX.md carries. The generated
    `## Reference` table's own rows (`| Anchor | Rows |`) never match this pattern — an anchor
    reads `INV-###`/`T-#`/etc, never `M-###` — so splitting the file at the heading is not needed."""
    out = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        m = MATRIX_ROW_RE.match(line)
        if m:
            out.append((m.group(1), lineno))
    return out


def _roadmap_ids(text, label):
    """(id, "label:line") for every row line one ROADMAP-shaped document carries."""
    out = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        m = ROADMAP_ROW_RE.match(line)
        if m:
            out.append((m.group(1), "%s:%d" % (label, lineno)))
    return out


def _duplicates(pairs):
    """{id: [locations]} for every id `pairs` names more than once."""
    seen = {}
    for ident, where in pairs:
        seen.setdefault(ident, []).append(where)
    return {k: v for k, v in seen.items() if len(v) > 1}


class TestEveryMatrixRowIdIsUnique(unittest.TestCase):
    def test_every_matrix_id_is_unique(self):
        # Corrected 2026-09-02 (hostile review, docs/prover/2026-09-02-overnight-run-hostile-review.md,
        # finding 4): every M-### row moved from TEST_MATRIX.md's own body into matrix/*.md parts at
        # 35bc12e8, and this test still read only the bare core file — zero rows scanned, silently
        # passing, ever since. That is exactly how the M-621 collision between q-48 and q-804 reached
        # a merge tonight uncaught. Read the assembled document (core + every part) the way the real
        # gates do, through the shared parser, and refuse to pass on an empty scan.
        _, joined = sf.read_document(sf.spec_paths([MATRIX]))
        pairs = [("%s:%d" % (os.path.basename(MATRIX), lineno), ident)
                 for ident, lineno in _matrix_ids(joined)]
        self.assertGreater(
            len(pairs), 50,
            "the matrix id scan found %d rows — TEST_MATRIX.md's parts map is empty, unreadable, or "
            "this test regressed to reading the bare core file again; either way the scan looked at "
            "nothing and would pass on an empty set" % len(pairs))
        # swap to (id, where) for _duplicates
        pairs = [(ident, where) for where, ident in pairs]
        dupes = _duplicates(pairs)
        self.assertEqual(
            dupes, {},
            "TEST_MATRIX.md (core + parts) carries the same row id more than once — two rows claim "
            "one identifier and a reader following either citation lands on whichever row sorts "
            "first: %s" % dupes)


def _plan_ids(text, label):
    """(id, "label:line") for every task the one list carries. A task heading reads
    `### <mark> <title> \u2014 id: <id>`, and the id is what every citation of that row follows."""
    out = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        m = PLAN_ID_RE.match(line)
        if m:
            out.append((m.group(1), "%s:%d" % (label, lineno)))
    return out


class TestEveryPlanRowIdIsUnique(unittest.TestCase):
    def test_every_plan_id_is_unique(self):
        pairs = _plan_ids(_read(PLAN), "PLAN.md")
        self.assertGreater(len(pairs), 20, "the one list parsed no tasks — the id scan looked at "
                                           "nothing and would pass on an empty set")
        dupes = _duplicates(pairs)
        self.assertEqual(
            dupes, {},
            "the one list claims the same row id more than once \u2014 two tasks answer one "
            "citation and a reader following it lands on whichever sorts first: %s" % dupes)


class TestEveryRoadmapRowNumberIsUnique(unittest.TestCase):
    def test_every_roadmap_row_number_is_unique(self):
        pairs = _roadmap_ids(_read(ROADMAP), "attic/ROADMAP.md")
        for path in sorted(glob.glob(ARCHIVE_GLOB)):
            pairs += _roadmap_ids(_read(path), os.path.basename(path))
        dupes = _duplicates(pairs)
        self.assertEqual(
            dupes, {},
            "a ROADMAP row number is claimed more than once across the live queue and its archives "
            "— the nothing-lost, grepable-by-number law (base rule 10) breaks the moment two rows "
            "answer one grep: %s" % dupes)


if __name__ == "__main__":
    unittest.main()
