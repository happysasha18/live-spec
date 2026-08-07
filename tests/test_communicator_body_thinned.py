"""Row 280: communicator's body thinned under the ~500-line ideal without cutting a rule.

Row 266 extracted the writing register to references/ but the body still sat at 565 lines; row 280 is
the follow-on that brings it under ~500 by grouping tighter and spilling the unpinned worked EXAMPLES to
a second references/ file — every one of the 22 rules kept (folded, grouped, or pointered, never cut).

This test is the conservation floor under that refactor. It guards the exact failure the row hit once (an
auto-tighten pass that silently dropped four normative sub-rules) from the other side: the body stays
under the ideal AND every rule tag stays present AND the relocated examples remain reachable in the new
references file. The per-rule NORMATIVE phrases stay pinned by their own feature tests across the suite;
here we hold the structural conservation.
"""

import os
import re
import unittest

from conftest import ROOT, read, read_flat

SKILL_REL = os.path.join("skills", "communicator", "SKILL.md")
EXAMPLES_REL = os.path.join("skills", "communicator", "references", "field-examples.md")
# Derivation: the published skill-authoring guidance (~/.claude/skills/skill-creator/SKILL.md,
# "Keep SKILL.md under 500 lines") — not a project-invented number.
IDEAL_MAX_LINES = 500  # the Done-when's "under ~500"


class TestCommunicatorBodyThinned(unittest.TestCase):
    def test_body_is_under_the_size_ideal(self):
        body = read(SKILL_REL)
        n = body.count("\n")
        self.assertLess(
            n, IDEAL_MAX_LINES,
            "communicator body regrew past the ~500-line ideal (row 280): %d lines" % n,
        )

    def test_all_twenty_two_rule_tags_present(self):
        flat = read_flat(SKILL_REL)
        for n in range(1, 23):
            self.assertIn(
                "(rule %d)" % n, flat,
                "communicator lost rule %d's tag — a rule may fold or pointer, never vanish" % n,
            )

    def test_examples_reference_exists_and_body_points_at_it(self):
        self.assertTrue(
            os.path.exists(os.path.join(ROOT, EXAMPLES_REL)),
            "the field-examples reference file is missing",
        )
        self.assertIn(
            "references/field-examples.md", read_flat(SKILL_REL),
            "the body dropped its pointer to the worked-examples reference",
        )

    def test_relocated_examples_live_in_the_reference(self):
        ex = read_flat(EXAMPLES_REL)
        for needle in (
            "suite running in the background",          # rule 13 detached cadence
            "you're needed again",                       # rule 13 offline return-beat
            "довожу до безопасной точки",                # rule 13 leave-word
            "the stem-name resolver",                    # rule 6 one-name case
            "Option A (recommended",                     # the fork template
            "Typography decision",                       # a live field case
            "verified: suite green",                     # rule 11 worked answer
        ):
            self.assertIn(needle, ex, "field-examples.md missing a relocated example: %s" % needle)

    def test_prereport_walk_still_points_at_the_register_home(self):
        self.assertIn(
            "open [`references/writing-register.md`](references/writing-register.md)",
            read_flat(SKILL_REL),
            "the pre-report walk's step-1 pointer to the register no longer resolves",
        )


if __name__ == "__main__":
    unittest.main()
