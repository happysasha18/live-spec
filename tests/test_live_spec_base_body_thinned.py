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
reference files (so a later edit cannot silently empty one), and every one of the numbered rules
still standing has its heading in the body (a rule may fold, shrink, or pointer out its illustration,
but it may never vanish once kept).

2026-08-26 (PLAN.md step 7, commit 0ae778bc) cut thirteen more rule numbers whole — 11, 14, 15, 18,
19, 20, 21, 23, 28, 32, 33, 34, 35 — for carrying no eval fixture and no executable script, moving
their text to attic/live-spec-base-unbacked-rules-2026-08-26.md; twenty-one rule numbers stand today.
That cut is a legitimate removal, not the drift this test guards against, so RULE_NUMBERS below
tracks the current surviving set rather than the historical 34.
"""

import os
import re
import unittest

from conftest import ROOT, read, read_flat

SKILL_REL = os.path.join("skills", "live-spec-base", "SKILL.md")
GLOSSARY_REL = os.path.join("skills", "live-spec-base", "references", "glossary.md")
EXAMPLES_REL = os.path.join("skills", "live-spec-base", "references", "worked-examples.md")
SETTINGS_LADDER_REL = os.path.join("skills", "live-spec-base", "references", "settings-ladder.md")
RULE_ORIGINS_REL = os.path.join("skills", "live-spec-base", "references", "rule-origins.md")

# The 21 rule numbers this rulebook carries today. Rule 30 was cut whole (his D2 word
# 2026-08-11); rules 11, 14, 15, 18, 19, 20, 21, 23, 28, 32, 33, 34, 35 were cut 2026-08-26
# (PLAN.md step 7, commit 0ae778bc) for carrying no eval fixture and no executable script,
# moved to attic/live-spec-base-unbacked-rules-2026-08-26.md. Every cut number stays
# retired, never reused (the body's own "## The shared rules" preamble states this). Not
# derived from the file here on purpose — this is the independent census the description's
# own rule-count claim is checked against elsewhere (tests/test_request_classifier.py); this
# test instead asserts each number's heading survives by name, so a silent drop reds even if
# the total count coincidentally still matches (e.g. two rules merging while a third is cut).
RETIRED_RULE_NUMBERS = {11, 14, 15, 18, 19, 20, 21, 23, 28, 30, 32, 33, 34, 35}
RULE_NUMBERS = tuple(n for n in range(1, 36) if n not in RETIRED_RULE_NUMBERS)

# Ratchet, not a target: an earlier session's move brought the body from 620 to 606 lines; this one
# moved five bare dated citations to docs/lenses.md with no pointer left behind (the one pattern a
# reverted second-pass attempt proved byte-positive — docs/prover/2026-08-25-live-spec-base-second-pass.md),
# landing at 602. A further session compressed rules 6/14/19/29/31 in place — merging sentences,
# cutting connective filler, removing one confirmed duplicate (rule 6's leave-word restatement) —
# landing at 592 (docs/prover/2026-08-25-a7-rule-compression.md). Still well past skill-creator's
# <500-line ideal (the number test_communicator_body_thinned.py's IDEAL_MAX_LINES derives from,
# ~/.claude/skills/skill-creator/SKILL.md). Getting live-spec-base under 500 is a further
# structural move — grouping or folding rules, the way communicator needed a second pass (row 280)
# after its first reference-extraction (row 266) still left it at 565 lines. Until that second
# pass happens here, this threshold holds the line at "no regrowth past where this session left
# it", with headroom for small, legitimate edits — not "under the ideal".
CURRENT_MAX_LINES = 598


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
        # Every retired number (rule 30's cut plus the thirteen cut 2026-08-26) stays retired;
        # a heading reappearing for any of them is its own kind of drift, out of this test's
        # scope, but worth not silently accepting here either.
        reappeared = found & RETIRED_RULE_NUMBERS
        self.assertFalse(
            reappeared,
            "rule(s) %r are retired and should carry no heading of their own" % sorted(reappeared),
        )

    def test_reference_modules_exist_and_body_points_at_each(self):
        flat = read_flat(SKILL_REL)
        for rel, name in (
            (GLOSSARY_REL, "glossary"),
            (EXAMPLES_REL, "worked-examples"),
            (SETTINGS_LADDER_REL, "settings-ladder"),
            (RULE_ORIGINS_REL, "rule-origins"),
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

    def test_rule_41s_relocated_history_lives_in_rule_origins(self):
        """2026-09-05: rule 41's own dated history (the two boards' measured numbers, the
        retired raised-field attempt) moved out of the body into references/rule-origins.md's
        new "## Rule 41" section, replaced by a one-line pointer — the same shape rule 40's own
        entry already used. Every operative sentence of the rule stayed in the body; only this
        test guards the moved half against silently emptying."""
        body = read_flat(SKILL_REL)
        self.assertIn(
            "references/rule-origins.md", body,
            "rule 41 dropped its pointer to references/rule-origins.md",
        )
        origins = read_flat(RULE_ORIGINS_REL)
        self.assertIn(
            "## Rule 41 — a row is opened by the person, or by a defect someone outside "
            "this repository meets",
            origins, "rule-origins.md lost rule 41's own section heading",
        )
        for needle in (
            "53 of 106",
            "thirty-three rows to eleven",
            "a `raised` field on every row, was refused for exactly that reason",
        ):
            self.assertIn(
                needle, origins,
                "rule-origins.md's Rule 41 section is missing relocated text: %s" % needle,
            )

    # base rule 23 (the live-channel law this sentence closed) was cut 2026-08-26 (PLAN.md
    # step 7, commit 0ae778bc, moved to attic/live-spec-base-unbacked-rules-2026-08-26.md):
    # no eval fixture or executable script enforced its exact wording, only this prose lock
    # and its sibling in tests/test_live_channel_law.py (which is now red for the same
    # reason — out of this task's file scope, flagged in the report rather than fixed here).


if __name__ == "__main__":
    unittest.main()
