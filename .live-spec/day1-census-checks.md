# Day 1 census: every check `guardrails/pre-push` runs

Scope: the 31 gate letters `guardrails/pre-push` announces, plus any check script under
`guardrails/` that the push chain does not run. Measurement only — no removal proposals, no
new checks, no plan edits (per the frozen culling plan).

**On the second half of the scope.** Every `check-*.py` / `check-*.sh` file under `guardrails/`
that carries no gate letter has its own `tests/test_*.py` file that subprocesses or imports it
for real, and that test file runs inside `pytest`, which gate b runs on every push (unless the
diff is prose-only or narrowly scoped). `pre-push`'s own comment on this pattern (the INV-239
"named-reference presence nets") says it plainly: a suite-riding check "carries no gate letter"
but "a real violation reds the suite and gate b already blocks this push." Checked systematically
against every `check-*` file in `guardrails/` (57 total, 30 gate-scripts + 27 others): every one
of the 27 others is either (a) exercised by its own test inside gate b's suite — 24 of them — or
(b) invoked directly as a nested sub-step of another gate's script — `check-config-health-perms.py`
inside gate m, `check-suite-budget.sh` inside gate b — or (c) `check-deletion-only-push.sh`, which
`pre-push` runs unconditionally on every push, ahead of the gate chain, by design carrying no
letter. **Finding: no check script under `guardrails/` goes fully unrun by the push chain.** The
second bucket the task asked for is empty; the table below therefore holds exactly the 31 gate
letters, which is the complete census.

(The 9 non-`check-*` files under `guardrails/` — `archformat.py`, `specformat.py`,
`nonempty_input.py`, `crosscut_counter.py`, `net_meter.py`, `node_growth_counter.py`,
`reap_owned_group.py`, `route_agent_transport.py`, `cleanup_notice.py` — are shared library code
imported by the check scripts and their tests, not independent checks, so they carry no row.)

**Timing method.** Each script was run once, on this machine, on the current tree (HEAD
`63cc21c`), invoked exactly the way `pre-push` invokes it — same flags, same arguments, same
working directory — with no push performed. `check-prover-record.sh --push` and
`check-push-review.sh` exited non-zero (no fresh prover/review record is dated today in this
session); their timings are still the real wall-clock cost of running them — a red exit is not
a timing defect. Gate b was run as the full, unscoped suite (`tests/`, no `SCOPED_TEST_FILES`),
which is the shape `check-tests.sh` itself takes as canonical and the one that also runs the
nested suite-budget check.

**Real-catch method.** For each gate, git history (`git log --all --grep`), `JOURNAL.md`,
`docs/PROGRESS.md`, `guardrails/gate-red-proofs.json`, and the `docs/prover/`, `docs/audit/`,
`docs/gate-audit/`, `docs/push-review/` folders were searched for the gate firing on genuine
broken work, as distinct from a test fixture built to prove the gate CAN fail.
`gate-red-proofs.json`'s `proofs` map is exactly that fixture ledger — every one of the 31 gates
has an entry there by construction of gate w (a gate with none reds the meta-gate), so its mere
presence proves nothing about a real catch and is never cited below as one.

A pattern recurred in the search: most of these gates were built reactively, the day after a
human, a prover pass, or an adversarial audit found a real incident by hand — and the gate's
first fixture then enshrines exactly that incident. That motivating incident predates the gate
and is not something the gate itself caught after going live; it is noted as context below,
never counted as a real catch.

## Table (31 gates, ordered by seconds descending)

| Gate | Script (as `pre-push` invokes it) | What it checks | Real catch on record | Seconds |
|---|---|---|---|---|
| b | `check-tests.sh` (full pytest suite; runs `check-push-reach.sh` to scope, and nests `check-suite-budget.sh`) | The full test suite is green; also covers gate c (anchor ownership) | No single dated instance distinct from ordinary development; see note below | 451.45 |
| aa | `check-doc-findings-bound.py` | No live document carries more findings than its recorded, only-downward count | No real catch on record | 9.82 |
| e | `check-prototype-fence.sh` | Blocks a prototype/experimental reference from reaching shipped, production code | No real catch on record | 9.15 |
| g | `check-pin-drift.sh` | Architecture pin lines haven't drifted from the code or anchors they cite | No real catch on record | 6.49 |
| l | `check-muted-launch.sh` | Every script launching a headless browser carries the mute flag | No real catch on record | 2.40 |
| h | 4 scripts: `scaffold/guardrails/check_{completeness,tests_present,traces_to_spec,conflicts}.py --base origin/main` | The host-adapter's own four checks: doc completeness, tests present, spec traceability, no conflicts | Yes — 2026-07-23 | 2.34 |
| t | `check-doc-rotation.py` | Every rotated doc row is findable in its archive and named in a manifest | Yes — 2026-07-27 | 0.86 |
| o | `check-cleanup-notice.sh` | A process-ending cleanup path reports what it ended and why | No real catch on record | 0.64 |
| j | `check-broad-kill.sh` | Blocks cleanup code that kills a browser by broad name instead of an owned PID/path | No real catch on record | 0.58 |
| i | `check-shipped-language.sh` | No personal names or stray Cyrillic text in the shipped-facing document set | No real catch on record | 0.44 |
| m | `check-config-health.sh` | Installed hooks/skills match `guardrails/` source; no dead permission path | Yes — 2026-07-20 | 0.36 |
| ac | `check-push-review.sh` | The delta being pushed carries a fresh adversarial review record | Yes — 2026-08-05 | 0.27 |
| f | `check-skill-loadability.sh` | Every skill file loads and parses within its structural limits | No real catch on record | 0.25 |
| ae | `check-named-checks.py` | The check registry says what each runnable file a skill body names actually is | No real catch on record | 0.16 |
| r | `check-authority-anchor.py` | A decision recorded as the person's names the exchange where he made it | No real catch on record | 0.15 |
| k | `check-freeze.sh` | Guarded docs' anchor map, markers and numbers stay unchanged (compaction freeze) | No real catch on record | 0.15 |
| u | `check-ci-mirror.sh` | Every local pre-push gate letter is mirrored in CI or carved out by name | No real catch on record | 0.13 |
| ad | `check-tree-counts.py` | Every published tree count matches the real tree; its repro command returns the number | No real catch on record | 0.12 |
| d | `check-matrix-reference.py` | `TEST_MATRIX.md`'s generated Reference table agrees with the body | No real catch on record | 0.08 |
| x | `check-index-generated.py` | `PRODUCT_SPEC.md`'s committed index equals a fresh build off the body | No real catch on record | 0.08 |
| a | `check-prover-record.sh --push` | A fresh prover review record is dated today before the push | Yes — 2026-07-20 | 0.07 |
| z | `check-doc-bound.py` | Each growable working doc stays within its declared byte bound, or was freshly rotated | No real catch on record | 0.07 |
| s | `check-skill-review.sh` | A substantive skill change carries a fresh skill-creator review record | Yes — 2026-07-20 | 0.06 |
| w | `check-every-gate-can-fail.py` | Every gate in this chain carries a known-red proof (the meta-gate) | No real catch on record | 0.06 |
| ab | `check-handover-provenance.py` | A session handover names its transcript, its extract and the agent that wrote it | No real catch on record | 0.06 |
| p | `check-touchpoint-kind.py` | A surface speaks only the message kind its declared touchpoint affords | No real catch on record | 0.05 |
| q | `check-board.py` | The waiting-list board loses nothing: no omitted item, no silent demotion, no over-cap set | No real catch on record | 0.05 |
| v | `check-judge-listed.py` | Every wired chat judge is listed in the installed `settings.json` | No real catch on record | 0.05 |
| n | `check-earned-message.py` (report-only at push) | An inbox deposit names the blocked work that earned it | No real catch on record | 0.05 |
| y | `check-agent-card.py` | A live-spec host tree carries its `.live-spec/agent.md` card | No real catch on record | 0.04 |
| c | *(no script — rides gate b; `tests/test_traceability.py::test_architecture_owns_every_anchor_once`)* | Every spec anchor is owned by exactly one architecture node | No real catch on record | 0 (counted inside gate b) |

## Totals

- **Checks covered: 31** (30 with an independently timed script, plus gate c which runs no script of its own and rides gate b).
- **Total seconds: 486.48** (sum of the 30 timed scripts; gate c adds 0 on top since its cost is already inside gate b's 451.45).
- **Checks with a real catch on record: 6** — a, h, m, s, t, ac.
- **Checks with no real catch on record: 25** — b, c, d, e, f, g, i, j, k, l, n, o, p, q, r, u, v, w, x, y, z, aa, ab, ad, ae.

## The six real catches, with their evidence

- **Gate a** (`check-prover-record.sh`) — 2026-07-20. The v3.2.0 axes-from-kind push "blocked
  twice on provenance gates I had skipped — a prover record dated to cover the spec change, and
  a fresh skill-review for spec-author" (`JOURNAL.md`, the 2026-07-20 v3.2.0 entry). Both a
  missing prover record and a missing skill-review were caught on the same real push.
- **Gate h** (the four scaffold host checks, specifically `check_tests_present.py`) — 2026-07-23,
  row 476. "The v4.0.1 push was blocked by tests-present: the eleven SKILL.md files carried only
  the version stamp, and the check reads file paths with no content read — the gate-reach class
  on the pack's own gate." (`JOURNAL.md`, "row 476: the push gate met its first stamp-only push
  and red it"). The check was hardened same-day to compare normalized content, not just paths.
- **Gate m** (`check-config-health.sh`) — 2026-07-20. "INV-243 earned its keep on the first run:
  it caught that all ten installed skills on the machine had drifted to 2.8.1 while the pack
  source was at 3.0.0, and they were re-synced." (`JOURNAL.md`, the v3.1.0 conduct-audit entry).
- **Gate s** (`check-skill-review.sh`) — 2026-07-20. Same push and same journal line as gate a
  above: the push blocked a second time for a skill change (`spec-author/SKILL.md`) carrying no
  fresh skill-creator review record.
- **Gate t** (`check-doc-rotation.py`) — 2026-07-27. "Run against the real tree it found seven
  more — three rows in the current archive whose status cells never followed their own delivery
  reports, and four decision rows from the pre-conversion archives." (`JOURNAL.md`, the 2026-07-27
  entry building the terminal-status net for archived rows).
- **Gate ac** (`check-push-review.sh`) — 2026-08-05. "The 24 unpushed commits went to four
  adversarial reviewers at once... They found eleven, and every one of them repaired the same
  hour." (`JOURNAL.md`, "the push review, run adversarially and in parallel"), including four
  repairs to the worker-restore check and a genuine tracked-file deletion with no attic copy.

## Checks with no real catch on record — what they cost instead

**Gate b** sits apart from the other 25: it is the whole pytest suite (2502 tests, 451.45s), the
project's primary correctness net, and it almost certainly catches broken code on nearly every
day of development — but that happens during ordinary iteration before a commit, and routine
test failures are not journaled as discrete "gate b caught X" events the way the narrow gates'
single incidents are. The one dated, named defect specific to gate b's own mechanism is a miss,
not a catch: on 2026-07-14, CI's pytest run caught a version-pin regression the *local* gate had
missed, because `check-tests.sh` then ran `python3 -m unittest discover`, which silently
under-collects the plain-function pytest-style tests. Fixed same day by switching the local
runner to `pytest`, matching CI. Cost either way: 451.45 seconds on every push that is not
prose-only or narrowly scoped.

For the remaining 24 gates, the search found either nothing, or a related-but-distinct fact worth
separating from a real catch:

- **c** — rides gate b entirely; no independent cost or catch of its own.
- **d, k, n, p, q, v, w, x, y, z, ad, ae** — no real-work incident, no gate-quality finding
  either; each costs only its own seconds above (0.04s–0.16s, except k at 0.15s) on every push.
- **e** (9.15s) — the second most expensive check with zero real-catch evidence found.
- **f** (0.25s) — no incident found.
- **g** (6.49s, the third most expensive) — a prover pass, not the gate itself, found that
  `check-pin-drift.sh` sliced its target text in shell while the enforcing test read only Python,
  leaving a hole "exactly the shape of the surviving violation" (`JOURNAL.md`, 2026-07-23). That
  is a defect found *in* the check by review, not the check catching a real violation.
- **i, o** — no incident found beyond the check's own construction.
- **j** (0.58s) — built after a real recurring browser-kill incident, but that incident predates
  the check by design (the check exists because of it); no post-installation catch is on record.
- **l** (2.40s) — an audit on 2026-07-16 found the check's own detection logic could be evaded by
  a comment-only `--mute-audio` mention or a docstring-only reference; that is a hole found in the
  gate, fixed the same day, not a real unmuted-launch the gate caught in the wild.
- **r** (0.15s) — the gate was rebuilt on 2026-07-17 after a habits-to-gates audit found the prior
  version hollow (it fabricated its read-back rather than reading a real exchange); the audit
  caught the gate's own emptiness, not a real authority violation.
- **u** (0.13s) — before this gate existed, a manual CI-mirror comparison was already found
  "proven-drifted" (`docs/gate-audit/2026-07-18-habits-to-gates.md`), which is what motivated
  building it; no catch by the gate itself, once live, is on record.
- **ab** (0.06s) — built after a 2026-07-28 incident of a handover written from memory that named
  a question as still open when the owner had already answered it that same day; the incident
  predates the check.
- **aa** (9.82s, the single most expensive check in the table) — no incident found.
