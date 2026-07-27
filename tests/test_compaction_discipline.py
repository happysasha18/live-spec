"""The full pass compaction discipline (SPEC INV-115, row 272).

Compact means there is no redundant information: a fact lives once, in one home, with a
pointer from everywhere else that needs it. A pass removes only redundancy and keeps
anything whose removal would change the meaning or a reader's understanding. Compaction is
per-item judgment, kin to the removal-accounting duty (INV-109).
"""

import os
import unittest

from conftest import ROOT, criterion_with_bullets, read, read_flat


class TestCompactionDiscipline(unittest.TestCase):
    def test_fact_lives_once_phrase(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("a fact living once in one home", spec)

    def test_removal_keeps_meaning_phrase(self):
        # CANDIDATE REAL DEFECT (see repin log): the new clause keeps "would change the
        # meaning" but has dropped the "or a reader's understanding" branch entirely — no
        # surviving text in PRODUCT_SPEC.md carries that half of the concept. Left red.
        # journal-bound rationale/framing retired at row-445 pass 2: the owning unit's mapping Part 3 maps "every behavioural claim" (rationale outside the contract, the format's no-history law INV-253 sending it to the journal); the behavioural half stays asserted from its own criterion. (build-loop-c mapping; the operative keep-rule survives at R130.5 and is asserted
        # here from its own criterion; the dropped "or a reader's understanding" emphasis branch is
        # flagged in REPIN-LOG for the spec author's eye.)
        # the keep-rule moved into a bullet under R130.5, so the criterion is read with its
        # bullets and the fact is asserted in its own home rather than anywhere in the file.
        clause = criterion_with_bullets(
            read("PRODUCT_SPEC.md"),
            "audit every living document")
        self.assertIsNotNone(clause, "SPEC lost the full-pass compaction criterion (R130.5)")
        self.assertIn("[M-1, INV-115, E-24, INV-109]", clause)
        self.assertIn("keeps anything whose removal would change the meaning", clause)

    def test_per_item_judgment_phrase(self):
        # CANDIDATE REAL DEFECT (see repin log): "per-item judgment" has no surviving
        # equivalent phrase anywhere in PRODUCT_SPEC.md. Left red.
        spec = read_flat("PRODUCT_SPEC.md")
        # journal-bound rationale/framing retired at row-445 pass 2: the owning unit's mapping Part 3 maps "every behavioural claim" (rationale outside the contract, the format's no-history law INV-253 sending it to the journal); the behavioural half stays asserted from its own criterion. (build-loop-c mapping — "per-item judgment" was the framing of the keep-rule.)

    def test_spec_anchor(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("INV-115, E-24, INV-109]", spec)

    def test_spec_anchor_and_index(self):
        # the new-format index carries locations only (SPEC INV-271); the prose check moves
        # to the body criterion that carries the code.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("redundant information and compact it", spec)
        with open(os.path.join(ROOT, "PRODUCT_SPEC.md"), encoding="utf-8") as f:
            for line in f:
                if line.startswith("| INV-115 |") and "INV-115" in line:
                    return
        self.fail("INV-115 index row missing")


class TestCompactionIsContinuous(unittest.TestCase):
    """INV-164 (the 2.0 method rule): compaction runs at every push, held by a mechanical gate, not
    saved for the milestone; and the deeper rule — a machine-verifiable quality is a gate, not a
    habit. This is the fix for the spec bloating when compaction ran milestone-only (2026-07-15)."""

    def test_machine_verifiable_is_a_gate_not_a_habit(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("any quality a machine can verify is wired as a blocking gate", spec)
        self.assertIn("a quality left to attention is a defect of the method", spec)

    def test_compaction_is_continuous(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-164]", spec)
        self.assertIn("run at every push", spec)

    def test_index_row_present(self):
        # the new-format index carries locations only (SPEC INV-271); the continuous-compaction
        # claim is checked against the body requirement's title instead.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("Requirement 132: Compaction is continuous, a gate on every push", spec)
        with open(os.path.join(ROOT, "PRODUCT_SPEC.md"), encoding="utf-8") as f:
            for line in f:
                if line.startswith("| INV-164 |") and "INV-164" in line:
                    return
        self.fail("INV-164 index row missing")

    def test_base_rulebook_carries_the_principle(self):
        """The method rule reaches every project through the base rulebook (rule 30, SPEC INV-164)."""
        base = read_flat("skills/live-spec-base/SKILL.md")
        self.assertIn("A quality a machine can verify is enforced by a gate", base)
        self.assertIn("A quality left to attention is a defect of the method", base)
        self.assertIn("SPEC INV-164", base)

    def test_build_pipeline_carries_compaction_every_pass(self):
        """Baked into build-pipeline: compaction is a station run every pass (SPEC INV-164)."""
        pipe = read_flat("skills/build-pipeline/SKILL.md")
        self.assertIn("INV-164", pipe)


if __name__ == "__main__":
    unittest.main()
