---
name: text-audit
description: Use to check any human-facing text — README, spec, copy, article — for places a first-time reader stops, then repair them.
metadata:
  version: 4.3.0
---

# text-audit — read a text as a stranger, fix where they stop

> Part of the **live-spec pack**. The shared working rules live once in the pack's base skill,
> `live-spec-base` (v4.3.0), whose file is `skills/live-spec-base/SKILL.md`. Four scopes settle a
> setting there, in this order: the session's live word, then the host profile, then the personal
> profile, then the package default. This skill points at those rules and covers only its own subject.
> Used on its own, this skill is plain advice a person applies by hand, and "The by-hand mode" below
> states what that mode covers.

This skill checks whether a stranger understands a text, and repairs the places where they stop.

**Where the paths in this file point.** Two trees are in play. The named files under `guardrails/`,
`scripts/`, and `skills/` are the live-spec pack's own, at `github.com/happysasha18/live-spec`. So
are the design notes this page names by filename under `docs/`. An install copies each skill folder
into one place, so a path naming another skill points to that skill's folder, beside this skill's
folder. A path opening with `references/` names a file in this skill's own folder, beside this file.
The dated pages under `docs/skill-review/`, `docs/plans/`, `docs/reports/`, and `docs/language-reads/`
are the live-spec repository's own records, cited here as evidence. Every other path belongs to the
project whose text is under audit, including `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, and
`TEST_MATRIX.md`.

A **cold reader** meets the text with no knowledge of its history. It holds no earlier draft, no
author's intent, and no project background beyond the words on the page. Inside the pack a cold reader
is a fresh session, which is one conversation with a model started empty. By hand it is a person who
has not read the text before.

An author cannot be their own cold reader. The author holds the context the text is missing, so the
author reads a meaning a stranger cannot reach. This skill supplies the prompt that turns a fresh
session, or a person, into that stranger. The prompt stands at
[`references/reader-prompt.md`](references/reader-prompt.md).

The reading step runs two cold readers over the same text, and both run every time. One works under
the printed rule list at [`references/reader-prompt.md`](references/reader-prompt.md). One works
under [`references/unprompted-reader-brief.md`](references/unprompted-reader-brief.md), which hands
over the text, the reader it is written for, and the task.

This skill runs on any text a person will read: a spec section, a README, a decision page, marketing
copy, an article, a release note.

The loop came from the comprehension gate on spec sections, recorded in `docs/spec-format.md`. A
comprehension gate is a check a changed section passes before it ships, and it reads whether a stranger
understands that section. That gate runs the mechanical lints first, then fresh cold readers. A finding
**blocks** when the reader could not go on, or would have applied the text wrongly.

Those readers found new blocking terms on every pass, and the terms already repaired stayed repaired.
The findings reached zero only after two reads in a row returned nothing that blocks. Every reading is
written to a dated **reading record** under `docs/language-reads/`, and by hand that record sits beside
the audited text. The reading record holds one reading's full output: every stop it reported and any
check that did not run. `docs/language-defects.md` is the record of why each language rule says what
it says. It carries the stops those readings left standing, sorted into the ones both readings made
and the ones one reading made alone. A stop one reader found alone still blocks when it meets that
test. Step 3 of "The loop" orders those blocking stops after the stops both readers found. This skill
packages that loop for any text.

## The roles and the words this skill uses

Three roles run through this skill, and two readers fill the cold reader role in every round. One
person may hold the auditor role and own the text, and the cold reader is never either of them.

- **the auditor** — the session running this skill. It runs the lints, briefs both cold readers,
  merges what they return, and writes the fixes.
- **the cold reader** — the fresh reader defined above. It reports where it stopped, and it repairs
  nothing. Each reading round fills this role twice, with the two readers named below.
- **the prompted reader** — a cold reader working under the printed rule list at
  [`references/reader-prompt.md`](references/reader-prompt.md).
- **the unprompted reader** — a cold reader holding the text, the reader it is written for, and the
  task. It holds no rule list and no project background. Its brief stands at
  [`references/unprompted-reader-brief.md`](references/unprompted-reader-brief.md).
- **the person** — whoever owns the text: its author, or whoever asked for the audit and answers for
  the text's intent.

A **surface** is a kind of text. One file carries several kinds at once: the numbered requirements of a
spec are one kind, and the prose paragraphs beside them are another.

The live-spec repository names six surfaces: a spec body, human prose, chat, a published artifact, a
commit message, and a worker brief.

**The auditor names the text's one primary surface**, reading it against the surface list in
`guardrails/language-rules.json`. A text published to someone outside the project carries the artifact
surface as well. Every rule that binds either surface is then in force.

This skill runs on a text standing on any surface a person reads. It holds that text to the register of
the text's own primary surface. A README, a report, a decision page, and a skill body stand on human
prose. Marketing copy, an article, and a release note stand on the artifact surface, which covers any
page published outside the project. A numbered requirement stands on the spec body, and the section
"Running it on a spec section" covers that surface.

The **register** of a surface is the set of writing rules its text is held to. It settles which words a
text takes, which sentence shapes it holds, and how it addresses its reader. The register carries the
word cap: 25 words for a human-prose sentence, and 35 for a spec-body criterion (rule `r08`).

The human-prose register is printed at
[`references/human-prose-rules.md`](references/human-prose-rules.md).

A **class** is the shape of a mistake: the form it takes wherever it turns up. One rule names one class,
and a stop in one place stands for that class everywhere else.

`guardrails/language-rules.json` is where three things are edited: the six surfaces, the three words
defined above (surface, register, and class), and every rule of every register.

## When it fires

Load this skill when a human-facing text is about to ship and its clarity matters:

- a README before a push;
- a spec section after an edit;
- a decision page before it goes to the person;
- a piece of marketing copy or an article draft.

The trigger is a person asking whether a reader will understand the text: "audit this", "cold-read this",
"is this clear", "will a stranger get this".

## Work that belongs elsewhere

- **A design review of a spec** belongs to design-reviewer, at `skills/design-reviewer/SKILL.md`. That
  pass judges the design behind the words: whether similar features behave one way, and which
  same-kind items the spec left ungrouped. This skill
  reads whether the words land on a stranger, and it invents no answer about the design. The two passes
  read different failures on the same page, so run each one for the failures only it finds.
- **An argument with a spec's claims** belongs to product-prover, at
  `skills/product-prover/SKILL.md`. That pass hunts a missing state, a false invariant, and an
  unhandled transition. This skill reads the words, and it judges no claim the spec makes.
- **Taste and voice** stay with the person, and with whatever writing skills the host installs beside
  the pack. This skill holds a text to the register of its surface, and it reports where a reader stops.
  It grades no voice, and it rewrites no style beyond those rules.
- **Machine-read text** needs no cold reader, because no stranger returns to it. A worker brief, a
  checkpoint, and an internal note are machine-read.

## The loop

The audit runs in five steps. A reading round is one pass by each of the two readers. The audit closes
when both readers of a round return zero blocking findings, in two consecutive rounds.

1. **Run the mechanical lints, and fix every hit.** Run every check that a script or a grep can decide,
   before a reader spends attention on the text. Fix each hit at this step. The five lints under
   "The mechanical lints" are that whole set. The cold readers then spend their attention on what no
   script can judge: whether the text lands on a stranger.
2. **Hand the text to two fresh cold readers.** Both sessions hold zero context on the text's history.
   One works under the reader-prompt, and one works under the unprompted reader's brief. The two run
   apart, and neither reader sees the other's output. Each session returns the places a stranger
   stops, each one marked blocking or non-blocking. Both readers repair nothing.
   Where the text leaves an answer out, that session
   writes down the guess it made in place of a missing answer. The guess shows where the text sent
   the reader.
3. **The auditor merges the two lists.** The auditor is the session running this skill, and the merge
   belongs to it alone. Work these steps in order:
    - read both lists whole before matching anything;
    - match the stops that name the same passage. The two readers label one passage differently, so
      the match is made on the passage each stop quotes;
    - mark a passage both readers stopped on as found by both. Those stops are the strongest, and
      they lead the list;
    - where the two readers named different faults in one passage, keep both faults under that one
      entry;
    - keep every stop one reader found alone, and record beside it which reader found it;
    - carry every stop into one ordered list: the stops found by both first, then the remaining
      blocking stops, then the non-blocking ones.

   Before step 4 begins, the auditor checks each stop's factual claims against the sources that stop
   cites, and cuts what no source holds. That check is refutation, and the auditor runs it or hands it
   to a second worker told to knock each stop down.

   That merged list is what step 4 repairs, and the reading record carries it whole.
4. **Write each fix from the source.** For a blocking finding, take the fix from the material the text
   already rests on. "Where a fix comes from" holds the rules. A non-blocking finding waits: it
   queues for the person's taste call once the blocking ones are gone.
5. **Read again, and close on two clean rounds.** After the fixes land, hand the text to a fresh pair
   of readers, one under each brief. The loop ends when both readers of a round return zero blocking
   findings, in two consecutive rounds. The comprehension gate
   settled on two reads, and `docs/spec-format.md` records that pattern.

   **A repair writes text nobody has read.** Both readers of round one met the text as it stood before
   the fixes. Whatever the repair wrote is unread, and a definition written to close a finding carries
   its own claims. On 2026-08-05 a separate review of the repaired `live-spec-base` skill found four
   defects inside the repair's own new sections
   (`docs/skill-review/2026-08-05-live-spec-base-readability.md`). Three of them blocked. One was a
   false claim about where every path in that file resolves. Neither cold reader could have caught
   them, because neither ever saw those sentences.

   So round two reads the repaired text, and it is the round that earns the closing. An audit stopped
   after round one has repaired the text a reader met and shipped the text nobody met. Say so in the
   reading record when a run stops early, and record the audit as open.

A section-sized run puts one definition and a handful of sentences in front of a reader. A whole-page
run puts every sentence of that page in front of one reader. Audit the section the edit touched, and
read a whole page when the person asks for it.

## Running it on a spec section

A spec section here is one requirement with its Context paragraph, its User Story, and its acceptance
criteria. A short run of such requirements is also a section.

Ten requirements at a time is the working size, and one such run is a **batch**. Ten requirements run to
about 250 lines of `PRODUCT_SPEC.md`. The plan chose that size for two reasons
(`docs/plans/2026-07-28-top-level-readability.md`). A fresh reader holds that much, and a repair inside
those lines cannot break a requirement a hundred lines away.

A spec section stands on the spec-body surface. Four things differ there from the human-prose run that
the sections above describe.

**The requirement-shape lint applies here.** It is one of the three lints only a spec section runs:
`python3 guardrails/check-requirement-shape.py FILE`. The vocabulary lint and the weak-word lint are
the other two, and "The mechanical lints" names what each of the three reads. This lint reads three
things nobody would ask of a README. Context comes before criteria. Each criterion carries one trigger and one response. Every
judgment names a judge and a measure.

**A criterion and the prose around it take different rules.** A numbered acceptance criterion writes in
the third person and names the actor it binds. The Context paragraph beside it speaks to the reader
directly. The third-person rule binds the criterion lines, and the direct-address rule binds the
Context paragraphs, so neither one judges the other's sentences.

**Every mark a machine reads survives the repair.** A requirement's number and its bracket anchors stay
exactly as they were. A bracket anchor is a short code in square brackets at a line's end, such as
`[INV-241]`. It points to that code's home in the spec (`docs/spec-format.md`). Headings stay as they
were, and so does any phrase a test quotes. A rewrite that moves one of them breaks a test, or one of
the two maps below.

- The **code-to-location table** is the map a script builds from the body criteria at freeze. It gives
  the location of every code (`PRODUCT_SPEC.md`, glossary entry "generated index").
- The **test matrix** is `TEST_MATRIX.md`, whose rows pair one architecture node with one spec fact and
  pin the test level that covers it.

**A fix comes from the spec's own neighbours.** The architecture document, the recorded decision, and the
test matrix hold the answers this text rests on. Where none of them answers, the finding is a real hole,
and it takes an inline `[GAP: what is missing]` note.

Three checks run after the section is repaired, and each one reports what it read. The structure checks,
third in the list, are four commands of their own:

- the test suite, which pins exact phrases from the spec, so a dropped phrase fails a test. Run the
  audited project's own suite command, whatever it is;
- the meaning-check reader, who puts the old text and the new text side by side and reports every
  difference in meaning. This reader holds both drafts, which a cold reader never does, and it works
  the eight fields at [`references/rewrite-meaning-check.md`](references/rewrite-meaning-check.md);
- the four structure checks, each one run from the repository root:
    - `python3 guardrails/check-requirement-shape.py PRODUCT_SPEC.md` — every requirement keeps its
      Context, its User Story, and its criteria in named cases;
    - `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md PRODUCT_SPEC.index.md` — the
      code-to-location table still matches a fresh build off the body;
    - `python3 guardrails/check-matrix-reference.py TEST_MATRIX.md` — every anchor on a body row of the
      test matrix stands in that matrix's generated Reference section;
    - `bash guardrails/check-freeze.sh` — the three guarded documents match the frozen baseline.

Two of these three checks run anywhere: the project's own suite and the meaning-check reader. The
structure checks need the live-spec scripts on disk.
Where those are absent, run the first two checks, and write in the reading record that the third did
not run.

The frozen baseline is the recorded map of a guarded document's anchors, marker lines, numbers, and
paths. `python3 scripts/spec-freeze.py --freeze PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md
--compaction` writes that map under `.spec-freeze/`. A checkout carrying no baseline there skips the
check.

The census and its push-time ratchet measure this pack's own documents against this pack's own writing
rules, so they stay inside the pack. A text you audit is measured by the style lint and the register lint
this section already names.

**The build test is defined, and its first run is still owed.** It measures the work once Step 5's two
clean rounds close the audit. A build test asks a further question: does the repaired text still
say enough to build from? Hand the repaired requirements to a fresh agent that holds no other context.
Ask it to implement them, and count how many it builds without asking a question. A higher count is
better, and the count to reach is every requirement in the batch.
`docs/plans/2026-07-28-top-level-readability.md` sets out that measure, taking the count before and
after each batch, by two different fresh agents. No build test has been run under it. Nothing on record
names the requirements a build test ran on, the agent that read them, or what it produced
(`docs/reports/2026-07-28-document-state-and-plan.md`). So this skill states no build count. Until such
a run is recorded, the evidence for the loop is the cold readings alone, which stand under
`docs/language-reads/`.

## The mechanical lints

Run these before any reader. Each lint names a script and a grep fallback.

The scripts sit under the live-spec repository's `guardrails/` and `scripts/` directories. When that
repository is on the auditor's disk, run the scripts from its root, whatever project the audited text
belongs to. Each script takes the path of the audited file as its argument, so that path may lead
anywhere on disk. When the repository is absent, use the grep fallbacks. They need no scripts and work
anywhere, so the audit never waits on a download.

**Three of these scripts read a spec section and nothing else.** `check-vocabulary.py` reads the
glossary. `check-weak-words.py` and `check-requirement-shape.py` read the acceptance criteria.

A README, an article, or a piece of copy carries neither. Each of the three then exits 1 and names
its input set as empty. That refusal is the honest answer, and it is the answer to expect here.

On those surfaces the class stays with the grep fallback and with the cold reader. Record the
refusal in the reading record and move on. Editing a script or a document to make one of them pass
is out of bounds. A run over ten documents met four such refusals on 2026-08-05 and recorded them as
coverage (`docs/skill-review/2026-08-05-audit-skill-names-its-spec-only-lints.md`). That run made the
mistake this paragraph forbids. A refusal recorded as coverage leaves its class with no owner.

- **Every term is defined at first use.** Every domain noun the text uses carries a one-sentence
  definition, and the reader meets it before the noun's first working use. A domain noun is one whose
  meaning is particular to this project or this field.
    - Script: `python3 guardrails/check-vocabulary.py FILE`.
    - Grep fallback: list the nouns written with an initial capital and the nouns this project coined,
      then confirm each one has an introducing sentence above its first use.
- **A weak relational word fills the slot it opens.** Words such as *depends*, *related*, *handles*,
  *based on*, *corresponds to*, *proportional*, *larger*, *sufficient*, *appropriate*, *fast*, and
  *easily* open a slot. The slot takes a reference point, a measure, or a reason, and the sentence fills
  it where the word stands.
    - Script: `python3 guardrails/check-weak-words.py FILE`. The fuller list lives in
      `guardrails/weak-words.json`, seeded from the ISO 29148 and INCOSE vague-term lists. Those are two
      published requirements-writing standards, and each names the vague terms to avoid.
    - A run reads the `weak-words.json` sitting beside the `check-weak-words.py` that ran. The
      environment variable `WEAK_WORDS` names another path, and that path wins.
    - When a cold reader reports a new slot-opening word, the auditor adds it by hand to the file that
      run just read. A project holding no such file gets one, carrying a `weak_words` list. Each word
      added this way is one more class the mechanical layer holds from then on.
    - Grep fallback: search for the words this bullet lists, and read each hit for a filled slot nearby.
- **A spec section owes the requirements genre.** Context comes before criteria, each criterion carries
  one trigger and one response, and every judgment names a judge and a measure. This lint reads a text
  written as a spec. Skip it for a README, an article, or marketing copy.
    - Script: `python3 guardrails/check-requirement-shape.py FILE`.
    - Grep fallback: read each requirement by hand against the three points above.
- **Style and register.** A sentence past the cap for its surface is a hit. A human-prose sentence aims
  at the band of 15 to 25 words. No word stands in capitals for emphasis, though an acronym and a code
  identifier pass. No sentence names a thing by denying its neighbour, and no adjective grades a
  result's size. The banned shape reads `a spec, not a plan`, where the denied half hands the reader
  nothing. A contrast between two things the reader already holds passes.
    - Scripts: `python3 scripts/spec-style-lint.py FILE` for a spec section, and `python3
      scripts/preshow-register-lint.py FILE` for any human-facing surface.
    - Grep fallback: read for those four classes by hand. The neighbour-denying one shows up as *not*
      after a comma or a dash. The last one shows up as *big*, *huge*, *minor*, or *breakthrough*.
- **One name per thing.** No named thing appears under two names: a file, a script, a command, or a
  concept.
    - Script: `python3 guardrails/check-one-name.py FILE`.
    - Grep fallback: list each named thing, and confirm one name carries it throughout.

A mechanical hit is fixed before the cold reader runs, so no reader spends a finding on a class a machine
already owns.

## The cold reader

Hand the text to two fresh sessions. One reads under
[`references/reader-prompt.md`](references/reader-prompt.md), which prints 39 kinds of place to stop.
One reads under [`references/unprompted-reader-brief.md`](references/unprompted-reader-brief.md),
which prints none. Both passes run on every audit, whatever the budget allows. Two rules govern each
pass.

Each reader holds **zero context on the text's history**: no earlier draft, no project background, no
author's intent beyond the page. In this pack that means a fresh worker with the pack not loaded, reading
the text from outside. `docs/spec-style.md` states that separation: a writer or reader holding the
project's rules is kept apart from one who does not.

Every finding is **marked blocking or non-blocking**. One test decides it, stated at the top of this
skill: the reader could not go on, or would have applied the text wrongly. Most blocking findings fall
into three kinds, and that test decides any case outside them:

- an undefined term the rest of the text leans on;
- a relational word whose slot decides what the reader does;
- a claim with no findable ground.

A non-blocking finding is a place where the text still reads and the fix would only sharpen it. A
smoother ordering, a shorter sentence, and a term that helps without carrying weight are non-blocking.

The loop closes when both readers of a round return zero blocking findings, twice in a row. The
non-blocking ones go to the person as a list, and the person decides which of them to spend a rewrite
on.

### What each reader is handed, and what each one brings back

**The prompted reader** works under the printed rule list. In a measurement over three documents on
2026-08-05, recorded in `docs/skill-review/2026-08-05-audit-runs-two-readers.md`, it alone caught
local sentence mechanics. It found a pronoun with no antecedent, one word
carrying two meanings, a sentence with no actor, and an image with no referent. Every one of those is
a readability problem.

**The unprompted reader** is handed the text, the reader the text is written for, and the task. Its
brief tells it to leave the page. It opens what a claim cites, runs the steps the text teaches, and
checks a number against its source. In the same measurement it alone caught whether the document can
be used. It found these:

- prerequisites the page never states;
- an install section that installs nothing the page promises;
- a link pointing at another repository;
- a rule its own evidence contradicts;
- an arithmetic error in a worked example.

No prompted reader stepped outside the page.

About thirty passages came back from both readers. Those are the strongest stops, and every one of
them survived refutation.

### What the pass costs

Both readers report stops that fall away when a second worker is told to knock them down. Over the
three documents read on 2026-08-05, whose figures stand in
`docs/skill-review/2026-08-05-audit-runs-two-readers.md`:

- the prompted reader reported 227 stops. 135 survived refutation and 36 blocked. 40.5% were thrown
  out.
- the unprompted reader reported 128 stops. 87 survived refutation and 21 blocked. 32.0% were thrown
  out.

Adding the two lines above gives 355 stops, of which 222 survived and 57 blocked. That arithmetic is
this skill's own, and the record prints none of the three sums. It also counts twice the roughly
thirty passages both readers found, so the pair's distinct stops run nearer 325.

This change replaced the prompted reader running alone, whose 227 stops are the baseline a reader
carries. Against those 227, the pair's roughly 325 distinct stops run about 1.43 times as many, so
the judging work grows by about two fifths. Between a third and two fifths of what comes back leads
to no repair.

That record quotes a per-document figure from an earlier draft of this skill, and no measurement
stands behind it. It also names none of the three documents, so this skill states no figure for one
document.

A second measurement the same day read a publish candidate under both briefs, and it reproduced the
split. That record states no counts for the second run, so this skill states none.

### The by-hand mode

A person working alone still needs a reader other than the author. Hand the text to a person who has not
read it, together with the prompt and nothing else. That reader gets no repository, no earlier draft, and
no chance to ask the writer a question (`docs/language-rule-coverage.md`, "A person reading the text").

By hand the reading step takes two such people. One holds the printed prompt, and one holds the
unprompted reader's brief. Neither one sees the other's list, and the auditor merges the two lists by
the steps in "The loop".

Where no such reader is at hand, the by-hand mode covers the mechanical lints through their grep
fallbacks, and it stops there. The cold read does not run, and the audit does not close. Say so in the
reading record, rather than counting the text as read. Where one reader alone is at hand, the round
stands incomplete and the audit stays open, and the reading record says which brief went unread.

## Where a fix comes from

A fix comes from the material the text rests on, and from nowhere else.

- A **term** gets the definition its source gives it, written at the term's first use.
- A **relational word** gets the reference point, the measure, or the reason its source names, written
  where the word stands.
- A **judgment word** gets its judge and its inputs, from the source that decides the judgment.
- A **claim** gets its ground stated, or the claim shrinks to what the source supports.

That material is the source spec, the code, the recorded decision, or the author's own notes.

Sometimes the source holds no answer: the spec is silent, the decision was never made, the number was
never set. That finding is a genuine hole. Record it as a question for the person, and leave a visible
mark at the spot, so the open question travels with the text. The mark takes the text's own form. A spec
section takes an inline `[GAP: what is missing]` note. A README, an article, or a piece of copy takes a
bracketed query in the draft.

Inventing an answer to close a finding is the one move this skill forbids. An invented definition hides
the hole from the next reader, and leaves the text stating what no source backs.

## This skill is held to the rules it lists

This skill obeys the human-prose register printed in
[`references/human-prose-rules.md`](references/human-prose-rules.md).

This skill is human prose, so `scripts/preshow-register-lint.py` is the register check that applies to
it. Run `python3 scripts/preshow-register-lint.py skills/text-audit/SKILL.md` from the repository root,
and run it over each file under `skills/text-audit/references/` as well. A passing run prints one line
saying that the file is clean.

`guardrails/rule-census.json` records this file at zero findings, and the pack's doc-findings gate
refuses a push that raises that count.

Whoever changes this skill runs the register lint again. The same editor runs one cold-reader loop over
the changed section before the skill ships.

## The pack this skill belongs to

- **live-spec-base** holds the shared rules and the defaults.
- **spec-author** writes the spec.
- **product-prover** reviews the spec as written.
- **design-reviewer** judges the design the spec describes.
- **build-pipeline** ships the change.
- **test-author** derives the matrix and writes the tests.
- **communicator** carries the work to the human.
- **feedback-intake** files what comes back.
- **feedback-collector** offers a rare private note up to the authors.
- **text-audit** reads a text as a stranger and repairs where they stop.
- **publish** runs the checks a publication owes its reader.
