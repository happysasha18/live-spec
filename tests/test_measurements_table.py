"""scripts/measurements-table.py names the reader-prompt file that its own "readings" column
description points a person at — free text in the script's own source, checked by no import.
A path move anywhere else in the tree leaves that citation dangling silently: the readings
count in docs/MEASUREMENTS.md keeps counting real readings while the prose sends a reader
chasing a file that no longer exists. This happened once already (2026-08-19): the script
named `skills/text-audit/references/reader-prompt.md`, which left the pack with the text-audit
extraction; the real prompt this project's own readings use lives at
`docs/briefs/reader-prompt.md`, confirmed by the dated records under docs/language-reads/ that
already cite it by that path. This pins the citation to a real, existing path so a second move
reds here instead of shipping silently.

Red proven 2026-08-19: substituting the dead path
(`skills/text-audit/references/reader-prompt.md`) into the script's source made this test fail,
naming the dead path in its own assertion message; restoring the real citation passed it again.
"""
import os
import re
import unittest

from conftest import ROOT

SCRIPT = os.path.join(ROOT, "scripts", "measurements-table.py")


class TestReaderPromptCitation(unittest.TestCase):
    def test_named_reader_prompt_path_exists(self):
        with open(SCRIPT, encoding="utf-8") as f:
            source = f.read()
        m = re.search(r"one fixed list of questions, at `([^`]+)`", source)
        self.assertIsNotNone(
            m, "measurements-table.py no longer names the reader-prompt path in its "
               "readings-column description — this test needs re-aiming, not deleting")
        path = m.group(1)
        full = os.path.join(ROOT, path)
        self.assertTrue(
            os.path.isfile(full),
            "measurements-table.py names %r as the reader prompt, but no file stands there — "
            "the citation is dead; fix it to the file's real current home" % path)


if __name__ == "__main__":
    unittest.main()
