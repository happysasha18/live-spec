#!/usr/bin/env python3
"""Stop-hook: warn a session that hoards raw file content inline without dispatching a worker (SPEC INV-246).

The lean-orchestrator law asks the seat to delegate reads and drafts by default — the heavy reading lands
in a worker's own context, not the orchestrator's, so the orchestrator's window stays lean. It is one of
the standing orchestration laws (conduct-law.md), and it stood with no mechanical net, so orchestrator
context kept leaking [profile proactivity, the lean-orchestrator rule]. This arm is that net: a SOFT signal
that measures the raw file content the seat holds INLINE across the SESSION and warns past a threshold when
no worker dispatch accompanies the reading.

WHAT IT MEASURES — inline raw file content, held without a dispatch:
  - INLINE RAW FILE CONTENT is the byte size of the tool_result content for a file-dump call the seat made
    in its OWN main-thread turn: a Read (always a file dump), or a Bash file-dump command (cat / head /
    tail / less / more / sed reading a file). A read made INSIDE a worker is recorded on a sidechain, which
    is the worker's own context — never the orchestrator's — so a sidechain result is never counted.
  - A DISPATCH is an Agent or Task tool_use in the main thread: the seat handing a unit of work to a
    worker. When the seat dispatches, the reading it delegated lands in the worker's context, off the
    orchestrator's window.
  - The arm reads the WHOLE SESSION transcript, not just the last assistant message. A Stop hook reads only
    the last message by default (JOURNAL 2026-07-08), so a per-turn text scan never sees content hoarded
    across a long agentic turn; the leak this net catches lives in the accumulated action trace, so it
    reuses the conduct judge's transcript-reading mechanism [INV-241] and sums across every turn.

THE SIGNAL fires (a block+suppressOutput Stop decision, the soft-signal shape the hedge scan carries
[INV-238]) when cumulative inline raw content is at or over the threshold AND the dispatch count is zero.
The dispatch-count-zero gate is the honest false-positive floor: a session that spawned even one worker is
demonstrably delegating, so the soft signal steps aside rather than second-guess the mix — the same
conservative stance the retired answer-first arm took [INV-220]. It catches the pure-hoard case the rule actually
names (the seat does all the reading itself and never dispatches) and is honest that a mixed session slips
by, the way the hedge scan's literal net trails the class [INV-203]. The net naturally CLEARS the moment the
seat dispatches its first worker.

THRESHOLD — a tunable parameter, not a law [SPEC INV-70]. The default is 50 KB of cumulative inline raw
content (~600-800 lines): well past a glance or a single small config read, the point where the seat has
clearly pulled substantial raw material into its own window that a worker should have held. A host tunes it
through an optional overlay `~/.claude/hooks/lean-orchestrator-personal.json`, a JSON object with a
`threshold_bytes` integer, owned by the personal layer; this file never creates or edits that overlay.
Missing or malformed overlay falls back to the built-in default, silently (the hedge overlay contract
[INV-238]).

OFF BY DEFAULT, opt-in. Like the conduct judge [INV-241] and the rest of the orchestration-law family, this
net ships classified in `guardrails/judge-hooks.json` but is NOT wired into the pack's default settings.json
— a host turns it on by adding it to their own Stop array. Not every host runs a delegating orchestrator, so
it is the host's to enable. Its runs and fires are read by the net-meter [INV-202] rather than trusted.

It NEVER blocks on its own breakage: an unreadable payload or transcript stands it down silently, never a
false fire. Repo home: hooks/lean-orchestrator-scan.py; installed copy: ~/.claude/hooks/.
"""
import json
import os
import re
import sys

# The cumulative inline raw-content ceiling, in bytes, above which a dispatch-free session warns. A tunable
# proxy threshold [SPEC INV-70], not a law — ~50 KB, well past a glance or a single small read.
#
# The tunable claim is true and the override is real: load_threshold() below reads `threshold_bytes`
# from ~/.claude/hooks/lean-orchestrator-personal.json. The MAGNITUDE has no source — INV-70 says only
# that this is "a tunable parameter, not a law" and never argues for 50 KB, and the 2026-08-07 census
# (row 81) found no trace. It warns and never blocks, which is what keeps a wrong value cheap.
DEFAULT_THRESHOLD_BYTES = 50 * 1024

# A Bash command that dumps a file's raw content inline, the same way a Read does. The seat is discouraged
# from reading files through the shell (cat/head/tail); this catches those six literal verbs. It is a
# FIRST cheap net, not the whole class: a dump through grep/awk/nl/cut/python, a shell loop, or an env
# prefix (`LC_ALL=C cat f`) is not matched and escapes, the way the hedge scan's literal list trails one
# escape behind the next phrasing [INV-203]. The main net is Read; this arm only keeps the plainest shell
# dumps from being a free pass.
_DUMP_BASH = re.compile(r"^\s*(cat|head|tail|less|more|sed)\b")

# The tool_use names that dispatch a unit of work to a worker — the reading they delegate lands off the
# orchestrator's own window.
_DISPATCH_NAMES = {"Agent", "Task"}


def load_threshold():
    """PERSONAL overlay: ~/.claude/hooks/lean-orchestrator-personal.json, a JSON object carrying a
    `threshold_bytes` integer, owned by the personal layer. Missing or malformed -> the built-in default,
    silently (the hedge overlay contract)."""
    path = os.path.expanduser("~/.claude/hooks/lean-orchestrator-personal.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return DEFAULT_THRESHOLD_BYTES
    if not isinstance(data, dict):
        return DEFAULT_THRESHOLD_BYTES
    n = data.get("threshold_bytes")
    if isinstance(n, bool) or not isinstance(n, int) or n <= 0:
        return DEFAULT_THRESHOLD_BYTES
    return n


def _is_dump_call(name, inp):
    """True when a tool_use reads raw file content inline: a Read, or a Bash file-dump command."""
    if name == "Read":
        return True
    if name == "Bash" and isinstance(inp, dict):
        cmd = inp.get("command", "")
        return isinstance(cmd, str) and bool(_DUMP_BASH.match(cmd))
    return False


def _byte_len(s):
    """The UTF-8 byte length of a string, so the total is honest bytes for non-ASCII content too."""
    return len(s.encode("utf-8", "replace"))


def _result_len(block):
    """The byte length of a tool_result's content, whether a plain string or a list of text parts."""
    content = block.get("content", "")
    if isinstance(content, str):
        return _byte_len(content)
    if isinstance(content, list):
        total = 0
        for part in content:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                total += _byte_len(part["text"])
            elif isinstance(part, str):
                total += _byte_len(part)
        return total
    return 0


def scan_transcript(path):
    """Walk the WHOLE session transcript and return (inline_raw_bytes, dispatch_count), main thread only.

    A sidechain record is a worker's own context, skipped entirely. A dump call's tool_use_id is remembered,
    and the matching tool_result's content length is added to the inline total; an Agent/Task tool_use adds
    to the dispatch count.
    """
    if not path or not os.path.exists(path):
        return (0, 0)
    try:
        with open(path, encoding="utf-8") as f:
            records = []
            for line in f:
                try:
                    records.append(json.loads(line))
                except ValueError:
                    continue
    except OSError:
        return (0, 0)

    dump_ids = set()
    dispatches = 0
    inline = 0

    for rec in records:
        if rec.get("isSidechain"):
            continue
        rtype = rec.get("type")
        content = rec.get("message", {}).get("content", [])
        if not isinstance(content, list):
            continue
        if rtype == "assistant":
            for b in content:
                if not isinstance(b, dict) or b.get("type") != "tool_use":
                    continue
                name = b.get("name", "")
                if name in _DISPATCH_NAMES:
                    dispatches += 1
                elif _is_dump_call(name, b.get("input", {})):
                    tuid = b.get("id")
                    if tuid:
                        dump_ids.add(tuid)
        elif rtype == "user":
            for b in content:
                if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("tool_use_id") in dump_ids:
                    inline += _result_len(b)

    return (inline, dispatches)


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        sys.exit(0)
    # never loop: if a prior stop-hook already fired this turn, stand down.
    if payload.get("stop_hook_active"):
        sys.exit(0)
    inline, dispatches = scan_transcript(payload.get("transcript_path", ""))
    threshold = load_threshold()
    if inline < threshold or dispatches > 0:
        sys.exit(0)
    kb = inline / 1024.0
    reason = (
        "LEAN-ORCHESTRATOR CHECK — this session holds raw file content inline with no worker dispatch:\n"
        "  · ~%.0f KB of raw Read / file-dump content sits in your own main-thread turns, and no "
        "Agent/Task dispatch accompanies it.\n\n"
        "The lean-orchestrator law asks the seat to delegate reads and drafts by default — the heavy "
        "reading belongs in a worker's own context, off this window. From the next unit of work, dispatch "
        "the reading to a worker (the Agent tool) and keep the seat lean; hand it a precise brief and take "
        "back the conclusion, not the raw file dumps. If this session genuinely owed a large orchestrator "
        "read — a spec it must hold to coordinate — say so in one line and continue; a dispatch on the next "
        "unit clears this notice." % kb
    )
    # suppressOutput keeps the machine's complaint off the human's screen: the hook talks to the model, and
    # what the human is owed is the leaner behaviour the model then holds (as the hedge scan does).
    print(json.dumps({"decision": "block", "reason": reason, "suppressOutput": True}))
    sys.exit(0)


if __name__ == "__main__":
    main()
