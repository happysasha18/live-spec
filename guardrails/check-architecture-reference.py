#!/usr/bin/env python3
"""check-architecture-reference.py — the generated architecture-Reference gate (SPEC INV-315, INV-269).

Gate z. The architecture and the committed Reference are named on the command line, the sibling shape of
the matrix-reference gate (`guardrails/check-matrix-reference.py`, gate d) and the generated-index gate
(`guardrails/check-index-generated.py`, gate x).

THE LAW: the architecture's Reference maps each spec anchor to the node names that own it, built from the
node sections' owns fields at freeze and output only (INV-315). This gate holds three faults:

  - DRIFT: the committed Reference differs from a fresh build off the current node sections — a hand
    edit, or nodes that moved without a rebuild. Reds, since the Reference is not hand-kept.
  - A NODE OWNS AN ANCHOR THE REFERENCE MISSES: an anchor on a node's owns field absent from the
    committed Reference. Reds, naming the anchor.
  - THE REFERENCE HAS AN ANCHOR NO NODE OWNS: an anchor in the committed Reference owned by no node — an
    empty home. Reds, naming the anchor.

It declares its expected-non-empty input with the shared guard (INV-218): a document that parses to zero
node sections reds by name rather than passing over nothing.

Usage:
  check-architecture-reference.py <ARCHITECTURE.md> <committed-index.md>
Exit 0 when the committed Reference equals the fresh build and the nodes and the Reference agree
(printing the reach line, INV-269); exit 1 naming each fault; exit 2 on a usage error. Stdlib only.
"""
import importlib.util
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)
import specformat as sf  # noqa: E402 — green_reach + code_sort_key
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
    if len(argv) != 3:
        print("%s: usage: %s <ARCHITECTURE.md> <committed-index.md>" % (CHECK, os.path.basename(argv[0])))
        return 2
    arch_path, index_path = argv[1], argv[2]
    for p in (arch_path, index_path):
        if not os.path.isfile(p):
            print("%s: cannot read %s — the gate stands on the architecture file and the committed "
                  "Reference." % (CHECK, p))
            return 1
    arch_name = os.path.basename(arch_path)
    index_name = os.path.basename(index_path)

    with open(arch_path, encoding="utf-8") as f:
        text = f.read()

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
        problems.append("the committed Reference differs from a fresh build off the current node "
                        "sections — the table is generated output, never hand-kept; rebuild it with "
                        "scripts/build-architecture-reference.py (INV-315).")
    missing = sorted(owned - committed_codes, key=sf.code_sort_key)
    if missing:
        problems.append("%d anchor(s) on a node's owns field are absent from the committed Reference "
                        "(INV-315): %s" % (len(missing), ", ".join(missing)))
    orphan = sorted(committed_codes - owned, key=sf.code_sort_key)
    if orphan:
        problems.append("%d anchor(s) in the committed Reference are owned by no node — an empty home "
                        "(INV-315): %s" % (len(orphan), ", ".join(orphan)))

    if problems:
        print("%s: %d Reference fault(s) between %s and %s:" % (CHECK, len(problems), arch_name, index_name))
        for p in problems:
            print("  - %s" % p)
        return 1

    n_nodes = len(nodes)
    print(sf.green_reach(CHECK, [arch_name, index_name], n_nodes, n_nodes,
                         "committed Reference equals the fresh build; %d anchors agree node-to-table"
                         % len(owned)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
