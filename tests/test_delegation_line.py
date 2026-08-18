"""Every landed queue row carries its delegation accounting, and a suite check reads the queue — M-241 (SPEC INV-103, row 254).

His 2026-07-12 ~00:27 word: a landed row's status cell records its delegation — what went to a worker
with a rough saving, or a stood-down line naming why the senior kept the work; the duty binds the
orchestrator seat whatever model leads. Prose alone did not hold the routing rule until he asked what
stops the glitch. Beyond the string needles on the law's two homes, the ROADMAP scan is the mechanical
check itself: every row landed 2026-07-12 or later must carry the line.
"""

import glob
import os
import re
import unittest

from conftest import ROOT, open_spec, read_all, read_all_flat, read_flat

LANDED = re.compile(r"\*\*landed (20\d\d-\d\d-\d\d)")
BINDS_FROM = "2026-07-12"


def _queue_lines():
    """Every line of the live queue AND its archives: the union the checks scan so a landed row holds
    in both eras — pre-conversion it stands in ROADMAP.md's body, post-conversion its row has moved to
    docs/queue-archive/*.md under the live-body law (SPEC INV-276, ROADMAP row 480)."""
    files = [os.path.join(ROOT, "ROADMAP.md")]
    files += sorted(glob.glob(os.path.join(ROOT, "docs", "queue-archive", "*.md")))
    for path in files:
        with open(path, encoding="utf-8") as f:
            for line in f:
                yield line


class TestDelegationLineLaw(unittest.TestCase):
    HOMES = ("PRODUCT_SPEC.md", "skills/build-pipeline/SKILL.md")

    def test_law_in_both_homes(self):
        # PRODUCT_SPEC.md's rewrite renamed "landed" to "delivered" and folded the two
        # suite-check needles into one sentence; the skill's references/delegation-protocol.md
        # (included via read_all_flat) still carries the original wording verbatim.
        needles = {
            "PRODUCT_SPEC.md": (
                "delivered row's delivery report",
                "a suite check reds a delivered row",
                "omits the line, reading it from the archive",
                "bind the duty to the orchestrating seat whatever tier leads it",
            ),
            "skills/build-pipeline/SKILL.md": (
                "the row's delivery report",
                "a suite check reads it from the archive",
                "a delivered row without the line goes red",
                "binds the orchestrator seat regardless of",
            ),
        }
        for home in self.HOMES:
            body = read_all_flat(home)
            for needle in needles[home]:
                self.assertIn(needle, body, home)

    def test_spec_anchor_and_index(self):
        # INDEX-ROW pattern (RECIPE): the Reference table now carries locations only.
        # "delegation" prose is asserted against the flattened spec body instead.
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertRegex(spec, r"\[INV-103[,\]]")  # bare or compound anchor
        self.assertIn("delegation accounting", spec)
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-103 |"):
                    self.assertIn("R209.1", line)
                    return
        self.fail("INV-103 index row missing")

    def test_every_forward_landed_row_carries_the_line(self):
        checked = 0
        for line in _queue_lines():
            m = LANDED.search(line)
            if not m or m.group(1) < BINDS_FROM:
                continue
            cells = line.split("|")
            status = next((c for c in cells if "**landed" in c), "")
            self.assertIn(
                "delegation",
                status.lower(),
                "landed-forward row missing its delegation line: " + line[:70],
            )
            checked += 1
        self.assertGreater(checked, 0, "no forward-landed rows found to scan (body or archive)")


if __name__ == "__main__":
    unittest.main()
