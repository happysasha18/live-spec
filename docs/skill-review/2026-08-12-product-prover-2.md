# Skill review — product-prover (the three findings that each asked a scope question)

SKILL-REVIEW

Skill: product-prover

Date: 2026-08-12
Reviewer: the orchestrator seat's worker, which authored all three edits. The read they come from is
`docs/prover/2026-08-12-product-prover-full-read.md`, findings 2, 3 and 4.

Verdict: passes as a skill. Two edits state a rule the skill already implied. The third names where
a law is enforced. The frontmatter is untouched, and every test that reads this file is green.

The first draft of these edits went to a readability review and an adversarial review before the
push, on Alexander's word of 2026-08-12 23:09. The adversarial review refused the push over six
blocking findings, and the readability review returned fourteen of its own. Two of the blocking findings were
design questions the orchestrator seat answered, and both answers are recorded below as decisions.

Both reviews then ran a second time over the repaired tree, on his word of 2026-08-12 23:47. The
adversarial pass refused again over two blocking findings, and returned eight more beside them. The
readability pass returned twelve, four of them blocking. One blocking finding was a design question,
answered below as decision D-C. This record describes what landed after both rounds of repairs.

## What changed

The three findings the day's earlier review left open. Each one asked where a duty sits. So each carries a decision below, with the evidence that
settled it.

### Row 609 — the declaration member of the composition-lens family

The decision: INV-226 is the author's writing duty. This skill runs no sweep of its own for it.

**Seat decision D-B, forced by the adversarial review.** That review was right that membership of a
node settles nothing on its own. INV-138 and INV-248 are owned by the spec-author too, and both
carry prover lenses. The row's own recorded reason was also unrebutted: the spec's word for the
failure is defect, and defect is this skill's verdict to issue. The rebuttal that landed is narrower.
A defect this skill cannot see without knowledge the document does not carry is no verdict of its
own to issue. The part it can see is already swept, because the cross-surface uniformity sweep
catches the case where the members are sibling surfaces the document registers. So the answer is
stated in that qualified form everywhere it appears.

Four pieces of evidence settled that. The requirement's own user story is written from the author's
seat, reading "as a person writing a general law over instances". `ARCHITECTURE.md:98` gives INV-226
to the spec-author node, and `tests/test_instance_enumeration_keying.py` pins that ownership.
`TEST_MATRIX.md` row M-407 says the law is owned by spec-author, and none of its never-clauses names
a prover behaviour.

Membership of the family settles nothing on its own. The family already spreads across both tiers.
Paired-transition symmetry rides inside the lifecycle sweep with no line of its own.
Interactive-overlap and delivery separability sit among the imaginative probes, owing no verdict.

The deciding fact is who can answer the question. The law keys the choice on whether a member set is
closed, and the author is the person who knows that. A reviewer reads the declaration the author
wrote.

The edit: the cross-surface policy uniformity sweep gains a closing passage, in two paragraphs. The
first names the choice the law asks for, in plain words and with no project vocabulary. The second
says the author writes it, that this skill runs no sweep for it, and what this sweep does catch.
`PRODUCT_SPEC.md` criterion R264.5 places enforcement with the author and names that sweep, so the
spec carries the same qualification the skill carries. Its verb reads "place", since the spec's own
glossary gives "seat" to the acting session. The second readability pass moved that criterion's
"surface-shaped case" to "the sibling-surface case", which self-defines to a cold reader. The public
edition's own uniformity sweep then gained the same two paragraphs, carrying no invariant code,
which is the second adversarial pass's finding 9.

### Row 610 — what the cross-link mode skips

The decision: the skipped thing is Phase 3's property analysis, steps 3a through 3d. Every mandatory
sweep of Phase 3e runs on a surface add, the declared-laws sweep among them, with one exception. The
lifecycle sweep sends its paired-transition symmetry sub-question alone, and its other angles stand
down. The first draft promised all five sweeps fourteen lines under a bullet that stood the
lifecycle sweep down. The adversarial review caught it, and both copies now state the exception
where the promise is made.

The mode's own opening settled the first half. It already sent the mode into Phase 3e, and this
edit says how much of it runs.

The declared-laws half was settled by INV-101 and the spec-author skill. There the author writes a
new section's line against each declared law, "before the prover ever reads the delta". The prover's
cross-cutting station then audits those lines. On a surface add no other pass audits them. A new
surface is also the one surface arriving with no clause and no test row.

The edit: the mode's paragraph now names the skipped steps and says the declared-laws sweep fires,
with the reason beside it. Its opening reads "plus the Phase 3e lenses named below", since Phase 3e
holds eighteen entries and this mode runs seven. The declared-laws sentence names the mandatory
sweeps; its first draft said "the five", which pointed at the composition-lens list beside it. The
second readability pass then rewrote the lens list beneath that opening, so the seven derive on the
page. Five are members of the composition-lens family, the unwritten-seams sweep runs beside them,
and declared cross-cutting laws is the seventh. The public
edition carries the twin sentences, so it was swept. Its new-surface list gains the declared-laws
entry, its lens count moves from six to seven, and its verdict-line count moves from four to five.
The edition also stops implying that its five verdict lines fill the same columns a full review
renders. A full review's fifth column is lifecycle, and this mode's fifth entry is paired-transition
symmetry. The edition's mode section now says where the class line is written.

### Row 611 — the class lens in the tier that owes nothing

The decision: the class lens owes one line per pass, and it stands in a tier of its own.

**Seat decision D-A, forced by the adversarial review.** The first draft left the lens inside the
imaginative-probe list. It put a mandatory record line on it, citing INV-171 as the authority.
Criterion R67.2 says the opposite of what that citation was asked to carry: the probes are
discretionary and owe no verdict. A probe is a check the pass invents for the document in front of
it. The class sweep is a standing duty on every pass, whatever the document holds. Those are
different kinds, so the class lens leaves the list and stands under a heading of its own after it,
in both copies. Its sentences cite base rule 14 and state that rule in full beside the code. That
is what this page's own contract on bracket codes demands. R67.2 stands untouched, since the class
lens is no longer inside the set it describes.

The edit: the probe tier's opening returns to its committed wording, whole, with its colon and its
list. The class lens follows the list as its own tier. It opens on one sentence for why it stands
apart, and one that states base rule 14 in full. Its three questions move across unchanged. The
record shape gives the line three shapes: `Class lens: swept — <the classes filed>`,
`Class lens: no class`, and `Class lens: N/A — <reason>`. It also says when N/A applies, and when
"no class" does. The three renderings that stood in the tree are settled on that one. The README says the
lens is one duty standing beside the probes, and it introduces the written record before leaning on
it.

The public edition carries the class lens in `reference/stress-lenses.md`. Its tier list, its lens
and its README were swept the same way. Its lens moved under a heading of its own after the probe
list. The tier counts move from two to three in both copies. The edition README now reads
twelve imaginative probes, which is what the list holds once the class lens stands beside it.
The edition's two sample records gain their class line under the verdict table. Both probe notes now
say the class lens owes a line beside them, run 1's added by the second adversarial pass.

**Seat decision D-C, forced by the second adversarial review.** That review was right that the
first defence read criterion R67.2 alone and never read the Context sentence two lines above it.
Requirement 67's Context said the stress lenses split into two tiers, while both skill copies now
open on three. That Context now names three tiers, the third being the class lens, the standing
sweep that owes one record line every pass. Criterion R67.4 stands beneath it, stating the class
line's duty and its three readings, so the record's shape has a home in the spec.
`PRODUCT_SPEC.md` was refrozen afterwards.

## Findings

1. **No edit changes what a lens looks for.** Reviewed and clear. Row 609 names where an existing
   law is enforced. Row 610 names what an existing mode already ran. Row 611 adds a record line to a
   sweep the skill already described in full.

2. **The five mandatory sweeps stay five.** Reviewed and clear. Row 609 landed with no sixth sweep.
   The count pinned in `PRODUCT_SPEC.md` criterion R67.1, in both READMEs and in the edition's two
   sample records is therefore untouched. Row 610 widened no set either, because the declared-laws
   sweep was always one of the five.

3. **The class line agrees with INV-171.** Corrected by decision D-A. The first draft claimed this
   while the class lens still sat inside the set R67.2 calls discretionary, and it cited INV-171 for
   a duty that criterion refuses. The lens now stands in a tier of its own, cites base rule 14, and
   leaves R67.2 describing a set it is no longer in. Decision D-C then carried the third tier into
   Requirement 67's Context and gave the class line criterion R67.4.

4. **The edition was swept where it shares a sentence.** Reviewed and clear. It shares the
   cross-link skip sentence, the probe-tier opening and the class lens, and all three were swept. It
   carries no invariant codes, so the INV-226 passage was ported there with its code dropped.

5. **The fixture check is test-embodied, and it reaches fixtures alone.** Recorded so nobody reads
   it as a gate. `tests/test_class_hunt.py` now carries the class line's shape and five fixtures. A
   pass with a point finding and no class line reds. A swept line naming its class passes, and each
   of the three verdicts passes. A bare `swept` naming no class reds, and so does an N/A with an
   empty reason. The records already on disk in `docs/prover/` predate the rule, so a push gate over
   real records is queue row 615's work.

6. **The author's own skill states no enumerate-or-ride duty.** Open, and outside this unit's
   footprint. Row 609 places INV-226 with the author, and `skills/spec-author/SKILL.md` carries no
   paragraph asking whether a member set is closed. On this pack's own spec the law still has a net,
   because `tests/test_instance_enumeration_keying.py` holds that the three named laws cite the
   class. A project adopting the pack gets no such habit. It is now queue row 614.

7. **The queue's status vocabulary is open in fact.** Open, and queue row 616 carries it. Thirteen
   live rows read `done` in the status cell, three of them written by this change, and nine read
   `landed`. The file's own preamble declares neither, and `docs/roadmap-format.md` says a body row
   never carries `landed` as a status. This change keeps `done`, since it is what every closed row
   in the live body already reads.

8. **The prose holds its ceiling.** Reviewed and clear. Every file touched measures at or under its
   recorded count in `guardrails/rule-census.json`. The two counts standing above zero were already
   there. First drafts that ran past the 25-word cap were split before the measure, in both rounds.

## The measures this review was held to

Commands run and their results:

- `python3 -m pytest tests/test_class_hunt.py tests/test_prover_doc_homes.py
  tests/test_skill_review.py tests/test_declared_laws.py
  tests/test_instance_enumeration_keying.py tests/test_crosslink_quantifier_reverify.py
  tests/test_mirror_editions.py tests/test_readme_stance.py tests/test_traceability.py` — 260
  passed.
- `python3 -m pytest tests/test_full_pass_coverage_record.py` — 5 passed.
- `bash guardrails/check-skill-loadability.sh` — OK, 11 skills load, named, versioned,
  negative-scoped.
- `bash guardrails/check-skill-review.sh` — OK.
- `python3 guardrails/check-criterion-readability.py PRODUCT_SPEC.md` — OK, counts at or under
  baseline. Criterion R264.5 was trimmed to hold the 60-word total, which that gate refused at 68.
  Criterion R67.4, added by decision D-C, holds under the same baseline.
- `python3 scripts/spec-freeze.py --freeze PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md
  --compaction`, then `bash guardrails/check-freeze.sh` — green over three files.
- `python3 scripts/rule-census.py --json guardrails/rule-census.json` — every finding count held.
  Only the byte sizes of the touched documents moved.
- `python3 scripts/progress-report.py` — the progress page regenerated over the fresh census.
- `python3 scripts/spec-style-lint.py --tier full` on each touched document — no new tell landed,
  and every pre-existing count held at its HEAD figure. `ROADMAP.md` stands at 207, the two sample
  records at 43 and 46, and `editions/product-prover/SKILL.md` at 1, its caps tell on line 170. This
  record carries the marker its own format demands on line 3. Every document recorded at zero came
  back at zero.

## The skill-creator pass over the frontmatter, 2026-08-13

On Alexander's word of 2026-08-13 at 00:09 the skill went through Anthropic's skill-creator before the
night's push. That pass measured the one surface neither adversarial review read: the frontmatter
description, the line that decides whether the skill fires at all.

The measurement. Sixteen queries, eight positive and eight near-miss negatives, three runs each. The
skill never fired wrongly, at 24 of 24 negatives clean. It failed to fire on three of the eight
positives it should have caught:

- "read ARCHITECTURE.md and tell me whether every node earns its place" — 0 of 3.
- "stress test this migration plan" — 0 of 3. Generative stress-testing is Phase 3e, this skill's own
  core work, and the word was absent from the description.
- "attached checkout-v2-spec.md — thoughts?" — 1 of 3, against a description that promised that case.

### What landed on 2026-08-13

Four items, and nothing beyond them.

1. **The internal skill takes the edition's frontmatter description.** The `description:` value in
   `editions/product-prover/SKILL.md` was copied into `skills/product-prover/SKILL.md`. It carries what
   the internal line lacked: stress-test, lint, "is this spec ready", "what did I miss", "poke holes in
   this", architecture documents as a first-class noun, the skill's own name as a trigger, and the
   sentence saying it reads documents while code and diffs route elsewhere. It was measured before the
   paste: every sentence sits at or under 25 words, the longest at 21, and no sentence pairs a positive
   claim with the alternative it rejects. The frontmatter's other fields are untouched.
   `tests/test_prover_doc_homes.py` still finds "hold together as written" in the line, and no
   sibling-pass name and no anchor code entered it.

2. **The glossary trigger nothing can fire is gone.** The skill said its triggers were `/glossary`,
   `/glossary <term>` and `/define <term>`. This repository carries no `.claude/commands/` and registers
   none of those words, so a leading slash reaches the tool's own command picker. The skill now carries
   the edition's honest wording: the triggers are plain English inside a message, the same words after a
   leading slash count too, and a paragraph says why ordinary text is the working form. The two examples
   that quoted the slash form were rewritten with it. `skills/product-prover/README.md` repeated the
   claim to readers and now names the plain-text form with the same reason, matching the edition
   README's own line.

3. **"Seam" is defined in the internal skill.** The word carried sixteen uses across three senses and
   no entry in "Words this skill uses". The edition's bullet moved across whole, naming the three
   kinds — structural, situational, journey — and what each one owes. It carries no invariant code,
   because the edition's own sentence had none to carry.

4. **The tier definitions have one home in the public edition.** The three tiers stood near-verbatim in
   both `editions/product-prover/SKILL.md` and `editions/product-prover/reference/stress-lenses.md`, and
   the class-lens paragraph widened that duplication in both. The reference file keeps the rule, since
   the lenses live there. The main page now points at it in two sentences. Two rules the bullets carried
   beyond the reference file's copy moved down to the verdict table's own section, where the table is
   described: one verdict per cell, and the single-row collapse where a document lists no surfaces.

The later work the pass named opened as queue rows 618, 619 and 620: the body's split into a reference
directory, the standing sweep for skill-versus-edition content drift, and the base version pinned in
prose against two skills that forbid it.

### The measures this addition was held to

- `python3 scripts/rule-census.py <path>` on each touched file — `skills/product-prover/SKILL.md` 0
  findings at a longest of 25, `skills/product-prover/README.md` 0 at 25,
  `editions/product-prover/SKILL.md` 1 at 25, `editions/product-prover/reference/stress-lenses.md` 0 at
  25, and `ROADMAP.md` at 215 with 8 long sentences. Every one is at its recorded entry.
- `python3 scripts/spec-style-lint.py --tier full` on the same files — the edition's single caps tell on
  line 170 and `ROADMAP.md`'s 207 both held at their recorded figures, and no new error landed.
- `bash guardrails/check-skill-loadability.sh` and `bash guardrails/check-skill-review.sh` — both OK.

Red proof for the two new string tests. The adversarial review measured the first draft of them at
five searched sentences, one of which hit against the committed tree. That one read "reads as a
skipped sweep", which already stood in the mandatory-sweep paragraph, so it proved nothing about the
class line. Every searched sentence now names the class line, and there are seven of them. All seven
return no hit in the committed copies of the skill and its README. Both tests therefore fail against
the tree as it stood.
