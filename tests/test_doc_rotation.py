"""Document rotation — the pack's append-only working docs are split and rotated, and nothing
rotated is lost (SPEC INV-209, ROADMAP rows 390 + 392, the growth/grooming family).

ROADMAP.md, JOURNAL.md, PRODUCT_SPEC.md, and TEST_MATRIX.md grow with every landing until a guard's
scan and a grep run slow (the owner's word, 2026-07-17 ~18:25). So a fully-closed portion of a growable
document rotates out of the live file into a dated archive with a manifest line (base rule 10), the live
file keeping only live material and the archive keeping everything, grepable, so a rotated row stays
findable by its number.

Two machines hold the invariant:
  - scripts/rotate-doc.py         — the mechanism: moves closed rows to a dated archive, leaves the
                                    manifest line in the live file.
  - guardrails/check-doc-rotation.py (gate t) — the net: reds a rotation that DROPS content (a
                                    manifested row found in neither the live file nor its archive) and a
                                    rotation with NO manifest (a rotated-* archive no manifest points to).

This file is red-first: run it against the pre-delta tree and the gate/mechanism are absent, the
spec/index/architecture/matrix carry no INV-209, and the push chain is unwired.
"""
import os
import re
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, "guardrails", "check-doc-rotation.py")
ROTATE = os.path.join(ROOT, "scripts", "rotate-doc.py")


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def run_gate(base, docs, extra=None):
    """Run the gate over a fixture base dir; return (exit_code, combined_output)."""
    cmd = [sys.executable, GATE, "--base", base]
    for d in docs:
        cmd += ["--doc", d]
    cmd += ["--archive-glob", "rotated-*.md"]
    if extra:
        cmd += extra
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


# ---- fixtures ---------------------------------------------------------------

MANIFEST = (
    "<!-- rotated-manifest -->\n"
    "Rotated closed rows (base rule 10 — nothing lost; the archive keeps everything):\n"
    "- rows 14, 27 → rotated-ROADMAP-2026-07-18.md\n"
    "<!-- /rotated-manifest -->\n"
)


def _live_doc(manifest):
    return (
        "# live-spec Roadmap (dated version: 2026-07-18)\n\n"
        "The wish queue.\n\n"
        + manifest +
        "\n| # | Wish (plain words) | Class | Status | Decision / acceptance |\n"
        "|---|---|---|---|---|\n"
        "| 42 | a live open wish | surface | queued 2026-07-18 | Done when: x |\n"
    )


def _archive(rows):
    head = "> ARCHIVED 2026-07-18 by scripts/rotate-doc.py from ROADMAP.md — nothing lost (base rule 10).\n\n"
    body = "".join(
        "| %d | closed wish %d | small | **landed 2026-07-05** | Done when: met |\n" % (n, n)
        for n in rows
    )
    return head + "| # | Wish | Class | Status | Decision |\n|---|---|---|---|---|\n" + body


def _write(base, name, text):
    with open(os.path.join(base, name), "w", encoding="utf-8") as f:
        f.write(text)


class TestRotationGate(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp(prefix="rotation-fixture-")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_gate_ships(self):
        self.assertTrue(os.path.isfile(GATE), "the rotation gate guardrails/check-doc-rotation.py is missing")

    def test_mechanism_ships(self):
        self.assertTrue(os.path.isfile(ROTATE), "the rotation mechanism scripts/rotate-doc.py is missing")

    def test_gate_reds_a_rotation_that_loses_a_row(self):
        # the manifest claims rows 14 and 27 rotated, but the archive holds only 14 — row 27 is
        # present in neither the live file nor the archive: the nothing-lost violation.
        _write(self.tmp, "ROADMAP.md", _live_doc(MANIFEST))
        _write(self.tmp, "rotated-ROADMAP-2026-07-18.md", _archive([14]))
        code, out = run_gate(self.tmp, ["ROADMAP.md"])
        self.assertNotEqual(code, 0, "a rotation that drops row 27 must red")
        self.assertIn("27", out)

    def test_gate_reds_a_rotation_with_no_manifest(self):
        # a rotated-* archive exists but no manifest line in any live doc points to it: the
        # base-rule-10 violation (a superseded portion moved with no manifest line).
        _write(self.tmp, "ROADMAP.md", _live_doc(""))  # no manifest block at all
        _write(self.tmp, "rotated-ROADMAP-2026-07-18.md", _archive([14, 27]))
        code, out = run_gate(self.tmp, ["ROADMAP.md"])
        self.assertNotEqual(code, 0, "an orphan archive with no manifest line must red")
        self.assertIn("rotated-ROADMAP-2026-07-18.md", out)

    def test_gate_reds_a_row_that_is_both_live_and_rotated(self):
        # row 14 is declared rotated yet still present as a live table row — ambiguous, findable
        # twice, the canonical copy unclear.
        live = _live_doc(MANIFEST) + "| 14 | still here | small | **landed 2026-07-05** | Done: met |\n"
        _write(self.tmp, "ROADMAP.md", live)
        _write(self.tmp, "rotated-ROADMAP-2026-07-18.md", _archive([14, 27]))
        code, out = run_gate(self.tmp, ["ROADMAP.md"])
        self.assertNotEqual(code, 0, "a row both live and rotated must red")
        self.assertIn("14", out)

    def test_gate_passes_a_clean_rotation(self):
        # the live file shrank, the archive holds every rotated row, the manifest names them, and no
        # rotated row is still live: a clean rotation passes.
        _write(self.tmp, "ROADMAP.md", _live_doc(MANIFEST))
        _write(self.tmp, "rotated-ROADMAP-2026-07-18.md", _archive([14, 27]))
        code, out = run_gate(self.tmp, ["ROADMAP.md"])
        self.assertEqual(code, 0, "a clean rotation must pass:\n" + out)

    def test_rotated_row_is_findable_by_number_in_the_archive(self):
        # findability: a reader who greps the archive for the row's own `| n |` line finds it.
        _write(self.tmp, "rotated-ROADMAP-2026-07-18.md", _archive([14, 27]))
        arch = open(os.path.join(self.tmp, "rotated-ROADMAP-2026-07-18.md"), encoding="utf-8").read()
        self.assertRegex(arch, r"(?m)^\| 27 \|", "a rotated row must keep its `| n |` line so a grep finds it")

    def test_gate_passes_the_real_tree(self):
        # the repo's own ROADMAP.md after the first rotation must be clean under the gate.
        p = subprocess.run([sys.executable, GATE], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(p.returncode, 0, "the real tree fails the rotation gate:\n" + p.stdout + p.stderr)


class TestMechanism(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp(prefix="rotation-mech-")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_rotate_moves_closed_rows_and_leaves_a_manifest(self):
        live = (
            "# live-spec Roadmap (dated version: 2026-07-18)\n\n"
            "The wish queue.\n\n"
            "| # | Wish (plain words) | Class | Status | Decision / acceptance |\n"
            "|---|---|---|---|---|\n"
            "| 14 | closed wish | small | **landed 2026-07-05** | Done when: met |\n"
            "| 42 | open wish | surface | queued 2026-07-18 | Done when: x |\n"
        )
        _write(self.tmp, "ROADMAP.md", live)
        p = subprocess.run(
            [sys.executable, ROTATE, "--doc", "ROADMAP.md", "--rows", "14",
             "--base", self.tmp, "--date", "2026-07-18"],
            capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, "rotate-doc.py failed:\n" + p.stdout + p.stderr)
        new_live = open(os.path.join(self.tmp, "ROADMAP.md"), encoding="utf-8").read()
        self.assertNotRegex(new_live, r"(?m)^\| 14 \|", "the rotated row is still a live table row")
        self.assertRegex(new_live, r"(?m)^\| 42 \|", "the live open row was dropped")
        self.assertIn("rotated-manifest", new_live, "no manifest block left in the live file")
        self.assertIn("14", new_live, "the manifest does not name the rotated row number")
        arch = os.path.join(self.tmp, "docs", "queue-archive", "rotated-ROADMAP-2026-07-18.md")
        self.assertTrue(os.path.isfile(arch), "no archive file written")
        self.assertRegex(open(arch, encoding="utf-8").read(), r"(?m)^\| 14 \|", "rotated row not in the archive")

    def test_rotate_halts_on_a_row_that_is_not_closed(self):
        # safety: a row still open (queued / in-work / deferred / open field leg) is never rotated.
        live = (
            "# live-spec Roadmap (dated version: 2026-07-18)\n\n"
            "| # | Wish (plain words) | Class | Status | Decision / acceptance |\n"
            "|---|---|---|---|---|\n"
            "| 42 | open wish | surface | queued 2026-07-18 | Done when: x |\n"
        )
        _write(self.tmp, "ROADMAP.md", live)
        p = subprocess.run(
            [sys.executable, ROTATE, "--doc", "ROADMAP.md", "--rows", "42",
             "--base", self.tmp, "--date", "2026-07-18"],
            capture_output=True, text=True)
        self.assertNotEqual(p.returncode, 0, "rotating a still-open row must halt, not proceed")

    def test_rotate_output_survives_the_gate(self):
        # the mechanism and the net agree: what rotate-doc.py produces passes check-doc-rotation.py.
        live = (
            "# live-spec Roadmap (dated version: 2026-07-18)\n\n"
            "| # | Wish (plain words) | Class | Status | Decision / acceptance |\n"
            "|---|---|---|---|---|\n"
            "| 14 | closed wish | small | **landed 2026-07-05** | Done when: met |\n"
            "| 27 | closed wish two | small | **landed 2026-07-05** | picked X |\n"
            "| 42 | open wish | surface | queued 2026-07-18 | Done when: x |\n"
        )
        _write(self.tmp, "ROADMAP.md", live)
        subprocess.run(
            [sys.executable, ROTATE, "--doc", "ROADMAP.md", "--rows", "14,27",
             "--base", self.tmp, "--date", "2026-07-18"],
            capture_output=True, text=True, check=True)
        code, out = run_gate(self.tmp, ["ROADMAP.md"],
                             extra=["--archive-glob", "docs/queue-archive/rotated-*.md"])
        self.assertEqual(code, 0, "rotate-doc.py output failed the gate:\n" + out)


MONTH_MANIFEST = (
    "<!-- rotated-manifest -->\n"
    "Rotated closed rows (base rule 10 — nothing lost; the archive keeps everything):\n"
    "- rows 480 → docs/queue-archive/rotated-ROADMAP-2026-07.md\n"
    "<!-- /rotated-manifest -->\n"
)
MONTH_MANIFEST_TWO = MONTH_MANIFEST.replace("- rows 480 →", "- rows 480, 483 →")


def _month_archive(rows):
    head = ("# Rotated ROADMAP rows — 2026-07\n\n"
            "> ARCHIVED 2026-07 by scripts/rotate-doc.py from ROADMAP.md at the closing commit — nothing lost.\n\n")
    body = "".join(
        "| %d | closed wish %d | small | *landed 2026-07-23* | Done: met |\n" % (n, n) for n in rows)
    return head + "| # | Wish (plain words) | Class | Status | Decision / acceptance |\n|---|---|---|---|---|\n" + body


class TestMonthlyClosingCommitGate(unittest.TestCase):
    """Piece 2 (SPEC INV-276): the doc-rotation gate accepts the monthly-growing manifest shape — one
    line per month archive whose row-set grows across commits, a monthly-named archive as legal as the
    day-named legacy ones — and the three reds stay live on it."""

    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp(prefix="rotation-month-")
        os.makedirs(os.path.join(self.tmp, "docs", "queue-archive"))

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run(self, docs=("ROADMAP.md",)):
        return run_gate(self.tmp, list(docs),
                        extra=["--archive-glob", "docs/queue-archive/rotated-*.md"])

    def test_a_row_moved_into_a_month_file_passes(self):
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", _month_archive([480]))
        code, out = self._run()
        self.assertEqual(code, 0, "a clean monthly close must pass:\n" + out)

    def test_a_second_row_appended_with_the_line_grown_passes(self):
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST_TWO))
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", _month_archive([480, 483]))
        code, out = self._run()
        self.assertEqual(code, 0, "a grown month manifest line must pass:\n" + out)

    def test_a_moved_row_missing_from_the_archive_reds(self):
        # RED-PROOF: manifest names 480 and 483 but the month archive holds only 480.
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST_TWO))
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", _month_archive([480]))
        code, out = self._run()
        self.assertNotEqual(code, 0, "a row lost from the month archive must red")
        self.assertIn("483", out)

    def test_a_row_in_both_body_and_archive_reds(self):
        # RED-PROOF: row 480 is declared moved yet still stands as a live body row — ambiguous.
        live = _live_doc(MONTH_MANIFEST) + "| 480 | still here | small | *queued 2026-07-23* | Done: x |\n"
        _write(self.tmp, "ROADMAP.md", live)
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", _month_archive([480]))
        code, out = self._run()
        self.assertNotEqual(code, 0, "a row both live and archived must red")
        self.assertIn("480", out)

    def test_an_orphan_month_archive_reds(self):
        # RED-PROOF: a month archive with no manifest line pointing to it (base-rule-10 violation).
        _write(self.tmp, "ROADMAP.md", _live_doc(""))
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", _month_archive([480]))
        code, out = self._run()
        self.assertNotEqual(code, 0, "an orphan month archive must red")
        self.assertIn("rotated-ROADMAP-2026-07.md", out)


class TestNonTerminalArchiveRow(unittest.TestCase):
    """Arm (d) (docs/prover/2026-07-27-push-gate-addendum.md finding A4): a row inside an archive
    whose Status cell carries none of the terminal words (landed / decided / declined / superseded) reds — a
    row like this is reachable from no live answer, no cap count and no gate. Red-first proof: HEAD's
    docs/queue-archive/rotated-ROADMAP-2026-07.md row 482 carried `*queued* 2026-07-23` with no
    terminal word; this fixture is the permanent, minimal shape of that same red."""

    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp(prefix="rotation-nonterminal-")
        os.makedirs(os.path.join(self.tmp, "docs", "queue-archive"))

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run(self):
        return run_gate(self.tmp, ["ROADMAP.md"],
                        extra=["--archive-glob", "docs/queue-archive/rotated-*.md"])

    def test_a_queued_row_in_the_archive_reds(self):
        # RED-PROOF: the row-482 shape — a bug row moved to the archive still reading *queued*, no
        # terminal word standing anywhere in its Status cell.
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        archive = (
            "# Rotated ROADMAP rows — 2026-07\n\n"
            "> ARCHIVED 2026-07 — a row's terminal exit is certified by the landed, declined, or "
            "superseded word standing somewhere in the cell.\n\n"
            "| # | Wish (plain words) | Class | Status | Decision / acceptance |\n|---|---|---|---|---|\n"
            "| 480 | mid-turn chat lines reach the human ungated | bug | *queued* 2026-07-23 | Done "
            "when: x |\n"
        )
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", archive)
        code, out = self._run()
        self.assertNotEqual(code, 0, "a non-terminal row sitting in the archive must red:\n" + out)
        self.assertIn("480", out)
        self.assertIn("live queue body", out)

    def test_terminal_word_bolded_and_dated_passes(self):
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        archive = _month_archive([480]).replace(
            "*landed 2026-07-23*", "**LANDED 2026-07-07 ~11:47**")
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", archive)
        code, out = self._run()
        self.assertEqual(code, 0, "a bolded, dated terminal word must pass:\n" + out)

    def test_terminal_word_declined_passes(self):
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        archive = _month_archive([480]).replace("*landed 2026-07-23*", "declined 2026-07-23")
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", archive)
        code, out = self._run()
        self.assertEqual(code, 0, "a declined row must pass:\n" + out)

    def test_terminal_word_decided_passes(self):
        # A row that exists to settle a question exits as decided, the fourth word of the vocabulary
        # docs/roadmap-format.md states in one home; the pre-format archives carry it on their
        # decision rows.
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        archive = _month_archive([480]).replace("*landed 2026-07-23*", "**decided 2026-07-05**")
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", archive)
        code, out = self._run()
        self.assertEqual(code, 0, "a decided row must pass:\n" + out)

    def test_terminal_word_superseded_passes(self):
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        archive = _month_archive([480]).replace("*landed 2026-07-23*", "superseded 2026-07-23")
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", archive)
        code, out = self._run()
        self.assertEqual(code, 0, "a superseded row must pass:\n" + out)

    def test_stale_leading_narration_word_still_passes_when_terminal_word_stands_later(self):
        # the archive preamble's own caveat: the leading word can be a stale narration opener (queued
        # or in-work) on a row that later landed, so the check reads the whole cell, never the leading
        # word alone.
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        archive = _month_archive([480]).replace(
            "*landed 2026-07-23*",
            "*queued* 2026-07-20, then **landed 2026-07-23**")
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", archive)
        code, out = self._run()
        self.assertEqual(code, 0, "a terminal word standing anywhere in the cell must pass:\n" + out)


class TestClosingCommitMechanism(unittest.TestCase):
    """Piece 1: scripts/rotate-doc.py --close-row moves ONE row into the month archive, grows the
    month's single manifest line, and its output survives the gate."""

    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp(prefix="rotation-close-")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    LIVE = (
        "# live-spec Roadmap (dated version: 2026-07-23)\n\n"
        "The wish queue.\n\n"
        "| # | Wish (plain words) | Class | Status | Decision / acceptance |\n"
        "|---|---|---|---|---|\n"
        "| 480 | first closed wish | surface | *landed 2026-07-23* | Done: met |\n"
        "| 481 | a live open wish | small | *queued 2026-07-23* | Done: x |\n"
        "| 483 | second closed wish | small | *landed 2026-07-23* | Done: met |\n"
    )

    def _close(self, rownum):
        return subprocess.run(
            [sys.executable, ROTATE, "--doc", "ROADMAP.md", "--close-row", str(rownum),
             "--month", "2026-07", "--base", self.tmp], capture_output=True, text=True)

    def test_close_row_moves_one_row_and_grows_one_manifest_line(self):
        _write(self.tmp, "ROADMAP.md", self.LIVE)
        p = self._close(480)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        p = self._close(483)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        live = open(os.path.join(self.tmp, "ROADMAP.md"), encoding="utf-8").read()
        self.assertNotRegex(live, r"(?m)^\| 480 \|", "row 480 still a live body row")
        self.assertNotRegex(live, r"(?m)^\| 483 \|", "row 483 still a live body row")
        self.assertRegex(live, r"(?m)^\| 481 \|", "the live open row 481 was dropped")
        # ONE manifest line for the month archive, its row list grown to both rows
        month_lines = [l for l in live.splitlines()
                       if "rotated-ROADMAP-2026-07.md" in l and l.strip().startswith("- rows")]
        self.assertEqual(len(month_lines), 1, "the month archive must own exactly one manifest line: %s" % month_lines)
        self.assertIn("480", month_lines[0])
        self.assertIn("483", month_lines[0])
        arch = open(os.path.join(self.tmp, "docs", "queue-archive", "rotated-ROADMAP-2026-07.md"),
                    encoding="utf-8").read()
        self.assertRegex(arch, r"(?m)^\| 480 \|")
        self.assertRegex(arch, r"(?m)^\| 483 \|")

    def test_close_row_halts_on_an_absent_row(self):
        _write(self.tmp, "ROADMAP.md", self.LIVE)
        p = self._close(999)
        self.assertNotEqual(p.returncode, 0, "closing a row the body does not hold must halt")

    def test_close_row_output_survives_the_gate(self):
        _write(self.tmp, "ROADMAP.md", self.LIVE)
        self._close(480)
        self._close(483)
        code, out = run_gate(self.tmp, ["ROADMAP.md"],
                             extra=["--archive-glob", "docs/queue-archive/rotated-*.md"])
        self.assertEqual(code, 0, "rotate-doc.py --close-row output failed the gate:\n" + out)


# --- wired into the push chain, both nets ---

def test_gate_wired_into_pre_push():
    assert "check-doc-rotation.py" in read("guardrails/pre-push"), \
        "pre-push does not wire the rotation gate (gate t)"


def test_gate_mirrored_in_ci():
    assert "check-doc-rotation.py" in read(".github/workflows/gates.yml"), \
        "the CI mirror does not run the rotation gate"


# --- traceability across the four documents ---

def test_spec_states_the_law():
    # PRODUCT_SPEC.md states this law in plain behaviour, not by script filename — the literal
    # rotate-doc.py / check-doc-rotation.py names moved to ARCHITECTURE.md's ownership row (see
    # test_architecture_owns_the_invariant), the rewrite's document-boundary convention (spec =
    # behaviour, architecture = implementation file). Re-pinned to the plain-language equivalents.
    spec = read("PRODUCT_SPEC.md")
    assert "[INV-209]" in spec
    assert "move the closed rows into a dated archive" in spec
    assert "nothing-lost violation" in spec


def test_formal_index_row():
    assert "| INV-209 |" in read("PRODUCT_SPEC.md")


def test_architecture_owns_the_invariant():
    arch = read("ARCHITECTURE.md")
    assert "INV-209" in arch
    assert "check-doc-rotation.py" in arch


def test_matrix_row_covers_the_law():
    matrix = read("TEST_MATRIX.md")
    assert "M-390" in matrix
    assert "INV-209" in matrix


if __name__ == "__main__":
    unittest.main()


class TestStatusColumnReadFromHeader(unittest.TestCase):
    """The Status cell is located by the archive table's own header (the record's S8), so an archive
    whose columns sit in another order is still read at the right cell."""

    def setUp(self):
        import tempfile
        self.tmp = tempfile.mkdtemp(prefix="rotation-header-")
        os.makedirs(os.path.join(self.tmp, "docs", "queue-archive"))

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run(self):
        return run_gate(self.tmp, ["ROADMAP.md"],
                        extra=["--archive-glob", "docs/queue-archive/rotated-*.md"])

    ARCHIVE_HEAD = ("# Rotated ROADMAP rows — 2026-07\n\n> ARCHIVED 2026-07 — terminal words: landed, "
                    "decided, declined, superseded.\n\n")

    def test_a_reordered_header_still_finds_the_status_cell(self):
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        archive = (self.ARCHIVE_HEAD +
                   "| # | Status | Wish | Class | Decision |\n|---|---|---|---|---|\n"
                   "| 480 | *queued* 2026-07-23 | a wish | bug | Done when: x |\n")
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", archive)
        code, out = self._run()
        self.assertNotEqual(code, 0, "the non-terminal row must red at its real column:\n" + out)
        self.assertIn("480", out)

    def test_a_reordered_header_passes_a_terminal_row(self):
        _write(self.tmp, "ROADMAP.md", _live_doc(MONTH_MANIFEST))
        archive = (self.ARCHIVE_HEAD +
                   "| # | Status | Wish | Class | Decision |\n|---|---|---|---|---|\n"
                   "| 480 | **landed 2026-07-23** | a wish | bug | Done when: x |\n")
        _write(self.tmp, "docs/queue-archive/rotated-ROADMAP-2026-07.md", archive)
        code, out = self._run()
        self.assertEqual(code, 0, "a terminal row at a moved column must pass:\n" + out)
