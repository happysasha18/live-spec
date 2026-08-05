# Prover record — the public edition and the reader repairs, 2026-08-05

Prover skill: product-prover, live-spec pack v4.3.0. Mode: cross-link over the three changes waiting
to be pushed, plus a re-read of `PRODUCT_SPEC.md` and `ARCHITECTURE.md` against them (SPEC M-6,
INV-116). Written by a seat that authored none of this work (SPEC INV-237).

## Scope

**What this record reviews.** The tree at `4071f8a`, with `eb1d4a5` and `4071f8a` as the committed
delta against `c869cbb`, plus three changes standing uncommitted in the working tree. Five surfaces
carry it:

- `README.md`, `OVERVIEW.md`, `ARCHITECTURE.md` and `DECISIONS.md` were repaired for a first-time
  reader: the skill count, the install steps, one link, and one evidence sentence;
- `scripts/sync-mirrors.sh` gained a selection step, so a skill's public mirror publishes
  `editions/<skill>/` where that directory exists;
- `tests/test_mirror_editions.py` holds six tests over that selection;
- `editions/product-prover/` stands in the working tree at 116 kilobytes, holding the first public
  edition: `SKILL.md`, `README.md`, `PROVENANCE.md`, `LICENSE`, `examples/`, and `reference/`;
- `tests/test_skill_count_agrees.py` and a rebuilt `guardrails/rule-census.json` stand beside it,
  both uncommitted.

The delta ships machines, so this pass reads the machines beside the text:

- `scripts/sync-mirrors.sh:71-79` (the selection) · `:81-91` (the print flag) · `:399-403` (the copy
  step) · `:406-448` (the banner, the stamps, and the language scan);
- `scripts/rule-census.py:73` · `guardrails/check-doc-findings-bound.py`;
- `PRODUCT_SPEC.md` glossary entry for the standalone mirror · Requirements 148, 198 and 199 ·
  `docs/architecture-format.md` · `TEST_MATRIX.md` rows M-168, M-225 and M-339.

**The record this pass stands on.** `docs/prover/2026-08-05-night-campaign-push-recheck.md` holds
seven findings and its addendum holds one more. This pass files nothing that repeats them. Its F1 and
F6 named the shape that recurs below: a shipped behaviour whose only home is a test.

**Commands run.** Every claim below was taken from a run or from the file.

- `python3 -m pytest -q tests` — 1 failed, 2325 passed, log at `suite-run-6.log` in this session's
  scratch directory. The section below reads that log.
- `python3 -m pytest -q tests/test_skill_count_agrees.py tests/test_mirror_editions.py` — 10 passed.
- `git show --stat eb1d4a5` and `git show --stat 4071f8a`, with the full diff of each.
- Six probes of the count test's own expression, quoted inside the section that judges it.
- `python3 -c` over `guardrails/progress-baseline.json`, printing every recorded reading round.
- Searches of `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, `TEST_MATRIX.md` and `ROADMAP.md` for the words
  `editions`, `test_mirror_editions` and `test_skill_count_agrees`. All four searches return nothing.

## Verdict

**The public edition is working machinery standing on no written rule, and the specification still
describes a mirror that copies the skill folder.**

The selection behaves the way its commit message describes. A skill with no edition publishes its own
directory, a skill with one publishes the edition, and a neighbour is unaffected. Six tests cover each
of those, and they run in a scratch pack, so the real tree never decides the answer.

The strongest hole is F1. The mirror is now a place where a second copy of a skill's method is
published, and no requirement says so. The glossary sentence a reader would consult still describes a
mirror rebuilt from the pack folder.

F2 follows from the architecture's own format. A new top-level directory that ships something is a
part, and the component inventory does not name it.

Three more sit in the machinery. An edition holding no skill file publishes a public repository with
no skill in it. An edition that falls behind its skill has no way out, and every sync reports the
mirror up to date. And one repaired sentence in `DECISIONS.md` now cites a file that records twice the
rounds the sentence claims.

One more sits on the delta's own record. The commit message of `4071f8a` states nine tests, and the
file holds six.

| # | Kind | Claim | Status |
|---|---|---|---|
| F1 | defect | The public edition is shipped behaviour with no requirement, no matrix row, and a glossary entry describing the older mirror | open |
| F2 | defect | `editions/` ships to the public and stands in no part of the architecture: no inventory line, no pin, no owning node | open |
| F3 | defect | A directory alone decides the publish source, so an edition missing `SKILL.md` publishes a public repository holding no skill | open |
| F4 | defect | Nothing binds an edition to the skill it stands for, and the sync reports a stale mirror as up to date | open |
| F5 | defect | The sync publishes from the working tree while its commit message names a commit, so a published text can exist in no commit | open |
| F6 | defect | `DECISIONS.md` states three reading rounds and cites a file recording six on the same document | open |
| F7 | defect | The commit message of `4071f8a` states nine tests and `tests/test_mirror_editions.py` holds six | open |
| F8 | recommendation | The count test pins one English phrase in four documents, and no criterion states the rule it holds | open |

## Phase 1 — the model, as the delta leaves it

**The mirror sync.** Some skills in this pack also stand as their own public repositories. One script
rebuilds each of them from the pack at every push. For each folder under `skills/`, the script looks
for a public repository of the same name and clones it. It then replaces the contents, writes a
read-only banner, and stamps a generated release history and an attribution line. It scans the
assembled README for stray Cyrillic and owner names, and pushes any change.

Tonight the replace step gained a choice. Where `editions/<skill>/` exists, that directory is what
goes out, and `skills/<skill>/` stays the copy this project loads. Where it is absent, the skill's own
directory goes out as before. A flag `--print-publish-source` prints the choice for one skill and
exits before any clone.

**The first edition.** `editions/product-prover/` holds a rewrite of the prover skill for a reader
outside this project. The internal copy cites about fifty internal codes as its authority. The edition
states each of those rules in plain words, and `PROVENANCE.md` records the mapping in a table. The
internal copy measures 62 kilobytes. The edition measures 42 kilobytes of skill text, plus 26
kilobytes of reference.

**The count of skills.** Eleven folders stand under `skills/`. One of them is the shared rulebook the
other ten load. Four documents each state that number, and each now states the unit beside it. One
test reads the number off disk and requires the four documents to agree with it.

**Actors.** The owner runs the sync script from this machine before or after a push. A stranger
arrives at a public mirror, reads it, and copies files into their own skills directory. A session in
this project loads the copy under `skills/`. A first-time reader of this repository reads the four
documents that state the count.

### What I assumed

- I read the glossary entry for the standalone mirror as the specification's statement of what the
  mirror publishes. No requirement states a source directory. F1 rests on that reading. The other
  reading is that the entry says only where the content comes from. F1 then becomes a request for a
  missing sentence.
- I read `editions/` as a shipped part of the pack, because its contents are pushed to a public
  repository by this pack's own script. F2 rests on that. Under the other reading it is working
  material, and it then owes an entry in the recoverable-file list instead.
- I treated the edition's own accuracy as out of scope. Reading 42 kilobytes of rewritten method
  against 62 kilobytes of source is a full pass on its own. This record covers the mechanism that
  publishes it.
- I found no criterion, no matrix row, and no queue row naming `editions/`, `test_mirror_editions.py`
  or `test_skill_count_agrees.py`. F1, F2 and F7 rest on that search.

## Phase 2 — the shipped machines, read against the text

**What holds in the selection.** `scripts/sync-mirrors.sh:71-79` returns the edition directory where
it exists and the skill directory otherwise. `:399-403` calls that function at the copy step and
prints a line naming the edition when one is chosen. `:81-91` handles the print flag above the
release-history computation, so a scratch tree with no history can still run it. The six tests build a
scratch pack and assert each branch, and one of them asserts that the flag reaches no repository.

**What holds in the reader repairs.** The install section now names the second install step, its
configuration file, its hook lines, and its two prerequisites. The four checks it names match the four
files under `scaffold/guardrails/`: completeness, conflicts, tests present, and traces to spec. The
prover link now points at `skills/product-prover/`, which exists. The four documents that state the
skill count agree at ten working skills plus the rulebook, and the suite holds that agreement.

**What the specification says about the mirror.** Two sentences carry it.

> "**standalone mirror** — a public mirror repository rebuilt from the pack folder by the sync script,
> carrying its own generated banner, release history, and attribution line." — PRODUCT_SPEC.md,
> glossary

> "The pack *shall* treat the package as the source and the standalone repositories as read-only
> mirrors of it." — PRODUCT_SPEC.md, Requirement 198, criterion 3

Both still hold in the weak sense: the pack is still the source, and a hand edit on a mirror is still
overwritten. Neither describes what now ships. A reader of the glossary expects the mirror to carry the
pack folder's own text. The mirror now carries a separately written document that states the same
method in different words. That difference is the whole point of the change, and the specification is
silent on it.

**What the architecture format demands.** `docs/architecture-format.md` states three things this delta
touches. The first is the architecture's reading job:

> "a reader opens it to learn what parts exist, what each part is for, which spec facts each part
> owns, and where to find the part on disk"

The second is what the opening section carries: "a few lines naming the whole system and the places
it runs". The third is what a pin is:

> "the list of `file:line` pins with a short label each, stating where the node's responsibility is
> carried on disk"

## Phase 3 — findings

F1 — The public edition is shipped behaviour with no requirement behind it

> "**standalone mirror** — a public mirror repository rebuilt from the pack folder by the sync script"
> — PRODUCT_SPEC.md, glossary

Since `4071f8a` the mirror is rebuilt from one of two places, and the specification names neither. No
requirement mentions an edition. Requirement 148 governs the release-history section on a mirror.
Requirement 198 criterion 3 governs the mirror's read-only status. Requirement 199 governs skill lists.
The matrix rows that touch the sync script — M-225 and M-339 — describe the attribution line and the
release history. The six new tests are claimed by no row.

The person affected is the next session that reads the glossary to learn what a mirror holds. It will
read that the mirror carries the pack folder, open a mirror, and find text that appears nowhere under
`skills/`. A later session repairing the script to match the glossary would delete the selection and
take the six tests red with it. A second consequence reaches the public. The mirror is now a second
normative home for the shared rules. Requirement 198 criterion 2 calls a second full statement of a
shared rule drift.

Write one requirement covering the edition. It should state these properties:

> A skill *shall* be able to ship a public edition under `editions/<skill>/`, stating the same method
> with every internal code resolved into the rule it stands for. *when* that directory exists, the
> mirror sync *shall* publish it, and `skills/<skill>/` *shall* stay the copy this project loads.
> *when* it is absent, the sync *shall* publish the skill's own directory. An edition *shall* carry the
> files a reader needs to run the skill, and the sync *shall* refuse a publish source missing them. An
> edition *shall* record which skill and which version it was written from, and the pack *shall* hold
> the two in step.

The last two sentences answer F3 and F4. Then add a matrix row claiming the six tests. Correct the glossary
entry to say the mirror carries the skill's public edition where one exists. Requirement 198's drift
rule needs one sentence carving the edition out. The edition restates shared rules by design, for a
reader who cannot follow a code.

`defect · missing-rule (invariant)`

F2 — A directory that ships to the public stands in no part of the architecture

> "Its reading job is a component inventory: a reader opens it to learn what parts exist, what each
> part is for, which spec facts each part owns, and where to find the part on disk." —
> docs/architecture-format.md

`editions/` is a new top-level directory whose contents are pushed to a public repository. A search of
`ARCHITECTURE.md` for the word returns nothing. The opening section reads:

> "live-spec is a skill pack: ten working skills plus the one shared rulebook they all load, each of
> them text a model reads. Templates, guardrails, and its own dogfood documents sit beside them in one
> repo." — ARCHITECTURE.md, the shape at a glance

That inventory names four kinds of content, and the directory this delta added is a fifth. The publish
node carries the sync script's pin with a four-part label:

> "the mirror sync `scripts/sync-mirrors.sh:1` (banner · release history · attribution · language
> scan)" — ARCHITECTURE.md, node publish, pins

The label enumerates what the script does, and the selection step is now a fifth thing it does.

The format's own answer settles whether a node is owed. A node is a place spec facts live. This
behaviour's facts belong to the publish node, which already owns the sync script and the mirror
anchors. So no new node is owed. Two things are owed. One line in the opening inventory names
`editions/` and what it holds. The publish node's pin label gains the selection. Once F1's
requirement exists, its anchor joins the publish node's owns list.

The person affected is a reader using the architecture as the component inventory it promises to be.
They will count the parts of this repository and miss the one whose contents strangers read.

`defect · missing-rule (invariant)`

F3 — An edition holding no skill file publishes a public repository holding no skill

> ```
> if [ -d "$edition" ]; then
>   printf '%s\n' "$edition"
> ```
> — scripts/sync-mirrors.sh:74-75

The presence of a directory is the whole test. Nothing checks that the directory holds `SKILL.md`,
which is the one file a skill needs. The copy step then runs `rsync -a --delete`, which empties the
mirror of everything the edition lacks. Two later steps pass over the gap in silence.
`stamp_attribution` opens with `[ -f "$file" ] || return 0` at `:113`. `check_mirror_language` opens
with the same line at `:324`. So a half-written edition reaches the commit and the push.

I read the shape by hand. A run of this script pushes to a public repository. The
sequence is plain in the file: select, delete, copy, banner, stamp, scan, commit, push. An edition
holding a README alone produces a mirror holding a banner, a README, a release history, and an
attribution line. A stranger clones it and installs nothing.

The consequence lands in public and stays there until someone notices. The mirror's own history keeps
the previous good state, so recovery is a revert, and the loss is the time the empty repository stood.

Have the selection refuse a source directory with no `SKILL.md`, and have the script stop with that
skill's name. The class behind the instance is wider: every step after the copy treats a missing file
as nothing to do. One check before the copy, asserting the publish source holds the files a skill
needs, closes the class at its root.

`defect · partial-success-risk (atomicity)`

F4 — Nothing brings an edition forward, and the sync reports a stale mirror as up to date

> "The pack stays the source of both, so a hand edit made on a mirror is still overwritten by the next
> sync." — the commit message of `4071f8a`

The pack is the source of both copies, and only one of them changes when the method changes. A session
editing `skills/product-prover/SKILL.md` leaves `editions/product-prover/SKILL.md` as it stands. No
test compares them. No check counts them. No criterion asks for either. The prover skill was edited on
2026-08-04, and two of its sections moved several hundred lines. An edition written before that edit
would still publish today.

The state has no exit. Once the edition exists, the mirror's content is decided by a file that no
process updates. The sync's own report makes it worse. With the edition unchanged, the script prints
`product-prover: up to date`. A reader takes that line to mean the mirror matches the pack.

The person affected is the stranger the edition was written for. They read a method that this project
has moved past, with no date and no version on the page telling them so.

Two roads stand. Road a: the edition records the skill's version it was written from, and a suite test
reds when the skill's version moves ahead. Road b: a suite test compares the two files' rule sets and
reds on a rule present in one and absent from the other. I prefer road a. It is cheap, it reds at the
moment the debt is created, and it needs no comparison of two texts written in different words. Road b
catches more and costs a comparison nothing today can perform reliably. Either road also fixes the
report line, which should say which source it published.

`defect · unenforceable-promise (discharge)`

F5 — The sync publishes from the working tree while its commit message names a commit

> `commit_msg="sync from live-spec pack ${PACK_VERSION} (${PACK_SHA})"` — scripts/sync-mirrors.sh:456

`PACK_SHA` comes from `git rev-parse --short HEAD`. The content comes from the disk. Today those two
disagree. `editions/product-prover/` is untracked, so the mirror would publish 116 kilobytes of text
that `HEAD` does not hold, under a message naming `HEAD`. A reader of the mirror's history who checks out
that commit of the pack finds the internal copy where the edition should be.

This predates the delta for the skill directories, and the delta widens it. Before, an uncommitted edit
under `skills/` was visible to the session doing the sync. Now a whole publish source can exist outside
git. The tests that hold the selection all run in scratch packs, so none of them reads the real tree's
tracking state.

Commit `editions/` with this push. For the class, two roads stand. Road a: the sync refuses to publish a
source carrying uncommitted changes. Road b: the commit message says the working tree when the tree is
dirty. Road a is the stronger answer, since a public artifact should be traceable to a commit.

`defect · direct-contradiction (contradiction)`

F6 — The evidence sentence states three rounds and cites a file recording six

> "three rounds of readings on one document returned fifteen and ten blocking stops, then five and
> eight, then nine and four... Inside a single round the two readers did stop at some of the same
> places, and `guardrails/progress-baseline.json` holds that count per round." — DECISIONS.md,
> the 2026-07-29 entry as `eb1d4a5` left it

The repair fixed the half that contradicted the rule above it, and it added a pointer to the evidence.
The pointer does not lead where the sentence says. `guardrails/progress-baseline.json` records rounds
for one document, `skills/text-audit/SKILL.md`. It holds six of them, dated 2026-07-29, with agreed
counts of 8, 3, 2, 2, 2 and 3. The reading counts the sentence quotes — fifteen and ten, five and
eight, nine and four — appear in no entry. The sentence also says each round gave the file to two
readers, and the sixth entry records three.

The person affected is a reader checking the arithmetic on the page, which is exactly the reader this
commit was written for. They follow the pointer and find a different number of rounds and no matching
counts. A decision record whose evidence fails a check is weaker than one that cites nothing.

Restate the sentence from the file it names. Six rounds ran on one document, and the agreed count fell
from eight to two and held there. Keep the per-reader stop counts only where a named source carries
them. The wider rule this instance serves is sound, and only its evidence line needs the repair.

`defect · direct-contradiction (contradiction)`

F7 — The commit message states nine tests and the file holds six

> "Nine tests hold it... Two more prove the choice reaches the copy step and that reading it touches no
> repository." — the commit message of `4071f8a`

`tests/test_mirror_editions.py` holds six test functions, and pytest collects six from it. The message
describes them in two groups: three over the choice itself, and two more over the copy step and the
print flag. That is five described against a stated nine. A sixth stands in the file, asserting that the print
flag names the skill it needs.

The commit message is the record of what landed, and a reader counting tests from it counts wrong. The
same mismatch reaches this pass. The first reading of this delta took the number from the message. It
carried it into three sections of this record before the file was counted.

Two consequences follow. A later session judging coverage from the message believes three more tests
exist than do. And the message repeats the shape the sibling commit was written to
repair: `eb1d4a5` exists because four documents stated one count four ways.

Restate the number in the message from the file. The class behind it is the one `eb1d4a5` opened and
left half closed. A count is written in prose beside the thing it counts, and nothing reads the two
together. The count test now covers four documents for one number. Commit messages sit outside every
such check, and a message cannot be changed after the fact. So the repair here is the discipline of
counting before writing.

`defect · direct-contradiction (contradiction)`

## The count test, judged

`tests/test_skill_count_agrees.py` reads the number off disk as the count of folders under `skills/`
less one for the rulebook. It then requires four documents to state that number: the README, the
overview, the architecture, and the base skill. Each must name the rulebook in the same sentence.
A fourth test reads the overview's section heading and counts the entries under it.

**Could it pass while the documents disagree?** Yes, in three ways.

The pattern it searches for is a number word, the word `working`, up to three further words, and
`skill` or `skills`. Anything stating the count in another shape is invisible to it. I probed the
expression on five sentences:

- `The pack holds 10 working skills, plus the one shared rulebook.` — no match. A numeral is invisible.
- `Nine skills carry the pipeline.` — no match.
- `Eleven folders stand under skills/.` — no match.
- `ten working skills, plus the one shared rulebook they all load` — matched.

So a document may carry the required phrase once and contradict itself anywhere else, and the test
stays green. The commit message names that exact defect in the overview: a heading claiming nine over
eleven entries. The fourth test catches it in the overview alone, because it reads that one heading.

Second, only four documents are read. The skill count also reaches `docs/pipeline.md`, the plugin
metadata, the closing lists inside the skills, and now `editions/product-prover/README.md`, which a
stranger reads. None of those is in the list.

Third, the rulebook check searches for the first matching sentence only. A document with two count
sentences must name the rulebook in the first one alone.

**Could it red on a lawful change?** Yes, in three ways.

The gap of up to three words between `working` and `skills` matches ordinary prose. Two probes:

- `A session loads one working copy of the skills.` — matched, reporting the count as one.
- `It reds on one working session over installed skills.` — matched, reporting the count as one.

Either sentence, written into any of the four documents, reds the suite. The message says the document
states one working skill.

Second, the test pins an English phrase. A lawful copy edit that says the same thing in other words
reds with "states no working-skill count at all". No criterion states that phrasing, so an editor
meeting the red has nothing to consult except the test.

Third, the number is derived from a directory listing that skips only dotted names. A folder added
under `skills/` for shared material would raise the count and red all four documents at once. Above
twenty working skills the number word lookup raises a key error, so the reader meets a stack trace.

**The judgement.** The test holds a real fact and holds it in a brittle place. It would have caught
the original four-way disagreement, since three of the four documents lacked the phrase entirely. It
would miss the same class restated in numerals or without the word `working`. Its shape is the one the
2026-08-05 record's F6 already named: a blocking check owning a rule the specification never states.

Two repairs, both cheap. Read the count as any number word or numeral standing before `skill` or
`skills` within a short window. Then require every such statement in a document to agree, so a
contradiction inside one document reds. Then write the rule down. One criterion under Requirement 199
would cover it. Every place stating how many skills the pack holds states the unit it counts, and
agrees with the folders on disk. That is F8, and it is the honest half of this section.

## The suite, 1 failed and 2325 passed

The run: `python3 -m pytest -q tests` — **1 failed, 2325 passed** in 398.74 seconds. I read the log at
`suite-run-6.log` in this session's scratch directory. Its last line reads
`1 failed, 2325 passed in 398.74s (0:06:38)`.

The single failure is `tests/test_guardrails.py::TestGateA_ProverRecord::test_real_repo_passes`. The
log carries the gate's own output under it:

```text
OK (prover record): committed record(s) for 2026-08-05 found:
  docs/prover/2026-08-05-night-campaign-push-recheck.md
OK (freshness): record commit is not older than the last PRODUCT_SPEC.md commit.
FAIL (prover record): the newest committed prover record predates the last ARCHITECTURE.md change.
  ARCHITECTURE.md last changed in commit eb1d4a5...; newest docs/prover/ commit is c869cbb...
```

So today's record exists and is committed, and the spec arm passes. The architecture arm fails, because
`eb1d4a5` changed `ARCHITECTURE.md` after the last record landed in `c869cbb`. This document is that
missing record, and committing it clears the gate. Nothing else in the suite is red.

Two checks on that reading. The previous run over the earlier tree read 2,316 passed with none failing.
This run holds 2,326 outcomes, ten more, and the ten are the six tests `4071f8a` brought plus the four
in the uncommitted count test. One test that passed then fails now, which is the gate this record
answers. I ran all ten directly and they pass. Prover records sit outside the findings census by name.
`scripts/rule-census.py:73` lists `docs/prover` among the record directories, so this file owes no
census row and gate aa is unaffected.

## The mandatory sweeps over the delta

The whole-document sweeps of a full pass are out of scope for a cross-link mode. The sweeps below ran
over the delta's own surfaces, and each verdict names what it read.

| Surface | Declared laws | Edge completeness | Cross-surface uniformity | Lifecycle | Unwritten seams |
|---|---|---|---|---|---|
| The edition selection | hit — F1, shipped behaviour with no requirement, no matrix row, and a glossary entry describing the older mirror | hit — F3, the edition holding no skill file | clean — one function decides for every skill, and the print flag reads the same function | hit — F4, an edition falling behind its skill with no way back | hit — F5, the publish source that exists in no commit |
| The published edition itself | hit — F1, a second full statement of shared rules against Requirement 198 criterion 2 | out of scope — reading 42 kilobytes against 62 kilobytes is a pass of its own | N/A — one edition exists | hit — F4, the same staleness seen from the reader's side | clean — the shipped-language scan reaches `editions/` through the repository walk |
| `editions/` as a part of the repository | hit — F2, absent from the inventory and from the publish node's pin | N/A — no stated bound | clean — the directory follows the `skills/` layout | clean — the recoverable-file list is untouched | clean |
| The four reader repairs | clean — the install steps, the four checks, and the link all match the files | clean — the four documents agree at ten plus the rulebook | hit — F6, the evidence sentence against the file it cites | N/A — no state carried | clean |
| The count test | hit — F8, no criterion states the rule it holds | hit — F8, the numeral and the bare noun both invisible | hit — F8, four documents read while others state the same count | N/A — no state carried | hit — F8, the three-word gap matching ordinary prose |

**The quantifier re-verify (INV-170).** Five enumerations were re-read against the delta. Eleven
folders stand under `skills/`. The four documents that state the count agree at ten working skills
plus the rulebook, checked by a run of the test. The four host checks the README now names match the
four files under `scaffold/guardrails/`. The publish node's pin label enumerates four parts of the sync
script and the script now does five — the first failure, folded into F2. The matrix's rule index lists
M-168 and M-171 under the skill-list rule. The four new count tests belong to neither, which is the
second failure, folded into F8. The commit message of `4071f8a` states nine tests over a file holding six —
the third failure, which is F7.

## Phase 3.5 — acknowledged gaps

The requirements this delta touches — 148, 198 and 199 — carry no open item, no marked decision, and no
rhetorical question. `editions/product-prover/README.md` states its own known issues in a section of
that name. The two narrow modes carry less mileage than the full pass. No mechanical check ships with
the skill. The trigger phrasing carries no measurement for this edition. Those are the edition's own
declared gaps, and this pass files nothing anticipating them. `editions/product-prover/PROVENANCE.md`
records two codes that carried no instruction into the edition, each with its reason.

## Phase 4 — human and operational factors

**What a reader sees.** A stranger arriving at the prover mirror after this push meets a document
written for them. The internal codes are resolved, and the provenance table shows the
resolution. The known-issues section is honest about what the edition has less experience with. That is the reader
outcome this delta was built for, and it lands.

**What an operator sees.** The sync prints one line per skill: `updated`, `up to date`, or a note that
the edition is being published. F4 makes the second of those misleading once an edition exists. The
line should name the source it published, so an operator reading the run can tell which of the two
copies went out.

**What a first-time reader of this repository sees.** The install section now runs from a plugin
command or a clone. It then passes a second script, a configuration file, four hook lines, and two
prerequisites. That path is longer than the one sentence it replaced, and it is the path that works.
The count of skills now reads the same in every place a reader is likely to land.

**Scale.** The suite took 398.74 seconds, against 489 seconds in the run before it. The ten new tests
run in a scratch pack and cost little. `editions/` adds 116 kilobytes to the repository and will grow by
roughly that much per edition.

**Privacy.** This delta widens what leaves the machine, since the edition is published text. The
shipped-language scan walks the whole repository except a named set of directories. `editions/` stands
outside that set, so the edition is scanned for stray Cyrillic and owner names before a push. The
mirror's own README is scanned a second time inside the sync.

## Phase 5 — closing

**What to fix before this push.** F5, because `editions/` is untracked and the push publishes it. F3,
because it stands between a half-written edition and a public repository, and one condition closes it.
F1's criterion, because the specification currently describes a mirror that no longer ships.

**Properties the documents should state.**

- A skill may ship a public edition under `editions/<skill>/`, stating the same method with every
  internal code resolved into the rule it stands for.
- Where an edition exists, the mirror publishes it, and `skills/<skill>/` stays the copy this project
  loads. Where it is absent, the mirror publishes the skill's own directory.
- An edition carries the files a reader needs to run the skill, and the sync refuses a publish source
  missing them.
- An edition records the skill and the version it was written from, and the two are held in step.
- The shared-rule drift rule carves out an edition, which restates those rules for a reader who cannot
  follow a code.
- Every place stating how many skills the pack holds states the unit it counts, and agrees with the
  folders on disk.

**Open questions for Alexander.** Whether an edition is bound to its skill by a recorded version or by
a comparison of the two texts. Whether the mirror sync should refuse to publish from a tree carrying
uncommitted changes.

**Queued for a taste call.** F8, together with the recommendations left open by the record of earlier
today.

**Readiness.** The specification is sound enough for these commits to be pushed, on two conditions.
`editions/` is committed, and the edition selection refuses a source with no `SKILL.md`. The push
publishes a new public artifact, and those two stand between a good artifact and a broken one. F1, F2,
F4, F6 and F7 are honest debts against working machinery. F1's criterion with F2's two architecture
lines is cheap enough to ride the same commit. Pushing with `editions/` untracked publishes text that no commit
holds.
