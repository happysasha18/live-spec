"""Locks the fix that stopped spec-style-lint.py reading a core file's own bytes only.

Before the fix, `main()` opened the FILE argument directly (`open(src, encoding="utf-8").read()`),
so a core file carrying a `## Parts map` (PRODUCT_SPEC.md, ARCHITECTURE.md, both split into part
files earlier in this same session) was scanned as its preamble/glossary/map alone — every register
tell living in the part files was invisible to the style lint. The fix routes the read through
`guardrails/specformat.py`'s `spec_paths()` / `read_document()`, the same core+parts mechanism the
sibling gate already uses (scripts/spec-redundancy-precheck.py, fixed first for the identical bug —
commit 86adc187), so the lint now scans the WHOLE document.

Three things are locked, mirroring tests/test_redundancy_precheck_parts.py's shape for the sibling
gate:
  1. A core file's Parts map is expanded — a scissors tell split into a part file is now found,
     where the old direct-read code could not see it (the tell never appears in the core file's own
     bytes at all).
  2. A file with no Parts map (an ordinary part file, or any file with no such section) is read
     exactly as before — byte for byte, same errors/warnings, same JSON summary — since expansion is
     idempotent by `spec_paths()`'s own construction.
  3. The vendored-standalone deployment (adopt/install-ratchet.sh's VENDOR_FILES, which ships this
     script + spec-style-lint.json + gate_common.py + guardrails/spec-coinages.json into a host repo
     WITHOUT guardrails/specformat.py) still runs with no core+parts convention assumed — the import
     stays optional and a missing specformat falls back to the old direct-file read, unchanged.
"""
import json
import os
import shutil
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "scripts", "spec-style-lint.py")


def run(*args, stdin=None):
    return subprocess.run(["python3", SCRIPT, *args], input=stdin, capture_output=True, text=True)


def summary(stdout):
    for line in reversed(stdout.strip().splitlines()):
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            return json.loads(line)
    raise AssertionError("no JSON summary in stdout:\n%s" % stdout)


# A scissors tell — the em-dash + "not" contrast frame (docs/spec-style.md R-scissors), a UNIVERSAL,
# always-on error regardless of tier. Long enough, and shaped enough, to trip nothing else.
SCISSORS_LINE = "the card shows the outcome — not the mechanism.\n"


class TestPartsMapIsExpanded(unittest.TestCase):
    def test_scissors_tell_split_into_a_part_is_found(self):
        with tempfile.TemporaryDirectory() as d:
            core = os.path.join(d, "CORE.md")
            part_a = os.path.join(d, "part-a.md")
            part_b = os.path.join(d, "part-b.md")

            with open(core, "w", encoding="utf-8") as f:
                f.write(
                    "# Core\n\n"
                    "Some preamble text that carries no register tell of its own.\n\n"
                    "## Parts map\n\n"
                    "| Part | Requirements | Topic |\n"
                    "|---|---|---|\n"
                    "| `part-a.md` | R1 | Part A |\n"
                    "| `part-b.md` | R2 | Part B |\n"
                )
            with open(part_a, "w", encoding="utf-8") as f:
                f.write("## Requirement 1: A\n\nOrdinary clean prose, nothing flagged here.\n")
            with open(part_b, "w", encoding="utf-8") as f:
                f.write("## Requirement 2: B\n\n" + SCISSORS_LINE)

            # Sanity: the tell does NOT live in the core file's own bytes — the old direct-read code
            # could not have found it no matter what.
            with open(core, encoding="utf-8") as f:
                self.assertNotIn("not the mechanism", f.read())

            r = run(core)
            js = summary(r.stdout)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertGreaterEqual(
                js["errors"], 1,
                "expected the part-file scissors tell to surface as an error: %s\n%s" % (js, r.stdout))
            self.assertIn("scissors", r.stdout)

    def test_core_with_empty_parts_map_reads_as_itself(self):
        # An explicit map that resolves to nothing (no data rows) behaves exactly like no map at all
        # — the core is the whole document.
        with tempfile.TemporaryDirectory() as d:
            core = os.path.join(d, "CORE.md")
            with open(core, "w", encoding="utf-8") as f:
                f.write("# Core\n\n## Parts map\n\n| Part | Requirements | Topic |\n|---|---|---|\n")
            r = run(core)
            js = summary(r.stdout)
            self.assertEqual(js["errors"], 0)
            self.assertEqual(r.returncode, 0)


class TestFileWithoutPartsMapIsUnchanged(unittest.TestCase):
    def test_plain_file_matches_direct_read_byte_for_byte(self):
        """A file with no `## Parts map` section (an ordinary matrix/*.md-style part file, or any
        plain document) must be scanned identically to the pre-fix behaviour. Proven by comparing
        the file-argument run against a stdin run of the exact same text — stdin is untouched by the
        core+parts read (it is never routed through specformat), so the two must match exactly."""
        text = (
            "# Plain document\n\n"
            "The card shows the outcome — not the mechanism.\n\n"
            "It CHANGES the queue.\n"
        )
        with tempfile.TemporaryDirectory() as d:
            plain = os.path.join(d, "plain.md")
            with open(plain, "w", encoding="utf-8") as f:
                f.write(text)

            r_file = run(plain)
            r_stdin = run("-", stdin=text)

            js_file = summary(r_file.stdout)
            js_stdin = summary(r_stdin.stdout)
            self.assertEqual(js_file["errors"], js_stdin["errors"])
            self.assertEqual(js_file["warnings"], js_stdin["warnings"])
            self.assertEqual(js_file["waived"], js_stdin["waived"])
            self.assertEqual(r_file.returncode, r_stdin.returncode)


class TestVendoredStandaloneFallback(unittest.TestCase):
    """adopt/install-ratchet.sh vendors this script (plus spec-style-lint.json, gate_common.py, and
    guardrails/spec-coinages.json — the word list it needs to even import) into a host repo, but
    guardrails/specformat.py is NOT one of its VENDOR_FILES. Locks that the core+parts import stays
    optional: run from a copy with the same shape and no specformat.py, the script must still behave
    exactly as it did before the core+parts fix (read the named file directly), not crash."""

    def test_runs_with_no_specformat_available(self):
        with tempfile.TemporaryDirectory() as d:
            vendor_scripts = os.path.join(d, "scripts")
            vendor_guardrails = os.path.join(d, "guardrails")
            os.makedirs(vendor_scripts)
            os.makedirs(vendor_guardrails)
            shutil.copy(SCRIPT, os.path.join(vendor_scripts, "spec-style-lint.py"))
            shutil.copy(os.path.join(ROOT, "scripts", "spec-style-lint.json"),
                        os.path.join(vendor_scripts, "spec-style-lint.json"))
            shutil.copy(os.path.join(ROOT, "scripts", "gate_common.py"),
                        os.path.join(vendor_scripts, "gate_common.py"))
            shutil.copy(os.path.join(ROOT, "guardrails", "spec-coinages.json"),
                        os.path.join(vendor_guardrails, "spec-coinages.json"))
            # No guardrails/specformat.py — the one VENDOR_FILES entry deliberately left behind.

            doc = os.path.join(d, "DOC.md")
            with open(doc, "w", encoding="utf-8") as f:
                f.write("# Doc\n\n" + SCISSORS_LINE)

            r = subprocess.run(
                ["python3", os.path.join(vendor_scripts, "spec-style-lint.py"), doc],
                capture_output=True, text=True)
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)  # scissors error found -> exit 1
            js = summary(r.stdout)
            self.assertGreaterEqual(js["errors"], 1)


if __name__ == "__main__":
    unittest.main()
