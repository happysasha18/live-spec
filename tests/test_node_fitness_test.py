"""A new or carved architecture node proves itself by three questions — row 260a (SPEC INV-122).

Every extraction or new/carved node is gated by a three-question fitness test at its birth: can it be
tested alone, does a real second place need it, can it and its neighbour be worked in parallel without
queuing on shared files — three yes make it right, two no make it premature. First home: build-pipeline's
architecture step (the gate a new node passes). Second home: product-prover, extending the
speculative-node flag — a node with one caller and no promised second is flagged.
"""

import unittest

from conftest import external_clone_or_skip, open_spec, read_all_flat, read_flat


class TestNodeFitnessTest(unittest.TestCase):
    def test_build_pipeline_carries_the_three_questions(self):
        # build-pipeline's former architecture-step gate moved to architect's own step
        # (SKILL.md plus its architecture-step-detail.md reference, read together as the
        # skill's whole surface). "Can it be tested alone?" carries a capital there, so the
        # comparison lower-cases both sides, the same pattern
        # test_architecture_lens_is_six_items in test_traceability.py uses for this exact
        # kind of register mismatch.
        bp = read_all_flat("skills/architect/SKILL.md").lower()
        self.assertIn("three-question fitness test", bp)
        self.assertIn("can it be tested alone", bp)
        self.assertIn("worked in parallel without queuing on shared files", bp)

    def test_prover_flags_the_speculative_node(self):
        external_clone_or_skip()
        # Release 1.6.0 moved the architecture lens out of the canon's SKILL.md body and into
        # its reference/architecture-lens.md, so the flag is read across the skill's whole
        # surface — the same whole-surface read the architect assertion above already uses.
        pp = read_all_flat("skills/product-prover/SKILL.md")
        self.assertIn("one caller and no promised second is flagged", pp)

    def test_spec_clause_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("three-question fitness test", spec)
        self.assertIn("[INV-122]", spec)

    def test_formal_index_row(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "fitness", spec.lower(),
            "INV-122's body criterion doesn't carry the fitness phrase",
        )
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-122 |"):
                    return
        self.fail("INV-122 Formal-index row missing")


if __name__ == "__main__":
    unittest.main()
