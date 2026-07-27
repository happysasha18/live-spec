#!/usr/bin/env python3
"""specformat.py — the shared parser for the requirements format (SPEC INV-250..271).

One home for reading the format `docs/spec-format.md` defines, so the
seven format gates (check-requirement-shape, check-vocabulary, check-one-name, check-weak-words,
check-no-history, check-index-generated + build-index, check-delta-record, check-size-ratchet) parse
the document the same way. A gate that re-implements the parse drifts from its siblings; this module
is the one reader they all import (the sibling of nonempty_input.py, imported via a sys.path insert of
the guardrails dir).

THE FORMAT, in the shapes this parser returns:

- A document opens with a PREAMBLE (prose before the glossary heading), then a GLOSSARY
  (`## Glossary` or `## Glossary additions`, a block of `- **term** — definition` lines), then a
  BODY of REQUIREMENTS.
- A REQUIREMENT is `## Requirement N: Title`, carrying a `**Context:**` block, a `**User Story:**`
  line, an `### Acceptance Criteria` heading, then CASES.
- A CASE is `**Case: name**`, followed by numbered CRITERIA.
- A CRITERION is a line `N. text ... [CODE]`, numbered continuously through its requirement, sitting
  in exactly one case, trailing a code anchor at the line's end. A `[GAP: ...]` line may sit under it.
- A criterion may carry a SUB-LIST: indented `- ` bullet lines directly under its numbered line, each
  holding one more piece of that criterion's rule. The bullets belong to the criterion, so a gate
  that reads a criterion's prose reads them too: `crit.bullets` holds them in order, and
  `crit.pieces` returns the criterion's own body first and then each bullet. The sub-list ends at the
  next criterion, the next case heading, the next requirement, or a blank line followed by
  unindented text. Without this, moving words from a criterion line into bullets under it drops them
  out of every prose gate's reach while the text a person reads stays the same length.

The code anchor is one or more `[...]` groups at the line's end; a group holds codes like `INV-250`,
`T-9`, `E-35`, `A-5`, `ACT-3`, or a range `T-1..T-7`, comma-separated, and may be preceded by a
`[default]` marker. `[GAP: ...]` is a gap line, never a criterion.

Stdlib only.
"""
import re

# A single code token: a letter-run, a dash, a number, with an optional range tail.
CODE = r"[A-Z]+-[0-9]+(?:\.\.[A-Z]*-?[0-9]+)?"
CODE_RE = re.compile(CODE)

# A trailing anchor block: one or more bracket groups at the very end of a line, each holding codes
# (or the bare `[default]` marker). `[GAP: ...]` is deliberately NOT an anchor.
_BRACKET = r"\[[^\]]*\]"
TRAILING_ANCHOR_RE = re.compile(r"(?:\s*%s)+\s*$" % _BRACKET)

GLOSSARY_HEADS = ("## Glossary additions", "## Glossary")
REQUIREMENT_RE = re.compile(r"^## Requirement\s+(\d+)\s*:\s*(.*)$")
CASE_RE = re.compile(r"^\*\*Case:\s*(.+?)\s*\*\*\s*$")
CONTEXT_RE = re.compile(r"^\*\*Context:\*\*")
USER_STORY_RE = re.compile(r"^\*\*User Story:\*\*")
AC_RE = re.compile(r"^###\s+Acceptance Criteria")
CRITERION_RE = re.compile(r"^(\s*)(\d+)\.\s+(.*\S)\s*$")
GAP_RE = re.compile(r"\[GAP:")
GLOSSARY_TERM_RE = re.compile(r"^\s*-\s+\*\*(.+?)\*\*\s+—\s+(.*\S)\s*$")
# A bullet of a criterion's sub-list: an indented `- ` line. The glossary's own `- **term**` lines
# sit at column zero, so the indent is what separates the two.
BULLET_RE = re.compile(r"^[ \t]+[-*+]\s+(.*\S)\s*$")

# The label `pieces` gives a criterion's own body, so a gate can tell it from a bullet's label.
CRITERION_LINE = "the criterion line"


class Bullet(object):
    """One indented bullet under a criterion line, carrying a piece of that criterion's rule."""

    def __init__(self, text, line_no, index):
        self.text = text                # the bullet's text after its `- ` marker
        self.line_no = line_no          # 1-based source line
        self.index = index              # 1-based position under its criterion

    @property
    def label(self):
        """How a gate names this bullet to a writer."""
        return "bullet %d" % self.index


class Criterion(object):
    def __init__(self, req_num, number, text, line_no):
        self.req_num = req_num          # the requirement number it sits under
        self.number = number            # its own criterion number (int)
        self.text = text                # the full criterion text after "N. "
        self.line_no = line_no          # 1-based source line
        self.case = None                # the case name it sits under (or None)
        self.gap_lines = []             # any [GAP: ...] lines recorded beneath it
        self.bullets = []               # Bullet objects of its sub-list, in order

    @property
    def codes(self):
        """The distinct codes in this criterion's trailing anchor, ranges kept whole."""
        anchor = self.anchor
        return CODE_RE.findall(anchor) if anchor else []

    @property
    def anchor(self):
        """The trailing anchor text, or '' when the criterion trails none."""
        m = TRAILING_ANCHOR_RE.search(self.text)
        if not m:
            return ""
        # A trailing `[GAP: ...]` on the criterion line itself is not an anchor.
        chunk = m.group(0)
        if "[GAP:" in chunk and not CODE_RE.search(chunk):
            return ""
        return chunk if CODE_RE.search(chunk) else ""

    @property
    def has_anchor(self):
        return bool(self.anchor)

    @property
    def body(self):
        """The criterion text with its trailing anchor stripped."""
        a = self.anchor
        return self.text[: self.text.rfind(a)].rstrip() if a else self.text

    @property
    def pieces(self):
        """The criterion's sentences in reading order: its own body first, then each bullet of its
        sub-list. Each piece is `(label, text, line_no)`. A gate that measures a criterion's prose
        measures every piece, so words moved from the line into a bullet stay in reach."""
        out = [(CRITERION_LINE, self.body, self.line_no)]
        for b in self.bullets:
            out.append((b.label, b.text, b.line_no))
        return out


class Requirement(object):
    def __init__(self, number, title, line_no):
        self.number = number
        self.title = title
        self.line_no = line_no
        self.has_context = False
        self.has_user_story = False
        self.has_ac = False
        self.cases = []                 # ordered case names
        self.criteria = []              # Criterion objects, in order


class Document(object):
    def __init__(self):
        self.preamble = ""
        self.glossary_head = None       # the heading text used, or None
        self.glossary = []              # list of (term, definition, line_no) in order
        self.requirements = []          # Requirement objects
        self.text = ""

    @property
    def glossary_terms(self):
        return [t for (t, _d, _l) in self.glossary]

    @property
    def criteria(self):
        out = []
        for r in self.requirements:
            out.extend(r.criteria)
        return out


def parse(text):
    """Parse a requirements-format document into a Document. Tolerant: unknown lines are ignored, so
    a partly-formed document still yields the structure the gates can red against."""
    doc = Document()
    doc.text = text
    lines = text.split("\n")

    # Locate the glossary heading (the first of the two forms that appears).
    gloss_idx = None
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s in GLOSSARY_HEADS:
            gloss_idx = i
            doc.glossary_head = s
            break

    # Preamble: everything before the glossary heading (or before the first requirement if no
    # glossary heading is present).
    first_req = None
    for i, ln in enumerate(lines):
        if REQUIREMENT_RE.match(ln.strip()):
            first_req = i
            break
    cut = gloss_idx if gloss_idx is not None else (first_req if first_req is not None else len(lines))
    doc.preamble = "\n".join(lines[:cut]).strip()

    # Glossary terms: from the glossary heading up to the first requirement (or the next `## ` head).
    if gloss_idx is not None:
        for i in range(gloss_idx + 1, len(lines)):
            s = lines[i].strip()
            if REQUIREMENT_RE.match(s) or (s.startswith("## ") and s not in GLOSSARY_HEADS):
                break
            m = GLOSSARY_TERM_RE.match(lines[i])
            if m:
                doc.glossary.append((m.group(1).strip(), m.group(2).strip(), i + 1))

    # Requirements, cases, criteria.
    cur_req = None
    cur_case = None
    in_ac = False
    last_crit = None
    bullet_owner = None                 # the criterion whose sub-list is open here
    prev_blank = True
    for i, raw in enumerate(lines):
        s = raw.strip()
        if not s:
            prev_blank = True
            continue
        if prev_blank and raw[:1] not in (" ", "\t"):
            # A blank line and then unindented text close the open sub-list.
            bullet_owner = None
        prev_blank = False
        mreq = REQUIREMENT_RE.match(s)
        if mreq:
            cur_req = Requirement(int(mreq.group(1)), mreq.group(2).strip(), i + 1)
            doc.requirements.append(cur_req)
            cur_case = None
            in_ac = False
            last_crit = None
            bullet_owner = None
            continue
        if cur_req is None:
            continue
        if CONTEXT_RE.match(s):
            cur_req.has_context = True
            continue
        if USER_STORY_RE.match(s):
            cur_req.has_user_story = True
            continue
        if AC_RE.match(s):
            cur_req.has_ac = True
            in_ac = True
            continue
        mcase = CASE_RE.match(s)
        if mcase:
            cur_case = mcase.group(1).strip()
            cur_req.cases.append(cur_case)
            last_crit = None
            bullet_owner = None
            continue
        # A [GAP: ...] line attaches to the criterion above it.
        if GAP_RE.search(s) and CRITERION_RE.match(raw) is None:
            if last_crit is not None:
                last_crit.gap_lines.append(s)
            continue
        mcrit = CRITERION_RE.match(raw)
        if mcrit and in_ac:
            crit = Criterion(cur_req.number, int(mcrit.group(2)), mcrit.group(3).strip(), i + 1)
            crit.case = cur_case
            cur_req.criteria.append(crit)
            last_crit = crit
            bullet_owner = crit
            continue
        # An indented bullet under an open criterion is a piece of that criterion.
        mbul = BULLET_RE.match(raw)
        if mbul and bullet_owner is not None:
            bullet_owner.bullets.append(
                Bullet(mbul.group(1).strip(), i + 1, len(bullet_owner.bullets) + 1))
            continue
    return doc


def normalize_criterion(text):
    """The delta-classifier normal form (SPEC INV-261): whitespace collapsed, italic `*` markers
    stripped, letters case-folded OUTSIDE code anchors — so a `[INV-4]` anchor keeps its case while
    the sentence around it folds. Bracketed groups are held verbatim, the rest is folded."""
    parts = re.split(r"(\[[^\]]*\])", text)
    out = []
    for j, part in enumerate(parts):
        if j % 2 == 1:                  # a bracketed anchor group: keep verbatim
            out.append(part)
        else:
            out.append(part.replace("*", "").casefold())
    joined = "".join(out)
    return re.sub(r"\s+", " ", joined).strip()


def criterion_bytes(text):
    """The UTF-8 byte length of a criterion's full line text (the ratchet and budget unit)."""
    return len(text.encode("utf-8"))


def code_sort_key(code):
    """A stable sort key for a code token: (prefix, first number)."""
    m = re.match(r"([A-Z]+)-(\d+)", code)
    return (m.group(1), int(m.group(2))) if m else (code, 0)


def build_index_table(doc):
    """The generated code-to-location table (SPEC INV-258): each code the body's criteria carry,
    mapped to the requirement-and-criterion locations it appears at, sorted stably. Output only — this
    is what `scripts/build-index.py` emits and the index gate rebuilds to compare. A range code like
    `T-1..T-7` is carried whole, exactly as the criterion writes it."""
    loc = {}
    for c in doc.criteria:
        where = "R%d.%d" % (c.req_num, c.number)
        for code in c.codes:
            loc.setdefault(code, [])
            if where not in loc[code]:
                loc[code].append(where)
    rows = ["| Code | Location |", "|---|---|"]
    for code in sorted(loc, key=code_sort_key):
        rows.append("| %s | %s |" % (code, ", ".join(loc[code])))
    return "\n".join(rows) + "\n"


def index_table_codes(text):
    """The set of codes in the first column of a committed code-to-location table."""
    codes = set()
    for line in text.split("\n"):
        s = line.strip()
        if not (s.startswith("|") and s.endswith("|")):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not cells:
            continue
        first = cells[0]
        if first.lower() == "code" or set(first) <= set("-: "):
            continue
        if CODE_RE.fullmatch(first):
            codes.add(first)
    return codes


def body_codes(doc):
    """The set of codes carried on the body's criteria."""
    codes = set()
    for c in doc.criteria:
        codes.update(c.codes)
    return codes


def green_reach(check, files, matched, scanned, extra=""):
    """The green line every gate in this family prints (SPEC INV-269): the verdict, the files it
    opened, and the count of rows it matched of the rows it scanned — so a reader tells a real pass
    from one that read nothing. A zero scanned count is never a bare green line; a gate reaches this
    only after its require_nonempty guard has already red an empty input (INV-218), so `scanned` here
    is non-zero by construction, and the reach states it plainly."""
    names = ", ".join(files)
    tail = ("; %s" % extra) if extra else ""
    return ("%s: OK — reach: files=[%s]; matched %d of %d rows scanned%s"
            % (check, names, matched, scanned, tail))
