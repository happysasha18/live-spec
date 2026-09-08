"""The session-start probe reads recorded state; it runs no acceptance command (PLAN q-826, the
owner's word 2026-09-07 22:00).

Until this row the probe ran every plan row's own recorded acceptance command, serially, with no
time limit — 75 commands at every session start. It now takes the same road
scripts/render-board.sh already takes off the machine that holds the work
(LIVE_SPEC_BOARD_CHECKS=off): no command runs, and a done row's checkpoint — its own passed
acceptance receipt, and whether its definition of done or its acceptance command has moved since
that receipt was written — decides what the probe names as needing a fresh check.

Each test builds a throwaway copy of the tree in tmp_path and runs `scripts/state-probe.sh`
there, never against the real PLAN.md or the real checkpoints (the same isolation
tests/test_plan_is_not_executable.py uses, for the same reason: a test that mutates a file a
person owns is a bad test even when its restore is correct).
"""
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from conftest import ROOT

ROOT = Path(ROOT)

# task-admission.py cannot be `import`ed by its hyphenated name; loaded the same way
# tests/test_task_admission.py already loads it, so dod_digest here is the real function the
# probe itself calls, never a re-derived copy of its formula.
_SCRIPT = ROOT / "scripts" / "task-admission.py"
sys.path.insert(0, str(_SCRIPT.parent))
_spec = importlib.util.spec_from_file_location("task_admission", _SCRIPT)
admission = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(admission)

NEEDED = (
    "scripts/state-probe.sh",
    "scripts/plan_checks.py",
    "scripts/plan_checks_core.py",
    "scripts/task-admission.py",
    "scripts/checkpoint.py",
)

ACCEPTANCE_COMMAND = "true"


def _row(task_id, title, dod_hash):
    """One `## Tasks` row, done, carrying a definition of done and its own recorded hash."""
    return (
        "### ✅ %s — id: %s\n"
        "**Group:** Test · **Priority:** normal\n"
        "**Source:** the test.\n"
        "\n"
        "**Done when:** it happens.\n"
        "\n"
        "**DOD hash.** %s\n"
        "\n" % (title, task_id, dod_hash)
    )


def _checkpoint_text(dod_anchor=None, accept_anchor=None, receipt=None):
    lines = ["# fixture checkpoint", "Status: closed", "Owner: test", "", "## DONE"]
    if dod_anchor is not None:
        lines.append("DOD: %s" % dod_anchor)
    if accept_anchor is not None:
        lines.append("ACCEPT: %s" % accept_anchor)
    if receipt is not None:
        lines.append("RECEIPT: %s" % json.dumps(receipt))
    return "\n".join(lines) + "\n"


def _build(tmp_path, sentinel, heal=()):
    """Build the fixture tree. `heal` names ids whose checkpoint should be rewritten so that
    id's own drift no longer holds — the row it names stays done, receipted and unmoved, so
    a test can prove a specific drift is what drives the count by comparing this against the
    drifted build with everything else held equal."""
    for rel in NEEDED:
        dst = tmp_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)

    accept_digest = admission.dod_digest(ACCEPTANCE_COMMAND)

    plan = (
        "# Plan\n\n## Tasks\n\n"
        + _row("row-sentinel", "A row whose key must never run", "hash-sentinel")
        + _row("row-standing", "A row whose recorded state holds", "hash-standing")
        + _row("row-dod-moved", "A row whose done moved since its receipt", "hash-dod-current")
        + _row("row-accept-moved", "A row whose acceptance moved since its receipt", "hash-accept")
        + _row("row-no-receipt", "A row with no receipt at all", "hash-no-receipt")
        + "## Blockers\n\n- none\n"
    )
    (tmp_path / "PLAN.md").write_text(plan, encoding="utf-8")

    checks = tmp_path / "scripts" / "plan_checks.py"
    checks.write_text(
        checks.read_text(encoding="utf-8")
        + "\nCHECKS.clear()\n"
        + "".join(
            "CHECKS[%r] = %r\n" % (task_id, cmd)
            for task_id, cmd in (
                ("row-sentinel", "touch %s" % sentinel),
                ("row-standing", ACCEPTANCE_COMMAND),
                ("row-dod-moved", ACCEPTANCE_COMMAND),
                ("row-accept-moved", ACCEPTANCE_COMMAND),
                ("row-no-receipt", ACCEPTANCE_COMMAND),
            )
        ),
        encoding="utf-8",
    )

    cps = tmp_path / ".live-spec" / "checkpoints"
    cps.mkdir(parents=True)
    passed = {"by": "test", "at": "2026-01-01T00:00:00", "verdict": "passed"}
    # row-sentinel: no checkpoint at all — untested for the recheck line, only for the spawn ban.
    (cps / "row-standing.md").write_text(
        _checkpoint_text(dod_anchor="hash-standing", accept_anchor=accept_digest, receipt=passed),
        encoding="utf-8",
    )
    (cps / "row-dod-moved.md").write_text(
        # The checkpoint's DOD anchor is the hash the row was admitted with; the row's own
        # `**DOD hash.**` line now reads "hash-dod-current" — the done moved since. Healed:
        # the anchor is rewritten to match the row's current hash, so this row's done no
        # longer moved since its receipt.
        _checkpoint_text(
            dod_anchor=("hash-dod-current" if "row-dod-moved" in heal else "hash-dod-admitted"),
            accept_anchor=accept_digest,
            receipt=passed,
        ),
        encoding="utf-8",
    )
    (cps / "row-accept-moved.md").write_text(
        # Healed: the accept anchor is rewritten to the digest of the command actually
        # recorded now, so this row's acceptance command no longer moved since its receipt.
        _checkpoint_text(
            dod_anchor="hash-accept",
            accept_anchor=(accept_digest if "row-accept-moved" in heal else "a-digest-nobody-runs-now"),
            receipt=passed,
        ),
        encoding="utf-8",
    )
    # row-no-receipt: no checkpoint file at all, unless healed — then it gets a real one, with
    # nothing moved and a passed receipt, same shape as row-standing.
    if "row-no-receipt" in heal:
        (cps / "row-no-receipt.md").write_text(
            _checkpoint_text(dod_anchor="hash-no-receipt", accept_anchor=accept_digest, receipt=passed),
            encoding="utf-8",
        )


def _run(tmp_path, heal=()):
    tmp_path.mkdir(parents=True, exist_ok=True)
    sentinel = tmp_path / "sentinel-fired"
    _build(tmp_path, sentinel, heal=heal)
    r = subprocess.run(
        ["bash", str(tmp_path / "scripts" / "state-probe.sh")],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
        env={"HOME": str(tmp_path), "PATH": __import__("os").environ.get("PATH", "")},
    )
    return r, sentinel


def _recheck_line(stdout):
    lines = [ln for ln in stdout.splitlines() if "need a fresh check" in ln]
    return lines[0] if lines else ""


def _recheck_count(stdout):
    """The probe now names only a COUNT of done rows needing a fresh check, plus a pointer to
    the board — never the wall of ids it used to print. A test that wants to prove one specific
    row's drift is what the count counts has to isolate that row: heal only its own drift, hold
    every other row exactly as built, and show the count drops by exactly one."""
    line = _recheck_line(stdout)
    m = re.search(r"(\d+) done row", line)
    return int(m.group(1)) if m else 0


def test_the_probe_spawns_no_acceptance_command(tmp_path):
    r, sentinel = _run(tmp_path)
    assert not sentinel.exists(), (
        "the probe ran a row's acceptance command: %s\n%s" % (r.stdout, r.stderr)
    )


def test_a_row_whose_recorded_state_holds_is_not_named(tmp_path):
    r, _ = _run(tmp_path)
    line = _recheck_line(r.stdout)
    assert "row-standing" not in line, (
        "a row with a passed receipt, an unmoved done and an unmoved acceptance command was "
        "still named as needing a fresh check: %r" % line
    )


def test_a_row_whose_done_moved_since_its_receipt_is_named(tmp_path):
    r_drifted, _ = _run(tmp_path / "drifted")
    r_healed, _ = _run(tmp_path / "healed", heal=("row-dod-moved",))
    n_drifted = _recheck_count(r_drifted.stdout)
    n_healed = _recheck_count(r_healed.stdout)
    # Healing only row-dod-moved's own drift, and nothing else in the fixture, must drop the
    # count by exactly one. If the DOD-drift read stopped firing, healing it would change
    # nothing and n_healed would equal n_drifted.
    assert n_healed == n_drifted - 1, (
        "healing row-dod-moved's DOD drift did not drop the count by one: drifted=%d healed=%d\n"
        "drifted:\n%s\nhealed:\n%s" % (n_drifted, n_healed, r_drifted.stdout, r_healed.stdout)
    )


def test_a_row_whose_acceptance_moved_since_its_receipt_is_named(tmp_path):
    r_drifted, _ = _run(tmp_path / "drifted")
    r_healed, _ = _run(tmp_path / "healed", heal=("row-accept-moved",))
    n_drifted = _recheck_count(r_drifted.stdout)
    n_healed = _recheck_count(r_healed.stdout)
    # Healing only row-accept-moved's own drift must drop the count by exactly one. If the
    # acceptance-drift read stopped firing, healing it would change nothing.
    assert n_healed == n_drifted - 1, (
        "healing row-accept-moved's acceptance drift did not drop the count by one: "
        "drifted=%d healed=%d\ndrifted:\n%s\nhealed:\n%s"
        % (n_drifted, n_healed, r_drifted.stdout, r_healed.stdout)
    )


def test_the_probe_names_what_it_could_not_read_instead_of_falling_silent(tmp_path):
    """F3: a host installed through adopt/install-status-view.sh used to lose the whole
    recheck arm with no word at all when scripts/task-admission.py or scripts/checkpoint.py was
    not vendored beside the probe — the failure read exactly like a tree where every done row's
    recorded state held. Proved here by building a tree that carries neither file."""
    for rel in ("scripts/state-probe.sh", "scripts/plan_checks.py", "scripts/plan_checks_core.py"):
        dst = tmp_path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    plan = (
        "# Plan\n\n## Tasks\n\n"
        + _row("row-1", "A done row", "hash-1")
        + "## Blockers\n\n- none\n"
    )
    (tmp_path / "PLAN.md").write_text(plan, encoding="utf-8")
    r = subprocess.run(
        ["bash", str(tmp_path / "scripts" / "state-probe.sh")],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
        env={"HOME": str(tmp_path), "PATH": __import__("os").environ.get("PATH", "")},
    )
    assert "the recorded-state read did not run" in r.stdout, (
        "the probe fell silent instead of naming what it could not read:\n%s\n%s"
        % (r.stdout, r.stderr)
    )
    assert "task-admission.py" in r.stdout, r.stdout


def test_a_row_with_no_receipt_at_all_is_named(tmp_path):
    r_drifted, _ = _run(tmp_path / "drifted")
    r_healed, _ = _run(tmp_path / "healed", heal=("row-no-receipt",))
    n_drifted = _recheck_count(r_drifted.stdout)
    n_healed = _recheck_count(r_healed.stdout)
    # Giving row-no-receipt an actual passed, unmoved checkpoint — and changing nothing else —
    # must drop the count by exactly one. If a done row with no receipt stopped being counted
    # as needing a fresh check, adding the receipt would change nothing.
    assert n_healed == n_drifted - 1, (
        "giving row-no-receipt a receipt did not drop the count by one: drifted=%d healed=%d\n"
        "drifted:\n%s\nhealed:\n%s" % (n_drifted, n_healed, r_drifted.stdout, r_healed.stdout)
    )
