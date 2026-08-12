# Skill review — product-prover (the record filename matches its own gate, and the lifecycle lead-in counts what follows it)

SKILL-REVIEW

Skill: product-prover

Date: 2026-08-12
Reviewer: the orchestrator seat, which authored both edits. It read the whole skill earlier the same
day, and that read is `docs/prover/2026-08-12-product-prover-full-read.md`.

Verdict: passes as a skill. Both edits are textual, neither touches a rule the skill states, the
frontmatter is untouched and still describes the body, and every test that reads this file is green.

## What changed

Two of the five findings from the day's full read, chosen because neither carries a judgment call.

**Row 608.** The meta rules said the findings are written to `docs/prover/YYYY-MM-DD.md`.
`guardrails/check-prover-record.sh:131` tells the author the opposite in its own repair line, naming
`$TODAY-<slug>.md`, and 356 of the 360 dated records in this tree already carry a slug. The sentence now
reads `docs/prover/YYYY-MM-DD-<slug>.md`, and two short sentences after it say what the slug is for:
it names the pass, and it is what lets a second pass on the same day write beside the first. Without
that, the second pass overwrites the first record's folded-or-rejected column, which the very next
paragraph says is what makes a fold verifiable after a memory wipe.

**Row 612.** The lifecycle sweep read "The parent gathers five angles:" and six bullets followed. The
count was defensible, because the first bullet is the transition-payload parent itself. It still
stopped a reader against the skill's own count-versus-contents lens. The lead-in now reads "The parent
lens stands first below, and the five angles it gathers follow it:", so the bullet count and the
stated count agree on first reading.

## Findings

1. **Neither edit changes a rule.** Reviewed and clear. The record's shape, its fields, and the six
   lifecycle sub-questions are all untouched. Row 608 changes the path a record is written to and
   nothing about what it must carry. Row 612 changes a lead-in and no bullet.

2. **The prescribed path now matches the gate that reads it.** Reviewed and clear.
   `guardrails/check-prover-record.sh` matches records by `<prover-dir>/<date>*.md`, so both the old
   bare-date form and the new slug form satisfy the match; what changed is that the skill and the
   gate's repair line now tell an author the same string. The 360 dated records already on disk are
   unaffected.

3. **The public edition needs no sweep for row 608, and none exists for row 612.** Reviewed, and it
   corrects an assumption the full-read record made. `editions/product-prover/SKILL.md` is a
   standalone edition carrying no `docs/prover/` path at all, so the record-filename sentence has no
   twin there. Its lifecycle section carries no "gathers five angles" lead-in either. The one sentence
   the two copies do share is the cross-link mode's "whole-document property sweep", which is row 610
   and stays open.

4. **The three findings left open each carry a decision.** Recorded so the next pass reads them as
   deliberate. Row 609 asks whether the declaration member of the composition-lens family earns a
   sixth mandatory sweep, which moves a count pinned in the spec, the README, the public edition and
   its examples. Row 610 asks what the cross-link mode skips, and answering it either narrows or
   widens what a surface add checks. Row 611 asks whether the class lens owes a verdict line though
   its tier says none is owed. None of the three is a wording fix, and none was made here.

5. **The prose stays at zero.** Reviewed and clear. This file is a cleared document in
   `guardrails/rule-census.json`. The first draft of the row-608 edit put a 33-word sentence in and
   the ratchet caught it; the sentence was split, and the file measures 0 findings again at 67,562
   bytes.

## The measures this review was held to

Commands run and their results: `python3 -m pytest tests/test_class_hunt.py
tests/test_full_pass_coverage_record.py tests/test_edge_completeness.py
tests/test_crosslink_quantifier_reverify.py tests/test_declared_laws.py
tests/test_enumeration_reads_as_list.py tests/test_design_principles.py
tests/test_interface_coverage.py tests/test_clean_context_review.py` — 74 passed;
`bash guardrails/check-skill-loadability.sh` — OK, 11 skills load, named, versioned, negative-scoped;
`python3 scripts/rule-census.py skills/product-prover/SKILL.md` — 0 findings, longest sentence 25
words; `python3 guardrails/check-doc-findings-bound.py` — OK, 123 live documents, none above its
record.

The mirror re-sync his standing ask names is owed after these edits are pushed, because
`scripts/sync-mirrors.sh` publishes the public edition and reads the committed tree.
