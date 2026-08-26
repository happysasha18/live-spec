"""Every point of contact with the person has a kind, and the kind decides what may be said there
(SPEC INV-205, ROADMAP 413).

The frame this row states is the HOME four scattered rows were missing — the waiting list [408], the
parked question with its default taken [409], the release note's offer of next steps [402], and the far
tier's rare self-surfacing [403]. Each names a touchpoint and its kind under one frame:

  * SYNCHRONOUS — the person is present and the work waits on him (a live question, a decision page he is
    looking at now). It affords an interruption, a wait, and a teaching line.
  * ASYNCHRONOUS — he reads on his own clock while the work rolls (a status line, the resume file, an
    inbox note, the waiting list he opens on request). It never affords an interruption; it affords a
    teaching line only where the person OPENS it himself.

The machine: each touchpoint declares its kind in a small manifest (`guardrails/touchpoints.json`), and
the gate (`guardrails/check-touchpoint-kind.py`) reds a surface that speaks in a kind its touchpoint
lacks — an interruption raised from an asynchronous point, or a teaching line on a point the person did
not open. A genuine touchpoint passes quiet.
"""
import json
import os
import subprocess

from conftest import ROOT, read

MANIFEST = os.path.join(ROOT, "guardrails", "touchpoints.json")
GATE = os.path.join(ROOT, "guardrails", "check-touchpoint-kind.py")
FIXTURES = os.path.join(ROOT, "guardrails", "touchpoint-fixtures")


def _gate(*args):
    return subprocess.run(["python3", GATE, *args], capture_output=True, text=True)


def _fix(name):
    return os.path.join(FIXTURES, name)


# --- the declaration manifest ---

def test_manifest_is_well_formed():
    data = json.loads(read("guardrails/touchpoints.json"))
    entries = data["touchpoints"] if isinstance(data, dict) else data
    seen = set()
    for e in entries:
        assert e["name"] not in seen, "duplicate touchpoint name %r" % e["name"]
        seen.add(e["name"])
        assert e["kind"] in ("synchronous", "asynchronous"), e
        assert e["opened_by"] in ("person", "agent"), e


def test_manifest_declares_the_four_instances():
    data = json.loads(read("guardrails/touchpoints.json"))
    entries = data["touchpoints"] if isinstance(data, dict) else data
    by_name = {e["name"]: e for e in entries}
    # 408 — the waiting list: an asynchronous point the person opens on request.
    assert by_name["waiting-list"]["kind"] == "asynchronous"
    assert by_name["waiting-list"]["opened_by"] == "person"
    # 409 — the parked feedback question: rides the waiting list, asynchronous, person-opened.
    assert by_name["parked-feedback-question"]["kind"] == "asynchronous"
    assert by_name["parked-feedback-question"]["opened_by"] == "person"
    # 402 — the release note offer: a human-audience, no-answer-needed changelog he reads on his clock.
    assert by_name["release-note"]["kind"] == "asynchronous"
    assert by_name["release-note"]["opened_by"] == "person"
    # 403 — the far tier's rare self-surfacing: rides the status report, pushed at him.
    assert by_name["far-tier-surfacing"]["kind"] == "asynchronous"
    assert by_name["far-tier-surfacing"]["opened_by"] == "agent"


def test_manifest_names_each_instance_row():
    # each instance entry cites the roadmap row it grounds, so the frame is traceable to its four rows.
    data = json.loads(read("guardrails/touchpoints.json"))
    entries = data["touchpoints"] if isinstance(data, dict) else data
    by_name = {e["name"]: e for e in entries}
    for name, row in (("waiting-list", "408"), ("parked-feedback-question", "409"),
                      ("release-note", "402"), ("far-tier-surfacing", "403")):
        assert row in str(by_name[name].get("row", "")), (name, row)


# --- the gate reds a surface speaking in a kind its touchpoint lacks ---

def test_gate_reds_an_interruption_from_an_asynchronous_point():
    # RED-FIRST: a far-tier surfacing (asynchronous, agent-pushed) that raises an interruption.
    r = _gate(_fix("async-interrupt.txt"))
    assert r.returncode != 0, "gate passed an interruption raised from an asynchronous point"
    assert "INV-205" in (r.stdout + r.stderr)
    assert "interrupt" in (r.stdout + r.stderr).lower()


def test_gate_reds_a_teaching_line_on_a_point_the_person_did_not_open():
    # RED-FIRST: an asynchronous, agent-pushed point carrying a teaching line.
    r = _gate(_fix("async-teach-unopened.txt"))
    assert r.returncode != 0, "gate passed a teaching line on a point the person did not open"
    assert "INV-205" in (r.stdout + r.stderr)


def test_gate_passes_a_wait_line_on_an_asynchronous_point():
    # a genuine asynchronous touchpoint carrying only waiting traffic passes quiet.
    r = _gate(_fix("async-wait-quiet.txt"))
    assert r.returncode == 0, r.stdout + r.stderr


def test_gate_passes_an_interruption_on_a_synchronous_point():
    # a synchronous point affords an interruption — the person is present and the work waits on him.
    r = _gate(_fix("sync-interrupt-ok.txt"))
    assert r.returncode == 0, r.stdout + r.stderr


def test_gate_passes_a_teaching_line_on_a_point_the_person_opens():
    # the waiting list is opened on request, so a teaching line on it is afforded.
    r = _gate(_fix("opened-teach-ok.txt"))
    assert r.returncode == 0, r.stdout + r.stderr


def test_gate_passes_the_clean_repo():
    # push mode: the manifest is well-formed and no real declared surface speaks an unafforded kind.
    r = _gate()
    assert r.returncode == 0, r.stdout + r.stderr


def test_gate_reds_a_malformed_manifest(tmp_path):
    bad = tmp_path / "touchpoints.json"
    bad.write_text(json.dumps({"touchpoints": [
        {"name": "x", "kind": "whenever", "opened_by": "person", "surface": None}]}))
    r = _gate("--manifest", str(bad))
    assert r.returncode != 0, "gate passed a manifest with an invalid kind"


def test_gate_wired_into_pre_push():
    pre_push = read("guardrails/pre-push")
    assert "check-touchpoint-kind.py" in pre_push, "pre-push does not wire the touchpoint-kind gate"


# --- the frame in the spec, the index, the architecture, the matrix ---

def test_spec_states_the_law():
    spec = read("PRODUCT_SPEC.md")
    assert "INV-205" in spec
    # the frame names both kinds and what each licenses.
    assert "synchronous" in spec.lower() and "asynchronous" in spec.lower()


def test_formal_index_row():
    spec = read("PRODUCT_SPEC.md")
    assert "| INV-205 |" in spec


def test_architecture_owns_the_invariant():
    arch = read("ARCHITECTURE.md")
    assert "INV-205" in arch


def test_matrix_row_covers_the_law():
    matrix = read("TEST_MATRIX.md")
    assert "INV-205" in matrix
