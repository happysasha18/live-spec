"""The deferral-marker gate — the mechanical net for INV-152 (SPEC).

Rule 29 / INV-152 already says: writing a needs-the-human's-word marker requires
naming the human-only fact, and a marker that cannot name it defaults to the seat.
Until now that was discipline only. This gate is its mechanical arm, the same shape
as INV-155's retry-plugin grep: a defer marker in a resume/decision file that names
no reason category (taste / policy / irreversible / device-feel) is a finding, and
the commit is blocked on it. A negated mention ("NOT owner-reserved") is not a marker.

Zero dependencies beyond the stdlib; run from the repo root:
  python3 -m pytest -q tests
"""

import glob
import os
import subprocess
import tempfile
import unittest

from conftest import ROOT

SCRIPT = os.path.join(ROOT, "guardrails", "check-deferral-marker.py")


def run(*paths):
    return subprocess.run(
        ["python3", SCRIPT, *paths], capture_output=True, text=True
    )


def write(tmp, name, body):
    p = os.path.join(tmp, name)
    with open(p, "w") as f:
        f.write(body)
    return p


class TestDeferralMarkerGate(unittest.TestCase):
    def test_bare_marker_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "NEXT_STEPS.md",
                      "# q\n- The two thresholds still stand (HIS to correct): brightness _any, lead_share _lead.\n")
            r = run(p)
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("HIS to correct", r.stdout)

    def test_marker_with_reason_tag_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "NEXT_STEPS.md",
                      "# q\n- Caption weight: C is live, he may raise it to E later (his word) — a taste call.\n")
            r = run(p)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_device_feel_reason_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "NEXT_STEPS.md",
                      "# q\n- Phone FEEL on the pinch: the polaroid drag on a real device. His motion/visual meter.\n")
            r = run(p)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_negated_mention_is_not_a_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "NEXT_STEPS.md",
                      "# q\n- Version bumps are NOT owner-reserved: cut them on green.\n")
            r = run(p)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_line_without_signal_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "NEXT_STEPS.md",
                      "# q\n- Offload the set-piece tables to references/ to bring the file under 500 lines.\n")
            r = run(p)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_reports_path_and_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "DECISION.md",
                      "intro\n\n- Bump 1.5.0 — his word, row 231 reserved.\n")
            r = run(p)
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("DECISION.md:3", r.stdout)

    def test_wrapped_signal_is_flagged(self):
        # F1: a park whose signal straddles the line break must still be caught —
        # the item is folded before scanning, not read a physical line at a time.
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "NEXT_STEPS.md",
                      "# q\n- the door layout decision is held for\n  his word on the arrangement.\n")
            r = run(p)
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("NEXT_STEPS.md:2", r.stdout)

    def test_wrapped_reason_passes(self):
        # F2: a reason on the continuation line of a wrapped bullet covers its signal —
        # the folded item names its fact, so the commit is not blocked.
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "NEXT_STEPS.md",
                      "# q\n- the brightness threshold is still his to correct;\n"
                      "  it is a taste call on the look.\n")
            r = run(p)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_far_negation_passes(self):
        # F6: a negator a few words before the signal still negates it.
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "NEXT_STEPS.md",
                      "# q\n- these items are not currently owner-reserved, ship them.\n")
            r = run(p)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_signal_in_fenced_block_is_skipped(self):
        # R1: a park phrase quoted inside a fenced code block is not a work item.
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "NEXT_STEPS.md",
                      "# q\n```\n- the export path is still his to decide\n```\n")
            r = run(p)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_bare_decide_marker_is_caught(self):
        # ROADMAP 417: the gate reads the GRAMMATICAL SHAPE of a deferral, so an open-decision marker
        # like ⟨DECIDE⟩ — the very marker that walks through a literal signal list — is itself caught
        # when it names no human-only fact. (RED-FIRST against the pre-delta literal SIGNALS list.)
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "NEXT_STEPS.md",
                      "# q\n- ⟨DECIDE⟩ whether the caption sits above or below the frame.\n")
            r = run(p)
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("NEXT_STEPS.md:2", r.stdout)

    def test_decide_marker_parking_a_config_choice_reds(self):
        # ROADMAP 417, adversarial review 2026-07-17: `⟨DECIDE⟩ which sound file the build should bundle`
        # used to PASS because "sound" sits in the reason list — a coincidence, the noun not the
        # feel-call. An open-decision marker is an unresolved decision by definition and must name a CORE
        # human-only fact; a soft craft noun that merely appears does not clear it. (RED-FIRST.)
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "NEXT_STEPS.md",
                      "# q\n- ⟨DECIDE⟩ which sound file the build should bundle.\n")
            r = run(p)
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("NEXT_STEPS.md:2", r.stdout)

    def test_decide_marker_with_a_named_reason_passes(self):
        # a genuinely-justified deferral does not start reding: an open-decision marker that names its
        # human-only fact (a taste call) is the human's to make, and the marker stands.
        with tempfile.TemporaryDirectory() as tmp:
            p = write(tmp, "NEXT_STEPS.md",
                      "# q\n- ⟨DECIDE⟩ caption placement above or below — a taste call on the look.\n")
            r = run(p)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_real_repo_tree_is_clean(self):
        # F4: the CI backstop — the gate runs against this repo's own resume and
        # decision files, so the "reds a commit" promise is wired even where the local
        # pre-commit hook is skipped (the suite runs in CI).
        from conftest import ROOT
        targets = [os.path.join(ROOT, "NEXT_STEPS.md")]
        targets += sorted(glob.glob(os.path.join(ROOT, "docs", "decisions", "*.md")))
        targets = [t for t in targets if os.path.isfile(t)]
        r = run(*targets)
        self.assertEqual(r.returncode, 0,
                         "live-spec's own NEXT_STEPS/decisions carry a parked item with no "
                         "named reason:\n" + r.stdout)


if __name__ == "__main__":
    unittest.main()
