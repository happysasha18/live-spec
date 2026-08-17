#!/usr/bin/env python3
"""Stop-hook: an internal code may only trail a sentence as a quiet anchor (SPEC INV-28, base rule 2).

The law says every human-facing sentence stands on its own in the product's words, and internal handles
— a queue row number, an INV/M/E/T code — trail in parentheses for anyone who wants to follow them. A
sentence that leads with a handle hands the reader a number he has no way to resolve.

It decayed for want of a machine. On 2026-07-27 the human was handed "rows 386 and 412, hanging since 18
July" and answered plainly: he does not remember row numbers, the sentence tells him nothing, put a hook
on it. This is that hook.

WHAT IT READS. Every assistant message shown since the last human turn (hooks/turn_reader.py), so a
naked code in an early narration line reds like one in the final reply.

WHAT PASSES, by construction:
  - a code inside parentheses or square brackets — the lawful trailing anchor; the span is now allowed
    to carry one embedded line break, so an anchor broken across a line by wrapping still clears;
  - a table row (a line starting with `|`), where the neighbouring cell carries the plain words;
  - a fenced code block, an inline `backtick` span, and a «quoted» or "quoted" span — text ABOUT a code
    rather than a code addressed to the reader;
  - a bare number with no code word in front of it, since this net reads the naming, not arithmetic;
  - the Russian naming word plus a number when the same line goes on to name a file — either the word
    for "file" in any inflection, or a filename-shaped token (word.ext) — since that is a line inside a
    source file, which owes no anchor.

WHAT NOW ALSO REDS, this repository's own citation idioms that the first cut of the net missed:
  - a document name run directly against its number — "ROADMAP 480", "ARCHITECTURE 122",
    "PRODUCT_SPEC 352", "TEST_MATRIX 6" — the same naked-code shape as "row 480" one word earlier;
  - the multi-letter codes (INV, ROW, ACT) read aloud with a space instead of the inline dash —
    "INV 281" reds exactly as "INV-281" does; the single-letter codes (M, E, T, S, D, A, B, C, F, R)
    keep the dash-only requirement, since "M 402" is safe but "a 2" or "b 12" are ordinary English and
    a space-tolerant single-letter net would fire on them constantly;
  - "row #386" — a hash between the word and the number.

CASE. The multi-letter (INV/ROW/ACT) and single-letter dash codes match uppercase letters only; the
working-language naming word and the document-name pattern match either case.

HONEST BOUNDARY. This arm sees whether a code was left standing outside an anchor. It cannot see whether
the plain words that replace it are the RIGHT words: "the thing from yesterday (row 386)" passes the
machine and still fails the reader. It is a Stop-hook notice, so the reply is already sent when it fires;
it asks for the naming to be repeated in plain words in the next message, which is the most a chat
surface allows.

THE FILE-LINE SIGNAL, AND WHAT IT STILL CANNOT TELL APART. In the working language one word carries
both meanings, a queue row and a line inside a source file, so a bare naming word plus a number is read
as a queue row by default. The signal this net acts on is textual and local: the word for "file" in any
of its inflections, or a filename-shaped token (letters, digits or underscore, a dot, an extension),
appearing on the same line shortly after the number. Either one flips the reading to a source line. What
it still cannot tell apart: the genuinely ambiguous case with no file word and no filename anywhere on
the line, which still reads as a naked queue row and reds even where a source line was meant. English
carries no matching ambiguity in this repository's usage, a source line always being written "line N",
so the English pattern needs no equivalent carve-out.

Repo home: hooks/code-anchor-scan.py; installed copy: ~/.claude/hooks/ (beside scissors-scan.py).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import turn_reader  # noqa: E402

# The naming patterns: a code word followed by its number, in either working language, plus the bare
# letter-dash-number handles the documents use. The working-language naming word and the document-name
# form match either case; the two internal-code forms match uppercase only, since a lowercase reading
# of either is ordinary English (a step or a play's "act 3", the letter-dash-digit pairs "b-2", "f-16",
# "c-4") rather than a code.
CASE_INSENSITIVE_PATTERNS = [
    r"(?<![\w-])строк[аиуеойы]?\s+\d+",  # user-language: the naming word when chat runs in Russian
    r"(?<![\w-])строки\s+\d+",  # user-language: its plural, same naming word
    r"(?<![\w-])rows?\s+#?\d+",  # 'row 386' and the hash form 'row #386'
    r"(?<![\w-])(?:ROADMAP|ARCHITECTURE|PRODUCT_SPEC|TEST_MATRIX)\s+\d+",  # 'ROADMAP 480'
]
CASE_SENSITIVE_PATTERNS = [
    r"(?<![\w-])(?:INV|ROW|ACT)[-\s]+\d+",  # multi-letter code, dash or the spoken space: 'INV 281'
    r"(?<![\w-])(?:M|E|T|S|D|A|B|C|F|R)-\d+",  # single-letter codes: dash only, never a bare space
]
COMPILED = (
    [re.compile(p, re.IGNORECASE) for p in CASE_INSENSITIVE_PATTERNS]
    + [re.compile(p) for p in CASE_SENSITIVE_PATTERNS]
)

# The working language's naming word is ambiguous between a queue row and a line inside a source file;
# a nearby file word or filename-shaped token on the same line flips the reading to the source line.
RU_LINE_WORD = re.compile(r"строк[аиуеойы]?\s+\d+", re.IGNORECASE)  # user-language: the naming word
FILE_SIGNAL = re.compile(r"файл\w*|\b[\w-]+\.\w{1,5}\b", re.IGNORECASE)  # user-language: the file word

FENCE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")
QUOTED = re.compile(r"«[^»\n]*»|\"[^\"\n]*\"|“[^”\n]*”")
BRACKETED = re.compile(r"\([^()]*\)|\[[^\[\]]*\]", re.DOTALL)


def _strippable(text):
    """Remove every span where a code is lawful or is being quoted, leaving live prose behind."""
    text = FENCE.sub(" ", text)
    text = INLINE_CODE.sub(" ", text)
    text = QUOTED.sub(" ", text)
    # Table rows carry their describing cell beside the number.
    lines = [ln for ln in text.split("\n") if not ln.lstrip().startswith("|")]
    text = "\n".join(lines)
    # Parenthesised and bracketed spans are the lawful anchor position. Two passes so a nested pair
    # collapses too.
    for _ in range(2):
        text = BRACKETED.sub(" ", text)
    return text


def _is_file_line_reference(live, match):
    """The naming word plus a number, followed on the same line by the word for a file or by a
    filename-shaped token, names a line inside a source file, which owes no anchor."""
    if not RU_LINE_WORD.fullmatch(match.group()):
        return False
    line_end = live.find("\n", match.end())
    if line_end == -1:
        line_end = len(live)
    return bool(FILE_SIGNAL.search(live, match.end(), line_end))


def find_matches(text):
    """Every naked code in `text`, as (fragment, context) pairs.

    The fragment is the matched code itself — a row named by its number in either working language, or a bracket code such as "INV 281" — and the context is the
    surrounding sixty characters on either side, which is what a reader needs to find the sentence
    again. The two are separated because a caller that remembers which offences it has already
    reported needs an identity that survives the turn growing around it; a context window shifts as
    later text arrives, and the fragment does not. The caller that needed it was the tool-boundary scan,
    retired 2026-08-17 to attic/midturn-chat-scan.py; the split is kept because the identity it gives is
    the right one for any future caller that reports once.
    """
    live = _strippable(text)
    matches = []
    for rx in COMPILED:
        for m in rx.finditer(live):
            if _is_file_line_reference(live, m):
                continue
            start = max(0, m.start() - 60)
            end = min(len(live), m.end() + 60)
            matches.append((m.group().strip(), live[start:end].replace("\n", " ").strip()))
    return matches


def find_hits(text):
    return [context for _, context in find_matches(text)]


def main():
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        sys.exit(0)
    if payload.get("stop_hook_active"):
        sys.exit(0)
    text = turn_reader.turn_text(payload.get("transcript_path", ""))
    if not text:
        sys.exit(0)
    hits = find_hits(text)
    if not hits:
        sys.exit(0)
    quoted = "\n".join("  · " + h for h in hits[:5])
    reason = (
        "CODE-ANCHOR CHECK — the reply leaves an internal code standing where plain words belong:\n"
        + quoted
        + "\n\nA queue row number or an INV/M/E/T code names nothing to the reader on its own. Name the "
        "wish in the product's words and let the code trail in parentheses: 'branches and working copies "
        "for parallel lanes have been open since 18 July (row 386)'. Send the naming now, in one line "
        "per code, so what was asked of him is legible."
    )
    print(json.dumps({"decision": "block", "reason": reason, "suppressOutput": True}))
    sys.exit(0)


if __name__ == "__main__":
    main()
