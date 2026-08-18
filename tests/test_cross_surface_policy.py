"""A cross-surface policy is stated at the surface-class level and held uniform — INV-125.

When a decision governs an interaction KIND that lives on several sibling surfaces (a gesture policy, an
affordance, an input-to-action mapping), the spec states it once at the surface-class level and enumerates
the surfaces it governs; a policy written for one surface while siblings exist is a spec defect. The prover
writes itself the check (enumerate the surfaces of that kind from the surface registry, flag any the clause
does not cover); a product with a DOM instantiates the completeness guardrail to assert the policy across
every registered sibling root. The preventive twin of the class hunt (INV-124). Homes: the composition
clause, product-prover's cross-surface-policy lens, build-pipeline's completeness guardrail. (Born of
tlvphotos's pinch-zoom policy shipped for the walk alone, 2026-07-12.)
"""

import os
import unittest

from conftest import ROOT, external_clone_or_skip, open_spec, read_all, read_all_flat, read_flat


class TestCrossSurfacePolicy(unittest.TestCase):
    def test_spec_clause_stands(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "the spec states it once at the surface-class level, naming the class and "
            "enumerating the surfaces it governs",
            spec,
        )
        self.assertIn("[INV-125]", spec)

    def test_spec_names_the_class_rule_and_the_two_holds(self):
        spec = read_flat("PRODUCT_SPEC.md")
        for needle in (
            "naming the class and enumerating the surfaces it governs",
            "is a spec defect",
            "enumerate the surfaces of that kind from the surface registry",
            "the preventive twin of the class hunt",
        ):
            self.assertIn(needle, spec, needle)

    def test_formal_index_row(self):
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-125 |"):
                    self.assertIn("surface-class", read_flat("PRODUCT_SPEC.md").lower())
                    return
        self.fail("INV-125 Formal-index row missing")

    def test_prover_carries_the_cross_surface_lens(self):
        external_clone_or_skip()
        pv = read_all_flat("skills/product-prover/SKILL.md")
        self.assertIn("Cross-surface policy uniformity", pv)
        # the canon states the twin relation mid-sentence ("This sweep is the preventive twin
        # of the class lens below"), so the needle is pinned lowercase.
        self.assertIn("the preventive twin of the class lens", pv)

    def test_build_pipeline_completeness_holds_uniformity(self):
        bp = read_all_flat("skills/build-pipeline/SKILL.md")
        self.assertIn("cross-surface policy uniformity (SPEC INV-125)", bp)
        self.assertIn("EVERY registered sibling root", bp)

    def test_sentence_form_trigger(self):
        """The sharpened trigger fires on a kind-general rule worded inside one member's own
        section while siblings exist — the prose-law form the declared-class enumeration misses.
        (Born of the tlvphotos openable-face miss: one member stated 'the way out mirrors the way
        in' and a pinch-to-zoom sibling closed only by a control, 2026-07-14.)"""
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("a sentence states a principle for a whole kind", spec)
        self.assertIn("lift", spec)
        external_clone_or_skip()
        pv = read_all_flat("skills/product-prover/SKILL.md")
        self.assertIn("kind-general rule", pv)
        self.assertIn("scope it to the one member", pv)

    def test_matrix_row_covers_the_uniformity_law(self):
        with open(os.path.join(ROOT, "TEST_MATRIX.md"), encoding="utf-8") as f:
            for line in f:
                if line.startswith("| M-266 |"):
                    self.assertIn("INV-125", line)
                    return
        self.fail("M-266 matrix row missing")


if __name__ == "__main__":
    unittest.main()
