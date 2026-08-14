"""The queue has a far tier, and it stands down by name and surfaces itself rarely.

SPEC INV-222 (ROADMAP 382) — a wish kept because discarding it would lose the thought, carrying
no revisit trigger and no plan to run, takes the `far` status, distinct from `deferred` whose
trigger the queue-take re-scans every time [INV-129]; the what's-left report and the feature map
read the runnable queue and stand the far tier down by name, offering it on request.

SPEC INV-223 (ROADMAP 403) — the far backlog surfaces itself rarely and unasked: the status
report carries a rare line naming that a far tier exists, at a settings-ladder cadence default
(at most once every fourteen days) with a dated marker; a second offer inside the window reds.

The checker `guardrails/check-far-tier.py` is report-shape only and is NOT in the pre-push chain
(a chat report is not a committed file a push gate could scan); the suite drives it over fixtures.
"""
import os
import subprocess

from conftest import ROOT, read, read_all, read_all_flat

CHECK = os.path.join(ROOT, "guardrails", "check-far-tier.py")
FIX = os.path.join(ROOT, "guardrails", "far-tier-fixtures")


def _run(*args):
    return subprocess.run(["python3", CHECK, *args], capture_output=True, text=True)


def _fix(name):
    return os.path.join(FIX, name)


# --- the checker ships ---

def test_checker_ships():
    assert os.path.isfile(CHECK), "guardrails/check-far-tier.py missing"


def test_checker_not_wired_into_pre_push():
    # report-shape, chat-surface: it rides the suite, never the push chain.
    assert "check-far-tier" not in read("guardrails/pre-push")


# --- INV-222: the runnable report stands the far tier down (red-first) ---

def test_report_reds_a_far_row_named_in_the_runnable_region():
    r = _run("--report", _fix("report-names-far-in-runnable.md"))
    assert r.returncode != 0, "checker passed a far row named among runnable work"
    assert "INV-222" in (r.stdout + r.stderr)
    assert "411" in (r.stdout + r.stderr)


def test_report_reds_runnable_work_with_no_standdown():
    r = _run("--report", _fix("report-runnable-no-standdown.md"))
    assert r.returncode != 0, "checker passed a runnable report that stands the far tier down nowhere"
    assert "INV-222" in (r.stdout + r.stderr)


def test_report_passes_when_the_far_tier_is_stood_down_and_offered():
    r = _run("--report", _fix("report-stands-far-down.md"))
    assert r.returncode == 0, r.stdout + r.stderr


# --- INV-222: the far-vs-deferred distinction, mechanical (red-first) ---

def test_vocab_reds_a_far_row_carrying_a_trigger():
    r = _run("--vocab", _fix("vocab-far-with-trigger.md"))
    assert r.returncode != 0, "checker passed a far row carrying a revisit trigger"
    assert "INV-222" in (r.stdout + r.stderr)
    assert "500" in (r.stdout + r.stderr)


def test_vocab_reds_a_deferred_row_carrying_no_trigger():
    r = _run("--vocab", _fix("vocab-deferred-without-trigger.md"))
    assert r.returncode != 0, "checker passed a deferred row with nothing for the re-scan to read"
    assert "INV-129" in (r.stdout + r.stderr)


def test_vocab_passes_a_clean_far_and_deferred_set():
    r = _run("--vocab", _fix("vocab-clean.md"))
    assert r.returncode == 0, r.stdout + r.stderr


# --- INV-223: the rare self-surfacing window (red-first) ---

def test_window_reds_a_second_offer_inside_the_window():
    r = _run("--window", _fix("window-second-offer-in-window.md"))
    assert r.returncode != 0, "checker passed a second far-tier offer inside the cadence window"
    assert "INV-223" in (r.stdout + r.stderr)


def test_window_passes_a_first_offer_after_the_window():
    r = _run("--window", _fix("window-first-offer-after-window.md"))
    assert r.returncode == 0, r.stdout + r.stderr


# --- the far status stands in the vocabulary homes ---

def test_roadmap_template_carries_the_far_status():
    t = read("templates/ROADMAP.template.md")
    assert "*far*" in t, "the roadmap template's status vocabulary does not carry *far*"


def test_settings_ladder_carries_the_cadence_default():
    base = read_all("skills/live-spec-base/SKILL.md")
    assert "far-tier.surface-cadence" in base, "the settings ladder carries no far-tier cadence default"


def test_communicator_report_stands_the_far_tier_down():
    flat = read_all_flat("skills/communicator/SKILL.md")
    assert "far tier" in flat or "far backlog" in flat
    assert "on request" in flat


def test_communicator_carries_the_rare_surfacing_line():
    flat = read_all_flat("skills/communicator/SKILL.md")
    assert "INV-223" in flat


# --- the real queue: the far tier is populated, and the two rows landed ---

def test_real_roadmap_far_rows_carry_the_far_token():
    roadmap = read("ROADMAP.md")
    # rows 411 and 381 are far-tier by the owner's word (NEXT_STEPS)
    for line in roadmap.splitlines():
        if line.startswith("| 411 |") or line.startswith("| 381 |"):
            assert "far" in line.lower(), "a far-tier row does not carry the far token: %s" % line[:60]


# --- INV-222/223 in the spec, index, architecture, matrix ---

def test_spec_states_both_laws():
    spec = read("PRODUCT_SPEC.md")
    assert "INV-222" in spec
    assert "INV-223" in spec
    assert "far tier" in spec.lower() or "far backlog" in spec.lower()


def test_formal_index_rows():
    spec = read("PRODUCT_SPEC.md")
    assert "| INV-222 |" in spec
    assert "| INV-223 |" in spec


def test_architecture_owns_both_invariants():
    arch = read("ARCHITECTURE.md")
    assert "INV-222" in arch
    assert "INV-223" in arch


def test_matrix_rows_cover_both_laws():
    matrix = read("TEST_MATRIX.md")
    assert "INV-222" in matrix
    assert "INV-223" in matrix
