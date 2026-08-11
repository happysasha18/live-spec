# Prover record — the architecture's repointed pins, 2026-08-11

Re-check of `ARCHITECTURE.md` against the tree, covering the two commits that moved the file since
the last committed prover record `2121b91`. `3915e95` is the R6 landing, "the architecture-pointer
gate proves a pin against its own line, and eight rotten pointers come home".
`d7d73e1` is the R1 landing, "every path a skill names says which tree it lives in".

The push gate requires a committed prover record at least as new as the last `ARCHITECTURE.md`
change (SPEC M-6, INV-116, read by `guardrails/check-prover-record.sh`). The gate reads red today,
naming `d7d73e1` as the last architecture change and `2121b91` as the newest record commit. This
pass answers that demand.

Verdict: all seventeen pin lines the two commits touched carry what their labels name. A sweep of
the sixty-six line pins in the whole document found four stale pins in
`skills/build-pipeline/SKILL.md`. Each of the four sat nine lines above the thing its label names.
A separate hand repointed the four while this pass was open, and this record re-verifies the
repair. This record and that repoint land in one commit.

## What the two commits changed

`git diff 2121b91..HEAD -- ARCHITECTURE.md` returns seventeen changed pin lines across six node
sections. Fourteen changed a line number and three changed only the label's wording.

`3915e95` touches nine pins. Six moved onto a new line and three kept their line with a reworded
label. The commit message names eight rotten pointers, so the count in the message and the count in
the diff differ by one. Its line moves were
`skills/product-prover/SKILL.md:723` to `712`, `skills/build-pipeline/SKILL.md:217` to `226`,
`skills/build-pipeline/SKILL.md:527` to `536`, `skills/communicator/SKILL.md:105` to `35`,
`install.sh:2` to `1`, and `skills/build-pipeline/SKILL.md:489` to `498`. The three label rewordings
dropped a dash frame from the communicator's rule 9, rule 7 and rule 5 pins.

`d7d73e1` grew eight skill pages during the install repair and followed nine pins onto their new
lines. Six of them are the spec-author pins, which each moved by seven lines. The other three are
the product-prover pins for the review modes, the unwritten-seam hunt and the restructure-merge
gate.

## Each changed pin, checked against its own line

Every pin below was opened at its named line and read with two lines of context on each side. The
column on the right names the line that carries the label.

| Pin | Label | Carried at |
| --- | --- | --- |
| `skills/spec-author/SKILL.md:228` | spine | 228, the heading "The spine" |
| `skills/spec-author/SKILL.md:254` | [target] tag tripwire | 254, the tripwire paragraph's opening |
| `skills/spec-author/SKILL.md:381` | axes composition | 381, the composition-axes rule (INV-244) |
| `skills/spec-author/SKILL.md:340` | fences | 340, the heading "The regression fences" |
| `skills/spec-author/SKILL.md:356` | facet sweep | 356, the heading "The facet sweep" |
| `skills/spec-author/SKILL.md:161` | enumeration threshold, INV-215 | 161, the rule's own bullet |
| `skills/product-prover/SKILL.md:282` | review modes | 283, the heading "Review modes" |
| `skills/product-prover/SKILL.md:717` | unwritten-seam hunt, INV-72 | 718, the unwritten-seams bullet |
| `skills/product-prover/SKILL.md:364` | restructure-merge gate, INV-114 | 365, the gate's own paragraph |
| `skills/build-pipeline/SKILL.md:226` | the work-kind table | 226, the heading "The work-kind table" |
| `skills/build-pipeline/SKILL.md:536` | gates | 536, the heading "Gates worth remembering" |
| `skills/build-pipeline/SKILL.md:498` | the design-sync line in step 9 | 498, the design-sync sentence in step 9 |
| `skills/communicator/SKILL.md:35` | the rules | 35, the heading "The twenty-two rules" |
| `skills/communicator/SKILL.md:231` | rule 9's outcome-leads line shape | 231, inside rule 9, anchored at 222 |
| `skills/communicator/SKILL.md:286` | rule 7's chat-arm clock sentence | 286, inside rule 7, anchored at 281 |
| `skills/communicator/SKILL.md:181` | rule 5's channel line | 181, inside rule 5, anchored at 175 |
| `install.sh:1` | E-21, the installer itself | line 1, the shebang of the installer |

Three of the seventeen land one line off their heading and stay inside the gate's tolerance of two
lines. The three communicator rule numbers were confirmed against the nearest `(rule N)` anchor above each
pinned line. Every one of them matches the rule its line belongs to.

## The unchanged pins, swept whole

The brief asked for three unchanged pins. A first sample of five raised two questions, so the sweep
widened to every line pin in the document. All sixty-six were opened with their windows and read.

Sixty-two carried their labels. Four failed, and the next section holds them.

## Finding — four pins in the pipeline skill sat nine lines early

`skills/build-pipeline/SKILL.md` grew by nine lines on 2026-08-06, in commit `fee77fb`. That commit
inserted the section "Setting a project up on the pack" after old line 216. Seven pins pointed below
the insertion. `3915e95` moved three of them by nine lines. Four kept their old numbers.

| Label | Old line | What that window held | Real home |
| --- | --- | --- | --- |
| steps | 232 | the contract sentence before the work-kind table | 241, the heading "The steps" |
| re-carve paragraph, INV-113 | 336 | the node-fitness test, INV-122 | 345 to 351, the re-carving paragraph |
| trains, one pen | 554 | the bookkeeping bullet, INV-61 | 563, the bullet "Trains, one pen" |
| the graph picks the lane set at queue-take | 571 | the pen-stage paragraph | 580, the bullet on picking lanes by graph |

Each of the four sat nine lines above its target, which is the exact size of the `fee77fb`
insertion.

The pins for INV-113 and INV-122 deserve a note. `ARCHITECTURE.md:163` promises the reader the
redesign-owes-rework law of INV-113. Line 336 delivered the birth test for a carved node, which is
INV-122. A reader following that pin arrived at a different law with a similar vocabulary.

## The repair, and its re-verification

A separate hand repointed all four in `ARCHITECTURE.md` while this pass was open. The moves are 232
to 241, 336 to 347, 554 to 563, and 571 to 580. Each new line was then opened here and read with two
lines of context on each side.

| Pin | Label | Carried at |
| --- | --- | --- |
| `skills/build-pipeline/SKILL.md:241` | steps | 241, the heading "The steps" |
| `skills/build-pipeline/SKILL.md:347` | re-carve paragraph, INV-113 | 347, inside the re-carving paragraph, with INV-113 named at 349 |
| `skills/build-pipeline/SKILL.md:563` | trains, one pen | 563, the bullet "Trains, one pen" (T-18, INV-39) |
| `skills/build-pipeline/SKILL.md:580` | the graph picks the lane set at queue-take | 580, "Lanes are picked by a graph" (INV-49), naming queue-take in its own sentence |

Pin 347 now sits in the re-carving paragraph that opens at 345. Its sentence carries the redesign
clause, and INV-113 stands two lines below it, inside the gate's tolerance. The pin therefore
delivers the law its label promises.

`bash guardrails/check-pin-drift.sh` was re-run over the repaired document. It reports the same 210
pins checked and the same 66 line pins proved, with no failure line.

The repair moves four line numbers and touches no label. It changes nothing in
`skills/build-pipeline/SKILL.md`, so no other pin in the document shifts.

## Why the drift gate read green over these four

The four stale pins crossed the drift gate green. `bash guardrails/check-pin-drift.sh` printed this
over the document as the two commits left it, and prints the same line over the repaired document:

```
OK (pin drift): 210 pin(s) checked — 66 line pin(s) proved against their own line (tolerance ±2 lines), 138 file-level :1 pin(s) proved against the whole file, 6 unlabelled pin(s) proved by the file's existence alone: templates/ROADMAP.template.md:1, PRODUCT_SPEC.md:1, JOURNAL.md:1, VERSION:1, guardrails/install.sh:1, tests/test_guardrails.py:1.
```

The script proves a pin when one naming word of its label, four characters or longer, stands
anywhere in the five-line window. Each of the four stale pins won on a topic word that recurs
through its whole section. Pin 232 matched the word "step" inside a sentence about door-granted
steps. Pin 336 matched "carve" inside "carved node". Pin 554 matched "landing", and pin 571 matched
"lane".

This is the same class the gate was rebuilt to catch in `3915e95`, met one layer deeper. A rulebook
repeats its section's vocabulary in every paragraph of that section. A topic word inside the window
is therefore weak evidence that the window is the right one. A stronger rule would ask for the
label's rarest word. It could also ask that the heading above the pinned line match the pin's label.

Recording this as an observation for whoever owns the gate. No change is proposed here.

## Verdict

The seventeen pin lines that `3915e95` and `d7d73e1` changed all verify against the tree. Both
commits did the work their messages claim, and the label rewordings match the rules they name.

This pass found four further pins in `skills/build-pipeline/SKILL.md` pointing nine lines above
their targets. They predate both commits, and `3915e95` swept three of their siblings while leaving
these four. A separate hand repointed all four, and each new line was re-read here and carries what
its label names.

Every one of the sixty-six line pins in `ARCHITECTURE.md` now stands on the thing it names. The
drift gate reports 210 pins checked with no failure. The document matches the tree.

Nothing here blocks the commit or the push. One observation stands open, addressed to whoever owns
the drift gate's matching rule.

## Reach

Read whole: the diff `git diff 2121b91..HEAD -- ARCHITECTURE.md`, the node sections it touched, and
`guardrails/check-pin-drift.sh` including its matching doctrine.

Read in part, each at its pinned lines with a five-line window:

- `skills/spec-author/SKILL.md`, six pins.
- `skills/product-prover/SKILL.md`, three pins.
- `skills/communicator/SKILL.md`, seven pins, plus its `(rule N)` anchors.
- `skills/build-pipeline/SKILL.md`, ten pins.
- `skills/live-spec-base/SKILL.md`, twenty-one pins.
- `install.sh` at line 1, and the remaining pinned files at their own windows.

Commands run:

- `git diff 2121b91..HEAD -- ARCHITECTURE.md`.
- `git show 3915e95 -- ARCHITECTURE.md`, and the same for `d7d73e1`.
- `git log --numstat -- skills/build-pipeline/SKILL.md`.
- `git show fee77fb -- skills/build-pipeline/SKILL.md`.
- `python3 guardrails/archformat.py --pins ARCHITECTURE.md`, over every line pin.
- `bash guardrails/check-pin-drift.sh`, once before the repair and once after it.
- `bash guardrails/check-prover-record.sh`.

Not verified: the 138 file-level pins. The drift gate proves each against a whole file, and this
pass opened them only where a line pin shared the file. The pin at `~/.claude/CLAUDE.md` also stands
unverified, since it lives outside this repository.

Files written by this pass: this record alone. The four repointed lines in `ARCHITECTURE.md` were
written by a separate hand and are re-verified here. The two files land in one commit.
