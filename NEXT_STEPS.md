# live-spec — NEXT_STEPS (resume file: LIVE STATE + queue only; history → JOURNAL.md; ≤100 lines, INV-48)

## LIVE STATE (2026-07-27 ~13:14 — a day of intake and two mechanisms; NOTHING PUSHED)
Rows 484-493 taken in from his asks and the promoter's deposit; rows 471 and 166 widened instead of
duplicated; git tags retired as a practice (four deleted locally, the remote deletion rides the next push).
Shipped: the hook proof runner (every session hook fires against its own red fixture; all seven do), the
code-anchor Stop hook (a queue row number standing in prose with no plain-word naming reds), the
affirmation hook brought into the repo and given the whole-turn reach plus ten tests, the legibility fix,
and the architecture cleanup. `docs/measure/movements.md` opened. Full suite 1884 green.
TO RESUME, in order: (1) fold the four must-fix findings of `docs/prover/2026-07-27-push-gate-addendum.md`
— R292.1/R292.6 claim a hook sweep the runner never performs and miss the library carve-out; R294.1 and
M-460 describe the last-message reach the affirmation hook no longer has; the turn_reader pin names three
readers where five import it; row 482 sits archived at *queued* while this delta ships its other half.
(2) `python3 -m pytest -q`. (3) A fresh record dated after the last PRODUCT_SPEC.md change, since that is
what the gate reds on. (4) `git push`, then
`git push origin --delete v1.0.0 v2.7.0 v2.8.0 spec-format-before-2026-07-22`.

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
- Rows 484-493 (2026-07-27): 484 the seat declares what it did on its own · 485 a handed-in text is edited
  only where he pointed · 486 a wish taken in says what it resembles · 487 a sentence he could not parse is
  repaired at its source · 488 an engine carries no personal trace · 489 hook proofs (in-work) · 490 the
  legibility pairing (in-work) · 491 reusable suite-speed guidance · 492 the pack's own measures on a clock
  · 493 no person's verb for a thing that cannot act (promoter deposit).
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
R290.1's "at most one parenthetical sentence" has no length gate and a few owns cells carry multi-clause parentheticals; fold into row 483's doc-cleanup.

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
