# Prover record — 2026-08-31 one home per rule

PUSH-REVIEW

Range: 57ec6d85..HEAD (6 commits, plan-16).

## What this range is

Three rules that stood in several homes at once converged to one home each, with a pointer wherever
a copy stood: the report the owner reads every turn, the parallel-work law, and the ask-never-guess
family. Six skills stopped listing sixteen base rules by nickname, three of them retired on
2026-08-26. A new check, `tests/test_one_home_per_rule.py`, reds a second copy. The director gained
the five houses a rule can enter and the sentence that sends it to one of them.

## The architecture delta, which is what this record is owed for

`architecture/pipeline-and-lanes.md` changed in three pin lines and one clause of a pin's label.
The `[node: parallel-lanes]` node kept its responsibility, its owned facts and its notes word for
word. Two pins into `skills/director/references/lanes-and-pen.md` follow that file's new line
numbers, one pin's label now names the half of the law it actually stands over rather than the whole
of it, and the base-rulebook pin says that the cap and the lane-open act have their one home there.
No fact moved out of the node, none entered it, and no owned code was added or dropped. The pin at
`skills/director/SKILL.md:250` moved to `:258` because that file gained a paragraph above it.

This is the small-delta case the host profile's `prover.cadence` line names, so it rides the short
form.

## Why this record is honest rather than exhaustive

The pins were not re-derived by hand. `bash guardrails/check-pin-drift.sh` reads all 173 of them and
proves each against its own line, and it was run before and after: it named the drift this range
introduced, and it returns OK now, alongside the r5 page's 39 range pins, which were repointed in
the same range with a dated note on the page.

The one judgment worth recording is what was cut from `lanes-and-pen.md` and what stayed. Cut: every
sentence base rule 7 already states — the cap, the pen's serialization, the lane-open act's steps,
worktree isolation, the one-row landing commit, and the seat's-read clause. Kept: the dependency
graph and what draws an edge, the pre-rolled build stages with the landing order declared at claim,
the queue-take's re-scan of deferred triggers, the bug that takes the pen at the end of a pen-stage,
the re-fence waiting lanes run after a landing, the drafter-applier form, and the re-door's rebuild
of the independence edges. Every one of those is a fact base rule 7 does not carry, so nothing left
the tree. Three suite assertions that had pinned cut sentences in the copy now read them at the
home, with the reason written beside each.

Files read: `skills/live-spec-base/SKILL.md` rule 7 in full, `skills/director/SKILL.md`,
`skills/director/references/lanes-and-pen.md` as it stood, `architecture/pipeline-and-lanes.md`'s
parallel-lanes node, and the four suite files that pin into them.

Checks run: `bash guardrails/check-pin-drift.sh` (OK, 173 pins + 39 r5 range pins); `python3
guardrails/check-architecture-reference.py` via the suite; `python3 guardrails/check-board.py` (OK);
`python3 guardrails/check-doc-rotation.py` (OK); `python3 guardrails/check-language-rules.py` (OK);
`LIVE_SPEC_DIFF_BASE=57ec6d85 python3 guardrails/check-landing-next-steps.py` (OK);
`LIVE_SPEC_DIFF_BASE=57ec6d85 bash guardrails/check-skill-review.sh` (OK, ten skills);
`python3 scripts/preshow-register-lint.py` on each new or rewritten page (OK); `python3 -m pytest
-q` on the committed tree.

Findings: none against the architecture. No requirement, criterion, invariant or anchor changed
meaning; the node's owned code list is untouched.

Blocking: none.

Standing, and not this record's to clear: `tests/test_config_health.py` reds while the installed
skills under the machine's own home differ from this branch's sources, which is what editing a skill
on a lane branch always looks like until the merged tree is synced.
