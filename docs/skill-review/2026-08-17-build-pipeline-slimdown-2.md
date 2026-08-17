# `SKILL-REVIEW` — build-pipeline, second pass: the returns land clean, one duplicate survives them

Skill: build-pipeline. Date: 2026-08-17. Range: 9efe559..HEAD.

This record supersedes `docs/skill-review/2026-08-17-build-pipeline-slimdown.md` (the first-pass record,
committed at 3905f7f) for `build-pipeline`. That record reviewed the tree as of commit 88c4622 and is now
stale: commit 94ae4c3 changed the skill again after it was written, so its own commit is older than the
skill's last change and it can no longer satisfy the push gate's freshness rule (`guardrails/check-skill-review.sh`,
SPEC INV-208). This record reviews the current tree, HEAD, which includes 94ae4c3.

Verdict: ALLOW WITH FINDINGS. Three of the first record's four repair items are fully cured: the broken
relative link, the audit's firing condition, and the fitness test's three questions are all back where a
worker needs them, restored word for word against the pre-slimdown body, with no new duplication at either
of those two return sites. The fourth item — the six-invariant restatement in
`references/delegation-protocol.md` — is mostly cured but not entirely: one paraphrase pair survives inside
that same file, and a stale byte-count sentence sits beside a count that no longer matches it.

## What 94ae4c3 actually did (verified, not assumed)

I ran `git show 94ae4c3 -- skills/build-pipeline/` myself. Five files changed under this skill:

- `SKILL.md` — the architecture step's fitness-test bullet regains its three questions and the one-no/two-no
  reading (was: a bare "see reference" naming the test and nothing else); the verify step's audit bullet
  regains the high-stakes definition and the author's-own-review definition, both named traps included (a
  prover pass in the author's own context, delegation). Net: SKILL.md 559 to 568 lines.
- `references/architecture-step-detail.md` — the fitness-test section drops its own copy of the three
  questions, opens "The three questions themselves... stand in `SKILL.md` at the architecture step: they are
  the test's firing condition and belong where the step is walked," then states only the test's two homes
  and what a failed carve costs.
- `references/verify-step-detail.md` — same move for the audit: the high-stakes and author's-own-review
  definitions are gone, replaced by "When the audit FIRES... stands in `SKILL.md` at the verify step: that
  is the gate's firing condition," then the file keeps only how the audit runs once fired.
- `references/lanes-and-pen.md` — the drafter-applier link changes from
  `[references/drafter-applier-example.md](references/drafter-applier-example.md)` to
  `[drafter-applier-example.md](drafter-applier-example.md)`.
- `references/delegation-protocol.md` — the appended tail's heading changes from "The brief, the worker
  contract, and the reporting duty, as the body stated them" to "The cleanup-safety constraint, and the
  grounding law's canonical wording"; the paragraph restating the brief's three birth laws, the worker
  contract, and write-set disjointness is deleted, replaced by one sentence saying those, plus the reporting
  duty, are stated above in the file and not restated here, then just the cleanup-safety clause.

This matches the brief's description of "four operational passages... plus one relative-link fix," with one
correction: the delegation-protocol.md change is a fifth, real edit in the same commit, not folded into the
"four passages" count — it repairs (partially, see below) the first record's separate finding about that
file's duplication, which the brief's summary did not mention. `ARCHITECTURE.md` and
`guardrails/rule-census.json` also move in the same commit, consistently with the SKILL.md line shift (60
lines changed in each, per `git show 94ae4c3 --stat`).

## Verbatim check on the two returns

I diffed the restored SKILL.md passages against `git show 9efe559:skills/build-pipeline/SKILL.md`. The
fitness-test sentence at current SKILL.md:310-312 is byte-identical to the pre-slimdown body's lines
337-339. The audit passage at current SKILL.md:402-410 is byte-identical to the pre-slimdown body's lines
442-450. Both firing conditions are back in the body in their original words, not paraphrased.

## Whether the returns introduced new duplication

No, at both sites. `references/architecture-step-detail.md`'s fitness-test section and
`references/verify-step-detail.md`'s audit section were rewritten, not merely trimmed — each now opens by
naming the firing condition's location in the body and explicitly disclaims restating it ("What follows is
where the test lives," "What follows is how the audit is run once it has fired"), then states only the
elaboration the body doesn't carry (the test's two homes and the folded-back consequence; the briefing
protocol and the ladder). I read both files in full: neither repeats a sentence that now stands in the body.
This is the shape the first record asked for — the firing condition in one home, the elaboration in the
other, a live pointer stating when to leave the body — and it is done correctly at both sites.

`references/lanes-and-pen.md`'s link now resolves: `test -f
skills/build-pipeline/references/drafter-applier-example.md` succeeds, and the link as written,
`[drafter-applier-example.md](drafter-applier-example.md)`, is the correct relative form from inside
`references/`. A repo-wide grep for `drafter-applier-example` finds it in exactly one place, that link, and
it is no longer broken — the file has exactly one hop in from `SKILL.md` via `lanes-and-pen.md`, same as
before the defect, not zero hops as it was after 88c4622.

## The one item not fully cured: `references/delegation-protocol.md`

The first record's fourth finding said this file restated all six things the body's "Junior delegation"
bullet had pointed at it for, with the brief's birth laws, the worker contract, disjointness, and the
reporting duty paraphrased rather than quoted, and asked that the appended section shrink to the one clause
it actually added (the cleanup-safety constraint). 94ae4c3 does most of this: the paragraph restating the
birth laws (INV-53/54/55), the worker contract (ACT-3), and write-set disjointness (INV-105) is deleted
outright, and the file's new closing section states plainly that those, plus the reporting duty, "are stated
above and are not restated here" — true, I checked, they appear exactly once each, in the file's older,
pre-append body (lines 22-97).

But one restatement survives, because it predates 88c4622's original append boundary and 94ae4c3 never
touched it. Line 96 of the file (unchanged before and after 94ae4c3) reads: "Each work block in the report
opens by naming its root, and the report accounts the block against its announced plan line (SPEC INV-314)."
Lines 108-110, the file's closing paragraph (also unchanged by 94ae4c3 — the diff shows it as context, not a
hunk), read: "Each work block in the report opens by naming its root. The root is the person's dated
request, a standing instruction, or a stated reason, and machinery is never a root. The report accounts each
block against its announced plan line (SPEC INV-314)." Both state the same duty under the same invariant,
twelve lines apart in the same file — the second adds one definition ("what a root is") the first lacks, so
it is not a byte-identical duplicate and the first record's exact-string check would not have caught it, but
it is the same law told twice with no marker for which telling governs. I confirmed this predates 94ae4c3 by
diffing `git show 88c4622:.../delegation-protocol.md` against the current file: the exact pair is present,
unchanged, at both commits. 94ae4c3 cured four of the five restated items and left this fifth standing.

A second, smaller loose end in the same neighborhood: `guardrails/rule-census.json`'s entry for this file
was updated by 94ae4c3 on its numbers (`"total": 58` to `53`, bytes 10060 to 9263) but not on its `reason`
narrative, which still reads "...this entry rose 52 to 58" — a sentence now contradicted by the `"total": 53`
three keys over in the same JSON object. This is bookkeeping, not skill content, and every rule-census test
I ran passes against the current numbers (`test_rule_census_ratchet.py`, `test_rule_census_prose_units.py`,
`test_doc_findings_bound.py`, `test_skill_count_agrees.py` — all green), so nothing is mechanically broken;
the stale sentence is a small honesty gap in a file that otherwise exists to keep provenance honest.

## The rest of the skill, re-walked

Frontmatter, name, and description are untouched by 94ae4c3 and were already sound at the first pass: the
name is unambiguous against sibling skills, and the description enumerates every door by name, gives the
setup entry its own spoken phrases, and closes with an explicit negative boundary (a tiny reversible edit,
pure research) — exactly the near-miss discrimination skill-creator's guidance asks a description to carry.
No finding here.

Length moved the wrong direction on the raw number, in service of the right fix: SKILL.md is 568 lines
against skill-creator's <500-line guidance, up from 559 at the first pass, because the two restorations
added content back. This is the correct trade-off — a required gate's firing condition belongs in the body
even at a few lines' cost — and skill-creator's own escape hatch ("feel free to go longer if needed," paired
with "add an additional layer of hierarchy" as you approach the limit) is what this skill is doing: the body
still defers the bulk of the architecture and verify steps' elaboration to references, it just no longer
defers the part a worker needs to decide whether the gate fires. Step 3 still opens three separate "see
reference" hops to the same `architecture-step-detail.md` file (budgets' per-kind numbers, the two extra
views, and now the fitness test's two homes) — the first record's mild navigability quibble here is
unchanged, though two of the three passages are now inline content followed by a pointer, not bare pointers.

All twelve reference-file names outside `drafter-applier-example.md` are still named directly in `SKILL.md`
and all resolve; `drafter-applier-example.md` is reachable in one hop through `lanes-and-pen.md`. No
reference file in this skill is orphaned. `references/delegation-protocol.md`'s own architecture pin in
`ARCHITECTURE.md` (lines 166 and 464) still resolves to real content at those lines. The first record's
lower-priority items — the runtime/placement-view gloss sitting closer to the prover step than the authoring
step; `mockup-first-entry.md` being a thin file for a thin saving; the two lane-law pins both citing
SKILL.md:513 — are untouched by 94ae4c3, which is consistent with the brief's description of this commit's
scope. They were called misses or waste, not defects, at the first pass, and that grading still holds: none
is a firing condition or a lost fact, and `tests/test_architecture_pins.py` passes with both pins present.

## What I ran

`git show 94ae4c3 -- skills/build-pipeline/` and `--stat` for the full commit; `git show
9efe559:skills/build-pipeline/SKILL.md` diffed by hand against the current body at both return sites;
`test -f` and `grep -rn` across `skills/build-pipeline/` for every reference filename to check reachability;
`git show 88c4622:skills/build-pipeline/references/delegation-protocol.md` against the current file to date
the surviving duplicate; a `python3 -c` read of `guardrails/rule-census.json`'s two build-pipeline entries;
and `python3 -m pytest -q` over ten targeted test files (`test_skill_count_agrees.py`,
`test_doc_findings_bound.py`, `test_rule_census_ratchet.py`, `test_rule_census_prose_units.py`,
`test_check_registry.py`, `test_delegation_line.py`, `test_no_dramatization_law.py`, `test_worker_restore.py`,
`test_traceability.py`, `test_architecture_pins.py`) — 345 passed, 1 failed. The one failure reds on this
machine's own historical worker-run transcripts under `~/.claude/projects`, unrelated to `build-pipeline`'s
content or to 94ae4c3 — the same machine-local transcript matter this range's other commits (`ed7c3bf`,
`b0a2066`) already track, not a finding against this skill. No file under `skills/`, `guardrails/`,
`ARCHITECTURE.md`, or `tests/` was modified during this review.

## The net

`build-pipeline` clears the push gate on this record. The two firing conditions the first pass flagged as
the review's most consequential findings are back in the body, verbatim, without re-duplicating into the
reference files they came from, and the orphaned reference is reachable again by the correct relative path.
What is left is small: `references/delegation-protocol.md:96` and `:108-110` still tell the per-block root
and plan-line accounting duty twice in twelve lines, a leftover from 88c4622 that 94ae4c3's cleanup did not
reach, and the same file's `rule-census.json` entry carries a `reason` sentence whose numbers no longer
match its own `total`. Neither blocks a worker executing the pipeline and neither is a lost or reworded
fact; both are worth a follow-up commit, not a hold on this one.

Reviewer: an independent adversarial second-pass read of `build-pipeline` at HEAD against 9efe559 and
against the first-pass record's own findings, performed by a dedicated reviewer agent for this range.
Evidence gathered by `git show`, `git diff`, `test -f`, `grep -rn`, a `python3 -c` JSON read of
`guardrails/rule-census.json`, and `python3 -m pytest -q` over ten targeted test files. No file outside this
one review record was written or modified during the review.
