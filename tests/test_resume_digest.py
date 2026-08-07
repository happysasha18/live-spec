"""Row 115 (M-146, INV-48): the resume file is a digest with no redundancy —
the whole NEXT_STEPS.md holds one live-state block and nothing removable
without losing information; detail flows to the journal and queue rows it
points at; an open leg is never dropped, only stated tersely."""

import os
import unittest

from conftest import ROOT


class TestResumeDigestLaw(unittest.TestCase):
    def test_template_states_the_law(self):
        with open(os.path.join(ROOT, "templates", "NEXT_STEPS.template.md"),
                  encoding="utf-8") as f:
            t = f.read()
        self.assertIn("no redundancy", t,
                      "the template must state the digest law (SPEC INV-48)")
