#!/usr/bin/env python3
"""check-index-generated.py — the generated-index gate (SPEC INV-258, INV-259).

UNARMED until the spec-format conversion delivery (INV-270); the document and the committed index are
named on the command line.

THE LAW: the code-to-location table is generated from the body criteria at freeze and is output only
(INV-258). This gate holds three faults:

  - DRIFT (INV-258): the committed table differs from a fresh build off the current body — a hand edit,
    or a body that moved without a rebuild. Reds, since the table is not hand-kept.
  - BODY HAS A CODE THE INDEX MISSES (INV-259): a code on a body criterion absent from the committed
    table. Reds, naming the code.
  - INDEX HAS A CODE THE BODY MISSES (INV-259): a code in the committed table carried by no body
    criterion — an empty home. Reds, naming the code.

It declares its expected-non-empty input with the shared guard (INV-218): a body that parses to zero
coded criteria reds by name rather than passing over nothing.

Usage:
  check-index-generated.py <document.md> [<part.md> ...] <committed-index.md>
Exit 0 when the committed table equals the fresh build and body and table agree (printing the reach
line, INV-269); exit 1 naming each fault. Stdlib only.
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
import specformat as sf  # noqa: E402
from nonempty_input import require_nonempty, VacuousInputError  # noqa: E402

CHECK = "check-index-generated"


def main(argv):
    if len(argv) < 3:
        print("%s: usage: %s <document.md> [<part.md> ...] <committed-index.md>"
              % (CHECK, os.path.basename(argv[0])))
        return 2
    # The document may arrive as a core plus its parts (specformat's parts map); the committed index
    # is always the LAST argument and the ones before it are the document, read as one concatenation.
    # The table is aggregate over that whole document, so a part left out of the list is a body the
    # committed table then over-carries, and the orphan-code fault below is what says so (INV-259).
    index_path = argv[-1]
    doc_paths = sf.spec_paths(argv[1:-1])
    for p in doc_paths + [index_path]:
        if not os.path.isfile(p):
            print("%s: cannot read %s — the gate stands on the document and the committed index."
                  % (CHECK, p))
            return 1
    doc_names = [os.path.basename(p) for p in doc_paths]
    _read, doc_text = sf.read_document(doc_paths, expand=False)
    doc = sf.parse(doc_text)
    with open(index_path, encoding="utf-8") as f:
        committed = f.read()

    body = sf.body_codes(doc)
    try:
        require_nonempty(CHECK, "the body's coded criteria", body)
    except VacuousInputError as e:
        print("%s: %s" % (CHECK, e))
        return 1

    fresh = sf.build_index_table(doc)
    committed_codes = sf.index_table_codes(committed)

    problems = []
    # INV-258: drift between the committed table and a fresh build.
    if committed.strip() != fresh.strip():
        problems.append("the summary index doesn't match what a fresh rebuild of the body produces "
                        "(INV-258).")
    # INV-259: body has a code the index misses.
    missing = sorted(body - committed_codes, key=sf.code_sort_key)
    if missing:
        problems.append("%d requirement(s) in the body are missing from the summary index "
                        "(INV-259): %s" % (len(missing), ", ".join(missing)))
    # INV-259: index has a code the body misses.
    orphan = sorted(committed_codes - body, key=sf.code_sort_key)
    if orphan:
        problems.append("%d requirement(s) listed in the summary index aren't backed by any criterion "
                        "in the body — an empty entry (INV-259): %s" % (len(orphan), ", ".join(orphan)))

    if problems:
        print("FAIL (index generated): the document's summary index no longer matches its own body "
              "(%s vs %s):" % (", ".join(doc_names), os.path.basename(index_path)))
        for p in problems:
            print("  - %s" % p)
        print("  Fix: ask your agent to rebuild the index (scripts/build-index.py) and commit the "
              "refreshed version.")
        return 1

    print(sf.green_reach(CHECK, doc_names + [os.path.basename(index_path)],
                         len(body), len(body),
                         "committed index equals the fresh build; %d codes agree body-to-table"
                         % len(body)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
