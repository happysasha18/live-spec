"""Narrowness proof for the `promoter-alexander` name_waivers entries (SPEC INV-120, ROADMAP 417).

scripts/shipped-language-allowlist.json carries two `name_waivers` entries scoped to the exact
snippet "promoter-alexander" — one for PLAN.md, one for scripts/state-probe.sh — covering a real
host project's directory name that collides with the owner-name gate's word-bounded match on
"alexander" (the "-alexander" segment of a filesystem path is the one shape the gate cannot tell
apart from a leaked personal name). This repo's own history holds a documented burn from an
over-broad gate exemption accepted on a person's word rather than proved narrow (the `recordless`
class in guardrails/check-prover-record.sh, commit 2718c69, tests/test_deletion_only_push.py), so
a new waiver earns a test proving its scope instead.

Each test builds a temp tree and runs scripts/check-shipped-language.py with `--root` on that tree
and `--allowlist` pointed at the REAL, committed allowlist file, so the proof exercises the actual
waiver data rather than a fixture copy of it.
"""
import json
import os
import subprocess
import tempfile
import unittest

from conftest import ROOT

GATE = os.path.join(ROOT, "scripts", "check-shipped-language.py")
ALLOWLIST = os.path.join(ROOT, "scripts", "shipped-language-allowlist.json")


def run(root):
    return subprocess.run(
        ["python3", GATE, "--root", root, "--allowlist", ALLOWLIST],
        capture_output=True, text=True,
    )


def summary(r):
    """The gate's final JSON summary line, parsed."""
    return json.loads(r.stdout.strip().splitlines()[-1])


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


class TestPromoterAlexanderWaiverScope(unittest.TestCase):
    def test_plan_md_promoter_alexander_line_clears(self):
        """PLAN.md's own host-roster shape — the waived token, standing alone — reports no
        owner-name offence."""
        with tempfile.TemporaryDirectory() as tmp:
            write(os.path.join(tmp, "PLAN.md"),
                  "Host roster: promoter-alexander/ tracked here for provenance.\n")
            r = run(tmp)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertEqual(summary(r)["offences"], 0)
            self.assertNotIn("[owner-name]", r.stdout)

    def test_plan_md_plain_name_line_still_reds(self):
        """The waiver does not blanket-exempt PLAN.md: a line naming the person plainly, with no
        hyphenated token, still reports an owner-name offence."""
        with tempfile.TemporaryDirectory() as tmp:
            write(os.path.join(tmp, "PLAN.md"), "A line naming Alexander directly.\n")
            r = run(tmp)
            self.assertNotEqual(r.returncode, 0, r.stdout)
            self.assertEqual(summary(r)["offences"], 1)
            self.assertIn("PLAN.md:1  [owner-name]", r.stdout)

    def test_plan_md_mixed_lines_report_only_the_plain_name_line(self):
        """With both shapes in the same PLAN.md, exactly the plain-name line is reported and the
        promoter-alexander line is not — the per-line narrowness the waiver claims."""
        with tempfile.TemporaryDirectory() as tmp:
            write(os.path.join(tmp, "PLAN.md"),
                  "Host roster: promoter-alexander/ tracked here for provenance.\n"
                  "A line naming Alexander directly.\n")
            r = run(tmp)
            self.assertNotEqual(r.returncode, 0, r.stdout)
            self.assertEqual(summary(r)["offences"], 1)
            self.assertIn("PLAN.md:2  [owner-name]", r.stdout)
            self.assertNotIn("PLAN.md:1  [owner-name]", r.stdout)

    def test_state_probe_sh_promoter_alexander_line_clears(self):
        """scripts/state-probe.sh's own host-loop shape — the waived token, standing alone —
        reports no owner-name offence."""
        with tempfile.TemporaryDirectory() as tmp:
            write(os.path.join(tmp, "scripts", "state-probe.sh"),
                  "# host loop: promoter-alexander is one tracked directory\n")
            r = run(tmp)
            self.assertEqual(r.returncode, 0, r.stdout)
            self.assertEqual(summary(r)["offences"], 0)
            self.assertNotIn("[owner-name]", r.stdout)

    def test_state_probe_sh_plain_name_line_still_reds(self):
        """The same narrowness holds for scripts/state-probe.sh: a line naming the person plainly
        still reports an owner-name offence."""
        with tempfile.TemporaryDirectory() as tmp:
            write(os.path.join(tmp, "scripts", "state-probe.sh"),
                  "# a comment naming Alexander directly\n")
            r = run(tmp)
            self.assertNotEqual(r.returncode, 0, r.stdout)
            self.assertEqual(summary(r)["offences"], 1)
            self.assertIn("scripts/state-probe.sh:1  [owner-name]", r.stdout)

    def test_unnamed_file_with_the_same_token_still_reds(self):
        """A file the waivers do not name still reports an offence for the same token, proving
        the waiver is scoped per-file rather than exempting the token globally."""
        with tempfile.TemporaryDirectory() as tmp:
            write(os.path.join(tmp, "OTHER.md"),
                  "Host roster: promoter-alexander/ tracked here for provenance.\n")
            r = run(tmp)
            self.assertNotEqual(r.returncode, 0, r.stdout)
            self.assertEqual(summary(r)["offences"], 1)
            self.assertIn("OTHER.md:1  [owner-name]", r.stdout)


if __name__ == "__main__":
    unittest.main()
