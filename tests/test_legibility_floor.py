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
    arch = read("ARCHITECTURE.md")     # the whole architecture: the core and the parts its map names
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


def _unresolved_section(stdout):
    return stdout.split("UNRESOLVED", 1)[1] if "UNRESOLVED" in stdout else ""


def test_chainless_selector_is_scored_against_the_card_its_element_sits_in():
    """The shape a class is usually written in, judged three ways across three landings.

    A selector with no chain at all — `.card-title`, on a dark page holding a white card. The
    2026-07-13 lint paired it with the PAGE, reporting the readable caption (#4d5156, 8:1 on the
    card) as a failure at 2.3:1 and passing the invisible one (#e8e4de, 1.3:1 on the card) at
    14.6:1. The 2026-08-28 repair stopped scoring it at all and sent both to UNRESOLVED, which
    stopped the wrong numbers and stopped the right ones with them. The stylesheet cannot say which
    surface a chainless class sits on; the MARKUP can, and it is in the same file. Both captions are
    inside `<div class="card">`, so both are scored against #ffffff: the readable one passes and the
    invisible one reds."""
    r = _run(FIX / "legibility_chainless.html")
    assert r.returncode == 1, "the invisible caption went unreported: " + r.stdout
    title_lines = [l for l in r.stdout.splitlines() if ".card-title" in l]
    assert any("low-contrast" in l for l in title_lines), (
        "#e8e4de on the card's #ffffff is 1.3:1 and must red: " + r.stdout
    )
    assert any("#ffffff" in l for l in r.stdout.splitlines() if "ratio" in l), (
        "the failing pair must be measured against the card it sits in, not the page: " + r.stdout
    )
    for line in r.stdout.splitlines():
        if ".card-note" in line:
            assert "low-contrast" not in line, (
                "#4d5156 on the card's #ffffff is 8:1 and must pass: " + r.stdout
            )
    assert ".card-note" not in _unresolved_section(r.stdout), (
        "a pair the markup determines must be measured, never stood down: " + r.stdout
    )


def test_one_unrelated_painted_element_does_not_silence_the_page():
    """The defect the markup read removes, stated as its own case.

    The whole-file question — does this stylesheet paint any surface of its own? — was asked once
    per file and answered for every rule in it. So a single `.chip { background: … }` the text is
    not inside, or one inline `style="background:…"` on an unrelated box, sent every chainless rule
    in the page to UNRESOLVED, and the run then printed OK. The red fixture with that one line added
    must stay exactly as red as the red fixture."""
    import tempfile
    original = (FIX / "legibility_red.html").read_text(encoding="utf-8")
    noisy = original.replace(
        "</style>", ".chip { background: #eee; }\n</style>",
    ).replace(
        "</body>",
        '<span class="chip">a chip</span>\n'
        '<div style="background: linear-gradient(#111,#222)">an unrelated painted box</div>\n'
        "</body>",
    )
    assert noisy != original, "the fixture's shape changed; this test no longer adds anything"
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "legibility_red_with_noise.html"
        path.write_text(noisy, encoding="utf-8")
        r = _run(path)
    assert r.returncode == 1, "an unrelated painted element silenced the whole page: " + r.stdout
    assert r.stdout.count("low-contrast") >= 2, (
        "both contrast hits must survive the unrelated paint: " + r.stdout
    )
    assert r.stdout.count("small-text") >= 2, (
        "both size hits must survive the unrelated paint: " + r.stdout
    )


def test_page_background_is_never_invented_where_the_page_declares_none():
    """The same guess one layer down. Where no root element declares a background, the lint used to
    substitute the most commonly declared colour in the file — here #7f7f7f, read off three
    TRANSLUCENT rules whose rendered colour depends on what is under them — and then scored every
    rule against it. Two invented inputs, one confident ratio. Nothing in this file determines a
    background, so nothing in it is scored."""
    r = _run(FIX / "legibility_no_page_background.html")
    assert "low-contrast" not in r.stdout, (
        "a ratio was computed against a background the file never declares: " + r.stdout
    )
    assert "body" in _unresolved_section(r.stdout), (
        "the undeterminable page background must be reported, not substituted: " + r.stdout
    )


def test_translucent_colour_is_not_read_as_its_opaque_triple():
    """A colour that lets the layer beneath it through is not a colour this reader knows."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("leg", SCRIPT)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    assert mod.parse_color("rgba(127,127,127,.14)") is None
    assert mod.parse_color("#7f7f7f24") is None
    assert mod.parse_color("rgba(127,127,127,1)") == (127, 127, 127)
    assert mod.parse_color("#7f7f7f") == (127, 127, 127)


def test_unresolvable_background_reported_separately_not_silently_paired():
    """A surface painted in a colour this reader cannot read still has to be said out loud.

    `.outer-wrap` is painted with a gradient, so the caption inside it renders against something no
    static read of the text can name. That pair must be listed as UNRESOLVED — never silently scored
    against the page behind the gradient, which is a false pass or a false failure hiding behind a
    guessed pair."""
    r = _run(FIX / "legibility_ancestor.html")
    assert "UNRESOLVED" in r.stdout, "no unresolved section printed: " + r.stdout
    assert "odd-caption" in r.stdout.split("UNRESOLVED", 1)[1]
    for line in r.stdout.splitlines():
        if "odd-caption" in line:
            assert "low-contrast" not in line, "unresolved pair must not be reported as a failure: " + r.stdout


def test_a_run_that_could_not_measure_everything_never_says_the_text_meets_the_floor():
    """The verdict is the result, and it has to be true of the whole file.

    Until 2026-08-28 the OK line printed whenever no hit was found, however many pairs went unread,
    so "text meets the contrast and size floor" was a claim about text the reader never looked at.
    The stand-down says what was covered instead, in the shape preshow-register-lint.py already
    prints when its judge could not read a file."""
    r = _run(FIX / "legibility_no_page_background.html")
    assert "UNRESOLVED" in r.stdout, "this fixture no longer leaves anything unresolved: " + r.stdout
    assert "OK (preshow-legibility)" not in r.stdout, (
        "a run that could not measure the page still gave it a clean bill: " + r.stdout
    )
    assert "STOOD DOWN IN PART" in r.stdout, (
        "a run that read only part of a page must say so: " + r.stdout
    )
    # The exit code stays put on purpose: a gradient or an image background is not a defect an
    # author can lift to a floor, and a gate that reds on one gets switched off with the real hits
    # inside it. What changed is the sentence, which now tells the truth about what was read.
    assert r.returncode == 0, "an unmeasurable pair must not block the showing: " + r.stdout


def test_a_fully_measured_clean_page_still_says_so_plainly():
    """The stand-down must not swallow the plain pass, or every green run reads as a warning."""
    r = _run(FIX / "legibility_green.html")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "OK (preshow-legibility)" in r.stdout
    assert "STOOD DOWN" not in r.stdout, (
        "nothing in this fixture is unreadable, so nothing should stand down: " + r.stdout
    )
