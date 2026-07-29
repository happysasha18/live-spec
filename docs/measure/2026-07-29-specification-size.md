# How much of the specification is stated twice — measured 2026-07-29

`PRODUCT_SPEC.md` holds 303 requirements, 1609 acceptance criteria, and a glossary of 250 entries.
Nothing has ever measured how much of that is one fact written down more than once.

This page runs the measurement the campaign plan puts before any design. It answers the plan's three
questions with a number each, and it names the requirements behind every number.

Three numbers came out. Thirty-nine requirement pairs state a fact twice, with twenty more close
calls. Twelve shapes are shared by three or more requirements. Four glossary pairs name one thing
under two words, with six more close calls.

Every count below is reachable by repeating the method stated beside it. Every count is a floor. The
sweeps that produced the candidates are described where they run, and none of them reads all 45,753
possible requirement pairs.

## The two existing tools, and what each one reaches

### The regex layer

`python3 scripts/spec-redundancy-precheck.py PRODUCT_SPEC.md` exits 1 and reports 123 candidates, 119
of them open and none waived.

Those 119 pairs split three ways by where their two spans sit. The split is computed by mapping each
reported line number to the requirement heading above it.

- 75 pairs sit inside one requirement. Two criteria of the same requirement overlap.
- 31 pairs put one span in the glossary and the other in the body. A definition and a criterion share
  their wording.
- 13 pairs cross two requirements. Two requirement pairs are reported twice, so these 13 reports cover
  10 distinct requirement pairs. This is the only slice that speaks to question one.

The class the tool catches is lexical overlap. It flags a pair when the two spans share content words
or three-word runs above a threshold. It found the strongest single hit in this whole measurement that
way: criterion 4 of Requirement 210 and criterion 3 of Requirement 216 score 1.00 on containment.

The class the tool misses is everything reworded. Its own header says so, and the miss is wide. Of the
39 pairs question one confirms below, the precheck reaches 5. It misses the other 34, including all
fifteen restatements of the forward-binding rule, because those fifteen say one thing in fifteen
different sentences.

The tool also reports outside the question. Its 75 same-requirement pairs and its 31 glossary-to-body
pairs answer something else. 106 of its 119 open pairs sit outside the subject the campaign asked
about.

### The judge harness

`scripts/spec-judge.py` runs cleanly. `--emit-prompt PRODUCT_SPEC.md` produces a 717 KB prompt: a
pinned rubric, the whole document line-numbered, and three planted defects appended as a self-test.
`--verify` reads a judge's JSON back, discards any finding whose quote is absent from the document, and
fails the run as invalid unless all three planted defects were caught.

The harness is sound, and its rubric answers a narrower question than question one. Its redundancy
criterion, C1, judges sentences: a sentence stating a claim an earlier sentence already stated. Question
one judges requirements. A pair like Requirement 48 and Requirement 265 states one fact in two
sentences that share almost no words, and a sentence-level judge has no reason to pair them.

A judge pass ran against the emitted prompt for this measurement, and the harness verified it.

    {"code":"spec-judge","selftest":"passed","surviving":156,"waived":0,"discarded":0}

The judge returned 161 findings. All three planted defects were caught, so the run counts as valid.
Every quote was located verbatim in the document, so nothing was discarded as hallucinated. 156
findings survived at severity definite or likely.

146 of them are C1. Mapping each finding's quote and its `duplicate_of` back to the requirement heading
above it splits those 146 the same three ways the precheck splits.

- 71 sit inside one requirement.
- 67 put one span in the glossary and the other in the body.
- 8 cross two requirements.

The judge's dominant pattern is structural, and its own summary names it: a requirement's `**Context:**`
block states the claims its numbered criteria then state again as *shall* sentences. The second family
is a glossary entry and the criterion that owns the same rule.

Two instruments built on different principles agree on the shape of the sentence layer. The precheck
splits 75 / 31 / 13 and the judge splits 71 / 67 / 8, and both put the cross-requirement slice last.
The requirement-level count below is 39, which is larger than either instrument's cross-requirement
slice. That gap is the measurement's central result.

The judge's 8 cross-requirement pairs were each read at the criteria level. Two confirm pairs found by
hand. Six were new, and all six are folded into the count below.

## Question one — how many requirements state a fact another requirement already states?

**39 pairs, with 20 more close.**

### Method

A pair counts when a criterion of one requirement states a fact a criterion of the other already
states, so a reader who has read the first learns nothing from the second.

Candidates came from four sweeps, each repeatable.

1. The precheck's 10 distinct cross-requirement pairs, extracted by mapping its line numbers to
   headings.
2. A word-overlap sweep over the 303 titles plus their user stories, keeping a pair at Jaccard 0.14 or
   containment 0.30 with at least three shared content words. It returned 57 candidates.
3. An anchor sweep. Every criterion carries bracket codes. Grouping criteria by code shows which
   requirements cite one rule. 386 distinct codes appear on criteria, and 193 of them are cited by
   three or more requirements. A code cited widely marks a fact with many homes.
4. The judge run's 8 cross-requirement C1 findings, located by matching each quote back to its line.

Every candidate was then read at the criteria level, and a pair was kept only where two criteria carry
the same duty.

### The confirmed pairs

**The forward-binding rule — Requirement 48 with fifteen partners. 15 pairs.**

Requirement 48 states the convention: a rule governs from the first landing that touches its surface,
and what already landed stays as it landed. Its own criterion 3 gives every duty that binds forward one
instruction — cite this law, and leave the words of it here. Its criterion 4 makes a bare citation with
no root the finding.

Twenty-one requirements cite the code INV-159 on a criterion. Fifteen of them restate the rule in their
own words while citing it.

| Partner | The sentence that restates it |
| --- | --- |
| R44 | leaving rows that landed before it as they landed |
| R47 | require no retroactive kind on a row queued before the kind axis existed |
| R57 | owe a landed feature its walk at the first landing that touches it |
| R68 | leave records written before the class was declared unreshaped |
| R76 | bind both sentences forward from features specified after this rule |
| R104 | add a clause's pointer at the first landing that touches it, never retroactively |
| R116 | leave members declared before the class unreshaped |
| R123 | the duty shall bind forward from the first landing that touches the architecture |
| R124 | a project predating these layers shall bring them up as an owned landing |
| R209 | bind it forward from its own reach rather than over rows already delivered |
| R262 | have a new scenario state its edges from the first draft |
| R265 | a surface that predates it carry the read at the first landing that touches it |
| R266 | from the first draft for a new surface, at the first touching landing for an older one |
| R267 | the bodies that predate this rule standing as they are cited |
| R275 | the members named before the class standing as they are cited |

The remaining six citing requirements — R88, R121, R122, R188, R193 and R48 itself — cite without
restating, which is the behaviour Requirement 48 asks for.

**The green-line reach rule — Requirement 282 with three partners. 3 pairs.**

Requirement 282 states that a gate in this family prints a green line naming what it read. Requirement
284 criterion 4, Requirement 285 criterion 3 and Requirement 288 criterion 5 each carry the phrase
"state its reach on the green line" again, each citing INV-269 beside its own code.

**The config-health check — Requirements 270, 271 and 275. 3 pairs.**

Requirement 270 holds an installed hook to its source. Requirement 271 holds an installed skill to its
source. Requirement 275 declares the class both belong to, and its criteria 3 and 5 restate what 270
and 271 already state.

Requirements 270 and 271 duplicate each other twice over. Both state that the check reads the whole
source directory against the installed set. Both state that a copy with no pack source is left alone.
Both state that a continuous-integration checkout stands the check down. Criterion 4 of Requirement 271
even names the carve-out as a single one, which confirms that the two requirements describe one check.

**A derivable question is done, never asked — Requirements 21, 72 and 211. 3 pairs.**

Requirement 21 criterion 2 turns a question the agent can answer into work done. Requirement 211
criteria 3 and 4 surface only what cannot be decided without the human, and never park derivable work.
Requirement 72 criterion 3 moves every task it can and reserves a question for what it genuinely cannot
decide. One duty, three homes.

**Requirements 71 and 72 — the tagged default. 1 pair.**

Both state that the walk takes the call itself, writes it with its `[default]` tag, names it in the
delivery report, and owes no re-ask. Requirement 71's object is a taste call and Requirement 72's is a
numeric knob.

**Requirements 78 and 241 — proceeding on the recommendation. 1 pair.**

Requirement 78 criterion 1 proceeds on the recommended option while a question stays open. Requirement
241 criterion 1 proceeds on the default the work took while the question waits on the board.

**Requirements 37 and 38 — preemption belongs to the bug door. 1 pair.**

Requirement 37 criterion 1 lets only the bug door preempt the in-work lane. Requirement 38 says it
twice more, in criterion 1 and again in criterion 2.

**Requirements 80 and 89 — the lane cap. 1 pair.**

Requirement 80 criterion 1 holds the profile-declared cap with a package default of three. Requirement
89 criterion 1 holds the cap at three by the package default and by the profile line.

**Requirements 54 and 55 — a law with no net. 1 pair.**

Requirement 54 criterion 4 ranks a declared law naming no net a broken invariant. Requirement 55
criterion 2 ranks a law with no named net a broken invariant.

**Requirements 210 and 216 — the brief-owed read. 1 pair.**

R210 criterion 4: dispatch the brief-owed read of the files a change will touch to the reader worker
whose distillation returns the per-file lines, or make it a bounded decide-read for a small edit.
R216 criterion 3 says the same sentence with "three" added before "per-file lines". Both carry
INV-53 and INV-137. Both carry a `[GAP]` line about the same undefined boundary, and R216's gap line
opens with "at this second occurrence either", so the document already records the duplication.

**Requirements 12 and 50 — the mandatory sentences. 1 pair.**

Requirement 12 criterion 3 keeps every cut clear of the regression fences, a kept surface's facets, the
non-goals, and the success measure. Requirement 50 criterion 4 repeats that same list inside a
parenthesis.

**Requirements 252 and 253 — one new inbox file. 1 pair.**

Both state that a deposit is one new file naming its source, that it never edits an existing file, and
that it therefore races nothing.

**Requirements 141 and 256 — the inbox push carve-out. 1 pair.**

R141 criterion 3: when a push's diff is exactly one new file under `inbox/`, the system owes the fence
and no re-check record. R256 criterion 7 says it again with "inbox file" for "file under `inbox/`".
This pair is one the precheck caught, at containment 0.94.

### The six pairs the judge added

Each was read at the criteria level before it was kept.

**Requirements 5 and 287 — a closed row moves to the archive.**
R5 criterion 1: when a row closes with a terminal exit — landed, declined, or superseded — move it to
the queue archive in the same commit that closes it, carrying it verbatim. R287 criterion 1 states the
same three exits, the same verbatim move, and the same closing commit.

**Requirements 5 and 94 — the far tier.**
R5 criterion 5 stands the far tier down by name in the runnable report. R94 criterion 3 stands the far
tier down by name in the what's-left report. The pair duplicates twice over: R5 criterion 4 and R94
criterion 1 both define a far row as one kept with no revisit trigger and no plan to run.

**Requirements 43 and 44 — the footprint note.**
R43 criterion 2 writes the footprint in the row's footprint note beside the door, kind, and map notes.
R44 criterion 1 writes it in the landing row's footprint note beside the door, kind, and map notes, and
repeats R43 criterion 1's three values as well.

**Requirements 85 and 90 — what git refuses.**
R85 criterion 2 relies on git refusing every other worktree's attempt to check out, force, or push to a
branch a tree holds checked out. R90 criterion 1 relies on git refusing every other worktree's
checkout, branch-force, and push against a branch a tree holds checked out.

**Requirements 110 and 172 — a donor-specific constant.**
R110 criterion 2 records a donor-specific constant as a named entry in the engine's content contract
with a test that the engine works without it. R172 criterion 6 records it as a named content-contract
entry with a test that proves the engine works without it. Both carry INV-79.

**Requirements 219 and 220 — who moves the pressure setting.**
R219 criterion 1 holds `budget.pressure` as one setting moved only on the human's word. R220 criterion
5 moves `budget.pressure` only by the human's word.

### The close pairs, with both readings

Twenty more pairs are close. Each is stated with the reading that counts it and the reading that does
not.

- **R21, R211 and R72 each against R212** (3 pairs). R212 re-tests a deferral marker for derivability
  and gives a derivable item to the seat. Counted: this is the derivable-question duty a third time.
  Not counted: R212's trigger is a parked backlog item, and the others trigger on a question about to
  be asked.
- **R71 against R211** (1 pair). R211 criterion 1 reports a decided default with its `[default]` tag.
  Counted: the tag-and-report duty again. Not counted: R211's object is any derivable decision.
- **R21 against R35** (1 pair). R35 criterion 1 asks with a chosen recommendation. Counted: R21
  criterion 3 already requires the recommendation. Not counted: R35 criterion 2 says it sharpens the
  rule for a taste call, and it adds mined exemplars and citations.
- **R37 against R160** (1 pair). Counted: both order waiting bugs critical first. Not counted: R160
  cites INV-12 for the ordering and leaves that code's conditions unrepeated.
- **R116 against R54 and against R55** (2 pairs). Counted: a class member naming no net is a defect,
  which is R54 criterion 4 and R55 criterion 2. Not counted: R116's population is the suite-honesty
  class and the others' is the declared cross-cutting laws.
- **R252 and R253 each against R254** (2 pairs). R254 criterion 1 converts a stranger Issue into one
  committed inbox file naming its source, touching the inbox alone. Counted: the one-new-file duty a
  third time. Not counted: R254 adds the bridge from a public tracker.
- **R228, R246, R249 and R292, all six pairs among them** (6 pairs). One law: a net counts only once it
  has been proven able to fire. R228 criterion 6 proves a project-side check red-first on a planted
  defect. R246 criteria 5 and 6 require a red-first proof per pushed gate letter. R249 criterion 1
  requires a skill eval proven red without the skill. R292 criteria 1 and 2 run each session hook
  against a fixture built to fire it. Counted: one law, four times. Not counted: four populations, four
  fixture kinds, and a context in R292 that cites the push side and leaves its words there.
- **R283, R286 and R289, all three pairs** (3 pairs). Each states that its document follows the family
  genre by reference to `docs/spec-format.md` and restates none of the laws. Each states the family's
  one-delivery arming rule. Counted: the arming rule and the by-reference rule are family facts, and
  each member repeats both. Not counted: the subject differs per member, so the sentences differ.
- **R278 against R284** (1 pair). Both state that a generated section is output only, that a hand edit
  is caught, and that the gate reds a body-to-table disagreement in either direction. Counted: one law
  over two artifacts. Not counted: R284's context cites R278's table as its model.

### What the number does not reach

Thirty-nine is a floor and the sweep behind it is partial. Six of the thirty-nine arrived from an
instrument added last, which is itself evidence that more remain.

The anchor sweep is the instrument that found the two largest classes, and it was run to completion on
two codes: INV-159 and INV-269. 193 codes are cited by three or more requirements, so 191 remain
unaudited. On the two audited, restatement ran at 15 of 21 citing requirements and at 3 of 10. A
straight extrapolation is unreliable. Most codes carry far fewer citations, and many of them name an
entity, which has no rule to restate.

The honest statement is this: the requirement-level number was not reached exhaustively, and it cannot
be by hand at 45,753 pairs. What was reached is 39 confirmed pairs and a set of repeatable instruments
that keep finding more.

## Question two — how many requirements share a shape one requirement could carry with a parameter?

**12 groups, holding 51 distinct requirements.**

### Method

Requirements were grouped by the shape of the user story and the criteria: the same actor, the same
duty, and the same consequence, with one slot filled differently per member. A group counts at three or
more members. Members were read at the criteria level before the group was kept.

### The groups

**1. The format-family member. R283, R286, R289.**
Shape: document D is a family member, follows the family genre by reference to `docs/spec-format.md`
restating none of its laws, opens with a preamble then its own body shape then its generated tables,
and converts under the family's one-delivery arming rule.
Parameter: the document, and the shape of its body.

**2. A generated section built from the body. R148, R278, R284.**
Shape: section S is built from body B at freeze, is output only, and a gate reds a hand edit or a
disagreement between S and B.
Parameter: the generated section and the body it reads.

**3. A row carries a field, and a check reds a row missing it. R44, R209, R285, R288.**
Shape: every row of document D carries field F, and a mechanical check reads every row and reds one
missing F, naming the row.
Parameter: the document, the field, and the check.

**4. A net counts only once proven able to fire. R228, R246, R249, R292.**
Shape: each member of net population P is classified with a fixture that drives it to a live failure,
and a member that stays silent against its fixture is named and fails the run.
Parameter: the population, and the fixture kind it fires on.

**5. An installed copy is held to its pack source. R270, R271, R273, R275.**
Shape: artifact kind K lives twice, its source in the pack and a running copy on the host, and a named
check reds the running copy going stale.
Parameter: the artifact kind and its check. Requirement 275 already declares this parameter and
enumerates four members, and Requirements 270 and 271 still stand as full requirements of their own.

**6. A class declares its member and binds forward. R68, R116, R263, R264, R266, R267, R275.**
Shape: this requirement is the named member of family F; a new member states its own answer against the
family's parity; members declared before the class stand unreshaped.
Parameter: the family, the member's name, and the parity each member owes.
This is the largest group, and its closing sentence is near-identical across the composition-lens
members. Requirement 263 criterion 9, Requirement 264 criterion 5 and Requirement 266 criterion 9 differ
only in the member name.

**7. The walk takes the call, tags it, tells it, and never re-asks. R71, R72, R211, R241.**
Shape: when the walk meets choice of kind C, it decides, writes the choice with its `[default]` tag,
names it in the delivery report with what the reader needs to judge it, and owes no re-ask.
Parameter: the kind of choice, and what the report names beside it.

**8. Founding declares an attribute and records it in one home. R170, R171, R172, R173, R174, R175.**
Shape: at founding, attribute A is asked outright or proposed, the human's word decides, and the answer
is recorded in one home so later machinery runs against a stated value.
Parameter: the attribute — the shaping questions, the personal profile, the engine split, the project
kind, the concrete layers and proof kinds, the design principles.

**9. A lens runs by construction on a named spec trigger. R62, R63, R64, R65, R66.**
Shape: when a spec-delta carries trigger T, lens L runs by construction, and the blank it exposes
becomes a finding before code.
Parameter: the trigger and the lens.
The spec names this group itself. Requirement 65 criterion 3 reads the motion-parity lens as this lens
on an exit's animation and the entry-state lens as this lens on a re-entry's internal state, calling
both instances the parent generalizes. Those two lenses are Requirement 62 and Requirement 64, and each
still stands as a full requirement of its own.

**10. A chat arm reds a named offence in the seat's replies. R19, R231, R232, R293, R294.**
Shape: offence O in text the person reads is caught by a cheap literal net, with the register judge
holding the class in any phrasing.
Parameter: the offence and its literal net.

**11. An inbox arm deposits exactly one new file. R252, R253, R254.**
Shape: arm A deposits one new inbox file naming its source under its own safe path, touches the inbox
alone, edits nothing, and therefore races nothing.
Parameter: the arm — the outside depositor, the remote seat, the co-located session, the stranger
bridge.

**12. A cleanup is scoped to what the run owns, and says what it ended. R114, R117, R234, R235.**
Shape: process kind K is ended only where the run provably owns it, the ownership proof is named, and
the ending is announced in one line.
Parameter: the process kind and its ownership proof. Requirement 114 is the loosest fit, because its
subject is the browser harness and the ownership rule is one of eight criteria.

### A note on the glossary's own shapes

The same pattern runs inside the glossary. Four entries — `requirements format`, `architecture format`,
`roadmap format`, `test-matrix format` — share one sentence shape with the document as its parameter.
Two more, `cadence` and `staleness bound`, are the producer's and the consumer's copy of one sentence.
Question three's close calls carry these, so they are left out of the count above.

## Question three — how many glossary entries name the same thing twice under two words?

**4 pairs, with 6 more close.**

### Method

All 250 entries were extracted. Two sweeps ran over them.

1. A word-overlap sweep over the definitions, keeping a pair at Jaccard 0.25 or containment 0.45 with
   at least three content words each side. It returned 26 candidates.
2. A reading of the 250 term names for near-synonyms, grouped into 25 clusters and read in full. This
   sweep is what the first one cannot do, because two names for one thing can be defined in disjoint
   words.

A pair counts when both entries denote one referent.

### The confirmed pairs

**`monitor` and `stranger-wish monitor`.**
The scheduled script that bridges each open issue a stranger filed into one committed inbox file, and
the scheduled process that converts each open stranger Issue or Discussion into one committed inbox
file. One referent, two entries. The body uses the short name nine times and the long name once. This
is a direct break of the spec's own one-name-per-thing law.

**`milestone` and `milestone gate`.**
A milestone is defined as a rhythm point where the whole spec and architecture are re-proven, the design
review runs, and the full gate list completes. A milestone gate is defined as the whole-spec pass that
re-proves the spec and the architecture, runs the design review, and completes the full gate list. The
three actions are identical.
The close reading: a point in the rhythm and the pass that runs at it could be two things. As the
entries stand, the point is defined only by the pass.

**`catch-up` and `catch-up walk`.**
The sequence that brings an already-adopted host onto the pack's current version, and the ordered set of
steps a session walks to run catch-up on an adopted host. A sequence and an ordered set of steps are one
thing.

**`leg` and `open leg`.**
A leg is one of the separately-accepted parts a multi-part row still carries, each with its own
Done-when acceptance. An open leg is a leg whose own Done-when acceptance has not yet been met. The
phrase "still carries" in the first entry already means not yet met.
The close reading: `leg` could be read as any part, met or open, which would leave `open leg` its own
work. The entry's own wording closes that reading.

### The close pairs, with both readings

- **`milestone gate` and `release gate`.** Counted: both are the full prover re-prove over the spec and
  the architecture. Not counted: the release gate adds a dated clean-context review record, and the
  milestone gate adds the design review and the gate list.
- **`description field` and `named reference`.** Counted: both name a code paired with its plain
  statement. Not counted: one names where the statement lives and the other names the pairing a reader
  meets. Requirement 278 criterion 7 retires the description-field gate, so this entry may be describing
  a mechanism that has gone.
- **`freshness check` and `config-health check`.** Counted: both compare an installed copy against its
  pack source. Not counted: one compares version strings and re-reads, the other diffs bytes and reds.
- **`rendered page` and `transient page`.** Counted: the identifying mark given for a transient page is
  exactly the mark given for a rendered page. Not counted: the transient page adds "built for one
  reading and cleared to the attic".
- **`narration` and `status report`.** Counted: both are defined as "the running account". Not counted:
  one is spoken live between the capture echo and the delivery report, the other is a view a session
  keeps.
- **`slot` and `weak word`.** Counted: each is defined through the other, so the pair states one idea
  twice. Not counted: a slot and the word that opens it are two things.

### Two redundancies inside the glossary that are not two-name pairs

`priority bubble` closes with a sentence that restates the whole `priority` entry. `delta record`
restates the four words the `delta kind` entry defines. Both are one fact in two entries, and in each
the two terms denote different things, so neither counts under question three.

### What the existing one-name gate reaches

`guardrails/check-one-name.py` passes green on `PRODUCT_SPEC.md` today. Its green line reads: matched 0
of 13 rows scanned, no known alias present across 13 aliases of 5 artifacts.

The gate compares the document against a hand-kept alias list in `guardrails/one-name-aliases.json`.
That list holds 5 artifacts. None of the four confirmed pairs above is in it, and the gate's own header
says a two-name drift the list does not know is outside its reach.

So the one mechanical check the spec has against naming one thing twice covers 5 of the 250 entries. It
prints green over a glossary holding at least four two-name pairs.

## What the numbers say the mechanism against growth has to do

The measurement says four things about what has to be built.

**The mechanism must judge a pair of requirements.** The largest class found — fifteen restatements of
one convention — shares no wording. Every sentence-level instrument the project owns misses it. The
precheck reaches 5 of the 39 confirmed pairs, and the judge run reaches 8. Both instruments spend most
of their output on the sentence layer inside one requirement, where the precheck reports 75 pairs and
the judge 71.

**Two layers below the requirement layer already have numbers, and they need an owner too.** The judge
puts 71 findings inside single requirements and 67 between the glossary and the body. The precheck puts
75 and 31 in the same two places. Neither layer is question one's subject, and both are large enough
that the campaign should name who fixes them. The Context block restating its own criteria is one
mechanical class, and a glossary entry restating the criterion that owns its rule is another.

**The bracket code is the instrument that already works.** The anchor sweep found both large classes,
and it costs one pass over the criteria. A code cited by many requirements marks a fact with many homes.
193 codes are cited by three or more requirements and 191 of them have never been read for restatement.
A gate that groups criteria by code and puts each group before a judge would reach the class the regex
cannot, at a cost that does not grow with the document.

**The rule against restatement exists and nothing enforces it.** Requirement 48 criterion 3 already
tells every forward-binding duty to cite the law and leave its words alone. Fifteen requirements write
the words out anyway, each one citing the code correctly while doing so. The same holds for the
green-line rule and its three restatements. A correct citation is silent about whether the citing text
added anything, and today nothing reads the difference.

**A gate that measures bytes cannot see any of this.** `check-size-ratchet.py` holds
bytes-per-criterion and may only lower it. Every duplication above is spread across separate
requirements, and each one is short and well written on its own line. Fifteen short restatements pass a
per-criterion byte bound and pass a bytes-per-criterion average. `docs/spec-compaction-protocol.md`
prunes a working skill's restatement of a base-skill rule, which is a different subject from one
requirement restating another.

The measurement's answer to the campaign's question is that the two mechanisms already built do not
reach. What they measure is size. What grows is the number of homes one fact has, and the number of
requirements that differ only in one slot. Twelve shapes hold 51 of the 303 requirements, which is one
requirement in six sitting in a group where one parameterized requirement could carry the whole set.

The design that follows this measurement owes two instruments. One groups criteria by their anchors and
judges each group for a fact stated twice. One groups requirements by the shape of their user story and
criteria, and asks of every group of three or more whether one requirement with a parameter would carry
it. Both are cheap, both are repeatable, and neither exists today.
