"""One canonical state directory; worktree isolation by default on overlap — M-244 (SPEC INV-105, row 227).

The audit found a ghost `.livespec` dir with a different profile beside the real `.live-spec` (two
competing truths), and overlapping write-sets ran unisolated (2026-07-10). The law: the canonical state
directory is named `.live-spec`, once; a near-miss dir found at attach or resume is a red finding retired
to the attic under a manifest line; and worktree isolation is the default when two lanes' write-sets
overlap. String rows on the law's three homes plus the INV-105 anchor and index.
"""

import unittest

from conftest import open_spec, read_flat


class TestCanonicalStateDirLaw(unittest.TestCase):
    def test_canonical_name_in_both_attach_and_spec(self):
        self.assertIn(
            "the canonical state directory is named", read_flat("adopt/ADOPT.md"), "adopt/ADOPT.md"
        )
        self.assertIn(
            "one canonical state directory named `.live-spec`",
            read_flat("PRODUCT_SPEC.md"),
            "PRODUCT_SPEC.md",
        )

    def test_lookalike_retired_to_attic(self):
        for home in ("PRODUCT_SPEC.md", "adopt/ADOPT.md"):
            body = read_flat(home)
            # The requirements-format spec states the retire-a-near-miss rule compactly; adopt carries
            # the attach/resume framing. Both homes state a near-miss look-alike retired to the attic
            # under a manifest line naming the path, the reason, and the canonical directory.
            self.assertIn("to the attic under a manifest line", body, home)
            self.assertIn("manifest line naming the path, the reason, and the canonical directory", body, home)

    def test_worktree_default_in_both_fence_homes(self):
        self.assertIn(
            "worktree isolation is the default when two lanes' write-sets overlap",
            read_flat("skills/live-spec-base/SKILL.md"),
            "skills/live-spec-base/SKILL.md",
        )
        self.assertIn(
            "two lanes' write-sets overlap, the system *shall* default the later lane to worktree isolation",
            read_flat("PRODUCT_SPEC.md"),
            "PRODUCT_SPEC.md",
        )

    def test_spec_anchor_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-105", spec)
        self.assertIn("one canonical state directory named `.live-spec`", spec)
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-105 |"):
                    return
        self.fail("INV-105 index row missing")


if __name__ == "__main__":
    unittest.main()
