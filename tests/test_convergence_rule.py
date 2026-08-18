"""The convergence principle stated once — matrix row M-234 (SPEC INV-98, row 218).

His 2026-07-10 ~10:24 word: convergence covers every process and every kind of artifact —
there is a goal, and the work walks toward it, always. The goal is an artifact the work is
held against; a paraphrase cannot serve; iterations measure distance to the goal itself;
reached levels lock by mechanism; divergence only as a named, bounded phase. String rows on
the two homes: the spec clause and the base rulebook (the playbook chapter is machine-local,
verified by deed at its own repo).
"""

import unittest

from conftest import open_spec, read_flat


class TestConvergenceRule(unittest.TestCase):
    HOMES = ("PRODUCT_SPEC.md", "skills/live-spec-base/SKILL.md")

    def test_goal_is_an_artifact(self):
        for home in self.HOMES:
            body = read_flat(home)
            self.assertIn("the work can be held against", body, home)
        self.assertIn(
            "A paraphrase cannot serve as the goal.",
            read_flat("skills/live-spec-base/SKILL.md"),
        )
        self.assertIn(
            "A paraphrase cannot serve as that goal.", read_flat("PRODUCT_SPEC.md")
        )

    def test_distance_to_the_goal_itself(self):
        self.assertIn(
            "a proxy never replaces the goal", read_flat("skills/live-spec-base/SKILL.md")
        )
        self.assertIn(
            "a stand-in is where a look-alike is born", read_flat("PRODUCT_SPEC.md")
        )

    def test_levels_lock_and_divergence_bounded(self):
        self.assertIn("locks by a mechanism", read_flat("skills/live-spec-base/SKILL.md"))
        self.assertIn("lock it by a mechanism", read_flat("PRODUCT_SPEC.md"))
        for home in self.HOMES:
            body = read_flat(home)
            self.assertIn("named and bounded by its convergence point", body, home)

    def test_spec_anchor_index_and_playbook_cite(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-98]", spec)
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-98 |"):
                    self.assertIn("convergence point", spec)
                    break
            else:
                self.fail("INV-98 index row missing")
        base = read_flat("skills/live-spec-base/SKILL.md")
        self.assertIn("PLAYBOOK.md", base)


if __name__ == "__main__":
    unittest.main()
