"""live-spec-base's body keeps thinning toward references/, without cutting a rule.

2026-08-17 moved the glossary and the worked examples out to references/glossary.md and
references/worked-examples.md, word for word (commit 5295b06, plus the reading-key follow-up
94ae4c3). This session moved a further four illustrative chunks — the paths-and-codes section, rule
23's worked proof, rule 33's 2.7.0 history, and rule 35's worked failure plus its withdrawn-script
note — into those same two reference files, again word for word, leaving every rule's operative
sentence in the body.

Two of the four 08-17 reviews' open findings were about exactly this gap: no conservation test existed
for live-spec-base's body-thinning, unlike communicator's `tests/test_communicator_body_thinned.py`
(the model this test follows). This is that test, extended to the reference files this skill now
carries.

This test does NOT re-derive whether a moved chunk reads correctly in its new home, or whether a
body pointer names the right section — that is a one-time human/reviewer judgment already made when
the text moved. It holds the structural floor after the fact: the reference files exist, the body
still points at each of them, the moved text's characteristic substrings are actually present in the
reference files (so a later edit cannot silently empty one), and every one of the 34 numbered rules
still has its heading in the body (a rule may fold, shrink, or pointer out its illustration, but it
may never vanish).
"""

import os
import re
import unittest

from conftest import ROOT, read, read_flat

SKILL_REL = os.path.join("skills", "live-spec-base", "SKILL.md")
GLOSSARY_REL = os.path.join("skills", "live-spec-base", "references", "glossary.md")
EXAMPLES_REL = os.path.join("skills", "live-spec-base", "references", "worked-examples.md")
SETTINGS_LADDER_REL = os.path.join("skills", "live-spec-base", "references", "settings-ladder.md")

# The 34 rule numbers this rulebook carries today: 1-29 and 31-35: rule 30 was cut whole and its
# number stays retired (the body's own "## The shared rules" preamble states this). Not derived from
# the file here on purpose — this is the independent census the description's own rule-count claim
# is checked against elsewhere (tests/test_minor_gate_reconciliations.py); this test instead asserts
# each number's heading survives by name, so a silent drop reds even if the total count coincidentally
# still matches (e.g. two rules merging while a third is cut).
RULE_NUMBERS = tuple(n for n in range(1, 36) if n != 30)

# Ratchet, not a target: this session's move brought the body from 620 to 606 lines, still well past
# skill-creator's <500-line ideal (the number test_communicator_body_thinned.py's IDEAL_MAX_LINES
# derives from, ~/.claude/skills/skill-creator/SKILL.md). Getting live-spec-base under 500 is a
# further structural move — grouping or folding rules, the way communicator needed a second pass
# (row 280) after its first reference-extraction (row 266) still left it at 565 lines. Until that
# second pass happens here, this threshold holds the line at "no regrowth past where this session left
# it", with headroom for small, legitimate edits — not "under the ideal".
CURRENT_MAX_LINES = 615


class TestLiveSpecBaseBodyThinned(unittest.TestCase):
    def test_body_has_not_regrown_past_the_current_ratchet(self):
        body = read(SKILL_REL)
        n = body.count("\n")
        self.assertLess(
            n, CURRENT_MAX_LINES,
            "live-spec-base body regrew past the current ratchet: %d lines "
            "(still short of skill-creator's <500 ideal; see the module docstring)" % n,
        )

    def test_all_thirty_four_rule_numbers_present(self):
        flat = read(SKILL_REL)
        found = set(int(m) for m in re.findall(r"(?m)^(\d+)\. \*\*", flat))
        missing = [n for n in RULE_NUMBERS if n not in found]
        self.assertFalse(
            missing,
            "live-spec-base lost the heading for rule(s) %r — a rule may fold or pointer its "
            "illustration out, never vanish" % missing,
        )
        # Rule 30 stays retired; a heading reappearing for it is its own kind of drift, out of this
        # test's scope, but worth not silently accepting here either.
        self.assertNotIn(30, found, "rule 30 is retired and should carry no heading of its own")

    def test_three_reference_modules_exist_and_body_points_at_each(self):
        flat = read_flat(SKILL_REL)
        for rel, name in (
            (GLOSSARY_REL, "glossary"),
            (EXAMPLES_REL, "worked-examples"),
            (SETTINGS_LADDER_REL, "settings-ladder"),
        ):
            self.assertTrue(
                os.path.exists(os.path.join(ROOT, rel)),
                "the %s reference file is missing" % name,
            )
            self.assertIn(
                "references/%s.md" % name, flat,
                "the body dropped its pointer to references/%s.md" % name,
            )

    def test_relocated_paths_and_codes_text_lives_in_the_glossary(self):
        gl = read_flat(GLOSSARY_REL)
        for needle in (
            "SKILL.md names paths of two kinds",
            "github.com/happysasha18/live-spec",
            "A bracket code such as",
            "So a row SKILL.md cites may sit there instead",
        ):
            self.assertIn(needle, gl, "glossary.md missing relocated paths-and-codes text: %s" % needle)

    def test_relocated_worked_examples_live_in_the_reference(self):
        ex = read_flat(EXAMPLES_REL)
        for needle in (
            "the guard holding this pack's register laws was built as a list of literal",  # rule of thinking
            "Here is the worked proof",                                                     # rule 23
            "The 2.7.0 release ran its adversarial pass",                                    # rule 33
            "Worked failure: on 2026-07-28 a session wrote its",                             # rule 35
            "the live-spec pack withdrew that script after finding no error",                # rule 35
            "The 2.0.0 release is the boundary case",                                        # rule 32
        ):
            self.assertIn(needle, ex, "worked-examples.md missing a relocated example: %s" % needle)

    def test_body_keeps_the_test_checked_sentence_rule_23_needs(self):
        # tests/test_live_channel_law.py asserts this exact substring against SKILL.md directly (not
        # through the reference file); the rule-23 worked-proof move deliberately left it in place.
        # Restated here so a future edit that moves it out reds close to the cause, not only in the
        # other test.
        body = read_flat(SKILL_REL)
        self.assertIn("the same cure that killed invented clock stamps", body)


if __name__ == "__main__":
    unittest.main()
