# Prover record — 2026-08-18 stale-usage-pin

PUSH-REVIEW

Range: 99e526b9..81738e6e
- 81738e6e The record carries the stale pin
- 225d893f A fixture's pin follows the builder's usage after the split
Files read: tests/test_text_audit_fixtures.py, scripts/build-index.py
Findings: the split changed a command's usage line and a fixture still pinned the old one — the detail is below
Blocking: none

A fixture's pin follows the builder's usage line after the split.

Root: the server refused the spec split. `scripts/build-index.py` now takes the core and its
parts, so its usage reads `build-index.py <document.md> [<part.md> ...] -o <file>`, and a
text-audit fixture test pinned the older `build-index.py <document.md> -o <file>`. The pin
had nothing to do with the fixture's subject; it existed to notice exactly this — the test's
own message says "scripts/build-index.py changed the way it takes an output file; re-read
the fixture's command against the new usage". It did its job.

What happened: the pin is re-read against the current usage line. Nothing else moves. The
fixture still plants the same defect it always planted — a clean sentence teaching a command
that writes the wrong file — and its other assertions are untouched.

Checks run: `tests/test_text_audit_fixtures.py` — 9 passed.

Findings:
- Landing this repair by deleting the test was available and was refused. The package that
  extracts text-audit removes this file wholesale, and pushing that package would have taken
  main green without anyone reading why it was red. A red that disappears because its test
  left the tree is not a repair.
- This is the shape the day kept meeting: a record pinned to a number or a string, correct
  when written, quietly wrong after the thing it describes moves. The pin here was the good
  kind — it failed loudly and named its own repair.

Blocking:
- none.
