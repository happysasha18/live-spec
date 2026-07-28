"""The M-1 milestone gate enumerates the design-review pass — SPEC INV-141 (audit D1, 2026-07-14).

INV-141 says the design review "runs in full at every full prover pass", and a milestone runs a full
spec re-prove — so the design review is owed at the milestone. But the enumerated M-1 milestone-gate
step list (the checklist a session actually walks) never named it, so a pure-milestone movement ran the
prover, stood the design review down at the push gate, and skipped it silently with every gate green.
This is the red-first fence: the M-1 list must name the design-review pass, and the architecture's
"Decisions — where they live" append duty must land its dated record beside the prover record.
String level against the shipped docs.
"""

import os
import unittest

from conftest import ROOT, read


def _milestone_list(spec):
    """The enumerated M-1 milestone-gate step list. The requirements-format rewrite moved this
    from a "**Milestone (minor gate):**" bullet block to Requirement 130's Acceptance Criteria
    (nine numbered steps across four Cases), so this now extracts that requirement's whole body.

    The heading boundaries are found on the raw text (each heading is its own physical line),
    then the extracted body is whitespace-flattened so a wrapped line inside it still matches a
    prose needle byte-for-byte.
    """
    head = "## Requirement 130: The milestone gate re-proves and audits the whole"
    start = spec.index(head)
    tail = spec.index("\n## Requirement 131", start)
    return " ".join(spec[start:tail].split())


class TestMilestoneEnumeratesDesignReview(unittest.TestCase):
    def test_m1_list_names_the_design_review(self):
        block = _milestone_list(read("PRODUCT_SPEC.md"))
        self.assertIn("design review", block.lower(),
                      "the M-1 milestone-gate list never enumerates the design-review pass (D1)")
        # R130.2's tag is now a shared bracket [M-1, INV-141, INV-154] rather than a standalone
        # [INV-141] — check the bare code instead.
        self.assertIn("INV-141", block,
                      "the M-1 design-review step carries no INV-141 anchor")

    def test_m1_step_lands_the_dated_record(self):
        block = _milestone_list(read("PRODUCT_SPEC.md")).lower()
        # the design-review step names its outcome AND its dated record, not just "runs" — the
        # Context paragraph's own first "design review" mention is a bare summary with no record
        # detail, so this checks R130.2's own criterion sentence directly.
        self.assertIn("design-review record", block,
                      "the M-1 design-review step never lands its dated record")

    def test_architecture_append_duty_names_the_design_review_record(self):
        arch = read("ARCHITECTURE.md")
        section = arch.split("## Decisions — where they live", 1)[1].split("## Prover record", 1)[0]
        section = " ".join(section.split())
        self.assertIn("design-review record", section.lower(),
                      "ARCHITECTURE's append duty never names the design-review record beside the prover's")


if __name__ == "__main__":
    unittest.main()
