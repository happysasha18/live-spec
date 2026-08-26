"""Which transport carries a message between two agents is decided by the traffic's kind
(SPEC INV-236, ROADMAP 396).

INV-183's transport sentence was written on a refused premise: that git is the universal
transport for all inter-agent traffic and co-location only a fast path. The owner refused it
2026-07-17 — the cut runs by the traffic's KIND. A message needing no timely answer (a durable
record a neighbour reads on its own clock, or a notification) travels by the store: one file the
sender deposits and the receiver sweeps later, reachable while the receiver is not running, the
road that works today [ROADMAP 247]. A conversation — a back-and-forth needing a live peer that
answers in turn — needs a direct channel, and the harness has not shipped one: the socket
plumbing is built and switched off, no listener has shipped [INV-231], so two local sessions have
no live direct channel today.

The router's availability read for the conversation road is FIELD-GATED on the same machine-fact
the listener tripwire reads [INV-231]: a session record carrying a non-empty socket field is a
listener, and today's listenerless harness leaves the direct channel unavailable. The tests drive
FIXTURE records through the router, never a live listener simulated as real; the road's
availability is read from the records rather than hardcoded, so a fixture listener flips it to
available — the proof it is machine-read.
"""
import importlib.util
import json
import os
import subprocess

from conftest import ROOT, read

MODULE = os.path.join(ROOT, "guardrails", "route_agent_transport.py")


def _load():
    assert os.path.isfile(MODULE), "guardrails/route_agent_transport.py missing"
    spec = importlib.util.spec_from_file_location("route_agent_transport", MODULE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- a no-answer message takes the git store road, available today ---

def test_no_answer_message_takes_the_store_road():
    mod = _load()
    for msg in ({"kind": "record"}, {"kind": "notification"}, {"needs_answer": False}):
        r = mod.route(msg)
        assert r["traffic_kind"] == "no-answer", r
        assert r["road"] == "store", r


def test_store_road_is_available_today():
    mod = _load()
    r = mod.route({"kind": "record"})
    assert r["available"] is True, r


# --- a conversation is routed to the direct channel, unavailable today ---

def test_conversation_takes_the_direct_channel():
    mod = _load()
    for msg in ({"kind": "conversation"}, {"needs_answer": True}):
        r = mod.route(msg, records=[])
        assert r["traffic_kind"] == "conversation", r
        assert r["road"] == "direct-channel", r


def test_conversation_road_is_unavailable_today():
    # no session record carries a socket field, so the harness ships no listener.
    mod = _load()
    r = mod.route({"kind": "conversation"}, records=[])
    assert r["available"] is False, r


def test_conversation_road_names_the_listener():
    mod = _load()
    r = mod.route({"kind": "conversation"}, records=[])
    assert "INV-231" in r.get("waits_on", ""), r


def test_conversation_available_when_a_listener_ships():
    # a fixture session record carrying a socket field flips the road to available —
    # the proof the availability is read from the machine, never hardcoded.
    mod = _load()
    records = [{"pid": 1, "socket": "/tmp/claude-messaging-1.sock"}]
    r = mod.route({"kind": "conversation"}, records=records)
    assert r["available"] is True, r
    assert "waits_on" not in r, r


# --- an unclassified message is refused, never guessed ---

def test_route_rejects_an_unclassified_message():
    mod = _load()
    for msg in ({}, {"kind": "mystery"}, "not-a-dict"):
        try:
            mod.route(msg)
        except ValueError:
            continue
        assert False, f"an unclassified message was not refused: {msg!r}"


# --- the wiring decision: a suite check, NOT a pre-push gate ---

def test_not_wired_as_a_prepush_gate():
    assert "route_agent_transport" not in read("guardrails/pre-push")


def test_not_a_ci_step():
    assert "route_agent_transport" not in read(".github/workflows/gates.yml")
    assert "route-agent-transport" not in read(".github/workflows/gates.yml")


# --- spec / index / architecture / matrix / roadmap carry the law ---

def test_spec_states_the_law():
    spec = read("PRODUCT_SPEC.md")
    assert "[INV-236]" in spec
    assert "| INV-236 |" in spec


def test_spec_corrects_inv183_transport_sentence():
    spec = read("PRODUCT_SPEC.md")
    # the refused-premise sentence is gone from INV-183's body.
    assert "changes the transport's speed and leaves the contract itself untouched" not in spec
    # and gone from its Formal-index row too — the index paraphrase drops "co-location is only a
    # fast path" (the refused premise) and "reaches the other through git alone" as the universal
    # transport claim; both index and body must agree on the traffic-kind cut.
    assert "co-location changes transport speed" not in spec
    assert "a remote agent reaches the other through git alone" not in spec
    # the corrected sentence states the traffic-kind cut and hands the detail to INV-236.
    assert "the traffic's kind picks the transport" in spec


def test_formal_index_row():
    assert "| INV-236 |" in read("PRODUCT_SPEC.md")


def test_architecture_owns_the_invariant():
    assert "INV-236" in read("ARCHITECTURE.md")
    assert "route_agent_transport" in read("ARCHITECTURE.md")


def test_matrix_row_covers_the_law():
    matrix = read("TEST_MATRIX.md")
    assert "INV-236" in matrix
    assert "M-417" in matrix


def test_roadmap_row_396_landed():
    # Read the UNION of the live queue and its archives: row 396 landed, so pre-conversion it stands in
    # ROADMAP.md's body and post-conversion its row moves to docs/queue-archive/*.md under the live-body
    # law (SPEC INV-276, ROADMAP row 480) — its later normalization or archiving cannot red this pin.
    import glob
    import os
    texts = [read("ROADMAP.md")]
    for path in sorted(glob.glob(os.path.join(ROOT, "docs", "queue-archive", "*.md"))):
        with open(path, encoding="utf-8") as f:
            texts.append(f.read())
    union = "\n".join(texts)
    assert "route_agent_transport" in union
    assert "LANDED" in union.upper()
