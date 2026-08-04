# Skill review — the installed copies land, and six clauses come back

SKILL-REVIEW

Skills: build-pipeline, communicator, design-reviewer, feedback-collector, feedback-intake,
live-spec-base, product-prover, publish, spec-author, test-author, text-audit.

Date: 2026-08-05
Reviewer: skill-creator (Anthropic), run by this session. One record covers the eleven skills,
because one change reached all of them and each file took the same kind of edit.

Verdict: passes, with three findings. Every summary line still reaches the work its skill owns.
Every line is far shorter than the line it replaced. No body states a rule twice or contradicts
itself.

## What changed

Three commits, all on the night of 2026-08-04.

`d105b85` wrote the copies that each machine actually runs into the repository. Eleven summary lines
had been shortened on 2026-07-30 in the installed copies alone, and the repository still held the
long ones. Twelve situations that should make a skill fire had been restored into those short lines
before the commit. The `text-audit` body was swapped for a version rebuilt in place, replacing a
regenerated one.

`d3384a4` put one clause back into six skills, after the test suite showed the shortening had
dropped text this project's own tests require. Five clauses went back into a summary line. The sixth
went into the `test-author` body.

`cee884c` split one sentence in `text-audit` that ran to 31 words against the 25-word cap the skill
itself teaches.

## The summary lines, before and after

Word counts of the `description` field, taken from the frontmatter of each `SKILL.md` at
`origin/main` and at `HEAD`. They answer whether the shortening survived the restorations.

| Skill | Words before | Words after | Cut |
|---|---|---|---|
| build-pipeline | 119 | 31 | 74% |
| communicator | 138 | 65 | 53% |
| design-reviewer | 162 | 33 | 80% |
| feedback-collector | 124 | 44 | 65% |
| feedback-intake | 149 | 45 | 70% |
| live-spec-base | 159 | 53 | 67% |
| product-prover | 139 | 52 | 63% |
| publish | 118 | 36 | 69% |
| spec-author | 178 | 40 | 78% |
| test-author | 127 | 23 | 82% |
| text-audit | 186 | 21 | 89% |
| **all eleven** | **1599** | **443** | **72%** |

The five restored clauses cost about 66 words across three lines. The gain from shortening survived.
`communicator` is now the longest line at 65 words, and it carries the exclusion an earlier
triggering test demanded.

## Verdict per skill

**build-pipeline — passes.** The line names all six doors: feature, bug fix, behavior change,
refactor, docs-only change, feature removal. It keeps both exclusions. The spoken phrases went away:
a request worded only as "do this by the method" or "build X properly" now carries no matching word.
The body still names every door and the new-stateful-surface case.

**communicator — passes, with finding 2.** The line names the decision ask, the milestone report,
the "did we do X" answer, the product walkthrough, and the problem that needs a word. It keeps the
exclusion that an earlier triggering test was written for, so a passing status line no longer loads
the skill. Three words stand in capitals for emphasis, which finding 2 covers.

**design-reviewer — passes.** The line names the consistency check and the ungrouped same-kind items,
and it states that the skill holds no landing. The words "design review" left the line; the skill's
own name carries them. No body change.

**feedback-collector — passes.** The line opens with the enabled condition, so a host that never
switched the flag on stays clear of it. The restored clause names the actor that never sends the
note, matching the body's own statement at three places. No body change.

**feedback-intake — passes.** The line widened the inbox trigger on purpose: a file an agent left in
`inbox/` now reaches the skill, where the old wording read as a person's drop. The line drops the
exclusion for a remark a person merely mentions without handing it in. The body keeps that exclusion,
so behaviour after loading is unchanged.

**live-spec-base — passes.** The line names the ten pack skills, the worker briefing, and the
settings question, which is the whole set of load occasions. The restored clause says the body holds
thirty-five rules; the body holds thirty-five, counted from the numbered rule list. The claim appears
once, in the line alone.

**product-prover — passes.** The line names the review ask, the document kinds, the uploaded
document, and the unsaid word "review". The restored clause states the one question the skill
answers. The phrases "stress-test", "lint", and "poke holes in this" left the line; "find gaps"
carries the same ask.

**publish — passes.** The line names the public repo, the README push, the release, and the shared
skill, and it states that the human's own publish decision comes after. A plugin-directory submission
and a set of rendered cards sent outside the project are covered by the phrase about work leaving the
machine publicly, without being named.

**spec-author — passes.** The line names starting a spec, adding a feature, and keeping a spec in
sync, plus both exclusions. A question about how to structure a spec now has no matching word, and
that ask was in the old line.

**test-author — passes, with finding 1.** The line names the derivation from a proven spec and
architecture, and it separates the skill from reviewing the spec. Three direct-use phrases came back
into the body, and the summary line still lacks them. Finding 1 covers that.

**text-audit — passes.** The line names the text kinds and the first-time reader, in 21 words, the
shortest of the eleven. The body swap holds: see the next section. The line names no spoken phrase at
all, which is the deepest case of finding 3.

## The text-audit body swap

The whole body was replaced, so the review measured it against the version it displaced. A script
compared the two token by token over everything below the frontmatter.

- Every heading is identical, in the same order: twelve headings.
- Every code span is identical: no script name, file path, or rule code differs in either direction.
- Every number is identical: the four loop steps, the five lints, the two clean reads, the 25-word
  and 35-word caps, the ten-requirement batch.
- The differences are wording inside 23 regions. Each one names an actor, splits a long sentence, or
  turns a possessive phrase into a plain clause.

So the rebuilt version instructs the same actions as the version it replaced. The one later edit,
`cee884c`, split a 31-word sentence into two and left the phrase a test pins whole on one line.

## Findings

**Finding 1 — `test-author` states direct-use guidance under a heading that denies it.** Two
sentences now open the section `## Work that belongs elsewhere`: "Normally invoked by build-pipeline
at its matrix and test steps (5–6). Use it directly to derive the test matrix, to pin test levels, or
to rebuild a suite by the method." A reader who follows the heading reads work that belongs to this
skill as work that belongs to another. Two moves fix it, and both are for the owner to call: put the
sentences in a "When it fires" section of their own, or put the three phrases back in the summary
line where triggering reads them. `tests/test_traceability.py` pins the phrase "Normally invoked by
build-pipeline", so the test moves with the text. `skills/test-author/README.md` still advertises a
fourth phrase, "why did green tests miss this bug?", which neither the line nor the body carries.

**Finding 2 — the `communicator` summary line uses capitals for emphasis.** Three words stand in
capitals: the one for a reported milestone, and two in the exclusion clause. This project's writing
rules refuse a word in capitals for emphasis, and the rename of 2026-07-28 took that shape out of
every skill heading for that reason. `tests/test_traceability.py` asserts these exact strings, so a
repair changes the skill and the test together. The clause itself earns its place: it was written
after an evaluation caught the skill loading on every passing status line.

**Finding 3 — the shortening dropped the words a person actually types.** A skill is reached through
its summary line alone, so a phrase that lives in the body never reaches triggering. Each short line
keeps the meaning and drops the phrasing. The specific losses: "build X properly", "spec and ship Y",
"do this by the method" (build-pipeline); "should these be one kind", "what siblings did we miss"
(design-reviewer); "spec this out", "how do I structure a spec" (spec-author); "poke holes in this",
"is this spec ready" (product-prover); "why did green tests miss this bug" (test-author);
"cold-read this", "is this README clear", "check this for undefined terms" (text-audit). The bodies
still list them under "When it fires", where triggering never looks. The cheap repair is one short
clause of example phrasing per line, which costs about eight words each and keeps the lines well
under their old length.

## What was checked, and what it said

- **The gate.** `bash guardrails/check-skill-review.sh` names all eleven skills as carrying a review
  older than their last change. It will keep naming them until this record is committed, because it
  reads committed files alone. Running it as `sh` fails with a syntax error at line 120: the script
  uses a bash-only construct and declares bash in its first line.
- **The register lint.** `python3 scripts/preshow-register-lint.py` was run over all eleven skill
  files. Ten pass. `communicator` reports 11 findings, and the same 11 stand at `origin/main`, so
  this change neither added nor removed one. They fall on the passages where the skill quotes banned
  wording as its own examples.
- **Duplication.** Each of the five restored clauses appears once in its file. None repeats a
  sentence that already stood elsewhere in the same body.
- **The rule count.** `live-spec-base` claims thirty-five rules and holds thirty-five.
- **The tests behind the restorations.** Five tests pin the restored text by exact phrase:
  `test_traceability.py` for the communicator clause and the test-author clause,
  `test_clean_context_review.py` and `test_resume_rederive.py` for the rule count,
  `test_prover_doc_homes.py` for the prover's question, and `test_reader_prompt_shape.py` for the
  reader's written guess.

## What a fresh reviewer should look at

Whether a summary line should carry example phrasing at all. Finding 3 assumes it should, following
the skill-creator guidance that a description names both what the skill does and the contexts that
should reach it. The shortening of 2026-07-30 was a deliberate move the other way. One of the two
readings should win for all eleven skills at once.

Also worth a second opinion: `communicator` says "a human" where its own body now says "the user" in
places. The word choice is older than this change and reaches far past these eleven files, so it was
left alone here.
