"""Enumerable facts earn bullet structure — a prose paragraph packing an enumeration reads as a list.

SPEC INV-215 (ROADMAP row 379). The owner, 2026-07-17, reading the promoter's inter-agent design doc:
a single paragraph packed a filename rule, a collision law, three header fields, and four body parts;
that is a list the reader should meet as a list, the human language already right and the fine-tuning
reading efficiency. The verdict is honest: this stays a STATED writing rule in spec-author's structure
guidance, read by eye and by the prover's cognitive-load lens — it earns NO mechanical lint of its own,
because a regex flagging every three-comma sentence would trip on ordinary rhetorical triads, and telling
a genuine list-owed enumeration from a rhetorical triad is a meaning call no regex makes.

These are string-level checks against the shipped docs: the rule stands in its two homes (spec-author,
the prover's cognitive-load lens), the spec states the law with its Formal-index row, the architecture
assigns it to the spec-author node, the matrix covers it, and the verdict (a stated rule, not a new
pre-push gate) is written where a reader meets it.
"""

import os
import re
import sys
import unittest

from conftest import ROOT, read, read_flat

sys.path.insert(0, os.path.join(ROOT, "guardrails"))
import archformat  # the one node reader every consumer reads through (SPEC INV-280)


class TestEnumerationReadsAsList(unittest.TestCase):

    def test_spec_author_states_the_enumeration_threshold(self):
        body = read_flat("skills/spec-author/SKILL.md")
        self.assertIn("INV-215", body,
                      "spec-author's structure guidance carries no INV-215 rule")
        self.assertIn("three or more", body,
                      "spec-author names no enumeration threshold (three or more parallel facts)")
        # the rule is a structure rule about lists, not something incidental
        self.assertIn("enumeration", body,
                      "spec-author's INV-215 rule never speaks of an enumeration")

    def test_prover_cognitive_load_lens_reads_the_packed_enumeration(self):
        body = read_flat("skills/product-prover/SKILL.md")
        self.assertIn("cognitive-load", body,
                      "the prover has no cognitive-load lens to carry the reading-load reading")
        # the INV-215 anchor is a pack fact: the externalized canon carries no project codes,
        # so the pack adapter's pin map binds the code to the cognitive-load lens — on one
        # line, so the reading is anchored on the lens rather than stranded elsewhere.
        pack = read_flat("skills/product-prover-pack/SKILL.md")
        self.assertIn("INV-215", pack,
                      "the pack adapter names no INV-215 binding for the packed-enumeration reading")
        cog_line = next((ln for ln in read("skills/product-prover-pack/SKILL.md").splitlines()
                         if "cognitive-load" in ln and "INV-215" in ln), None)
        self.assertIsNotNone(cog_line,
                             "the adapter's INV-215 line never names the cognitive-load lens")

    def test_spec_states_the_law(self):
        body = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-215]", body, "PRODUCT_SPEC.md carries no INV-215 clause")
        self.assertIn("Enumerable facts earn bullet structure", body,
                      "the INV-215 clause never states the enumerable-facts-earn-bullets rule")

    def test_verdict_is_a_stated_rule_not_a_new_gate(self):
        # The honest footprint verdict is written where a reader meets it: this earns no mechanical lint.
        spec = read_flat("PRODUCT_SPEC.md")
        i = spec.find("[INV-215]")
        # read the clause's own neighbourhood (it precedes its trailing anchor)
        clause = spec[max(0, i - 1600):i]
        self.assertIn("no mechanical lint", clause,
                      "the INV-215 clause never states its verdict (no mechanical lint of its own)")
        # and no new pre-push gate letter was wired for an enumeration check
        pre_push = read("guardrails/pre-push")
        self.assertNotIn("enumeration", pre_push.lower(),
                         "an enumeration gate was wired into pre-push — INV-215 is a stated rule, not a gate")

    def test_formal_index_row(self):
        body = read_flat("PRODUCT_SPEC.md")
        self.assertRegex(body, r"\|\s*INV-215\s*\|",
                         "PRODUCT_SPEC.md's Formal index carries no INV-215 row")

    def test_architecture_owns_the_invariant(self):
        nodes = archformat.parse_nodes(read("ARCHITECTURE.md"))
        spec_author = next((n for n in nodes if n.name == "spec-author"), None)
        self.assertIsNotNone(spec_author, "ARCHITECTURE.md carries no spec-author node")
        self.assertIn("INV-215", spec_author.anchors_expanded,
                      "the spec-author node's owns-list never claims INV-215")

    def test_matrix_row_covers_the_law(self):
        body = read_flat("TEST_MATRIX.md")
        self.assertIn("M-396", body, "TEST_MATRIX.md carries no M-396 row")
        m396 = next((ln for ln in read("TEST_MATRIX.md").splitlines()
                     if ln.startswith("| M-396 ")), "")
        self.assertIn("INV-215", m396, "the M-396 row does not cite INV-215")


if __name__ == "__main__":
    unittest.main()
