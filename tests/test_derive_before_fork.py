"""Derive from a proven artifact before offering a fork — row 270 (SPEC INV-121).

The read-the-doc twin of ask-never-guess: before surfacing a design choice, a session checks whether an
existing proven artifact (the architecture, the spec, the invariants) already determines the answer;
when it does, it derives the requirement and cites the section, offering no fork. A fork reaches the
human only for what the artifacts leave genuinely open. The law lives in the base rulebook beside
ask-never-guess and in the spec. (Born of a track-coach session that offered the owner two options while
its ARCHITECTURE.md layer split already determined the answer, 2026-07-12.)
"""

import unittest

from conftest import open_spec, read_flat


class TestDeriveBeforeFork(unittest.TestCase):
    def test_base_rule_carries_the_twin(self):
        base = read_flat("skills/live-spec-base/SKILL.md")
        self.assertIn("the read-the-doc twin of ask-never-guess", base)
        self.assertIn("a proven artifact already settles", base)

    def test_spec_clause_stands(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("A proven artifact settles a fork before the person hears it", spec)
        self.assertIn("[INV-121]", spec)

    def test_formal_index_row(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "fork", spec.lower(),
            "INV-121's body criterion doesn't carry the fork phrase",
        )
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-121 |"):
                    return
        self.fail("INV-121 Formal-index row missing")


if __name__ == "__main__":
    unittest.main()
