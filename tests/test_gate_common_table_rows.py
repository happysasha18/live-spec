"""Tests for gate_common.segment_units()'s table-row handling.

Locks the fix that stopped scripts/gate_common.py skipping every markdown table row outright:
a delimiter row (`|---|---|`) is still dropped, but a data row's cells are scanned like prose,
so a duplicated fact sentence living inside a table cell (TEST_MATRIX.md's own rows, a spec's
own tables) is no longer invisible to spec-redundancy-precheck.py.
"""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
sys.path.insert(0, SCRIPTS)
import gate_common  # noqa: E402


class TestTableDelimiterRows(unittest.TestCase):
    def test_delimiter_row_produces_no_units(self):
        for delim in ("|---|---|", "| --- | --- |", "|:--|--:|"):
            units = gate_common.segment_units(delim)
            self.assertEqual(units, [], "delimiter row %r should yield no units" % delim)


class TestTableDataRows(unittest.TestCase):
    def test_data_row_cells_are_scanned(self):
        row = "| M-999 | The system shall build the widget from its parts at freeze. | string | built |"
        units = gate_common.segment_units(row)
        raws = [u["raw"] for u in units]
        self.assertTrue(
            any("shall build the widget from its parts at freeze" in r for r in raws),
            "a data cell's sentence should surface as its own unit: %r" % raws,
        )

    def test_short_structural_cells_still_produce_units_but_stay_below_min_tokens(self):
        # The caller (spec-redundancy-precheck.py) filters units shorter than MIN_TOKENS before
        # pairing candidates; this test only locks that segment_units() itself does not special-case
        # short cells away — id/status cells are real units, just short ones.
        row = "| M-999 | string | *built* |"
        units = gate_common.segment_units(row)
        self.assertTrue(len(units) >= 1)

    def test_duplicated_cell_sentence_across_two_rows_is_detected(self):
        text = (
            "| M-100 | Retired: gate ad retired. Never re-armed without a fresh decision. | string | *retired* |\n"
            "| M-101 | Retired: gate ad retired. Never re-armed without a fresh decision. | string | *retired* |\n"
        )
        units = gate_common.segment_units(text)
        raws = [u["raw"] for u in units if "never re-armed without a fresh decision" in u["raw"].lower()]
        self.assertEqual(len(raws), 2, "the same cell sentence on two rows should surface as two units: %r" % raws)


if __name__ == "__main__":
    unittest.main()
