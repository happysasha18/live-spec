# -*- coding: utf-8 -*-
"""The lean-orchestrator arm warns a session that hoards raw file content inline (SPEC INV-246).

The lean-orchestrator law [profile proactivity, orchestration-law family, conduct-law.md] asks the
seat to delegate reads and drafts by default — the heavy reading lands in a worker's own context, not
the orchestrator's. The rule stood with no machine, so orchestrator context kept leaking. This arm is
that machine: a Stop-hook SOFT signal that measures the raw file content the seat holds INLINE across
the SESSION (large Read / file-dump results in its own main-thread turns) and warns past a threshold
when NO Agent/Task dispatch accompanies the reading.

Modeled on the hedge scan [INV-238] for its Stop-hook shape — a block+suppressOutput decision that
talks to the model, an optional personal overlay a host tunes, a silent stand-down on its own
breakage. It parts from its text-scanning siblings in WHAT it reads: not the last reply's prose but the
whole session's ACTION TRACE (the JOURNAL 2026-07-08 lesson — a Stop hook reads only the last message
by default, so a per-turn text scan never sees content hoarded across a long agentic turn). It reuses
the conduct judge's transcript-reading mechanism [INV-241]: tool_use / tool_result events, main-thread
only (a sidechain read is the worker's own context, never counted).

Red-first: before hooks/lean-orchestrator-scan.py exists, this module fails to load it — that is the red.
"""
import importlib.util
import json
import os
import subprocess

from conftest import ROOT, read as _read

HOOKS = os.path.join(ROOT, "hooks")
SCRIPT = os.path.join(HOOKS, "lean-orchestrator-scan.py")

KB = 1024


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


los = _load(SCRIPT, "lean_orchestrator_scan")


# ---- transcript builders --------------------------------------------------------------------------

def _asst(blocks, mid, sidechain=False):
    rec = {"type": "assistant", "message": {"role": "assistant", "id": mid, "content": blocks}}
    if sidechain:
        rec["isSidechain"] = True
    return rec


def _user_text(text, sidechain=False):
    rec = {"type": "user", "message": {"role": "user", "content": text}}
    if sidechain:
        rec["isSidechain"] = True
    return rec


def _tool_use(tuid, name, inp):
    return {"type": "tool_use", "id": tuid, "name": name, "input": inp}


def _tool_result(tuid, content, sidechain=False):
    rec = {"type": "user",
           "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tuid,
                                                     "content": content}]}}
    if sidechain:
        rec["isSidechain"] = True
    return rec


def _read_pair(tuid, mid, nbytes, sidechain=False):
    """An assistant Read call and the harness tool_result carrying nbytes of file content."""
    call = _asst([_tool_use(tuid, "Read", {"file_path": "/repo/f_%s.py" % tuid})], mid, sidechain)
    result = _tool_result(tuid, "x" * nbytes, sidechain)
    return [call, result]


def _bash_dump_pair(tuid, mid, nbytes, cmd="cat /repo/big.py"):
    call = _asst([_tool_use(tuid, "Bash", {"command": cmd})], mid)
    result = _tool_result(tuid, "y" * nbytes)
    return [call, result]


def _dispatch(tuid, mid):
    return _asst([_tool_use(tuid, "Agent", {"description": "draft the delta", "subagent_type": "claude"})], mid)


def _transcript(tmp_path, records):
    p = tmp_path / "t.jsonl"
    with open(p, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return str(p)


def _run(payload, env=None):
    run_env = dict(os.environ)
    if env:
        run_env.update(env)
    return subprocess.run(["python3", SCRIPT], input=json.dumps(payload),
                          capture_output=True, text=True, env=run_env)


def _stop(tp, active=False):
    return {"transcript_path": tp, "hook_event_name": "Stop", "stop_hook_active": active}


# ---- the measurable proxy: hoarding fires, lean stays silent (both directions) --------------------

def test_scan_counts_inline_read_bytes_and_dispatches(tmp_path):
    """scan_transcript returns the cumulative inline raw-content bytes and the dispatch count."""
    recs = [_user_text("go")]
    recs += _read_pair("a", "m1", 30 * KB)
    recs += _read_pair("b", "m2", 30 * KB)
    tp = _transcript(tmp_path, recs)
    inline, dispatches = los.scan_transcript(tp)
    assert inline >= 60 * KB
    assert dispatches == 0


def test_hoard_over_threshold_with_no_dispatch_fires(tmp_path):
    """A session holding raw file content past the threshold with ZERO dispatch warns (liveness)."""
    recs = [_user_text("read the whole tree yourself")]
    recs += _read_pair("a", "m1", 30 * KB)
    recs += _read_pair("b", "m2", 30 * KB)
    tp = _transcript(tmp_path, recs)
    r = _run(_stop(tp))
    assert r.returncode == 0
    decision = json.loads(r.stdout)
    assert decision["decision"] == "block"
    assert decision["suppressOutput"] is True
    assert "  · " in decision["reason"]  # one net-meter-countable hit line


def test_clean_lean_turn_stays_silent(tmp_path):
    """A lean turn — a few small inline reads under the threshold — never fires (safety)."""
    recs = [_user_text("what does this config say?")]
    recs += _read_pair("a", "m1", 3 * KB)
    recs += _read_pair("b", "m2", 2 * KB)
    tp = _transcript(tmp_path, recs)
    r = _run(_stop(tp))
    assert r.returncode == 0 and r.stdout.strip() == ""


def test_below_threshold_stays_silent(tmp_path):
    """A single legitimately moderate inline read under the threshold does not fire (safety)."""
    recs = [_user_text("go")] + _read_pair("a", "m1", 40 * KB)
    tp = _transcript(tmp_path, recs)
    r = _run(_stop(tp))
    assert r.stdout.strip() == ""


def test_a_dispatch_suppresses_the_warning(tmp_path):
    """Heavy inline reads WITH at least one worker dispatch stay silent — the seat is delegating."""
    recs = [_user_text("go")]
    recs += _read_pair("a", "m1", 40 * KB)
    recs += [_dispatch("d1", "m2")]
    recs += _read_pair("b", "m3", 40 * KB)
    tp = _transcript(tmp_path, recs)
    r = _run(_stop(tp))
    assert r.stdout.strip() == "", "a dispatched session is delegating; the arm steps aside"


def test_sidechain_reads_are_not_counted(tmp_path):
    """Raw file content read INSIDE a worker (a sidechain) is the worker's own context, never the
    orchestrator's — so it never counts toward the inline total."""
    recs = [_user_text("go")]
    recs += _read_pair("a", "m1", 80 * KB, sidechain=True)
    tp = _transcript(tmp_path, recs)
    inline, dispatches = los.scan_transcript(tp)
    assert inline == 0
    r = _run(_stop(tp))
    assert r.stdout.strip() == ""


def test_bash_file_dump_is_counted(tmp_path):
    """A file dumped via Bash (cat/head/tail) is inline raw content too — the net does not reward the
    escape hatch of reading files through the shell."""
    recs = [_user_text("go")]
    recs += _bash_dump_pair("a", "m1", 35 * KB, cmd="cat /repo/big.py")
    recs += _bash_dump_pair("b", "m2", 35 * KB, cmd="head -2000 /repo/other.py")
    tp = _transcript(tmp_path, recs)
    r = _run(_stop(tp))
    decision = json.loads(r.stdout)
    assert decision["decision"] == "block"


def test_non_dump_bash_is_not_counted(tmp_path):
    """A Bash result that is not a file dump (a build log, a test run) is not raw file content held
    inline, so a large such result alone never fires."""
    recs = [_user_text("go")]
    call = _asst([_tool_use("a", "Bash", {"command": "pytest -q"})], "m1")
    recs += [call, _tool_result("a", "z" * (80 * KB))]
    tp = _transcript(tmp_path, recs)
    inline, _ = los.scan_transcript(tp)
    assert inline == 0


def test_measures_across_the_session_not_the_last_message(tmp_path):
    """The JOURNAL 2026-07-08 lesson: a Stop hook reads only the last message by default. This arm
    measures content hoarded across EARLIER turns, so a clean final reply after a hoarding session
    still fires."""
    recs = [_user_text("go")]
    recs += _read_pair("a", "m1", 30 * KB)
    recs += [_asst([{"type": "text", "text": "One moment."}], "m2")]
    recs += [_user_text("continue")]
    recs += _read_pair("b", "m3", 30 * KB)
    recs += [_asst([{"type": "text", "text": "Done — all read."}], "mF")]
    tp = _transcript(tmp_path, recs)
    r = _run(_stop(tp))
    decision = json.loads(r.stdout)
    assert decision["decision"] == "block", "content across earlier turns is measured, not just the last"


def test_stop_hook_active_stands_down(tmp_path):
    """Never loop: a prior stop-hook already fired this turn stands the arm down."""
    recs = [_user_text("go")] + _read_pair("a", "m1", 80 * KB)
    tp = _transcript(tmp_path, recs)
    r = _run(_stop(tp, active=True))
    assert r.stdout.strip() == ""


def test_unreadable_transcript_stands_down(tmp_path):
    """A missing transcript is the arm's own breakage — it stands down silently, never a false fire."""
    r = _run(_stop(str(tmp_path / "nope.jsonl")))
    assert r.returncode == 0 and r.stdout.strip() == ""


def test_malformed_payload_stands_down():
    r = subprocess.run(["python3", SCRIPT], input="not json", capture_output=True, text=True)
    assert r.returncode == 0 and r.stdout.strip() == ""


# ---- the personal overlay (the tunable threshold) -------------------------------------------------

def test_personal_overlay_tunes_the_threshold(tmp_path, monkeypatch):
    """~/.claude/hooks/lean-orchestrator-personal.json tunes threshold_bytes; missing/malformed falls
    back to the built-in default silently (the hedge overlay contract)."""
    home = tmp_path / "home"
    (home / ".claude" / "hooks").mkdir(parents=True)
    overlay = home / ".claude" / "hooks" / "lean-orchestrator-personal.json"
    overlay.write_text(json.dumps({"threshold_bytes": 1000}), encoding="utf-8")
    monkeypatch.setenv("HOME", str(home))
    assert los.load_threshold() == 1000

    monkeypatch.setenv("HOME", str(tmp_path / "no-overlay-home"))
    assert los.load_threshold() == los.DEFAULT_THRESHOLD_BYTES

    bad = tmp_path / "bad-home"
    (bad / ".claude" / "hooks").mkdir(parents=True)
    (bad / ".claude" / "hooks" / "lean-orchestrator-personal.json").write_text("nope", encoding="utf-8")
    monkeypatch.setenv("HOME", str(bad))
    assert los.load_threshold() == los.DEFAULT_THRESHOLD_BYTES


def test_lowered_threshold_fires_on_a_small_read(tmp_path):
    """A host that lowers the threshold via the overlay fires earlier — the parameter is live."""
    home = tmp_path / "home"
    (home / ".claude" / "hooks").mkdir(parents=True)
    (home / ".claude" / "hooks" / "lean-orchestrator-personal.json").write_text(
        json.dumps({"threshold_bytes": 5000}), encoding="utf-8")
    recs = [_user_text("go")] + _read_pair("a", "m1", 8 * KB)
    tp = _transcript(tmp_path, recs)
    r = _run(_stop(tp), env={"HOME": str(home)})
    assert json.loads(r.stdout)["decision"] == "block"


# ---- wiring: judge classification -----------------------------------------------------------------

def test_classified_in_judge_hooks():
    """An opt-in orchestration-law net, classified in guardrails/judge-hooks.json the way the
    conduct-judge arms are — not wired into the pack's default settings.json, so gate v never demands
    it live. Every hooks/ file must be classified or check-judge-listed reds [INV-211]."""
    with open(os.path.join(ROOT, "guardrails", "judge-hooks.json")) as f:
        decl = json.load(f)
    assert "lean-orchestrator-scan" in decl.get("library", [])
    assert "lean-orchestrator-scan" not in decl.get("wired", {})


# ---- traceability: the law stands in every document it is owed in (SPEC INV-246) ------------------


def test_spec_states_the_law():
    spec = _read("PRODUCT_SPEC.md")
    assert "[INV-246]" in spec
    # the "Ships as `hooks/lean-orchestrator-scan.py`" sentence is gone from the compact rewrite;
    # the filename anchor now lives only in ARCHITECTURE.md (already checked by
    # test_architecture_owns_the_invariant below), so the spec check moves to the criterion text
    # that names the same duty.
    assert "cumulative inline raw file content across the session reaches the threshold" in spec
    assert "the worker-dispatch count is zero" in spec


def test_formal_index_row():
    spec = _read("PRODUCT_SPEC.md")
    assert "| INV-246 |" in spec
    # index now carries locations only (SPEC INV-271) — the "the lean-orchestrator arm:" prose
    # moves onto the body requirement heading that carries INV-246.
    assert "Two Stop-hook soft signals: the hedge gate and the lean-orchestrator arm" in spec


def test_architecture_owns_the_invariant():
    arch = _read("ARCHITECTURE.md")
    assert "INV-246" in arch
    assert "hooks/lean-orchestrator-scan.py:1" in arch


def test_matrix_row_covers_the_law():
    mat = _read("TEST_MATRIX.md")
    assert "| M-431 |" in mat and "INV-246" in mat
