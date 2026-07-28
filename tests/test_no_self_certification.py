"""No self-certification of sincerity — matrix row M-223 (SPEC INV-94, row 237).

His 2026-07-10 ~13:53 word, off the README's "we say so plainly": a line that labels its author's
honesty or directness adds no information — naming not-A informs only where not-A was a live
alternative. The rule stands in the spec and the communicator, the register lint's pattern family
grows with the caught phrases, and the pack's own README is swept clean of the class.
"""

import json
import os
import unittest

from conftest import ROOT, read, read_flat


class TestNoSelfCertification(unittest.TestCase):
    def test_law_in_both_homes(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-94]", spec)
        self.assertIn("| INV-94 |", spec)
        self.assertIn("certifies its own sincerity", spec)
        comm = read_flat("skills/communicator/SKILL.md")
        self.assertIn("Self-certification", comm)
        self.assertIn("INV-94", comm)

    def test_lint_patterns_grew_with_the_caught_phrases(self):
        lint = read("scripts/preshow-register-lint.py")
        for pat_id in (
            "en-say-so-plainly",
            "en-honest-treatment",
            "en-unsoftened",
            "ru-iz-chestnogo",
            "ru-chestno-govorya",
            "ru-ne-po-pamyati",
        ):
            self.assertIn(pat_id, lint, f"lint pattern {pat_id} missing")
        floor = json.loads(read("scripts/register-lint-floor.json"))["min_patterns"]
        self.assertGreaterEqual(floor, 23, "pattern floor not raised with the family")

    def test_readme_swept_of_the_class(self):
        readme = read_flat("README.md")
        for phrase in ("we say so plainly", "honest treatment", "unsoftened",
                       "keep this list honest"):
            self.assertNotIn(phrase, readme, f"self-certification survives: {phrase}")


if __name__ == "__main__":
    unittest.main()
