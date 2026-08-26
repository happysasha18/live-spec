"""A worker's teardown reaps its own process group (SPEC INV-230, ROADMAP 393).

INV-213 already landed the NOTICE — a report-only mechanism that finds an owned, orphaned, burning
descendant and reports it, ending nothing. This row lands the remaining two arms of the same class:

  1. THE REAP. A worker's teardown reaps its OWN process group — a scoped kill of the process group
     the run itself owns. It is safe because it targets the run's own group, exactly INV-162's
     owned-identity discipline: the reap takes a numeric process group, never a program name, and
     refuses any group it cannot prove the run owns. It reports through the shared cleanup-notice
     shape (row 417, INV-204), so the reap says what it ended.

  2. THE IDLE-OUTPUT DETECTION HABIT. A worker whose status reads "running" while its output file has
     stopped growing is checked by output mtime — the liveness-via-mtime read (INV-76) — so a stalled
     worker is caught rather than left to a frozen status line (the memory instance, 2026-07-17).

The tests drive fakes and a simulated worker table — no process is ever killed on the real machine.
"""
import importlib.util
import os
import signal

import pytest
from conftest import ROOT, read

MOD = os.path.join(ROOT, "guardrails", "reap_owned_group.py")


def _load():
    assert os.path.isfile(MOD), "guardrails/reap_owned_group.py missing"
    spec = importlib.util.spec_from_file_location("reap_owned_group", MOD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class _Killpg:
    """A fake os.killpg that records its calls and ends nothing real."""
    def __init__(self):
        self.calls = []

    def __call__(self, pgid, sig):
        self.calls.append((pgid, sig))


# --- the mechanism ships and reuses the shared cleanup-notice shape ---

def test_reap_reports_through_the_cleanup_notice_module():
    # the reap reuses the shared notice home (row 417), it mints no second one.
    assert "cleanup_notice" in read("guardrails/reap_owned_group.py")


# --- arm 1: the reap is named and scoped to the run's own owned group ---

def test_reap_of_owned_group_is_named_and_scoped():
    import io
    mod = _load()
    fake = _Killpg()
    buf = io.StringIO()
    line = mod.reap_owned_group(500, {500}, "worker child group (this run spawned it)",
                                killpg=fake, out=buf)
    # it killed exactly the owned process group, by its numeric id, once.
    assert fake.calls == [(500, signal.SIGTERM)], fake.calls
    # and it said what it ended, with the ownership proof, through the shared shape.
    out = buf.getvalue() + line
    assert "CLEANUP-NOTICE" in out, out
    assert "ended=pgid=500" in out
    assert "pgid=500" in out  # the owned-via proof names the group


def test_reap_refuses_an_unowned_group_and_ends_nothing():
    # THE core safety proof: a group the run cannot prove it owns is refused — killpg is never called.
    mod = _load()
    fake = _Killpg()
    with pytest.raises(mod.UnownedReapRefused):
        mod.reap_owned_group(9001, {500}, "a foreign group", killpg=fake)
    assert fake.calls == [], "a reap fired on an unowned group — INV-162 breach: %r" % fake.calls


def test_reap_refuses_a_non_numeric_target():
    # a name is not even expressible: the reap takes a numeric process group, never a program name.
    mod = _load()
    fake = _Killpg()
    with pytest.raises(mod.UnownedReapRefused):
        mod.reap_owned_group("chrome", {500}, "a name", killpg=fake)
    assert fake.calls == []


def test_reap_source_names_no_process_by_name():
    # the reap ends a process, but only by owned process group (os.killpg) — never a name-based kill.
    src = read("guardrails/reap_owned_group.py")
    for verb in ("pkill", "killall", "pgrep", "pidof"):
        assert verb not in src, "the reap must not end a process by name, found %r" % verb


# --- arm 2: the idle-output detection habit (INV-76 kin) ---

def test_idle_output_running_but_stale_is_detected():
    mod = _load()
    now = 1_000_000.0
    workers = [
        {"status": "running", "output_mtime": now - 600, "pgid": 500, "label": "stalled"},
    ]
    got = mod.find_idle_output_workers(workers, now, idle_threshold=120.0)
    assert [w["label"] for w in got] == ["stalled"], got
    assert got[0]["pgid"] == 500


def test_idle_output_running_and_fresh_is_not_detected():
    mod = _load()
    now = 1_000_000.0
    workers = [{"status": "running", "output_mtime": now - 5, "pgid": 500}]
    assert mod.find_idle_output_workers(workers, now, idle_threshold=120.0) == []


def test_idle_output_finished_worker_is_not_detected():
    # a worker whose status is not "running" is not the stalled-but-claiming-running case.
    mod = _load()
    now = 1_000_000.0
    workers = [{"status": "done", "output_mtime": now - 9999, "pgid": 500}]
    assert mod.find_idle_output_workers(workers, now, idle_threshold=120.0) == []


def test_idle_output_no_output_yet_is_not_flagged_here():
    # with no output timestamp there is nothing to read idleness from — not this habit's case.
    mod = _load()
    now = 1_000_000.0
    workers = [{"status": "running", "output_mtime": None, "pgid": 500}]
    assert mod.find_idle_output_workers(workers, now, idle_threshold=120.0) == []


# --- the reap is a process-space habit, NOT a pre-push gate ---

def test_reap_not_wired_as_a_prepush_gate():
    assert "reap_owned_group" not in read("guardrails/pre-push")


def test_reap_not_a_ci_step():
    assert "reap_owned_group" not in read(".github/workflows/gates.yml")


# --- the reap module passes the owned-identity gate (the row-417 probe pattern) ---

def test_reap_module_passes_the_broad_kill_gate():
    import subprocess
    guard = os.path.join(ROOT, "guardrails", "check-broad-kill.sh")
    r = subprocess.run(["bash", guard, MOD], capture_output=True, text=True)
    assert r.returncode == 0, "the reap tripped the broad-kill gate: %s" % (r.stdout + r.stderr)


# --- spec / architecture / matrix carry the law ---

def test_spec_states_the_law():
    import re
    spec = read("PRODUCT_SPEC.md")
    assert re.search(r"\[[^\]\n]*\bINV-230\b[^\]\n]*\]", spec)
    assert "| INV-230 |" in spec


def test_worker_contract_carries_the_idle_habit():
    # the idle-output detection habit stands in the worker contract (ACT-3 home).
    spec = read("PRODUCT_SPEC.md")
    assert "INV-230" in spec


def test_architecture_owns_the_invariant():
    assert "INV-230" in read("ARCHITECTURE.md")


def test_matrix_row_covers_the_law():
    assert "INV-230" in read("TEST_MATRIX.md")
