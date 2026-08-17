#!/usr/bin/env python3
"""route_agent_transport.py — which transport carries a message between two agents (SPEC INV-236, ROADMAP 396).

INV-183's transport sentence was written on a refused premise: that git is the universal transport
for all inter-agent traffic and co-location only a fast path. The owner refused it 2026-07-17. The
cut runs by the traffic's KIND, not by where the two agents sit:

- A message needing no timely answer — a durable record a neighbour reads on its own clock, or a
  notification — travels by the STORE: the sender deposits one new file and the receiver sweeps it
  later, reachable while the receiver is not running and committed-and-pushed when the sender is
  remote [INV-112]. This road works today; the remote-deposit arm landed [ROADMAP 247].

- A conversation — a back-and-forth needing a live peer that answers in turn — needs a DIRECT
  CHANNEL, and the harness has not shipped one: the socket plumbing is built and switched off, no
  listener has shipped, so two local sessions have no live direct channel today.

The conversation road's availability is FIELD-GATED on the same machine-fact the listener tripwire
reads [INV-231]: a session record carrying a non-empty socket field is a listener. Today's
listenerless harness leaves the direct channel unavailable. The availability is read from the
session records, never hardcoded, so the day a listener ships the road flips to available on its
own — that day being row 405's mechanical tripwire.

WHERE IT LIVES. Like the listener tripwire, this rides the suite and takes NO push-gate letter: a
router is a stated routing rule a test exercises, not a committed file a push gate scans [INV-83].
"""
import importlib.util
import os

_HERE = os.path.dirname(os.path.abspath(__file__))

# The traffic kinds. A conversation needs a live peer answering in turn; a no-answer message needs
# no timely reply — a durable record or a notification the receiver reads on its own clock.
_CONVERSATION_KINDS = ("conversation", "dialogue", "live-exchange")
_NO_ANSWER_KINDS = ("record", "notification", "deposit", "no-answer")


def _listener_module():
    """The listener tripwire's single source of the socket-field truth, loaded by path.

    Reusing it keeps ONE home for what counts as a shipped listener [INV-194], so the router and
    the tripwire never drift on the machine-fact they both read. The tripwire moved to
    `guardrails/attic/` on 2026-08-18; the router still reads it there, so the one home holds.
    """
    path = os.path.join(_HERE, "attic", "check-listener-tripwire.py")
    spec = importlib.util.spec_from_file_location("check_listener_tripwire", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def classify(message):
    """The message's traffic kind: 'conversation', 'no-answer', or None when it declares neither.

    A message declares its kind through a `kind` field (a conversation, or a no-answer
    record/notification) or a `needs_answer` boolean. A message stating neither is unclassified;
    the router refuses it rather than guessing [INV-4].
    """
    if not isinstance(message, dict):
        return None
    kind = message.get("kind")
    if kind in _CONVERSATION_KINDS:
        return "conversation"
    if kind in _NO_ANSWER_KINDS:
        return "no-answer"
    na = message.get("needs_answer")
    if na is True:
        return "conversation"
    if na is False:
        return "no-answer"
    return None


def direct_channel_available(records=None):
    """Whether a live direct channel stands between two local sessions right now.

    Read from the machine [INV-231], never assumed: a session record carrying a non-empty socket
    field is a listener. `records` is a list of session-record dicts (a test injects fixtures);
    None reads the real listing through the tripwire's own reader. No listener, no channel.
    """
    lm = _listener_module()
    recs = records if records is not None else lm._read_records()
    return len(lm.find_listeners(recs)) > 0


def route(message, records=None):
    """Route a message to the transport its traffic kind takes.

    Returns a dict naming the traffic kind, the road, and whether that road is available today. A
    no-answer message takes the store road, available now [INV-112, ROADMAP 247]. A conversation
    takes the direct channel, whose availability is read from the machine [INV-231]; while no
    listener has shipped the road is unavailable and the result names the listener it waits on. An
    unclassified message raises ValueError rather than a guessed route [INV-4].
    """
    kind = classify(message)
    if kind is None:
        raise ValueError(
            "a message states its traffic kind: a conversation, or a no-answer record/notification"
        )
    if kind == "no-answer":
        return {
            "traffic_kind": "no-answer",
            "road": "store",
            "transport": "git-store",
            "available": True,
            "why": "a durable deposit the receiver sweeps later, reachable while it is not "
                   "running, committed and pushed when remote [INV-112, ROADMAP 247]",
        }
    available = direct_channel_available(records)
    result = {
        "traffic_kind": "conversation",
        "road": "direct-channel",
        "available": available,
    }
    if not available:
        result["waits_on"] = "the harness shipping a listener [INV-231, ROADMAP 405]"
    return result


if __name__ == "__main__":
    # Exercisable by hand: route a fixture message from LIVE_SPEC_TRANSPORT_MESSAGE, reading the
    # real listener listing for the conversation road's availability.
    import json
    import sys

    raw = os.environ.get("LIVE_SPEC_TRANSPORT_MESSAGE", "{}")
    try:
        msg = json.loads(raw)
    except ValueError:
        print("route_agent_transport: LIVE_SPEC_TRANSPORT_MESSAGE is not JSON", file=sys.stderr)
        sys.exit(2)
    try:
        print(json.dumps(route(msg)))
    except ValueError as e:
        print(f"route_agent_transport: {e}", file=sys.stderr)
        sys.exit(2)
