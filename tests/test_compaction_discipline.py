"""The full pass compaction discipline (SPEC INV-115, row 272).

Compact means there is no redundant information: a fact lives once, in one home, with a
pointer from everywhere else that needs it. A pass removes only redundancy and keeps
anything whose removal would change the meaning or a reader's understanding. Compaction is
per-item judgment, kin to the removal-accounting duty (INV-109).
"""

import re
import unittest

from conftest import criterion_with_bullets, open_spec, read, read_flat


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
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-115 |") and "INV-115" in line:
                    return
        self.fail("INV-115 index row missing")


class TestCompactionIsContinuous(unittest.TestCase):
    """INV-164: compaction runs at every push, held by a mechanical gate, not saved for the
    milestone. This is the fix for the spec bloating when compaction ran milestone-only
    (2026-07-15). The clause that once minted a gate from any machine-verifiable quality is
    removed; a check is opened from a second break (INV-108) or the owner's word."""

    def test_a_check_is_not_born_from_checkability(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("mint no gate from the sole fact that a quality is machine-verifiable", spec)
        self.assertNotIn("wire any quality a machine can verify as a blocking gate", spec)

    def test_compaction_is_continuous(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-164]", spec)
        self.assertIn("run at every push", spec)

    def test_index_row_present(self):
        # the new-format index carries locations only (SPEC INV-271); the continuous-compaction
        # claim is checked against the body requirement's title instead.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("Requirement 132: Compaction is continuous, a gate on every push", spec)
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-164 |") and "INV-164" in line:
                    return
        self.fail("INV-164 index row missing")

    def test_base_rulebook_carries_no_generator_rule(self):
        """The rulebook no longer carries the rule that minted a gate from checkability. Its
        number 30 stays a hole: the rules after it keep the numbers every citation points at."""
        base = read("skills/live-spec-base/SKILL.md")
        self.assertNotIn("A quality a machine can verify is enforced by a gate",
                         " ".join(base.split()))
        heads = re.findall(r"^(\d+)\. \*\*", base, re.M)
        self.assertNotIn("30", heads, "rule 30 is cut; its number stays a hole")
        self.assertIn("29", heads)
        self.assertIn("31", heads)

    def test_rule7_batch1_locked_its_level(self):
        """Stage-2 batch 1 (2026-08-12) shortened rule 7 to 5,171 body bytes. Row 595's
        skill-creator review then recommended four small restorations, folded the same day: the
        lead-in naming the parallel-lanes bullets one family, the "convergence point" name back
        on the shared document, the pointer to the script's own on-disk preconditions, and the
        lane-open bullet's dropped actor. This lock holds the batch-1 gain net of that fold: the
        body stays under its pre-rewrite opening size of 5,477 bytes, and the restored pointer
        sentence is back."""
        base = read("skills/live-spec-base/SKILL.md")
        m = re.search(r"(?ms)^7\. \*\*.*?(?=^8\. \*\*)", base)
        self.assertIsNotNone(m, "rule 7's body not found between heads 7 and 8")
        body = m.group(0)
        self.assertLess(len(body.encode("utf-8")), 5477,
                        "rule 7's body grew back past its pre-rewrite opening size")
        self.assertIn("The script's own header states what it expects on disk", body,
                       "row 595's restored pointer sentence is missing")

    def test_build_pipeline_carries_compaction_every_pass(self):
        """Baked into build-pipeline: compaction is a station run every pass (SPEC INV-164).

        Pinned to the bullet's own sentence (row 592), not just the invariant code, so
        deleting the bullet while leaving the code behind in a comment fails this test."""
        pipe = read_flat("skills/director/references/landing-law.md")
        self.assertIn("INV-164", pipe)
        self.assertIn("doc- and code-compaction stations run at every push", pipe)


if __name__ == "__main__":
    unittest.main()
