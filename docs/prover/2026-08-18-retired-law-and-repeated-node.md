# Prover record — 2026-08-18 retired-law-and-repeated-node

PUSH-REVIEW

Range: 51104be0..0b939c2e
- 28dff1e The record names the pushed range by its hashes
- 80d15fa The record names the server's two findings
- 0b939c2e The record carries the server's two findings
- d135358 A retired law leaves an empty number, and the new node points instead of repeating
Files read: ARCHITECTURE.md, tests/test_formal_index.py, tests/test_convergence_locks.py, scripts/spec-redundancy-precheck.py
Findings: retiring a law costs edits in several hand-pinned places, and that is a class worth closing — the detail is below
Blocking: none

A retired law leaves an empty number, and the new node points instead of repeating.

Root: the server refused the previous push on two counts, both left by the text-audit
extraction. The new architecture node for text-audit restated the product-prover node's
sentence about pins standing on a tracked adapter, near enough word for word, and the
redundancy check counted two open pairs against a floor of none. Separately, retiring the
growable-doc ceiling took its law, INV-234, out of the index, and the index test pins the
set of holes it expects.

What happened: the node now points at the product-prover node for the reason rather than
saying it again. The index test records INV-234 as an expected hole with the reason it
exists. Renumbering the laws after it was never a candidate: every citation written before
today would then mean something else.

Checks run: `tests/test_formal_index.py` and `tests/test_convergence_locks.py` — 7 passed.
`spec-redundancy-precheck.py ARCHITECTURE.md` — 0 open pairs, down from 2. The style lint
over the same document — 0 errors. The census was rebuilt over the edited tree.

Findings:
- Retiring one law cost edits in several places that each keep their own hand-pinned list:
  the index's expected holes here, and earlier today the CI mirror, the red-proof roster and
  the check registry. Each list is honest on its own, and together they mean a retirement is
  only as complete as the person doing it remembers. The class fix is to declare a
  retirement once — the attic manifest is the natural home, since a retired thing already
  moves there — and have the lists read that declaration rather than carry their own copy.
  It is not built here: main was red while this was written, and a consolidation is not
  work to do at speed. It stands first in the handoff for tomorrow.
- The duplication caught here is the same one the pack removes from its own documents all
  day. It arrived in a node written an hour after the extraction, by a worker who had just
  read the node it copied. Proximity is what makes a restatement feel like precision.

Blocking:
- none.
