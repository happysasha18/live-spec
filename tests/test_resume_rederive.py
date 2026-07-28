"""INV-247 — a deferred item's own state is re-derived from the code before its work resumes (ROADMAP 430).

A method discipline with no mechanical gate: these checks assert the SHIPPED law stands in the spec,
the formal index, and the base rulebook, and that it stays distinct from the queue-take trigger re-scan
(INV-129) rather than folding into it. Zero dependencies; run from the repo root:
    python3 -m pytest -q tests/test_resume_rederive.py
Red proven against HEAD 31a2bb3, where none of these strings exist yet.
"""

import re
import unittest

from conftest import read_flat


class ResumeRederive(unittest.TestCase):
    def test_inv247_spec_clause_stands(self):
        # the requirements-format heading carries no trailing period
        spec = read_flat("PRODUCT_SPEC.md")
        title = "A deferred item's own state is re-derived from the code before its work resumes"
        self.assertIn(
            title,
            spec,
            "the INV-247 clause title is missing from the product spec",
        )
        # the clause carries its trailing anchor (now bundled with a sibling code) and names the
        # act it owes
        clause = spec.split(title, 1)[1][:2600]
        self.assertRegex(
            clause, r"\[[^\]\n]*\bINV-247\b[^\]\n]*\]",
            "the INV-247 clause carries no trailing anchor",
        )
        self.assertIn("reads the code the item touches", clause)
        self.assertIn("re-derives the item's real current state", clause)

    def test_inv247_formal_index_row(self):
        # the old Formal index (with its scenario-name "owner" column, e.g. "Throwing a wish") is
        # gone; the Reference table now carries locations only (SPEC INV-271). Check the index row
        # exists, and that INV-247's own defining requirement is on record as its home.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("| INV-247 |", spec, "no INV-247 row in the Reference table")
        self.assertIn(
            "## Requirement 93: A deferred item's own state is re-derived from the code "
            "before its work resumes",
            spec,
        )

    def test_inv247_base_rule_states_the_reread(self):
        skill = read_flat("skills/live-spec-base/SKILL.md")
        self.assertRegex(
            skill,
            r"34\. \*\*A deferred item's own state is re-derived from the code before its work resumes \(SPEC INV-247\)\.\*\*",
            "base rule 34 does not state the resume re-derivation law",
        )
        # the description's rule count moved with the added rule
        self.assertIn("thirty-five rules in the body", skill)
        self.assertNotIn("thirty-three rules in the body", skill)

    def test_inv247_distinct_from_queue_take_rescan(self):
        """The law must stand beside INV-129, not collapse into it: one reads the returning
        trigger, the other the item's own internals. The register rewrite's contrast-frame ban
        (INV-166 — never name a thing by denying its neighbour) retired the old prose contrast
        sentence; distinctness is now structural — two separate, adjacently-numbered requirements
        (92 for the trigger re-scan, 93 for the item's own re-derivation) that cite each other
        where they compose, rather than collapsing into one."""
        spec = read_flat("PRODUCT_SPEC.md")
        title = "A deferred item's own state is re-derived from the code before its work resumes"
        self.assertIn(
            "## Requirement 92: Deferred rows are revisited at every queue-take", spec,
            "INV-129's own defining requirement is missing, so the sibling law has no distinct home",
        )
        clause = spec.split(title, 1)[1][:2600]
        # it cites INV-129 as the sibling on the very criterion that composes the two reads
        self.assertRegex(
            clause, r"\[[^\]\n]*\bINV-129\b[^\]\n]*\]",
            "the clause does not situate itself beside the trigger re-scan",
        )
        # and it answers the mechanical-net question rather than leaving it silent
        self.assertIn("no committed artifact for a gate to scan", clause)


if __name__ == "__main__":
    unittest.main()
