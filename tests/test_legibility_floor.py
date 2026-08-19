"""INV-139 — the legibility floor: min contrast ratio + min text size, checked at the pre-show gate.
Landed 2026-07-13."""
import subprocess, sys
from pathlib import Path

from conftest import SPEC, read

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "preshow-legibility-lint.py"
FIX = ROOT / "tests" / "fixtures"


def _run(path):
    return subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)


def test_red_fixture_flagged():
    r = _run(FIX / "legibility_red.html")
    assert r.returncode == 1, r.stdout + r.stderr
    assert "low-contrast" in r.stdout
    assert "small-text" in r.stdout


def test_green_fixture_passes():
    r = _run(FIX / "legibility_green.html")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "OK (preshow-legibility)" in r.stdout


def test_contrast_math():
    import importlib.util
    spec = importlib.util.spec_from_file_location("leg", SCRIPT)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    # black vs white is 21:1
    assert round(mod.contrast((0, 0, 0), (255, 255, 255)), 1) == 21.0


def test_spec_clause_and_index():
    spec = read(SPEC)     # the whole spec: the core and the parts its map names
    assert "legibility floor" in spec
    assert "[INV-139]" in spec
    assert any(line.startswith("| INV-139 |") for line in spec.splitlines())


def test_design_principle_and_preshow_wired():
    arch = (ROOT / "ARCHITECTURE.md").read_text(encoding="utf-8")
    assert "legibility floor" in arch
    comm = (ROOT / "skills" / "communicator" / "SKILL.md").read_text(encoding="utf-8")
    assert "preshow-legibility-lint.py" in comm


def test_matrix_row():
    matrix = read("TEST_MATRIX.md")
    assert any(l.startswith("| M-") and "INV-139" in l for l in matrix.splitlines())


def test_ancestor_background_not_page_background():
    """Bug: the lint paired every foreground with the PAGE background, never a painting ancestor.
    A light card (`.gg { background:#fff }`) holding a near-black caption (`.gg .cap`) must be judged
    against the CARD's white background (ratio ~8:1, passes) — not against the dark page (~2.3:1, a
    false low-contrast hit). Inbox: 2026-07-27-from-tlvphotos-legibility-lint-reads-the-wrong-background."""
    r = _run(FIX / "legibility_ancestor.html")
    assert ".cap" not in r.stdout or "low-contrast" not in r.stdout.split(".cap")[1].split("\n")[0], (
        "the light-card caption must not be reported as low-contrast: " + r.stdout
    )
    for line in r.stdout.splitlines():
        if ".cap" in line and "low-contrast" in line:
            raise AssertionError("false low-contrast hit on a resolvable light-card caption: " + r.stdout)


def test_genuine_failure_under_a_card_is_still_caught():
    """The other direction: a genuinely low-contrast pair sitting under the SAME kind of light card
    (`.gg2 .low`, light-gray-on-white, ratio ~1.3:1) must still be reported — and reported against its
    real ancestor background, not waved through because the page itself is dark."""
    r = _run(FIX / "legibility_ancestor.html")
    assert r.returncode == 1, r.stdout + r.stderr
    hit_lines = [l for l in r.stdout.splitlines() if ".low" in l]
    assert any("low-contrast" in l for l in hit_lines), "genuine low-contrast pair went unreported: " + r.stdout
    assert any("#ffffff" in l for l in hit_lines), (
        "the failing pair must be paired with its real ancestor (#ffffff), not the page background: " + r.stdout
    )


def test_unresolvable_background_reported_separately_not_silently_paired():
    """When the painting rule can't be found from the CSS text at all (ancestor class with no
    declared background — the lint can't see what covers it), the pair must be listed as UNRESOLVED,
    never silently scored against the page background (that was the other half of the bug: a false
    pass/fail hiding behind a guessed pair)."""
    r = _run(FIX / "legibility_ancestor.html")
    assert "UNRESOLVED" in r.stdout, "no unresolved section printed: " + r.stdout
    assert "odd-caption" in r.stdout.split("UNRESOLVED", 1)[1]
    for line in r.stdout.splitlines():
        if "odd-caption" in line:
            assert "low-contrast" not in line, "unresolved pair must not be reported as a failure: " + r.stdout
