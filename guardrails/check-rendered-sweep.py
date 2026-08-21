#!/usr/bin/env python3
"""check-rendered-sweep.py — a transient rendered page left standing reds (SPEC INV-286).

A rendered page is built to be read once, and the tree carried four of them at the root when
this check was written, the oldest eighteen days old and one of them a render of a document that
no longer exists under that name. The clearing was a habit nobody held, and a quality left to
attention fails without a sound. So the clearing gets a machine.

The rule this check reads is the renderer rule, stated once in `scripts/sweep-rendered.py` and
imported from there so the check and the sweep can never disagree: a page the pack's document
renderer produced is transient, and every other page in the tree is the artifact itself. The
check reds while a transient page still stands, and the sweep clears the red by moving it to the
attic — the same shape `check-earned-message.py` takes, where the red clears by declining the
message at the door.

WHERE IT RUNS. The gate rides the SUITE. The push chain's letters run a..z with every one taken,
and the pack already declares this placement for the checks that arrived after them — the
named-reference presence nets ride the suite too.
A suite-riding check carries no gate letter, and gate b already blocks a push on a red suite.

WHAT IT DOES NOT SEE. The check reads a page's MARK, and never whether the person finished
reading. A page rendered a minute ago and still open in a browser reds exactly like one that has
stood for a week. That bound is deliberate: the suite runs at verify and at landing, by which
point the exchange the page served has closed, and a rule that tried to read the person's
attention would guess. A directory reached only through a symbolic link stands outside the walk.
The reach stops at what version control tracks, and four homes stand outside it beside that; both
halves are named on the green line.

Usage:
  check-rendered-sweep.py [--root PATH]
Exit 0 when no transient rendered page stands; exit 1 with one line per page otherwise. Stdlib only.
"""
import argparse
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SWEEP = os.path.join(os.path.dirname(HERE), "scripts", "sweep-rendered.py")


def _load_sweep():
    """The classification's one home, loaded by path since the filename carries a hyphen."""
    spec = importlib.util.spec_from_file_location("sweep_rendered", SWEEP)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv=None):
    parser = argparse.ArgumentParser(description="red while a transient rendered page stands")
    parser.add_argument("--root", default=os.path.dirname(HERE))
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    if not os.path.isfile(SWEEP):
        print("FAIL (rendered sweep): scripts/sweep-rendered.py is missing, so the renderer rule "
              "has no home to be read from (SPEC INV-286).")
        return 1

    sweeper = _load_sweep()
    outside_reach = sweeper._config(root)
    transient, records = sweeper.classify(root)

    if transient:
        for rel, why in transient:
            print("%s: a page the document renderer produced, standing past its one reading — %s "
                  "(SPEC INV-286)" % (rel, why))
        print()
        print("A rendered page is cleared once its reading is over, and the clearing moves it to")
        print("the attic with its manifest line, deleting nothing (base rule 10). Run:")
        print()
        print("    python3 scripts/sweep-rendered.py")
        print()
        print("A page that belongs in the tree is the artifact itself, so it carries no")
        print("`%s` generator mark and no source document stands beside it." % sweeper.GENERATOR)
        print("Committing a page also puts it beyond the clearing, since removing tracked history")
        print("is a commit with its own gate. A host declares its own homes outside the reach")
        print("under `rendered_pages` in guardrails.config.json (SPEC INV-286, INV-224).")
        return 1

    print("OK (rendered sweep): no transient page stands. Read %d page%s under %s, every one an "
          "artifact carrying no `%s` mark and no source document beside it; everything version "
          "control tracks and the homes %s stand outside the reach (SPEC INV-286)."
          % (len(records), "" if len(records) == 1 else "s", root, sweeper.GENERATOR,
             " * ".join(outside_reach) or "(none)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
