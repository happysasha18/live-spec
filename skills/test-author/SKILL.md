---
name: test-author
description: Derive TEST_MATRIX.md from a proven spec through a proven architecture, then write the tests — the level ladder (string / DOM-text / browser-computed / pixel), real-artifact assertions, red-first proof, the pinned skip-set, and traceability as a standing test. Normally invoked by build-pipeline at its matrix and test steps (5–6). Use it directly when the user asks to "derive the test matrix", "pin test levels", "why did green tests miss this bug", or "rebuild the suite by the method". NOT for a project with no proven spec or matrix — "write tests for X" alone routes to build-pipeline first (the spec and architecture steps come before tests); and never a substitute for product-prover — this skill covers facts with tests, the prover finds holes in what documents claim.
metadata:
  version: 4.3.0
---

# test-author — from a proven spec to tests that would have caught the bug

> Part of the **live-spec pack** — the shared working rules (ask-never-guess · plain words, anchors trail ·
> one surface = one name · one home per fact · junior/senior split · checkpoints · the concurrent-edit
> fence · freshness · journal discipline · attic-never-delete · verify by deed · the human's gates · claims
> need primary sources · fix the class, sweep look-alikes · the door before code · prototype ≠ product) live ONCE in the pack's base skill, `live-spec-base` (v4.3.0), together with the
> settings ladder — this skill references them and elaborates only its own domain. Used standalone, this
> note is plain advice.

The method was born on a real project: two user-visible bugs shipped past ~660 green tests, because
the facts those tests covered were pinned at the wrong LEVEL — string checks proved the code SAYS the
right thing while the page showed the wrong one. The rebuild that followed (the track-coach test
overhaul, 2026-07-02..04) produced the level ladder, the state-space walk, and the traceability
enforcement this skill carries. Worked patterns are paraphrased from track-coach's matrix (MIT,
credited); the pack's own matrix template is the shipped shape.

## What this skill owns

Two artifacts, in order. **TEST_MATRIX.md** — the spec projected into a checkable grid: derived from
the proven spec THROUGH the proven architecture, one block per architecture node, and the spec keeps
sole authority over what is true. Then **the tests** — one
owning test per matrix row, asserting the real shipped artifact. build-pipeline keeps the order and
the gates; product-prover keeps semantic review; the guardrails keep mechanical enforcement. This
skill owns the JUDGMENT in between: which facts, at which level, asserted how.

## Deriving the matrix (the pipeline's step 5)

1. **Open with the artifact inventory** — every file the user receives, each owning at least one
   rendered-level row. An artifact nobody renders in a test can ship broken with the suite green.
2. **Blocks per architecture node; every spec fact ≥ 1 row.** A fact with no row is a derivation
   defect, found here, fixed here, always before a user could find it.
3. **Every row states BOTH sides** — what the fact does, and what it must never do. The never side is
   the regression fence: a row without it proves the happy path and nothing else.
4. **Every row pins a LEVEL** — the ladder below. The level is the row's most important judgment.
5. **Name the state space before filling cells.** Axes first: view states (mode, toggles), data
   states (present / absent / empty per source). A cell is element × view-state × data-state; a fact
   that must hold in EVERY state is an invariant and owns its own test. A flat element-by-view grid
   hides the data axis — the classic home of "empty shell shipped" bugs.
6. **Matrix-local row ids are legal, spec anchors stay the parent.** One spec fact may project into
   several separately-testable rows (sub-variant suffixes), and node-level mechanics (a decoder
   table, a gate mechanism) may carry their own contract rows. The spec anchor cited is the parent
   fact; an audit finding "matrix id absent from the spec" for these two kinds is expected.
7. **A norm-pointered clause owes a norm-conformance row.** When a spec clause carries a
   `norm: <path>` pointer (SPEC INV-43), the matrix owes a conformance row asserting the render's
   STRUCTURE against the frozen norm — every norm section and row name present in the render, no
   invented sections or value formats — at DOM-text level or above; the look itself stays the human's
   eye at the feel gate, and no pixel row claims it. The never side: a render that invents its own
   structure never ships green. Its sibling half lives in build-pipeline's code step — the norm-open rule
   with the plan-vs-prototype diff line in the delivery report — and a review cites the two halves
   together.
8. **Close by the mechanical gates, not a hand-walked list.** The coverage checklist the matrix once
   walked by hand retires; its facts are held mechanically at every run. The row lint
   (`test_matrix_rows_have_level_and_negative_side` in `tests/test_traceability.py`) reds a row that
   pins no level from the ladder or states no never side, naming the offending row. The generated
   Reference gate (`guardrails/check-matrix-reference.py`) maps every spec anchor a body row carries to
   its rows and reds a stale anchor no row carries, so anchor coverage and stale-reference catching are
   the gate's. The interface-level row per module block and the level-follows-the-layer rule (P8, P9)
   stay a standing suite check in `tests/test_interface_coverage.py`. The matrix `## Reference` is built
   by `scripts/build-matrix-reference.py` and never hand-edited — generated output, the way the spec's
   own code-to-location table is.

## The level ladder — where green suites lie

| Level | Proves | Lies about |
|---|---|---|
| string | the source or output text contains X | everything the user actually sees |
| DOM-text | the rendered document says X | position, visibility, color, interaction |
| browser-computed | real layout/style/behaviour in a real engine | subjective look and feel |
| pixel | the rendered look matches a frozen norm | nothing — but brittle; reserve it |

Pinning rules: any fact about visibility, layout, color, or interaction takes browser-computed or
higher — a string test on such a fact is the exact class that shipped the two bugs. Content facts
take DOM-text. Wiring and config facts may take string, legally. Pixel is reserved for look-and-feel
against a frozen, approved norm. When in doubt, ask what the USER would see broken — the level must
be able to see the same thing.

**The ladder is a kind-abstract shape; read the project's declared proofs, do not assume code (SPEC
INV-135).** The four levels above are the codebase's rungs. A project of another kind fills the ladder
with its own concrete proof kinds, declared at founding in the host profile's `project.proofs` line
(SPEC INV-36, INV-135) — a photo site's rendered level is a byte-diff of the baked output plus the
owner's eye-walk, a promotion campaign's is a register lint plus the owner's review, and the pack's own
rendered level is a string assertion against the shipped file (live-spec's matrix records that no fact
needs a browser-computed rung). So read the declared proof kinds before pinning levels: the rung a fact
takes is the project's own, and mapping every fact onto the code ladder for a non-code kind is the
derivation defect this reading closes.

**The level follows the footprint's layer (SPEC INV-128).** In one line: the test level follows the layer
the change touches. A presentation change is asserted at browser-computed or above, because the user sees
it. A single-module change is asserted at its module's interface: the row asserts the module's contract.
It leaves the module's internals and any neighbour's render out of scope. A cross-cutting law is asserted
by a string or traceability test that holds across every surface it governs. Tying the level to the
footprint layer makes the right level a derivation rule, so the level stops being a fresh judgment call
each time; a presentation fact tested as a string is the exact defect the ladder exists to catch (the
visibility rule above — any visibility/layout/colour fact takes
browser-computed — is the first instance of this mapping).

**A module's tests run against its interface; a cross-cutting law gets a test per surface (SPEC INV-101).**
Each module declares its interface, and each module block in the matrix owns at least one interface-level
row: each module's tests assert its declared interface, and they leave its internals and a neighbour's render alone.
A test bound to a module's internals breaks on every refactor and proves nothing about the contract; a test
bound to a neighbour's render couples two modules the boundary meant to separate. This gives the
three-question fitness test's "testable alone" [INV-122] a concrete home — one interface-level row per
architecture-node block. A cross-cutting law lives in the spec's declared-laws home [INV-101], is
enumerated once, and gets one test per surface it governs, at string or traceability level. The
traceability test enforces both: a declared law with a surface that has no test row goes red (the shape of
a spec invariant with no matrix row), and a module block with no interface-level row is a derivation defect
at the coverage walk (`tests/test_interface_coverage.py`).

**The ladder tops out below the real device (SPEC INV-77).** Touch physics, scroll snapping, and
background throttling live past a desktop headless browser's reach — iOS ignores
`scroll-snap-stop`, a backgrounded tab throttles timers, momentum has no faithful emulation. A
behaviour living there gets a **real-device walk row**: a matrix row the suite can never turn
green, owed to the human's own hands on a real phone before ship — kin of the feel gate (feel is
the human's call, never shipped off green alone). The row states WHAT the hands check and on which
device class; the suite says plainly what it cannot see.

## Writing the tests (the pipeline's step 6)

- **Assert the real shipped artifact**: render the page, produce the file, call the function — then
  inspect the output. A source-string match on such a fact only reveals a matrix defect; the row still owes a real test.
- **Red first, proven.** A new test runs against the pre-change state (or the bug) and FAILS before
  the implementation makes it pass; the red run is recorded. A test born green proves nothing. Red
  before code is the default order at every size. On a tiny reversible edit within the pipeline's skip
  boundary, the fix and its test may be authored in one batch only when the batch closes with the
  mechanical red proof: restore the pre-change file (`git show HEAD:<file>`), run the suite, watch the
  new rows fail, restore the fix. The landing record names that proof. A batch without a recorded red
  run is a defect.
- **Tests clean up after themselves; test files are born in a temp home (SPEC INV-100).** Every
  test removes what it creates — temp files, fixtures on disk, spawned processes, mutated shared
  state — and a suite run leaves the machine as it found it; a leak is a defect of the test. A
  test's files are born in the system temp home or the host's gitignored state dir and erased at
  the run's end; a user-visible folder — Downloads, Desktop, Documents — is never a test's
  workspace, and a headless browser's download directory is pointed at the temp home explicitly
  (the 42-files-in-Downloads incident, 2026-07-10). Give temp artifacts the suite's own prefix and
  keep one session-scoped before/after diff of the temp home in the suite, so a leak turns the run
  red at once, before a human eye would catch it.
- **A test's expected value derives independently of the code under test (SPEC INV-102).** A test
  compares the code's output against an expected value, and that value comes from a source other than
  the code under test. Never recompute the code's own formula and assert the result as the expected
  value; such an assertion is a mirror that can never catch the formula being wrong, since the code is
  only ever asserted equal to itself. Three sources are legal: a hand-computed constant, an independent
  derivation, or a recorded real output reviewed by a human. A round-trip or property test over the
  outputs stays legal, because it asserts an invariant. The ban strikes only an assertion whose
  expected value is produced by the same formula the code runs.
- **A geometry fact is asserted relative, wide, and long (SPEC INV-78).** A centering or
  positioning fact asserts relative geometry — the element's center within ε of the viewport's
  center — at two or more viewport sizes, and after N consecutive steps of the interaction, so
  cumulative drift shows. An absolute-pixel assertion at one viewport after one step passes forever
  while each next step lands further off-center.
- **Never edit a test to make a change pass.** A red test means the change or the matrix cell is
  wrong; the cell is corrected first, and the test follows the corrected cell.
- **Pin the skip-set.** Green means zero failures AND the skip list is exactly the expected, pinned
  set. An unexpected skip (a browser missing, a fixture absent) is a failure in a quieter color.
- **A test passes for the same reason every run — green means deterministic (SPEC INV-155).** A test
  that passes on some runs and fails on others is flaky, and one question routes it: is the source of
  the nondeterminism removable in code the project owns, the test or the product? When it is — a
  dependence on wall-clock time, on test ordering, on shared or leaked state, on an unseeded random
  draw, on a timing assumption, or a missing wait on a tool the test drives — it is a defect fixed at
  its root: name the source and remove it, never a retry, a rerun-until-green, or a raised timeout that
  hides the race. When the tool itself misbehaves at random, with nothing to correct in the test, it is
  workshop noise on the problem ledger [SPEC INV-23] instead. A flake understood but not removable in
  one landing is quarantined by name in the pinned skip-set, marked distinct from an environment skip,
  with a dated reason and an owning queue row.
- **A browser test harness launches muted and reaps what it spawned (SPEC INV-157).** A harness driving
  a real browser starts it muted (`--mute-audio`), reaps the whole process group of the browser it
  launched so no orphan accumulates, and bounds each command with a real per-command deadline. A
  blanket timeout would misread a slow machine as a failure. Clean teardown covers EVERY exit, the
  abrupt ones as much as the tidy one: teardown runs on `atexit` and on `SIGINT`/`SIGTERM`, so Ctrl-C and most kills
  still reap the group; and because the uncatchable exits (`SIGKILL`, power loss, sleep mid-run) never
  run teardown, a launch-time sweep is the backstop — each launch reaps a prior run's leaked profile
  dir and process group when the run's recorded owner is dead, so a killed run's orphans are swept on
  the next launch (and never a live concurrent run, whose owner is still alive). The harness has one canonical home —
  the pack ships it once as a template (`templates/headless_harness.py`), a consumer adopts it by
  updating the pack and layers its own methods on top, so the implementation never drifts into
  divergent copies (SPEC INV-158). A third net catches a fork the first two miss: a guardrail scans
  every tracked script and reds a file whose code both launches a real headless Chrome and carries the
  mute flag nowhere in it (`guardrails/check-muted-launch.sh`) — a whole-file check reading the
  comment-stripped code, since the launch call and the flag rarely share a line — so a hand-rolled
  harness's unmuted launch fails the run by machine, swept across the whole tree on every run (SPEC
  INV-157).
- **The suite's own plumbing must not lie (SPEC INV-80).** The skip machinery must load even on a run
  that never takes the skip: import the skip helper at module load, so a skip that cannot run goes red on every machine.
  Without that early import, a broken skip would pass silently on the one machine that needed it (a `skip()` NameError once hid exactly there).
  An engine/instance shim owes a re-export completeness test — every name the instance re-exports
  from the engine, asserted present (a missing re-export once kept a whole suite silently red). And
  a wrapper's exit code is never the verdict for a background or delegated run: the gate reads the
  suite log's own tail line ("N/N green"), because a wrapper's exit 0 reports the wrapper finishing
  and says nothing about the tests.
- **Traceability is a standing, enforced test**: a test in the suite fails on a matrix row citing a
  missing test, a duplicate id, a spec fact with no row, or a resolved-but-live decision marker — so
  drift is caught at every commit.
- **An engine extracted from an instance tests on its own generic fixtures (SPEC INV-79).** When a
  generic engine is carved out of a working project, its suite runs on engine-shaped fixtures — its
  own ids, its own content model; the donor's data may stay as an extra real-data suite, never as
  the only one. Every donor constant the extraction finds gets a works-without-it test against the
  content contract the spec names.
- **The bug protocol:** a bug fixes the matrix cell (or adds the missing invariant row) first, then a
  test proven red on the bug, then the code. Code chases the matrix.

## Work that belongs elsewhere

Use it only with a proven spec and architecture; without them the derivation has nothing sound to derive from, and
"write tests for X" alone routes to build-pipeline (the earlier steps first). Not for reviewing
documents (product-prover's job). Not for the mechanical gates themselves (the guardrails' job —
this skill DERIVES what they later enforce).

> The pack, whole: **live-spec-base** holds the shared rules and defaults · **spec-author** writes the spec ·
> **product-prover** reviews it · **design-reviewer** judges the design behind it · **build-pipeline** ships the change · **test-author** derives the matrix
> and writes the tests · **communicator** makes the human exchange land · **feedback-intake** brings what
> comes back to its home · **feedback-collector** offers a rare private note up to the authors · **text-audit** reads a text as a stranger and fixes where they stop · **publish** sees the work out the door, owing its kind's checklist.

Credits: the level ladder, the state-space walk, and the bug protocol were proven on track-coach
(github.com/happysasha18/track-coach, MIT) during its 2026-07 test overhaul; the enforcement pattern
follows its `test_traceability.py`. Paraphrased with thanks, per the pack's borrowing practice.
