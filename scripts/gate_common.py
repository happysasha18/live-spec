"""gate_common.py — shared helpers for the prose-quality DONE-GATE (docs/prose-quality-gate-design.md).

Imported by the hyphenated gate scripts (spec-style-lint.py in --gate mode, spec-redundancy-precheck.py,
spec-judge.py, spec-done-gate.py). Holds the pieces they must agree on: text scrubbing, sentence/bullet
segmentation, the machine-readable waiver file, and informative-region (exemption) detection. One home per
rule, so the linter and the redundancy check strip and segment text the same way.
"""
import datetime
import json
import os
import re

# --- text scrubbing (shared with the linter) ------------------------------------------------
LEAD_MARKERS = re.compile(r"^\s*(?:(?:[-*+>]\s+)|(?:#{1,6}\s+))+")
BOLD_TITLE = re.compile(r"^\s*\*\*[^*]+\*\*\.?\s*")
FILENAME_RE = re.compile(r"\b[\w./-]+\.(?:md|py|sh|json|txt|html|js|css|yml|yaml|toml)\b")


def scrub(text):
    """Strip lead markers, inline code, bracketed anchors, and filenames — the neutral form the
    register checks run against, so `[INV-4]` and `docs/x.md` never trip a rule."""
    s = LEAD_MARKERS.sub("", text)
    s = re.sub(r"`[^`]*`", " ", s)
    s = re.sub(r"\[[^\]]*\]", " ", s)
    s = FILENAME_RE.sub(" ", s)
    return s


# --- informative-region (exemption) detection ------------------------------------------------
# Normative-only rules (second-person, negation-opener, reassurance, future-narration) skip these
# regions; global rules (scissors, machine-jargon, caps-shout) always run. A user quote or a
# user-story line is a marked informative companion (docs/spec-style.md R7b/R7c), not normative law.
USER_STORY = re.compile(r"^\s*(?:[-*+>]\s+)*\*\*\s*user\s*story\s*:?\s*\*\*", re.I)
NOTE_INFORMATIVE = re.compile(r"^\s*(?:[-*+]\s+)*(?:\*\*)?\s*note\s*\(informative\)", re.I)
BLOCKQUOTE = re.compile(r"^\s*>")


REQUIREMENT_HEADING = re.compile(r"^##\s+Requirement\s+\d+\b")
CRITERIA_HEADING = re.compile(r"^###\s+Acceptance Criteria\b")
ANY_HEADING = re.compile(r"^#{1,6}\s")


def spec_body_flags(lines):
    """Given a list of raw lines, return a list[bool] — True where the line carries the requirements
    genre's numbered criteria, which is the surface the person rule binds.

    Three shapes are told apart:

    - a requirements file, carrying a `## Requirement N` or `### Acceptance Criteria` heading: the
      criteria run from an `### Acceptance Criteria` heading to the next `##` heading, so the Context
      and User Story paragraphs above it stay explanatory prose;
    - a prose document, carrying headings and no such marker: a skill body, a README, a reader page.
      Every line is explanatory prose, where the register asks the writer to address the reader;
    - a fragment with no heading at all, which a caller hands in to be judged as a criterion. Every
      line counts, which keeps the piped-snippet contract this lint has always had.
    """
    if not any(REQUIREMENT_HEADING.match(l) or CRITERIA_HEADING.match(l) for l in lines):
        if any(ANY_HEADING.match(l) for l in lines):
            return [False] * len(lines)
        return [True] * len(lines)
    flags, inside = [], False
    for raw in lines:
        if raw.startswith("## "):
            inside = False
        if CRITERIA_HEADING.match(raw):
            inside = True
            flags.append(False)
            continue
        flags.append(inside)
    return flags


def exempt_flags(lines):
    """Given a list of raw lines, return a list[bool] — True where normative-only rules are exempt
    (inside a user-story block, an informative NOTE block, or a blockquote line). A user-story /
    NOTE block runs from its lead line to the next blank line; a blockquote is per-line."""
    flags = []
    in_block = False
    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            in_block = False
            flags.append(False)
            continue
        if USER_STORY.match(raw) or NOTE_INFORMATIVE.match(raw):
            in_block = True
        flags.append(in_block or bool(BLOCKQUOTE.match(raw)))
    return flags


# --- sentence / bullet segmentation (for the redundancy pre-check) ---------------------------
_ABBREV = ("e.g.", "i.e.", "etc.", "vs.", "cf.", "al.")


# A markdown table delimiter row — `|---|---|`, `|:--|--:|`, with or without leading/trailing pipes.
# Only dashes, colons, pipes and whitespace: never a data row, which always carries some other
# character. Skipped outright — it is punctuation, not content, and would otherwise shingle into
# spurious short-token collisions with every other table's delimiter row.
TABLE_DELIM_RE = re.compile(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?$")


def _sentence_parts(body):
    """Split scrubbed text into sentence/clause parts, guarding common abbreviations. Shared by a
    prose line and by a table cell's content, so the two are scanned by the same rule."""
    guarded = body
    for a in _ABBREV:
        guarded = guarded.replace(a, a.replace(".", "\0"))
    parts = re.split(r"(?<=[.?!;])\s+", guarded)
    return [p.replace("\0", ".").strip() for p in parts if p.replace("\0", ".").strip()]


def segment_units(text):
    """Split the document into content units — sentences and bullet clauses — each with its 1-based
    start line. Returns a list of dicts {line, raw, norm_tokens}. Splits on sentence punctuation and
    on ';', guarding common abbreviations, and treats each bullet as its own unit.

    A markdown table row is handled specially rather than skipped outright: a delimiter row
    (`|---|---|`, ruled punctuation, never prose) is dropped, but a DATA row's cells are scanned —
    each cell scrubbed and sentence-split on its own, the same as a prose line — so a fact sentence
    that happens to live inside a table cell (TEST_MATRIX.md's rows, a spec's own tables) is not
    invisible to the redundancy check. A short cell (an id, a level word, a `*status*` marker) never
    survives MIN_TOKENS in the caller, so this costs no new false positives on the structural cells."""
    units = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("|"):
            if TABLE_DELIM_RE.match(stripped):
                continue
            for cell in stripped.strip("|").split("|"):
                cell = cell.strip()
                if not cell:
                    continue
                for part in _sentence_parts(scrub(cell)):
                    units.append({"line": lineno, "raw": part})
            continue
        for part in _sentence_parts(scrub(stripped)):
            units.append({"line": lineno, "raw": part})
    return units


# --- waivers -----------------------------------------------------------------------------------
WAIVER_FIELDS = ("id", "rule", "file", "snippet", "reason", "owner", "date", "expiry")
# A ceiling on how far out a waiver's own expiry may sit (e.g. "at most 30 days from its date") was
# removed 2026-08-26: it carried no external source and no incident (the 2026-08-15 dossier's own
# words: "no waiver has ever expired and blocked a push ... no single recommended replacement, so
# today's value stands" — a number kept only because nothing better was found, not because it was
# right). The owner's standing rule forbids exactly that shape: no source, no number. The no-park
# mechanism this ceiling sat on top of does not need a magnitude to work — every waiver already MUST
# carry an `expiry` field (WAIVER_FIELDS, checked below), and `waiver_status` already reverts an
# expired waiver to a hard error rather than letting it fade to silence. That is the real thing being
# tested; the extra "and it must be short" cap was an invented add-on. A durable per-host ceiling, if
# one is ever wanted, belongs in the settings ladder's package-defaults table
# (skills/live-spec-base/references/settings-ladder.md) with a real source cited, not invented here.


def _today():
    return datetime.date.today()


def load_waivers(path):
    """Load the waiver list. Missing file → empty list."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("waiver file must be a JSON array: %s" % path)
    return data


def waiver_status(waiver, today=None):
    """'active' | 'expired' — a waiver whose expiry has passed no longer suppresses (it reverts to a
    hard error, so a forgotten debt breaks the gate rather than fading to silence)."""
    today = today or _today()
    exp = datetime.date.fromisoformat(waiver["expiry"])
    return "active" if today <= exp else "expired"


def match_waiver(rule, filename, offending_text, waivers, today=None):
    """Return the active waiver covering this finding, or None. A waiver matches when its rule and
    file match and its snippet occurs verbatim in the offending text. Snippet-based (not line-based)
    so the waiver self-invalidates once the offending text is fixed."""
    base = os.path.basename(filename)
    for w in waivers:
        if w.get("rule") != rule:
            continue
        if w.get("file") not in (filename, base):
            continue
        if w.get("snippet") and w["snippet"] in offending_text:
            if waiver_status(w, today) == "active":
                return w
    return None


def stale_waivers(waivers, matched_ids):
    """Waivers whose snippet matched no finding this run — the defect they covered is gone, so the
    waiver should be removed. Returns the list of stale waiver dicts."""
    return [w for w in waivers if w.get("id") not in matched_ids]
