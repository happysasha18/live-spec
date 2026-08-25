"""A confirmed bug drives a class hunt before it closes — INV-124.

Four moves, not one: (1) name the defect abstractly and go FIND the un-seen siblings, fixing all in the
same change; (2) check the architecture for a structural cause; (3) check the spec — a spec silent on the
broken behaviour is the real defect, fixed first so the prover can flag it; (4) escalate to the human when
the class boundary needs his read. The product-prover carries the class lens for the same questions. The
four moves are the bug door's close condition. Homes: the F-bug spec clause, build-pipeline's bug entry,
product-prover's class lens, base rule 14. (Born of the exhibition's pinch-zoom bug — one report turned
into five live siblings, 2026-07-12.)
"""

import re
import unittest

from conftest import external_clone_or_skip, open_spec, read, read_all_flat, read_flat


class TestClassHunt(unittest.TestCase):
    def test_base_rule_14_goes_and_finds_the_class(self):
        base = read_flat("skills/live-spec-base/SKILL.md")
        self.assertIn("go find the class, sweep the look-alikes", base)
        self.assertIn("the siblings not yet seen", base)
        self.assertIn("escalate to the human when the class boundary needs his read", base)

    def test_spec_clause_stands(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("A confirmed bug drives a class hunt before it closes", spec)
        self.assertIn("[INV-124]", spec)

    def test_spec_names_the_four_moves(self):
        spec = read_flat("PRODUCT_SPEC.md")
        for needle in (
            "search every surface",
            "a structural cause",
            "fix the spec first so the prover can flag it",
            "the class boundary needs the human's read",
        ):
            self.assertIn(needle, spec, needle)

    def test_formal_index_row(self):
        # The generated index carries locations only (SPEC INV-271); "class hunt" prose lives in the
        # body criterion (asserted above). Here the index must map INV-124 to at least one location.
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-124 |"):
                    self.assertRegex(line, r"R\d+\.\d+")
                    return
        self.fail("INV-124 index row missing")

    def test_build_pipeline_bug_entry_drives_the_hunt(self):
        bp = read_flat("skills/build-pipeline/SKILL.md")
        self.assertIn("A confirmed bug drives a class hunt before it closes (SPEC INV-124)", bp)
        self.assertIn("The hunt is four moves:", bp)

    def test_director_has_its_own_home_for_the_hunt(self):
        """Director's own top-level text carries no door/work-kind vocabulary, so this fact's
        Director-side home is a reworded reference, not a lift of build-pipeline's prose — see
        docs/prover/2026-08-25-class-hunt-director-home.md for why a near-verbatim first and
        second draft were each rejected on review."""
        director = read_all_flat("skills/director/SKILL.md")
        self.assertIn("references/class-hunt.md", director)
        hunt = read_flat("skills/director/references/class-hunt.md")
        for needle in (
            "Name the defect's class",
            "Read the architecture for a structural cause",
            "Read the spec for the same gap",
            "Bring the human in where the class boundary is a judgment call",
            "SPEC INV-26",
        ):
            self.assertIn(needle, hunt, needle)

    def test_prover_carries_the_class_lens(self):
        # the SPEC INV-124 tie is a pack anchor: since the v5.0.0 externalization the generic
        # prover canon carries no project codes, and the pack adapter binds the class lens to
        # the confirmed-bug class hunt instead.
        pack = read_flat("skills/product-prover-pack/SKILL.md")
        self.assertIn("the document-side face of the confirmed-bug class hunt", pack)
        self.assertIn("INV-124", pack)
        # The tracked-adapter anchors above hold on a bare checkout; only the canon read below needs the clone.
        external_clone_or_skip()
        pv = read_all_flat("skills/product-prover/SKILL.md")
        self.assertIn("Class lens", pv)

    def test_the_class_lens_owes_a_line_where_it_stands(self):
        """ROADMAP row 611 — the class lens stands in a tier of its own and owes a line.

        The imaginative-probe tier reads "no verdict is owed", and the class lens sat under it, so a
        pass could file a point finding, skip the sweep, and owe no line saying so. The lens now
        stands beside that tier with the reason it stands apart, and it owes one line per pass.

        Each needle here names the class line. A needle reading only "reads as a skipped sweep"
        would pass against the mandatory-sweep paragraph, which carried that sentence before this
        duty existed.
        """
        external_clone_or_skip()
        pv = read_all_flat("skills/product-prover/SKILL.md")
        # the standing-duty paragraph lives in the canon's reference/stress-lenses.md now, as
        # its own "The class lens" section, and the canon says "review" where the pack said
        # "pass" — the duty (its own tier, one line every time, silence reads as a skip) holds.
        self.assertIn("One duty standing beside the probes above, in a tier of its own", pv)
        self.assertIn("it runs on every review, whatever the document holds", pv)
        self.assertIn("Every review writes one class line in its record", pv)
        self.assertIn("writes no class line reads as a skipped sweep", pv)
        self.assertIn("`Class lens: swept — <the classes filed>`", pv)

    def test_readme_names_the_class_lens(self):
        """A standalone reader learns the sweep exists from the README alone (row 611)."""
        external_clone_or_skip()
        rd = read_flat("skills/product-prover/README.md")
        self.assertIn("The class lens stands beside them, and it owes a line of its own", rd)
        self.assertIn("Each pass records whether that sweep ran", rd)

    def test_matrix_row_covers_the_class_hunt(self):
        for line in read("TEST_MATRIX.md").splitlines():
            if line.startswith("| M-265 |"):
                self.assertIn("INV-124", line)
                return
        self.fail("M-265 matrix row missing")


CLASS_LINE = re.compile(
    r"^Class lens:\s*(?:(swept|N/A)\s*—\s*\S.*?|(no class))\s*$",
    re.MULTILINE)


def class_line_verdict(record):
    """The class line a persisted prover record owes, or None where the record carries none.

    The rule this embodies is the skill's, stated under the surface × sweep table: every pass
    writes one class line reading `Class lens: swept — <the classes filed>`, `Class lens: no
    class`, or `Class lens: N/A — <reason>`. The swept line names each class the pass filed, so a
    bare `swept` carries no sweep anyone can read. A record with no class line at all owes a
    verdict nobody wrote, and it reads as a skipped sweep. A missing line never reads as a clean
    one, which is the reading INV-171 gives a missing sweep verdict. The check is embodied here, in
    fixtures alone: the records already on disk predate the rule, and the push gate this would
    become is a later row's work.
    """
    hit = CLASS_LINE.search(record)
    return (hit.group(1) or hit.group(2)) if hit else None


_POINT_FINDING = (
    "## F1 — The caption law is scoped to one surface\n\n"
    "`recommendation · now · confusing-for-users (cognitive-load)`\n\n"
    "| Surface | Cross-cutting laws | Edge conditions |\n"
    "|---|---|---|\n"
    "| Gallery | clean | hit (F1) |\n"
)


class TestClassLineFixtures(unittest.TestCase):
    """ROADMAP row 611 — a pass with a point finding and no class line reds."""

    def test_a_point_finding_with_no_class_line_reds(self):
        self.assertIsNone(class_line_verdict(_POINT_FINDING))

    def test_a_swept_line_naming_its_class_passes(self):
        record = _POINT_FINDING + "\nClass lens: swept — the scoped-caption class, F1 and F4.\n"
        self.assertEqual("swept", class_line_verdict(record))

    def test_the_three_verdicts_each_pass(self):
        for line in ("Class lens: swept — the scoped-caption class",
                     "Class lens: no class",
                     "Class lens: N/A — section 7 arrived as a stub, so the whole document "
                     "was never in view"):
            record = _POINT_FINDING + "\n" + line + "\n"
            self.assertIsNotNone(class_line_verdict(record), line)

    def test_a_bare_swept_line_reds(self):
        """The swept line names each class filed, so `swept` on its own carries no sweep."""
        record = _POINT_FINDING + "\nClass lens: swept\n"
        self.assertIsNone(class_line_verdict(record))

    def test_an_empty_reason_reds(self):
        record = _POINT_FINDING + "\nClass lens: N/A — \n"
        self.assertIsNone(class_line_verdict(record))


if __name__ == "__main__":
    unittest.main()
