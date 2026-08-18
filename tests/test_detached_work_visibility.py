"""Detached work stays visible — matrix row M-232 (SPEC INV-35 tightened, row 248).

His 2026-07-10 ~17:10 word from the track-coach window: twice a multi-minute background run
went silent and read as lost. A detached operation (a background command or a delegated worker
the chat does not stream) expected past ~2 minutes opens with a start line, keeps a beat every
~2 minutes or per stage, and closes with a done digest. String rows on the two homes: the spec
clause and the communicator skill.
"""

import unittest

from conftest import open_spec, read_flat


class TestDetachedWorkVisibility(unittest.TestCase):
    HOMES = ("PRODUCT_SPEC.md", "skills/communicator/SKILL.md")

    # PRODUCT_SPEC.md's rewritten Requirement 22 states the cadence in its own word order
    # (the skill keeps the older, more colloquial phrasing) — same meaning, different string.
    CADENCE_NEEDLES = {
        "PRODUCT_SPEC.md": (
            "an operation runs detached past about 2 minutes",
            "start line",
            "every 2 minutes or at each stage",
            "done digest",
        ),
        "skills/communicator/SKILL.md": (
            "expected to run past ~2 minutes detached",
            "start line",
            "every ~2 minutes or at each stage",
            "done digest",
        ),
    }

    def test_cadence_in_both_homes(self):
        for home in self.HOMES:
            body = read_flat(home)
            for needle in self.CADENCE_NEEDLES[home]:
                self.assertIn(needle, body, home)

    def test_the_trap_is_named(self):
        # CANDIDATE REAL DEFECT (see repin log): "shows in no agent panel" has no surviving
        # text in PRODUCT_SPEC.md's rewritten Requirement 22 — only the communicator skill
        # still carries it. Left red for the spec home.
        spec = read_flat("PRODUCT_SPEC.md")
        # journal-bound rationale/framing retired at row-445 pass 2: the owning unit's mapping Part 3 maps "every behavioural claim" (rationale outside the contract, the format's no-history law INV-253 sending it to the journal); the behavioural half stays asserted from its own criterion. (build-loop-a mapping — the trap framing; the law survives as the User Story "a silent
        # stretch never reads to me as lost work" + the detached-run cadence criterion.)
        self.assertIn("reads to me as lost work", spec, "PRODUCT_SPEC.md")
        skill = read_flat("skills/communicator/SKILL.md")
        self.assertIn("shows in no agent panel", skill, "skills/communicator/SKILL.md")
        self.assertIn("reads as lost", skill, "skills/communicator/SKILL.md")

    def test_mechanism_free_visibility_required(self):
        # CANDIDATE REAL DEFECT (see repin log): "visibility is the requirement" has no
        # surviving text in PRODUCT_SPEC.md's rewritten Requirement 22 — only the
        # communicator skill still carries it. Left red for the spec home.
        for home in self.HOMES:
            body = read_flat(home)
            if home == "PRODUCT_SPEC.md":
                # journal-bound rationale/framing retired at row-445 pass 2: the owning unit's mapping Part 3 maps "every behavioural claim" (rationale outside the contract, the format's no-history law INV-253 sending it to the journal); the behavioural half stays asserted from its own criterion. (build-loop-a mapping — the requirement/mechanism framing; the cadence criterion
                # carries the behaviour; the skill home below still states the sentence.)
                self.assertIn("keep a beat landing about every 2 minutes", body, home)
            else:
                self.assertIn("visibility is the requirement", body, home)

    def test_spec_index_row_carries_the_cadence(self):
        # the new-format index carries locations only (SPEC INV-271); the prose check moves
        # to the body criterion that carries the code.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn(
            "open with a start line naming what runs, where its log lives, and an honest "
            "range, keep a beat landing about every 2 minutes or at each stage, and close "
            "with a done digest",
            spec,
        )
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-35 |"):
                    return
        self.fail("INV-35 index row missing")


if __name__ == "__main__":
    unittest.main()
