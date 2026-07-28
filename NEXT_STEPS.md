# live-spec — NEXT_STEPS (resume file: LIVE STATE + queue only; history → JOURNAL.md; ≤100 lines, INV-48)

## LIVE STATE (2026-07-28 morning)
The rules about this project's own writing live in `guardrails/language-rules.json`, 53 of them, with
`scripts/gen-language-consumers.py` building the judging model's rule text, the writer's page, and the
maintainer's page from that one home, and `guardrails/check-language-rules.py` refusing any drift.
Requirements 300, 301, and a case on 208 carry the movement in the spec. 93 acceptance criteria were
rewritten by those rules: 469 criteria past the word cap fell to 378, in-place definitions 120 → 65,
closes with no finite verb 147 → 123, and seven rewrites lost meaning (three caught by the suite, four
by an independent read).

## THE LIVE MOVEMENT — the top-level documents read for a stranger
Alexander's word, 2026-07-28 morning: this is the main task, and everything else waits. The plan is
`docs/plans/2026-07-28-top-level-readability.md`, written to be executed by a session with a clean
context — it carries the goal, the seven rules with their measures, the order, the commands, the five
self-checks per batch, and the stopping rule. Start there and read nothing else first.

The state it starts from: the rule home holds 53 rules; one document was rewritten by them, being 93
acceptance criteria of `PRODUCT_SPEC.md`; the census of all 106 live documents stands at
`docs/audit/2026-07-28-rule-census.md` with 5429 findings, and its data at `guardrails/rule-census.json`.
The plan's step 1 is building `guardrails/check-noun-grounding.py`, which gives a machine to the one
rule that readers actually stop on.

## PARKED behind the movement (2026-07-28 morning, Alexander's word: everything else waits)
- `docs/language-defects.md` stops taking cold readings. It is an internal record shown to nobody, and
  nine readings on it produced no convergence. The shipping bar stands for texts a person is shown.
- The rules reference reads at 33 of the 39 rules binding a documentation page; a third reading waits.
- 30 criteria carry more than one rule and want splitting; splitting renumbers neighbours, so it is its
  own delivery with a record.
- The three questions answered 2026-07-28 morning without the owner: a clean-context worker drafts, this
  seat briefs and revises; a rule with no measure states its bar as its reader test; a flat run of peer
  items is long at seven, to be recorded as r45's threshold when that rule gets its check.

## Near queue
- Rows 510-516 (2026-07-28): 510 a part of a set is named by what its members are · 511 a cross-project
  finding travels on its own and nothing notices when it stays home · 512 the rotation road reaches one
  document · 513 a checker whose reach is a whole file holds one surface's rule over another's · 514 a
  rule pinned to a line number that an edit moves · 515 the gate over skill reviews reads the wrong record · 516 the two-clean-readings bar is not approached in nine readings.
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
302; next ROADMAP row 517 (A-12, B-4, C-2, D-8, S-1, ACT-4 free too).

## Research in hand
Direct-protocol research: docs/research/2026-07-17-agent-routing-prior-art.md. The routing experiment's
record with its two baseline points: docs/measure/2026-07-28-tier-routing-experiment.md, week ending
2026-08-04.
