#!/usr/bin/env python3
"""register_judge_core.py — the register judge's one mechanism (ROADMAP rows 416+418, SPEC INV-203).

A register law that names a CLASS is held by a model that reads meaning; a list of literal patterns
holds only the instances someone already thought of, so each escape earns one more pattern while the
next word walks through and a human ends up working as the regular expression. This module is the judge
that holds the class, in ONE place. It hands the outgoing text plus the law to the cheapest sufficient
tier [SPEC INV-69] and takes back the sentences that carry no information or leak register.

The law TEXT is no longer written here. It is stated once in guardrails/language-rules.json and rendered
into hooks/language-laws.json by scripts/gen-language-consumers.py, keyed by the checker that runs each
law and the surface it runs on; this module reads the body it holds from the artifact installed beside
it. A rule edited in that one home reaches both readers below at once, and the gate
guardrails/check-language-rules.py reds an artifact that has drifted from it.

Two surfaces share this mechanism, each handing it its OWN law:
  - the chat hook (register-judge.py) — the three chat laws, universal + personal (SPEC INV-173);
  - the shown-document lint (scripts/preshow-register-lint.py) — the machine-dialect / register law.
The literal list stays the free first pass on each surface; this judge is what the law actually rests
on. The list grows by nobody's duty — the judge holds what a list cannot.

It NEVER blocks on its own breakage. No binary on PATH, a timeout, a non-zero exit, or a shape it
cannot read stands the judge down and returns an error string in place of a verdict — a guard that reds
when its own machinery breaks trains the guarded to route around it. Its runs and fires are read by the
net-meter [SPEC INV-202], never trusted; it retires by the owner's standing word when it stops firing.

Repo home: hooks/register_judge_core.py; installed copy: ~/.claude/hooks/ (beside register-judge.py).
"""
import json
import os
import re
import subprocess

DEFAULT_MODEL = os.environ.get("REGISTER_JUDGE_MODEL", "claude-haiku-4-5-20251001")
DEFAULT_TIMEOUT_S = float(os.environ.get("REGISTER_JUDGE_TIMEOUT", "25"))

# A quote shorter than this floor is a hallucination guard: a real offence is a sentence or a bounded
# span of one, never a lone word like "the" that happens to sit in the text. The model is asked to quote
# a bounded VERBATIM span (the offending sentence's first QUOTE_SPAN_CHARS) rather than truncate with an
# ellipsis, so a genuine long offence is matched by its verbatim prefix instead of being dropped.
MIN_QUOTE_CHARS = 12
QUOTE_SPAN_CHARS = 80

# The FRAME is the universal mechanism: how to judge and the exact answer shape. The LAW BODY is handed
# in per surface. Keeping the frame here and the law outside is what lets one mechanism serve two laws.
_PROLOGUE = """You are a register judge for {surface}. Judge the TEXT below against the laws stated here.
Each law names a CLASS, so judge by MEANING rather than by matching particular words.

{law_body}

Return STRICT JSON, nothing else, no prose, no code fence:
{{"offences": [{{"quote": "<the offending sentence copied VERBATIM from the text; if it runs longer than
80 characters, copy only its first 80 characters exactly as written — no ellipsis, no added quotation
marks, no changed punctuation, so the quote is always an exact span of the text>",
"law": <the law number>, "why": "<at most 12 words: what it carries no information toward>"}}]}}

An empty list is the right answer for a clean text, and it is the answer most texts deserve. Judge only
what the text asserts. Ignore file paths, code, command output, and any text the author is QUOTING
rather than asserting.

TEXT:
"""

# ---- Where the law text comes from -----------------------------------------------------------------
# The laws live in guardrails/language-rules.json and are rendered into hooks/language-laws.json by
# scripts/gen-language-consumers.py. That artifact is installed beside this module (~/.claude/hooks/), so
# the same read works from the repo and from the installed copy. Each body is keyed by the checker that
# runs the law and the surface it runs on, so this module takes the laws it holds and no others; a law
# whose home is the reader's personal layer is filtered out here and supplied at run time by
# load_personal_law().
LAWS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "language-laws.json")
CHAT_CHECKER = "hooks/register-judge.py"
DOCUMENT_CHECKER = "scripts/preshow-register-lint.py"
NO_LAW_TEXT = ("no law text: hooks/language-laws.json is missing or unreadable beside the judge "
               "(rebuild it with scripts/gen-language-consumers.py)")


def load_law_body(checker, surface, path=None):
    """The law body one checker holds on one surface, read from the generated artifact.

    A missing, unreadable, or unexpectedly shaped artifact returns "" and the judge stands down on it
    with NO_LAW_TEXT, the same way load_personal_law() degrades to universal-only: a guard that raises
    on its own machinery breaking is a guard the guarded route around."""
    try:
        with open(path or LAWS_PATH, encoding="utf-8") as fh:
            laws = json.load(fh)["bodies"][checker][surface]["laws"]
        return "\n\n".join(law["text"] for law in laws if not law.get("personal_home"))
    except (OSError, ValueError, KeyError, TypeError):
        return ""


# ---- The UNIVERSAL chat law (SPEC INV-173: a pack law every host inherits; ships here) --------------
UNIVERSAL_CHAT_LAW = load_law_body(CHAT_CHECKER, "chat")

# ---- The DOCUMENT register law (ships with preshow-register-lint.py; universal to every host) -------
DOCUMENT_REGISTER_LAW = load_law_body(DOCUMENT_CHECKER, "human-prose")


def renumber_laws(text):
    """Renumber every `LAW N —` marker sequentially from 1, in order of appearance.

    The universal law and the personal overlay are each numbered from their own base, so concatenating
    them collides (universal LAW 1..2, personal LAW 2..3 give two LAW 2s). The judge cites a law by its
    number, so a duplicate number mis-attributes an offence. Renumbering the joined text keeps the numbers
    a single sequence whatever each block started at, so a personal overlay may number from any base."""
    counter = [0]

    def repl(_m):
        counter[0] += 1
        return "LAW %d —" % counter[0]

    return re.sub(r"LAW\s+\d+\s+[—-]", repl, text)


def load_personal_law(path=None):
    """The PERSONAL law overlay (SPEC INV-173): plain law text the personal layer owns, appended after the
    universal law. Missing or unreadable -> universal-only, silently. The pack ships nobody's personal rules."""
    if path is None:
        path = os.path.expanduser("~/.claude/hooks/register-judge-personal.md")
    try:
        with open(path, encoding="utf-8") as fh:
            body = fh.read().strip()
    except OSError:
        return ""
    return body


def build_prompt(text, law_body, surface):
    return _PROLOGUE.format(surface=surface, law_body=law_body.strip()) + text


def judge(text, law_body, surface="one person's working chat", model=None, timeout=None):
    """Ask the model against the given law. Returns (offences, error).

    error set means the judge stood down (no verdict). offences is a list of dicts, each already proven to
    quote the text verbatim — a hallucinated quote is no evidence and is dropped.
    """
    model = model or DEFAULT_MODEL
    timeout = DEFAULT_TIMEOUT_S if timeout is None else timeout
    if not (law_body or "").strip():
        return [], NO_LAW_TEXT
    prompt = build_prompt(text, law_body, surface)
    try:
        proc = subprocess.run(
            # No --bare: it strips the environment the launch needs and reports the run as logged out
            # (probed 2026-07-17). --tools "" keeps the judge from acting.
            ["claude", "-p", "--model", model, "--tools", ""],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        return [], "no claude binary on PATH"
    except subprocess.TimeoutExpired:
        return [], "judge timed out at %gs" % timeout
    if proc.returncode != 0:
        return [], "judge exited %d: %s" % (proc.returncode, proc.stderr.strip()[:120])
    return parse_offences(proc.stdout, text)


def _normalize_quote(q):
    """Strip artifacts the model adds around a quote — surrounding quotation marks and a trailing ellipsis
    it appends when it truncates a long sentence — so the verbatim span underneath can be matched."""
    q = (q or "").strip()
    q = q.strip("\"'“”‘’«»").strip()
    for tail in ("…", "..."):
        while q.endswith(tail):
            q = q[: -len(tail)].strip()
    return q


def matched_span(quote, text, floor=MIN_QUOTE_CHARS):
    """The verbatim span of `quote` present in `text`, or "" if none reaches the floor.

    A whole-quote substring wins. Otherwise the longest LEADING prefix that is verbatim in the text is
    matched, so a genuine long offence the model truncated (or ellipsized past the quote cap) is still
    caught by its verbatim prefix rather than silently dropped. A span below the floor is treated as a
    hallucination guard and rejected."""
    q = _normalize_quote(quote)
    if len(q) < floor:
        return ""
    if q in text:
        return q
    lo, hi, best = floor, len(q), ""
    while lo <= hi:
        mid = (lo + hi) // 2
        if q[:mid] in text:
            best = q[:mid]
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def parse_offences(raw, text):
    """Parse the model's answer into (offences, error). Kept apart from the model call so a test can drive
    it against canned responses without a live binary."""
    out = (raw or "").strip()
    if out.startswith("```"):
        out = out.strip("`").split("\n", 1)[-1].rsplit("```", 1)[0]
    try:
        parsed = json.loads(out)
    except ValueError:
        return [], "judge answered in no readable shape: %s" % out[:120]
    offences = parsed.get("offences") if isinstance(parsed, dict) else None
    if not isinstance(offences, list):
        return [], "judge answered without an offences list"
    # Only an offence quoting the text itself is real, and a trivially short quote is no evidence; a
    # hallucinated or below-floor quote is dropped, a truncated long quote recovered to its verbatim span.
    kept = []
    for o in offences:
        if not isinstance(o, dict):
            continue
        span = matched_span(o.get("quote", ""), text)
        if span:
            o = dict(o)
            o["quote"] = span
            kept.append(o)
    return kept, None


def block_reason(offences, header="REGISTER JUDGE"):
    """The block message shown to the model, listing each offence with its law and why."""
    lines = "\n".join(
        "  · %s\n      [law %s] %s" % (o.get("quote", ""), o.get("law", "?"), o.get("why", ""))
        for o in offences[:5]
    )
    return (
        header + " — the text carries lines that add no information:\n"
        + lines
        + "\n\nRestate each as a plain positive sentence carrying its fact, and send the correction now. "
        "If one of them genuinely informs, say which and why in one line and continue."
    )
