"""A finished worker leaves no runaway child that burns unseen (SPEC INV-213, ROADMAP 420 candidate 4).

When a worker or task the run spawned COMPLETES, a descendant it left behind can keep burning a full
core unnoticed — the difflib process that burned one core for forty-six minutes after its worker
reported done, masked by a frozen status line (memory 2026-07-17). The run owns that descendant, so
the run answers for it. At a stopping point the run REPORTS a runaway descendant it provably owns:
what it is, how much CPU it holds, and why the run owns it — the notice word Alexander gave
2026-07-17 ~16:58, the same word that ordered row 417's cleanup notice.

This lives in process space, where a coarse scope does real harm — a broad kill once closed the
owner's real browser (SPEC INV-162). So the check names a runaway ONLY by PROVABLE OWNERSHIP: a
process in the run's OWN process group, or under the run's own temp tree — never by a program name.
It is a NOTICE-first mechanism: it REPORTS through the shared cleanup-notice module and ends nothing.

The tests drive a SIMULATED process table — no runaway is ever spawned on the real machine.
"""
import importlib.util
import json
import os
import subprocess

from conftest import ROOT, read

CHECK = os.path.join(ROOT, "guardrails", "check-runaway-child.py")
HELPER = os.path.join(ROOT, "guardrails", "cleanup_notice.py")


def _load():
    assert os.path.isfile(CHECK), "guardrails/check-runaway-child.py missing"
    spec = importlib.util.spec_from_file_location("check_runaway_child", CHECK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _proc(pid, ppid, pgid, pcpu, command="python", path=None):
    return {"pid": pid, "ppid": ppid, "pgid": pgid, "pcpu": pcpu,
            "command": command, "path": path}


# The run owns process group 500; the lead of that group (pid 500) is alive.
OWNED_PGIDS = {500}
LEAD = _proc(500, 1, 500, 0.1, "claude")


# --- the mechanism ships and reuses the cleanup-notice module ---

def test_notice_helper_emits_a_runaway_line():
    # the shared cleanup-notice module carries the runaway report shape: WHAT it is, how much CPU,
    # and the proof the run owns it. Report-only — it names no ended identity.
    r = subprocess.run(
        ["python3", "-c",
         "import sys; sys.path.insert(0, %r); import cleanup_notice as c; "
         "c.runaway_notice('python difflib (an orphaned worker child)', '99.4', "
         "'pgid=500 (this run own process group)')" % os.path.dirname(HELPER)],
        capture_output=True, text=True)
    out = r.stdout + r.stderr
    assert "RUNAWAY-NOTICE" in out, out
    assert "python difflib" in out
    assert "99.4" in out
    assert "pgid=500" in out


def test_check_reports_through_the_cleanup_notice_module():
    # the check reuses the shared module (row 417), it does not mint a second notice home.
    assert "cleanup_notice" in read("guardrails/check-runaway-child.py")


# --- the ownership discipline (INV-162): only what the run provably owns ---

def test_owned_orphaned_burning_is_reported():
    mod = _load()
    burner = _proc(777, 1, 500, 98.0, "python", "/usr/bin/python3")   # pgid owned, orphaned, burning
    got = mod.find_runaways([LEAD, burner], OWNED_PGIDS)
    assert [p["pid"] for p in got] == [777], got
    assert "pgid=500" in got[0]["owned_via"]


def test_live_owned_working_child_is_not_reported():
    # a child in the owned group whose PARENT IS ALIVE is a live worker at work, never a runaway.
    mod = _load()
    parent = _proc(600, 500, 500, 0.2, "worker")
    working = _proc(777, 600, 500, 97.0, "python")   # owned + burning, but parent 600 is alive
    got = mod.find_runaways([LEAD, parent, working], OWNED_PGIDS)
    assert got == [], got


def test_below_threshold_is_not_reported():
    mod = _load()
    idle = _proc(777, 1, 500, 3.0, "python")   # owned + orphaned, but not burning
    got = mod.find_runaways([LEAD, idle], OWNED_PGIDS)
    assert got == [], got


def test_bare_name_match_never_fires():
    # THE core safety proof: a process whose COMMAND matches a known burner ("difflib"), orphaned and
    # burning a full core, but in a foreign process group and under no owned tree, is NEVER targeted.
    # The run cannot prove it owns it, so a name match alone must not fire — the browser-kill lesson.
    mod = _load()
    foreign = _proc(9001, 1, 42, 99.9, "python difflib", "/Users/someone/other/difflib.py")
    got = mod.find_runaways([LEAD, foreign], OWNED_PGIDS)
    assert got == [], "a bare-name match with no ownership proof fired — INV-162 breach: %r" % got


def test_ownership_by_owned_tree_path(tmp_path):
    # the second ownership proof: a process running from UNDER the run's own temp tree is owned even
    # when its process group differs — the run launched it into its own tree.
    mod = _load()
    owned_tree = str(tmp_path)
    child_path = os.path.join(owned_tree, "checkpoints", "worker.py")
    burner = _proc(9002, 1, 42, 96.0, "python", child_path)   # foreign pgid, but under owned tree
    got = mod.find_runaways([LEAD, burner], OWNED_PGIDS, owned_tree=owned_tree)
    assert [p["pid"] for p in got] == [9002], got
    assert owned_tree in got[0]["owned_via"]


def test_a_process_outside_the_owned_tree_is_not_owned(tmp_path):
    mod = _load()
    owned_tree = str(tmp_path)
    outside = _proc(9003, 1, 42, 96.0, "python", "/tmp/elsewhere/worker.py")
    got = mod.find_runaways([LEAD, outside], OWNED_PGIDS, owned_tree=owned_tree)
    assert got == [], got


def test_self_pids_are_excluded():
    # the hook itself and the lead of the group are never reported as runaways of themselves.
    mod = _load()
    hook = _proc(555, 1, 500, 80.0, "check-runaway-child")   # owned, orphaned, burning, but is self
    got = mod.find_runaways([LEAD, hook], OWNED_PGIDS, self_pids={555})
    assert got == [], got


def test_orphaned_by_missing_parent_is_owned_and_reported():
    # orphaned means the owning parent is no longer alive: a ppid that is not in the live table (the
    # worker that spawned it has ended) counts as orphaned even when it is not reparented to init.
    mod = _load()
    burner = _proc(778, 4242, 500, 95.0, "python")   # ppid 4242 is absent from the table
    got = mod.find_runaways([LEAD, burner], OWNED_PGIDS)
    assert [p["pid"] for p in got] == [778], got


# --- report-only: the mechanism emits the notice and ends nothing ---

def test_run_emits_a_notice_for_a_runaway_and_returns_zero():
    mod = _load()
    burner = _proc(777, 1, 500, 98.0, "python", "/usr/bin/python3")
    import io
    buf = io.StringIO()
    code = mod.run([LEAD, burner], OWNED_PGIDS, out=buf)
    out = buf.getvalue()
    assert "RUNAWAY-NOTICE" in out, out
    assert code == 0, "a notice must never block the stop"


def test_the_check_source_ends_no_process():
    # report-only by construction: the source carries no kill / terminate of any process.
    src = read("guardrails/check-runaway-child.py")
    for verb in ("killpg", "pkill", "killall", ".terminate(", ".kill("):
        assert verb not in src, "the report-only check must end no process, found %r" % verb


def test_cli_injected_table_reports_and_exits_zero(tmp_path):
    # the subprocess path, driven with a SIMULATED table via env — never the real process list.
    procs = [dict(LEAD), _proc(777, 1, 500, 98.0, "python", "/usr/bin/python3")]
    env = dict(os.environ,
               LIVE_SPEC_RUNAWAY_PROCS_JSON=json.dumps(procs),
               LIVE_SPEC_OWNED_PGIDS="500")
    r = subprocess.run(["python3", CHECK], capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "RUNAWAY-NOTICE" in (r.stdout + r.stderr)


def test_cli_clean_table_is_silent_and_exits_zero():
    procs = [dict(LEAD)]
    env = dict(os.environ,
               LIVE_SPEC_RUNAWAY_PROCS_JSON=json.dumps(procs),
               LIVE_SPEC_OWNED_PGIDS="500")
    r = subprocess.run(["python3", CHECK], capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "RUNAWAY-NOTICE" not in (r.stdout + r.stderr)


# --- the wiring decision: a Stop-time notice, NOT a pre-push gate ---

def test_not_wired_as_a_prepush_gate():
    # candidate 4 lives at the Stop surface, not the push gate — a push gate runs long after the
    # runaway would have burned its cores. So it takes no pre-push letter and is absent from pre-push.
    assert "check-runaway-child" not in read("guardrails/pre-push")


def test_not_a_ci_step():
    assert "runaway-child" not in read(".github/workflows/gates.yml")


# --- spec / architecture / matrix carry the law ---

def test_spec_states_the_law():
    spec = read("PRODUCT_SPEC.md")
    assert "[INV-213]" in spec
    assert "| INV-213 |" in spec


def test_architecture_owns_the_invariant():
    assert "INV-213" in read("ARCHITECTURE.md")


def test_matrix_row_covers_the_law():
    assert "INV-213" in read("TEST_MATRIX.md")
