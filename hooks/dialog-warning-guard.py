#!/usr/bin/env python3
"""PreToolUse(Bash): warn before a command known to raise a macOS security dialog (PLAN q-581).

The owner's own words, deposit 2026-08-07: twice in one session a step raised a keychain dialog on
his screen — a deploy script reading a Cloudflare key with `security find-generic-password`, and
four launches of a Chrome binary the machine had never run — and he interrupted the work both times
and said he always presses Deny. The session never sees the dialog itself: the OS call blocks a
foreign process or returns an empty secret, so the only channel that ever reported it was him
interrupting. A second case folded into the same row 2026-08-28 (PLAN q-542): a server bound to
every network interface makes macOS ask about incoming connections the moment the socket binds, not
only once it is left running afterward.

THE RULE (stated once, here, and nowhere else in this tree — grep proves it):

    Before running a command that can raise a macOS security dialog, name the dialog in one line
    and let the human decide whether it should run.

THE LIST beside it, so a new case is one entry added to KNOWN_DIALOG_COMMANDS below, not a second
document to keep in step with this one. Each entry names the dialog it raises and the finding that
put it on the list. This stays a flat list, on purpose (PLAN q-581): no stale-process reaper, no
general command registry — one pattern, one dialog, one source, per row.

Contract: reads a PreToolUse(Bash) event on stdin (`{"tool_name": "Bash", "tool_input":
{"command": ...}}`), and where the command matches a known dialog-raising shape, writes a
`permissionDecision: "ask"` hook decision — the human sees the reason and decides before the shell
ever runs the command — then exits 0. An ordinary command matching nothing on the list prints
nothing and exits 0, same as the command never having been seen. Malformed or foreign-tool input
exits 0 silently, the same stand-down-on-its-own-breakage contract `worker-restore-guard.py` uses:
a hook that cannot read its input is not evidence that the command is safe, but it is also not this
hook's place to invent a verdict from nothing.

Repo home: hooks/dialog-warning-guard.py; installed copy (once a host wires it, the way
`scripts/install-worker-restore-guard.sh` wires its neighbour): ~/.claude/hooks/.
"""
import json
import re
import sys

RULE = "Before running a command that can raise a macOS security dialog, name the dialog in one line and let the human decide whether it should run."  # noqa: E501

# The flat list. Every entry: a NAME, a compiled PATTERN matched against the whole command text, the
# DIALOG it raises in plain words, an EXAMPLE command it must catch, and the SOURCE that put it here.
# Adding a case is adding one entry — no other file changes.
KNOWN_DIALOG_COMMANDS = [
    {
        "name": "keychain-read",
        "pattern": re.compile(r"\bsecurity\s+find-(generic|internet)-password\b"),
        "dialog": "a keychain access prompt",
        "example": "security find-generic-password -s cloudflare-deploy-key -w",
        "source": "deposit 2026-08-07 — scripts/deploy-lab.sh reading a Cloudflare key this way",
    },
    {
        "name": "unrun-browser-binary",
        "pattern": re.compile(
            r"(Google Chrome(?: for Testing)?\.app/Contents/MacOS/Google Chrome(?: for Testing)?"
            r"|chrome-headless-shell(?:[^/\s]*)?\s*(?:--|$))"
        ),
        "dialog": "a Gatekeeper first-run prompt",
        "example": '"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new',
        "source": "deposit 2026-08-07 — four launches of a Chrome binary new to the machine",
    },
    {
        "name": "server-bound-to-every-interface",
        "pattern": re.compile(r"--bind[= ]0\.0\.0\.0|--host[= ]0\.0\.0\.0|\b0\.0\.0\.0:\d+"),
        "dialog": "a firewall incoming-connections prompt",
        "source": "PLAN q-542, folded into q-581 2026-08-28 — a server left listening on every "
                  "interface asked for approval repeatedly; binding one raises the same ask",
        "example": "python3 -m http.server 8080 --bind 0.0.0.0",
    },
]


def find_dialog_command(command):
    """The first entry whose pattern matches `command`, or None."""
    for entry in KNOWN_DIALOG_COMMANDS:
        if entry["pattern"].search(command):
            return entry
    return None


def warn_payload(entry, command):
    reason = (
        "dialog-warning-guard: `%s` can raise %s (%s). %s Run it only once the human has said so."
        % (command, entry["dialog"], entry["source"], RULE)
    )
    return {"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason,
    }}


def main():
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except ValueError:
        return 0
    if payload.get("tool_name") not in (None, "Bash"):
        return 0
    command = (payload.get("tool_input") or {}).get("command")
    if not isinstance(command, str) or not command.strip():
        return 0
    entry = find_dialog_command(command)
    if entry:
        print(json.dumps(warn_payload(entry, command)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
