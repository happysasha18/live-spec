"""The full pass proves the architecture beside the spec (SPEC INV-116, row 271).

Every milestone gate [M-1] and every push gate [M-6] runs the product-prover over
ARCHITECTURE.md as well as PRODUCT_SPEC.md, so the design-level seams meet the same
structured review the spec gets. The taste call: commit-time freshness only, no content-grep
— the guardrail side of this (tests/test_guardrails.py) proves the freshness mechanics; this
file proves the spec says so.
"""

import os
import unittest

import re

from conftest import ROOT, read, read_flat


class TestArchitectureProvedAtFullPass(unittest.TestCase):
    def test_full_architecture_reprove_phrase(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("full spec and architecture re-prove", spec)

    def test_both_documents_named_phrase(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "a fresh prover pass over the spec and the architecture", spec
        )

    def test_spec_anchor(self):
        spec = read("PRODUCT_SPEC.md")
        self.assertRegex(spec, r"\[[^\]\n]*\bINV-116\b[^\]\n]*\]")

    def test_spec_anchor_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("| INV-116 |", spec, "INV-116 has no Reference index row")
        self.assertIn(
            "re-prove the architecture beside it",
            spec,
            "INV-116's body criterion doesn't carry the architecture phrase",
        )


if __name__ == "__main__":
    unittest.main()
