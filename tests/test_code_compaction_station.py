"""Compaction is a scheduled station for code as well as docs, with its second trigger — row 260b (SPEC INV-123).

Milestone DOC compaction already stands (INV-115). This widens the station to CODE — duplicate logic
merges, dead weight leaves with its listing (INV-109), a ripened abstraction is extracted only through
the three-question fitness gate (INV-122) — and gives it a SECOND trigger: apart from the milestone, the
second occurrence of the same problem (base rule 19) fires it. Each pass locks the reached level with a
test or a lint (the convergence law, rows 216-218 / INV-98). Homes: the milestone-rhythm compaction
section + build-pipeline's before-a-MINOR gate.
"""

import unittest

from conftest import open_spec, read_flat


class TestCodeCompactionStation(unittest.TestCase):
    def test_spec_clause_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("widen the compaction station to code", spec)
        self.assertIn("INV-123", spec)

    def test_spec_names_second_trigger_and_gate(self):
        spec = read_flat("PRODUCT_SPEC.md")
        # the second trigger (base rule 19's second occurrence) and the extraction gate (INV-122)
        self.assertIn("the second occurrence of one problem", spec)
        self.assertIn("[INV-122]", read_flat("PRODUCT_SPEC.md"))

    def test_build_pipeline_minor_gate_carries_code_compaction(self):
        bp = read_flat("skills/build-pipeline/SKILL.md")
        self.assertIn("code compaction", bp)

    def test_build_pipeline_minor_gate_carries_skill_creator_review(self):
        # Requirement 130 (SPEC M-1): the milestone/MINOR gate re-runs the skill evals and
        # walks every skill through skill-creator's craft review — a real gap the eval/iterate
        # run (Полоса B п.10) found missing from both build-pipeline's own summary bullet and
        # its reference file; this guards the two staying in sync.
        bp = read_flat("skills/build-pipeline/SKILL.md")
        self.assertIn("the skill-creator craft review", bp)
        detail = read_flat("skills/build-pipeline/references/minor-bump-gate.md")
        self.assertIn(
            "re-runs the skill evals and sends every skill in the pack through skill-creator's "
            "craft review",
            detail,
        )
        self.assertIn("SPEC M-1", detail)

    def test_formal_index_row(self):
        # INDEX-ROW pattern (RECIPE): the Reference table now carries locations only,
        # no prose. Assert the row's presence here; the "code" prose is asserted
        # against the flattened spec body in test_spec_clause_and_index above.
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-123 |"):
                    self.assertIn("R130.6", line)
                    return
        self.fail("INV-123 Formal-index row missing")


if __name__ == "__main__":
    unittest.main()
