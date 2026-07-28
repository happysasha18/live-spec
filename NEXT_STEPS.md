# live-spec — NEXT_STEPS (resume file: LIVE STATE + queue only; history → JOURNAL.md; ≤100 lines, INV-48)

## LIVE STATE (2026-07-28 night — the rules about the project's own writing moved into one home; PUSHED 73741a9..d7f2dbb, all gates green, suite 2209)
Alexander's word opened the movement: the rules about how this project writes are relatives of each
other, they are worked in one pass, and the kinship belongs in the spec. An inventory found 61 such
rules spread over 57 files, nine of them stated twice with different verdicts and 24 held by no checker.
They now live in `guardrails/language-rules.json`, 53 rules after five folds retired seven duplicate ids.
`scripts/gen-language-consumers.py` writes three artifacts from that home: the rule text the judging
model reads, a writer's page, and a maintainer's page. `guardrails/check-language-rules.py` reds when any
of the three drifts from the source, when a rule names no catcher and no reason, or when a pin names a
file or line that is gone.

Three places in the spec carry the movement. Requirement 300 states the one-home law. Requirement 301
states that a worker restores a file by writing back bytes it read before mutating it. Requirement 208
gained a case: a dispatch to the expensive tier opens with an instruction that assumes a cheaper tier.

93 acceptance criteria were rewritten worst-first. Sentence length fell from 469 criteria past the cap to
378, in-place definitions from 120 to 65, closes with no finite verb from 147 to 123. Seven rewrites lost
meaning; the suite caught three and the prover found four. The readability gate now reads a criterion's
bullets and carries a fifth measure over a criterion's total weight, recorded at 31.

## TO RESUME, in order
(1) `docs/language-defects.md` owes two consecutive blind reads with no blocking finding before anyone
is shown it. The four readings so far, oldest first: 45 stops with 11 blocking, 34 with 8, 27 with 12,
28 with 6. Round eleven repaired all six, so read nine is owed and read ten after it.
(2) The reference reads at 33 of the 39 rules that bind a documentation page, applicable with no
question to the author. The reader named one question per rule for the six that remain, and three of
those six wait on the three answers below. A third reading measures what the worked example moved.
(3) The three questions the reference's reader left standing and this seat could not derive: what "the
register laws" names for a drafting brief, how a rule with no measure states its bar (r62's own note says
its measure does not exist), and the number behind "a long flat run of peer items" in r45.
(4) 30 criteria carry more than one rule and want splitting into criteria of their own; splitting
renumbers neighbours, so it runs as its own delivery with a record. The list is in the 2026-07-28 trim
worker's account.

## Near queue
- Rows 510-515 (2026-07-28): 510 a part of a set is named by what its members are · 511 a cross-project
  finding travels on its own and nothing notices when it stays home · 512 the rotation road reaches one
  document · 513 a checker whose reach is a whole file holds one surface's rule over another's · 514 a
  rule pinned to a line number that an edit moves · 515 the gate over skill reviews reads the wrong record.
- Rows 484-493 (2026-07-27): 484 the seat declares what it did on its own · 485 a handed-in text is
  edited only where he pointed · 486 a wish taken in says what it resembles · 487 a sentence he could not
  parse is repaired at its source · 488 an engine carries no personal trace · 489 hook proofs · 490 the
  legibility pairing · 491 reusable suite-speed guidance · 492 the pack's own measures on a clock · 493
  no person's verb for a thing that cannot act.
- Row 483: the four architecture-doc reader stumbles the row-456 cold read surfaced. Small doc cleanup.
- Row 481: the live-queue staleness sweep at the milestone gate; owns the two trigger-less deferred rows.
- Rows 471-475 (row 470's children; 475 the enforcement-coverage registry, now served by the rule home's
  own coverage page and its gate).
- Rows 465-467 · row 437 · row 460 · row 469 · row 479 (landed tonight, awaiting its closing sweep).

## FIRST at intake — classify one-time vs standing (Alexander 2026-07-21, ROADMAP 440)
Name every request's persistence class before actioning it, and say it yourself.

## Standing word / OWNER-HELD
- Onboarding runs closer to the weekend (his word 2026-07-27). Of its 26 parked questions, 23 are the
  seat's, 1 is his, 2 wait on a first outside host.
- Whole movement solo, push on green; plain English in docs, plain Russian in chat; gates mandatory.
- The lane cap is lifted and helper runs are unlimited (his word 2026-07-27 night); push and deploy to
  production on green without asking.
- Max agentic, conserve orchestrator context (delegate reads and drafts; hold briefs and decisions).
- Push on green is his grant; re-test every "needs his word" by derivability first.
- Row 421 (open, his call): one window ruling several instance-agents against the one-window law.

## CONCURRENCY — multiple windows share ~/live-spec
Commit narrowly by explicit path, never git add -A; re-check HEAD before writing; re-arm with
guardrails/fence-refresh.sh after accounting for a move. No session and no worker runs a command that
discards working-tree changes (Requirement 301). The spec freeze re-baselines at each landing commit
(python3 scripts/spec-freeze.py --freeze PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md --compaction).

## Migration readiness
The format family is complete. The answer on carrying it to tlvphotos, written 2026-07-28: convert the
FORMAT now, since conversion is what attaches the measuring machinery and a seeded baseline records the
debt instead of demanding it be repaid first; hold the language rewrite until the reference clears its
own blind read. track-coach has no working tree on this machine, only an intake folder.

## Open movements
CLOSED: row 456 architecture format v4.3.0 · row 480 queue format v4.2.0 · row 477 matrix format v4.1.0 ·
rows 461-464 audit batch v4.0.1 · row 445 spec format v4.0.0 · conduct audit v3.1.0 · comms/naming v3.0.0.
DEFERRED: adoption + onboarding (his 2026-07-18 word; owns the parameters registry, row 427).

## Queue's open head (field-gated + far tier)
385 first real contract · 389 cross-machine read · 247 remote-deposit field leg · 396/405 conversation
channel + listener · far tier 381, 411, 435.

## Next free codes
Next free INV-301 (292-300 taken 2026-07-28), E-36, T-25, M-479 (468-478 taken 2026-07-28), requirement
302; next ROADMAP row 516 (A-12, B-4, C-2, D-8, S-1, ACT-4 free too).

## Research in hand
Direct-protocol research: docs/research/2026-07-17-agent-routing-prior-art.md. The routing experiment's
record with its two baseline points: docs/measure/2026-07-28-tier-routing-experiment.md, week ending
2026-08-04.
