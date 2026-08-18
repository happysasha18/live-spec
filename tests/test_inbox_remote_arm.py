"""The inbox door has a remote arm — M-251 (SPEC INV-112, row 247).

The owner thought the cloud seat through mid-session on 2026-07-10: today's inbox law assumes a shared
filesystem, and a cloud session, a scheduled routine, or another machine reaches a repo only through git.
The remote arm states the deposit — one new file in inbox/, committed touching inbox/ only with the source
named, then pushed — under a per-repo grant recorded in the host profile like the push grant. A seat with no
grant fails honestly: it names the grant it lacks and hands the owner the one action that supplies it. String
rows on the law's three prose homes plus the spec anchor and its index row.
"""

import unittest

from conftest import open_spec, read_flat


class TestInboxRemoteArm(unittest.TestCase):
    HOMES = (
        "PRODUCT_SPEC.md",
        "inbox/README.md",
        "adopt/ADOPT.md",
    )

    # PRODUCT_SPEC.md's rewritten Requirement 253 restates the law in its own word order
    # ("the repository" / "per-repository grant" / "touching the inbox alone"); the other two
    # homes were not touched by the spec rewrite and keep the original phrasing.
    REMOTE_ARM_NEEDLES = {
        "PRODUCT_SPEC.md": (
            "A remote seat reaches the repository only through git",
            "under a per-repository grant",
            "recorded in the host profile",
        ),
        "inbox/README.md": (
            "A remote seat reaches a repo only through git",
            "under a per-repo grant",
            "recorded in the host profile like the push grant",
        ),
        "adopt/ADOPT.md": (
            "A remote seat reaches a repo only through git",
            "under a per-repo grant",
            "recorded in the host profile like the push grant",
        ),
    }

    def test_remote_arm_in_all_prose_homes(self):
        for home in self.HOMES:
            body = read_flat(home)
            for needle in self.REMOTE_ARM_NEEDLES[home]:
                self.assertIn(needle, body, home)
        # the new spec drops the "like the push grant" prose comparison but keeps the same fact
        # as a co-citation of the push grant's own code on the same criterion
        self.assertIn("[INV-112, INV-82]", read_flat("PRODUCT_SPEC.md"))

    def test_honest_failure_in_all_prose_homes(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("fail honestly", spec, "PRODUCT_SPEC.md")
        self.assertIn("the one action that supplies it", spec, "PRODUCT_SPEC.md")
        for home in ("inbox/README.md", "adopt/ADOPT.md"):
            body = read_flat(home)
            self.assertIn("fails honestly", body, home)
            self.assertIn("hands the owner the one action", body, home)

    def test_deposit_stays_inbox_only(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("committed touching the inbox alone", spec, "PRODUCT_SPEC.md")
        for home in ("inbox/README.md", "adopt/ADOPT.md"):
            body = read_flat(home)
            self.assertIn("committed touching inbox/ only", body, home)

    def test_spec_anchor_and_index(self):
        spec = read_flat("PRODUCT_SPEC.md")
        self.assertIn("[INV-112]", spec)
        # CANDIDATE REAL DEFECT (see repin log): "holds no bar over the deposit" — the old
        # spec's explicit carve-out that the live-session stand-down does not block the inbox
        # deposit push — has no surviving equivalent; the new Requirement 256 states a
        # same-shape but unqualified "never push while another session is known live" with no
        # inbox-deposit exemption stated anywhere. Left red.
        self.assertIn("holds no bar over the deposit", spec)
        self.assertIn("owe the fence and no re-check record", spec)
        with open_spec() as f:
            for line in f:
                if line.startswith("| INV-112 |"):
                    self.assertIn("remote arm", spec)
                    self.assertIn("grant", spec)
                    return
        self.fail("INV-112 index row missing")


if __name__ == "__main__":
    unittest.main()
