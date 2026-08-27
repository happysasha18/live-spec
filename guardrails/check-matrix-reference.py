#!/usr/bin/env python3
"""check-matrix-reference.py — the generated matrix-Reference gate (SPEC INV-273, INV-269).

UNARMED until the row-477 conversion delivery converts TEST_MATRIX.md to the format-family member and
splices in the generated Reference table; it arms in that same delivery (INV-272). The matrix and the
committed Reference are named on the command line, the sibling shape of the generated-index gate
(`guardrails/check-index-generated.py`).

THE LAW: the matrix's Reference maps each spec anchor to the matrix rows covering it, built from the
body rows at freeze and output only (INV-273). This gate holds three faults:

  - DRIFT: the committed Reference differs from a fresh build off the current body — a hand edit, or a
    body that moved without a rebuild. Reds, since the Reference is not hand-kept.
  - BODY HAS AN ANCHOR THE REFERENCE MISSES: an anchor on a body row absent from the committed
    Reference. Reds, naming the anchor.
  - REFERENCE HAS AN ANCHOR NO BODY ROW CARRIES: an anchor in the committed Reference carried by no
    body row — an empty home. Reds, naming the anchor.

It declares its expected-non-empty input with the shared guard (INV-218): a body that parses to zero
converted rows reds by name rather than passing over nothing.

Usage:
  check-matrix-reference.py <matrix.md> [<part.md> ...] <committed-index.md>
Exit 0 when the committed Reference equals the fresh build and body and Reference agree (printing the
reach line, INV-269); exit 1 naming each fault. Stdlib only.
"""
import importlib.util
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)
import specformat as sf  # noqa: E402 — spec_paths + read_document + green_reach + code_sort_key
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402

CHECK = "check-matrix-reference"


def _load_builder():
    """Load the (hyphen-named) builder module so the gate reuses its ONE parser — no re-implemented
    reader drifting from its sibling (the same one-reader discipline specformat.py holds for the
    index gates)."""
    path = os.path.join(REPO_ROOT, "scripts", "build-matrix-reference.py")
    spec = importlib.util.spec_from_file_location("build_matrix_reference", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    if len(argv) < 3:
        print("%s: usage: %s <matrix.md> [<part.md> ...] <committed-index.md>"
              % (CHECK, os.path.basename(argv[0])))
        return 2
    # The matrix may arrive as a core plus its parts (specformat's parts map); the committed
    # Reference is always the LAST argument and the ones before it are the matrix, read as one
    # concatenation.
    index_path = argv[-1]
    doc_paths = sf.spec_paths(argv[1:-1])
    for p in doc_paths + [index_path]:
        if not os.path.isfile(p):
            print("%s: cannot read %s — the gate stands on the matrix and the committed Reference."
                  % (CHECK, p))
            return 1
    doc_names = [os.path.basename(p) for p in doc_paths]
    _read, text = sf.read_document(doc_paths, expand=False)

    b = _load_builder()

    try:
        require_nonempty(CHECK, "the matrix body rows", b.parse_rows(text))
    except VacuousInputError as e:
        print("%s: %s" % (CHECK, e))
        return 1

    with open(index_path, encoding="utf-8") as f:
        committed = f.read()

    fresh = b.build_reference_table(text)
    body = b.body_anchors(text)
    committed_codes = b.table_anchors(committed)

    problems = []
    if committed.strip() != fresh.strip():
        problems.append("the summary table doesn't match what a fresh rebuild of the body produces "
                        "(INV-273).")
    missing = sorted(body - committed_codes, key=sf.code_sort_key)
    if missing:
        problems.append("%d requirement(s) covered in the body are missing from the summary table "
                        "(INV-273): %s" % (len(missing), ", ".join(missing)))
    orphan = sorted(committed_codes - body, key=sf.code_sort_key)
    if orphan:
        problems.append("%d requirement(s) listed in the summary table aren't covered by any row in "
                        "the body — an empty entry (INV-273): %s" % (len(orphan), ", ".join(orphan)))

    if problems:
        print("FAIL (matrix reference): the test matrix's summary table no longer matches its own body "
              "(%s vs %s):" % (", ".join(doc_names), os.path.basename(index_path)))
        for p in problems:
            print("  - %s" % p)
        print("  Fix: ask your agent to rebuild the table (scripts/build-matrix-reference.py) and "
              "commit the refreshed version.")
        return 1

    n_rows = len(b.parse_rows(text))
    print(sf.green_reach(CHECK, doc_names + [os.path.basename(index_path)], n_rows, n_rows,
                         "committed Reference equals the fresh build; %d anchors agree body-to-table"
                         % len(body)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
