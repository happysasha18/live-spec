# The test-matrix format — definition

This page defines the format the test matrix is written in. The matrix is a member of the same format family as the spec, and this page states only what is particular to the matrix. The shared family laws live once in `docs/spec-format.md`, and this page inherits them by reference rather than restating them.

## What the matrix inherits from the family

The matrix is written in the requirements genre `docs/spec-format.md` defines, and every law that page states holds here unchanged:

- the closed-vocabulary glossary, so every domain noun the matrix uses carries one glossary entry under one name;
- the criterion form, so the keywords *when*, *while*, *if*, *then*, and *shall* are set in lowercase italics, no word stands in all capitals outside a code anchor, and the code anchor trails at the line's end;
- the no-history law, so the matrix states today's coverage and its dates, provenance, and past reasons live in the journal;
- the generated-section gating, so a section a script builds is output only and a gate reds a hand edit of it;
- the comprehension gate, so a changed section clears the mechanical lints and then a panel of cold readers, passing only after two consecutive reads return zero blocking findings.

A reader who needs any of these consults `docs/spec-format.md`. The rest of this page adds the parts the matrix carries that the spec does not.

## What the matrix is

The matrix is the spec projected into a checkable grid. It is derived from the proven spec through the proven architecture, and the spec keeps sole authority over what is true; a fact the matrix carries that the spec does not is a derivation defect. The matrix answers one question the spec does not: for each fact the spec states, which test holds it, pinned at which level, and whether that test exists yet.

## Document structure

TEST_MATRIX.md is the matrix's core. The body's other parts live outside it, described below. The core opens with a short preamble, the same shape the family gives it. The preamble states what the document covers, what the bracket codes are, and how the keywords read. Two things follow the preamble, in this order:

1. **The artifact inventory** — a table of every file the reader receives, each entry owning at least one row that asserts it at the rendered level. An artifact that no test renders can ship broken while the suite stays green, so the inventory closes that gap by construction.
2. **The Parts map** — a table naming every part file the matrix's rows live in, one row per part. Its order is the order a reader should read the parts in. A part is a file under `matrix/`, holding one architecture node's whole block of rows. The map names each part's row count and its topic line, the node's own responsibility line carried over from `ARCHITECTURE.md`. Together they let a reader judge a part's size and purpose before opening it.

The matrix rows — the body, grouped into node blocks — live outside the core, one file per architecture node under `matrix/`, never inside TEST_MATRIX.md. The generated Reference, mapping each spec anchor to the matrix rows that cover it, lives outside the core too, in its own committed file, `TEST_MATRIX.index.md`.

A reader who wants the whole matrix as one document reads it through the shared reader rather than opening TEST_MATRIX.md alone. `guardrails/specformat.py`'s `spec_paths()` and `read_document()` join the core and the parts the Parts map names into one body, in map order. This is the same join the spec's own core and parts already use. A gate or a builder script takes the core, then each part, on its command line, and reads them this way. The test suite goes one step further. `tests/conftest.py`'s `read()` takes that joined body and appends the committed `TEST_MATRIX.index.md` under a synthesized `## Reference` heading. A test that calls `read("TEST_MATRIX.md")` then sees the core, every part, and the Reference, exactly as if the file had never been split.

## The matrix row is one criterion

One matrix row is one criterion. It states one trigger and one response in a single sentence, and the sentence carries both sides of the fact: what the fact does, and what it must never do. The never side is the regression fence; a row that states only the happy path proves the happy path and nothing else. The author writes the never side carrying the literal word *never* — the word the row lint reads to find the forbidden half, the convention the suite already holds today. The spec anchor the row derives from trails at the sentence's end, the family's criterion form, and it is the row's parent fact — the Reference the matrix generates reads the row's coverage from that trailing anchor.

A converted row carries five cells: the row id, the fact sentence with its trailing anchors, the pinned level, the owning test, and the status. The spec-reference column the pre-conversion grid carried folds into the trailing anchors, so the anchors are parsed from the trailing brackets of the fact sentence.

Beside the criterion the row carries three fields the spec criterion has no need of:

- **the pinned level** — the rung the row's test sits at, drawn from the project's declared level ladder. The level is the row's most important judgment, and the family's criterion form does not carry it, so the matrix row states it as its own field. The ladder's rungs are named by what proves them, so each project kind fills them with its own concrete proof artifacts, declared at founding, and the row pins one of its own project's rungs.
- **the owning test** — the test that holds this row, named so a reader walks from the fact to the test that proves it.
- **the status** — one of *built* (the test exists and runs green), *todo* (the test's future owner is named in the row), or *retired* (the row is kept, never deleted).

A matrix-local row id is legal, and the spec anchor stays the parent. One spec fact may project into several separately-testable rows, and a node's own mechanics may carry their own contract rows; an audit finding that a matrix row id is absent from the spec is expected for these, since the anchor the row cites is the parent fact, not the row id.

## Node blocks stand as the case grouping

The spec groups its criteria into named cases. The matrix groups its rows into node blocks: one block per architecture node, headed `### [node: <name>]`, and the block heading is the matrix's case grouping. Each node block is its own file under `matrix/`, named after the node. Any `[target]` marker is dropped from the filename only, never from the heading text. A node the architecture marks `[target]` — promised under an owned queue row, its machinery not yet landed — keeps that mark in its block heading, so the matrix and the architecture read the same. Every architecture node owns at least one block, and every module block owns at least one row that asserts the module at its declared interface. A new row is written into its node's own part file under `matrix/`, the file the Parts map names for that node, never into TEST_MATRIX.md.

The spec criterion sits inside a requirement that gives it a Context block and a User Story; the matrix row carries neither. The fact's Context and its User Story live once at the spec, and the row inherits them through its trailing anchor. Restating them on the row would give one fact a second home, so the row stands down from carrying them and points at the spec instead.

## The generated Reference

The Reference maps each spec anchor to the matrix rows covering it. Its committed home is `TEST_MATRIX.index.md`, a file of its own beside the core, the same home `PRODUCT_SPEC.index.md` gives the spec's own Reference. `scripts/build-matrix-reference.py` builds it from the body rows at freeze. It reads each row's trailing anchors and its row id across the core and every part the Parts map names. The file is output only; no one edits it by hand. The builder is a sibling of `scripts/build-index.py`. The table is the matrix's own generated map, the way the spec's committed index is the spec's code-to-location table. The builder reads a row's anchors the way the suite reads them today: a row may cite several codes, each mapped, and a range anchor of the form `T-1..T-7` expands to its members before mapping.

A gate holds the Reference against drift, `guardrails/check-matrix-reference.py`, a sibling of `guardrails/check-index-generated.py`. It takes the core, then each part, then the committed index path, on its command line, and it reds on three faults:

- the committed Reference differs from a fresh build off the current body — a hand edit, or a body that moved without a rebuild;
- a spec anchor sits on a body row and is absent from the committed Reference;
- a spec anchor sits in the committed Reference and is carried by no body row.

When it passes it states its reach on the green line — the files it opened and the rows it matched of the rows it scanned — the reach every gate in this family states.

## The row lint

The coverage checklist the matrix once walked by hand is promoted to a mechanical row lint. The lint reads every body row and reds a row that pins no level from the declared level ladder, or that states no never side — the row's forbidden half, found by the literal word *never* in the fact sentence. Walking the two facts per row by hand let a row slip through with a missing level or a bare happy-path fact; the lint holds them at every suite run instead, one row at a time.

The lint's home is the suite check that already holds these two facts, `test_matrix_rows_have_level_and_negative_side` in `tests/test_traceability.py`, extended rather than duplicated: it gains the naming of each offending row and the reach line on green, stating how many body rows it read, and no new standalone script is built. It supersedes the hand-walked checkbox list. The reach line prints through the suite's terminal summary, the pytest terminal-summary hook, so a quiet run still shows it at the suite's tail.

The two checklist items the lint now holds — a level pinned per row, a never side present per row — leave the hand-walked checklist, and the checkbox gate that read that checklist retires with it. The retirement fans out to six homes, all retired, repointed, or re-taught in the conversion delivery: the gate script `guardrails/check-matrix-coverage.sh`, its caller in `guardrails/pre-push`, its exercising tests in `tests/test_guardrails.py`, the matrix's own `## Coverage validation` section, the checklist-walk instruction in `skills/test-author/SKILL.md`, and the six-column header and shipped checklist in `templates/TEST_MATRIX.template.md` — so no surviving document teaches the retired form. The remaining coverage facts move to the Reference gate: that every spec anchor is covered by at least one row, and that no row cites an anchor the spec no longer carries, are the body-and-Reference agreement the Reference gate already holds.

## The conversion delivery

One delivery converts the whole matrix to this format, and everything that reads the old shape moves in that same delivery:

- **The traceability reader is rebuilt beside the rows.** The suite's matrix reader, `matrix_blocks()` in `tests/test_traceability.py`, today requires six cells per row and reads the anchors from the third cell. The conversion makes the row five cells — id, fact sentence with trailing anchors, level, owning test, status — with the anchors parsed from the trailing brackets of the fact sentence, and the reader is repointed in the same delivery, never left reading the retired shape.
- **The statuses lowercase as a declared delta.** The pre-conversion statuses are written in capitals; the conversion lowercases them to *built*, *todo*, and *retired* under the family's capitals rule, names the change as a content-preservation delta, and repoints the suite assertions in `tests/test_traceability.py` that expect the capital forms in the same delivery.
- **The gates arm here.** The Reference gate and the row lint's extended duties arm in this delivery and never before it, and the checkbox gate's six homes retire, repoint, or re-teach here, as the sections above state.

## The comprehension gate

A changed matrix section clears the comprehension gate the family defines, stated once in `docs/spec-format.md`: the mechanical lints first, then a panel of cold readers, passing only after two consecutive reads return zero blocking findings. The matrix adds two mechanical lints of its own to that first layer — the Reference gate and the row lint above — and they run beside the family's vocabulary, one-name, weak-word, and style lints.
