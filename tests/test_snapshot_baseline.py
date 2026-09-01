"""Row q-802 (SPEC E-7, `spec/doc-order-generated.md` Requirement 247): the design-sync snapshot's
own baseline advances only at a delivery, and only for the surfaces that delivery declared.

`.live-spec/snapshot/baseline.py` is the one place that ever rewrites a manifest line. This suite
walks a fixture delivery through one baseline advance and proves the asymmetry the requirement
names: a declared surface's baseline moves, an undeclared surface's line is left byte-for-byte
where it stood.

Every fixture manifest here is written under a tempfile.TemporaryDirectory() — never into this
worktree's real (git-tracked) `.live-spec/snapshot/`.
"""

import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAPSHOT_HOME = os.path.join(ROOT, ".live-spec", "snapshot")
sys.path.insert(0, SNAPSHOT_HOME)
import baseline  # noqa: E402


class TestSnapshotBaselineAdvance(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.snapshot_dir = self.tmp.name

        # Seed a manifest as if two prior deliveries had already set baselines: one for
        # 'alpha', one for 'beta' — the fixture delivery below declares only 'alpha'.
        seed_entries = {
            "alpha": {
                "surface": "alpha",
                "baseline": "q-100",
                "hash": baseline.content_hash(b"alpha original"),
                "kind": "inline",
                "pointer": "alpha.snap",
            },
            "beta": {
                "surface": "beta",
                "baseline": "q-101",
                "hash": baseline.content_hash(b"beta original"),
                "kind": "inline",
                "pointer": "beta.snap",
            },
        }
        order = ["alpha", "beta"]
        baseline.write_manifest(self.snapshot_dir, seed_entries, order)
        with open(os.path.join(self.snapshot_dir, "alpha.snap"), "wb") as f:
            f.write(b"alpha original")
        with open(os.path.join(self.snapshot_dir, "beta.snap"), "wb") as f:
            f.write(b"beta original")

        self.beta_line_before = self._beta_manifest_line()

    def _beta_manifest_line(self):
        entries, _order = baseline.read_manifest(self.snapshot_dir)
        return entries["beta"]

    def test_undeclared_surface_baseline_untouched_across_an_advance(self):
        """The fixture delivery declares only 'alpha'. After the advance, 'alpha' carries the
        new delivery id and hash; 'beta' — never declared — keeps its old baseline line exactly,
        and its .snap file is not read or written."""
        beta_snap_path = os.path.join(self.snapshot_dir, "beta.snap")
        beta_mtime_before = os.path.getmtime(beta_snap_path)

        entries = baseline.advance_baseline(
            self.snapshot_dir,
            delivery_id="q-802",
            declared=["alpha"],
            rendered={"alpha": b"alpha rendered by q-802"},
        )

        # alpha's baseline moved: new delivery id, new hash, new content on disk
        self.assertEqual(entries["alpha"]["baseline"], "q-802")
        self.assertEqual(
            entries["alpha"]["hash"], baseline.content_hash(b"alpha rendered by q-802")
        )
        with open(os.path.join(self.snapshot_dir, "alpha.snap"), "rb") as f:
            self.assertEqual(f.read(), b"alpha rendered by q-802")

        # beta was never declared: its manifest line is untouched, field for field
        self.assertEqual(entries["beta"], self.beta_line_before,
                          "an undeclared surface's baseline moved during an advance it was never "
                          "part of")

        # beta's rendered bytes on disk were never touched either
        self.assertEqual(os.path.getmtime(beta_snap_path), beta_mtime_before)
        with open(beta_snap_path, "rb") as f:
            self.assertEqual(f.read(), b"beta original")

        # the manifest file on disk reproduces the same untouched line for beta, read fresh
        manifest_text = open(os.path.join(self.snapshot_dir, baseline.MANIFEST_NAME),
                              encoding="utf-8").read()
        self.assertIn(
            baseline.format_entry("beta", "q-101", self.beta_line_before["hash"],
                                   "inline", "beta.snap"),
            manifest_text,
            "beta's manifest line changed shape even though beta was never declared",
        )

    def test_heavy_surface_keeps_only_its_line_and_hash_under_git(self):
        """A heavy-byte surface's rendered content is held outside the tracked manifest: the
        manifest carries only the line and the hash, the bytes sit under blobs/, and no
        git-tracked .snap file is ever written for it (Requirement 247, criterion 4)."""
        entries = baseline.advance_baseline(
            self.snapshot_dir,
            delivery_id="q-802",
            declared=["gamma"],
            rendered={"gamma": b"a very large rendered surface" * 1000},
            heavy=["gamma"],
        )

        self.assertEqual(entries["gamma"]["kind"], "external")
        self.assertEqual(entries["gamma"]["pointer"], "blobs/gamma.bin")

        blob_path = os.path.join(self.snapshot_dir, "blobs", "gamma.bin")
        self.assertTrue(os.path.exists(blob_path), "heavy surface's bytes were not written outside git")
        with open(blob_path, "rb") as f:
            self.assertEqual(f.read(), b"a very large rendered surface" * 1000)

        # no inline .snap file was written for the heavy surface — only the pointer travels
        self.assertFalse(os.path.exists(os.path.join(self.snapshot_dir, "gamma.snap")))

        # the manifest line itself carries the hash, never the raw bytes
        manifest_text = open(os.path.join(self.snapshot_dir, baseline.MANIFEST_NAME),
                              encoding="utf-8").read()
        self.assertIn("hash: `sha256:%s`" % entries["gamma"]["hash"], manifest_text)
        self.assertNotIn("a very large rendered surface", manifest_text)

        # beta, again never declared, is still untouched
        entries2, _ = baseline.read_manifest(self.snapshot_dir)
        self.assertEqual(entries2["beta"], self.beta_line_before)

    def test_manifest_round_trips_through_the_real_shape(self):
        """The on-disk manifest at .live-spec/snapshot/MANIFEST.md — the real, git-tracked one —
        parses to an empty ledger today (no surface has synced yet; design-sync itself, E-18, is
        still planned) and re-renders to the exact same bytes, proving the shape this row promises
        is what's actually on disk."""
        real_manifest = os.path.join(SNAPSHOT_HOME, baseline.MANIFEST_NAME)
        with open(real_manifest, encoding="utf-8") as f:
            on_disk = f.read()
        entries, order = baseline.parse_manifest(on_disk)
        self.assertEqual(entries, {})
        self.assertEqual(order, [])
        self.assertEqual(baseline.render_manifest(entries, order), on_disk)


if __name__ == "__main__":
    unittest.main()
