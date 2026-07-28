"""The catch-up walk — matrix rows M-217/M-218/M-219/M-220 (SPEC A-11, INV-89, INV-90, INV-91).

String-level rows on the SHIPPED guides: MIGRATION.md is the walk's operating guide, ADOPT.md holds
the canonical document set once, adoption.md and pair-adoption.md point and route. Red-proven against
the pre-rewrite guides on 2026-07-10 (the old MIGRATION.md was a single rename note with a
non-idempotent `git mv` step and no walk at all).
"""

import os
import unittest

from conftest import read_flat


class TestCatchupWalk(unittest.TestCase):
    """M-217 — the walk has one named home with routing, four phases, and the owner's gate."""

    def test_catchup_walk(self):
        # RE-PINNED pass-2 (see repin log): the pass-2 restore moved every pilot-unit feature
        # tag (F-bootstrap, F-adoption, F-catchup, F-onboarding, F-pair) onto its own-line
        # "[feature: F-...]" heading tag instead of citing it inline in the User Story — the
        # convention is applied consistently across all five, not just this one. F-catchup now
        # sits on Requirement 180's H2 heading; A-11 stays inline in the User Story/criteria.
        spec = read_flat("PRODUCT_SPEC.md")
        # the spec side: the scenario and its anchors exist
        self.assertIn(
            "## Requirement 180: The catch-up sequence brings an adopted host onto the current pack"
            " [feature: F-catchup]",
            spec,
        )
        for anchor in ("[A-11]", "[INV-89]", "[INV-90]", "[INV-91]"):
            self.assertIn(anchor, spec, f"spec anchor {anchor} missing")

        mig = read_flat("MIGRATION.md")
        # routing opens the guide
        self.assertIn("## When to run this", mig)
        self.assertIn("A host that never adopted the pack goes to adoption", mig)
        self.assertIn("A host that already adopted goes to this catch-up walk", mig)
        # the four phases, in the spec's order
        for phase in (
            "Phase 1 — orient on the delta",
            "Phase 2 — plan, behind the owner's gate",
            "Phase 3 — execute, preserving facts",
            "Phase 4 — verify and re-record",
        ):
            self.assertIn(phase, mig, f"phase heading missing: {phase}")
        self.assertLess(
            mig.index("Phase 1 — orient"), mig.index("Phase 2 — plan"),
            "phases out of order",
        )
        self.assertLess(mig.index("Phase 2 — plan"), mig.index("Phase 3 — execute"))
        self.assertLess(mig.index("Phase 3 — execute"), mig.index("Phase 4 — verify"))
        # the gate before any file moves; the plan's home; reversibility; resumability
        self.assertIn("The owner's word on the plan comes before any file moves", mig)
        self.assertIn(".live-spec/adopt/", mig)
        self.assertIn("baseline commit", mig)
        self.assertIn("checkpoint", mig)

    def test_catchup_pair_and_machine_level(self):
        """M-217 (pair + once-per-machine legs)."""
        mig = read_flat("MIGRATION.md")
        self.assertIn("one inbox wish naming the other half's catch-up debt", mig)
        self.assertIn("runs the full adoption for that repo", mig)
        self.assertIn("once per machine", mig)
        self.assertIn("already-done check", mig)
        pair = read_flat("docs/pair-adoption.md")
        self.assertIn("one inbox wish naming the other half's catch-up debt", pair)


class TestCatchupHalfDoneSafety(unittest.TestCase):
    """M-218 — every step safe on a half-done state (INV-89)."""

    def test_precondition_and_merge_law(self):
        mig = read_flat("MIGRATION.md")
        self.assertIn("reads its precondition from the tree", mig)
        self.assertIn("already holds is reported done and skipped", mig)
        self.assertIn("merge file by file", mig)
        self.assertIn("never nest the old directory inside the new one", mig)
        self.assertIn("never overwrite the new form with the old", mig)
        self.assertIn("rides the plan to the owner's gate", mig)
        # the concrete born-of case: both state dirs exist
        self.assertIn("both exist", mig)
        # the installed set is read from disk, and the shared-profile write re-reads first
        self.assertIn("version lines of the skills actually installed", mig)
        self.assertIn("immediately before appending", mig)

    def test_never_a_bare_git_mv(self):
        """The old non-idempotent step 1 is gone: no unconditional rename instruction."""
        mig = read_flat("MIGRATION.md")
        self.assertNotIn(
            "`git mv .livespec .live-spec` — the host's pack folder",
            mig,
            "the old unconditional git-mv step is still in the guide",
        )


class TestCatchupPreserveAndRehome(unittest.TestCase):
    """M-219 — preserve facts, re-home them, one canonical list (INV-90)."""

    def test_no_blanket_rewrite_and_naming(self):
        mig = read_flat("MIGRATION.md")
        self.assertIn(
            "Settled prose is rewritten only where the owner rejected it "
            "or where the new shape cannot hold it as written",
            mig,
        )
        self.assertIn("spec.file", mig)
        self.assertIn(".live-spec/checkpoints/", mig)

    def test_canonical_set_has_one_home(self):
        heading = "## The canonical document set"
        self.assertIn(heading, read_flat("adopt/ADOPT.md"))
        for other in ("docs/adoption.md", "docs/pair-adoption.md", "MIGRATION.md"):
            self.assertNotIn(
                heading, read_flat(other),
                f"second canonical-set list in {other} — the one home is ADOPT.md",
            )
        self.assertIn("The canonical document set lives in `adopt/ADOPT.md`", read_flat("docs/adoption.md"))

    def test_spec_file_row_in_defaults_table(self):
        self.assertIn("spec.file", read_flat("skills/live-spec-base/SKILL.md"))


class TestCatchupSelfTest(unittest.TestCase):
    """M-221 — the walk's before-and-after self-test and the named restore point (INV-92)."""

    def test_before_after_inventory_and_restore(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-92]", spec)
        mig = read_flat("MIGRATION.md")
        self.assertIn("pre-walk inventory", mig)
        self.assertIn("fingerprint", mig)
        self.assertIn("anchor multiset", mig)
        self.assertIn("at least as green as before", mig)
        self.assertIn("restore point", mig)
        self.assertIn("restore command", mig)


class TestCatchupVersionChain(unittest.TestCase):
    """M-220 — per-version migration chapters, the chain walked oldest first (INV-91)."""

    def test_chapters_and_chain(self):
        mig = read_flat("MIGRATION.md")
        self.assertIn("## Migration chapters", mig)
        self.assertIn("### 1.0.0", mig)
        self.assertIn("oldest first", mig)
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("dated migration chapter", spec)

    def test_versionless_record_starts_at_earliest_chapter(self):
        """The dry-read hole (2026-07-10): an old-format record has no readable version —
        the chain's start must be stated, in the spec and in the guide.

        RE-PINNED (see repin log): MIGRATION.md's sentence subject is "a record" ("... starts
        the chain..."), while PRODUCT_SPEC.md's rewritten Requirement 180 criterion 3 casts
        every clause as "the system *shall*..." ("...shall start the chain..." — grammatical
        conjugation only, same fact). The shared substring below matches the same meaning at
        both homes without depending on either home's subject/verb form.
        """
        for rel in ("MIGRATION.md", "PRODUCT_SPEC.md"):
            self.assertIn(
                "the chain at the earliest chapter", read_flat(rel),
                f"no-readable-version fallback missing in {rel}",
            )


if __name__ == "__main__":
    unittest.main()
