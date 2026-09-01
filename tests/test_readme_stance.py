"""The README states the feels boundary as the method's own position — M-250 (rides INV-84/INV-83, row 242).

Born of gate h (SPEC INV-97, this repo attached as its own first host) correctly blocking a
README-only push (2026-07-12): `check_tests_present.py` reds on any user-facing diff (README.md is a
registered `user_facing_globs` entry) that touches nothing under tests/, whether or not the row mints
an invariant or matrix row. Row 242 is prose-only (INV-84 clean-writer authorship, INV-83 the pre-show
register lint) and mints no new spec clause — this string pin exists solely to satisfy that gate, not
because the row needed a new law. It pins the clean writer's paragraph appended to the README's "Why
live-spec, when BMAD…" critique block, before "## Known issues".
"""

import os
import re
import unittest

from conftest import ROOT, read_flat


class TestReadmeStanceParagraph(unittest.TestCase):
    def test_stance_paragraph_present(self):
        body = read_flat("README.md")
        self.assertIn("A spec owns what a project can write down and test.", body)
        self.assertIn("Feel belongs to the owner's eye.", body)
        # "will ever catch" tightened to "will catch" in the current copy.
        self.assertIn("no rubric will catch honestly", body)

    def test_stance_paragraph_before_known_issues(self):
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
            text = f.read()
        stance_idx = text.find("A spec owns what a project can write down and test.")
        known_issues_idx = text.find("Known issues")
        self.assertGreater(stance_idx, -1, "stance paragraph not found")
        self.assertGreater(known_issues_idx, -1, "Known-issues section not found")
        self.assertLess(
            stance_idx, known_issues_idx,
            "stance paragraph must sit before the Known-issues section",
        )


class TestReadmeNoCommandSurface(unittest.TestCase):
    """Row 312: the README states plainly there is no command surface to learn — you drive
    it by talking and the pipeline runs underneath. Pins the strengthened intro sentence."""

    def test_no_command_surface_stated(self):
        body = read_flat("README.md")
        # the semicolon join became two sentences: "There is no CLI. You talk to it."
        self.assertIn("There is no CLI. You talk to it", body)


class TestReadmeTurnkeyGoalParagraph(unittest.TestCase):
    """The README states the pack's actual end goal, not only the spec-code gap it already
    closes — the owner asked for this directly, 2026-08-25: a compact autonomous software
    house (the mandate's own words, `LIVESPEC_DIRECTOR_REBUILD_PLAN.md`) was the pack's whole
    point and the README never said so. Pins the added paragraph and its explicit
    still-under-construction framing (a fast reader could otherwise mistake the direction for
    an already-shipped capability, since the surrounding prose reads as present-tense fact)."""

    def test_turnkey_goal_paragraph_present(self):
        body = read_flat("README.md")
        self.assertIn(
            "a small, self-running engineering team sitting behind your one conversation", body)
        self.assertIn(
            "ask you only about taste, strategy, authority, and anything irreversible", body)

    def test_turnkey_goal_paragraph_marked_not_yet_delivered(self):
        body = read_flat("README.md")
        self.assertIn("still under construction", body)
        self.assertIn("What ships today is the first working piece of that goal", body)

    def test_turnkey_goal_paragraph_after_the_spec_code_gap(self):
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
            text = f.read()
        gap_idx = text.find("There is no CLI. You talk to it")
        goal_idx = text.find("self-running engineering team sitting behind your one conversation")
        self.assertGreater(gap_idx, -1, "the spec-code gap paragraph not found")
        self.assertGreater(goal_idx, -1, "turnkey goal paragraph not found")
        self.assertLess(
            gap_idx, goal_idx,
            "the turnkey goal paragraph must follow the spec-code gap it builds on",
        )


class TestReadmeFirstStepInstallsTheProver(unittest.TestCase):
    """A stranger who obeys the first step ends up with the reviewer the pack pins a version
    of. `install.sh` skips any skill carrying its own `.git`, and `product-prover` only ever
    exists as such a clone, so the page must name the script that fetches it — a rehearsal of
    the stranger walk ended with ten skills and no reviewer when the page did not."""

    def test_step_one_names_the_external_skill_installer(self):
        body = read_flat("README.md")
        step_one = body.split("Step 2", 1)[0]
        self.assertIn("scripts/install-external-skills.sh", step_one,
                      "the first step must name the script that installs product-prover")

    def test_the_pack_still_needs_the_skill_that_step_installs(self):
        """If the prover pack ever stops naming it, this step stops being load-bearing."""
        self.assertIn("product-prover", read_flat("skills/product-prover-pack/SKILL.md"))


class TestReadmeKnownIssuesNoFalseDiscoveryPatternClaim(unittest.TestCase):
    """The Known-issues section has three times carried the false claim that this repo's own
    `surface_discovery_pattern` cannot match plain markdown and that `check_completeness.py`
    silently passes as a result. Both halves are false — the pattern is deliberately armed
    (`tests/test_four_checks_contract.py::test_own_attach_arms_the_discovery_pattern` locks it
    catching) and a live plant of `<section id="...">` still reds the check
    (`completeness.rendered-but-unregistered`). Debunked once, 2026-08-18
    (`docs/prover/2026-08-18-readme-false-known-issue.md`), the claim regenerated via a later
    cold-read pass and survived a 2026-08-27 fix that only reworded around the check's own
    substring scan without removing the false substance, then closed again 2026-09-01 (q-501,
    commit e3b745b1).

    Each reappearance traces to the same source, not three unrelated bugs: `text-audit`'s
    fresh-reader design (attic/inbox-2026-08-05-from-promoter-readme-replacement-returns-corrected.md,
    "How the draft was worked") runs a reader with no memory of prior findings by design, so the
    same first-glance oddity — an HTML-tag regex sitting over markdown files — reads as a bug to
    every reader meeting it cold, however many times an earlier reader's conclusion was refuted.
    That design is not what is broken here and stays untouched. This test is the guard the design
    itself cannot provide: it fails the suite if the substance returns under any rewording, so a
    fourth reappearance is caught here instead of needing a fourth manual read-and-fix. Mirrors
    SURFACES.md's own precedent for this shape of problem — pin the content that must (not) be
    present and let a rewrite that breaks it turn red — rather than adding new machinery."""

    # Either half of the false claim, phrased loosely enough to survive a paraphrase: the pattern
    # keyed to a negative-match/inert verdict, or the completeness check keyed to a silent-pass
    # verdict. `re.S` lets the co-occurrence span a wrapped sentence.
    FALSE_CLAIM_SIGNATURES = [
        re.compile(r"(?:surface_)?discovery[ _]pattern.{0,220}"
                   r"(?:matches? nothing|can(?:not|['’]t) match|is inert)", re.S | re.I),
        re.compile(r"(?:matches? nothing|can(?:not|['’]t) match|is inert).{0,220}"
                   r"(?:surface_)?discovery[ _]pattern", re.S | re.I),
        re.compile(r"check_completeness\.py.{0,220}"
                   r"(?:silently pass|passes? (?:clean )?while seeing (?:no|nothing))", re.S | re.I),
        re.compile(r"(?:silently pass|passes? (?:clean )?while seeing (?:no|nothing)).{0,220}"
                   r"check_completeness\.py", re.S | re.I),
    ]

    def _known_issues_section(self):
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
            text = f.read()
        start = text.find("**Known issues.**")
        self.assertGreater(start, -1, "Known issues section not found")
        end = text.find("\n---", start)
        section = text[start:end] if end != -1 else text[start:]
        return " ".join(section.split())

    def test_known_issues_carries_no_false_discovery_pattern_claim(self):
        section = self._known_issues_section()
        for pattern in self.FALSE_CLAIM_SIGNATURES:
            match = pattern.search(section)
            self.assertIsNone(
                match,
                "Known issues section regenerated the debunked claim that the discovery "
                "pattern can't match markdown, or that check_completeness.py silently "
                "passes as a result (matched %r) -- both are false; see "
                "docs/prover/2026-08-18-readme-false-known-issue.md and q-501's 2026-09-01 "
                "entry in PLAN.md" % (match.group(0) if match else None,),
            )


if __name__ == "__main__":
    unittest.main()
