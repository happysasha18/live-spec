"""A cleanup says what it ended (SPEC INV-204, ROADMAP 417).

Every process this pack ends is reported with WHAT it was and WHY the run owned it — the PID, the
process group, or the owned path that proves ownership — so an ending nobody expected is visible the
moment it happens rather than at the next unexplained loss. This notice ships AHEAD of INV-162's
stricter form: it shows what the strict check would have refused before the strict check starts
refusing.

Two arms, the same shape as the pack's other nets:
  * a shared notice helper (`guardrails/cleanup_notice.py`) the cleanup paths emit through, and
  * a gate (`guardrails/check-cleanup-notice.sh`) that reds a cleanup path ending a process WITHOUT
    emitting the notice.
The pack's one real cleanup path is the headless harness's process-group reap; it emits the notice.
"""
import os
import re
import subprocess
import tempfile

from conftest import ROOT, read

HELPER = os.path.join(ROOT, "guardrails", "cleanup_notice.py")
GATE = os.path.join(ROOT, "guardrails", "check-cleanup-notice.sh")
HARNESS = os.path.join(ROOT, "templates", "headless_harness.py")


def _gate(target=None):
    cmd = ["bash", GATE] + ([target] if target else [])
    return subprocess.run(cmd, capture_output=True, text=True)


def _write(d, name, body):
    p = os.path.join(d, name)
    with open(p, "w") as f:
        f.write(body)
    return p


# --- the shared helper ---

def test_helper_emits_what_and_why():
    # driving the real helper prints one CLEANUP-NOTICE line naming WHAT ended and the owned-via proof.
    r = subprocess.run(
        ["python3", "-c",
         "import sys; sys.path.insert(0, %r); import cleanup_notice as c; "
         "c.cleanup_notice('pgid=48213', 'chrome (test browser)', 'process-group this run launched')"
         % os.path.dirname(HELPER)],
        capture_output=True, text=True)
    out = r.stdout + r.stderr
    assert "CLEANUP-NOTICE" in out, out
    assert "pgid=48213" in out
    assert "chrome (test browser)" in out
    assert "process-group this run launched" in out


# --- the gate ---

def test_gate_reds_an_ending_without_a_notice():
    # RED-FIRST: a cleanup that reaps a process group but never says what it ended.
    with tempfile.TemporaryDirectory() as d:
        bad = _write(d, "reap.py",
                     "import os, signal\n"
                     "def reap(pgid):\n"
                     "    os.killpg(pgid, signal.SIGKILL)\n")
        r = _gate(bad)
        assert r.returncode != 0, "gate passed an ending that emits no notice"
        assert "INV-204" in (r.stdout + r.stderr)


def test_gate_reds_a_terminate_only_ending():
    # RED-FIRST against the pre-review gate: a file whose only ending is `proc.terminate()` (or
    # `proc.kill()`) ends a spawned child but the gate was blind to the standard Popen endings, so it
    # passed with no notice. The adversarial review of 2026-07-17 added them.
    with tempfile.TemporaryDirectory() as d:
        bad = _write(d, "stop.py",
                     "import subprocess\n"
                     "def stop(proc):\n"
                     "    proc.terminate()\n")
        r = _gate(bad)
        assert r.returncode != 0, "gate passed a proc.terminate() ending that emits no notice"
        assert "INV-204" in (r.stdout + r.stderr)


def test_gate_reds_a_proc_kill_ending():
    with tempfile.TemporaryDirectory() as d:
        bad = _write(d, "stop.py",
                     "import subprocess\n"
                     "def stop(proc):\n"
                     "    proc.kill()\n")
        r = _gate(bad)
        assert r.returncode != 0, "gate passed a proc.kill() ending that emits no notice"


def test_gate_passes_an_ending_that_emits_the_notice():
    with tempfile.TemporaryDirectory() as d:
        ok = _write(d, "reap.py",
                    "import os, signal\n"
                    "def reap(pgid):\n"
                    "    print('CLEANUP-NOTICE ended=pgid=%d what=chrome owned-via=process-group' % pgid)\n"
                    "    os.killpg(pgid, signal.SIGKILL)\n")
        r = _gate(ok)
        assert r.returncode == 0, r.stdout + r.stderr


def test_gate_passes_a_file_that_ends_nothing():
    with tempfile.TemporaryDirectory() as d:
        ok = _write(d, "probe.py",
                    "import os\n"
                    "def alive(pid):\n"
                    "    os.kill(pid, 0)   # a liveness probe, ends nothing\n")
        r = _gate(ok)
        assert r.returncode == 0, r.stdout + r.stderr


def test_gate_passes_the_clean_repo():
    r = _gate()
    assert r.returncode == 0, r.stdout + r.stderr


# --- the real cleanup path emits ---

def test_harness_reap_emits_the_notice():
    src = read("templates/headless_harness.py")
    assert "CLEANUP-NOTICE" in src, "the harness reaps a process group but emits no cleanup notice"
    # the notice sits with the real reap, naming the owned-via proof (process group / recorded owner).
    assert re.search(r"owned-via", src), "the harness notice names no ownership proof"


# --- wiring + spec ---

def test_gate_wired_into_pre_push():
    pre_push = read("guardrails/pre-push")
    assert "check-cleanup-notice.sh" in pre_push, "pre-push does not wire the cleanup-notice gate"


def test_spec_states_the_law():
    spec = read("PRODUCT_SPEC.md")
    assert "[INV-204]" in spec
    assert "| INV-204 |" in spec
