#!/usr/bin/env python3
"""PreToolUse hook: the seat's own narration is judged at the first boundary after it is written.

WHY THIS EVENT. A line written to the human between two tool calls named two queue rows by bare
number, with no plain-word naming of the wish, which the plain-language anchor law forbids, and
loan-translated the pack's internal word for an acceptance criterion, which the no-calques law forbids.
The sentence itself stands in this hook's red fixture and in the record of the day it happened.

The Stop-side scan (code-anchor-scan.py) does fire on that exact sentence, and it is installed and
wired. It stayed quiet because Stop arrives when the whole turn ends, and the human had read the line
many minutes before. The earliest boundary a hook can reach after a narration line is the next tool
call, which is the PreToolUse event. This scan sits there, so a correction reaches the human inside
the same turn.

WHAT IT READS. Every assistant message shown since the last human turn, through the shared reader
hooks/turn_reader.py — the same reader the Stop-side scans use.

WHAT IT JUDGES.
  1. Naked internal codes, through code-anchor-scan.py's own matcher, imported rather than copied, so
     the two arms can never drift into judging the same law differently.
  2. Calques — the pack's internal English vocabulary loan-translated into the working language and
     handed to the human as if it were his. The list is data, hooks/chat-calques.json, and each entry
     carries the plain industry word the reply owed the reader, which the deny quotes.

THE NO-LOOP RULE. The offending text stays in the transcript for the rest of the session, so a scan
that judged it afresh at every tool call would deny every later call in that session. A fragment is
reported ONCE: its hash lands in a per-session state file under $HOME/.claude/hooks/.midturn-chat/,
the same state home and per-session shape the register judge's verdict file already uses, and a
fragment already recorded there passes silently. Identity is the matched fragment itself, never its
surrounding context, so a fragment stays the same as the turn grows around it. A NEW offence later in
the same turn still denies.

WHERE IT STANDS DOWN, silently and with exit 0: an unreadable event payload, an unreadable or absent
transcript, a turn carrying no assistant text, and a state directory that cannot be written.

COST. It runs before every tool call, so its whole judgment is a regex pass over the turn text plus
one small state file. No model call, no network.

OUTPUT SHAPE. The documented PreToolUse deny (https://code.claude.com/docs/en/hooks): exit 0 with
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
"permissionDecisionReason": ...}} on stdout. The top-level decision/reason pair belongs to other
events and carries no meaning here.

HONEST BOUNDARY. This arm sees the text between tool calls. A turn whose narration line is followed by
no tool call at all is still the Stop arm's to catch, and there the correction arrives after the human
has read the line. It also reads shape rather than meaning: a sentence that names its wish in plain
but WRONG words passes the machine.

Repo home: hooks/midturn-chat-scan.py; installed copy: ~/.claude/hooks/ (beside code-anchor-scan.py).
"""
import hashlib
import importlib.util
import json
import os
import re
import sys

HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HOOK_DIR)
import turn_reader  # noqa: E402

CALQUES_PATH = os.path.join(HOOK_DIR, "chat-calques.json")
STATE_DIR = os.path.join(os.path.expanduser("~"), ".claude", "hooks", ".midturn-chat")
REPORTED_CAP = 500  # the tail kept per session; a turn never carries anywhere near this many


_CODE_ANCHOR = []  # loaded once per process; the module compiles its patterns at import


def _load_code_anchor():
    """code-anchor-scan.py carries a dash in its name, so it is loaded by path rather than imported by
    name. Its matcher is reused whole: one law, one set of patterns, two delivery points."""
    if not _CODE_ANCHOR:
        path = os.path.join(HOOK_DIR, "code-anchor-scan.py")
        spec = importlib.util.spec_from_file_location("code_anchor_scan", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _CODE_ANCHOR.append(module)
    return _CODE_ANCHOR[0]


_CALQUES_CACHE = {}  # path -> compiled list; loaded once per process, not once per call


def load_calques(path=CALQUES_PATH):
    """The calque list as data: each entry's pattern compiled, with the plain word it asks for and its
    cheap pre-filter keys. Compiled once per process and cached by path, since every call before this
    change re-parsed the JSON and re-compiled all fifteen patterns even though the list never changes
    within a single hook invocation."""
    if path in _CALQUES_CACHE:
        return _CALQUES_CACHE[path]
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return []
    out = []
    for entry in data.get("calques", []):
        try:
            rx = re.compile(entry["pattern"], re.IGNORECASE)
        except (re.error, KeyError):
            continue
        keys = entry.get("keys") or []
        if isinstance(keys, str):
            keys = [keys]
        keys = tuple(k.lower() for k in keys if k)
        out.append((entry.get("word", ""), rx, entry.get("say", ""), keys))
    _CALQUES_CACHE[path] = out
    return out


def read_turn(transcript_path):
    return turn_reader.turn_text(transcript_path)


def _quoted_spans_removed(text, anchor):
    """Text ABOUT a word, rather than a word addressed to the reader, carries no offence.

    A fenced block, an inline backtick span and a «quoted» or "quoted" span are the shapes the pack
    already uses to name a word it is discussing, and code-anchor-scan.py's own patterns for them are
    reused here. The correction this hook asks for quotes the calque and its replacement in exactly
    that shape, so the correction itself reads clean.

    The bracketed spans code-anchor-scan.py also strips are left standing: parentheses are the lawful
    resting place of an internal CODE, and a calque inside them is still handed to the reader as his
    own language.
    """
    text = anchor.FENCE.sub(" ", text)
    text = anchor.INLINE_CODE.sub(" ", text)
    return anchor.QUOTED.sub(" ", text)


def _readable_window(text, start, end, reach):
    """A context window cut back to whole words, so the correction quotes a readable fragment."""
    left = max(0, start - reach)
    right = min(len(text), end + reach)
    if left > 0:
        space = text.find(" ", left, start)
        if space != -1:
            left = space + 1
    if right < len(text):
        space = text.rfind(" ", end, right)
        if space != -1:
            right = space
    return text[left:right].replace("\n", " ").strip()


def judge(text, calques=None):
    """Every offence in the turn's text, as dicts carrying kind, fragment, context and replacement."""
    if not text:
        return []
    findings = []

    anchor = _load_code_anchor()
    for fragment, context in anchor.find_matches(text):
        findings.append({"kind": "code", "fragment": fragment, "context": context, "say": ""})

    if calques is None:
        calques = load_calques()
    live = _quoted_spans_removed(text, anchor)
    # The pre-filter: a plain substring test costs far less than a regex pass, so an entry with keys
    # only pays for its expensive pattern when at least one of its keys is present. An entry with no
    # keys (a missing or empty `keys` field) runs its pattern unconditionally, since a keyless entry has
    # given the scan no cheap signal to filter on — silently skipping it would let a live law go dark.
    low = live.lower()
    for word, rx, say, keys in calques:
        if keys and not any(k in low for k in keys):
            continue
        for m in rx.finditer(live):
            findings.append({
                "kind": "calque",
                "word": word,
                "fragment": m.group().strip(),
                "context": _readable_window(live, m.start(), m.end(), 60),
                "say": say,
            })
    return findings


def fingerprint(finding):
    """A fragment's identity: its own matched text, normalised. The surrounding context shifts as the
    turn grows, so it can carry no part of the identity."""
    core = " ".join(finding["fragment"].lower().split())
    return hashlib.sha1((finding["kind"] + "|" + core).encode("utf-8")).hexdigest()[:16]


def _state_path(session_id, state_dir=STATE_DIR):
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", session_id or "unknown")
    return os.path.join(state_dir, safe + ".json")


def read_reported(session_id, state_dir=STATE_DIR):
    try:
        with open(_state_path(session_id, state_dir), encoding="utf-8") as fh:
            return set(json.load(fh).get("reported", []))
    except (OSError, ValueError):
        return set()


def write_reported(session_id, reported, state_dir=STATE_DIR):
    """Record what has been reported. A state home that cannot be written stands the arm down rather
    than denying twice on the same fragment."""
    path = _state_path(session_id, state_dir)
    try:
        os.makedirs(state_dir, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"reported": list(reported)[-REPORTED_CAP:]}, fh)
        return True
    except OSError:
        return False


def build_reason(fresh):
    """The correction the seat reads: what was written, and the words it owed the reader instead."""
    lines = []
    for f in fresh[:6]:
        if f["kind"] == "code":
            lines.append("  · internal code with no plain-word naming — «%s» in: %s"
                         % (f["fragment"], f["context"]))
        else:
            lines.append("  · calque «%s», say «%s» — in: %s"
                         % (f["fragment"], f["say"], f["context"]))
    return (
        "MID-TURN CHAT CHECK — this narration line has already been shown to the human, and it carries "
        "text the pack's laws keep out of his reading:\n"
        + "\n".join(lines)
        + "\n\nA queue row number names nothing to a reader on its own, and a loan-translated internal "
        "word names nothing to him at all. Say the sentence again in plain words in the very next "
        "message, before anything else: name each wish in the product's own words with the code "
        "trailing in parentheses, and use the plain industry word quoted above in place of each calque. "
        "This tool call is denied so the correction reaches him inside this turn; make the call again "
        "straight after the correction."
    )


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        sys.exit(0)
    if not isinstance(payload, dict):
        sys.exit(0)

    text = read_turn(payload.get("transcript_path", ""))
    if not text:
        sys.exit(0)

    findings = judge(text)
    if not findings:
        sys.exit(0)

    session_id = payload.get("session_id", "unknown")
    already = read_reported(session_id)
    fresh = []
    seen = set()
    for f in findings:
        fp = fingerprint(f)
        if fp in already or fp in seen:
            continue
        seen.add(fp)
        fresh.append(f)
    if not fresh:
        sys.exit(0)

    if not write_reported(session_id, already | seen):
        sys.exit(0)

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": build_reason(fresh),
        }
    }, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except BaseException:
        # A check standing at the tool boundary must never stop the session's work: any failure of
        # its own leaves the tool call running (SPEC R295.7).
        sys.exit(0)
