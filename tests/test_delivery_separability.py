"""Delivery separability along a declared composition axis — M-433 (SPEC INV-248, ROADMAP 438).

The dual of the composition-axes law (INV-244). Composition reads whether a surface's BEHAVIOUR
splits along a cross-cutting axis its kind owes; its dual reads whether the delivered ARTIFACT splits
along that same axis or ships as one monolith. When a spec declares such an axis and covering it adds
runtime code, the design carries one of two decided sentences — the axis ships whole for a named
architectural reason (one bundle, one page never torn down, a no-server delivery, a payload too small
to split), or it owes a delivery road a later row lands (a platform split, a lazy load). The finding
is the unexamined third case: an axis adding runtime code that ships as one artifact and names neither.
The lens stays a senior read the prover carries rather than a gate, since a named-reason monolith is
lawful. product-prover carries the lens body and a standing discovery habit — for a lens it applies it
may ask whether that lens's dual bites — held as a habit, never a law that every lens ship paired.

This file proves the law's homes: the SPEC clause and Formal-index row, the product-prover lens body
and its dual-discovery habit, spec-author's duty to state the delivery answer, and the owning
spec-author node in ARCHITECTURE (the lens carried by product-prover). Against HEAD 4dd3857 (pre-delta)
none of these exist — recorded in the station's red run.
"""

import os
import sys
import unittest

from conftest import ROOT, external_clone_or_skip, read, read_all_flat, read_flat

sys.path.insert(0, os.path.join(ROOT, "guardrails"))
import archformat  # the one node reader every consumer reads through (SPEC INV-280)


class TestDeliverySeparabilityLaw(unittest.TestCase):
    def test_inv248_spec_clause_stands(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "Requirement 266: A declared axis that adds runtime code names whether its "
            "artifact divides or ships whole",
            spec,
        )
        self.assertIn("[INV-248]", spec)

    def test_inv248_formal_index_row(self):
        # the new-format index carries locations only (SPEC INV-271); the prose checks move
        # to the body criteria that carry the code.
        spec = read("PRODUCT_SPEC.md")
        row = next((l for l in spec.splitlines() if l.startswith("| INV-248 |")), "")
        self.assertTrue(row, "INV-248 Formal-index row missing")
        flat = read_flat("PRODUCT_SPEC.md")
        self.assertIn("delivered artifact", flat)
        self.assertIn("axis", flat)
        self.assertIn("read the finding as the third case", flat)

    def test_inv248_prover_carries_the_lens(self):
        external_clone_or_skip()
        pp = read_all_flat("skills/product-prover/SKILL.md")
        self.assertIn("Delivery separability along a declared axis", pp,
                      "product-prover does not carry the delivery-separability lens")
        # the INV-248 anchor is a pack fact: the pack adapter's pin map carries it (unbracketed,
        # the pin-map row form) against the lens's name.
        pack = read_flat("skills/product-prover-pack/SKILL.md")
        self.assertIn("INV-248", pack)
        self.assertIn("unexamined monolith", pp,
                      "the lens does not name the unexamined-monolith finding")

    def test_inv248_prover_carries_the_dual_habit(self):
        """The lens carries the dual-discovery habit — ask whether an applied lens's dual bites — as a
        habit, never a law that every lens ship a partner."""
        external_clone_or_skip()
        pp = read_all_flat("skills/product-prover/SKILL.md")
        self.assertIn("whether that lens's dual bites", pp,
                      "product-prover does not carry the dual-discovery habit")
        self.assertIn("never demands every lens ship a partner", pp,
                      "the dual habit is not held as a habit rather than a law")

    def test_inv248_spec_author_states_delivery(self):
        """When an owed axis adds runtime code, spec-author states how the axis is delivered
        (SPEC INV-248) — a monolith with a named reason, or a delivery road a later row lands."""
        sa = read_flat("skills/spec-author/SKILL.md")
        self.assertIn("INV-248", sa, "spec-author does not carry the delivery-separability duty")
        self.assertIn("how that axis is delivered", sa,
                      "spec-author does not state the delivery answer for a runtime-code axis")

    def test_inv248_architecture_owns_the_lens(self):
        """The delivery-separability invariant is owned by the spec-author node (INV-244's owner), the
        lens body carried by product-prover — mirroring INV-49 (owned by parallel-lanes, carried)."""
        nodes = archformat.parse_nodes(read("ARCHITECTURE.md"))
        spec_author = next((n for n in nodes if n.name == "spec-author"), None)
        self.assertIsNotNone(spec_author, "ARCHITECTURE.md carries no spec-author node")
        self.assertIn("INV-248", spec_author.anchors_expanded,
                      "spec-author does not own INV-248")
        product_prover = next((n for n in nodes if n.name == "product-prover"), None)
        self.assertIsNotNone(product_prover, "ARCHITECTURE.md carries no product-prover node")
        self.assertTrue(
            "delivery-separability lens" in product_prover.owns
            or "delivery-separability lens" in product_prover.notes,
            "product-prover does not carry the delivery-separability lens")

    def test_inv248_distinct_from_composition_axes_law(self):
        """The delivery-separability law is the DUAL of the composition-axes law, never folded into it:
        composition reads whether behaviour splits, this reads whether the delivered artifact splits."""
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("Its dual reads whether the artifact the visitor receives divides", spec,
                      "the clause does not state itself as the dual of the composition law")
        self.assertIn("[INV-244]", spec)


if __name__ == "__main__":
    unittest.main()
