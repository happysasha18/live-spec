# Prover record — 2026-09-03, Requirement 309 restored from the attic

Prover version: 1.6.2 (external skill, `skills/product-prover/`), under `product-prover-pack` 6.1.0.
Mode: new-surface review — one requirement re-entering the live document, read for whether it still
fits the tree it left.

Not a push review: no range is measured here, and this record carries none. It covers exactly one
commit's delta. The push that carries this work owes its own record.

Scope: `061d1294` alone, the commit that restored `spec/work-board.md` Requirement 309 and
`matrix/work-board.md` from `attic/` after `q-813` retired them past the owner's own already-recorded
2026-09-02 12:46 word. This record does not re-derive
`docs/prover/2026-09-03-full-range-adversarial-review.md`, which read the same chapter in the other
direction — its retirement — and closed the `INV-308`/`INV-67` handoff chain as correctly withdrawn.
That verdict was right for the tree it read. This one reads the restoration.

Files read: `git show 061d1294` whole (18 files, both renames out of `attic/`),
`spec/work-board.md` (Requirement 309, all 96 criteria), `spec/live-status-reporting.md`
(Requirement 310, whole), `matrix/work-board.md` (all 26 rows), `PRODUCT_SPEC.md` (glossary and
Parts map), `PRODUCT_SPEC.index.md`, `architecture/exchange.md`, `architecture/seams.md`,
`architecture/runtime-and-placement.md`, `architecture/quality-budgets.md`,
`architecture/feature-coverage.md`, `ARCHITECTURE.md`, `TEST_MATRIX.md`, `attic/MANIFEST.md`,
`tests/test_traceability.py` (`TARGET_ROW_OWNERS` and `TestTargetOwnership` whole),
`tests/test_formal_index.py` (`EXPECTED_GAPS` and its comment trail), `PLAN.md` rows `q-166`,
`q-813` and `q-816`, `docs/queue-archive/rotated-PLAN-2026-09-03-q811-declined.md`.

Checks run, each on the restored tree:
`python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md` — OK, 401 of 401
rows, 401 codes agree body-to-table, the map names all 33 parts and 312 requirement numbers each
claimed once.
`python3 guardrails/check-matrix-reference.py TEST_MATRIX.md TEST_MATRIX.index.md` — OK, 561 of 561
rows, 408 anchors agree.
`python3 guardrails/check-requirement-shape.py PRODUCT_SPEC.md` — OK, 1799 criteria well-shaped
across 312 requirements.
`python3 guardrails/check-vocabulary.py PRODUCT_SPEC.md` — OK, 262 rows, every glossary term used in
the body, no banned coinage.
`python3 scripts/spec-style-lint.py spec/work-board.md` and the same on
`spec/live-status-reporting.md` — 0 errors, 0 warnings each.
`python3 -m pytest -q tests/test_traceability.py tests/test_formal_index.py` — 189 passed, 2 skipped.
`python3 -m pytest -q tests/test_vocabulary_check.py tests/test_spec_parts.py
tests/test_style_lint_parts.py tests/test_clean_context_review.py
tests/test_redundancy_precheck_parts.py` — 52 passed, 2 skipped.
`grep -rn "ROADMAP row 166"` and `grep -rn "\[target: row"` over `matrix/`, `architecture/`,
`TEST_MATRIX.md`, `spec/` and `PLAN.md` — counted by hand, reported in F1.

## What the restoration got right

The mechanical half is clean and it is clean everywhere, which is worth saying before the finding
below. The renumbering held: the three retired heartbeat criteria came out and the remaining 96
renumbered continuously with no gap, and `check-requirement-shape.py` reads all of them well-shaped.
The two `[target]` markers came back in the right places — one under the requirement heading, one
under criterion 8, whose trailing bracket `[INV-308, INV-67]` is the pair `target_marker_anchors()`
actually reads — and `TARGET_ROW_OWNERS` names `q-816` for exactly those two anchors and nothing
else, so `test_targets_owned_by_open_rows` closes on the real row rather than on a comment.
`q-816` is a real `⬜` row in `## Tasks` with a checkable trigger (package 2 closing, cited to
`.live-spec/turnkey-contract-composed.md:305` and `q-806`'s own acceptance), which is a genuine
improvement on `q-811`'s "a real ask for it" — the exact defect that got `q-811` declined.
`tests/test_formal_index.py`'s `EXPECTED_GAPS` dropped `INV-308`–`INV-313` in the same commit, so no
invariant is declared retired while its criteria stand. `attic/MANIFEST.md` records the move back
rather than leaving two stale entries. The one piece the owner's same 12:46 word did retire — the
~5-second refresh heartbeat — stayed retired in all four of its homes: the three criteria, the two
matrix-fact halves (M-540, M-542), and the `architecture/quality-budgets.md` budget row, each naming
`.live-spec/turnkey-contract-composed.md:304` as the reason. That is a careful cut, not a bulk revert.

## F1 — The restoration re-pointed one home of the owning-row fact and left thirty-two naming a row that closed without it

> `"INV-308": "q-816",  # the work board surface, kept and deferred until after package 2`
> — `tests/test_traceability.py`, `TARGET_ROW_OWNERS`

> "| Requirement 309 [target: row 166] | a wish arrives → build-pipeline (door, intake) → …"
> — `architecture/runtime-and-placement.md:30`

The commit moves the ownership of the unbuilt work board from the declined `q-811` to the fresh
`q-816`, and it moves it in one place. Every other place in the tree that names an owning row for
the same promise still names row 166, and `q-166` is `✅` in `PLAN.md`. Thirty-two pointers:

- `matrix/work-board.md` — 27, of which 25 are the forward-tense cell "lands with the generator
  (ROADMAP row 166)". The block's own header sentence says every owning-test cell "names the landing
  that carries the row's test."
- `architecture/exchange.md` — 2: the `work-board` node's responsibility line, and the note reading
  "the source file's name and the generator's path land with the machinery at row 166."
- `architecture/runtime-and-placement.md` — 1, the runtime row's own `[target: row 166]` tag.
- `architecture/quality-budgets.md` — 1, the work-board budget row's watcher cell: "the generator's
  own suite timing assertion at its landing (ROADMAP row 166)."
- `TEST_MATRIX.md` — 1, the artifact-inventory row added by this same commit.

Row 166 did not merely close; it disowned the work in its own closing text — "Nothing past the cheap
first leg is built — no card shape, no columns, no worker lanes", and "The two `[target]` lines this
row owned there (`INV-308`, `INV-67`) move to a fresh row." So these thirty-two cells do not name a
landing that already happened and carried them; they name one that happened and refused them.

This is not the general staleness of `ROADMAP row N` prose across the matrix. Elsewhere those
pointers are past-tense records of where a test landed, and they are accurate. `matrix/work-board.md`
is the only matrix file in the tree using the forward-tense "lands with … (ROADMAP row N)" form —
25 of the 25 in existence are in it. The sharpest instance is
`architecture/runtime-and-placement.md`, which carries exactly two `[target: row N]` tags: row 385,
whose `q-385` is a live `⬜`, and row 166, whose row is closed. Same table, same convention, one live
and one dead.

Who is affected and how: a session picking `q-816` up when package 2 closes reads its acceptance,
follows the matrix to find which tests it owes, and every cell tells it the tests belong to a landing
that finished on 2026-09-02. A reviewer running the reverse check — is this unbuilt block owned by an
open row? — gets a yes from `TARGET_ROW_OWNERS` and a no from all four documents.

Nothing mechanical catches it, and I checked rather than assumed: `check-matrix-reference.py`
validates ids and anchors, not the owning-test prose; `TARGET_ROW_OWNERS` validates the anchor map,
not the cells; `tests/test_traceability.py:290`'s owning-test assertion fires only on rows marked
BUILT, and all 26 of these read *todo*.

Proposed action: re-point the thirty-two to `q-816`, the same re-point the commit already made once.
No new gate is owed — the drift here is that one fact has five homes and the commit updated one, not
that a check is missing.

Not blocking: nothing is built, so nothing behaves wrong today, and the promise is genuinely owned by
an open row in the one home a test reads.

## F2 — The new criterion 10 in Requirement 310 promises a switch that q-816's own acceptance does not reach

> "That home *shall* be the work board's per-task plan once the board ships, and the written plan page
> until then. [INV-314, INV-308]" — `spec/live-status-reporting.md` R310 criterion 10

The commit splits R310's old criterion 9 in two and gives the new half a forward promise: once the
board ships, the announcement home for a work block moves from the written plan page to the board's
per-task plan. It is honestly written — it names both states and gates the unbuilt one on the ship —
and it carries `INV-308`, whose owner is `q-816`, so the anchor-level tie holds.

The acceptance on `q-816` does not. It reads "unchanged from `spec/work-board.md` Requirement 309's
own criteria, minus the retired heartbeat clauses above", which is scoped to one file. R310
criterion 10 lives in another. So the row that owns `INV-308` can close on its own stated acceptance
with criterion 10's switch never made, and the document would then promise a home that is not the
home in use.

Who is affected and how: whoever builds the board and closes `q-816` by its own words, leaving one
criterion in a different chapter quietly false.

Proposed action: name `spec/live-status-reporting.md` R310 criterion 10 in `q-816`'s acceptance, one
clause. This is narrow and cheap; it is reported rather than treated as a gap in the spec, because
the criterion itself is written correctly.

## What else this pass looked for, and found clean

**The column set against the live status vocabulary.** The queue's closed status vocabulary is
*queued*, *ready*, *in-work*, *deferred*, *far* (`spec/doc-order-generated.md` R-block criterion 2,
INV-277). Requirement 309 answers all five: criteria 20 and 22 give columns to *queued*, *ready* and
*in-work*; criterion 25 shows *deferred* as a stated count; criterion 23 keeps the far tier off the
board under its own request law. No status is left with no answer. Criterion 20's headline sentence
("one column per recorded state") reads wider than the four columns its own bullet names, but 23 and
25 carve the two exceptions out explicitly rather than leaving a blank — pre-existing wording,
restored verbatim, not a gap.

**The reopened state.** `🔁` joined the board's icon set on 2026-09-02, while Requirement 309 sat in
the attic — the obvious candidate for a promise that stopped fitting while it was away. It does not
apply: reopened is computed from a row's own acceptance command for the Canon's icon set, not a word
of the five-cell status vocabulary R309 criterion 22 reads its columns off. Nothing to reconcile.

**Duplicate promise between the restored chapter and its neighbours.** R309 criterion 34 ("show an
in-work row's plan on its board row") against R310 criterion 10 ("that plan is the home a block is
announced against"): different duties on one object, not one duty in two homes. Criteria 1–5 of R309
are the explicit non-encroachment case, each naming the neighbour whose scope it leaves alone
(INV-27, INV-35, INV-93, INV-38, INV-71), and each still matches its neighbour's live text.

**Orphaned pointers other than F1's.** `docs/norms/work-board.html` exists (51 KB, the frozen norm
criterion 15 cites). `WAITING.md`, `docs/queue-archive/` and `.live-spec/turnkey-contract-composed.md`
all exist at the cited paths. `attic/spec-work-board-R309.md` and `attic/matrix-work-board-R309.md`
are gone from `attic/` and from `attic/MANIFEST.md`'s live entries, replaced by a dated move-back
note — no dangling manifest line. `PLAN.md`'s `q-166` still names `q-811` as where the two anchors
went, which is a dated record of 2026-09-02 rather than a live pointer, and reads correctly as one.

**The glossary delta.** Five terms added (board row, card, chip, craft name, work board) and one
amended (echo-name). `check-vocabulary.py` reads every glossary term as used in the body and no
banned coinage present, over the whole 33-part document.

**Both generated indexes and the matrix Reference.** All three equal a fresh build. The Parts map
gained its `spec/work-board.md | R309` row and 312 requirement numbers are each claimed once.

## Class lens

One class, one finding. F1's class is a fact with several homes where a correction updates the home a
test reads and leaves the homes only a person reads. Swept for siblings inside this delta: the
heartbeat retirement is the same shape and was done correctly in all four of its homes, and the
`INV-308`–`INV-313` gap declaration was updated in `test_formal_index.py` in the same commit. So the
sweep found one instance, not a habit — the restoration was thorough everywhere except the row
number.

F2 is not a second instance of that class. It is a promise whose owning row's acceptance is narrower
than the promise, which is a different defect and reported separately.

## Verdict

The restoration is right and it is carefully done. Requirement 309 reads consistently with the live
spec: its anchors resolve, its criteria renumber cleanly, its cross-references into
`PRODUCT_SPEC.index.md` and `spec/live-status-reporting.md` hold, its `[target]` markers land on a
real open queue row with a real trigger, and every mechanical consistency check in the tree passes on
the restored state. The one substantive finding is that the row number the promise is owed to was
updated in one home and left stale in thirty-two others.

Findings: F1 (thirty-two pointers naming a closed row, non-blocking, no fix made — review only),
F2 (a criterion outside `q-816`'s stated acceptance, narrow, non-blocking, no fix made).

Blocking: none.
