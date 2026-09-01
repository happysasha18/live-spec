"""The convergence locks hold by test, never by attention (row 217, M-214..216).

Three locks the audit found attention-held, now each held by a test:
frozen norms are content-fingerprinted; the register lint's pattern set only
grows; the debt cap sits at zero for style errors and stale waivers. Changing
any guarded value is LEGAL only as a deliberate, visible edit to its
manifest/floor — in the same commit, named in the landing.

Each floor here names one specific thing that must not be present. None is a
count carried over from what the document last measured: the one lock of that
shape, the per-document redundancy-pair ceiling, was cut 2026-09-02.
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
        """M-216: the prose-debt caps ratchet downward only. Both are zero floors,
        pinned HERE; raising one means editing this test — a deliberate, visible
        act, never a quiet json touch. Each names one specific thing a document
        must not carry: a style error the lint can point at by line, and a waiver
        standing over a finding that is gone. Neither is a bound seeded from what
        the document happened to measure before.

        The redundancy cap that used to sit beside them was exactly such a bound
        — a per-document count of fuzzy-matched near-duplicate pairs, seeded at
        whatever the last measurement read (PRODUCT_SPEC.md's ran 121 -> 119 ->
        116, ARCHITECTURE.md's 0 -> 15). It was cut 2026-09-02 with the rest of
        the invented-ceiling family, on the owner's word. The reading itself
        stays: scripts/spec-redundancy-precheck.py still prints its candidate
        pairs for a person to judge, and holds nothing against them."""
        cap = json.load(open(DEBT_CAP))
        self.assertLessEqual(cap["max_waivers"], 0,
                             "max_waivers was raised above the reached ratchet value")
        self.assertLessEqual(cap["max_style_errors"], 0,
                             "max_style_errors was raised above the reached ratchet value")

    def test_live_spec_sits_at_the_clean_floor(self):
        """The 2.0 ratchet's live half (M-217): the style gate reports zero errors on the real
        PRODUCT_SPEC.md and ARCHITECTURE.md, and no waiver stands over a finding that is gone — so a
        future edit that reintroduces a shout, a scissors, or a second person reddens HERE instead of
        fading in silently. Each failure names the line and the construction; the floor is zero
        because the rule is "never write this", not "do not write more of it than last time".

        The redundancy half of this assertion — each document at or under a recorded count of
        near-duplicate pairs — was cut 2026-09-02: that count was seeded from the document's own past
        state, so a delivery that genuinely improved the document could still red on it. The reading
        remains available by hand (`python3 scripts/spec-redundancy-precheck.py PRODUCT_SPEC.md`) and
        gates nothing."""
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

        for doc in ("PRODUCT_SPEC.md", "ARCHITECTURE.md"):
            style = gate_json("spec-style-lint.py", doc, "--gate")
            self.assertEqual(
                style["errors"], 0,
                "%s re-grew a register defect: %d style errors (floor 0)" % (doc, style["errors"]))
            self.assertEqual(style["stale"], 0,
                             "a stale waiver lingers in scripts/spec-waivers.json — remove it")


if __name__ == "__main__":
    unittest.main()
