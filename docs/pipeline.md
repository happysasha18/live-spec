# The pipeline walk

This page walks one change through the full pipeline, station by station. The order is fixed: spec →
prove → architecture → prove architecture → matrix → test → code → verify → commit & show. The
normative home for every step is the build-pipeline skill (`skills/build-pipeline/SKILL.md`); the
shared rules every station obeys live once in `skills/live-spec-base/SKILL.md`. This page explains the
walk in plain words and points there for the letter of each law.

## Station 1 — a wish arrives

- **Enters:** a request from the human, spoken in chat or dropped as one file in the project's
  `inbox/` folder (the parallel-safe door for anything born outside the assigned session).
- **Produces:** one intake line before any tool call: size, priority, the door (feature · bug ·
  refactor · docs-only · skip), the work-kind (product · infra · skill · prose), and the wish's place
  on the feature map. The line is echoed back to the human and the wish becomes a queue row. A wish
  carrying several user stories splits here, one row per story (SPEC T-17).
- **Owner:** build-pipeline (step zero); feedback-intake sweeps the inbox itself.
- **Blocks:** work stays parked until the door is named. Hard tripwires decide the door by rule — a
  new visible surface, new persistent state, a new interaction, or behaviour with no spec clause
  behind it means the feature door, however casually the wish was phrased (SPEC T-12, INV-16).

## Station 2 — spec delta

- **Enters:** the classified wish and the current `PRODUCT_SPEC.md`.
- **Produces:** a spec delta in plain product language: the scenario the person walks, entities,
  states, transitions, invariants, and how the touched surface composes with its neighbours. A
  feature delta opens with regression fences (neighbouring promises that must stay true) and closes
  with two sentences: non-goals and one success measure. Real gaps become a marked open question
  (`⟨DECIDE⟩`) with a recommended pick.
- **Owner:** spec-author writes the spec; it is the authoring half of a pair.
- **Blocks:** code before spec is banned; a spec written after the code documents whatever got built,
  and the reviewer at the next station can no longer catch the difference.

## Station 3 — prover review of the spec

- **Enters:** the fresh spec delta.
- **Produces:** a structured review with formal-verification thinking (states, transitions,
  invariants, composition), written to `docs/prover/YYYY-MM-DD.md` with a folded / rejected column
  per finding, so the folding is verifiable after a memory wipe.
- **Owner:** product-prover, the reviewing half of the pair. It reads documents; the test suite
  proves what the artifact does.
- **Blocks:** every defect finding is folded into the spec before the walk continues. Open
  questions the change touches are resolved or asked; the rest are listed, and they carry no gate.

## Station 4 — architecture delta

- **Enters:** the proven spec.
- **Produces:** an updated `ARCHITECTURE.md`: named nodes with one responsibility each, every spec
  fact owned by exactly one node, named seams between nodes, quality budgets with the place their
  real numbers can be read, a runtime view that walks every promised flow, and a placement view that
  says where each node runs. In a live codebase every node pins to a `file:line` that came from a
  command actually run.
- **Owner:** build-pipeline (step 3). A small change cites its existing node and moves on.
- **Blocks:** a spec fact with no owning node, or a node with no spec backing, is a defect found at
  the next station.

## Station 5 — prover pass on the architecture

- **Enters:** the changed architecture doc.
- **Produces:** findings in the same `docs/prover/` record, from six checks: every fact owned · no
  unbacked node · every seam names what crosses it · budgets stated with their measurement homes ·
  the runtime view walks every flow · the placement view covers every node.
- **Owner:** product-prover, with the architecture lens.
- **Blocks:** the same folding discipline as station 3. The pass runs whenever the doc changed;
  a change that touched no structure stands this station down by name in the landing report.

## Station 6 — test matrix rows

- **Enters:** the proven spec and the proven architecture.
- **Produces:** rows in `TEST_MATRIX.md`, derived, never hand-filled: one block per architecture
  node, every spec fact with at least one row, every row stating both what the fact does and what it
  must never do (the never side is the regression fence), and every row pinned to a test level —
  string, DOM-text, browser-computed, or pixel. The matrix opens with an inventory of every file the
  user receives, and derivation closes by walking the coverage checklist.
- **Owner:** test-author (pipeline step 5).
- **Blocks:** a fact with no row, or a row at too weak a level, is a derivation defect fixed here.
  Any fact about visibility, layout, colour, or interaction needs level browser-computed or above.

## Station 7 — red-first tests

- **Enters:** the derived matrix rows.
- **Produces:** one owning test per row, asserting the real shipped artifact — the rendered page, the
  produced file, the actual function output. Each new test is watched failing first; the red run is
  the proof it can catch the missing behaviour.
- **Owner:** test-author (pipeline step 6).
- **Blocks:** a test that never went red proves nothing yet. Editing a test to make a change pass is
  banned.

## Station 8 — code

- **Enters:** the red tests and the spec sentences they serve.
- **Produces:** the implementation, driven until the suite is green. Mechanical, well-scoped work
  goes to a cheaper junior worker with a self-contained brief and a persistent checkpoint file;
  judgment stays with the seat, who verifies the worker's result by deed.
- **Owner:** build-pipeline (step 7), as a senior developer.
- **Blocks:** green tests are the exit condition; the next station adds eyes.

## Station 9 — verify by deed

- **Enters:** the green implementation.
- **Produces:** a verify-by-deed record: the builder runs the real thing and looks at the result with
  fresh eyes. Every check the diff can reach runs before any push (SPEC INV-45). For gated prose,
  `scripts/spec-done-gate.py` runs the prose gate; its conditions are described in
  [docs/push-law.md](push-law.md).
- **Owner:** build-pipeline (step 8), backed by the mechanical guardrails on the pre-push hook.
- **Blocks:** green means zero failures and the skip list exactly matches the pinned expected set; an
  unexpected skip is a failure outright. Red at a pause is never committed — the failing test name
  plus a hypothesis becomes the top `NEXT_STEPS.md` item.

## Station 10 — commit

- **Enters:** a green tree with no regression.
- **Produces:** the commit, a patch-level version bump by default, and the docs travelling in the
  same change: the readme, the changelog in the user's terms, the journal entry with the dated why.
- **Owner:** build-pipeline (step 9), as a careful release manager.
- **Blocks:** the concurrent-edit fence runs before the commit — `git status` and HEAD re-checked
  against what was last read. Gates the human personally named wait for the human's word.

## Station 11 — show the result

- **Enters:** the committed change.
- **Produces:** the real render opened for the human in a new window, with real data, plus a landing
  report: what landed, where it sits on the map, which taste defaults were picked (told plainly, with
  no confirmation requested), and every stood-down step named.
- **Owner:** communicator shapes the human-facing exchange; feedback-intake catches what comes back.
- **Blocks:** a push or deposit waits until the human has had the work in front of them, and a bare
  file path never counts as showing.

## When the pipeline may be shortcut

A tiny edit skips the pipeline only when all three hold: it touches a single file, it adds no new
state, element, or user-visible behaviour, and an existing test level already covers the touched fact.
Even then the edit still ships a test. A bug takes a shorter road — bug → matrix → test → code — with
a red-on-bug test first and a cite of the existing architecture node it lands in. Anything touching
visibility, layout, or colour enters at the matrix station at minimum.

The rules decide, ahead of anyone's mood: the tripwires at station 1 outrank a casual "it's just a
one-liner", and urgency moves a wish's priority while its door stays put. When the shortcut boundary
is genuinely unclear, the session asks the human one plain question and does not guess
(build-pipeline's skip boundary; SPEC T-12).
