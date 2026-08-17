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
  3. A count handed over with no method beside it (the owner's measurement law, 2026-07-29 12:08). A
     number stated to the human carries four things: why it is measured, what changes when it moves,
     its unit, and the method that produced it. Three of those are meaning. The fourth has a shape, and
     this arm reads for it. The law's prose home is the writing register, rule 17.

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

THE MEASUREMENT ARM'S OWN BOUNDARY. It catches one of the four parts, the method, and it catches that
part by shape. A paragraph carrying any command word or any backtick span satisfies it, even where that
command produced nothing of the number beside it. A number stated with no unit at all — "the reader
returned 15" — carries no counted noun, so this arm never sees it. Why the number is measured and what
changes when it moves are meaning, and a person or a reading model is what holds them.

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


# ---- The measurement arm's patterns ----------------------------------------------------------------
# A COUNT is a number standing directly in front of one of the counted nouns below, in either working
# language, so the noun names the unit. A percentage counts too, the sign being its own unit. The
# citation shape the code-anchor law owns is this one's mirror — there the naming word comes FIRST and
# the number second ("row 386") — so the two arms never judge one fragment twice.
#
# The nouns are the things this project MEASURES. An edit's own tally (a line, a byte, a file) stays
# out, since a working report of what was touched is no measurement handed over as a finding.
COUNTED_NOUNS = (
    "finding|stop|defect|error|failure|test|reading|pass|row|requirement|criteri|document|"
    "sentence|hit|warning|"
    # the same counted nouns when chat runs in Russian
    "находк|стоп|дефект|ошиб|провал|тест|чтени|проход|требовани|критери|документ|"  # user-language
    "предложени|замечани|пункт"  # user-language
)
COUNT = re.compile(
    r"(?<![\w.,:/-])\d+(?:[.,]\d+)?"      # the number, standing free of a date, a time or a path
    r"(?:\s*%%"                           # the percent sign, a unit of its own
    r"|\s+(?:[\w-]{1,15}\s+){0,2}"        # or up to two describing words in front of the noun
    r"(?:%s)\w*)" % COUNTED_NOUNS,
    re.IGNORECASE,
)
# The METHOD tokens: the shapes a reproducible procedure takes in this project's chat — a command or a
# path inside a backtick span, a script or record named by its extension, a command word, or a phrase
# naming the procedure that produced the number.
METHOD = re.compile(
    r"`[^`\n]+`"
    r"|\b[\w./-]+\.(?:py|sh|json|jsonl|md|log|txt|yml)\b"
    r"|\b(?:python3?|pytest|grep|rg|wc|git|jq|sed|awk|find|make|npm|node|curl)\b"
    r"|\b(?:measured|counted|produced|read|taken)\s+(?:by|with|from|off)\b"
    # user-language: the same procedure words when chat runs in Russian
    r"|измер\w+|посчита\w+|подсчита\w+|команд\w+|методом|скриптом|гейтом|по\s+записи",  # user-language
    re.IGNORECASE,
)
# A block opener: a list item carries its own point, so it opens a block of its own.
BULLET_LINE = re.compile(r"^\s*(?:[-*+]\s|\d+[.)]\s)")

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


def blocks(text):
    """The paragraphs a count is judged inside.

    A measurement is stated with its parts in one block of prose, so the block is the window: a count in
    one paragraph and a command three paragraphs later are two separate statements. A blank line closes
    a block, and a list item opens one, since a bullet carries its own point.
    """
    out, current = [], []
    for line in text.split("\n"):
        if not line.strip() or BULLET_LINE.match(line):
            if current:
                out.append("\n".join(current))
                current = []
        if line.strip():
            current.append(line)
    if current:
        out.append("\n".join(current))
    return out


def judge_measurements(text):
    """Every count in the text whose block names no method, as findings of kind `measure`.

    A fenced block is machine output rather than a sentence to the human, and a table row carries its
    own describing cell, so both stand outside this reading. A backtick span stays IN, since a quoted
    command is the commonest shape a method takes.
    """
    if not text:
        return []
    anchor = _load_code_anchor()
    live = anchor.FENCE.sub(" ", text)
    live = "\n".join(ln for ln in live.split("\n") if not ln.lstrip().startswith("|"))
    findings = []
    for block in blocks(live):
        if METHOD.search(block):
            continue
        m = COUNT.search(block)
        if not m:
            continue
        findings.append({
            "kind": "measure",
            "fragment": m.group().strip(),
            "context": _readable_window(block, m.start(), m.end(), 60),
            "say": "",
        })
    return findings


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

    findings.extend(judge_measurements(text))
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
        elif f["kind"] == "measure":
            lines.append("  · a count with no method beside it — «%s» in: %s"
                         % (f["fragment"], f["context"]))
        else:
            lines.append("  · calque «%s», say «%s» — in: %s"
                         % (f["fragment"], f["say"], f["context"]))
    tail = ""
    if any(f["kind"] in ("code", "calque") for f in fresh):
        tail += (
            "\n\nA queue row number names nothing to a reader on its own, and a loan-translated internal "
            "word names nothing to him at all. Say the sentence again in plain words in the very next "
            "message, before anything else: name each wish in the product's own words with the code "
            "trailing in parentheses, and use the plain industry word quoted above in place of each "
            "calque."
        )
    if any(f["kind"] == "measure" for f in fresh):
        tail += (
            "\n\nA number carries four things, and one of them is missing above: why it is measured "
            "(the decision it informs, or the question it answers), what changes when it moves, its "
            "unit, and the method that produced it. State the count again in the very next message "
            "with all four, naming the command or the procedure a reader runs to get the same number. "
            "The rule's home is the writing register, rule 17."
        )
    return (
        "MID-TURN CHAT CHECK — this narration line has already been shown to the human, and it carries "
        "text the pack's laws keep out of his reading:\n"
        + "\n".join(lines)
        + tail
        + "\n\nThis tool call is denied so the correction reaches him inside this turn; make the call "
        "again straight after the correction."
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
