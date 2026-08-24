#!/usr/bin/env python3
"""check-architecture-reference.py — the generated architecture-Reference gate (SPEC INV-315, INV-269).

Gate z. The architecture (a core plus any parts) and the committed index are named on the command
line, the sibling shape of the matrix-reference gate (`guardrails/check-matrix-reference.py`, gate d)
and the generated-index gate (`guardrails/check-index-generated.py`, gate x).

THE LAW: the committed index carries TWO generated tables, both built from the node sections at
freeze and output only (INV-315):

  1. `| Anchor | Nodes |` maps each spec anchor to the node names that own it. This gate holds three
     anchor-table faults:
       - DRIFT: the committed table differs from a fresh build off the current node sections — a
         hand edit, or nodes that moved without a rebuild. Reds, since the table is not hand-kept.
       - A NODE OWNS AN ANCHOR THE TABLE MISSES: an anchor on a node's owns field absent from the
         committed table. Reds, naming the anchor.
       - THE TABLE HAS AN ANCHOR NO NODE OWNS: an anchor in the committed table owned by no node — an
         empty home. Reds, naming the anchor.

  2. `| Node | Part | Responsibility |` routes each node to the part file its section lives in today,
     with a one-line generated copy of its own responsibility field. This gate holds two more faults:
       - DRIFT: the committed router table differs from a fresh build. Reds, since it is generated
         output, never a second hand-kept home for a node's responsibility.
       - A NODE WITH NO PART FILE: a node the anchor table's own node list carries that the router
         build could not place in any of the named files — the desync the router table exists to
         catch ahead of a stale reader. Reds, naming the node.

It declares its expected-non-empty input with the shared guard (INV-218): a document that parses to
zero node sections reds by name rather than passing over nothing.

Usage:
  check-architecture-reference.py <ARCHITECTURE.md> [<part.md> ...] <committed-index.md>
Exit 0 when both committed tables equal a fresh build and the nodes and tables agree (printing the
reach line, INV-269); exit 1 naming each fault; exit 2 on a usage error. Stdlib only.
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
                  "index." % (CHECK, p))
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

    fresh_anchor = b.build_reference_table(nodes)
    part_of = b.node_to_part(doc_paths)
    fresh_router = b.build_router_table(nodes, part_of)

    committed_anchor, committed_router = b.split_tables(committed)

    owned = b.node_anchors(nodes)
    committed_codes = b.table_anchors(committed_anchor)

    problems = []
    if committed_anchor.strip() != fresh_anchor.strip():
        problems.append("the committed Anchor table differs from a fresh build off the current node "
                        "sections — the table is generated output, never hand-kept; rebuild it with "
                        "scripts/build-architecture-reference.py (INV-315).")
    missing = sorted(owned - committed_codes, key=sf.code_sort_key)
    if missing:
        problems.append("%d anchor(s) on a node's owns field are absent from the committed Anchor "
                        "table (INV-315): %s" % (len(missing), ", ".join(missing)))
    orphan = sorted(committed_codes - owned, key=sf.code_sort_key)
    if orphan:
        problems.append("%d anchor(s) in the committed Anchor table are owned by no node — an empty "
                        "home (INV-315): %s" % (len(orphan), ", ".join(orphan)))

    no_part = sorted(n.name for n in nodes if n.name not in part_of)
    if no_part:
        problems.append("%d node(s) could not be placed in any of the named files while building the "
                        "router table — a node section that moved with no matching file argument "
                        "(INV-315): %s" % (len(no_part), ", ".join(no_part)))
    if committed_router.strip() != fresh_router.strip():
        problems.append("the committed Node/Part/Responsibility router table differs from a fresh "
                        "build off the current node sections — it is generated output, never a second "
                        "hand-kept home for a node's responsibility; rebuild it with "
                        "scripts/build-architecture-reference.py (INV-315).")

    if problems:
        print("%s: %d Reference fault(s) between %s and %s:"
              % (CHECK, len(problems), ", ".join(doc_names), os.path.basename(index_path)))
        for p in problems:
            print("  - %s" % p)
        return 1

    n_nodes = len(nodes)
    print(sf.green_reach(CHECK, doc_names + [os.path.basename(index_path)], n_nodes, n_nodes,
                         "committed Anchor and router tables equal a fresh build; %d anchors agree "
                         "node-to-table, %d nodes routed to their parts" % (len(owned), n_nodes)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
