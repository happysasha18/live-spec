#!/usr/bin/env python3
"""check-listener-tripwire.py — the tripwire for the day the harness ships a listener (SPEC INV-231, ROADMAP 405).

The dormant socket plumbing — messagingSocketPath, the uds client, the local-session recipient kind —
is built and switched off in the harness, and a private HTTP broker daemon is not worth building to
bridge a few crossings a day. So the addressed-push channel waits on the harness itself shipping a
listener. Row 405 is a DEFERRED row carrying a mechanical revisit trigger: a session record in
`claude agents --json` (or the session registry) showing a NON-EMPTY socket field, re-scanned at every
queue-take under INV-129's existing habit. This script is the one-shot check that reads that field.

FIELD-GATED. It fires ONLY when a real session record actually carries a socket field — today's harness
ships none, so on a real machine it stays quiet. It never simulates a fired state as real; a test drives
a FIXTURE record through `LIVE_SPEC_AGENTS_JSON` so the mechanism is exercisable without waiting on the
harness. When it fires, it returns non-zero and prints a `TRIGGER-FIRED` line, so the queue-take that
runs it returns row 405 to the runnable head [INV-129]; the firing is the signal that the addressed-push
work is now buildable.

WHERE IT LIVES. It rides the queue-take scan and the suite, NOT the push chain: it takes no gate letter,
the way the far-tier report-shape check does [INV-222] — the trigger is a queue-cadence read, not a
committed file a push gate would scan.

PARKED 2026-08-18 in `guardrails/attic/`. It reds only on a session record carrying a socket field, and
no harness has ever shipped a listener, so the condition it watches for has never once occurred. It is
parked, not dropped: `guardrails/route_agent_transport.py` still loads it from here for the one home of
the socket-field truth, and the day a listener ships it moves back with one `git mv`.
"""
import json
import os
import subprocess
import sys

# The field the harness would carry when it ships a listener, under whatever name it lands with. Any
# one non-empty is the fire.
SOCKET_FIELDS = ("socket", "messagingSocketPath", "socketPath", "messaging_socket_path")


def find_listeners(records):
    """The pure core: session records carrying a non-empty socket field.

    `records` is a list of session-record dicts (from `claude agents --json` or the session registry).
    A record with any known socket field set to a non-empty string is a listener; an absent or empty
    (or whitespace-only) field is not. Returns the firing records, each annotated with `_fired_field`
    and `_fired_value`.
    """
    out = []
    for rec in records or []:
        if not isinstance(rec, dict):
            continue
        for f in SOCKET_FIELDS:
            v = rec.get(f)
            if isinstance(v, str) and v.strip():
                r = dict(rec)
                r["_fired_field"] = f
                r["_fired_value"] = v
                out.append(r)
                break
    return out


def _read_records():
    """The session records, from a fixture via LIVE_SPEC_AGENTS_JSON, else from `claude agents --json`.

    A test injects records through the env so the tripwire is exercisable without the harness. Live, it
    reads the harness's own listing; a listing that does not parse or a missing command yields an empty
    set, which never fires — the honest quiet of a machine whose harness ships no listener yet.
    """
    injected = os.environ.get("LIVE_SPEC_AGENTS_JSON")
    if injected is not None:
        try:
            data = json.loads(injected)
        except ValueError:
            return []
    else:
        try:
            res = subprocess.run(["claude", "agents", "--json"],
                                 capture_output=True, text=True, check=False)
            data = json.loads(res.stdout) if res.stdout.strip() else []
        except (OSError, ValueError):
            return []
    # A registry may wrap the records under a key rather than hand back a bare list.
    if isinstance(data, dict):
        for k in ("sessions", "agents", "records"):
            if isinstance(data.get(k), list):
                data = data[k]
                break
        else:
            data = [data]
    return data if isinstance(data, list) else []


def run(records, out=None):
    """Fire (return 1, print TRIGGER-FIRED) on any non-empty socket field; stay silent (return 0)
    otherwise. Never blocks anything — the return code is the queue-take's signal, not a gate verdict."""
    if out is None:
        out = sys.stdout
    fired = find_listeners(records)
    if fired:
        out.write("TRIGGER-FIRED listener-tripwire: %d session record(s) carry a non-empty socket "
                  "field — the harness has shipped a listener, so ROADMAP 405 (addressed push under the "
                  "standing transport law) returns to the runnable head (SPEC INV-231, INV-129).\n"
                  % len(fired))
        for r in fired:
            out.write("  %s=%s\n" % (r["_fired_field"], r["_fired_value"]))
        out.flush()
        return 1
    out.write("OK (listener-tripwire): no session record carries a socket field — the harness ships no "
              "listener yet, so ROADMAP 405 stays deferred (SPEC INV-231).\n")
    out.flush()
    return 0


def main():
    return run(_read_records())


if __name__ == "__main__":
    sys.exit(main())
