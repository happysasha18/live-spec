# Skill review — the prover skill defines its own words and finishes its pointer sentences

SKILL-REVIEW

Skills: product-prover.

Date: 2026-08-05
Reviewer: skill-creator (Anthropic), run by this session.

Verdict: passes. The change adds a definitions block and completes sentences that trailed off. It
removes no instruction. Four places add a step, and each one is named below.

## Why it was worth a change

A readability audit read this file twice with fresh readers and confirmed 29 findings, 10 of them
blocking. Eleven findings, F1 to F11, named a step a reader cannot carry out from the page alone.
A session that loads a skill acts on it; a step it cannot perform is skipped with no trace, and the
output still looks complete.

## What changed

**A "Words this skill uses" block near the top.** It defines surface, the surface registry, lens,
sweep, station, fold, `[default]`, landing, queue row, seat, and the verb red. It says what the
`INV-`, `E-`, `M-`, `C-`, `T-`, `P9`, and base-rule codes are and where each resolves. It names the
two people the review addresses, the author and the person. It states that every path on the page is
relative to the live-spec repository root, and what a bare bracket at a lens's end means.

Every definition was taken from a source in the tree: the spec's own glossary, its preamble, and the
requirement each code trails.

**Four pointer sentences completed in place.** The three node-fitness questions are listed inline
(SPEC INV-122, R119.1). The declared-laws home now carries the test that recognizes it, with this
pack's own Requirement 54 as the worked case. CROSS-LINK names the Phase 3e items it runs. The seven
feature-fit seams each carry a half-line gloss, and the per-kind lens lists are pointed at their home
in `skills/spec-author/SKILL.md`.

**The mandatory-sweep record settled in one sentence.** Phase 3e now states that every FULL pass
renders the surface × sweep table, one verdict per sweep per surface, collapsing to one row where the
document lists no surfaces. The two later places repeat that rule rather than contradicting it.

**Smaller repairs.** Three "above" references that pointed at text below were corrected. The one
exception to "a defect blocks" is stated in words beside its code. The category table's densest cell
moved out into its own short block. The finding ID gained its numbering rule. Provenance passages are
marked as notes. Gendered pronouns for a role are written as the role.

## What the review looked at

**Does the summary line still trigger correctly?** The frontmatter description is untouched. The
change sits in the body.

**Does the body hold together?** Yes. Each new definition agrees with every later use of the word.
The `[default]` definition agrees with Phase 5's count line, and the surface-registry definition
agrees with the cross-surface uniformity sweep that reads it.

**Does it instruct anything new?** Four places do, and each is deliberate:

- Phase 0 gains the branch for a missing PRODUCT_SPEC.md: ask the author, and where none can be
  produced, record the ownership check as not runnable and run the remaining six. This text already
  ships in this pack's own standalone edition of the skill, `editions/product-prover/SKILL.md`.
- The merge gate now says it stands down where no old tree is in reach. The gate's own trigger, a
  restructure gated for merge, already scoped it that way.
- The token-identity part now states that no script ships for it today, and names ROADMAP row 204 as
  the queued home for one. That row reads *queued*.
- Phase 5's "oldest 5 `[default]`" now reads oldest as document order. See the finding below.

**Could the change be read as permission to skip a check?** One place invites the reading: a project
with no surface registry takes an N/A verdict on the sweeps that read one. INV-171 already holds
that road — an N/A verdict carries its reason, and a missing verdict line reads as a skipped sweep.
The escape is closed by the rule the sentence sits under.

## Findings

**One finding needs the owner's word.** A `[default]` tag carries no date, and nothing in the tree
says what "oldest" reads from. This repair chose document order, since that is the only age the
document itself carries. The other available reading is the prover records: a tag named in an earlier
dated record is older. Whoever owns the rule should settle which one holds.

**One observation for a later pass.** The file is 1053 lines. The skill-creator guide holds 500 lines
as the working ideal and asks for a layer of hierarchy past it, with pointers saying where to go
next. This pack's own standalone edition already does that: Phase 3e's lenses live in
`editions/product-prover/reference/stress-lenses.md`, and the main page tells the reader to open it.
The internal copy keeps every lens inline. Splitting it is its own delivery, and this change made the
file 106 lines longer.

**One repair reached past the audit.** The audit named three names for one artifact inside
`SKILL.md`. The skill's own `README.md` carried a fourth, "a reconciliation note", for the same
thing. It now reads "the architecture document's node pins", so the skill's directory holds one name.

**Two audit findings were left open, each with its reason.**

- One of the four wrong-direction "above" references, in the cross-surface uniformity sweep, is
  asserted verbatim by `tests/test_cross_surface_policy.py`. Correcting the word reds that test, and
  `tests/` sits outside this change's write-set.
- The diagram triggers still read "more than 3 entities with non-trivial relationships". Sharpening
  "non-trivial" would change when a diagram is rendered, which is an instruction rather than a
  definition.

## Checks run

`python3 scripts/preshow-register-lint.py skills/product-prover/SKILL.md docs/skill-review/2026-08-05-product-prover-readability-repair.md` — exit 0, no coined
metaphor, calque, or transliterated term found.

`python3 scripts/rule-census.py` — `skills/product-prover/SKILL.md` measures 0 findings before and 0
after, its longest sentence holding at 25 words. The count holds at the recorded ceiling.

`python3 -m pytest tests/test_config_health.py tests/test_prover_doc_homes.py tests/test_traceability.py -q` — 211 passed, so the repository copy
and the installed copy hold the same bytes.

The whole suite was run beside it: 2339 passed, 5 failed. Each failure traces to another process's
edit of `PRODUCT_SPEC.md` or `skills/text-audit/`, and none names this skill.

`sh guardrails/check-skill-loadability.sh` — 11 skills load, named, versioned, negative-scoped.
