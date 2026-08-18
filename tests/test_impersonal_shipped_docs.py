"""Shipped product docs state each requirement impersonally (SPEC INV-118, row 274).

A shipped product doc — the spec, the test matrix, the README, a skill card — reaches
everyone the project touches. Each requirement reads as three plain parts: the rule, the
actor as a role (the user, the producer, the target user), and the reason it holds. The
reason is load-bearing and stays; the personal attribution drops. A dated decision keeps
the date as a plain anchor and drops the name. Personal attribution and candid process
voice have one home: the local-only diaries (JOURNAL, NEXT_STEPS), which no publish ships.
"""

import unittest

from conftest import open_spec, read_flat

HOMES = ("PRODUCT_SPEC.md", "skills/spec-author/SKILL.md", "skills/publish/SKILL.md")

N1 = "the rule, the actor as a role (the user, the producer, the target user), and the reason"
N1_SPEC = "the actor as a role — the user, the producer, the target user — and the reason it holds"
N2 = "personal attribution and candid process voice"
N3 = "a dated decision keeps the date"
N3_SPEC = "a dated decision keeps its date as a plain anchor"


class TestImpersonalShippedDocs(unittest.TestCase):
    def test_impersonal_rule_in_all_three_homes(self):
        for home in HOMES:
            text = read_flat(home)
            if home == "PRODUCT_SPEC.md":
                self.assertIn(N1_SPEC, text, "%s missing needle N1_SPEC" % home)
            else:
                self.assertIn(N1, text, "%s missing needle N1" % home)

    def test_diaries_hold_attribution(self):
        for home in HOMES:
            text = read_flat(home)
            self.assertIn(N2, text, "%s missing needle N2" % home)

    def test_dated_decision_keeps_date_phrase(self):
        for home in HOMES:
            text = read_flat(home)
            if home == "PRODUCT_SPEC.md":
                self.assertIn(N3_SPEC, text, "%s missing needle N3_SPEC" % home)
            else:
                self.assertIn(N3, text, "%s missing needle N3" % home)

    def test_spec_anchor(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-118]", spec)

    def test_spec_anchor_and_index(self):
        # the index row is location-only (SPEC INV-271); "impersonal" lives on the body heading
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-118 |"):
                    break
            else:
                self.fail("INV-118 index row missing")
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("Shipped product docs state each requirement impersonally", spec)


if __name__ == "__main__":
    unittest.main()
