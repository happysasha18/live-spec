# -*- coding: utf-8 -*-
"""The authoring seat does not adversarially certify its own work (ROADMAP row 422, SPEC INV-237).

The 2.7.0 release ran its adversarial prover pass in the same context that authored the release's new
lenses, so it never turned a brand-new lens onto the skill body that introduced it; a fresh web review
then caught a Phase-5 count naming four blocks over five and two bullets packing three rules each. The
rule this module proves: a release's adversarial pass is authored by a fresh seat, and a newly added
lens or rule is self-applied to its own introducing document before release. It generalizes the
fresh-eyes freshness the verify audit already demands (INV-46) and the periodic audit's adversarial
stance (INV-145) to the release pass itself.

Whether a review was truly clean-context is a process fact no gate fully sees, so this is a traceability
proof that the pack's own text STATES the duty across its homes; the optional record gate checks only
that a dated record exists and names a different seat.

Red-first: against origin/main 03a4d26 the spec, Formal index, architecture, matrix, base rulebook, and
the two wiring skills carry no INV-237, so every assertion below fails.
"""
import os
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as f:
        return f.read()


def flat(rel):
    return " ".join(read(rel).split())


CLAUSE_OPENER = "The authoring seat does not certify its own work"


class TestCleanContextReview(unittest.TestCase):
    def test_spec_states_the_law(self):
        spec = flat("PRODUCT_SPEC.md")
        self.assertIn(CLAUSE_OPENER, spec)
        self.assertIn("INV-237", spec)
        # the authoring seat drafts and accepts but never self-certifies adversarially
        self.assertIn("drafts and accepts it but never provides its own adversarial certification",
                      spec)

    def test_names_both_carriers(self):
        spec = flat("PRODUCT_SPEC.md")
        # carrier one: the release adversarial pass authored by a fresh seat
        self.assertIn("release's adversarial pass", spec)
        self.assertIn("authored by a fresh, differently-contexted seat", spec)
        # carrier two: a new lens/rule self-applied to its own introducing document
        self.assertIn("applied to the very document that introduces it before release", spec)
        self.assertIn("self-applied", spec)

    def test_formal_index_row(self):
        # the index row is location-only (SPEC INV-271); the prose lives on the body criterion
        for line in read("PRODUCT_SPEC.md").splitlines():
            if line.startswith("| INV-237 |"):
                break
        else:
            self.fail("INV-237 index row missing")
        spec = flat("PRODUCT_SPEC.md")
        self.assertIn("The authoring seat does not certify its own work", spec)

    def test_base_rule_33_states_it(self):
        base = read("skills/live-spec-base/SKILL.md")
        self.assertIn("33. **The authoring seat does not adversarially certify its own work", base)
        self.assertIn("SPEC INV-237", base)
        # the rule-count claim in the description stays in sync
        self.assertIn("thirty-four rules in the body", base)

    def test_build_pipeline_wires_verify_station(self):
        bp = flat("skills/build-pipeline/SKILL.md")
        self.assertIn("The authoring seat never certifies its own work adversarially (SPEC INV-237)", bp)
        self.assertIn("authored by a fresh seat, never the seat that authored the change", bp)

    def test_product_prover_wires_self_application(self):
        pv = flat("skills/product-prover/SKILL.md")
        self.assertIn("A release's adversarial pass runs from a clean context", pv)
        self.assertIn("SPEC INV-237", pv)

    def test_architecture_owns_the_invariant(self):
        # Exactly one architecture node owns INV-237 (traceability owns every anchor once). Since the
        # row-456 format conversion the ownership is read through the node reader; the release-audit law
        # itself lives at the spec, cited by the anchor rather than restated in the architecture.
        import sys
        sys.path.insert(0, os.path.join(REPO, "tests"))
        from test_traceability import architecture_nodes
        owners = [node for node, owned in architecture_nodes().items() if "INV-237" in owned]
        self.assertEqual(owners, ["build-pipeline"],
                         "INV-237 must be owned by exactly the build-pipeline node, got %r" % owners)

    def test_matrix_row_covers_the_law(self):
        for line in read("TEST_MATRIX.md").splitlines():
            if line.startswith("| M-419 |"):
                self.assertIn("INV-237", line)
                self.assertIn("The authoring seat does not adversarially certify its own work", line)
                return
        self.fail("M-419 matrix row missing")


if __name__ == "__main__":
    unittest.main()
