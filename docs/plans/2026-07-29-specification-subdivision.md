# Plan — divide the specification into files one reader holds

## Who reads this document

The session that carries out the division. It also serves the person deciding whether to start.

## The state today

`PRODUCT_SPEC.md` is one file of 7777 lines and 661342 bytes (`wc -l -c PRODUCT_SPEC.md`).

Its body holds 303 requirements (`grep -c '^## Requirement ' PRODUCT_SPEC.md`) and 1609 acceptance
criteria (`python3 guardrails/check-size-ratchet.py PRODUCT_SPEC.md`, green line).

The file has four parts. A preamble of 12 lines and 2797 bytes. A glossary of 253 lines and 41947
bytes. A body of 7120 lines and 590700 bytes. A generated code-to-location table of 392 lines and
25894 bytes. All four counts come from the segment command in the last section of this plan.

The average requirement runs 23.5 lines and 1950 bytes. The largest runs 64 lines. Both come from the
grouping command in the last section.

Twenty-eight requirement headings carry a feature tag
(`grep '^## Requirement' PRODUCT_SPEC.md | grep -c 'feature: F-'`). Those tags name 16 distinct
features (`grep -o 'feature: F-[a-z][a-z-]*' PRODUCT_SPEC.md | sort -u | wc -l`).

## The idea in one paragraph

The body already runs in subject order. A reader walking it meets intake first, then the showing rules,
then the doors. The review passes follow, and the format family closes the file. The division therefore
cuts the body at boundaries that already exist. It renumbers nothing and moves almost nothing. Every
requirement number, every bracket anchor and every heading stays exactly as it stands.

---

# Part 1 — the grouping

## How the groups were derived

The 28 feature-tagged requirements were taken first. Each tag names a person-facing scenario, so each
tag seeds a subject. Fourteen of the sixteen feature codes already sit as a contiguous run of
requirements, and each such run became the core of one group.

The untagged requirements were then read by title and assigned to the nearest subject on either side.
That produced 26 subject clusters covering all 303 requirements. Every cluster is a contiguous run of
requirement numbers, with one exception named below.

The cap of Part 2 was then applied. Sixteen clusters ran past it and split into two parts each. Ten
clusters fit as one file. The result is 42 group files.

## The one requirement out of document order

Requirement 303 sits in the file between Requirement 127 and Requirement 128. Its subject is a
session's record read at both ends, which belongs with the checkpoint and resume rules around it. It
stays where it sits, in group G17, and the division carries it there. No other requirement moves.

## The 42 groups

Line, byte and criteria counts come from the grouping command in the last section of this plan. Bytes
count the requirement bodies of the group, with no file header included.

| Group | Name | Requirements | Reqs | Lines | Bytes | Criteria | Feature tags |
|---|---|---|---|---|---|---|---|
| G01 | The wish arrives and takes its row | 1–8 | 8 | 166 | 13262 | 35 | F-wish |
| G02 | Sizing a wish and closing it whole | 9–16 | 8 | 173 | 13233 | 36 | — |
| G03 | Showing the work to the person | 17–26 | 10 | 218 | 17597 | 47 | — |
| G04 | The away stretch and the person's word | 27–36 | 10 | 174 | 12141 | 31 | — |
| G05 | Priority, the doors, and the route in | 37–45 | 9 | 197 | 15797 | 37 | — |
| G06 | The work-kind and the steps it scales | 46–53 | 8 | 157 | 13330 | 32 | — |
| G07 | Cross-cutting laws and the fit interrogation | 54–59 | 6 | 122 | 10072 | 21 | — |
| G08 | The prover and the design review | 60–70 | 11 | 225 | 19456 | 42 | — |
| G09 | Calls the walk takes on its own | 71–78 | 8 | 155 | 12092 | 27 | — |
| G10 | Sessions, lanes, and the single pen | 79–86 | 8 | 174 | 13942 | 33 | — |
| G11 | The branch road and its machines | 87–91 | 5 | 121 | 10037 | 22 | — |
| G12 | Deferral, the far tier, and end-states | 92–97 | 6 | 113 | 8728 | 17 | — |
| G13 | The prototype fence | 98–104 | 7 | 140 | 9723 | 24 | F-prototype |
| G14 | The test method | 105–112 | 8 | 138 | 10976 | 23 | — |
| G15 | Suite honesty and the browser harness | 113–117 | 5 | 112 | 10045 | 22 | — |
| G16 | The architecture document | 118–124 | 7 | 160 | 13106 | 27 | — |
| G17 | Breakpoints, checkpoints, and session memory | 125–129, 303 | 6 | 152 | 12754 | 55 | — |
| G18 | The milestone gate and the periodic audits | 130–137 | 8 | 183 | 14784 | 30 | — |
| G19 | The push and the remote gate | 138–142 | 5 | 91 | 7048 | 16 | — |
| G20 | Publishing and the shipped tree's language | 143–151 | 9 | 175 | 13556 | 29 | F-publish |
| G21 | Feedback | 152–158 | 7 | 167 | 14026 | 34 | F-feedback |
| G22 | The feature map, bugs, and the problem ledger | 159–167 | 9 | 226 | 18689 | 51 | F-feature-map, F-bug, F-problem-ledger |
| G23 | Founding a project | 168–176 | 9 | 238 | 19225 | 61 | F-bootstrap |
| G24 | Adoption and catch-up | 177–182 | 6 | 158 | 13917 | 49 | F-adoption, F-catchup |
| G25 | The catch-up vehicles and the settings card | 183–186 | 4 | 114 | 9385 | 32 | F-onboarding |
| G26 | Engine and instance, and how the skills arrive | 187–192 | 6 | 192 | 17664 | 57 | F-pair |
| G27 | Agents: roster, contract, and message | 193–197 | 5 | 243 | 21034 | 73 | F-roster, F-contract, F-agent-ask, F-agent-birth |
| G28 | The settings ladder and the human's contract | 198–205 | 8 | 170 | 12906 | 36 | — |
| G29 | Delegation and the worker contract | 206–212 | 7 | 162 | 14837 | 37 | — |
| G30 | Second eyes, briefs, and the economy ladder | 213–220 | 8 | 159 | 14879 | 33 | — |
| G31 | Convergence, coverage, and the push gate's reach | 221–227 | 7 | 151 | 11559 | 31 | — |
| G32 | The nets: judges, arms, and cleanups | 228–235 | 8 | 212 | 19062 | 50 | — |
| G33 | Touchpoints, the board, and the records | 236–243 | 8 | 166 | 13283 | 34 | — |
| G34 | Growth bounds and the guards over the guards | 244–250 | 7 | 158 | 12585 | 34 | — |
| G35 | The inbox and the parallel-safe repository | 251–257 | 7 | 175 | 14328 | 42 | — |
| G36 | Composition axes and the lenses | 258–263 | 6 | 158 | 15003 | 36 | — |
| G37 | Enumeration, axes, and what an axis ships | 264–266 | 3 | 106 | 11494 | 29 | — |
| G38 | The pack's homes, copies, and versions | 267–276 | 10 | 222 | 19005 | 47 | — |
| G39 | The spec's own format | 277–282 | 6 | 198 | 15694 | 59 | — |
| G40 | The other format-family members | 283–291 | 9 | 209 | 17050 | 43 | — |
| G41 | Hooks, chat laws, and rendered pages | 292–297 | 6 | 187 | 16319 | 58 | — |
| G42 | The deployed kind and the project's own texts | 298–302 | 5 | 203 | 17078 | 77 | — |

The 42 groups sum to 303 requirements, 7120 lines, 590700 bytes and 1609 criteria. Those four totals
equal the body totals stated at the top, so the assignment covers every requirement once.

## Where the group files live

Each group becomes one file under a new directory `PRODUCT_SPEC/`, named by its number and a short
slug: `PRODUCT_SPEC/01-the-wish-and-its-row.md` through
`PRODUCT_SPEC/42-the-deployed-kind-and-our-own-texts.md`.

`PRODUCT_SPEC.md` stays as the front file. It keeps the preamble, the glossary, the generated
code-to-location table, and a new list of the 42 parts with one line of subject each.

The directory name repeats the artifact's own name, so the one-name-per-thing law holds. A reader
looking for the spec finds `PRODUCT_SPEC.md`, and the parts sit under a directory of the same name.

---

# Part 2 — the size rule

## The two written sources, and how they disagree

The first source is `docs/research/2026-07-05-skill-patterns.md` line 42. It states hard size guidance
of a SKILL.md body under 500 lines, with a split into reference files on approach.

The second source is `skills/text-audit/SKILL.md` line 86. It states that ten requirements at a time is
the working size, and that ten requirements run to about 250 lines. A fresh reader holds that much.

The two numbers differ by a factor of two. They also differ in reader and in material. The 500-line
number governs a skill body a model loads. The 250-line number governs a run of spec requirements a
person reads.

## The recommendation

**The cap is 250 lines of requirement bodies per group file.**

The reason is that the two sources answer two different questions, and only one of them answers this
one. The material being divided is spec requirements. The reader whose limit matters is a fresh person
reading them. Those are exactly the material and the reader the 250-line sentence names.

A second fact supports the same choice. The measured average requirement runs 23.5 lines. Ten average
requirements therefore run 235 lines. The text-audit sentence and the live document agree to within
one requirement, so the number is calibrated against this very spec.

The cap covers the requirement bodies alone. A group file also carries a title line and one short
paragraph naming its subject. That header sits outside the count, since the text-audit sentence counts
requirements.

## Which subject clusters exceed the cap

Sixteen of the 26 subject clusters run past the cap or sit exactly on it. Each splits into two parts,
cut at the strongest internal subject boundary. Ten clusters fit as one file.

| Subject cluster | Requirements | Lines | Verdict | Parts |
|---|---|---|---|---|
| Intake and the wish's row | 1–16 | 339 | over | G01, G02 |
| Showing the work | 17–36 | 392 | over | G03, G04 |
| The doors and the route in | 37–53 | 354 | over | G05, G06 |
| Laws, fit, and the review passes | 54–70 | 347 | over | G07, G08 |
| Calls the walk takes on its own | 71–78 | 155 | fits | G09 |
| Parallel work | 79–91 | 295 | over | G10, G11 |
| Deferral and end-states | 92–97 | 113 | fits | G12 |
| The prototype fence | 98–104 | 140 | fits | G13 |
| Tests and suite honesty | 105–117 | 250 | at the cap | G14, G15 |
| The architecture document | 118–124 | 160 | fits | G16 |
| Session rhythm and the milestone | 125–137, 303 | 335 | over | G17, G18 |
| Push, publish, and the shipped tree | 138–151 | 266 | over | G19, G20 |
| Feedback | 152–158 | 167 | fits | G21 |
| The feature map, bugs, the ledger | 159–167 | 226 | fits | G22 |
| Founding | 168–176 | 238 | fits | G23 |
| Adoption, catch-up, onboarding | 177–186 | 272 | over | G24, G25 |
| The pair and the agents | 187–197 | 435 | over | G26, G27 |
| The settings ladder | 198–205 | 170 | fits | G28 |
| Delegation and the budget | 206–220 | 321 | over | G29, G30 |
| Gates, nets, and cleanups | 221–235 | 363 | over | G31, G32 |
| Records, growth bounds, the guards | 236–250 | 324 | over | G33, G34 |
| The inbox and the shared repository | 251–257 | 175 | fits | G35 |
| Composition axes and the lenses | 258–266 | 264 | over | G36, G37 |
| The pack's homes and versions | 267–276 | 222 | fits | G38 |
| The format family | 277–291 | 407 | over | G39, G40 |
| Hooks, chat laws, our own texts | 292–302 | 390 | over | G41, G42 |

The cluster at 105–117 measures exactly 250 lines. A file sitting exactly on the cap leaves no room for
its own header, and a single added criterion would break it. It splits for that reason.

## The tightest groups after the split

Two group files sit within 15 lines of the cap. G27 measures 243 lines and G23 measures 238 lines.
Both are single-subject files with no obvious internal cut. Both are recorded here as the first places
a future requirement will force a further split.

---

# Part 3 — the mapping

## What each mapping is built from

An architecture node lists the spec anchors it owns in its `owns` field. The anchor list is parsed by
`guardrails/archformat.py`, the one node reader every consumer uses.

A matrix row carries its parent spec anchor as the last bracket group of its fact sentence. The
anchors are parsed by `row_anchors()` in `tests/test_traceability.py`.

An anchor is turned into requirement numbers by the generated code-to-location table,
`PRODUCT_SPEC.index.md`. A run of `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md
PRODUCT_SPEC.index.md` confirms 386 table rows agreeing body-to-table.

All counts in this part come from the seam command in the last section of this plan.

## The finding that governs the whole part

**An anchor is already spread across the document.** The table holds 393 codes. That count expands the
one range row `T-1..T-7` and places the two gap-line codes `D-1` and `D-6`. Of the 393, some 237 codes
have carrying criteria in more than one group. The other 156 sit in exactly one group.

The three widest are `INV-4` with criteria in 17 groups, `INV-159` with criteria in 15 groups, and
`INV-11` with criteria in 14 groups.

This spread exists in the single file today. `docs/measure/2026-07-29-specification-size.md` measures
the same fact from the other side: fifteen requirements restate the forward-binding rule while citing
`INV-159`. The division neither creates the spread nor cures it. It makes the spread visible, because
a code's location line will now name several files.

## Architecture nodes against the groups

There are 22 architecture nodes. **Nineteen of them own anchors whose criteria reach more than one
group.** Three land in exactly one group.

| Node | Owned anchors | Groups reached |
|---|---|---|
| build-pipeline | 72 | 40 |
| base-rulebook | 52 | 38 |
| guardrails [target] | 89 | 32 |
| communicator | 28 | 26 |
| spec-author | 26 | 24 |
| attach | 33 | 23 |
| parallel-lanes | 12 | 16 |
| product-prover | 8 | 14 |
| templates | 7 | 14 |
| inbox | 12 | 14 |
| package-docs | 9 | 10 |
| test-author | 13 | 10 |
| host-contract | 4 | 8 |
| design-reviewer | 6 | 8 |
| publish | 6 | 6 |
| snapshot [target] | 2 | 3 |
| design-sync | 1 | 3 |
| feedback-intake | 3 | 3 |
| skill-evals | 1 | 2 |
| feedback-collector | 4 | 1 |
| onboarding-card | 2 | 1 |
| text-audit | 3 | 1 |

**The stated answer.** A node's `owns` field names anchors, and it names no file today. It gains no
file column and needs no edit. Node ownership and file placement are two separate facts, and only the
second one changes. The suite holds one bond here: every spec anchor is owned by exactly one node. That
bond ties an anchor to a node, so it survives the division untouched.

**What must change is one thing.** The code-to-location table gains a file column. A location becomes
a part file plus a requirement plus a criterion, where today it is a requirement plus a criterion. Every
consumer that walks from an anchor to its text goes through that table, so one change reaches them all.

**The three nodes that already sit in one group** are feedback-collector in G21, onboarding-card in G25,
and text-audit in G39. They are the shape a node takes when its facts have one home, and they show the
target the duplication work is aiming at.

## Matrix rows against the groups

The matrix body holds 489 rows across 22 node blocks. **Three hundred and twenty-five rows cite
anchors whose criteria sit in more than one group.** One hundred and sixty-four rows land in exactly
one group. No row lands in none.

Of the 325 spanning rows, **297 cite exactly one anchor**. Those rows span groups for one reason
alone: the single anchor they cite is itself spread. The remaining 28 cite several anchors.

The span histogram runs as follows, with the group count first and the row count second.

| Groups a row spans | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 14 | 15 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Rows | 90 | 68 | 67 | 25 | 16 | 15 | 18 | 14 | 7 | 1 | 1 | 1 | 1 | 1 |

The five widest rows are these.

- Seventeen groups, reached from the single anchor `INV-4` (row M-024).
- Fifteen groups, reached from the single anchor `INV-159` (row M-306).
- Fourteen groups, reached from the single anchor `INV-11` (row M-005).
- Twelve groups, reached from three anchors (row M-384).
- Eleven groups, reached from the single anchor `INV-31` (row M-116).

**The stated answer.** No matrix row changes. A row's parent fact is its anchor, and the anchor is
unchanged. The row's walk to the spec text is resolved through the code-to-location table, which is the
one place gaining a file column. The 297 single-anchor spanners need nothing at all.

**The 28 multi-anchor spanners take one added duty.** Each cites several parent facts. After the
division, a reader following such a row may open several files. The matrix format already permits a
row to cite several codes, so the format needs no change. The reach line of the traceability suite
gains the count of part files a row's anchors resolve into, so a row growing wider is visible.

## Two anchor shapes the resolver must handle

The generated table carries `T-1..T-7` as a single row covering all seven codes. Its location is R6.1
through R6.5, all in group G01. The resolver expands the range before placing it.

`D-1` and `D-6` are owned by nodes and cited by matrix rows M-055 and M-202, and no criterion carries
them. Both appear only inside a `[GAP: ...]` line, which the format excludes from anchors. `D-1` sits
in Requirement 177 and `D-6` in Requirement 187, so they resolve to G24 and G26 by the gap line's own
position. This is a pre-existing hole in the table, and the division does not close it.

## Per-group counts of nodes and rows

| Group | Nodes touching it | Matrix rows resolving into it |
|---|---|---|
| G01 | 9 | 39 |
| G02 | 5 | 27 |
| G03 | 4 | 34 |
| G04 | 4 | 25 |
| G05 | 5 | 26 |
| G06 | 6 | 45 |
| G07 | 7 | 43 |
| G08 | 7 | 46 |
| G09 | 9 | 37 |
| G10 | 6 | 32 |
| G11 | 7 | 32 |
| G12 | 7 | 28 |
| G13 | 5 | 17 |
| G14 | 3 | 12 |
| G15 | 8 | 29 |
| G16 | 6 | 24 |
| G17 | 6 | 27 |
| G18 | 12 | 50 |
| G19 | 8 | 25 |
| G20 | 7 | 20 |
| G21 | 8 | 27 |
| G22 | 10 | 51 |
| G23 | 9 | 51 |
| G24 | 6 | 34 |
| G25 | 7 | 29 |
| G26 | 13 | 85 |
| G27 | 8 | 83 |
| G28 | 9 | 31 |
| G29 | 9 | 57 |
| G30 | 10 | 57 |
| G31 | 5 | 32 |
| G32 | 7 | 53 |
| G33 | 7 | 32 |
| G34 | 8 | 40 |
| G35 | 11 | 55 |
| G36 | 6 | 41 |
| G37 | 6 | 26 |
| G38 | 11 | 49 |
| G39 | 3 | 17 |
| G40 | 2 | 14 |
| G41 | 4 | 30 |
| G42 | 6 | 39 |

The node column names how many of the 22 nodes own an anchor with a criterion in that group. The row
column names how many of the 489 matrix rows resolve into it. A row resolving into several groups is
counted in each of them, so the row column sums past 489.

---

# Part 4 — what breaks

## The single chokepoint

The repository holds 195 test files, counted by `ls tests/test_*.py | wc -l`. One hundred and
thirty-three of them name `PRODUCT_SPEC.md` as a path. That count comes from the test-reader command in
the last section.

One hundred and fifteen of the 133 go through four conftest helpers. The helpers are `read`,
`read_flat`, `read_all` and `read_all_flat`, and together they carry 389 call sites. The call-site count
comes from the second test-reader command in the last section.

Eighteen build the path themselves. They are `test_answer_first_arm`, `test_config_health`,
`test_criterion_readability`, `test_founding_set_version`, `test_guardrails`, `test_hedge_arm`,
`test_index_generated`, `test_no_history`, `test_one_name_check`, `test_preshow_register_lint`,
`test_prose_gate`, `test_register_judge`, `test_requirement_shape`, `test_size_ratchet`,
`test_update_watcher`, `test_version_is_one_fact`, `test_vocabulary_check` and `test_weak_words`.

The 389 call sites are the reason the first step of Part 6 is an assembly reader. One helper change in
`tests/conftest.py` reaches 115 test files. Eighteen files are then repaired one at a time.

## The gates, scripts and hooks that name the path

Twenty executable files name `PRODUCT_SPEC.md`.

| File | What it does today | What it must do after |
|---|---|---|
| `guardrails/check-freeze.sh` | Its `DOCS` variable holds three document names, and the baseline file is `.spec-freeze/PRODUCT_SPEC.md.json`. | Its `DOCS` variable expands to the front file plus the 42 parts. The baseline becomes 43 files under `.spec-freeze/`. |
| `scripts/spec-freeze.py` | Freezes and verifies the anchor-occurrence map, marker lines, numbers and paths of each named document. | Takes a directory or a glob, and its verify output names the part a drift sits in. |
| `guardrails/check-doc-bound.py` | Compares each growable document against its ceiling in `guardrails/doc-bounds.json`. A green run today reads four docs. | Compares each part against a per-part ceiling, and keeps one ceiling over the assembled set. |
| `guardrails/doc-bounds.json` | Holds `PRODUCT_SPEC.md` with `max_bytes` 840000 and its recorded reason. | Holds one entry per part plus one for the set, each with a reason stated at the division. |
| `guardrails/check-size-ratchet.py` | Governs `PRODUCT_SPEC.md` alone. Its green line today reads 189.3 bytes per criterion against the recorded bound 207.2. | Runs over the assembled set, so the one number stays one number. A per-part ratchet would let one part rise while another falls. |
| `guardrails/spec-ratchet.json` | Its `governs` field holds `PRODUCT_SPEC.md`. | Its `governs` field holds the assembled set, named as the front file plus its parts. |
| `guardrails/check-index-generated.py` | Compares the committed `PRODUCT_SPEC.index.md` against a fresh build. Today 386 codes agree body-to-table. | Builds from the assembled set, and the table gains its file column. |
| `scripts/build-index.py` | Emits the code-to-location table from one document's body criteria. | Emits it from the 42 parts, each location carrying its part file. |
| `PRODUCT_SPEC.index.md` and the spec's `## Reference` | 392 lines and 25894 bytes of code-to-location rows, output only. | Same table with a file column. Both copies stay generated, and both stay at the front file. |
| `guardrails/check-index-prose.py` | Its `SPEC_PATH` default is `PRODUCT_SPEC.md`. Retired from the push gate, still shipped for its fixture proofs. | Its default becomes the assembled set. Retired status is unchanged. |
| `guardrails/check-description-field.py` | Its `SPEC_PATH` default is `PRODUCT_SPEC.md`. Retired in `guardrails/description-field.json`. | Its default becomes the assembled set. Retired status is unchanged. |
| `guardrails/check-doc-rotation.py` | Names `PRODUCT_SPEC.md` among the four growable documents. | Names each part, and the manifest line for a rotated part sits at the front file. |
| `scripts/rotate-doc.py` | Same four-document list. | Same change as the rotation gate. |
| `guardrails/check-prover-record.sh` | Runs `git log -1 --format=%H -- PRODUCT_SPEC.md` for the freshness check. | Runs the same log over the front file and every part, and takes the newest commit of the set. |
| `guardrails/check-push-reach.sh` | Its prose class is an explicit narrow list naming `PRODUCT_SPEC.md`. | Its list gains the parts directory. |
| `guardrails/pre-push` | Calls `check-index-generated.py` with the two explicit paths. | Calls it with the assembled set. |
| `guardrails/check-requirement-shape.py` | Takes the document on the command line and holds no default. | No code change. Its caller passes each part. |
| `scripts/check-shipped-language.py` | Its `STRICT_PROJECT_FILES` tuple holds `PRODUCT_SPEC.md` and `ARCHITECTURE.md`. | Its tuple gains the parts. |
| `scripts/needle-extract.py` | Its `SPEC` constant is the file path. Superseded by `build-index.py`. | Retires, or its constant becomes the assembled set. |
| `scripts/stamp-versions.py` | Stamps the title version into `PRODUCT_SPEC.md`. | Stamps the front file only. A part carries no version line. |
| `scripts/rank-criterion-defects.py` | Its header names the spec; its input arrives on the command line. | No code change. Its header sentence is repointed. |
| `scripts/gen-language-consumers.py` | Generates a page whose example commands name the file. | Regenerates with the new commands. |
| `hooks/chat-law-hook.sh` | Its reminder text tells the seat that a spec code lives in `PRODUCT_SPEC.md`. | Its text names the front file and its parts directory. |
| `hooks/conduct-judge.py` and `hooks/conduct-law.md` | Name the file inside an example trace line. | No change. The example is illustrative. |

## The data files keyed by the path

Seven data files hold `PRODUCT_SPEC.md` as a key or a governed name.

| File | What it holds | What it must do after |
|---|---|---|
| `guardrails/spec-ratchet.json` | `governs`, and the bytes-per-criterion bound 207.2. | `governs` names the set. The bound stays one number. |
| `guardrails/doc-bounds.json` | The 840000-byte ceiling and its reason. | One ceiling per part, plus one for the set. |
| `guardrails/criterion-readability.json` | `governs: PRODUCT_SPEC.md`, and five baselines with recorded reaches. | `governs` names the set. The baselines stay whole-set counts. |
| `scripts/spec-debt-cap.json` | `max_redundancy_open` keyed by `PRODUCT_SPEC.md`, value 119. | Keyed by the set. A per-part cap would hide a pair that crosses two parts. |
| `guardrails/language-rules.json` | Rule definitions, reaches and a pin `PRODUCT_SPEC.md:212`. **Another session owns this file.** | Its reach sentences and its one line pin are repointed by its owner. |
| `guardrails/progress-baseline.json` | Recorded sources naming the file. **Another session owns this file.** | Its source notes are repointed by its owner. |
| `guardrails/rule-census.json` | A census entry keyed by the file. | Gains one entry per part. |

`scripts/progress-report.py` also names the path six times, including its `SPEC_PATH` constant and two
`doc_bounds` lookups. **Another session owns that file**, together with `docs/PROGRESS.md` and
`tests/test_progress_report.py`. Its repoint is that session's, and this plan only names it.

## The pack files that name the path

Sixteen files under `skills/`, `templates/`, `adopt/`, `evals/` and `scaffold/` name the spec by path.

They are `skills/spec-author/SKILL.md` with eight mentions, `adopt/ADOPT.md` with four,
`adopt/install-ratchet.sh` with three, `skills/text-audit/SKILL.md` with three, and
`skills/build-pipeline/SKILL.md`, `skills/feedback-collector/SKILL.md`,
`skills/product-prover/SKILL.md`, `templates/test_scaffold.template.py` with two each. One mention
each sits in `skills/live-spec-base/SKILL.md`, `skills/spec-author/README.md`,
`templates/ARCHITECTURE.template.md`, `templates/ROADMAP.template.md`,
`templates/TEST_MATRIX.template.md`, `evals/build-pipeline.md`, `evals/spec-author.md` and
`scaffold/guardrails/guardrails.config.example.json`.

**`skills/text-audit/SKILL.md` is owned by another session.** Its three mentions and its 250-line
sentence are that session's to repoint.

The templates matter beyond this repo. A host adopting the pack scaffolds its own spec from
`templates/`. The templates therefore need a decision: does a new project start as one file and divide
later, or start divided? That question is in the open list at the end.

## The spec's own requirements about its own shape

Four requirements state the shape the division changes, and each is a spec edit the pipeline owns.

Requirement 277 criterion 1 states that the spec opens with a preamble, then a glossary, then a body of
requirements, in that order. After the division the body sits in 42 files. That criterion is amended.

Requirement 278 states that the generated index is built from the criteria. Its wording survives, and
the location's new file column joins it.

Requirement 280 states that a document's bytes-per-criterion may only fall. Its subject becomes the
assembled set.

Requirement 281 states that a changed section passes the mechanical lints and then the cold readers.
Its subject is already a section, so the division suits it. The wording is checked for any assumption
of one file.

`docs/spec-format.md` states the same document structure in its own words, and it is amended in the
same delivery.

---

# Part 5 — the review question

## The answer

**Yes. Both review skills can still check the whole set, and each needs three sentences added.**

Two conditions hold. The phrase "the document" must resolve to the assembled set of 43 files. The
assembly must be a stated step carrying a stated reach.

## What product-prover's own text requires

`skills/product-prover/SKILL.md` line 276 states that all three review modes keep the whole document in
view. It gives the reason on the next line: a cross-section hole is findable only when both sides of
the seam are present at prove time.

The same file names three more whole-document duties. Its FULL mode covers the whole spec (line 234).
Its CROSS-LINK mode keeps one mandatory whole-document step, the quantifier re-verify over every
enumeration and universal quantifier (lines 236 to 244). Its class-hunt question sweeps the whole
document for the same pattern in every other section (line 675). Its FULL-pass output carries the count
of `[default]`-tagged sentences accumulated in the document (line 861).

None of those four duties depends on the text sitting in one file. Each depends on the text being
present at once. A concatenation of the 42 parts satisfies every one of them.

## What design-reviewer's own text requires

`skills/design-reviewer/SKILL.md` step 1 builds its own element inventory, run fresh in the pass, over
every element a spec sentence names. Step 3 groups elements whose role sentences match. Step 4
tabulates the declared interactions of each member from the spec's own clauses.

Those three steps compare members that may sit in different groups. G36 and G37 hold the composition
axes, and the surfaces they govern sit across a dozen other groups. So the pass needs the assembled
set, exactly as the prover does.

## What changes for both

**One: a named assembly step.** Each skill gains a sentence at the point where the document is loaded.
It names the front file, the parts directory, and the order the parts concatenate in.

**Two: a reach line.** Each pass states, on its record, how many part files were opened and how many
requirements were covered. Today a whole-document read is invisible in the record. After the division a
missed part is a silent hole, so the reach line becomes the net against it.

**Three: a located finding.** A finding names its part file beside its requirement number. The prover's
finding form already quotes a section name, and the part file is one more field of the same kind.

## The one thing that gets harder

A scoped pass gets cheaper and a full pass gets no cheaper. CROSS-LINK and FEATURE-FIT narrow to one
surface's seams. After the division a scoped pass opens the glossary plus the two or three parts its
surface sits in. The FULL pass still opens all 43 files.

So the division buys nothing for the milestone pass, and it buys a great deal for the everyday one.
That trade is worth stating to the person before the work starts.

---

# Part 6 — the order of work

Each step lands green on its own and leaves the tree shippable.

## Step 1 — the location resolver

Add to `guardrails/specformat.py` one function mapping a code to its requirement, its criterion and its
file. Its only input at this step is the single `PRODUCT_SPEC.md`, so every file it returns is the same
name.

Extend `scripts/build-index.py` to emit the file column, and extend
`guardrails/check-index-generated.py` to compare it. The committed table gains a column whose every
cell reads `PRODUCT_SPEC.md`.

**Green when** the index gate passes with 386 codes agreeing body-to-table, and the full suite passes.

## Step 2 — the assembly reader

Add one function to `guardrails/specformat.py` returning the assembled spec text, and one matching
helper to `tests/conftest.py`. At this step the assembly is one file, so every consumer sees the exact
bytes it sees today.

Repoint the 389 conftest call sites across 115 test files to the new helper. Repoint the 18 test files
that build the path themselves. Repoint the 20 executable gates and scripts, except the file another
session owns.

**Green when** the full suite passes with no assertion changed, and every repointed gate prints its
reach line.

## Step 3 — the spec's own clauses

Run the amendment of Requirement 277 criterion 1, Requirement 278, Requirement 280 and Requirement 281
through the pipeline, together with `docs/spec-format.md`.

This step carries a delta record per code, per Requirement 279. It carries the prover pass and the
design review the format-family change earns.

**Green when** the delta classifier passes, the prover record is fresh, and the suite passes.

## Step 4 — the cut

Create `PRODUCT_SPEC/` and write the 42 part files. Leave the preamble, the glossary and the generated
table at `PRODUCT_SPEC.md`, and add the list of parts.

Prove content preservation by the family's word-and-punctuation multiset method, named in
`docs/architecture-format.md`. The concatenation of the 42 parts equals the removed body, byte for
byte, so the proof is a byte equality.

**Green when** the multiset proof holds, the assembled set equals the pre-cut document, and the full
suite passes with no assertion changed.

## Step 5 — the ceilings and the baselines

Rewrite `guardrails/doc-bounds.json` with one ceiling per part plus one for the set, each with its
reason. Repoint the `governs` fields of `guardrails/spec-ratchet.json` and
`guardrails/criterion-readability.json`. Repoint `scripts/spec-debt-cap.json`.

Re-freeze the 43 files with `scripts/spec-freeze.py`.

**Green when** the doc-bound gate, the size ratchet, the criterion-readability ratchet and the freeze
gate all pass, each printing the count of files opened.

## Step 6 — the review skills and the pipeline

Add the assembly step, the reach line and the located finding to `skills/product-prover/SKILL.md` and
`skills/design-reviewer/SKILL.md`. Repoint `skills/spec-author/SKILL.md`,
`skills/build-pipeline/SKILL.md` and `skills/live-spec-base/SKILL.md`.

Run each changed skill through skill-creator, per the standing rule on a skill-body change.

**Green when** the skill evals pass, the config-health check passes over the installed copies, and the
suite passes.

## Step 7 — the templates and adoption

Repoint `templates/`, `adopt/ADOPT.md`, `adopt/install-ratchet.sh`, `evals/` and the scaffold example.
Answer the founding question in the open list before this step starts.

**Green when** the scaffold tests pass and the adoption walk completes on a fixture host.

## Step 8 — retire the crutch

Where a gate is honest per part, point it at the part. The requirement-shape
gate, the no-history gate and the weak-word gate are the three candidates, since each judges a
criterion in isolation.

Leave the vocabulary gate, the one-name gate, the index gate, the size ratchet and the readability
ratchet on the assembly. Each of those compares one part of the document against another.

**Green when** every gate names its own reach, and no gate silently covers less than it did before.

---

# Open questions

Each names the fact that would settle it.

**1. Does the glossary split with the body?** This plan keeps all 250 entries at the front file. A
reader of one part then holds two files open. **Settled by:** an amended sentence in
`docs/spec-format.md` stating whether a family document's glossary may sit apart from its body. No
current sentence answers it.

**2. Does the cap count a group file's header?** This plan counts requirement bodies alone.
**Settled by:** an amended sentence in `skills/text-audit/SKILL.md` line 86 stating what the 250 lines
cover. That file is owned by another session this session.

**3. What is the parts directory named?** This plan proposes `PRODUCT_SPEC/`. **Settled by:** a
recorded decision in `DECISIONS.md`, since the one-name law permits several readings and none of them
is derivable from a written rule.

**4. Does a per-part byte ceiling replace the one ceiling, or join it?** This plan proposes both.
**Settled by:** the reason field already in `guardrails/doc-bounds.json`, which names the owner's cost
as a guard's scan and a grep run slowing with file size. A per-part ceiling matches that reason, and
whether the whole-set ceiling still earns its place needs the owner's word.

**5. Does a new host's spec start divided or start whole?** **Settled by:** a measurement of the
smallest adopted spec against the 250-line cap. A project below 250 lines of requirements has no
division to make, and the threshold at which the templates should switch is not written anywhere.

**6. Do the 16 split clusters read as one subject in two parts, or as two subjects?** This plan names
each part as its own subject. **Settled by:** a cold read of two adjacent parts by a fresh reader,
answering whether the second part stands without the first.

**7. Should the two gap-only codes `D-1` and `D-6` gain criteria?** Nodes own them and two matrix rows
cite them. No criterion carries either code. **Settled by:** a prover pass over Requirement 177 and
Requirement 187, which is where their gap lines sit.

---

# Where every number in this plan comes from

Each command runs from the repository root.

**Whole-file counts.**

    wc -l -c PRODUCT_SPEC.md
    grep -c '^## Requirement ' PRODUCT_SPEC.md
    ls tests/test_*.py | wc -l
    grep '^## Requirement' PRODUCT_SPEC.md | grep -c 'feature: F-'
    grep -o 'feature: F-[a-z][a-z-]*' PRODUCT_SPEC.md | sort -u | wc -l
    python3 guardrails/check-size-ratchet.py PRODUCT_SPEC.md
    python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md
    python3 guardrails/check-doc-bound.py

**The four segment counts** — preamble, glossary, body and generated table:

```bash
python3 - <<'PY'
t=open('PRODUCT_SPEC.md',encoding='utf-8').read().split(chr(10))
def seg(a,b,label):
    s=chr(10).join(t[a-1:b]); print(label, b-a+1, len(s.encode()))
seg(1,12,'preamble'); seg(13,265,'glossary')
seg(266,7385,'body'); seg(7386,7777,'reference')
PY
```

**Every group and cluster count** in Part 1 and Part 2:

```bash
python3 - <<'PY'
import re
L=open('PRODUCT_SPEC.md',encoding='utf-8').read().split(chr(10))
h=[(i,int(m.group(1))) for i,l in enumerate(L)
   for m in [re.match(r'## Requirement (\d+):',l)] if m]
e=[i for i,l in enumerate(L) if l.startswith('## Reference')][0]
S={}
for k,(i,n) in enumerate(h):
    j=h[k+1][0] if k+1<len(h) else e
    b=L[i:j]
    S[n]=(j-i, len(chr(10).join(b).encode())+1,
          sum(1 for x in b if re.match(r'^\s*\d+\. ',x)))
def g(spec):
    ns=[]
    for p in spec.split(','):
        a,_,b=p.partition('-')
        ns += list(range(int(a),int(b)+1)) if b else [int(a)]
    return len(ns), sum(S[n][0] for n in ns), sum(S[n][1] for n in ns), sum(S[n][2] for n in ns)
print(g('1-8'))   # one group; substitute any row's requirement range
print(len(S), sum(v[2] for v in S.values()))
PY
```

**The test-reader count** in Part 4:

    grep -roE '(read|read_flat|read_all|read_all_flat)\("PRODUCT_SPEC\.md"\)|open\([^)]*PRODUCT_SPEC\.md[^)]*\)|join\([^)]*"PRODUCT_SPEC\.md"\)' tests/*.py | sed 's/:.*//' | sort -u | wc -l
    grep -oE '(read|read_flat|read_all|read_all_flat)\("PRODUCT_SPEC\.md"\)' tests/*.py | wc -l

**The gate, data-file and pack-file lists** in Part 4:

    grep -l 'PRODUCT_SPEC\.md' guardrails/*.py guardrails/*.sh guardrails/pre-push scripts/*.py hooks/*
    grep -l 'PRODUCT_SPEC\.md' guardrails/*.json scripts/*.json
    grep -rl 'PRODUCT_SPEC' skills/ templates/ adopt/ evals/ scaffold/

**Every seam count** in Part 3. The script parses the architecture through
`guardrails/archformat.py`, the matrix through the reader in `tests/test_traceability.py`, and the
anchors through `PRODUCT_SPEC.index.md`:

```bash
python3 - <<'PY'
import re,sys
sys.path.insert(0,'guardrails'); import archformat
R=lambda p: open(p,encoding='utf-8').read()
TOK=r'[A-Z]+-[0-9]+(?:\.\.[A-Z]*-?[0-9]+)?'
def ex(a):
    m=re.match(r'([A-Z]+)-(\d+)\.\.(?:[A-Z]+-)?(\d+)$',a)
    return ['%s-%d'%(m.group(1),i) for i in range(int(m.group(2)),int(m.group(3))+1)] if m else [a]
cr={}
for line in R('PRODUCT_SPEC.index.md').split(chr(10)):
    m=re.match(r'^\|\s*(%s)\s*\|\s*(.+?)\s*\|$'%TOK,line)
    if m:
        rs={int(x) for x in re.findall(r'R(\d+)\.\d+',m.group(2))}
        for c in ex(m.group(1)): cr.setdefault(c,set()).update(rs)
cr.setdefault('D-1',set()).add(177); cr.setdefault('D-6',set()).add(187)
GS=[('G01','1-8'),('G02','9-16')]   # the full 42-row list of Part 1
rg={}
for gid,spec in GS:
    for p in spec.split(','):
        a,_,b=p.partition('-')
        for n in (range(int(a),int(b)+1) if b else [int(a)]): rg[n]=gid
cg={c:{rg[r] for r in rs if r in rg} for c,rs in cr.items()}
print('codes', len(cg), 'multi-group', sum(1 for g in cg.values() if len(g)>1))
for nd in archformat.parse_nodes(R('ARCHITECTURE.md')):
    gs=set()
    for a in nd.anchors_expanded: gs |= cg.get(a,set())
    print(nd.name_cell, len(nd.anchors_expanded), len(gs))
mat=re.split(r'(?m)^## Reference *$',R('TEST_MATRIX.md'),1)[0]
cur=None
for line in mat.split(chr(10)):
    m=re.match(r'^### \[node: (.*)\]\s*$',line)
    if m: cur=m.group(1); continue
    if cur and line.startswith('|') and not line.startswith('|---') and 'Owning test' not in line:
        cells=[c.strip() for c in line.strip('|').split('|')]
        if len(cells)==5:
            mm=re.search(r'\[([^\[\]]*)\]\s*$',cells[1].strip())
            refs=set()
            if mm:
                for t in re.findall(TOK,mm.group(1)): refs.update(ex(t))
            gs=set()
            for c in refs: gs |= cg.get(c,set())
            print(cells[0], cur, len(refs), len(gs))
PY
```

The full 42-row group list for that script is the Requirements column of the Part 1 table.
