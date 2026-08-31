#!/usr/bin/env python3
"""check-architecture-reference.py — the generated architecture-Reference gate (SPEC INV-315, INV-269).

Gate z. The architecture (a core plus any parts) and the committed index are named on the command
line, the sibling shape of the matrix-reference gate (`guardrails/check-matrix-reference.py`, gate d)
and the generated-index gate (`guardrails/check-index-generated.py`, gate x).

THE LAW: the architecture's Reference maps each spec anchor to the node names that own it, built from
the node sections' owns fields at freeze and output only (INV-315). This gate holds four faults, the
last of them the format family's shared map law (INV-322):

  - DRIFT: the committed Reference differs from a fresh build off the current node sections — a hand
    edit, or nodes that moved without a rebuild. Reds, since the Reference is not hand-kept.
  - A NODE OWNS AN ANCHOR THE REFERENCE MISSES: an anchor on a node's owns field absent from the
    committed Reference. Reds, naming the anchor.
  - THE REFERENCE HAS AN ANCHOR NO NODE OWNS: an anchor in the committed Reference owned by no node — an
    empty home. Reds, naming the anchor.
  - A PART THE MAP NAMES NOWHERE: a `.md` file sitting among the parts the core's map lists that no
    row of that map names. Reds, naming the file.

It declares its expected-non-empty input with the shared guard (INV-218): a document that parses to zero
node sections reds by name rather than passing over nothing.

Usage:
  check-architecture-reference.py <ARCHITECTURE.md> [<part.md> ...] <committed-index.md>
Exit 0 when the committed Reference equals the fresh build and the nodes and the Reference agree
(printing the reach line, INV-269); exit 1 naming each fault; exit 2 on a usage error. Stdlib only.
"""
import importlib.util
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)
import specformat as sf  # noqa: E402 — spec_paths + read_document + green_reach + code_sort_key
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402

CHECK = "check-architecture-reference"


def _load_builder():
    """Load the (hyphen-named) builder module so the gate reuses its ONE parser — no re-implemented
    reader drifting from its sibling (the same one-reader discipline specformat.py holds for the index
    gates, and archformat.py holds for the node shape itself)."""
    path = os.path.join(REPO_ROOT, "scripts", "build-architecture-reference.py")
    spec = importlib.util.spec_from_file_location("build_architecture_reference", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    if len(argv) < 3:
        print("%s: usage: %s <ARCHITECTURE.md> [<part.md> ...] <committed-index.md>"
              % (CHECK, os.path.basename(argv[0])))
        return 2
    # The architecture may arrive as a core plus its parts (specformat's parts map); the committed
    # index is always the LAST argument and the ones before it are the architecture, read as one
    # concatenation — the same shape check-matrix-reference.py already carries.
    index_path = argv[-1]
    doc_paths = sf.spec_paths(argv[1:-1])
    for p in doc_paths + [index_path]:
        if not os.path.isfile(p):
            print("%s: cannot read %s — the gate stands on the architecture file and the committed "
                  "Reference." % (CHECK, p))
            return 1
    doc_names = [os.path.basename(p) for p in doc_paths]
    _read, text = sf.read_document(doc_paths, expand=False)

    b = _load_builder()

    try:
        nodes = b.parse_nodes(text)
    except ValueError as e:
        print("%s: %s" % (CHECK, e))
        return 1

    try:
        require_nonempty(CHECK, "the architecture node sections", nodes)
    except VacuousInputError as e:
        print("%s: %s" % (CHECK, e))
        return 1

    with open(index_path, encoding="utf-8") as f:
        committed = f.read()

    fresh = b.build_reference_table(nodes)
    owned = b.node_anchors(nodes)
    committed_codes = b.table_anchors(committed)

    problems = []
    if committed.strip() != fresh.strip():
        problems.append("the summary table doesn't match what a fresh rebuild of the current node "
                        "sections produces (INV-315).")
    missing = sorted(owned - committed_codes, key=sf.code_sort_key)
    if missing:
        problems.append("%d requirement(s) a node claims to own are missing from the summary table "
                        "(INV-315): %s" % (len(missing), ", ".join(missing)))
    orphan = sorted(committed_codes - owned, key=sf.code_sort_key)
    if orphan:
        problems.append("%d requirement(s) listed in the summary table are owned by no node — an "
                        "empty entry (INV-315): %s" % (len(orphan), ", ".join(orphan)))
    # INV-322, the format family's map law: a part file sitting among the named parts that the map
    # names nowhere. The three faults above read the assembled text, which an unnamed part never
    # reaches, so they agree with each other about a document short of what the tree holds.
    unnamed = sf.unnamed_parts(doc_paths[0])
    if unnamed:
        problems.append("%d file(s) sit among the document's parts and the parts map names none of "
                        "them, so nothing reads them (INV-322): %s — add a row for each to the "
                        "`## Parts map` table, or move the file out of the parts directory."
                        % (len(unnamed), ", ".join(unnamed)))

    if problems:
        print("FAIL (architecture reference): the architecture's summary table no longer matches its "
              "own nodes (%s vs %s):" % (", ".join(doc_names), os.path.basename(index_path)))
        for p in problems:
            print("  - %s" % p)
        print("  Fix: ask your agent to rebuild the table (scripts/build-architecture-reference.py) "
              "and commit the refreshed version.")
        return 1

    n_nodes = len(nodes)
    print(sf.green_reach(CHECK, doc_names + [os.path.basename(index_path)], n_nodes, n_nodes,
                         "committed Reference equals the fresh build; %d anchors agree node-to-table"
                         % len(owned)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
