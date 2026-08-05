# [Project Name] — Test Matrix

Derived from the proven PRODUCT_SPEC.md **through the proven ARCHITECTURE.md**. The matrix is derived at
every row, and filling one in by hand is a defect. It is the test-matrix member of the format family
(`docs/test-matrix-format.md`). Rows are organized **architecture node × spec fact**:

- every fact gets at least one row under its owning node;
- every row pins a test level;
- each row is one criterion carrying both sides, what the fact does and what it must never do;
- each row's spec anchor trails its sentence.

The mechanical gates below close the derivation, and no hand-walked checklist stands behind them. Tests
come from the matrix. The matrix comes from the spec and the architecture, and the code is no source for
it.

**Test levels:**
- `string` — assert against raw source text / Python output (fast, no render)
- `DOM-text` — parse the rendered HTML and assert on element content
- `browser-computed` — headless browser, assert on computed style / layout / interaction
- `pixel` — screenshot comparison (use sparingly; fragile)

Any fact about visibility, layout, colour, or interaction gets level ≥ `browser-computed`.

---

## Artifact inventory

Every file the user receives. Each inventory entry owns at least one rendered-level test row.

| Artifact | Path | Type | Owning test |
|---|---|---|---|
| [e.g. Widget HTML] | `output/widget.html` | rendered | `test_widget_renders` |

---

## Matrix rows — grouped by architecture node

One `###` block per node from ARCHITECTURE.md, so "is this node covered?" is answerable by looking at one
block. Every row states both sides: what the fact does and what it must never do. Its status is one of
*built*, *todo*, or *retired*, in lowercase italic. Its spec anchor trails the fact sentence in
brackets.

### [node: renderer]

| ID | Fact (from spec) | Test level | Owning test | Status |
|---|---|---|---|---|
| M-001 | [Plain-language fact, e.g. "Stem player shows all four stems on load"; never a blank shell] [INV-1] | browser-computed | `test_stem_player_loads` | *built* |
| M-002 | [Fact; never its regression] [T-1] | string | `test_...` | *todo* |

---

## How coverage is held

The coverage checklist the matrix once walked by hand retires; two mechanical checks hold its facts at
every run.

- The **row lint** (`test_matrix_rows_have_level_and_negative_side`) reds a row that pins no level from
  the ladder or states no never side, naming the offending row.
- The **generated Reference gate** (`guardrails/check-matrix-reference.py`) maps every spec anchor a body
  row carries to its rows and reds a stale anchor no row carries, so the gate holds anchor coverage and
  stale-reference catching on its own.

The standing suite holds the derivation's other facts:

- every module block owns at least one **interface-level row** asserting the module's declared
  interface (P9);
- every row's level follows its footprint **layer** (P8):
  - a presentation fact sits at `browser-computed` or above;
  - a single-module fact sits at its module's interface;
  - a cross-cutting law is proved by a string test across the surfaces it governs;
- every declared cross-cutting law owns a test per surface it governs (INV-101);
- every artifact-inventory entry owns at least one rendered-level row;
- every test removes what it creates in a temp home the suite's leak check diffs.

A fact with no row is a derivation defect, and so is a row at a too-weak level. Fix it here, before it
becomes a production bug.

---

## Reference

The anchor-to-row table below is generated output, built from the body rows by
`scripts/build-matrix-reference.py`; no one edits it by hand. It is spliced in at freeze and maps each spec
anchor to the matrix rows that cover it, ranges and compound anchors expanded.

| Anchor | Rows |
|---|---|
| INV-1 | M-001 |
| T-1 | M-002 |

---

*Add rows as the spec grows. Retire rows (mark *retired*, never delete) when a feature is removed — so the
removal is auditable.*
