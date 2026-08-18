"""The bytes-per-criterion ratchet gate (SPEC INV-264, INV-265).

`guardrails/check-size-ratchet.py` computes a document's bytes-per-criterion and compares it to the
recorded bound in `guardrails/spec-ratchet.json`. The shipped config is UNSEEDED (bound null) — the
gate passes with its stated reason until the migration-end freeze seeds it (INV-264 criterion 3). A
seeded bound the document exceeds reds; a bound at or above it passes. UNARMED (INV-270).
"""
import json
import os
import subprocess
import tempfile
import unittest

from conftest import ROOT, spec_paths

GATE = os.path.join(ROOT, "guardrails", "check-size-ratchet.py")
FX = os.path.join(ROOT, "tests", "fixtures", "specformat")
MINI = os.path.join(FX, "mini_good.md")
REAL_CONFIG = os.path.join(ROOT, "guardrails", "spec-ratchet.json")


def run(*docs, config=None):
    """The gate over one or more document paths: a core and, when its map names them, its parts."""
    env = dict(os.environ)
    if config is not None:
        env["RATCHET_CONFIG"] = config
    return subprocess.run(["python3", GATE, *docs], capture_output=True, text=True, env=env)


class TestSizeRatchetGate(unittest.TestCase):
    def test_gate_and_config_ship(self):
        self.assertTrue(os.path.isfile(GATE))
        self.assertTrue(os.path.isfile(REAL_CONFIG), "the ratchet config does not ship")

    def test_shipped_config_is_seeded_at_migration_end(self):
        # Seeded at the row-445 migration-end freeze (INV-264 c3): the shipped bound now carries the
        # measured bytes-per-criterion of the requirements-format spec, no longer null.
        cfg = json.load(open(REAL_CONFIG, encoding="utf-8"))
        self.assertIsInstance(cfg.get("bytes_per_criterion"), (int, float),
                              "the shipped ratchet bound is unseeded — the migration-end freeze must "
                              "record it (INV-264 c3)")
        self.assertTrue(cfg.get("reason", "").strip(), "the seeded config states no reason")

    def test_unseeded_bound_passes_with_a_stated_reason(self):
        # The unseeded-passes-with-a-reason behaviour still holds, proven against a synthetic
        # unseeded config (the shipped config is now seeded at migration end).
        with tempfile.TemporaryDirectory() as tmp:
            cfg = os.path.join(tmp, "unseeded.json")
            json.dump({"bytes_per_criterion": None, "governs": "x",
                       "reason": "not yet seeded — awaiting the migration-end freeze"}, open(cfg, "w"))
            r = run(MINI, config=cfg)
            self.assertEqual(r.returncode, 0, "the gate red on an unseeded bound:\n%s" % r.stdout)
            self.assertIn("not yet seeded", r.stdout)
            self.assertIn("bytes/criterion", r.stdout)

    def test_bound_above_the_document_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = os.path.join(tmp, "high.json")
            json.dump({"bytes_per_criterion": 10000, "governs": "x"}, open(cfg, "w"))
            r = run(MINI, config=cfg)
            self.assertEqual(r.returncode, 0, "the gate red under a high bound:\n%s" % r.stdout)
            self.assertIn("reach:", r.stdout)

    def test_bound_below_the_document_reds(self):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = os.path.join(tmp, "low.json")
            json.dump({"bytes_per_criterion": 20, "governs": "x"}, open(cfg, "w"))
            r = run(MINI, config=cfg)
            self.assertNotEqual(r.returncode, 0, "passed a document above the bound:\n%s" % r.stdout)
            self.assertIn("above the recorded bound", r.stdout)

    def test_gate_not_wired_into_pre_push_or_ci(self):
        with open(os.path.join(ROOT, "guardrails", "pre-push"), encoding="utf-8") as f:
            self.assertNotIn("check-size-ratchet", f.read())
        with open(os.path.join(ROOT, ".github", "workflows", "gates.yml"), encoding="utf-8") as f:
            self.assertNotIn("check-size-ratchet", f.read())


class TestArmedOnTheRealSpec(unittest.TestCase):
    def test_armed_passes_on_the_real_spec(self):
        # Armed at the row-445 conversion delivery (INV-270): the seeded ratchet gate runs on the
        # live PRODUCT_SPEC.md with the shipped config via the suite (gate b).
        r = run(*spec_paths(), config=REAL_CONFIG)
        self.assertEqual(r.returncode, 0, "the armed ratchet gate red the live spec:\n%s" % r.stdout)


if __name__ == "__main__":
    unittest.main()
