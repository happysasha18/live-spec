#!/usr/bin/env python3
"""check_conflicts.py — structural drift across the docs is red (SPEC INV-97).

Four sub-checks: (a) duplicate anchor ids in the spec's index table; (b) an INV-* id
in the spec index that no matrix row cites; (c) a ⟨DECIDE⟩ marker on a line that also
says RESOLVED (both live and settled — pick one); (d) a surface named twice in the
registry. These are the inconsistencies that make a prover's findings unreliable.

Usage: python3 check_conflicts.py   (config: $GUARDRAILS_CONFIG or
./guardrails.config.json; run from the host repo root)

Python 3.9 stdlib only.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gate_lib  # noqa: E402

CHECK = "conflicts"
INDEX_ROW = re.compile(r"^\|\s*([A-Za-z]+-\d+)\s*\|")


def main():
    config, root = gate_lib.load_config(CHECK)
    spec_rel = gate_lib.require_key(CHECK, config, "spec_path")
    gate_lib.require_path(CHECK, root, spec_rel, "spec")
    matrix_rel = gate_lib.require_key(CHECK, config, "matrix_path")
    gate_lib.require_path(CHECK, root, matrix_rel, "matrix")
    registry_rel = gate_lib.require_key(CHECK, config, "registry_path")
    registry_path = gate_lib.require_path(CHECK, root, registry_rel, "registry")

    # The spec, and the matrix alike, may be written as a core file plus part files
    # (SPEC INV-259): read each as the one document every other reader in the suite
    # sees — core, parts, and its generated index — never a single file that may hold
    # only a fraction of it. `read_spec` reads either kind of document; its name is the
    # first caller it gained, not a limit on what it reads.
    spec = gate_lib.read_spec(CHECK, root, spec_rel)
    matrix = gate_lib.read_spec(CHECK, root, matrix_rel)

    # (a) duplicate anchor ids in the spec's index table rows
    index_ids = [m.group(1) for line in spec.splitlines()
                 for m in [INDEX_ROW.match(line.strip())] if m]
    duplicates = sorted({i for i in index_ids if index_ids.count(i) > 1})
    if duplicates:
        gate_lib.fail(CHECK, "duplicate-anchor",
                      "anchor id(s) indexed more than once in %s: %s"
                      % (spec_rel, ", ".join(duplicates)),
                      "keep exactly one index row per anchor id — renumber or merge "
                      "the duplicates")

    # (b) every indexed INV-* must be cited by a matrix row
    for inv in sorted({i for i in index_ids if i.startswith("INV-")}):
        if not re.search(r"\|.*\b%s\b" % re.escape(inv), matrix):
            gate_lib.fail(CHECK, "invariant-without-row",
                          "spec invariant %s is indexed in %s but no row in %s cites it"
                          % (inv, spec_rel, matrix_rel),
                          "add a matrix row citing %s (or retire the invariant from "
                          "the spec index)" % inv)

    # (c) a ⟨DECIDE⟩ marker sharing a line with RESOLVED is both live and settled
    for doc_rel, text in ((spec_rel, spec), (matrix_rel, matrix)):
        for number, line in enumerate(text.splitlines(), 1):
            if "⟨DECIDE⟩" in line and "RESOLVED" in line:
                gate_lib.fail(CHECK, "resolved-but-live",
                              "%s:%d carries a ⟨DECIDE⟩ marker on a line "
                              "marked RESOLVED: %r" % (doc_rel, number, line.strip()[:120]),
                              "a resolved decision drops its ⟨DECIDE⟩ marker; "
                              "a live one is not RESOLVED — edit the line to say one thing")

    # (d) duplicate surface names in the registry
    names = [name for name, _n, _a in
             gate_lib.parse_registry(gate_lib.read_file(registry_path))]
    twice = sorted({n for n in names if names.count(n) > 1})
    if twice:
        gate_lib.fail(CHECK, "surface-named-twice",
                      "surface name(s) registered more than once in %s: %s"
                      % (registry_rel, ", ".join(twice)),
                      "one registry row per surface — merge or rename the duplicates")

    gate_lib.ok(CHECK, "%d indexed anchor(s), %d registered surface(s): no duplicates, "
                       "no invariant without a matrix row, no resolved-but-live marker"
                       % (len(index_ids), len(names)))


if __name__ == "__main__":
    main()
