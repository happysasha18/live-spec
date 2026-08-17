"""Both directions of a paired state change get the same craft, or a stated reason they do not — INV-126.

When a surface has a pair of opposite state changes (open/close, enter/exit, expand/collapse, show/hide), a
transition crafted for one direction is a decision about the pair, so the other direction is stated too. The
default is symmetry (the exit mirrors the enter's feel unless a reason is written); a shorter or
deliberately-instant exit is a valid STATED answer. It rides the standard-facet sweep as its own facet, and
because motion feel is the human's own gate an undecidable pair is surfaced to him. The prover flags a pair
with one direction described and the opposite unstated. The temporal twin of INV-125. Homes: the composition
clause, the facet list in spec-author, product-prover's paired-transition check. (Born of tlvphotos's
polaroid room revealed under a soft veil and closed on a hard cut, felt on a real phone, 2026-07-12.)
"""

import os
import unittest

from conftest import ROOT, external_clone_or_skip, read_all_flat, read_flat


class TestPairedTransition(unittest.TestCase):
    def test_spec_clause_stands(self):
        spec = read_flat("PRODUCT_SPEC.md")
        # R261 heading: the requirements-format rewrite drops the trailing ", or a stated reason
        # they do not" clause from the heading itself, folding it into the criterion instead.
        self.assertIn(
            "Both directions of a paired state change get the same craft",
            spec,
        )
        self.assertIn("unless a written reason parts them", spec)
        self.assertIn("[INV-126]", spec)

    def test_spec_names_default_and_the_human_gate(self):
        spec = read_flat("PRODUCT_SPEC.md")
        for needle in (
            "The default is symmetry",
            "Motion feel is the human's own gate",
        ):
            self.assertIn(needle, spec, needle)
        # the "temporal twin of cross-surface uniformity" framing itself is gone from the spec
        # body (still stands in skills/product-prover/SKILL.md, checked by
        # test_prover_carries_the_paired_transition_check below); the structural equivalence it
        # named survives in the spec as both R260 (cross-surface, INV-125) and R261 (paired,
        # INV-126) routing their findings through the same blank-answer/unwritten-situation class.
        self.assertIn("finding of the same blank-answer class as an unwritten situation", spec)

    def test_formal_index_row(self):
        with open(os.path.join(ROOT, "PRODUCT_SPEC.md"), encoding="utf-8") as f:
            for line in f:
                if line.startswith("| INV-126 |"):
                    row = line
                    break
            else:
                self.fail("INV-126 Formal-index row missing")
        # index now carries locations only (SPEC INV-271) — move the "paired state change"
        # prose check onto the body requirement heading that carries INV-126.
        self.assertTrue(row)
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("Both directions of a paired state change get the same craft", spec)

    def test_spec_author_carries_the_facet(self):
        sa = read_all_flat("skills/spec-author/SKILL.md")
        self.assertIn("paired-transition symmetry", sa)
        self.assertIn("the exit's motion mirrors the enter's", sa)

    def test_prover_carries_the_paired_transition_check(self):
        external_clone_or_skip()
        pv = read_all_flat("skills/product-prover/SKILL.md")
        self.assertIn("Paired-transition symmetry", pv)
        self.assertIn("the temporal twin of the cross-surface uniformity sweep above", pv)

    def test_reversibility_of_means_half(self):
        """INV-126's second half: a continuous, reversible opening gesture carries its inverse
        among the ways to close, or a decided sentence states why not; silence blocks, the
        sentence's rightness stays the human's gate. (Born of the tlvphotos openable-face miss:
        a pinch opened a layer with no reverse pinch to close it, 2026-07-14.)"""
        spec = read_flat("PRODUCT_SPEC.md")
        # the old "two halves" sentence is gone; the requirements-format rewrite states the same
        # split structurally as two named Cases under R261 instead of naming them in prose.
        for needle in ("Case: the continuity of the transition", "Case: the reversibility of the means"):
            self.assertIn(needle, spec, needle)
        for needle in ("reversibility of the means", "reversible gesture"):
            self.assertIn(needle, spec, needle)
        external_clone_or_skip()
        pv = read_all_flat("skills/product-prover/SKILL.md")
        # the canon names the same sub-question "The inverse of the means"
        self.assertIn("The inverse of the means", pv)
        sa = read_all_flat("skills/spec-author/SKILL.md")
        self.assertIn("reversibility of the means", sa)

    def test_magnitude_sub_question(self):
        """INV-126's magnitude sub-question, matrix row M-341: where the paired open and close ride
        a continuous, reversible quantity, the spec states whether the inverse demands the same
        magnitude as the forward move — symmetric, or a named deliberate asymmetry."""
        spec = read_flat("PRODUCT_SPEC.md")
        for needle in ("same magnitude as the forward move", "a named deliberate asymmetry"):
            self.assertIn(needle, spec, needle)
        with open(os.path.join(ROOT, "PRODUCT_SPEC.md"), encoding="utf-8") as f:
            for line in f:
                if line.startswith("| INV-126 |"):
                    row = line
                    break
            else:
                self.fail("INV-126 Formal-index row missing")
        # index now carries locations only (SPEC INV-271) — the "same magnitude" prose check
        # already stands against the body above; here just confirm the row exists.
        self.assertTrue(row)
        external_clone_or_skip()
        pv = read_all_flat("skills/product-prover/SKILL.md")
        self.assertIn("The inverse's magnitude", pv)
        self.assertIn("same magnitude as the forward move", pv)
        sa = read_all_flat("skills/spec-author/SKILL.md")
        self.assertIn("asks magnitude beside existence", sa)
        self.assertIn("0.82×", sa)

    def test_matrix_row_covers_the_paired_transition_law(self):
        with open(os.path.join(ROOT, "TEST_MATRIX.md"), encoding="utf-8") as f:
            for line in f:
                if line.startswith("| M-267 |"):
                    self.assertIn("INV-126", line)
                    return
        self.fail("M-267 matrix row missing")


class TestOrientationFacet(unittest.TestCase):
    """Row 367 (M-349, grows INV-18's curated facet list): the standard-facet sweep gains the
    orientation / short-viewport facet. A landscape phone is wide and short, a distinct band
    width-thinking misses, so every layout-bearing feature ends the sweep with a decided or
    [default] sentence for the short-viewport band. Incident key: the tlvphotos caption-over-picture
    landscape overlap, the layout law said "on a phone", the styles mapped phone to width ≤ 640px,
    and a rotated phone fell out of both sentences, 2026-07-16."""

    def test_orientation_short_viewport_facet(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("the short-viewport band", spec)
        # the "a landscape phone is wide and short" illustration is thinned out of the compact
        # spec body but survives verbatim in spec-author's elaboration of the same facet.
        sa = read_all_flat("skills/spec-author/SKILL.md")
        for needle in ("orientation / short viewport", "a rotated phone", "width ≤ 640px",
                       "phone is wide and short"):
            self.assertIn(needle, sa, needle)
        with open(os.path.join(ROOT, "TEST_MATRIX.md"), encoding="utf-8") as f:
            for line in f:
                if line.startswith("| M-349 |"):
                    self.assertIn("INV-18", line)
                    break
            else:
                self.fail("M-349 matrix row missing")


class TestViewportQuantifierLens(unittest.TestCase):
    """Row 368 (M-350, grows INV-138): every layout guarantee states its viewport quantifier. A
    layout guarantee names "on every viewport" or the band it is scoped to, and a guarantee scoped
    to one band draws the standing question about the other bands. INV-138 already owns the
    range-and-lifecycle completeness class (both ends of a ranged quantity), and the viewport is
    such a quantity, so the quantifier lens grows INV-138's clause rather than a new law. Same
    incident key as row 367."""

    def test_viewport_quantifier_lens(self):
        spec = read_flat("PRODUCT_SPEC.md")
        # R263.7: requirements-format shifts "names" (descriptive) to "name" (subjunctive shall).
        for needle in ("every layout guarantee name its viewport quantifier",
                       "on every viewport", "the other bands"):
            self.assertIn(needle, spec, needle)
        with open(os.path.join(ROOT, "PRODUCT_SPEC.md"), encoding="utf-8") as f:
            for line in f:
                if line.startswith("| INV-138 |"):
                    row = line
                    break
            else:
                self.fail("INV-138 Formal-index row missing")
        # index now carries locations only (SPEC INV-271) — the row's presence is the anchor
        # proof; the "viewport quantifier" prose check already stands against the body above.
        self.assertTrue(row)
        external_clone_or_skip()
        pv = read_all_flat("skills/product-prover/SKILL.md")
        # the canon generalized the lens to "The condition quantifier", keeping the viewport
        # bands as its worked instance — the band-scoped standing question holds.
        for needle in ("The condition quantifier", "viewport sizes", "the other bands"):
            self.assertIn(needle, pv, needle)
        dr = read_flat("skills/design-reviewer/SKILL.md")
        self.assertIn("viewport band", dr)
        with open(os.path.join(ROOT, "TEST_MATRIX.md"), encoding="utf-8") as f:
            for line in f:
                if line.startswith("| M-350 |"):
                    self.assertIn("INV-138", line)
                    break
            else:
                self.fail("M-350 matrix row missing")


class TestGeneralSubDomainDuty(unittest.TestCase):
    """Row 369 (M-351, grows INV-138): the standing sub-domain question lifts to the general
    range law. The "answers for the rest" duty shipped worded for layout guarantees over viewport
    bands; a guarantee scoped to any other named sub-domain — a user state, a network condition, a
    locale — is the same hole class. The law states the general duty (a guarantee scoped to a named
    part of its domain draws the standing question about the remainder, each remaining part decided
    or [default]-tagged), with the viewport bands kept as the worked instance, and the prover lens
    and author facet cite it as instances. The general-duty needles lead in the spec clause, the
    Formal-index row, and the prover lens; the viewport needles from row 368 stay intact."""

    def test_general_sub_domain_duty(self):
        spec = read_flat("PRODUCT_SPEC.md")
        # R263 context / R263.5: "one named part" replaces the old "a named part" phrasing.
        for needle in ("one named part of its domain", "the remainder"):
            self.assertIn(needle, spec, needle)
        with open(os.path.join(ROOT, "PRODUCT_SPEC.md"), encoding="utf-8") as f:
            for line in f:
                if line.startswith("| INV-138 |"):
                    row = line
                    break
            else:
                self.fail("INV-138 Formal-index row missing")
        # index now carries locations only (SPEC INV-271) — the row's presence is the anchor
        # proof; the phrase checks above and below already stand against the body and the skill.
        self.assertTrue(row)
        external_clone_or_skip()
        pv = read_all_flat("skills/product-prover/SKILL.md")
        for needle in ("a named part of its domain", "the remainder"):
            self.assertIn(needle, pv, needle)
        with open(os.path.join(ROOT, "TEST_MATRIX.md"), encoding="utf-8") as f:
            for line in f:
                if line.startswith("| M-351 |"):
                    self.assertIn("INV-138", line)
                    break
            else:
                self.fail("M-351 matrix row missing")


if __name__ == "__main__":
    unittest.main()
