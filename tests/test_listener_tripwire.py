"""A tripwire for the day the harness ships a listener (SPEC INV-231, ROADMAP 405).

The dormant socket plumbing — messagingSocketPath, the uds client, the local-session recipient kind —
is built and switched off in the harness, and a private HTTP broker is not worth building for a few
crossings a day. So row 405 is a DEFERRED row carrying a mechanical revisit trigger: a session record
in `claude agents --json` (or the session registry) showing a NON-EMPTY socket field, re-scanned at
every queue-take under INV-129's existing habit, plus the one-shot check script that reads it.

The tripwire is FIELD-GATED — it fires only when the harness actually ships a listener. The tests drive
FIXTURE session records through the env, never a real firing simulated as real; today's real machine
carries empty socket fields, so the tripwire stays quiet.
"""
import importlib.util
import json
import os
import subprocess

from conftest import ROOT, read

CHECK = os.path.join(ROOT, "guardrails", "attic", "check-listener-tripwire.py")


def _load():
    assert os.path.isfile(CHECK), "guardrails/attic/check-listener-tripwire.py missing"
    spec = importlib.util.spec_from_file_location("check_listener_tripwire", CHECK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- the pure core: a non-empty socket field fires, an empty one does not ---

def test_nonempty_socket_field_fires():
    mod = _load()
    records = [{"pid": 1, "socket": "/tmp/claude-messaging-1.sock"}]
    fired = mod.find_listeners(records)
    assert [r["pid"] for r in fired] == [1], fired


def test_empty_socket_field_does_not_fire():
    mod = _load()
    records = [{"pid": 1, "socket": ""}, {"pid": 2, "socket": "   "}, {"pid": 3}]
    assert mod.find_listeners(records) == []


def test_alternate_socket_field_names_fire():
    # the harness may name the field messagingSocketPath rather than socket.
    mod = _load()
    records = [{"pid": 7, "messagingSocketPath": "/tmp/m.sock"}]
    assert [r["pid"] for r in mod.find_listeners(records)] == [7]


# --- the one-shot check script: reds/fires on a firing fixture, silent on an empty one ---

def test_cli_fires_on_a_nonempty_socket_fixture():
    records = [{"pid": 1, "socket": "/tmp/claude-messaging-1.sock"}]
    env = dict(os.environ, LIVE_SPEC_AGENTS_JSON=json.dumps(records))
    r = subprocess.run(["python3", CHECK], capture_output=True, text=True, env=env)
    assert r.returncode != 0, "the tripwire did not fire on a non-empty socket field"
    assert "TRIGGER-FIRED" in (r.stdout + r.stderr)


def test_cli_silent_on_empty_socket_fixture():
    records = [{"pid": 1, "socket": ""}, {"pid": 2}]
    env = dict(os.environ, LIVE_SPEC_AGENTS_JSON=json.dumps(records))
    r = subprocess.run(["python3", CHECK], capture_output=True, text=True, env=env)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "TRIGGER-FIRED" not in (r.stdout + r.stderr)


def test_cli_accepts_a_registry_dict_shape():
    # a session registry may wrap the records under a key rather than a bare list.
    records = {"sessions": [{"pid": 1, "socket": "/tmp/x.sock"}]}
    env = dict(os.environ, LIVE_SPEC_AGENTS_JSON=json.dumps(records))
    r = subprocess.run(["python3", CHECK], capture_output=True, text=True, env=env)
    assert r.returncode != 0
    assert "TRIGGER-FIRED" in (r.stdout + r.stderr)


# --- the wiring decision: a queue-take / suite check, NOT a pre-push gate ---

def test_not_wired_as_a_prepush_gate():
    assert "check-listener-tripwire" not in read("guardrails/pre-push")


def test_not_a_ci_step():
    assert "listener-tripwire" not in read(".github/workflows/gates.yml")


# --- spec / architecture / matrix carry the law ---

def test_spec_states_the_law():
    spec = read("PRODUCT_SPEC.md")
    # the tag always rides grouped with sibling codes now, never solo
    assert "INV-231" in spec
    assert "| INV-231 |" in spec


def test_architecture_owns_the_invariant():
    assert "INV-231" in read("ARCHITECTURE.md")


def test_matrix_row_covers_the_law():
    assert "INV-231" in read("TEST_MATRIX.md")


# --- the row stays deferred with its mechanical trigger (INV-129), distinct from far (INV-222) ---

def test_roadmap_row_405_carries_the_trigger():
    # Row 405's queue home moved into PLAN.md's Tasks section on 2026-08-27 (task q-405); the
    # ROADMAP.md body was emptied the same day. Read wherever the live task list actually is.
    plan = read("PLAN.md")
    assert "check-listener-tripwire" in plan
