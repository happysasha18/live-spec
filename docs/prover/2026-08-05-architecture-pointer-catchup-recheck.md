# Prover record — the design map's pointer catch-up, re-check, 2026-08-05

Prover skill: product-prover, live-spec pack v4.3.0. Mode: delta-scoped re-check over the one
`ARCHITECTURE.md` change in `50fffff`, plus the whole-document quantifier re-verify the mode keeps
(SPEC INV-170), plus the class sweep a found defect draws (base rule 14, SPEC INV-124). Written by a
seat that authored none of the work under review (SPEC INV-237).

## Scope

**What this record reviews.** The tree at `dce526c`. The delta is `50fffff`, which changed two lines
of `ARCHITECTURE.md`: the `[node: spec-author]` pin block's first two pins moved from
`skills/spec-author/SKILL.md:154` to `:221` and from `:180` to `:247`. The last committed prover
record before it is `c3c9899`, which the push gate reads as older than the architecture change.

The pass covers the delta, the pin block it sits in, the document preamble the commit message cites,
and the same-kind pins elsewhere in the document.

**What this record leaves alone.** Other sessions' uncommitted work stands in the tree —
`docs/PROGRESS.md`, `guardrails/progress-baseline.json`, `docs/push-review/`, `ROADMAP.md` and
`skills/text-audit/`. None of it is read as part of this delta, and none of it is touched. Findings
below that name a file other than `ARCHITECTURE.md` are recorded and left for their owner.

**What the earlier records already covered.** `docs/prover/2026-08-05-readability-day-spec-recheck.md`
re-read both guarded documents against the five commits up to `52aa815` and ran the pin gate, which
reported five pins at that point. `docs/prover/2026-08-05-public-edition-and-reader-repairs.md` and
`docs/prover/2026-08-05-night-campaign-push-recheck.md` cover the public edition, the mirror sync and
the night's five landings. This pass repeats none of that. It reads the pointer question alone,
which no earlier record on this date reached.

**Commands run.** Every number below comes from one of these.

- `git show 50fffff -- ARCHITECTURE.md` — two lines changed, two pins.
- `python3 guardrails/archformat.py --pins ARCHITECTURE.md` — 205 pins parsed; 21 into
  `skills/live-spec-base/SKILL.md`, 10 into `skills/build-pipeline/SKILL.md`, 7 into
  `skills/communicator/SKILL.md`, 6 into `skills/spec-author/SKILL.md`, 3 into
  `skills/product-prover/SKILL.md`.
- `bash guardrails/check-pin-drift.sh` — 205 pins checked, exit 0, four reported as drift. All four
  name a whole file by its first line: `scripts/install-pack-hooks.sh:1`,
  `guardrails/rule-census.json:1`, `skills/design-reviewer/SKILL.md:1`,
  `skills/text-audit/SKILL.md:1`.
- Direct reads of each pinned line in `skills/spec-author/SKILL.md` (739 lines),
  `skills/live-spec-base/SKILL.md` (730 lines), `skills/communicator/SKILL.md` (499 lines),
  `skills/build-pipeline/SKILL.md` (662 lines) and `skills/product-prover/SKILL.md` (1054 lines).
- Heading and anchor greps over the same five files, to locate where each pinned thing now stands.
- `git show 501212d:skills/spec-author/SKILL.md` — the copy the spec-author pins were last written
  against, read at the same line numbers.
- `git log --oneline -- <skill>` and `git show --stat` over today's commits, to establish which
  skills were rewritten after the last pin sweep in `6167a6e`.

## Verdict

**The delta is correct and incomplete. Both pins it moved now resolve, and the same rewrite left
three more pins in the same block pointing at the old text. The class reaches past that block:
29 pins across three skills point at lines the thing they name no longer stands on, and the drift
gate calls every one of them clean.**

Nothing here blocks the delta from going out. `50fffff` moved two pointers closer to the truth and
moved none of them further away. The blocking question is the pin gate's reach, which is a finding
against `guardrails/check-pin-drift.sh` and belongs to that file's owner.

## What holds

Three things are worth saying plainly.

The two moved pins land. `skills/spec-author/SKILL.md:221` is the line
`## The spine — what every spec must contain (not its section order)`, and the pin's label reads
`(spine)`. `:247` is the line beginning `**Name the future with the [target] tag — it is a tripwire
that drives the pipeline.**`, and the pin's label reads `([target] tag tripwire)`. Each pin names
the thing the label promises, at the line it gives.

The commit message's claim about the gate holds as stated. Four pointers stand named by the drift
check, and each names a whole file by its first line. The document preamble carries the sentence
that explains why: "A pin whose line reads 1 names the file as a whole."

The neighbouring nodes are clean. All 10 pins into `skills/build-pipeline/SKILL.md` and all 3 into
`skills/product-prover/SKILL.md` resolve to the line the label names. Those two skills were swept in
`6167a6e` and have not been rewritten since.

## Findings

F1 — Three of the six pins in the node this commit repaired still point at the pre-rewrite lines

> "- `skills/spec-author/SKILL.md:265` (fences)" — ARCHITECTURE.md, `[node: spec-author]`, pins

The same rewrite that moved the spine and the `[target]` tripwire moved three more of that node's
six pins, and the commit moved two of them. An agent following the design map to the regression
fences reads line 265, which now carries `**Reshaping an existing spec? Hold the anchor-set
guard.**`; the fences heading stands at 333. Following it to the facet sweep reads line 280, which
now carries a fragment of a facet list, `**concurrency** where it applies ·`; the facet sweep heading
stands at 349. Following it to the enumeration-threshold rule reads line 97, which now carries
`- **The body is a list of requirements; each opens with its situation.**`; the INV-215 rule stands
at 154. Each of the three landed correctly in `501212d`, the copy the pins were last written
against, so all three broke in today's rewrite alongside the two the commit fixed.

Move the three pins to the lines their labels name: `:265` to `:333`, `:280` to `:349`, `:97` to
`:154`. Re-read each after moving, since the gate cannot confirm the move.

`defect · missing-outcome-check (postcondition)`

F2 — Every pin into the shared rulebook points at the pre-rewrite line, and one lands on the wrong rule

> "- `skills/live-spec-base/SKILL.md:339` (rule 20, INV-65 — skill search at setup and struggle)" — ARCHITECTURE.md, `[node: base-rulebook]`, pins

`5e157de` rewrote `skills/live-spec-base/SKILL.md` today, 772 lines changed, after `6167a6e` had
swept the document's pins. All 21 pins into that file now sit 12 to 45 lines above the thing they
name. The pin quoted above is the sharpest case: line 339 is rule 19's own opening line,
`19. **The problem ledger — workshop noise is owned, never re-suffered.**`, while rule 20 stands at
358. An agent sent to rule 20 arrives at rule 19 and reads a rule that answers a different question.

The offsets, each read directly: rules section `:105` → 117; rule 6 `:148` → 160; rule 7 `:168` →
182; the lanes sub-rules `:173` → inside rule 6, since rule 7 opens at 182; the INV-298
worker-restore sub-rule `:195` → 209; one row per landing commit `:196` → 210; rules 15-16 `:279` →
297; rule 19 `:320` → 339; rule 20 `:339` → 358; rule 21 `:349` → 368; rule 22 `:359` → 378; rule 23
`:373` → 392; rule 26 `:428` → 447; rule 27 `:436` → 455; rule 28 `:444` → 465; rule 31 `:492` →
514; rule 32 `:556` → 578; rule 35 `:609` → 632; the settings ladder `:638` → 661; the
`design-sync` defaults row `:689` → 716; the `budget.pressure` defaults row `:674` → 719.

Re-resolve all 21 pins from a grep actually run and write the lines above into the node block. Two
of them, `:674` and `:689`, sit inside a table whose rows move together, so re-resolve them by
grepping the setting name rather than by adding an offset.

`defect · missing-outcome-check (postcondition)`

F3 — Five of the seven reporting-skill pins point about seventy lines past the rule they name

> "- `skills/communicator/SKILL.md:258` (rule 5 channel line)" — ARCHITECTURE.md, `[node: communicator]`, pins

`a97f95b` and `83ebd2d` changed `skills/communicator/SKILL.md` today, and five of that node's seven
pins now sit 69 to 77 lines above the sentence they name. This file numbers its rules out of
document order, so an offset cannot be derived by reading one pin; each needs its own grep. The
channel line of rule 5 stands at 181 and its pin reads 258, which carries a sentence about a name
that needs its story told first. The clock sentence of rule 7 stands at 287 and its pin reads 356.
The outcome-leads line shape of rule 9 stands at 231 and its pin reads 301. The decision page of
rule 10 stands at 299 and its pin reads 369. The evidence walk of rule 11 stands at 352 and its pin
reads 422, inside the writing-register section that follows the rules. An agent sent to any of the
five reads a rule it was not sent to and reports on the wrong law.

Move `:258` to `:181`, `:356` to `:287`, `:301` to `:231`, `:369` to `:299` and `:422` to `:352`.
The node's two other pins need no move: `:440` names the pre-report walk and lands on its heading,
and `:105` lands inside the rules section its label names.

`defect · missing-outcome-check (postcondition)`

F4 — The pin gate cannot see this class, so a pin can be wrong for a week and still read clean

> "DRIFT (pin drift): skills/text-audit/SKILL.md:1 (frontmatter + when it fires) — label not found within ±25 lines" — output of `bash guardrails/check-pin-drift.sh`

The gate reds on a missing file and on a line past the end of file, and otherwise it searches a
51-line window for any label word of four characters or more. Both halves miss this class. The
window is wider than most of the F2 offsets, so a pin landing on the wrong rule sits inside it. The
word match then passes on a generic word: every window in the shared rulebook holds the word "rule",
so every pin labelled "rule 20" or "rule 27" reads clean wherever it points inside that file. Across
the three skills above, the gate reported zero of the 29 stale pins and exited 0.

The gate's blindness is measurable on one pin. `skills/spec-author/SKILL.md:374`, labelled
`(axes composition)`, named line 304 in `501212d` and was wrong by 70 lines for at least a week. The
gate passed it every run, because the word "axes" appeared elsewhere in its window. Today's rewrite
moved that section to line 374, so the pin is now correct by accident rather than by a read. A pin
healed by chance is the same defect as a pin broken by chance, and this gate reports neither.

Two fixes are on offer, and they compose.

- a. Narrow the window and drop generic label words. Match the label against a tight band, three
  lines each way, and skip a word that appears more than a handful of times in the pinned file.
  Cheap, and it turns "rule 20" into a real anchor rather than a word that matches everywhere.
- b. Red when a pinned file changed after the design map's own last change to that pin. The pin
  block's line for a rewritten file then blocks until a person re-resolves it, which is what today's
  three commits each needed and none of them got.

Preference: b first, since it catches the whole class the moment a skill is rewritten, and a. after
it, to catch a pin that rots without a rewrite. This finding names a file this pass does not touch,
and it belongs to that file's owner.

`defect · hard-to-monitor (observability)`

F5 — The design map states a universal about its pins that the delta falsifies

> "Every pin below comes from a grep or read actually run, never from memory." — ARCHITECTURE.md, "What 'pin' means here"

This is the sentence the quantifier re-verify lands on, and the delta puts 29 pins outside it. The
sentence reads as a standing property of the document, and it is a property of one moment: the
sweep that wrote the pins. Any rewrite of a pinned file falsifies it silently, and nothing in the
document says who restores it or when. A reader trusting the sentence follows a pin without checking
it, which is exactly the trust F1 through F3 punish.

Rewrite the sentence to name the moment and the duty: every pin is resolved by a grep or a read when
it is written, and re-resolved whenever the file it names is rewritten. Then add the re-resolve step
to the architecture step's own checklist, so the duty has a home rather than a hope.

`defect · unenforceable-promise (discharge)`

F6 — The reconciliation date in the preamble predates two rewrites of the document

> "Last reconciled with the spec: 2026-07-23." — ARCHITECTURE.md, preamble

`6167a6e` rewrote this document today, 537 lines added and 175 removed, and
`docs/prover/2026-08-05-readability-day-spec-recheck.md` records a re-read of it against
`PRODUCT_SPEC.md` on the same date. A session reading the preamble date decides the document is
nearly two weeks behind the spec and re-runs a reconciliation that already happened, or trusts the
date and skips one that is due. Neither reading is the true state.

Set the line to the date of the reconciliation the 2026-08-05 record holds, and move the line's
update into the same step that writes the record, so the two cannot disagree again. If the line
means something narrower than that record covers, say what it means in the same sentence.

`recommendation · now · hard-to-monitor (observability)`

## Acknowledged gaps

The delta declares one, and it stands correct. The commit message records that four pointers remain
named by the drift check and states why the check cannot match them: each names a whole file by its
first line, where the label's words find nothing. The document preamble carries the explaining
sentence. No new finding is filed against those four.

`acknowledged · hard-to-monitor (observability)`

## The quantifier re-verify

The mode keeps this whole-document step (SPEC INV-170). Three universals in `ARCHITECTURE.md` were
re-read against the tree as it now stands.

| Sentence | Verdict |
|---|---|
| "Every spec fact is OWNED by exactly one node." | Holds. Outside this delta, and unchanged by it. |
| "Every pin below comes from a grep or read actually run, never from memory." | Falsified. F5 carries it, F1 through F3 carry the instances. |
| "A pin whose line reads 1 names the file as a whole." | Holds, and the four gate-reported pointers are its members. |

## Findings summary

| ID | Kind | Home | Folded |
|---|---|---|---|
| F1 | defect | ARCHITECTURE.md, `[node: spec-author]` pins | open |
| F2 | defect | ARCHITECTURE.md, `[node: base-rulebook]` pins | open |
| F3 | defect | ARCHITECTURE.md, `[node: communicator]` pins | open |
| F4 | defect | `guardrails/check-pin-drift.sh` | open |
| F5 | defect | ARCHITECTURE.md, "What 'pin' means here" | open |
| F6 | recommendation | ARCHITECTURE.md, preamble | open |

Six findings, five defects and one recommendation. None of them blocks `50fffff`, which is a strict
improvement on the state before it. F4 is the one to fix first, because F1 through F3 will recur on
the next rewrite of any pinned skill for as long as the gate reads a 51-line window for a generic
word.

## Closing

**Top three to fix before the next skill rewrite.** F4, the gate that reports clean on 29 stale
pins. F2, the 21 pins into the shared rulebook, one of which lands on the wrong rule. F1, the three
pins the catch-up commit left behind in the block it repaired.

**A sentence the document should state.** Every pin is resolved by a grep or a read at the moment it
is written, and re-resolved whenever the file it names is rewritten.

**Open question for the person.** F4 offers two gate fixes, and b changes what blocks a landing:
a rewritten skill would hold its node's pins red until someone re-resolves them. That is a cost per
rewrite, and whether it is worth paying is the person's call.

**Readiness.** The delta is ready to go out as it stands. The document needs another pass over its
pin blocks, and the gate needs the reach to make that pass unnecessary next time.
