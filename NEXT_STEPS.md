# live-spec — NEXT_STEPS (resume file: LIVE STATE + queue only; history → JOURNAL.md; ≤100 lines, INV-48)

## LIVE STATE (2026-07-27 midday — a working day of intake and two mechanisms, push pending)
Today: rows 484-492 taken in from his morning's asks, rows 471 and 166 widened instead of duplicated,
row 55 closed to the archive (all its legs read met), git tags retired as a practice. Two mechanisms
shipped and stand *in-work* with named remainders: the hook proof runner (row 489 — every session hook
must fire against its own red fixture; all seven do) and the legibility fix (row 490 — colours pair with
the surface they sit on; the bare-selector hole stays open). A new Stop hook, `hooks/code-anchor-scan.py`,
reds a queue row number left standing in prose with no plain-word naming, on his word that a bare number
tells him nothing. `docs/measure/movements.md` opened as the record a forward estimate reads from.
The review record `docs/prover/2026-07-27-push-gate.md` returned four must-fix findings; three are fixed,
the fourth (the four new mechanism files owned by no node, stated by no requirement, covered by no matrix
row) is in hand. THE PUSH WAITS ON IT.

## PRIOR STATE (2026-07-23 night — row 456 LANDED at v4.3.0; the format family is complete)
The architecture became the format family's fourth member (row 456, v4.3.0). ARCHITECTURE.md is now
per-node `### [node: <name>]` sections under `docs/architecture-format.md`, read through the one node
reader `guardrails/archformat.py`; the dated prover-record table relocated to
`docs/prover/architecture-prover-record.md`; six behavioral rules moved from owns cells into their spec
clauses; requirements 289-291 (INV-278/279/280) added; 17 consumers repointed to the reader; the doc shed
31 KB (107 to 76 KB). The two-stage content-preservation proof passed (nothing substantive lost or
invented). The fresh-context MINOR gate ran a prover + adversarial audit + design-review parity: two
blocking findings (the pin-drift check still slicing the raw shape in shell behind a Python-only test; the
Decisions section's dangling "prover record below" pointers) and two should-fix findings folded before the
landing. Suite green. Record: `docs/prover/2026-07-23-row456.md`.

With the spec (4.0.0), matrix (4.1.0), roadmap (4.2.0), and architecture (4.3.0) all converted, the
format family is complete. **tlvphotos migrates next on his word from its own window; other projects
stand until then.**

## Near queue
- Rows 484-490 (taken in 2026-07-27 from his morning's asks): 484 the seat declares what it did on its
  own (the class row folding outbound sends, work picked up in passing, defaults, retirements) · 485 a
  handed-in text is edited only where he pointed (rides row 204's preservation check) · 486 a wish taken
  in says what it resembles · 487 a sentence he could not parse is repaired at its source · 488 an engine
  carries no personal trace · 489 every hook proves it still works (the red-proof registry
  `guardrails/gate-red-proofs.json` covers pre-push gates and ZERO hooks — that gap is the build) · 490
  the legibility check pairs each colour with the surface it sits on (bug, tlvphotos deposit).
  Rows 471 and 166 widened rather than duplicated: the duration ledger feeds 471's estimate, the live
  task list is 166's cheap first leg.
- Git tags: the practice ended 2026-07-27 on his word. Four local tags deleted, their commits recorded in
  the journal; the remote deletion rides the next push, since a tag push runs the whole gate chain.
- Row 483: the four pre-existing architecture-doc reader stumbles the row-456 cold read surfaced
  (feature-coverage prose vs table on guardrails; two gates both lettered "gate x"; "Formal index"
  retired-vs-live terminology; the spec-author self-seam) — each resolved or recorded as an agreed
  non-problem. Small doc-cleanup.
- Row 481: the live-queue staleness sweep at the milestone gate (his 2026-07-23 word: the roadmap is no
  five-year plan); threshold [default: 30 days queued, 7 days in-work quiet]; owns the two deferred rows
  still trigger-less (143, 144). Rows 386/412 are NOT stale by re-derivation: the branch-and-worktree
  road is built (scripts/open-lane.sh, base rule 7, 37 green tests) and owes only its proof by deed —
  a live run of three lanes on three independent rows in one window, which his 07-27 word granted.
- Rows 471-475 (row 470's children; 475 the class answer — the enforcement-coverage registry).
- Rows 465-467 · row 437 pulled near (axis forcing step first, the recursive sweep its dear half) · row
  460 re-scoped (his 2026-07-23 word: public tier only; working tier possibly-never with two named
  triggers) · row 469 · row 479 (worker tree-restore guard).

## RECOMMENDATION carried from the row-456 prover (not blocking)
R290.1's "at most one parenthetical sentence" has no length/count gate; a few owns cells carry
multi-clause parentheticals. Candidate to fold into row 483's doc-cleanup.

## FIRST at intake — classify one-time vs standing (Alexander 2026-07-21, ROADMAP 440)
Name every request's persistence class before actioning it, and say it yourself.

## Standing word / OWNER-HELD
- Whole movement solo, push on green; plain English in docs, plain Russian in chat; gates mandatory.
- Max agentic, conserve orchestrator context (delegate reads and drafts; hold briefs and decisions).
- lean-orchestrator: the seat authors nothing long and reads nothing past a glance inline.
- Push on green is his grant; re-test every "needs his word" by derivability first; re-derive deferred
  state from the code itself (INV-247), setting any stale resume note aside.
- Row 421 (open, Alexander's call): one window ruling several instance-agents vs the one-window law.
- Budget word (2026-07-23): the two remaining formats fit; rows 460+437's expensive halves wait for the
  weekly reset. The format family is now done, so that spend closed.

## CONCURRENCY — multiple windows share ~/live-spec
Commit narrowly by explicit path, never git add -A; re-check HEAD before writing; re-arm with
guardrails/fence-refresh.sh after accounting for a move. The spec freeze re-baselines at each landing
commit (python3 scripts/spec-freeze.py --freeze PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md
--compaction). A closing commit moves its row to the archive via
`python3 scripts/rotate-doc.py --doc ROADMAP.md --close-row N` and touches this file (INV-242).

## Migration readiness
The format family is complete (all four core documents converted). tlvphotos migrates on his word from its
own window. Onboarding (movement 3) stays deferred on ~8 taste forks; framework coexistence and the
"superpower" positioning stay open questions.

## Open movements
CLOSED: row 456 architecture format v4.3.0 · row 480 queue format v4.2.0 · row 477 matrix format v4.1.0 ·
rows 461-464 audit should-fix batch v4.0.1 · row 445 spec format v4.0.0 · conduct audit v3.1.0 ·
comms/naming v3.0.0 · axes-from-kind v3.2.0.
DEFERRED: adoption + onboarding (his 2026-07-18 word; ~8 taste forks; owns the parameters registry, 427).

## Queue's open head (field-gated + far tier)
385 first real contract · 389 cross-machine read · 247 remote-deposit field leg · 396/405 conversation
channel + listener (wait on the harness listener, INV-231) · far tier 381, 411, 435. Runnable head is
field-gated (contract/listener) + far tier.

## Next free codes
Next free INV-282, E-36, T-25, M-458; next ROADMAP row 493 (A-12, B-4, C-2, D-8, S-1, ACT-4 free too).

## Research in hand
Direct-protocol research (scratchpad research-agent-transport.md, research-direct-channel.md; prior art docs/research/2026-07-17-agent-routing-prior-art.md): A2A re-invents our card.
