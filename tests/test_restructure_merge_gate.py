"""A restructure/migration merge gate judges the delta, in three parts — M-253 (SPEC INV-114, row 258).

The tlvphotos window's word, 2026-07-12 ~01:28 («надо переписать правила … пойми откуда пришло»): the pack
states no law today for what a restructure merge's equivalence proof consists of or how prover findings
route, so each session invents its own bar. Tonight that produced a wrong one — the orchestrator
over-sharpened his spoken «prover finds nothing both sides» into «any finding parks the merge» and parked a
strictly-improving merge on the OLD side's pre-existing clarity debts, which he corrected live: the gate
judges the DELTA. The law in three parts: (1) load-bearing token identity old-versus-new modulo the
per-chunk named deltas plus the punctuation-multiset check (INV-111); (2) the full suite green on the
merged tree (INV-39); (3) a full prover pass on both sides whose blocking set is delta-scoped — an
unmatched token, a red suite, a new-side finding absent on the old side, or an unnamed meaning change.
Pre-existing findings equal on both sides route to queue rows in the same landing and never block. And a
session that sharpens a human's spoken bar beyond his words says the sharpened form back and marks it as
its own interpretation. String rows on the law's three homes plus the spec anchor and its index row.
"""

import os
import unittest

from conftest import ROOT, external_clone_or_skip, open_spec, read_all_flat, read_flat


class TestRestructureMergeGateLaw(unittest.TestCase):
    """The law's three homes, split by who owns the bytes.

    Two of the three homes are TRACKED files this repository owns; the third is the
    externalized canon, an untracked clone that a bare checkout does not carry. A single
    loop over all three had to be guarded by the clone check, and that guard sat at the
    top — so on a bare checkout (and in CI, which installs no clone) the tracked halves
    of the law went unasserted along with the external one. The homes are therefore split
    into two tests apiece: the tracked home runs everywhere, unguarded, and only the canon
    read stands behind the guard. A bare checkout now reports the tracked assertions as
    PASSED and the canon assertions as SKIPPED, instead of reporting silence for both.

    The external home names the canon's SKILL.md, and the canon's clauses are read across the
    whole skill — SKILL.md plus its reference/*.md — because the canon offloads set-piece
    material there and release 1.6.0 moved the merge gate's mechanics out of the body. The
    skill is one home for a content-presence check, which is conftest's _skill_surface rule.
    """

    TRACKED_HOMES = (
        "PRODUCT_SPEC.md",
        "skills/director/references/landing-law.md",
    )
    EXTERNAL_HOME = "skills/product-prover/SKILL.md"

    def test_merge_gate_judges_the_delta_in_the_tracked_homes(self):
        for home in self.TRACKED_HOMES:
            body = read_flat(home)
            self.assertIn("merge gate judges the delta", body, home)
            # PRODUCT_SPEC.md's R184.1 rewords "delta-scoped" to "scoped to the delta"; the
            # skill home keeps the original compact phrasing, so each is checked its own way.
            if home == "PRODUCT_SPEC.md":
                self.assertIn("blocking set is scoped to the delta", body, home)
                # the old "token-identity part scopes to a content-preserving restructure"
                # sentence is gone; the same scoping relationship (token-identity applies to a
                # restructure, not a deliberate redesign) now lives as R184.4's exception clause.
                self.assertIn(
                    "with no token-identity demand over text the redesign meant to change",
                    body, home,
                )
            else:
                self.assertIn("blocking set is delta-scoped", body, home)
                self.assertIn("scopes to a content-preserving restructure", body, home)

    def test_merge_gate_judges_the_delta_in_the_external_canon(self):
        external_clone_or_skip()
        home = self.EXTERNAL_HOME
        # The canon's SKILL.md body still names the gate. Release 1.6.0 moved the gate's three
        # parts, its four blockers and its exception into reference/review-modes.md and left a
        # pointer in their place, so the body keeps the headline and the surface keeps the
        # mechanics. Both are asserted: a body that drops the headline hides the gate from a
        # reader who never opens the reference, and a surface that drops the scopings loses the
        # law itself.
        self.assertIn("merge gate judges the delta", read_flat(home), home)
        # the externalized canon states the same two scopings in its own words
        surface = read_all_flat(home)
        self.assertIn("blocking set is scoped to the delta", surface, home)
        self.assertIn(
            "The token-identity part applies to a restructure meant to preserve content",
            surface, home,
        )

    def test_preexisting_findings_route_not_block_in_the_tracked_homes(self):
        for home in self.TRACKED_HOMES:
            body = read_flat(home)
            if home == "PRODUCT_SPEC.md":
                # R184.3: "queue rows"/"same landing"/"never block" become singular/"delivery"/
                # "not block on it" under the shall-subjunctive requirements-format rewrite. R60's
                # rewrite then moved the routing verb again: a pre-existing finding is no longer
                # "route[d]" anywhere, it is written into the review record, same as a
                # recommendation (INV-140).
                self.assertIn(
                    "state it in the review record of the same delivery", body, home
                )
                self.assertIn("shall* not block on it", body, home)
            else:
                self.assertIn(
                    "route to queue rows in the same landing and never block", body, home
                )

    def test_preexisting_findings_route_not_block_in_the_external_canon(self):
        external_clone_or_skip()
        home = self.EXTERNAL_HOME
        # the canon's generic wording of the same routing law, which travelled with the rest of
        # the merge gate into reference/review-modes.md in release 1.6.0
        self.assertIn(
            "become tracked follow-ups in the same change and never block",
            read_all_flat(home), home,
        )

    def test_say_the_bar_back_duty_in_the_tracked_homes(self):
        for home in self.TRACKED_HOMES:
            body = read_flat(home)
            if home == "PRODUCT_SPEC.md":
                # R184.5: "say"/"mark" (shall-subjunctive) replace "says"/"marks".
                self.assertIn(
                    "shall* say the sharpened form back and mark it as its own interpretation",
                    body,
                    home,
                )
            else:
                self.assertIn(
                    "says the sharpened form back and marks it as its own interpretation",
                    body,
                    home,
                )

    def test_say_the_bar_back_duty_in_the_external_canon(self):
        external_clone_or_skip()
        home = self.EXTERNAL_HOME
        # the canon states the same duty imperatively, as the reviewer's own reading
        self.assertIn(
            "state the sharpened form back to them, and mark it as the reviewer's own reading",
            read_flat(home), home,
        )

    def test_the_split_covers_every_home_the_law_has(self):
        """The split itself is pinned: a home added to the law must land on one side.

        The defect this file was repaired for was a tracked home hiding behind an external
        guard. A future edit that adds a home to only one tuple, or drops one, would rebuild
        that hole quietly, so the union is asserted against the law's own roster.
        """
        self.assertEqual(
            set(self.TRACKED_HOMES) | {self.EXTERNAL_HOME},
            {
                "PRODUCT_SPEC.md",
                "skills/director/references/landing-law.md",
                "skills/product-prover/SKILL.md",
            },
        )
        self.assertNotIn(self.EXTERNAL_HOME, self.TRACKED_HOMES)
        for home in self.TRACKED_HOMES:
            self.assertTrue(
                os.path.isfile(os.path.join(ROOT, home)),
                "%s is listed as tracked but is not on disk — a tracked home must be "
                "readable on a bare checkout" % home,
            )

    def test_spec_anchor_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-114]", spec)
        row = None
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-114 |"):
                    row = line
                    break
        self.assertIsNotNone(row, "INV-114 index row missing")
        # index now carries locations only (SPEC INV-271) — no prose and no Section cell to
        # check; the "delta" prose check moves onto the body requirement heading that carries
        # INV-114 (already asserted in test_merge_gate_judges_the_delta_in_all_homes above).
        self.assertIn(
            "A restructure or migration merge gate judges the delta",
            read_flat("PRODUCT_SPEC.md"),
        )


if __name__ == "__main__":
    unittest.main()
