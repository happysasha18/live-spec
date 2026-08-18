#!/usr/bin/env python3
"""check-requirement-shape.py — the requirements-format shape gate (SPEC INV-250, INV-251, INV-252).

UNARMED. This gate ships as part of the spec-format migration and ARMS only in the one conversion
delivery that rewrites PRODUCT_SPEC.md into the requirements format (INV-270). Until then no pre-push
chain and no CI step invokes it, and its suite test drives it over FIXTURES and the prototype corpus,
never the live spec. It reads no default file: the document to check is named on the command line, so
an un-converted tree is never scanned.

THE LAW it enforces, from `docs/spec-format.md`:

  INV-250 — the document opens with a preamble, then a glossary, then a body of requirements; each
  requirement carries a Context block, a User Story line, and acceptance criteria grouped into named
  cases; each criterion sits in exactly one case, and the criteria number continuously through the
  requirement.

  INV-251 — each criterion trails its code anchor at the line's end and states its response as a
  lowercase-italic `*shall*`; no word in the document is written in all capitals outside a code
  anchor or a filename.

  INV-252 — a source hole is recorded as a well-formed `[GAP: ...]` line; a malformed gap line reds.

NOT MECHANICALLY CHECKED, by design (reported, never silently skipped): INV-251's "one trigger and
one response" cannot be enforced by counting keywords without red-ing the real corpus — section.md
carries criteria with two `*if* ... *then*` clauses and two `*shall*` responses joined in one
sentence, all valid. Counting `*when*/*while*/*if*` or `*shall*` occurrences would false-red them.
The atomicity of a criterion is a cold-reader judgment (Area 5), not a lint. Likewise INV-252's
"a gap line that carries an invented answer" and INV-257's "an evaluative phrase names its judge"
are semantic reads no script decides; the gap-line FORM is checked here, the rest is the panel's.

Usage:
  check-requirement-shape.py <document.md> [<part.md> ...]
Exit 0 on a well-shaped document (printing the reach line, INV-269); exit 1 naming each violation.
Stdlib only.
"""
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import specformat as sf  # noqa: E402
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402

CHECK = "check-requirement-shape"

# All-caps words that are not shouting: standard acronyms and document/file names the format uses in
# ordinary prose. A word.ext filename and any `[...]`-bracketed anchor are exempt separately.
CAPS_ALLOW = {
    "CLI", "HTML", "JSON", "CSS", "API", "URL", "PR", "CI", "AI", "MPS", "SDK", "HTTP", "HTTPS",
    "TODO", "SPEC", "VERSION", "README", "MIGRATION", "JOURNAL", "ROADMAP", "LICENSE", "OVERVIEW",
    "FEEDBACK", "DECISIONS", "SURFACES", "WAITING", "NEXT", "STEPS", "OK", "UTF",
}
FILENAME_RE = re.compile(r"[\w./-]+\.(?:md|py|sh|json|txt|html|js|css|yml|yaml|toml)\b")
CAPS_WORD_RE = re.compile(r"\b[A-Z]{2,}\b")
GAP_LINE_RE = re.compile(r"\[GAP:\s*\S.*\]")            # well-formed: a colon, then real text, then ]
GAP_ANY_RE = re.compile(r"\[GAP\b")
SHALL_RE = re.compile(r"\*shall\*")
BARE_SHALL_RE = re.compile(r"(?<!\*)\bshall\b(?!\*)")


def _caps_violations(text):
    """All-caps shouting words outside anchors, filenames, inline-code spans, code tokens, and the
    acronym allowlist, per line."""
    bad = []
    for i, raw in enumerate(text.split("\n"), 1):
        # Blank inline-code spans, bracketed groups (anchors, [GAP: ...], [default]), code tokens
        # (a caps prefix on a `-number` code like INV-250), and filenames first.
        s = re.sub(r"`[^`]*`", " ", raw)
        s = re.sub(r"\[[^\]]*\]", " ", s)
        s = re.sub(r"\b[A-Z]+-[0-9]", " ", s)
        s = FILENAME_RE.sub(" ", s)
        for w in CAPS_WORD_RE.findall(s):
            if w not in CAPS_ALLOW:
                bad.append((i, w))
    return bad


def main(argv):
    if len(argv) < 2:
        print("%s: usage: %s <document.md> [<part.md> ...]" % (CHECK, os.path.basename(argv[0])))
        return 2
    # The document may arrive as a core plus its parts (specformat's parts map). The gate
    # reads the concatenation as ONE document, so a rule that spans core and part is seen once; with
    # no parts this is the single file, byte for byte.
    paths = sf.spec_paths(argv[1:])
    missing = [p for p in paths if not os.path.isfile(p)]
    if missing:
        print("%s: cannot read %s — the gate stands on the document file."
              % (CHECK, ", ".join(missing)))
        return 1
    where = ", ".join(paths)   # what a fault line names: the file, or the files
    _read, text = sf.read_document(paths, expand=False)
    doc = sf.parse(text)

    problems = []

    # INV-250 c1: preamble, then glossary, then body, in that order.
    if not doc.preamble:
        problems.append("no preamble stands before the glossary (INV-250).")
    if doc.glossary_head is None:
        problems.append("no `## Glossary` (or `## Glossary additions`) heading (INV-250).")
    else:
        gloss_pos = text.find(doc.glossary_head)
        first_req = doc.requirements[0].line_no if doc.requirements else None
        gloss_line = text[:gloss_pos].count("\n") + 1
        if first_req is not None and gloss_line > first_req:
            problems.append("the glossary heading falls after the first requirement — order must be "
                            "preamble, glossary, body (INV-250).")

    # The input set the gate expects non-empty: the requirements. Zero reds by name (INV-218).
    try:
        require_nonempty(CHECK, "the document's requirements", doc.requirements)
    except VacuousInputError as e:
        print("%s: %s" % (CHECK, e))
        return 1

    scanned = 0
    for r in doc.requirements:
        tag = "Requirement %d" % r.number
        if not r.has_context:
            problems.append("%s has no `**Context:**` block (INV-250)." % tag)
        if not r.has_user_story:
            problems.append("%s has no `**User Story:**` line (INV-250)." % tag)
        if not r.has_ac:
            problems.append("%s has no `### Acceptance Criteria` (INV-250)." % tag)
        if not r.cases:
            problems.append("%s carries no named case (INV-250)." % tag)
        # INV-250 c3: continuous numbering through the requirement, 1..N.
        nums = [c.number for c in r.criteria]
        if nums and nums != list(range(1, len(nums) + 1)):
            problems.append("%s numbers its criteria %s — the numbering must run continuously 1..%d "
                            "through the requirement (INV-250)." % (tag, nums, len(nums)))
        for c in r.criteria:
            scanned += 1
            loc = "%s criterion %d (line %d)" % (tag, c.number, c.line_no)
            # INV-250 c3: exactly one case.
            if c.case is None:
                problems.append("%s sits in no named case (INV-250)." % loc)
            # INV-251 c4: a trailing code anchor.
            if not c.has_anchor:
                problems.append("%s trails no code anchor at the line's end (INV-251)." % loc)
            # INV-251: the response is a lowercase-italic *shall*.
            if not SHALL_RE.search(c.text):
                problems.append("%s states no lowercase-italic `*shall*` response (INV-251)." % loc)
            if BARE_SHALL_RE.search(c.body):
                problems.append("%s writes a bare `shall` — the keyword must be lowercase italic "
                                "`*shall*` (INV-251)." % loc)

    # INV-252: every gap line is well-formed.
    for i, raw in enumerate(text.split("\n"), 1):
        if GAP_ANY_RE.search(raw) and not GAP_LINE_RE.search(raw):
            problems.append("line %d carries a malformed gap marker — a source hole is recorded as "
                            "`[GAP: <what is unstated>]` (INV-252): %s" % (i, raw.strip()))

    # INV-251 c5: no all-caps shouting.
    for ln, w in _caps_violations(text):
        problems.append("line %d writes `%s` in all capitals outside a code anchor or filename "
                        "(INV-251)." % (ln, w))

    if problems:
        print("%s: %d shape violation(s) in %s:" % (CHECK, len(problems), where))
        for p in problems:
            print("  - %s" % p)
        return 1

    print(sf.green_reach(CHECK, [os.path.basename(p) for p in paths], scanned, scanned,
                         "all %d criteria well-shaped across %d requirements"
                         % (scanned, len(doc.requirements))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
