"""test_architecture_format.py — the architecture-format member's suite checks (SPEC INV-278/279/280,
ROADMAP row 456). Rides the suite; no push-gate letter.

Red-proven against the pre-conversion tree: the architecture was a 4-column `## Nodes` TABLE, so
`archformat.parse_nodes` raises on it (every INV-278 check reds); the owns cells restated spec laws and
the pins carried landing dates (INV-279 reds); consumers parsed the raw table by hand and
`crosscut_counter.PACK_NODES` was a hardcoded literal (INV-280 reds).
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "guardrails"))
import archformat  # noqa: E402
import specformat  # noqa: E402


def _read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def _nodes():
    return archformat.parse_nodes(_read("ARCHITECTURE.md"))


# ---------- INV-278: the architecture is a family member written as node sections ----------

def test_every_node_is_a_section_with_the_required_fields():
    nodes = _nodes()
    assert len(nodes) >= 20, "expected the full node set, got %d" % len(nodes)
    for n in nodes:
        assert n.responsibility.strip(), "%s: empty responsibility" % n.name
        assert n.owns.strip(), "%s: empty owns" % n.name
        assert "pins" in n.fields, "%s: no pins field" % n.name


def test_target_nodes_mark_the_tag_in_their_heading():
    by_name = {n.name: n for n in _nodes()}
    # the two [target] nodes at this landing
    for name in ("guardrails", "snapshot"):
        assert by_name[name].is_target, "%s should carry the [target] tag in its heading" % name


def test_every_anchor_owned_by_exactly_one_node():
    nodes = _nodes()
    owner = {}
    dup = []
    for n in nodes:
        for a in n.anchors_expanded:
            if a in owner:
                dup.append((a, owner[a], n.name))
            owner[a] = n.name
    assert not dup, "anchors owned by more than one node: %s" % dup


def test_archformat_refuses_the_retired_table_shape():
    old = ("## Nodes\n\n"
           "| Node | Responsibility (one line) | Owns spec facts (anchors) | Pinned to (file:line) |\n"
           "|---|---|---|---|\n"
           "| base-rulebook | rules | E-12 | `skills/live-spec-base/SKILL.md:17` |\n")
    try:
        archformat.parse_nodes(old)
        assert False, "archformat must refuse the retired 4-column table shape"
    except ValueError:
        pass


# ---------- INV-279: owns cites its rule, restates no law, carries no history ----------

# Provenance in a pin label: a calendar date, a "session N", or a "row N landed" / "landed <date>"
# note. A functional mention of the status word (a backticked `landed`-flipping commit) is not provenance.
_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
_SESSION = re.compile(r"\bsession\s+\d", re.I)
_LANDED = re.compile(r"\brow\s+\d+\s+landed\b|\blanded\s+\d{4}-\d{2}-\d{2}", re.I)


def _pin_labels(node):
    return [label for _path, label in node.pins if label]


def test_no_pin_label_carries_a_date_or_session_or_landed_provenance():
    offenders = []
    for n in _nodes():
        for label in _pin_labels(n):
            if _DATE.search(label) or _SESSION.search(label) or _LANDED.search(label):
                offenders.append((n.name, label))
    assert not offenders, "pin labels carrying history/provenance: %s" % offenders


def test_no_node_field_carries_history():
    """The no-history law reaches the architecture body, not only pin labels (SPEC INV-279, R290.4/5):
    a calendar date, a session number, or a `row N landed` note in a responsibility, owns, or notes field
    reds — the journal holds when and why a node landed. A roadmap-row pointer (`ROADMAP 424`, `row 241`)
    and a date inside a pin PATH (a real filename like `onboarding-card-2026-07-10.html`) are not history;
    only the field bodies are scanned here, pin paths excluded."""
    offenders = []
    for n in _nodes():
        for field in ("responsibility", "owns", "notes"):
            text = n.fields.get(field, "")
            for pat, kind in ((_DATE, "date"), (_SESSION, "session"), (_LANDED, "landed-row")):
                m = pat.search(text)
                if m:
                    offenders.append((n.name, field, kind, m.group(0)))
    assert not offenders, "node fields carrying history/provenance: %s" % offenders


def _top_level_parens(text):
    """Every top-level (...) group in text, nesting tolerated."""
    out, depth, start = [], 0, None
    for i, ch in enumerate(text):
        if ch == "(":
            if depth == 0:
                start = i + 1
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0 and start is not None:
                out.append(text[start:i])
                start = None
    return out


_WORD = re.compile(r"[a-z0-9]+", re.I)


def _longest_common_run(a_words, b_words):
    """Length of the longest contiguous shared word-run between two token lists."""
    if not a_words or not b_words:
        return 0
    best = 0
    bset_index = {}
    for j, w in enumerate(b_words):
        bset_index.setdefault(w, []).append(j)
    for i, w in enumerate(a_words):
        for j in bset_index.get(w, ()):
            k = 0
            while i + k < len(a_words) and j + k < len(b_words) and a_words[i + k] == b_words[j + k]:
                k += 1
            if k > best:
                best = k
    return best


def _spec_criteria_by_anchor():
    doc = specformat.parse(_read("PRODUCT_SPEC.md"))
    by = {}
    for c in doc.criteria:
        toks = [w.lower() for w in _WORD.findall(c.body)]
        for code in c.codes:
            for member in archformat.expand_anchor(code):
                by.setdefault(member, []).append(toks)
    return by


# A parenthetical that shares a run this long with its anchor's spec criterion is restating the law,
# not citing it. A short wiring note ("the reach map's directory classes as host config...") shares only
# incidental words; a copied clause shares a long verbatim run.
RESTATE_RUN = 10


def test_no_owns_parenthetical_restates_its_anchor_law():
    by_anchor = _spec_criteria_by_anchor()
    offenders = []
    for n in _nodes():
        # anchors this node owns, in order, so a parenthetical is checked against its own anchors' laws
        node_anchors = [a for a in archformat.ANCHOR_RE.findall(n.owns)]
        expanded = set()
        for a in node_anchors:
            expanded.update(archformat.expand_anchor(a))
        for paren in _top_level_parens(n.owns):
            ptoks = [w.lower() for w in _WORD.findall(paren)]
            for a in expanded:
                for crit in by_anchor.get(a, ()):
                    run = _longest_common_run(ptoks, crit)
                    if run >= RESTATE_RUN:
                        offenders.append((n.name, a, run, paren[:80]))
                        break
    assert not offenders, (
        "owns parentheticals restating a spec law (shared run >= %d words):\n%s"
        % (RESTATE_RUN, "\n".join("  %s [%s] run=%d: %s" % o for o in offenders)))


def test_prover_record_relocated_out_of_the_architecture():
    arch = _read("ARCHITECTURE.md")
    assert "## Prover record" not in arch, "the dated Prover-record table must leave the architecture"
    rec = "docs/prover/architecture-prover-record.md"
    assert os.path.exists(os.path.join(ROOT, rec)), "the prover-record must relocate to %s" % rec
    assert "| Date |" in _read(rec), "the relocated record must carry the dated table"


# ---------- INV-280: one node reader, every consumer through it ----------

def test_archformat_is_the_reader():
    nodes = _nodes()
    assert 20 <= len(nodes) <= 30
    assert all(n.name for n in nodes)


def test_node_growth_counter_rederives_its_node_list_from_the_reader():
    src = _read("guardrails/crosscut_counter.py")
    # no hardcoded literal node-name list survives — the names come from the reader
    assert "archformat" in src, "crosscut_counter must read node names through archformat"
    # the old hardcoded PACK_NODES literal (a bracketed list of quoted node names) must be gone
    m = re.search(r"PACK_NODES\s*=\s*\[([^\]]*)\]", src)
    if m:
        body = m.group(1)
        quoted = re.findall(r"['\"][a-z-]+['\"]", body)
        assert len(quoted) < 5, "crosscut_counter still hardcodes a node-name list: %s" % quoted


def test_no_consumer_parses_the_raw_node_table_by_hand():
    """No consumer under tests/ or guardrails/ (but archformat itself) reconstructs a node by SLICING the
    architecture's Nodes SECTION out and reading its rows. The reach covers BOTH the Python idiom (a
    `.split("## Nodes")` that carves the section) AND the shell idiom (a `sed`/`awk` range address
    `/## Nodes/,/## Seams/` that does the same) — the pin-drift check is a shell consumer INV-280 names, so
    a .py-only reach would leave it unseen (SPEC INV-280, gate-reach INV-269). A `.index("## Nodes")`
    heading-order check and a `|`-split of some OTHER table (feature coverage, seams, budgets) are
    legitimate and not flagged."""
    py_slice = re.compile(r"""\.split\(\s*['"]##\s*Nodes['"]""")
    sh_slice = re.compile(r"/##\s*Nodes/\s*,\s*/##\s*Seams/")
    offenders = []
    for base in ("tests", "guardrails"):
        d = os.path.join(ROOT, base)
        for fn in os.listdir(d):
            if fn in ("archformat.py", "test_architecture_format.py"):
                continue
            if not (fn.endswith(".py") or fn.endswith(".sh")):
                continue
            src = _read(os.path.join(base, fn))
            if py_slice.search(src) or sh_slice.search(src):
                offenders.append(base + "/" + fn)
    assert not offenders, "consumers still slicing the raw node section by hand: %s" % offenders
