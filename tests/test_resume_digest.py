"""M-146 / INV-48: the resume file is a taskless transient-state digest."""

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
        self.assertIn("PLAN.md", t)
        self.assertIn("TRANSIENT EXECUTION STATE", t)
