# The footprint — the three-source impact read

The full footprint read for accepted work (SPEC INV-128): the three sources, the three footprints, how
the footprint composes with the door, what a disagreement owes, and the mid-work re-classification. Every
line below reads exactly as it read in the body it was lifted from. It lived under `skills/director/`
until 2026-09-06, pointed at by an intake line the Director/build-pipeline split removed; the content is
execution routing — how far each step reaches — which belongs to the pipeline, so it came back here.

- **The same line reads the footprint — a three-source impact read that decides the route (SPEC INV-128).**
  Beside the door and the work-kind, read the change against three sources at once: the spec (what
  behaviour changes), the architecture (which module owns it), the code (what actually gets touched). Name
  one footprint — **presentation-only** (touches what the audience meets, nothing behind it) · **single-module**
  (stays inside one owned layer) · **cross-cutting** (moves a shared law or several layers) — spoken in the
  echo and written in the row's `footprint:` note beside `door:`, `kind:`, `map:`. **The footprint composes
  with the door, never overriding it:** the door decides which steps run, the footprint decides how far each
  step reaches, and the door's guarantees always hold — a feature never skips the spec step whatever its
  footprint (SPEC INV-16). A cross-cutting change opens the full pipeline from step 1, its architecture and
  matrix work spanning every layer it moves. A single-module change runs the steps its door grants with their
  scope narrowed to the one owned module (its architecture read, its matrix rows, its tests bounded to that
  module's block and interface); a single-module bug or refactor takes the existing matrix-step entry, a
  single-module feature keeps its spec step with the rest scoped down. A presentation-only change takes the
  lightest road its door already grants — the skip boundary or the docs-only door where the door routes it
  there, and the matrix-step minimum focused on the visible layer where it is a visible feature. The
  footprint sizes the reach, and the wish's size does not — a heavy process on a light change is as much a defect as the
  reverse. When the three sources DISAGREE (a spec-promised surface with no owning node, code behaviour no
  clause backs, a node pinned to a moved line), name the disagreement and route it to its owner (a bug row, a
  spec fix, a restructure row — SPEC INV-37), never silently trusting one source; the three-source read is
  the verdict derive-before-fork (SPEC INV-121) rests on. The footprint **re-classifies mid-work** the moment
  an edit reaches past its named layer (presentation → single-module, single-module → cross-cutting), the
  delivery report recording footprint held or re-classified to X at step N — the sibling of the door's
  mid-work re-fire below. (The mechanical `footprint:`-note suite check [INV-134], the per-kind
  concrete-layers-and-proofs declaration [INV-135], and the cross-cut counter [INV-128 boundary-health,
  `guardrails/crosscut_counter.py`] have landed; the declared-module-interface and interface-level test
  machinery rides its own follow-on row; this step states the read and the routing.)
