"""The convergence locks hold by test, never by attention (row 217, M-214..216).

Three locks the audit found attention-held, now each held by a test:
frozen norms are content-fingerprinted; the register lint's pattern set only
grows; the debt cap only ratchets downward. Changing any guarded value is
LEGAL only as a deliberate, visible edit to its manifest/floor — in the same
commit, named in the landing.
"""
import hashlib
import importlib.util
import json
import os
import unittest

from conftest import ROOT
NORMS_DIR = os.path.join(ROOT, "docs", "norms")
NORMS_MANIFEST = os.path.join(ROOT, "scripts", "norms-manifest.json")
LINT = os.path.join(ROOT, "scripts", "preshow-register-lint.py")
LINT_FLOOR = os.path.join(ROOT, "scripts", "register-lint-floor.json")
DEBT_CAP = os.path.join(ROOT, "scripts", "spec-debt-cap.json")


class TestConvergenceLocks(unittest.TestCase):

    def test_norm_fingerprints(self):
        """M-214: every frozen norm's content matches its recorded fingerprint,
        and every norm file is fingerprinted — a norm never drifts silently."""
        manifest = json.load(open(NORMS_MANIFEST))["sha256"]
        on_disk = sorted(f for f in os.listdir(NORMS_DIR) if not f.startswith("."))
        self.assertEqual(sorted(manifest), on_disk,
                         "docs/norms/ and the manifest disagree on the norm set")
        for name, recorded in manifest.items():
            actual = hashlib.sha256(
                open(os.path.join(NORMS_DIR, name), "rb").read()).hexdigest()
            self.assertEqual(actual, recorded,
                             "a frozen norm drifted from its fingerprint: %s "
                             "(a deliberate change updates the manifest in the "
                             "same commit and names why)" % name)

    def test_register_lint_pattern_floor(self):
        """M-215: the register lint's pattern set only grows — one per caught
        leak; the floor file pins the reached count."""
        floor = json.load(open(LINT_FLOOR))["min_patterns"]
        spec = importlib.util.spec_from_file_location("preshow_lint", LINT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        count = len(mod.PATTERNS)
        self.assertGreaterEqual(
            count, floor,
            "the register lint's pattern set SHRANK below its reached floor "
            "(%d < %d) — patterns are never removed, the set only grows" % (count, floor))

    def test_debt_cap_only_downward(self):
        """M-216: the prose-debt caps ratchet downward only. The zero floors are
        pinned HERE; raising one means editing this test — a deliberate, visible
        act, never a quiet json touch. Both documents' redundancy caps are moving
        ratchets, not zero floors (ARCHITECTURE.md's own zero pin was withdrawn
        2026-08-24, once its Parts map made two honest structural echo classes
        possible that a monolithic file never had — see scripts/spec-debt-cap.json,
        "_reason_redundancy_ARCHITECTURE"), so a literal pin here goes stale every
        time either ratchet legitimately moves (PRODUCT_SPEC.md's did, 121 -> 119
        -> 116, and this test's old 121 pin already missed one such move). Both
        are enforced live instead, read straight from the json's own recorded
        cap, in test_live_spec_sits_at_the_clean_floor below — the json's own
        history comments ("_reason_redundancy_PRODUCT_SPEC",
        "_reason_redundancy_ARCHITECTURE") are the deliberate, visible record of
        each move."""
        cap = json.load(open(DEBT_CAP))
        self.assertLessEqual(cap["max_waivers"], 0,
                             "max_waivers was raised above the reached ratchet value")
        self.assertLessEqual(cap["max_style_errors"], 0,
                             "max_style_errors was raised above the reached ratchet value")

    def test_live_spec_sits_at_the_clean_floor(self):
        """The 2.0 ratchet's live half (M-217): the real PRODUCT_SPEC.md and ARCHITECTURE.md each sit AT
        or under their recorded redundancy floor, and the style gate reports zero errors on both — so a
        future edit that reintroduces a shout, a scissors, a second person, or a fresh duplicated sentence
        reddens HERE instead of fading in silently. Both documents are read core+parts (the tool reads
        assembled text since 2026-08-24; see scripts/spec-debt-cap.json's two "_reason_redundancy_..."
        comments for how each floor was reached). A deliberate, reviewed regression would have to edit
        the json floor and this test's understanding of it, in the same commit, named in the landing."""
        import subprocess

        def gate_json(script, doc, *extra):
            r = subprocess.run(
                ["python3", os.path.join(ROOT, "scripts", script), *extra,
                 os.path.join(ROOT, doc)],
                capture_output=True, text=True)
            for line in reversed(r.stdout.strip().splitlines()):
                line = line.strip()
                if line.startswith("{") and line.endswith("}"):
                    return json.loads(line)
            raise AssertionError("no JSON summary from %s:\n%s" % (script, r.stdout))

        cap = json.load(open(DEBT_CAP))
        for doc in ("PRODUCT_SPEC.md", "ARCHITECTURE.md"):
            style = gate_json("spec-style-lint.py", doc, "--gate")
            self.assertEqual(
                style["errors"], 0,
                "%s re-grew a register defect: %d style errors (floor 0)" % (doc, style["errors"]))
            self.assertEqual(style["stale"], 0,
                             "a stale waiver lingers in scripts/spec-waivers.json — remove it")
            red = gate_json("spec-redundancy-precheck.py", doc)
            doc_floor = cap["max_redundancy_open"][doc]
            self.assertLessEqual(
                red["open"], doc_floor,
                "%s re-grew redundancy: %d open pairs (floor %d)"
                % (doc, red["open"], doc_floor))


if __name__ == "__main__":
    unittest.main()
