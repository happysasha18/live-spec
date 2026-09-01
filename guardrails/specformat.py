#!/usr/bin/env python3
"""specformat.py — the shared parser for the requirements format (SPEC INV-250..271).

One home for reading the format `docs/spec-format.md` defines, so the
format gates (check-requirement-shape, check-vocabulary, check-one-name, check-weak-words,
check-no-history, check-index-generated + build-index, check-delta-record) parse
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

THE PARTS MAP. A document may be written as a CORE file plus PART files. The core carries the
preamble, the glossary and a `## Parts map` table naming its parts in concatenation order; each part
carries requirements only. The core is the single source of that order — nothing else lists the
parts. A core with no map (or with an empty one) IS the whole document, which is the state this
module ships in: `spec_paths(["PRODUCT_SPEC.md"])` returns exactly `["PRODUCT_SPEC.md"]` and
`read_document` returns its bytes unchanged, so every reader behaves identically before and after the
map exists. Readers call `read_document(paths)` rather than opening a path themselves, and the gates
take a list of paths on the command line so a caller can name core and parts explicitly.

Two laws hold the map honest, and this module reads both for the gates that arm them. The map names
every part: a `.md` file sitting among the named parts that no row names is an orphan nobody reads
(`unnamed_parts`, SPEC INV-322). And one requirement number names one requirement across the whole
document, so a citation and a generated `R4.1` location resolve to one place
(`repeated_requirement_numbers`, SPEC INV-323).

Stdlib only.
"""
import os
import re

# A single code token: a letter-run, a dash, a number, with an optional range tail.
CODE = r"[A-Z]+-[0-9]+(?:\.\.[A-Z]*-?[0-9]+)?"
CODE_RE = re.compile(CODE)

# A trailing anchor block: one or more bracket groups at the very end of a line, each holding codes
# (or the bare `[default]` marker). `[GAP: ...]` is deliberately NOT an anchor.
_BRACKET = r"\[[^\]]*\]"
TRAILING_ANCHOR_RE = re.compile(r"(?:\s*%s)+\s*$" % _BRACKET)

PARTS_MAP_HEAD = "## Parts map"
# The path in a parts-map row's first cell. The path is READ OUT of the cell rather than required to
# be the whole of it, so a cell written as a backticked path, a markdown link or a path with a note
# after it still names its part: a row that silently named nothing would drop a part out of every
# aggregate reader at once.
PART_PATH_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_./-]*\.md")

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
    """The UTF-8 byte length of a criterion's full line text (the delta record's byte unit)."""
    return len(text.encode("utf-8"))


def bytes_per_criterion(doc):
    """(total criterion bytes, criterion count) for a parsed document — the density measurement the
    progress report and the measurements table print. It is a reading only: nothing compares it to a
    bound. The gate that once did, `check-size-ratchet.py`, was cut on 2026-09-02 with the rest of
    the invented-ceiling family, since a real structural cut raises the average as often as bloat
    does (the 2026-08-19 incident, docs/prover/2026-08-19-invented-numbers-out.md finding 9)."""
    crits = doc.criteria
    return sum(criterion_bytes(c.text) for c in crits), len(crits)


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


def parts_map(text):
    """The part files a core document's `## Parts map` table names, in concatenation order.

    An empty list means what it says: this core is the whole document. The table's first column
    carries the path, the rest (requirement range, topic) is for the reader; a header row and the
    `|---|` rule are passed over, and the table ends at the next `## ` heading. The map stands in the
    core's PREAMBLE, above the body, so the scan stops at the first requirement: a criterion that
    quotes the heading is prose about the map, never the map."""
    parts = []
    in_map = False
    for line in text.split("\n"):
        s = line.strip()
        if REQUIREMENT_RE.match(s):
            break
        if s == PARTS_MAP_HEAD:
            in_map = True
            continue
        if not in_map:
            continue
        if s.startswith("## "):
            break
        if not (s.startswith("|") and s.endswith("|")):
            continue
        first = s.strip("|").split("|")[0].strip()
        if set(first) <= set("-: ") or not first:
            continue
        m = PART_PATH_RE.search(first)
        if m and m.group(0) not in parts:
            parts.append(m.group(0))
    return parts


def unnamed_parts(core_path, root=None):
    """The `.md` files that sit among a core's parts and that the core's map names nowhere.

    A document written as a core plus parts IS the files the map lists, and nothing else. Drop a
    part file beside the named ones without adding its row, and no reader ever opens it: its
    requirements stand outside every aggregate the gates build, and the document is silently short
    of what the tree holds. The index gate's existing orphan-code fault does not see this one — a
    brand-new part carries codes that are in neither the assembled body nor the committed table, so
    the two agree about a document with a hole in it.

    The scan reaches only the directories the map itself draws parts from, and never the core's own
    directory: a core sits beside the whole repository's other documents, and those are nobody's
    parts. A core with no map is the whole document, so it has no parts directory and this returns
    nothing.

    Paths come back relative to the core's directory, in sorted order, spelled the way a map row
    would spell them."""
    try:
        with open(core_path, encoding="utf-8") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError):
        return []
    parts = parts_map(text)
    if not parts:
        return []
    base = root if root is not None else os.path.dirname(os.path.abspath(core_path))
    named = set()
    directories = set()
    for p in parts:
        full = os.path.join(base, p)
        named.add(os.path.realpath(full))
        directories.add(os.path.dirname(os.path.realpath(full)))
    directories.discard(os.path.dirname(os.path.realpath(core_path)))
    # The names come back relative to the core's own directory, resolved the same way the entries
    # are: a tree reached through a symlink (`/var` standing for `/private/var` on a Mac) would
    # otherwise spell one file two ways and the relative name would climb out of the tree.
    real_base = os.path.realpath(base)
    orphans = set()
    for d in directories:
        try:
            entries = os.listdir(d)
        except OSError:
            continue
        for name in entries:
            if not name.endswith(".md"):
                continue
            full = os.path.realpath(os.path.join(d, name))
            if full in named:
                continue
            orphans.add(os.path.relpath(full, real_base))
    return sorted(orphans)


def repeated_requirement_numbers(doc):
    """`{number: [line numbers]}` for every requirement number more than one requirement claims.

    A requirement number is how a reader, a criterion anchor and the generated code-to-location
    table all name one place. Let two parts open `## Requirement 4:` and that one name points at two
    different rules, and the table's `R4.1` stops resolving to a single criterion. Empty when every
    number is claimed once, which is what the whole document holds today."""
    seen = {}
    for r in doc.requirements:
        seen.setdefault(r.number, []).append(r.line_no)
    return {n: lines for n, lines in seen.items() if len(lines) > 1}


def spec_paths(paths, root=None):
    """The whole file list behind the documents named on a command line, in order, without repeats.

    A named path that is a core carrying a parts map expands to that core followed by its parts,
    resolved against `root` (default: the directory holding the core). Naming core and parts
    explicitly is the same list — expansion is idempotent — so a caller may pass either, in either
    spelling: sameness is decided on the resolved file, not on the string, so `spec/x.md` typed on a
    command line and the absolute path the map expanded to are ONE file and are read once. Reading a
    part twice would double every count built over the document, so this is the guard that keeps a
    hand-typed command line honest. A path that cannot be read is returned as given, so the caller's
    own missing-file red is what speaks."""
    out, seen = [], set()
    for p in paths:
        for q in _expand(p, root):
            key = os.path.realpath(q)
            if key not in seen:
                seen.add(key)
                out.append(q)
    return out


def _expand(path, root):
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError):
        return [path]
    parts = parts_map(text)
    if not parts:
        return [path]
    base = root if root is not None else os.path.dirname(os.path.abspath(path))
    return [path] + [os.path.join(base, p) for p in parts]


def read_document(paths, root=None, expand=True):
    """`(resolved_paths, text)` for the documents named on a command line: the core and its parts
    read as ONE text, in map order. With one path and no parts the text is that file's bytes
    unchanged. Where a part does not end in a newline the join supplies one, so the last line of one
    part and the first line of the next never fuse into a single line. `expand=False` reads the paths
    exactly as given — for a caller that has already resolved them through `spec_paths`."""
    resolved = spec_paths(paths, root) if expand else list(paths)
    chunks = []
    for p in resolved:
        with open(p, encoding="utf-8") as f:
            t = f.read()
        if chunks and not chunks[-1].endswith("\n"):
            chunks.append("\n")
        chunks.append(t)
    return resolved, "".join(chunks)


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
