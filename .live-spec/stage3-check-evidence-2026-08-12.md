# Stage 3, step C1: evidence lines for every check with no dated catch

Date: 2026-08-12.

What this is: one evidence line per check that `.live-spec/day1-census-checks.md` marks with
"No real catch on record" — a plain-fact record of when each check was born, what the tree's own
records say about it firing, what breakage it watches for, and what else in the tree would notice
the same breakage. This page carries no verdict and no recommendation; step C2 owns those.

Selection command: read `.live-spec/day1-census-checks.md`'s "Checks with no real catch on
record" line (the table's "Real catch on record" column read for every "No real catch on record"
cell), cross-checked against the "Real catch on record" column of the full table row by row.

**Count: 25, not 24.** The census's own totals line states it plainly: "Checks with no real catch
on record: 25 — b, c, d, e, f, g, i, j, k, l, n, o, p, q, r, u, v, w, x, y, z, aa, ab, ad, ae." The
plan text this step quotes expected 24; the tree gives 25. No check was added or dropped to force
a match.

One fact surfaced while building the "Born" column that belongs in this header rather than buried
in a single row: the census itself is dated 2026-08-09 and was already going stale within hours of
its own commit. Gate ab's script retired to `attic/` the same day, a few hours after the census
landed (commits `cef83d5` 01:08 then `0ef204e` 04:15). Gate g's script was removed and restored
the same day, then repaired two days later. Both are called out in their own rows below with the
commits that moved them; the "No real catch on record" reading for each still holds on the current
tree, which is why both stay in this count.

Method per check:
- **Born** — `git log --diff-filter=A --follow --format='%h %ad %s' --date=short -- <path>` for a
  file with its own path, or `git log -S'<distinctive string>' ...` for a check living inside a
  shared file (gate c).
- **Recorded firings** — `grep -n "<check-basename>" ROADMAP.md DECISIONS.md JOURNAL.md` and
  `grep -rl "<check-basename>" docs/prover/ docs/skill-review/`, read for a dated instance of the
  check catching a genuine violation, as distinct from a routine prover pass that reads it clean or
  an audit that found a hole in the check's own logic (the census's own distinction, reused here).
- **Failure class** — read from the check script's own header comment or docstring.
- **Other coverage** — grep across `tests/` and the other `guardrails/check-*` docstrings for the
  same failure class or the same SPEC invariant number; a relationship the check's own docstring
  names is quoted directly.

---

## b — `check-tests.sh`

- **Born**: `4e210ff` 2026-07-05, "Add guardrails scaffold: pack gates as git hooks (roadmap row 3)."
- **Recorded firings**: none found naming a single dated instance distinct from ordinary
  development. One documented miss instead: JOURNAL.md:1250 records that on 2026-07-14 the local
  runner (`python3 -m unittest discover`) silently under-collected plain-function pytest-style
  tests, so a real version-pin regression passed the local gate and was caught only by CI's own
  pytest run; fixed same day by switching the local runner to `pytest` (JOURNAL.md:1256).
  ROADMAP.md row 553 (found 2026-08-06) records a cost finding — a nested meta-test inside the
  suite costs 282 of 456 seconds — not a catch.
- **Failure class it guards**: any broken behavior anywhere in the tracked codebase that a test
  exercises; this is the suite itself, run in full or scoped to the diff's reach.
- **Other coverage of the same class**: `.github/workflows/gates.yml` re-runs the same suite on
  its own machine as the CI mirror (SPEC M-5) — the mechanism that caught the 2026-07-14 miss
  above when the local runner's collection was wrong. Searched: JOURNAL.md text around the
  2026-07-14 entry, and `guardrails/check-ci-mirror.sh`'s own docstring, which names CI as the
  second net for every local gate including this one.

## c — rides gate b; no script of its own (`tests/test_traceability.py::test_architecture_owns_every_anchor_once`)

- **Born**: `c23ec44` 2026-07-05, "row 50 lands: flagship bring-up of the lost layers —
  ARCHITECTURE.md (12 nodes, 69/69 anchors owned once ...) ... traceability suite (20 green, walk
  mechanized)." Found with `git log -S'test_architecture_owns_every_anchor_once' -- tests/test_traceability.py`.
- **Recorded firings**: none found. This check carries no independent cost or existence outside
  gate b's run, so no dated record separates a "gate c catch" from an ordinary suite-green run.
- **Failure class it guards**: a spec anchor owned by zero or more than one architecture node.
- **Other coverage of the same class**: none found. `tests/test_traceability.py` carries two
  neighboring tests — `test_spec_index_unique_anchors` (anchor uniqueness in the spec's own index)
  and `test_matrix_covers_every_anchor` (matrix coverage of anchors) — but each asserts a different
  fact (index uniqueness, matrix coverage) than architecture ownership, so neither is counted as
  covering this class. Searched: every `def test_.*anchor` and `def test_.*owns` in
  `tests/test_traceability.py`.

## d — `check-matrix-reference.py`

- **Born**: `f3b98c0` 2026-07-23, "row 477: TEST_MATRIX.md converts to the format family's second
  member ... generated Reference (gate d repointed, red-proven) ..." The commit message's own words
  "gate d repointed" mean an earlier version of gate d existed against a different target before
  this conversion; that earlier history is not traced further here.
- **Recorded firings**: none found in ROADMAP.md, DECISIONS.md, or JOURNAL.md naming a dated catch.
  `docs/prover/` carries six files that mention the script, all routine prover passes reading the
  Reference table clean, not a catch.
- **Failure class it guards**: `TEST_MATRIX.md`'s generated `## Reference` section drifting from
  the matrix body it is built from — a hand edit to the table, or a body row that no longer traces
  to the table.
- **Other coverage of the same class**: `check-index-generated.py` (gate x) is the same shape of
  gate — a generated table checked against its source body — applied to `PRODUCT_SPEC.md` instead
  of `TEST_MATRIX.md`; both scripts' docstrings cite SPEC INV-269 as the shared convention. It
  would not notice a drift specific to `TEST_MATRIX.md`, only the same class of drift in the other
  document. Searched: `grep -n "INV-269"` across both scripts.

## e — `check-prototype-fence.sh`

- **Born**: `a5ad4c2` 2026-07-05, "Rows 70-71 land: the door law + the prototype law (the Room
  incident) — 0.5.1, SPEC v0.10.1."
- **Recorded firings**: none found. JOURNAL.md's one hit (2026-07-27 entry, line 136) is a
  wall-time finding — this gate cost 215 of the suite's 471 seconds — not a catch.
- **Failure class it guards**: a production file structurally referencing a file inside a fenced
  `prototype/` folder (a script src, an import path, a link target) — narrative mentions in docs,
  attic, inbox, JOURNAL.md, ROADMAP.md, NEXT_STEPS.md, or a guardrails README are excluded by name.
- **Other coverage of the same class**: none found. Searched `tests/` for other tests asserting on
  prototype-to-prod wiring; none found outside the check's own test file.

## f — `check-skill-loadability.sh`

- **Born**: `ce79f80` 2026-07-05, "Row 80 lands: skill hygiene — when-NOT-to-use in all five skills
  + loadability gate (f), red-first; evals filed as row 94."
- **Recorded firings**: none found. All hits in `docs/prover/` and `docs/skill-review/` are routine
  reviews naming the gate as part of the checked set, not a catch.
- **Failure class it guards**: a shipped skill file that fails to load — broken frontmatter, a name
  that does not match its folder, a missing description or version, or a missing "when NOT to use"
  section.
- **Other coverage of the same class**: none found. Searched `tests/` for another test asserting
  skill-file structure; none found outside this check's own test file.

## g — `check-pin-drift.sh`

- **Born**: `aeaf922` 2026-07-05, "Rows 90+91 land: symbol-first pins + drift gate (g, red-first —
  caught 3 of our own stale labels) ..." — the birth commit's own message names a catch at build
  time (three stale labels found while building the gate), which the census counts as build-time
  self-test, not a post-installation catch. Removed `1b32d8f` 2026-08-09 ("Day 2 row 2.1: the
  architecture-pin drift gate goes, and its whole tail with it"), restored the same day `d58c903`
  ("The architecture-pointer check comes back on his word, with its own repair row"), repaired
  `3915e95` 2026-08-11 ("R6: the architecture-pointer gate proves a pin against its own line, and
  eight rotten pointers come home").
- **Recorded firings**: none found as a genuine post-installation catch. Two documented holes
  instead: ROADMAP row 541 (found 2026-08-05) — the gate accepted a pin whose label word sat
  anywhere within a 51-line window, so 29 stale pins stood green; row 588 (found 2026-08-11) — 38
  of 53 pins in a different, ungated file (`.live-spec/r5-rule-prices-2026-08-11.md`) had rotted,
  because this gate reads `ARCHITECTURE.md` alone.
- **Failure class it guards**: an architecture pin (`path/to/file:123`) whose target line no longer
  carries the thing the pin names.
- **Other coverage of the same class**: none found. `tests/test_guardrails.py` and
  `tests/test_traceability.py` both reference this script, but both are the check's own unit tests
  (`tests/test_guardrails.py:982` sets `SCRIPT = ... "check-pin-drift.sh"`), not an independent
  check. Row 588 states plainly that pin pointers outside `ARCHITECTURE.md` (`.live-spec/` pages)
  "carry no guard."

## i — `check-shipped-language.sh`

- **Born**: `48204a8` 2026-07-12, "Row 275: a machine holds the English + no-personal-names line on
  shipped artifacts (INV-120)."
- **Recorded firings**: none found catching a genuine language violation. One documented hole
  instead: ROADMAP row 530 (found 2026-07-29) — the check refused a decision-record entry that
  quoted the person's own words verbatim in his own alphabet, because it read every line as the
  project's own voice with no quoted-region exception.
- **Failure class it guards**: Cyrillic text outside a deliberate user-language string, or an
  owner/personal name, in a shipped-facing file.
- **Other coverage of the same class**: `test_preshow_register_lint.py` is named beside this script
  in JOURNAL.md:1171 as the pack's register net — "register by `check-shipped-language.sh` +
  `test_preshow_register_lint.py`" — read together as one net's two parts rather than as two
  independent checks of the same class; the register lint watches machine-dialect prose, a
  different fault than a stray alphabet or personal name. Searched: JOURNAL.md around line 1171,
  and the script's own header comment.

## j — `check-broad-kill.sh`

- **Born**: `e8f13bd` 2026-07-15, "live-spec 1.10.0 — a cleanup touches only what it owns, never a
  shared resource in use (INV-162, ROADMAP 334, HIGH safety)."
- **Recorded firings**: none found as a post-installation catch. JOURNAL.md:915 names the
  motivating incident directly: the gate exists because a broad `pkill chrome` once closed the
  owner's real browser mid-session, destroying work state outside git — that incident predates the
  gate by design and is not something the gate itself caught once live.
- **Failure class it guards**: a cleanup path that ends a process by a broad name (`pkill`,
  `killall`, or `kill` fed by a `pgrep`/`pidof` lookup) instead of an owned PID, process group, or
  path this run provably holds.
- **Other coverage of the same class**: `check-cleanup-notice.sh` (gate o) covers an adjacent but
  distinct property on the same process-ending surface; its own header comment says it "ships ahead
  of INV-162's stricter owned-identity check" — o requires a notice of what ended, j requires that
  the ending be identity-scoped, not name-scoped. o would not catch a broad-name kill that emits a
  notice; it is named here as the nearest neighbor, not as full coverage of the same failure class.

## k — `check-freeze.sh`

- **Born**: `5bfbf88` 2026-07-16, "2.0: PRODUCT_SPEC redundancy to 0 (real dedup) + other docs +
  the ratchet."
- **Recorded firings**: none found. All `docs/prover/` hits are routine passes over the guarded
  docs, not a catch.
- **Failure class it guards**: a silent meaning change in a guarded doc during compaction — a
  dropped anchor occurrence, a changed structural marker, a drifted number-with-unit, or a changed
  backticked path — against the session's frozen baseline.
- **Other coverage of the same class**: none found. `check-doc-bound.py` (z) and
  `check-doc-findings-bound.py` (aa) watch the same guarded documents but for different properties
  (byte ceiling, finding count), not meaning-preserving edits; neither would notice a dropped
  citation or a drifted number. Searched: `tests/` for another test asserting anchor-occurrence or
  marker-line stability; none found.

## l — `check-muted-launch.sh`

- **Born**: `bb33134` 2026-07-16, "A machine gate reds an unmuted browser launch in any consuming
  tree (row 337)."
- **Recorded firings**: none found as a post-installation catch. `docs/prover/2026-07-16` (two
  files) audit the gate's own construction, not a caught incident.
- **Failure class it guards**: a tracked script that shows a browser-launch signal with no mute
  signal anywhere in the same file — the gate's own header names this the THIRD net for SPEC
  INV-157.
- **Other coverage of the same class**: the script's own header comment names the other two nets by
  hand: "a string-check of the shipped template (`templates/headless_harness.py`)" and "a
  consumer's by-deed process-group diff" (proves teardown, not launch flags) — both live in
  `tests/test_harness_template.py`, which is grepped as citing INV-157 throughout. The header is
  explicit that neither of the other two nets would hear a divergent fork's unmuted launch, which
  is why this third, tree-wide scanner exists.

## n — `check-earned-message.py`

- **Born**: `3774685` 2026-07-17, "v2.6.0 — agents learn to talk, and a law with no machine is a
  wish (rows 371-378 + INV-195/196/197)."
- **Recorded firings**: none found as a genuine catch on an unearned message. One documented hole
  instead: ROADMAP row 585 (found 2026-08-07) — the gate read past every fenced block before
  reading any field, so a sender copying the home's own printed template verbatim (which fences the
  birth block) failed the check on four real, legitimate deposits between 2026-07-28 and
  2026-08-07.
- **Failure class it guards**: an inbox message from one agent to another that names neither of the
  two allowed births (blocked by the receiver's zone, or carrying evidence of a fault lived there).
- **Other coverage of the same class**: none found. This check runs report-only at push (per
  `guardrails/pre-push`'s own comment) — the judging moment is the intake sweep, which is a human
  or agent reading step, not a separate mechanical check.

## o — `check-cleanup-notice.sh`

- **Born**: `38d2488` 2026-07-17, "Row 417: a cleanup says what it ended, and four name-list guards
  invert."
- **Recorded firings**: none found. All hits are the row-417 landing entry and routine prover
  passes.
- **Failure class it guards**: a tracked script that ends a process (a cleanup path) but emits no
  notice naming what it ended and why the run owned it.
- **Other coverage of the same class**: `check-broad-kill.sh` (gate j) is the stricter successor on
  the same process-ending surface (this check's own header says it "ships ahead of INV-162's
  stricter owned-identity check"); j would catch a broad-name kill regardless of whether a notice
  was printed, but would not catch a correctly-scoped ending that simply prints no notice — so the
  two checks' coverage overlaps only partially. Searched: the script's own header comment and
  `guardrails/check-broad-kill.sh`'s header.

## p — `check-touchpoint-kind.py`

- **Born**: `ce37e95` 2026-07-17, "Row 413: every point of contact with the person has a kind, and
  the kind decides what may be said there."
- **Recorded firings**: none found. JOURNAL.md:552 and :564 describe the gate passing green on
  landing and its red-proof fixture corpus, not a real catch in the wild.
- **Failure class it guards**: a surface speaking in a message kind (interruption, teaching line,
  wait line) its declared touchpoint in `guardrails/touchpoints.json` does not afford.
- **Other coverage of the same class**: none found. `check-board.py` (q) reads a specific
  touchpoint (the waiting-list board) but for a different property (nothing lost, not message
  kind); it would not notice a wrong-kind message on any other surface. Searched: `tests/` for
  other tests asserting touchpoint-kind traffic rules; none found outside this check's own test.

## q — `check-board.py`

- **Born**: `607d40a` 2026-07-17, "row 408: the waiting list — everything waiting for his eyes has
  a home that outlives the scroll."
- **Recorded firings**: none found. JOURNAL.md:1812 records an ARM added to the gate (row 409,
  INV-229), which is a widened rule, not a catch.
- **Failure class it guards**: the waiting-list board (`WAITING.md`) losing an item — a closing
  report omitting a still-open item, a demotion with no matching board line, or a shown set over
  its twelve-item cap.
- **Other coverage of the same class**: none found. Searched `tests/` for another test asserting on
  `WAITING.md`'s content beyond this check's own test file; none found.

## r — `check-authority-anchor.py`

- **Born**: `df9a276` 2026-07-17, "ROADMAP 415: a decision recorded as the person's names its
  exchange (INV-207)." Rebuilt per commit `8a0209f`, named in `check-every-gate-can-fail.py`'s own
  docstring: "the authority-anchor gate shipped hollow (commit `8a0209f` rebuilt it), reporting
  green without reaching the surfaces it claimed to inspect."
- **Recorded firings**: none found as a genuine catch. One documented miss instead: ROADMAP row 550
  (found 2026-08-06 by Alexander) — the gate asked an entry for a date alone, so a session wrote
  its own reasoning under the person's name with a real date stamped on it, and it passed; this
  happened on 2026-08-05 with a decision-record entry on the reading queue. The row is still queued
  to require a quotation of the person's own words plus a pointer to the exchange, not a date
  alone.
- **Failure class it guards**: a sentence recording a decision, word, or ruling as the person's own
  that names no exchange (at minimum a date) a reader can go check.
- **Other coverage of the same class**: none found. Searched `tests/` and `docs/prover/` for
  another check reading `DECISIONS.md` entries for the same property; none found.

## u — `check-ci-mirror.sh`

- **Born**: `b179e79` 2026-07-18, "ROADMAP 420: two gate-chain-integrity gates land — CI-mirror
  parity (u) and judges-listed (v)."
- **Recorded firings**: none found as a post-installation catch. The check's own header names the
  motivating incident directly: "gates h, k, and n were missing from CI on 2026-07-18" — found
  before this gate existed, which is what motivated building it, not a catch by the gate once live.
- **Failure class it guards**: a gate letter `pre-push` invokes locally that `gates.yml` does not
  invoke in CI (and is not declared as a carve-out in `guardrails/ci-mirror.json`).
- **Other coverage of the same class**: none found. `check-every-gate-can-fail.py` (w) reads the
  same gate-letter enumeration (its own docstring says so: "the same enumeration
  `check-ci-mirror.sh` (gate u) reads") but for a different property — a known-red proof, not CI
  parity — so it would not notice a gate missing from CI.

## v — `check-judge-listed.py`

- **Born**: `b179e79` 2026-07-18, same commit as gate u above.
- **Recorded firings**: none found. `docs/prover/2026-07-18-row420-ci-mirror-and-judge-listed-gates.md`
  is the landing record, not a catch.
- **Failure class it guards**: a chat judge whose hook file is installed correctly but whose entry
  is missing from the installed `settings.json`'s hook array, so the judge never runs though its
  file is present.
- **Other coverage of the same class**: named explicitly, and explicitly insufficient, by this
  check's own docstring — `check-config-health.sh` (gate m) "proves an installed hook FILE matches
  its source" but "does not prove settings.json still LISTS the judge entries." The docstring calls
  out the exact gap this check exists to close: "a judge whose file is present and correct still
  never runs when its settings.json entry is gone." So m is the nearest neighbor and by the check's
  own account does not cover this failure class.

## w — `check-every-gate-can-fail.py`

- **Born**: `3f7a6b8` 2026-07-18, "Add the meta-gate: every push gate carries a known-red proof
  (gate w, INV-212)."
- **Recorded firings**: none found. The docstring names the motivating incident (the authority-
  anchor gate shipping hollow, commit `8a0209f`) as the lesson this gate was built to pay for, not
  a catch by this gate itself.
- **Failure class it guards**: a gate in the push chain carrying no known-red proof, meaning it
  cannot be shown to ever fire.
- **Other coverage of the same class**: none found. Searched `tests/` and `guardrails/` for another
  check reading `guardrails/gate-red-proofs.json`; none found outside this check's own script.

## x — `check-index-generated.py`

- **Born**: `7dc5a9a` 2026-07-22, "row 445 stage 1: seven spec-format gates + index builder,
  UNARMED (INV-250..271), red-proven both ways." The script's own docstring says it is unarmed
  until named on the command line at "the conversion delivery" (INV-270); JOURNAL.md:319 says the
  seven format gates including this one "arm at the conversion delivery per INV-270" as part of the
  same landing arc — the exact arming commit is not traced further here.
- **Recorded firings**: none found. All `docs/prover/` hits are routine passes.
- **Failure class it guards**: `PRODUCT_SPEC.md`'s committed index drifting from a fresh build off
  the body — a hand edit, a body code missing from the index, or an index code missing from the
  body.
- **Other coverage of the same class**: `check-matrix-reference.py` (gate d) is the same shape of
  gate on a different document (`TEST_MATRIX.md`); both cite SPEC INV-269. It would not notice a
  drift specific to `PRODUCT_SPEC.md`.

## y — `check-agent-card.py`

- **Born**: `c93e987` 2026-07-18, "Rows 384 + 387: two gate-correctness checks — the vacuous-pass
  law and the card's gate."
- **Recorded firings**: none found. JOURNAL.md:512 is the landing record describing the gate's
  red-proof fixture, not a catch.
- **Failure class it guards**: a live-spec host tree with no `.live-spec/agent.md` card, making the
  tree undeclared to any window trying to find, address, or read a zone from it.
- **Other coverage of the same class**: `tests/test_agent_channels.py` carries
  `test_pack_card_exists_and_names_its_five_fields`, a test asserting the pack's own tree carries
  its card with its five fields — the same fact this gate checks, but scoped to the pack's own
  tree rather than any adopting host tree; JOURNAL.md:512 names this test directly as the reason
  the gate passes on the pack's own self-application. It would not notice a missing card in a
  different host tree.

## z — `check-doc-bound.py`

- **Born**: `37365b8` 2026-07-18, "Land rows 390 + 392 residual legs: the node-growth law and the
  growable-artifact bound (INV-233, INV-234)."
- **Recorded firings**: none found. JOURNAL.md:480 is the landing record.
- **Failure class it guards**: one of the four large working docs (`PRODUCT_SPEC.md`, `ROADMAP.md`,
  `TEST_MATRIX.md`, `JOURNAL.md`) growing past its declared byte ceiling with no rotation applied
  today.
- **Other coverage of the same class**: the check's own docstring says it "COMPOSES with the
  doc-rotation gate (gate t, `guardrails/check-doc-rotation.py`, SPEC INV-209)" — a rotation today
  is the remedy this gate accepts in place of a red. Gate t is the check with a dated catch
  (2026-07-27) recorded in the census, so it is not one of the 25 in this page, but it is named
  here because it directly composes with this gate on the same document set. `check-doc-findings-
  bound.py` (aa) watches the same four documents for a different property (finding count).

## aa — `check-doc-findings-bound.py`

- **Born**: `84f74bd` 2026-07-28, "A cleared document is held at zero on every push, and the resume
  file is rewritten by two readings."
- **Recorded firings**: none found as a catch. Two documented holes instead: ROADMAP row 526 (found
  2026-07-29) — the gate scored a refused reading as zero and reported a pass, when the document's
  check had never actually run; ROADMAP row 532 (found 2026-07-30 by an outside audit) — the gate
  compared only the `total` field, never the `bytes` field the same record already carried,
  missing a byte-growth ratchet it could have enforced with no new instrument.
- **Failure class it guards**: a live document carrying more findings than its recorded ceiling in
  `guardrails/rule-census.json`, or a cleared document rising above zero.
- **Other coverage of the same class**: `check-doc-bound.py` (z) watches the same four large
  documents for byte size rather than finding count — a related but distinct property on an
  overlapping document set, not the same failure class. Searched: `tests/` for another finding-
  count reader; none found.

## ab — `check-handover-provenance.py` (retired to `attic/` 2026-08-09)

- **Born**: `9477afb` 2026-07-28, "A session's record is read at both ends by an agent that did not
  live the work." Retired the same day the census landed: `0ef204e` 2026-08-09, "Day 2 row 2.2: the
  handover-provenance gate goes, with its tail, its two reviews and the day's journal entry" — a
  few hours after the census's own commit (`cef83d5`, 01:08, versus `0ef204e`, 04:15). The script
  now lives at `attic/check-handover-provenance.py`; `guardrails/pre-push` no longer invokes it
  (confirmed: no "gate ab" line in the current file).
- **Recorded firings**: none found. ROADMAP.md row 522 states the retirement's own reason in plain
  words: "a standing gate once reded a handover naming no transcript, no extract and no writer; it
  retired 2026-08-09 for no real catch on record." This is the tree's own confirmation of the
  census's "No real catch on record" reading for this check.
- **Failure class it guards** (when it ran): a session handover written from memory rather than
  from a fresh reader's extract of the transcript, naming no transcript, no extract, and no writer
  — the failure mode row 522 traces to a 2026-07-28 incident where a handover named a question as
  open though the owner had already answered it that same day.
- **Other coverage of the same class**: none. ROADMAP row 522 states this directly for the closing
  half of the discipline: with the gate retired, "this half stays a discipline the seat holds too"
  — meaning no machine check covers this failure class today. The opening half (comparing a fresh
  read of decisions against `DECISIONS.md`/`NEXT_STEPS.md`) was never a committed-artifact gate to
  begin with, per the same row.

## ad — `check-tree-counts.py`

- **Born**: `c238ca1` 2026-08-06, "Every published count about this tree is measured, declared, and
  gated (row 555)."
- **Recorded firings**: none found. All `docs/prover/` hits are routine passes or the landing
  record itself.
- **Failure class it guards**: a count this repository publishes about its own tree (a file count,
  a row count, and similar) that does not match a fresh count of the real tree, or whose named
  reproduction command does not return the published number.
- **Other coverage of the same class**: none found. Searched `tests/` for another published-count
  reader; none found outside this check's own test file.

## ae — `check-named-checks.py`

- **Born**: `9a5df02` 2026-08-06, "The registry records what each runnable file a skill body names
  is."
- **Recorded firings**: none found. All hits are routine prover passes or the landing record.
- **Failure class it guards**: `scripts/check-registry.json` carrying a stale entry for a runnable
  file a skill body names — wrong description of what it does, which tree it judges, whether it
  belongs in an adopting project, or what it needs to run.
- **Other coverage of the same class**: none found. Searched `tests/` for another reader of
  `scripts/check-registry.json`; none found outside this check's own test file.

---

## Summary of what the search found, in numbers

- 25 checks selected (census total, not the plan's expected 24 — difference reported above).
- 0 of the 25 carry a recorded firing (a dated instance of catching a genuine violation, as
  distinct from a routine pass or an audit finding a hole in the check itself). All 25 read "no
  real catch on record" and this page's own search agrees on every row.
- 9 of the 25 carry a documented miss or hole instead of a firing, each with its own dated
  ROADMAP row: b (2026-07-14 miss, fixed same day), g (rows 541, 588), i (row 530), n (row 585),
  r (row 550, still queued), aa (rows 526, 532), ab (retirement note, row 522). That is 7 checks
  by letter (b, g, i, n, r, aa, ab) across 9 dated rows.
- Other coverage of the same failure class, named with a path or a direct quote from the check's
  own docstring: b (CI mirror), d and x (mirror each other), l (two other INV-157 nets named by
  its own header), o and j (partial, named by o's own header), v (m named and ruled insufficient
  by v's own docstring), y (`tests/test_agent_channels.py::test_pack_card_exists_and_names_its_five_fields`,
  scoped to the pack's own tree), z (gate t, composed by z's own docstring). That is 8 checks with
  some named coverage, all partial or scope-limited, none named as full coverage of the same class.
- 17 of the 25 have no other coverage found: c, e, f, k, n, p, q, r, u, w, aa, ab, ad, ae, plus g
  and i, which name only the check's own unit tests or a related-but-different net, not independent
  coverage of the same class.

The three checks with the thinnest evidence — no firing, no documented hole either, and no other
coverage found by this search — are **f** (`check-skill-loadability.sh`), **q** (`check-board.py`),
and **ae** (`check-named-checks.py`). Close behind: **e**, **k**, **p**, **u**, **w**, **ad**, which
carry the same "nothing found on any of the four facts beyond the check's own construction" reading.

## Left open

This page traces gate d's "repointed" predecessor no further than the row-477 conversion commit
that renamed it; an earlier gate-d history under a different script name was not chased down. Gate
x's exact arming commit (distinct from its unarmed birth commit) was read from JOURNAL.md's landing
narrative rather than isolated by hash. Neither gap changes any check's "No real catch on record"
reading.
