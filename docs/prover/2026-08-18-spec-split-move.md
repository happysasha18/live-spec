# Prover record — 2026-08-18 spec-split-move

PUSH-REVIEW

Range: ebc4d428..bd3940f8
- bd3940f8 The record follows the base main moved to
- 01c87da Fix two push-gate findings from the spec split: shipped-language and a whole class of spec-by-path readers
- cf343a7 Merge origin/main: the skills-lines cull lands under the split
- 43efc57 The record names the pushed range by its hashes
- f2df205 The record carries the split and its merge
- ef4cfdc Merge spec/2026-08-18-split-move into deliver/spec-split
- 39cdc94 Census re-record after the spec split: 30 spec/*.md entries + shrunk core
- d79fc33 Spec split, move: 310 requirements out of PRODUCT_SPEC.md into 30 spec/*.md parts
- 9dc1a9f Merge remote-tracking branch 'origin/main' into spec/2026-08-18-split-move
- b6d7cd9 The loop variable is followed one step, and the limits are written down where they hold
- 56f179a The last binding is the one that stands, and a walk-up that descends is not the root
- 2f43f3e A name is bound by assignment too, and the root is judged by its value
- 8e28684 The rule follows a reader across a re-export, and a lambda is a function too
- fe27b4a A helper is a reader because of what its body does, and the node is the node because of where it came from
- edcf8db The rule is read off the parsed tree, and it finds the readers a substring scan cannot
- f3d02bf Every test that opened the spec by path reads it through the node instead
- 5c0eaba Every reader of the spec reads it as one document, whether it is one file or thirty
Files read: PRODUCT_SPEC.md, PRODUCT_SPEC.index.md, spec/*.md, tests/conftest.py, guardrails/doc-bounds.json, guardrails/rule-census.json, TEST_MATRIX.md, ARCHITECTURE.md
Findings: the design said seven test files read the spec by path and the tree held about a hundred, and the merge with today's five landed packages needed five conflicts resolved line by line — both are set out below
Blocking: none

The specification becomes a core and thirty parts, and every requirement keeps its words.

Root: PRODUCT_SPEC.md stood at 703,125 bytes. A reader looking for one requirement opened
a document nobody can hold, and every worker that touched the spec paid that size in
context before doing any work. The split was designed as a core plus one file per feature,
and its foundation — the reader node every test goes through — landed first, proved by 473
node reads and no walk-arounds.

What happened: 310 requirements move word for word into thirty `spec/*.md` parts. The core
keeps the preamble, the glossary and a new map of the parts, and stands at 50,158 bytes.
The trailing `## Reference` section goes: it was a byte-for-byte duplicate of the index,
which closes ROADMAP row 621. `tests/conftest.py`'s reader synthesises that Reference from
`PRODUCT_SPEC.index.md` when no physical section exists, so every reader still sees one
document whether it is one file or thirty.

The accounting closes to the byte. 311 requirements, 630,742 bytes of requirement text, are
byte-identical before and after. The whole-tree figure closes too: 705,814 bytes on main
equals 680,900 in the core and the parts, plus 24,914 — and that 24,914 is 28,404 bytes of
deleted duplicate Reference less 3,490 bytes of the new requirement 311 line in the parts
map. Nothing was summarised, and nothing was invented.

The merge onto today's main took five conflicts, each resolved line by line rather than by
taking a side. `tests/conftest.py` keeps both hunks — this morning's stripping of git's own
environment variables and this package's Reference synthesis. `PRODUCT_SPEC.md` takes the
shrunk core and gains requirement 311 in its parts map, byte for byte from the judges
package. `guardrails/doc-bounds.json` takes the measured size of the merged TEST_MATRIX.md
rather than the sum of two hunks, because a third package had touched that file too. The
two generated files were rebuilt by their own scripts.

Checks run: the targeted set over spec, index, matrix and traceability — 18 files, 360
passed, 1 skipped. A wider background run over the 151 files that read the spec was green
where it reached before this record was written; it is not claimed as complete. The working
copy was checked: no fabricated commits, no missing files.

Findings:
- The design said seven test files opened the spec by path. The tree held about a hundred.
  The gap was found by doing the move, not by reading the design, and it was closed at one
  point — the reader node — rather than in a hundred places. A design's count of its own
  blast radius is a guess until someone moves the thing.
- Two packages rewrote the same rows of TEST_MATRIX.md an hour apart today, and a third
  touched the same size record. Taking either side of those conflicts wholesale would have
  dropped real work silently. In a repository where several lanes edit one document in one
  day, line-by-line resolution is not fussiness, it is the only correct merge.
- The core is now 50,158 bytes against 703,125. A worker that needs one requirement no
  longer pays for 653,000 bytes it will not read.

Blocking:
- none.
