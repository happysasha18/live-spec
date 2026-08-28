#!/usr/bin/env python3
"""preshow-register-lint.py — the mechanical register gate for anything SHOWN to a human (SPEC INV-83).

Why this exists, and how it differs from its neighbour preshow-lint.py:
  preshow-lint.py catches a human-facing line that OPENS with an internal handle (a spec code, a
  row/session number) — a placement tell. THIS lint catches a different disease on the same surface:
  the pack's machine dialect leaking into the words themselves — a coined internal metaphor shown raw
  ("the wish door", "work lean"), an English pack term loan-translated into Russian chat (a calque,
  «швы с соседями» for "seams with neighbours"), or a transliterated pack term («пайплайн»). The law
  it mechanizes is the profile's `language.no-calques` + `language.register`: Russian human-facing text
  NEVER loan-translates the pack's English doc terms, industry-standard words only, and internal
  coinages live in the DOCS only — never in a mockup, a report, a decision page, or a rendered artifact
  a new reader sees first. A caught leak is what «это бред» sounds like from the next user (2026-07-10).

  The two lints stay separate scripts on purpose; the senior decides any merge. Run BOTH at the
  pre-show gate.

What it can and cannot do (stated honestly, so no one over-trusts it):
  A PATTERN lint catches KNOWN coinages, KNOWN calques, and named term classes — the leaks already
  seen. It CANNOT judge a novel machine-flavoured abstraction it has never been shown ("everything
  comes up naturally when it first matters" is only caught because that exact leak was once folded in
  as a pattern). That residual — a fresh abstraction in the same machine register — is held by the
  REGISTER JUDGE (register_judge_core.py, SPEC INV-203): the same class-reading model the chat surface
  uses, pointed at the document a human reads. It hands the file's text and the document register law to
  the cheapest tier and takes back the sentences that leak the machine dialect, catching the class a
  fixed pattern list never could. This lint is the free first pass; the judge is the ceiling.

The list grows by NOBODY's duty (SPEC INV-83, retracted 2026-07-17). The old doctrine grew this list by
one per caught leak, per leak, forever — the pack's own head rule says a list is the wrong answer to a
class, and a growing list is still a list, always one escape behind the next word. The judge holds the
class; the list stays only as the free first pass for what it already happens to cover, and it earns no
new pattern by duty. A Russian fixture carrying this list's OWN listed coinages as calques passed it
clean when probed 2026-07-17 — the worked proof that the list cannot hold its own class.

Design rule that keeps the accepted reader docs green: a pattern is the SPECIFIC coined collocation,
never its ordinary constituent words. "station", "door", "lean", "full" are legitimate industry words
the reader docs use freely; only the coinages "pipeline station", "wish door", "work lean", "full
rigor" are flagged. Verified 2026-07-10: the nine accepted reader docs contain the constituent words
but none of the coinages.

Usage: preshow-register-lint.py FILE [FILE ...]      (or: cat text | preshow-register-lint.py -)
Exit 0 = clean · exit 1 = at least one pattern hit (printed with file, line, pattern id, source).
"""
import os
import re
import sys

# Each pattern: (id, language, compiled-regex, source-of-the-leak, date-folded-in).
# ALL patterns are case-insensitive; \w and \b are Unicode-aware in Python 3, so Cyrillic word
# boundaries work. A pattern is a SPECIFIC coinage/calque collocation, never a bare industry word.
_F = re.IGNORECASE | re.UNICODE

OFFENCES_SHOWN = 8   # display width for the judge's offence list; see the print loop for why
PATTERNS = [
    # ---- English: internal SETTING / MECHANISM names shown raw ---------------------------------
    # source: onboarding mockup jargon strip, «это бред» (2026-07-10 ~00:14)
    ("en-full-rigor", "en", re.compile(r"\bfull\s+rigou?r\b", _F),
     "onboarding mockup — internal setting name 'full rigor' shown raw", "2026-07-10"),
    ("en-work-lean", "en", re.compile(r"\bwork\s+lean\b", _F),
     "onboarding mockup — internal setting name 'work lean' shown raw", "2026-07-10"),
    # source: pack coinages that must live in docs only, never in a shown mockup/report
    ("en-pipeline-station", "en", re.compile(r"\bpipeline\s+stations?\b", _F),
     "pack coinage 'the pipeline station' shown raw to a reader", "2026-07-10"),
    ("en-wish-door", "en", re.compile(r"\bwish\s+doors?\b", _F),
     "pack coinage 'the wish door' shown raw to a reader", "2026-07-10"),
    # source: onboarding mockup — a machine-flavoured abstraction; folded in as the exact caught
    # phrases (the grows-by-one duty). NOTE: these two are ordinary English, not coinages; a stricter
    # reading leaves them to the clean-reader check. Kept here as tonight's caught leak; senior's call.
    ("en-comes-up-naturally", "en", re.compile(r"\bcomes?\s+up\s+naturally\b", _F),
     "onboarding mockup — 'comes up naturally' machine abstraction", "2026-07-10"),
    ("en-when-it-first-matters", "en", re.compile(r"\bwhen\s+it\s+first\s+matters\b", _F),
     "onboarding mockup — 'when it first matters' machine abstraction", "2026-07-10"),

    # ---- Russian: CALQUES of the pack's English coinages (loan-translations) --------------------
    # source: another window's chat, same disease class (2026-07-10)
    ("ru-shvy-s-sosedyami", "ru", re.compile(r"шв\w+\s+с\s+сосед\w+", _F),
     "chat calque «швы с соседями» ← 'seams with neighbours'", "2026-07-10"),
    ("ru-rabotniki-v-pole", "ru", re.compile(r"работник\w*\s+в\s+поле", _F),
     "chat calque «работники в поле» ← 'workers in the field'", "2026-07-10"),
    ("ru-smert-scheta", "ru", re.compile(r"смерт\w*\s+сч[её]т\w*", _F),
     "chat calque «смерть счёта» ← 'budget death'", "2026-07-10"),
    ("ru-styki-poverkhnostei", "ru", re.compile(r"стык\w*\s+поверхност\w+", _F),
     "chat calque «стыки поверхностей» ← 'surface seams'", "2026-07-10"),

    # ---- Russian: the known-bad calque list from the profile (language.no-calques) -------------
    # source: profile.md language.no-calques (2026-07-05 / 2026-07-07)
    ("ru-rastyazhki", "ru", re.compile(r"растяжк\w*", _F),
     "profile known-bad calque «растяжки» ← 'tripwires'", "2026-07-05"),
    ("ru-ta-zhe-semya", "ru", re.compile(r"(?<!\w)т[аяойеу]\w*\s+же\s+семь\w+", _F),
     "profile known-bad calque «та же семья» ← 'the same incident family'", "2026-07-05"),
    ("ru-posadka", "ru", re.compile(r"(?<!\w)посадк\w*", _F),
     "profile known-bad calque «посадка» ← 'landing'", "2026-07-05"),
    ("ru-uzel-vladelets", "ru", re.compile(r"уз(?:ел|л\w+)[-\s]владел\w+", _F),
     "profile known-bad coinage «узел-владелец» ← 'owner node'", "2026-07-07"),

    # ---- Russian: TRANSLITERATED pack terms (say the industry word or the mechanism instead) ---
    # source: profile.md language.no-calques — internal coinages transliterated read as machine-speak
    ("ru-payplayn", "ru", re.compile(r"(?<!\w)пайплайн\w*", _F),
     "transliterated pack term «пайплайн» ← 'pipeline'", "2026-07-07"),
    ("ru-vorker", "ru", re.compile(r"(?<!\w)воркер\w*", _F),
     "transliterated pack term «воркер» ← 'worker'", "2026-07-07"),
    ("ru-steyshn", "ru", re.compile(r"(?<!\w)стейшн\w*", _F),
     "transliterated pack term «стейшн» ← 'station'", "2026-07-07"),

    # ---- Self-certification of sincerity (SPEC INV-94) ------------------------------------------
    # source: the pack's own README certified itself twice in one day; his word 2026-07-10 ~13:53
    ("en-say-so-plainly", "en", re.compile(r"\bsay\s+so\s+plainly\b", _F),
     "self-certification 'we say so plainly' — the content carries the honesty", "2026-07-10"),
    ("en-honest-treatment", "en", re.compile(r"\bhonest\s+treatment\b", _F),
     "self-certification 'deserves the same honest treatment'", "2026-07-10"),
    ("en-unsoftened", "en", re.compile(r"\bunsoftened\b", _F),
     "self-certification 'published unsoftened' — say what it IS (in full)", "2026-07-10"),
    ("ru-iz-chestnogo", "ru", re.compile(r"(?<!\w)из\s+честного", _F),
     "self-certification «из честного» — as if the rest were otherwise", "2026-07-10"),
    ("ru-chestno-govorya", "ru", re.compile(r"(?<!\w)честно\s+говоря", _F),
     "self-certification «честно говоря»", "2026-07-10"),
    ("ru-ne-po-pamyati", "ru", re.compile(r"(?<!\w)не\s+по\s+памяти", _F),
     "self-certification of diligence «проверил не по памяти» — state the source, drop the label", "2026-07-10"),
]

# Comment example, deliberately NOT a pattern: a bare unevidenced claim like
#   "How setup feels — almost no questions"
# is a register/evidence problem a phrase-pattern cannot judge (nothing lexical to match). It belongs
# to the clean-reader check and the evidence/no-bare-claim gate, not here.


# ---- Reproduced source (SPEC INV-83, the lint's reach) ---------------------------------------
# A comparison page sets an original document beside its rewrite so a reader can judge the change by
# eye. The original's own coinages appear on that page BY DESIGN — they are the thing under review,
# and a page that hid them would show a lie. Read line by line, this lint charged the page for words
# it was quoting, so the pages that matter most could never be shown (caught 2026-08-04 on the
# comparison pages for profile.md and communicator/SKILL.md).
#
# A page marks each region it reproduces verbatim from another document with a fence, and this lint
# reads what is inside as quotation. Everything the page states in its OWN words stays under the full
# check, which is the whole point: the fence narrows the reach to text the page did not write.
#
# The fence fails closed. An opening marker with no closing one exempts NOTHING and the file is
# checked whole, so a broken page never buys silence.
_QUOTED_OPEN = re.compile(r"<!--\s*register-lint:quoted-source\s*-->")
_QUOTED_REGION = re.compile(
    r"<!--\s*register-lint:quoted-source\s*-->.*?<!--\s*register-lint:/quoted-source\s*-->",
    re.DOTALL)


def mask_quoted_source(text):
    """Blank every closed quoted-source region, keeping every line number intact.

    Returns the text unchanged when the file carries no fence, and when any opening marker is left
    unclosed. Line numbers survive because each region is replaced by its own newlines, so a hit
    reported after masking still points at the real line of the real file.
    """
    if "register-lint:quoted-source" not in text:
        return text
    masked = _QUOTED_REGION.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    if _QUOTED_OPEN.search(masked):
        return text
    return masked


_PARAGRAPH_MARK = "¶"  # non-whitespace, non-word: breaks \s+ AND keeps \b working, so a match can
                       # never cross it, unlike a plain space or a literal newline (\s matches both).


def _flatten_with_line_map(text):
    """Return the text with each whitespace run collapsed to one separator, and a map from each
    position in that flattened text back to its line number in the original.

    A coinage broken across a line break escapes a line-by-line scan entirely: "a pipeline\\n
    station passed" carries the banned collocation and no single line holds it. That is how
    `pipeline station` survived in skills/communicator/SKILL.md while this lint reported clean,
    and the commit that claimed to have removed it was wrong (caught 2026-08-05 by an adversarial
    review of the push). Prose wraps, so this is the ordinary case rather than a rare one.

    Paragraph model: a whitespace run holding ONE newline is a soft wrap inside one paragraph and
    collapses to a single space, so a phrase split across the wrap still joins and still reports.
    A whitespace run holding TWO OR MORE newlines is a blank line — a PARAGRAPH boundary — and
    collapses to `_PARAGRAPH_MARK` instead, a character no pattern's `\\s+` can cross. A phrase
    broken across a paragraph boundary ("it drives the pipeline\\n\\nstation crews then arrive")
    must NOT report — the two halves are not one phrase, they are two paragraphs that happen to
    share a word pair — and collapsing that gap to a plain space instead of this mark is what
    made it report as one coinage (caught 2026-08-05 by adversarial review of commit 83ebd2d).
    """
    out = []
    lines = []
    line_no = 1
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            run_start_line = line_no + 1 if ch == "\n" else line_no
            j = i
            newline_count = 0
            while j < n and text[j].isspace():
                if text[j] == "\n":
                    newline_count += 1
                j += 1
            out.append(_PARAGRAPH_MARK if newline_count >= 2 else " ")
            lines.append(run_start_line)
            line_no += newline_count
            i = j
        else:
            out.append(ch)
            lines.append(line_no)
            i += 1
    return "".join(out), lines


def scan(text):
    """Return a list of (line_no, pattern_id, snippet, source) for every pattern hit.

    Two passes run. The line pass reports a hit with the line it stands on. The flattened pass
    catches a collocation split across a line break, which the line pass cannot see.
    """
    hits = []
    masked = mask_quoted_source(text)

    flat, line_of = _flatten_with_line_map(masked)
    seen_wrapped = set()
    for pid, _lang, rx, source, _date in PATTERNS:
        for m in rx.finditer(flat):
            start, end = m.start(), m.end() - 1
            if end >= len(line_of):
                end = len(line_of) - 1
            # A hit inside one line is the line pass's to report, with its own snippet.
            if line_of[start] == line_of[end]:
                continue
            key = (line_of[start], pid)
            if key in seen_wrapped:
                continue
            seen_wrapped.add(key)
            snippet = " ".join(flat[max(0, start - 40):end + 40].split())
            hits.append((line_of[start], pid, "(wrapped) " + snippet[:110], source))

    for i, line in enumerate(masked.splitlines(), 1):
        if not line.strip():
            continue
        for pid, _lang, rx, source, _date in PATTERNS:
            if rx.search(line):
                hits.append((i, pid, line.strip()[:110], source))
    return hits


def _judge_enabled():
    """The register judge is the OPT-IN ceiling (SPEC INV-203). It costs a live model call, so it stays
    OFF unless a host asks for it, keeping the literal-list gate deterministic for the suite and the push
    gate. A host turns it on by setting PRESHOW_REGISTER_JUDGE truthy; it stands down silently on any
    breakage regardless."""
    return os.environ.get("PRESHOW_REGISTER_JUDGE", "").strip().lower() in ("1", "true", "yes", "on")


def judge_document(text):
    """Run the register judge over a shown document (SPEC INV-203). Returns (offences, stood_down).

    The judge NEVER blocks on its own breakage — a missing binary, a timeout, or an unreadable answer
    leaves the literal-list verdict standing. What it must not do is let that breakage read as a clean
    bill: an empty offence list from a judge that never ran is not a finding of nothing, and the
    closing verdict below says which of the two it is. `stood_down` is the plain reason, or None when
    the judge either ran or was never asked to.
    """
    if not _judge_enabled():
        return [], None
    try:
        hooks_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hooks")
        sys.path.insert(0, hooks_dir)
        import register_judge_core as core
    except ImportError:
        return [], "the judge's own reader could not be loaded"
    offences, error = core.judge(text, core.DOCUMENT_REGISTER_LAW, surface="a document shown to a human")
    if error:
        sys.stderr.write("preshow register judge stood down: %s\n" % error)
        return [], error
    return offences, None


def main(argv):
    if len(argv) < 2:
        sys.stderr.write("usage: preshow-register-lint.py FILE [FILE ...]|-\n")
        return 2
    any_hit = False
    stood_down = []
    for src in argv[1:]:
        text = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
        hits = scan(text)
        if hits:
            any_hit = True
            print("PRE-SHOW REGISTER LINT (SPEC INV-83): the pack's machine dialect leaked into text a")
            print("human is about to see. Say it in the reader's own plain words before showing. File: %s" % src)
            for line_no, pid, snippet, source in hits:
                print("  line %d  [%s]  %s" % (line_no, pid, snippet))
                print("          ↳ source: %s" % source)
        # The judge is the ceiling: it catches the machine-register leak no fixed pattern lists (INV-203).
        offences, judge_stood_down = judge_document(text)
        if judge_stood_down:
            stood_down.append((src, judge_stood_down))
        if offences:
            any_hit = True
            print("PRE-SHOW REGISTER JUDGE (SPEC INV-203): a shown surface leaks the machine dialect the")
            print("literal list does not carry. Say it in the reader's own plain words first. File: %s" % src)
            # A display width, not a threshold anything is checked against — how many judge offences
            # fit one screen before the reader stops reading. Nothing reds off it: the verdict below
            # is driven by `any_hit`, so a ninth offence still fails the lint, it just is not printed.
            # Named the way the progress report's table width was named (commit 31d3375, 2026-08-19).
            for o in offences[:OFFENCES_SHOWN]:
                print("  · %s" % o.get("quote", "")[:110])
                print("          ↳ %s" % o.get("why", ""))
    for src, reason in stood_down:
        # The judge was asked to read this file and could not. It still does not block (the literal
        # list's verdict stands), and it does not get to pass as a clean bill either.
        print("JUDGE DID NOT RUN (preshow-register): %s — %s. The verdict below covers only the "
              "literal pattern list; a novel machine-register leak in this file went unread." % (src, reason))
    if any_hit:
        print('{"severity":"error","code":"register-leak","message":"a shown surface carries a coined '
              'metaphor, a calque, or a transliterated pack term","fix":"say it in the reader\'s own '
              'plain words; internal coinages live in docs only"}')
        return 1
    print("OK (preshow-register): no coined metaphor, calque, or transliterated pack term found.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
