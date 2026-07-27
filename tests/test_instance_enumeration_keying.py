# -*- coding: utf-8 -*-
"""The general-law-plus-instances family declares enumerate-versus-ride (ROADMAP row 370, SPEC INV-226).

The pack carries several laws shaped as one general duty over concrete instances — the range law
(INV-138), the budget law (INV-41), the facet law (INV-18) — and each decided differently whether its
instances are named in the clause or ride the general duty silently, with the keying declared nowhere
(the 2.5.0 design review, finding 2, 2026-07-17). This row states one class sentence keying the choice on
whether the member set is open-ended or closed and enumerable, and has the three named laws cite it.

This module is the traceability proof: the class sentence stands in its one home, and the three laws each
reference it.

Red-first: against HEAD 573d8ea the spec carries no INV-226 and the three laws carry no citation to it, so
every assertion below fails — the red recorded in docs/prover/2026-07-18-rows-370-394.md.
"""
import os
import re
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from conftest import criterion_with_bullets

sys.path.insert(0, os.path.join(REPO, "guardrails"))
import archformat  # the one node reader every consumer reads through (SPEC INV-280)


def read(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as f:
        return f.read()


def line_with(text, phrase):
    """The single criterion carrying a distinctive phrase, read with the bullets under it.

    A law's citation bracket rides its criterion line while the member set it enumerates sits in
    the bullets beneath, so a check that reads one physical line sees half the law. The shared
    reader in conftest joins the two, and a table row (the matrix's own lines) still comes back
    as itself, since a row heads its own unit.
    """
    return criterion_with_bullets(text, phrase)


def requirement_block(spec, heading_phrase):
    """The text from a requirement's heading line to the next '---' divider — the class sentence
    used to sit in one paragraph, but the new requirement-format spec spreads the same class
    sentence across a Context line and its numbered criteria within one requirement block."""
    lines = spec.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("## Requirement") and heading_phrase in line:
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    return "\n".join(lines[start:end])


class TestClassSentenceStands(unittest.TestCase):
    def test_class_sentence_stands(self):
        spec = read("PRODUCT_SPEC.md")
        block = requirement_block(
            spec,
            "A general law over concrete instances declares whether it enumerates them or lets them ride",
        )
        self.assertIsNotNone(block, "the INV-226 class-sentence requirement is absent from the spec")
        self.assertIn("[INV-226]", block, "the requirement carries no [INV-226] tag")
        low = block.lower()
        # the keying: open-ended member set rides, closed enumerable set enumerates
        self.assertIn("closed", low)
        self.assertIn("enumerable", low)
        self.assertIn("open-ended", low)
        self.assertIn("member set", low)

    def test_formal_index_row(self):
        spec = read("PRODUCT_SPEC.md")
        # the index row is location-only (SPEC INV-271); the class sentence lives on the heading
        self.assertIn("| INV-226 |", spec, "no index row for INV-226")
        self.assertIn(
            "A general law over concrete instances declares whether it enumerates them or lets them ride",
            spec, "no class-sentence heading for INV-226")

    def test_architecture_owns_the_invariant(self):
        nodes = archformat.parse_nodes(read("ARCHITECTURE.md"))
        spec_author = next((n for n in nodes if n.name == "spec-author"), None)
        self.assertIsNotNone(spec_author, "ARCHITECTURE.md carries no spec-author node")
        self.assertIn("INV-226", spec_author.anchors_expanded,
                      "spec-author does not own INV-226 in the architecture owns-list")

    def test_matrix_row_covers_the_law(self):
        mat = read("TEST_MATRIX.md")
        self.assertIn("| M-407 |", mat)
        row = line_with(mat, "| M-407 |")
        self.assertIn("INV-226", row, "M-407 does not cite INV-226")


class TestThreeLawsCiteTheClass(unittest.TestCase):
    """The three named laws each reference the class sentence (SPEC INV-226)."""

    # each law's citation sentence, plus the SIDE it must state (a miskeyed law is a finding, so the
    # side is asserted textually, not only the citation's presence)
    LAWS = [
        ("range law INV-138", "range-and-lifecycle member of the composition-lens family", "open-ended"),
        ("budget law INV-41", "these kinds form a closed set, and each is named in this criterion",
         "closed"),
        ("facet law INV-18",
         "one closed enumerable set that grows a member only with a named real incident", "closed"),
    ]

    def test_three_laws_cite_the_class(self):
        spec = read("PRODUCT_SPEC.md")
        for name, phrase, side in self.LAWS:
            line = line_with(spec, phrase)
            self.assertIsNotNone(line, "%s: citation sentence absent (%r)" % (name, phrase))
            # the tag now rides grouped with siblings rather than solo — cite is by substring
            self.assertIn("INV-226", line, "%s: clause does not cite INV-226" % name)
            self.assertIn(side, line,
                          "%s: citation does not state its member-set side (%r)" % (name, side))

    def test_the_three_canonical_anchors_are_present(self):
        spec = read("PRODUCT_SPEC.md")
        for anchor in ("[INV-138]", "[INV-41]", "[INV-18]"):
            self.assertIn(anchor, spec)


if __name__ == "__main__":
    unittest.main(verbosity=2)
