# Skill review — the base rulebook gives its paths a root and its words a definition

SKILL-REVIEW

Skills: live-spec-base.

Date: 2026-08-05
Reviewer: skill-creator (Anthropic), run by a fresh seat that did not author the change and read
the file cold.

Verdict: passes with findings. Two fresh seats ran the review, neither of which authored the change.
Between them they returned four findings against the repair's own new text, three of them blocking.
All four were folded before this record closed. Neither seat found an edit that changes what a rule
instructs.

## What changed

`skills/live-spec-base/SKILL.md` is the shared rulebook every other skill loads. A two-reader audit
read it whole and returned 95 stops. Of those, 81 survived an adversarial check. The repair closed
every finding of one kind: a rule a reader cannot follow.

Three sections were added before the rules.

**Where the paths and the codes in this file point.** Every path in the file is relative to the
live-spec repository root, named by the files it holds. `.live-spec/` is the one exception. It names a
folder in the host's own tree. The ten working skills sit at `skills/<name>/SKILL.md`.

**The code families and their home.** Eight families carry the bracket codes — `INV`, `T`, `E`, `A`,
`M`, `B`, `D`, `ACT` — and every one lives in `PRODUCT_SPEC.md`. A roadmap row number names a line of
`ROADMAP.md`, and a closed row rotates to a dated file under `docs/queue-archive/`. The `[target]` and
`[default]` marks are glossed from `ROADMAP.md`.

**The words this file uses.** Eighteen definitions, each the entry the glossary of `PRODUCT_SPEC.md`
carries. The words are the pack · a host · the seat · a worker · a tier · a brief · a wish · a queue
row · a lane · the pen · a landing · a gate · a checkpoint · the attic · a breakpoint · a door · an
agent · an agent card.

Beyond the three sections, five smaller repairs landed. One wrong cross-reference was corrected, and
one stale claim with it. Two rows were added to the package-defaults table. All-capital emphasis was
lowercased, except where a test pins it. And 63 sentences past the word cap were split.

## Why it was worth a change

Both cold readers stopped on the same fifteen passages. The heaviest were these.

The rule-of-thinking paragraph said "Rule 27 (fix the class, sweep the look-alikes)". Rule 27 is "The
orchestrator decides what it can decide". The rule with that title is rule 14, so a reader following
the pointer landed on an unrelated rule.

About a hundred bracket codes were cited and nothing on the page said what they were or which file
held them. A reader who wanted the ground of any claim could not reach it.

The same paragraph said "the repair is ROADMAP row 416". Row 416 is not in `ROADMAP.md`. It sits in
`docs/queue-archive/rotated-ROADMAP-2026-07.md` with the status "landed 2026-07-17". So a reader of
the file's top rule was told the pack's own guard was still a plan.

The pen, the host, a landing, and a breakpoint each carried rules, and none was defined. Rule 24 sent
the reader to two settings the defaults table had no rows for, `project.layers` and `project.proofs`.
Rule 29 broke the pack's own one-name lint twice.

## What the review looked at

**Does the summary line still trigger correctly?** The frontmatter description is untouched, including
its count of thirty-five rules. The body still ends at rule 35.

**Does the body still hold together?** The definitions block draws from one home, the glossary of
`PRODUCT_SPEC.md`, and says so. It names the seat's four names rather than hiding the split, which is
the honest reading of a file that uses all four.

**Could any edit be read as changing what a rule instructs?** Every repair kept its rule. Where a
repair would have moved an instruction, the text stands and the finding is recorded. One sentence was
drafted for rule 30, naming the rules that carry no machine. It was removed for exactly that reason.

**Does anything now state one rule twice?** The three new sections state facts the file did not carry
before. The code-family paragraph is the file's only statement of where a code lives.

## What the review returned

Two fresh seats read the file cold and answered the five questions put to them. Both said the
frontmatter description still triggers correctly: it is unchanged, it claims thirty-five rules, and
the body runs rule 1 through rule 35. Both said no edit changes what a rule instructs. The
rule-27-to-14 correction and the row-416 correction are citation fixes. The two new table rows are
the table catching up to rule 24, which already required a project to declare both.

Four findings came back against the repair's own new text. Every one was folded before this record
closed.

**Blocking. The paths section named the wrong tree for most of the file's paths.** It said every path
is relative to the live-spec repository root. The file's own text says otherwise in four places: rule
10 calls the attic the host's, the `spec.file` row calls `PRODUCT_SPEC.md` the host's, rule 16 puts
`prototype/` in the host tree, and rule 9's journal and resume file are the host's living documents.
A host session reading this base would have been told its own journal lives in the pack's repository.
The section now names two classes. The pack's machinery — `guardrails/`, `scripts/`, `tests/`,
`templates/`, `hooks/`, `adopt/`, `skills/` — sits in the live-spec repository. A host's own documents
and workspace sit at the host root. The live-spec repository is a host of its own, so on that machine
the two trees are one directory.

**Blocking. "Eight families carry those codes" undercounted.** `PRODUCT_SPEC.md` carries `[C-1]` on
its composition-axis criteria and `[S-0]` on its promised-tag criteria, and its own preamble names
eleven letters. The sentence now points at that preamble, which names every letter and what it stands
for, so the count cannot drift again.

**Blocking. The glossary block claimed a provenance it did not have.** It said every definition is the
entry the glossary of `PRODUCT_SPEC.md` carries. A queue row has no entry in that glossary; its home
is `docs/roadmap-format.md`. Several other entries carried sentences the spec's entry does not. The
block now says each line gives a short read of its entry and the entry itself is the authority, and
the queue-row line names its real home.

**Non-blocking. One fact gained a second home.** The new entry for **an agent** restated rule 31's own
opening almost word for word, the same six-item list in the same order, against rule 4 and against the
file's own opening sentence about drift. The entry is now a pointer to rule 31.

Three smaller corrections came with them. Rule 7's "board reason" had been reworded to "the status
report", which renamed a surface `PRODUCT_SPEC.md` and `skills/build-pipeline/SKILL.md` both call the
board; it now reads "the departures board, the status-report view". A sentence added to rule 7 read as
a new duty; it is now a plain statement of fact about the script's header. And "the repair shipped the
same day as roadmap row 416" read as two events; it now says the repair shipped that day as row 416.

Neither cold reader caught any of these, because none had seen the new sections before. That is the
shape rule 33 names: an authoring seat is blind to what it just wrote.

## Findings this repair left standing

Fourteen findings were left standing on purpose, each with its reason. They are listed in
`~/context-slimdown/reports/live-spec-base-repair.md`. Six of them need a ruling only the pack can make:

- rule 2 forbids handles that rules 5 and 32 then use;
- rule 30 claims an enforcement that rules 32, 33, and 35 take back;
- rule 33's release-gate requirement is hedged;
- rule 14 and rule 26 each name two homes for one fact;
- no setting key exists for the full-audit count;
- the person answers to four names, two of them pinned by tests.

## Checks run

`python3 scripts/rule-census.py skills/live-spec-base/SKILL.md` — 226 findings before the repair and
91 after. Before: 140 sentences past the cap, longest 97 words, 86 style, 0 register. After: 77 past
the cap, longest 49 words, 14 style, 0 register.

`python3 scripts/preshow-register-lint.py skills/live-spec-base/SKILL.md` — exit 0.

`python3 guardrails/check-one-name.py skills/live-spec-base/SKILL.md` — exit 1 before, exit 0 after.

`python3 guardrails/check-vocabulary.py`, `check-weak-words.py`, and `check-requirement-shape.py` each
exit 1 on this file and name their input set as empty. Those three read a spec section alone, and a
skill body carries neither a glossary nor acceptance criteria. The refusal is their designed answer.
It is recorded and the class stays with the cold readers. No script and no document was edited to make
one of them pass.

`sh guardrails/check-skill-loadability.sh` — eleven skills load, named, versioned, negative-scoped.

`python3 -m pytest tests/test_config_health.py tests/test_traceability.py -q` — 208 passed, none
failed. That run includes the byte-parity check: the repository copy and the installed copy of this
skill hold the same 66,167 bytes, confirmed again with `cmp`.

Every one of the thirty-two test files that read this skill passes.
