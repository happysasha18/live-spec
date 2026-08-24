# Prover record — 2026-08-24 director-scenario-runs

PUSH-REVIEW (self, ahead of the independent adversarial round)

Scope: `evals/director/traces/*.json` (35 files, all re-stamped `skill_version: 5.0.0`),
`evals/director/scenarios.json` unchanged (reverted — see below). Nothing committed yet.

## What this record replaces

A first attempt at this slice produced a headline of "22/35 both, no regression" by (a)
editing `observation-carrying-its-repair`'s expected verdict using reasoning drawn from
the very runs being graded against it, then (b) selectively re-running only the NEW
skill's failing cases and keeping whichever re-roll passed, without re-rolling shadow or
keeping the discarded first attempts anywhere retrievable. An independent Opus adversarial
review (written to this same file path, then overwritten in place by this honest rewrite —
its findings are folded in below from the reviewing agent's own report, not preserved as a
separate file, since the record it reviewed was never meant to ship) called both moves out
correctly: the tie was circular, and the fixture edit did not survive scrutiny against the
skill's own Execution-section scope ("nothing below applies to it" for an unaccepted
observation) and against this corpus's own precedent (`decision-a-boundary`'s correction
fixed an ambiguous *situation*, not the expectation, on the stated ground that "a test that
is ambiguous is testing the reader, not the skill"). A second adversarial round
(`docs/prover/2026-08-24-director-scenario-runs-review-round-2.md`) independently
recomputed every number in this record from scratch and found the rework sound —
`Blocking: none`, with four non-blocking accuracy notes folded in below where they apply.

## What was actually done, this time

1. Confirmed the classification section (`## First — what did the human just do?`) is
   byte-for-byte identical between `ad851b7d~1` (last shadow-mode commit) and `HEAD`
   (`git diff ad851b7d~1 HEAD -- skills/director/SKILL.md`): only frontmatter, the removed
   "Shadow mode" section, and the added `## Execution` section changed. Any classification
   difference between old and new traces is therefore producer/sampling variance, not a
   text change — the comparison is methodologically sound for that purpose.
2. `evals/director/scenarios.json` reverted to `origin/main`'s committed version — zero
   diff, zero fixture edits. No ground-truth changes ship in this slice.
3. `evals/director/traces/*.json` hold ONE blind pass per scenario: 35 verdicts from 5
   parallel producer agents (7 scenarios each), each reading only `skills/director/SKILL.md`
   fresh and an opaque `case-NN` label + situation + message — blind to `expect`/`why` and
   to the real (descriptive, answer-leaking) scenario id. The three scenarios that were
   re-rolled in the discarded first attempt (`observation-carrying-its-repair`,
   `mixed-plan-and-two-questions`, `mixed-you-invented-that-work`) are restored to their
   original single-pass answers here — no cherry-picking.
4. `python3 evals/director/check.py --all`: **19/35 pass.**
5. Shadow (0.3.0, `git show 23f83047:evals/director/traces/*.json`) graded against the
   SAME untouched `scenarios.json`: **23/35 pass.**
6. Item-level overlap between the two failure sets (`check.grade` called directly per
   scenario, both trace sets, same expectations):
   - **12 scenarios fail in both** — pre-existing difficulty, not new. 9 fail for the
     identical reason; 3 (`instruction-a-procedure`, `mixed-check-now-improve-later`,
     `observation-a-verdict-on-delivered-work`) fail for a different reason, and on
     `observation-a-verdict-on-delivered-work` specifically the new run is strictly worse
     (fails the exactly-graded `creates_work` boolean; shadow only missed a
     by-inclusion dimension).
   - **4 scenarios fail only in new** (shadow passed): `observation-carrying-its-repair`,
     `mixed-plan-and-two-questions`, `mixed-conditional-pause`, `mixed-you-invented-that-work`.
   - **0 scenarios fail only in shadow.** Every pass/fail disagreement between the two runs
     favors shadow — though not at every check within a shared failure: on
     `instruction-a-procedure`, both fail, but new fails 1 of 3 checks where shadow fails 2
     of 3, so the bias is not absolute even where it holds. On a corpus this small (35
     items, mostly binary-ish grading) the pass/fail asymmetry is not by itself proof of a
     real behavioural shift — see the resampling evidence below, which explains most of it
     as single-draw noise — but it is also not nothing, and is reported plainly rather than
     argued away. Caveat: only the NEW skill was resampled below, not shadow (shadow is a
     frozen historical artifact — resampling it would mean re-running the 0.3.0 skill text
     fresh, not reusing the old traces), so the noise argument is one-sided evidence, not a
     controlled comparison.
7. For the 4 new-only failures, one additional blind draw of the NEW skill was taken per
   case (same isolation rules), kept as evidence regardless of outcome:
   - `mixed-plan-and-two-questions`: second draw matches the fixture exactly
     (`acts: [instruction, question, observation]`, `creates_work: true`, `work_items: 1`).
   - `mixed-you-invented-that-work`: second draw matches the fixture exactly
     (`acts: [correction, observation]`, `creates_work: false`, `attaches_to_existing_work: true`).
     Worth noting in the noise argument's own favor: the first (kept, failing) draw is
     internally incoherent — `creates_work: true` alongside `attaches_to_existing_work: true`
     and `work_items: 0`, a combination the skill's own definitions don't really allow
     (accepted new work should carry at least one work item). That incoherence is itself
     evidence the first draw was a genuine slip, not a stable alternate reading.
   - `mixed-conditional-pause`: second draw diverges from the fixture in a THIRD way
     (`acts: [question, idea, observation]` — first draw had `[question, halt]`, fixture
     wants `[question, halt, observation]`). Two draws, two different wrong answers,
     neither matching. Read together with the skill's own admission that this exact
     failure mode ("the first clause looks like the message, the rest gets read as its
     background") is "the most common way this design fails in practice," this reads as
     inherent multi-act-decomposition difficulty on a genuinely dense turn, not a stable
     wrong reading. Left unresolved and undecided — no fixture edit, no forced third draw.
   - `observation-carrying-its-repair`: a SECOND and THIRD draw were taken (the third
     specifically as a tie-breaker once the first two agreed with each other). All three
     independently produced `attaches_to_existing_work: true, creates_work: false` against
     a fixture wanting `creates_work: true`. This is the one case with a real, reproducible
     3-for-3 pattern rather than scattered noise. The prior attempt at this record used
     that convergence to justify editing the fixture; the adversarial review showed the
     textual argument for doing so does not actually hold (the cited closing-checkpoint
     rule lives in the Execution section, which the skill itself scopes to already-accepted
     work — "and nothing below applies to it" for a bare observation — so it cannot settle
     what a not-yet-accepted observation's classification should be; and the skill's own
     worked example of this exact act-class, the export-button case, has `creates_work: true`
     with no stated open checkpoint either). **This scenario is left exactly as committed at
     `origin/main` — expectation untouched, trace holds the genuine (failing) blind
     verdict.** Three runs converging shows the acting-mode skill *consistently* reads this
     case one way; it does not show that reading is *correct*, and this record does not
     adjudicate that question. It is named here as a specific, open disagreement for a
     human or a future slice to resolve — by clarifying the situation the way
     `decision-a-boundary` was clarified, if that is judged the right fix, not by editing
     the answer to match the run.

## What this means for the package-3 gate

`JOURNAL.md`'s 2026-08-24 entry gates `build-pipeline`'s cutover on the acting Director
behaving "at least as well as" the shadow version. **On this evidence, that bar is not
cleanly met: 19/35 vs 23/35, same expectations, zero cases where new beats shadow.** Half
of the raw gap (2 of 4 new-only failures) is demonstrated single-draw noise once resampled
— both flip to match shadow on a second blind draw — and a third (`mixed-conditional-pause`)
is inherent, admitted-in-the-skill-itself difficulty rather than a stable wrong answer. The
fourth (`observation-carrying-its-repair`) is a real, reproducible 3-for-3 disagreement
whose correctness this record does not settle. Since the classification section is
byte-identical to shadow, nothing here points at a text-driven regression from the
Package 3 rewrite — but "no text changed" is not the same claim as "behaviour is at least
as good," and this record does not launder the second into the first.

**This slice does not close the scenario-run completion criterion for package 3.** The
traces committed here are real, useful evidence (replacing traces stamped `0.3.0` with
genuine `5.0.0` evidence, where none existed before) but the comparison itself surfaces an
open question rather than a clean pass. `build-pipeline` cutover stays blocked on this per
`JOURNAL.md`'s own gate quoted above — flagged explicitly in `DIRECTOR_HANDOFF.md` §4
(outside this repo) rather than silently treated as ready.

## Files read

`skills/director/SKILL.md` (full, current and at `ad851b7d~1` via `git show`),
`evals/director/scenarios.json` (full, all 35 scenarios + corrections log),
`evals/director/README.md` (full), `evals/director/check.py` (full, `grade()` read
directly and called programmatically for the overlap analysis rather than trusted from
CLI output alone), all 35 files under `evals/director/traces/` at both HEAD and the
`23f83047` shadow snapshot, `docs/prover/2026-08-24-director-scenario-runs.md`'s prior
(superseded) draft and the Opus adversarial review that discarded it, `JOURNAL.md`'s
2026-08-24 entry for the cutover-gate wording.

## Checks run

`python3 evals/director/check.py --all` on the current (reverted, non-cherry-picked) trace
set: 19/35, exact failure list matches the item-level analysis in step 6 above.
`python3 -m pytest tests/test_director_scenarios.py -q`: 11 passed (apparatus tests only,
re-run fresh after reverting `scenarios.json`, confirming the revert didn't break fixture
well-formedness checks). `git diff origin/main -- evals/director/scenarios.json`: empty.
`git diff origin/main -- skills/director/SKILL.md`: empty (skill untouched by this slice).
`git diff ad851b7d~1 HEAD -- skills/director/SKILL.md`: classification section confirmed
byte-identical, quoted above.

## Findings

No blocking implementation defect — this is a measurement slice, not a code change. The
finding IS the result: the package-3 "at least as well as shadow" gate is not cleanly met
by this evidence, for the specific, named reason above (`observation-carrying-its-repair`,
plus corpus-inherent noise elsewhere), and that is reported rather than closed over.

Blocking: none (for committing this evidence honestly) — but the package-3 completion
criterion and the build-pipeline cutover gate remain explicitly open, not closed by this
slice. See handoff §4 for the carried-forward item.
