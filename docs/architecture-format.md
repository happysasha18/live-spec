# The architecture format — definition

This page defines the format ARCHITECTURE.md is written in. The architecture is a member of the same
format family as the spec, and this page states only what is particular to the architecture. The
shared family laws live once in `docs/spec-format.md`, and this page inherits them by reference
rather than restating them.

## What the architecture inherits from the family

The architecture is written under the family laws `docs/spec-format.md` defines, and every law that
page states holds here unchanged:

- the closed-vocabulary glossary, so every domain noun the architecture uses carries one glossary
  entry under one name — the glossary itself lives at the spec, and the architecture adds no second
  glossary;
- the style rules, so no word stands in all capitals outside a code anchor, and the trailing code
  anchor points to the rule's home in the project spec;
- the no-history law, so the architecture states today's structure and its dates, provenance,
  session numbers, and past reasons live in the journal and the dated records;
- the generated-section gating, so a section a script builds is output only and a gate reds a hand
  edit of it;
- the comprehension gate, so a changed section clears the mechanical lints and then a panel of cold
  readers, passing only after two consecutive reads return zero blocking findings.

A reader who needs any of these consults `docs/spec-format.md`. The rest of this page adds the parts
the architecture carries that the spec does not.

## What the architecture is

The architecture is the map of the named nodes the spec's facts live in. The spec keeps sole
authority over what is true; the architecture states where each fact lives — which node owns it,
where that node's text or code sits, and where two nodes meet. Its reading job is a component
inventory: a reader opens it to learn what parts exist, what each part is for, which spec facts each
part owns, and where to find the part on disk.

## Document structure

An architecture document opens with a short preamble, the same shape the family gives it: what the
document covers, what the bracket codes are, and what a pin is. The sections follow in a fixed
order, each keeping its heading name, since presence checks in the suite read the headings:

1. **The shape at a glance** — a few lines naming the whole system and the places it runs, so a
   reader lands oriented before the first table; the placement view later details those places
   (the spec's tiers-first opening rule, SPEC INV-75).
2. **Nodes** — the body: one section per node, defined below.
3. **Seams** — the table of places two nodes meet: what crosses, which side owns the format.
4. **Feature coverage** — the table mapping each person-facing feature tag to its implementing
   node(s) and an exercising test.
5. **Runtime view** — the table of promised flows: the walk, where it can fail, what happens then.
6. **Placement view** — the table of physical places the product runs.
7. **The per-kind tables** — footprint and proof, design principles, and composition axes, each by
   project kind.
8. **Quality budgets** — the table of declared numeric budgets, each with its instrumentation home
   and its watcher.
9. **Decisions — where they live** — the pointer paragraph naming the decision homes.

## The node section

The old shape held every node as one table row, and the large rows grew into essays: at conversion
the largest cell carried twenty-six kilobytes, a quarter of the document. The new shape gives each
node its own section under the heading `### [node: <name>]` — the same heading shape the test
matrix already uses for its blocks, so the family carries one node-heading convention. A node the
architecture marks `[target]` — promised under an owned queue row, its machinery still ahead —
carries that mark in its heading, and the matrix's block heading reads the same.

A node section carries four fields, each a short labelled line or list:

- **responsibility** — one sentence naming what the node is for.
- **owns** — the list of spec anchors the node owns. An anchor may trail one parenthetical sentence,
  and that sentence says where the anchor sits or why it sits here: an ownership note (why this node
  keeps an anchor a reader would expect elsewhere) or a wiring note (which other node carries the
  fact's text while ownership stays here). The rule the anchor names lives at the spec, and the
  section cites it rather than restating it; a restated law is a second home and a defect.
- **pins** — the list of `file:line` pins with a short label each, stating where the node's
  responsibility is carried on disk. A pin comes from a grep or read actually run; a pin carries no
  date and no provenance. A `[target]` node's pin list may be the single dash, and the suite holds
  the two-way tie between the mark and the dash.
- **notes** — at most a few sentences for what the other fields cannot carry, present only when
  needed.

Every spec anchor is owned by exactly one node, and the suite holds that bond both ways, the same
bond the old table carried.

## The shared reader

One parser module reads the node sections — the node names, each node's owned-anchor set, each
node's pins — and every consumer reads through it: the traceability suite's helpers, the node-growth
counter, the pin-drift check, and every test that asks which node owns an anchor. The module is the
sibling of `guardrails/specformat.py`, the spec format's one reader. A consumer that greps the raw
node shape on its own is a defect the conversion retires: at conversion the suite carried eleven
tests matching a node's table row by its leading characters, and each moves to an assertion through
the reader. The cross-cut counter's hardcoded node-name list retires the same way — it re-derives
the list from the reader, so a renamed node can never silently desync it.

## The matrix bond

The matrix groups its rows by this document's nodes: its `### [node: <name>]` headings and the
architecture's node names are the same set, equal both ways, and the suite asserts the equality. A
node carve, merge, or rename is a structure change the architecture step owns and re-proves; the
format conversion keeps the node set unchanged, so the matrix's block headings survive the
conversion as they stand and the walk that re-checks them against the converted node set closes the
bond.

## The conversion delivery

One delivery converts the whole document to this format, and everything that reads the old shape
moves in that same delivery:

- **The consumers are rebuilt beside the sections.** The shared reader lands first, every structural
  parser and row-prefix test repoints to it, and no consumer is left reading the retired table.
- **Content preservation is proven modulo named deltas.** The conversion proves nothing lost by the
  family's word-and-punctuation multiset method, with each delta named and verified:
  - a law restated inside an owns-cell is replaced by its anchor citation after a per-anchor check
    that the spec clause carries the content; a sentence the spec turns out to lack moves into the
    spec clause in the same delivery, so the words survive at their one home;
  - the prover-record table — twenty-four dated rows of pure history — relocates verbatim to its own
    dated home under the records, and the no-history law finally reaches this document;
  - a pin's inline provenance (a landing date, a session number) is dropped where the journal
    already tells it, each drop named.
- **The spec's table-shaped wording moves with it.** The placement requirement (SPEC INV-75) today
  offers "a column in the node table" as one of two homes for a node's run-place; the conversion
  retires the table, so the clause re-words to the surviving home — the placement view — in the
  same delivery, the prover re-reading the amended clause.
- **The gates arm here.** The format's own checks arm in this delivery and never before it.

## The comprehension gate

A changed architecture section clears the comprehension gate the family defines, stated once in
`docs/spec-format.md`: the mechanical lints first, then a panel of cold readers, passing only after
two consecutive reads return zero blocking findings.
