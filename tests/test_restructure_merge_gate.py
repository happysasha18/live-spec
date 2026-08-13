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

from conftest import ROOT, external_clone_or_skip, read_flat


class TestRestructureMergeGateLaw(unittest.TestCase):
    HOMES = (
        "PRODUCT_SPEC.md",
        "skills/product-prover/SKILL.md",
        "skills/build-pipeline/SKILL.md",
    )

    def test_merge_gate_judges_the_delta_in_all_homes(self):
        external_clone_or_skip()
        for home in self.HOMES:
            body = read_flat(home)
            self.assertIn("merge gate judges the delta", body, home)
            # PRODUCT_SPEC.md's R184.1 rewords "delta-scoped" to "scoped to the delta"; the two
            # skill homes keep the original compact phrasing, so each is checked its own way.
            if home == "PRODUCT_SPEC.md":
                self.assertIn("blocking set is scoped to the delta", body, home)
                # the old "token-identity part scopes to a content-preserving restructure"
                # sentence is gone; the same scoping relationship (token-identity applies to a
                # restructure, not a deliberate redesign) now lives as R184.4's exception clause.
                self.assertIn(
                    "with no token-identity demand over text the redesign meant to change",
                    body, home,
                )
            elif home == "skills/product-prover/SKILL.md":
                # the externalized canon states the same two scopings in its own words
                self.assertIn("blocking set is scoped to the delta", body, home)
                self.assertIn(
                    "The token-identity part applies to a restructure meant to preserve content",
                    body, home,
                )
            else:
                self.assertIn("blocking set is delta-scoped", body, home)
                self.assertIn("scopes to a content-preserving restructure", body, home)

    def test_preexisting_findings_route_not_block_in_all_homes(self):
        external_clone_or_skip()
        for home in self.HOMES:
            body = read_flat(home)
            if home == "PRODUCT_SPEC.md":
                # R184.3: "queue rows"/"same landing"/"never block" become singular/"delivery"/
                # "not block on it" under the shall-subjunctive requirements-format rewrite.
                self.assertIn(
                    "route it to a queue row in the same delivery", body, home
                )
                self.assertIn("shall* not block on it", body, home)
            elif home == "skills/product-prover/SKILL.md":
                # the canon's generic wording of the same routing law
                self.assertIn(
                    "become tracked follow-ups in the same change and never block", body, home
                )
            else:
                self.assertIn(
                    "route to queue rows in the same landing and never block", body, home
                )

    def test_say_the_bar_back_duty_in_all_homes(self):
        external_clone_or_skip()
        for home in self.HOMES:
            body = read_flat(home)
            if home == "PRODUCT_SPEC.md":
                # R184.5: "say"/"mark" (shall-subjunctive) replace "says"/"marks".
                self.assertIn(
                    "shall* say the sharpened form back and mark it as its own interpretation",
                    body,
                    home,
                )
            elif home == "skills/product-prover/SKILL.md":
                # the canon states the same duty imperatively, as the reviewer's own reading
                self.assertIn(
                    "state the sharpened form back to them, and mark it as the reviewer's own "
                    "reading",
                    body,
                    home,
                )
            else:
                self.assertIn(
                    "says the sharpened form back and marks it as its own interpretation",
                    body,
                    home,
                )

    def test_spec_anchor_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-114]", spec)
        row = None
        with open(os.path.join(ROOT, "PRODUCT_SPEC.md"), encoding="utf-8") as f:
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
