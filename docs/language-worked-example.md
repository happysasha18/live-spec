# One documentation page, from first draft to a draft that holds the rules

This page walks one short documentation page through every rule that binds it. The writer's page,
`docs/language-rules.md`, states each rule on its own. This page shows the human-prose roster applied
to one text at once. You get:

- the text as a competent engineer first wrote it;
- the text after the rules were held to it;
- the fix standing between each pair of sentences.

The first draft comes first, quoted whole. The rewrite follows, also quoted whole. Then the walk
takes the fixes in reading order, and each fix names the rule ids it answers.

Both drafts are quoted, so every line inside a quote block is reported material and none of it is this
page's own assertion. The first draft carries the defects on purpose.

## The subject

The drafts describe how a host project installs the pack's checks and what each installed check
refuses. The facts come from `adopt/install-scaffold.sh`, `adopt/install-ratchet.sh`, the four checks
under `scaffold/guardrails/`, and `guardrails.config.json`.

## The draft as it first stood

The writer of this draft had the facts and no rulebook. Nothing in it is labelled, and it is written
to read as a plausible first draft.

> **Installing the pack's checks in a host project**
>
> The adoption of the pack's checks by a host repository is described below. Some background is
> useful before the steps themselves.
>
> Every project that reaches a certain size accumulates documents that drift apart from each other,
> and the pack was built in response to that. INV-97 defines the four project-side checks that are
> vendored into a host tree, and these are what a host runs from its own repository from that point
> onward.
>
> Installation is performed by running the scaffold installer from the host repository root, at which
> point the four checks are copied into the host tree along with their shared library and a README,
> and the host's guardrails config — the JSON file naming the paths the checks read, such as the
> spec, the test folder and the surface registry — is seeded from the example when the host does not
> already carry one.
>
> The four checks are then available. The first refuses a rendered artifact that is missing
> something. The others cover tests, traceability, and structural drift. Each of these is critically
> important.
>
> Tests are checked for by the second gate, which is quite strict: when user-facing files are touched
> and nothing under the tests folder is touched, it complains. This is not a review of the test's
> quality; it is a presence check. NEVER bypass it.
>
> The third gate wants every registry row to cite an anchor, and it refuses anchors the spec does not
> carry. The fourth catches several kinds of structural drift, listed in its own header.
>
> There is also a ratchet installer, which seeds a cap at 100 and reds the suite on growth beyond it.
> Both installers write to the same source pin manifest, which lets the daily update check tell a
> current copy from a stale one, the manifest keys being the pack-relative source paths. An existing
> host settings file is never overwritten.
>
> Of course, one should read the vendored README before the first run. Ask if you want the full list
> of what each gate refuses.

## The draft after the rules were held to it

> **Installing the pack's checks in a host project**
>
> One command installs them. From your repository's root, run `adopt/install-scaffold.sh`.
>
> The installer copies the completeness check, the tests-present check, the traces-to-spec check, and
> the conflicts check into your tree. It copies the library those checks share and a README beside
> them. It writes `guardrails.config.json` from the shipped example when your repository carries
> none, and it leaves a config you already wrote untouched.
>
> That config is where you name your own paths. It tells each check where your spec lives, which
> folder holds your tests, and which file lists your surfaces. That last file is your registry. A
> surface is one named part of what your project shows a reader: a rendered page, a panel, a
> generated report.
>
> Each check refuses one thing.
>
> - The completeness check refuses a rendered page that leaves out a surface your registry lists. It
>   also refuses a surface the page shows and your registry never names.
> - The tests-present check refuses a change that edits a user-facing file and edits nothing under
>   your tests folder. Your config lists which files count as user-facing. This check reads whether a
>   test file changed, and your test matrix decides which cases a test covers.
> - The traces-to-spec check refuses a registry row citing no spec clause. It also refuses a citation
>   pointing at a clause your spec does not carry.
> - The conflicts check refuses these kinds of drift between your documents:
>     - one identifier defined twice in the spec index;
>     - an identifier in the spec index that no matrix row cites;
>     - one line marking a decision as open and as settled at once;
>     - one surface listed twice in your registry.
>
> A second installer, `adopt/install-ratchet.sh`, adds the gates that measure document size and
> repetition. It measures each gated document on the day you run it and records that measurement as
> the cap. Your suite then fails when a document grows past its own recorded cap. A document that
> shrinks passes. Raising a cap means editing the generated test by hand, so every raise appears in a
> diff.
>
> Both installers write into `scripts/ratchet-manifest.json`. Each entry there records the pack
> version a vendored file came from and a hash of that file's content. The daily update check
> compares each hash against the pack's current copy and reports the files that have fallen behind.

## The walk

Each fix gives the sentence before and the sentence after. It names the rule ids it answers, and one
line says what a reader would have done wrong under the original.

### The opening

**Fix 1 — r46, a reply that buries its answer. r14, a sentence carrying no information.**

Before:

> The adoption of the pack's checks by a host repository is described below. Some background is
> useful before the steps themselves.

After:

> One command installs them. From your repository's root, run `adopt/install-scaffold.sh`.

A reader who came for the command read two paragraphs of background before reaching it, and a reader
who stopped at the opening left with nothing.

**Fix 2 — r26, a sentence with no actor, or its action buried in a noun.**

Before:

> The adoption of the pack's checks by a host repository is described below.

After:

> One command installs them.

The act of the sentence sat in the noun `adoption`, so the reader could not tell who runs anything.

### The background paragraph

**Fix 3 — r14, a sentence carrying no information. r44, a paragraph carrying more than one point.**

Before:

> Every project that reaches a certain size accumulates documents that drift apart from each other,
> and the pack was built in response to that.

After: the sentence is cut, and no sentence replaces it.

The paragraph carried the pack's motive and the installer's contents at once. A reader looking for
the contents had to read past the motive.

**Fix 4 — r33, a relational word leaving its slot empty.**

Before:

> Every project that reaches a certain size accumulates documents that drift apart from each other.

After: the sentence is cut.

`a certain size` opened a slot the sentence never filled, so a reader could not tell whether their own
project had reached it.

**Fix 5 — r11, an internal code leading a sentence to the reader.**

Before:

> INV-97 defines the four project-side checks that are vendored into a host tree.

After:

> The installer copies the completeness check, the tests-present check, the traces-to-spec check, and
> the conflicts check into your tree.

A reader outside the project met a code as the sentence's subject and had no way to look it up.

**Fix 6 — r07, a set named by a count instead of given.**

Before:

> INV-97 defines the four project-side checks that are vendored into a host tree.

After:

> The installer copies the completeness check, the tests-present check, the traces-to-spec check, and
> the conflicts check into your tree.

The count told the reader how many checks arrive and left them unable to name one.

**Fix 7 — r39, a pronoun with no antecedent in its own sentence.**

Before:

> …and these are what a host runs from its own repository from that point onward.

After: the clause is cut.

`these` and `that point` both pointed back a sentence, so a reader had to reread to hold the
sentence.

### The installation paragraph

**Fix 8 — r08, a sentence running past its word cap and piling up clauses. r45, a long flat run of
peer items at one level.**

Before, at 71 words:

> Installation is performed by running the scaffold installer from the host repository root, at which
> point the four checks are copied into the host tree along with their shared library and a README,
> and the host's guardrails config — the JSON file naming the paths the checks read, such as the
> spec, the test folder and the surface registry — is seeded from the example when the host does not
> already carry one.

After, as four sentences of 20 words or fewer:

> From your repository's root, run `adopt/install-scaffold.sh`.
>
> The installer copies the completeness check, the tests-present check, the traces-to-spec check, and
> the conflicts check into your tree. It copies the library those checks share and a README beside
> them. It writes `guardrails.config.json` from the shipped example when your repository carries
> none, and it leaves a config you already wrote untouched.

A reader lost the subject halfway through and could not cite any one part of the sentence on its own.

**Fix 9 — r26, a sentence with no actor. r25, the person an explanatory sentence speaks in.**

Before:

> Installation is performed by running the scaffold installer from the host repository root.

After:

> From your repository's root, run `adopt/install-scaffold.sh`.

The passive hid the person doing the work, so a reader could not tell whether the installer runs
itself.

**Fix 10 — r01, an ordinary word carrying a private project meaning. r08, a sentence carrying a
definition.**

Before:

> …the host's guardrails config — the JSON file naming the paths the checks read, such as the spec,
> the test folder and the surface registry — is seeded from the example…

After:

> It writes `guardrails.config.json` from the shipped example when your repository carries none.
>
> That config is where you name your own paths. It tells each check where your spec lives, which
> folder holds your tests, and which file lists your surfaces.

The definition rode inside the sentence carrying the instruction. A reader following the steps had to
hold a gloss and a step at once.

This fix is one of three places where two rules pulled in different directions. The section `Where
two rules pulled against each other` below states how each was settled.

**Fix 11 — r43, an abstraction standing where a concrete noun would do. r41, an example restating a
rule that was already clear.**

Before:

> …the JSON file naming the paths the checks read, such as the spec, the test folder and the surface
> registry…

After:

> It tells each check where your spec lives, which folder holds your tests, and which file lists your
> surfaces.

`the paths the checks read` named nothing a reader could picture. The three items sat in an aside a
reader skimming the steps would skip.

**Fix 12 — r01, an ordinary word carrying a private project meaning.**

Before:

> …the spec, the test folder and the surface registry…

After:

> That last file is your registry. A surface is one named part of what your project shows a reader: a
> rendered page, a panel, a generated report.

`surface registry` reached the reader with no gloss, so a reader guessed at what a surface is and
carried that guess into the completeness check.

**Fix 13 — r03, a name stacking two nouns with no relation between them.**

Before:

> the surface registry

After:

> the file that lists your surfaces, which is your registry

Two nouns stood together with no word saying how the second relates to the first. A reader could take
it as a registry of surfaces or as a surface belonging to a registry.

### The paragraph introducing the checks

**Fix 14 — r14, a sentence carrying no information.**

Before:

> The four checks are then available.

After: the sentence is cut.

The sentence restated what the previous paragraph had said, and the reader lost nothing when it went.

**Fix 15 — r43, an abstraction standing where a concrete noun would do. r62, a sentence hiding what
it leaves out.**

Before:

> The first refuses a rendered artifact that is missing something.

After:

> The completeness check refuses a rendered page that leaves out a surface your registry lists. It
> also refuses a surface the page shows and your registry never names.

`missing something` left the reader guessing what the check reads, and the second direction of the
check was invisible.

**Fix 16 — r07, a set named by a position instead of given.**

Before:

> The first refuses… The others cover tests, traceability, and structural drift.

After: each check is named where it is described, under its own bullet.

A reader had to count the checks in an earlier sentence to work out which one `the third gate` meant.

**Fix 17 — r12, a word grading how important a thing is. r39, a pronoun with no antecedent.**

Before:

> Each of these is critically important.

After: the sentence is cut.

The sentence told the reader how much to care and gave them nothing to care about, and `these`
pointed back a sentence.

### The tests-present check

**Fix 18 — r26, a sentence with no actor.**

Before:

> Tests are checked for by the second gate.

After:

> The tests-present check refuses a change that edits a user-facing file and edits nothing under your
> tests folder.

The actor arrived after the action, so the reader met the rule before meeting the thing that holds
it.

**Fix 19 — r32, a judgment with no judge and no measure. r33, a relational word leaving its slot
empty.**

Before:

> …the second gate, which is quite strict…

After: the clause is cut, and the check's own condition stands in its place.

`quite strict` named no measure and no judge, so a reader could not tell what the check refuses.

**Fix 20 — r05, a predicate applied to a subject that cannot carry it. r62, a sentence hiding what it
causes.**

Before:

> …when user-facing files are touched and nothing under the tests folder is touched, it complains.

After:

> The tests-present check refuses a change that edits a user-facing file and edits nothing under your
> tests folder.

A check complains the way a person complains, and a reader could not tell whether their commit stops
or a note appears.

**Fix 21 — r43, an abstraction standing where a concrete noun would do.**

Before:

> …when user-facing files are touched…

After:

> …a change that edits a user-facing file… Your config lists which files count as user-facing.

`user-facing files` named a class the reader could not enumerate, and the sentence that names where
the list lives now stands beside it.

**Fix 22 — r10, a thing named by denying its neighbour. r27, an opener saying what a thing is not.**

Before:

> This is not a review of the test's quality; it is a presence check.

After:

> This check reads whether a test file changed, and your test matrix decides which cases a test
> covers.

The denied half gave the reader nothing they did not already have, and the sentence opened on the
thing the check is free of.

**Fix 23 — r23, a word standing in all capitals.**

Before:

> NEVER bypass it.

After: the sentence is cut.

The capitals carried the force the sentence had no fact to carry, and a reader still did not know
what a bypass would be.

### The remaining two checks

**Fix 24 — r05, a predicate applied to a subject that cannot carry it.**

Before:

> The third gate wants every registry row to cite an anchor.

After:

> The traces-to-spec check refuses a registry row citing no spec clause.

A check wanting something reads as a check with a preference, so a reader could not tell whether the
citation is required.

**Fix 25 — r01, an ordinary word carrying a private project meaning.**

Before:

> …to cite an anchor, and it refuses anchors the spec does not carry.

After:

> …citing no spec clause. It also refuses a citation pointing at a clause your spec does not carry.

`anchor` is this project's word for a bracketed identifier in a spec, and a reader outside the project
read it as a link target.

**Fix 26 — r07, a set pointed at by a count. r62, a sentence hiding what it leaves out.**

Before:

> The fourth catches several kinds of structural drift, listed in its own header.

After:

> The conflicts check refuses these kinds of drift between your documents:
>
> - one identifier defined twice in the spec index;
> - an identifier in the spec index that no matrix row cites;
> - one line marking a decision as open and as settled at once;
> - one surface listed twice in your registry.

The sentence promised a list it never gave and sent the reader to a file header to find it.

**Fix 27 — r33, a relational word leaving its slot empty.**

Before:

> several kinds of structural drift

After: the four kinds are listed.

`several` opened a slot the sentence never filled, and a reader could not tell whether the check
covers their case.

### The second installer

**Fix 28 — r02, a coined word standing where a plain standard word exists.**

Before:

> There is also a ratchet installer, which seeds a cap at 100 and reds the suite on growth beyond it.

After:

> A second installer, `adopt/install-ratchet.sh`, adds the gates that measure document size and
> repetition. Your suite then fails when a document grows past its own recorded cap.

`ratchet` is this project's name for a limit that never rises, and `reds` is its word for a failing
check. A reader outside the project met two words their own vocabulary does not hold.

**Fix 29 — r06, a number standing with no ground.**

Before:

> …seeds a cap at 100…

After:

> It measures each gated document on the day you run it and records that measurement as the cap. Your
> suite then fails when a document grows past its own recorded cap. A document that shrinks passes.

`100` carried no unit, no comparison, and no direction, so a reader could not tell whether a larger
number is better or worse.

**Fix 30 — r03, a name stacking nouns with no relation between them.**

Before:

> Both installers write to the same source pin manifest.

After:

> Both installers write into `scripts/ratchet-manifest.json`.

Three nouns stood together with nothing between them, so a reader could not say what pins what.

**Fix 31 — r20, English that reads as compressed. r26, a sentence with no actor.**

Before:

> …which lets the daily update check tell a current copy from a stale one, the manifest keys being
> the pack-relative source paths.

After:

> Each entry there records the pack version a vendored file came from and a hash of that file's
> content. The daily update check compares each hash against the pack's current copy and reports the
> files that have fallen behind.

The closing clause had no subject and no finite verb, so a reader reached the end of the paragraph
holding a phrase that stated nothing.

**Fix 32 — r04, one thing answering to a second name. r56, one fact stated a second time in another
place.**

Before:

> An existing host settings file is never overwritten.

After: the sentence is cut, and the fact stands once, earlier:

> …it leaves a config you already wrote untouched.

The same file was called the guardrails config in one paragraph and the settings file in another. The
rule about that file was stated twice, so a reader counted two files and two rules.

### The closing paragraph

**Fix 33 — r15, a word inflating a statement while adding nothing. r25, the person an explanatory
sentence speaks in.**

Before:

> Of course, one should read the vendored README before the first run.

After: the sentence is cut.

`Of course` added nothing the sentence did not carry, and `one` held the reader at a distance from
their own act.

**Fix 34 — r48, an offer to do work the writer could already derive.**

Before:

> Ask if you want the full list of what each gate refuses.

After: the list stands in the page, under `Each check refuses one thing.`

The writer had the list in hand and offered to hand it over on request, so a reader had to ask for
something already written.

## Where two rules pulled against each other

Three sentences met two rules that wanted opposite things. Each is settled here, so a writer meeting
the same pair does not have to settle it again.

**A term's first-use definition against the ban on a definition inside a rule-carrying sentence
(r01 against r08).** The guardrails config needed a gloss at its first use, and r08 refuses a
definition inside a sentence that carries a rule. The gloss takes its own sentence, placed before the
sentence carrying the instruction. Both rules then hold: the reader meets the picture first and the
instruction second.

**The opening that carries the answer against the cut of a sentence that adds no fact (r46 against
r14).** r46 asks the page to open with the answer, and r14 cuts a sentence that only announces what
follows. `One command installs them` carries a fact: the install takes one command. So it stands. A
lead reading `This page explains how to install the checks` would carry no fact and would be cut.

**Grounding an abstraction with an example against cutting an example that resolves no ambiguity
(r43 against r41).** r43 asks for a two- or three-item example at an abstraction's first use, and r41
refuses an example that restates a rule already clear. The three paths named after `the paths the
checks read` are the abstraction's grounding, so they stay. They move out of the dash aside into the
sentence that names what the config does, where a reader skimming the steps still meets them.

## The count

The human-prose roster binds 39 rules. On this page they fell into three groups.

**Fired on a sentence: 29.** r01, r02, r03, r04, r05, r06, r07, r08, r10, r11, r12, r14, r15, r20,
r23, r25, r26, r27, r32, r33, r39, r41, r43, r44, r45, r46, r48, r56, r62.

**Held over the page with no sentence to fix: 5.** r09 binds this page as a whole, since a page that
teaches these rules is the first test of them. r18 pins the page to English. r53 and r54 name process
steps, so no single sentence carries them. r53 asks for a first draft from a writer with no rules
loaded. r54 asks for cold readings until two in a row return nothing blocking. r61 binds the walk's
own shape, since
each fix names the class of mistake standing behind its instance.

**Never came up: 5.** r13 grades the person or the writer's own act, and the drafts address neither.
r49 covers a mistake expanded into a self-audit, and neither draft owns a mistake. r50 covers an
unmarked working note or a closed set of options, and neither draft offers a choice. r52 covers the
session's task list, which no documentation page carries. r57 covers a phrasing the human cut
returning in a later draft, and this pair of drafts has no review history behind it.

Twenty-nine rules fired on one draft of 344 words. A writer who runs the roster as a checklist walks
all 39 items. The 34 fixes above sit in the draft's eight paragraphs, because the defects cluster. One
sentence in the first draft broke five rules at once. It ran past the word cap, buried a definition,
hid its actor, left an abstraction ungrounded, and skipped an example. Reading the roster in id order
before writing puts the rules in the writer's hand while the sentence is still forming. The sentence
then arrives already holding five of them.
