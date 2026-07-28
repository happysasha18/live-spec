# Where the language rules came from

This document is the record behind the rules this project states about its own writing. It covers:

- the words this page uses, and where the rules themselves are kept;
- the people who write these texts and the people who read them;
- the one obligation the writer owes the reader;
- every reading that produced a rule: who read what, when, and where the reading stopped;
- one sentence of the spec before and after its repair;
- how a class of mistake becomes a rule;
- what no script and no model will ever find.

live-spec is this project: a set of skills, scripts, and gates that a person and an agent use together
to write, prove, and ship software. A gate is a script that refuses a commit or a push when the thing
it guards is wrong. The texts described below are this project's own documents.

Seven words carry the weight on this page: class, break, catcher, home, source, surface, and rule. Each
names its own thing, and the three paragraphs below define them in that order.

A **class** is the shape of a mistake: the form it takes wherever it turns up. A **break** is one place
a text falls short of a rule: a single instance of the class that rule names. A **catcher** is whatever
finds a break: a literal pattern in a script, a model reading for meaning, or a person reading the text.
A **home** is the one file a given fact is written in. The **source** is the home of every rule, the
file `guardrails/language-rules.json`, where each rule is edited and nowhere else.

A **surface** is a kind of text rather than a file, so one file carries several: the numbered criteria
of a spec are one surface and that same file's paragraphs are another. This project names six
surfaces — spec-body, human-prose, chat, artifact, commit, and worker-brief — and each rule binds the
ones it applies to. All six are defined, each with an example, on the writer's page named just below.
The six names stand on this page because the readings recorded here name them; the record reads through
without their definitions, and a writer picking the rules up meets each definition on that page.

A **rule** is one statement about one class, written as one entry in the source. An entry carries
fifteen parts in all: ten stand on every entry, and five more stand where the rule has them. The three
groups below name all fifteen, and a new entry is written against this list.

- The writer's five, on every entry: a short identifier; a short name for the defect; the sentence that
  removes the mistake; the question to ask of a sentence; and the surfaces the rule binds.
- The maintainer's five, on every entry and printed on the maintainer's page: whatever catches a break
  of the rule; the moment each catcher runs at; a status saying whether anything catches the rule today;
  the files that stated the rule in prose before the source existed; and the maintainer's notes, which
  carry what the entry was folded out of and what is still open on it.
- The five that stand only where the rule has them: examples of the defect with their repairs;
  exceptions the rule allows; thresholds it counts against; the lists it names; and an override
  recording where one reader's own layer holds the rule tighter than the package does. The first four
  reach the writer, and the override is printed on both pages.

Two pages are built from the source, and each has one reader.

- `docs/language-rules.md` is the writer's page. It carries every part of a rule that a writer applies.
- `docs/language-rule-coverage.md` is the maintainer's page. It carries the maintainer's five parts, how
  far each catcher reaches, how to run every kind of catcher by hand, and what a break costs at each
  moment a catcher runs.

Read the writer's page to write. Read the maintainer's page to run or repair a catcher. Read this page
to know why the rules say what they say. Each rule carries a short identifier such as `r02`, and this
page names a rule by that identifier together with the rule's short name in italics. A short name is a
clause naming the defect the rule removes, rather than a title. An identifier is never reused: a retired
rule takes its identifier out of the set with it, and no later rule takes it back. Nine identifiers stand
retired today: the source carries 53 rules, and the highest identifier in it is `r62`, a number larger
than that count.

## The people on this page

Five roles appear on this page: the writer, the reader, a cold reader, the maintainer, and the owner.

- **The writer** drafts a text here. The writer is a person, or the agent working for one.
- **The reader** reads that text afterwards, carrying whatever context they happen to have.
- **A cold reader** is given the text alone: no repository, no history of earlier drafts, and no chance
  to ask the writer a question. Every cold reading recorded on this page was made by a model — a fresh
  session with none of this project loaded, handed the text and the prompt described below.
- **The maintainer** builds the catchers and repairs them, and reads the maintainer's page to do it.
- **The owner** is the one person whose project this is. Every project has an owner, and this project's
  owner reads drafts and stops on sentences.

One person often holds more than one of those roles in a day.

A cold reading is run the same way every time. The reader is handed the text under a standing prompt,
which is kept in `skills/text-audit/SKILL.md` ready to paste. That prompt asks the reader to read the
text once, straight through, and to mark every place it stopped: a term used before it is defined, a
word such as depends or larger with no measure beside it, a sentence it had to read twice, a claim
whose ground is nowhere on the page. It asks for no fix and for no guess at a missing answer.

The reading comes back as a numbered list, one entry to a stop, and each entry carries four things:

- the phrase the reader stopped on;
- where that phrase sits on the page;
- what a stranger cannot tell from the page alone;
- whether the stop blocked the reader, or the reader noticed it and read on.

A rule enters this project when a reader stops on a sentence. Some rules came from a cold reader
stopping, and some from the owner stopping; the readings recorded below name which produced what.

## The one obligation

The writer owes the reader every word, number, and list the writing depends on. That debt is measured
on a cold reader, the reader who brings nothing to the text: no repository, no earlier draft, and no
answer given in some conversation. Each of those words, numbers, and lists therefore stands where it
is used, or in one named place the sentence points to. A text that holds for a cold reader holds for
every other reader, whatever context that reader arrived with.

Every rule on the writer's page names one way a text falls short of that obligation.

## The readings that produced the rules

The first three sections below stand in the order those readings happened. The fourth holds this page's
own readings, which run across both days and are still going on.

### Two cold readers, 2026-07-27

The English reader was given six requirements from the spec (`PRODUCT_SPEC.md`) with its glossary held
back, and was asked to name every place the reading stopped. That reader found no fault with the
grammar and called the structure professional work. The text used ordinary English nouns for jobs only
this project knows: seat, net, door, home, walk, lens, handle, frame, law, tier. It also used "red" as
a verb, meaning to report something as a failure. Those ten nouns and that one verb stand here as
instances of the class this reader met, and not as a vocabulary to carry onward. Four of the nouns —
home, seat, law, and tier — turn up again on this page, each defined where it is used.

Of the six requirements, that reader could implement two from the text alone. For a third, the reader
wrote down the questions the requirement left unanswered; a cold reading has no channel to ask them, so
the requirement stood unimplemented with its questions beside it. The reader did not attempt the
remaining three. Those three unattempted requirements depend on lists and on default values, and the
text gave neither anywhere.

The Russian reader was given six paragraphs of working chat, about 250 words meant to be read straight
through, and stopped twenty times. Working chat is what a person and an agent write to each other while
the work is going on. Every word that stopped that reader was made by translating an English term of
this project's own into Russian, one word at a time. The result
each time was a real Russian word that carries none of the meaning this project gives it. The writer's
page records those words with their plain replacements, under `r02`, *a coined, loan-translated, or
respelled word standing where a plain standard word exists*.

That reader also named two habits without being asked, and both are rules today. Actions handed to
things that cannot perform them are `r05`, *a predicate applied to a subject that cannot carry it*. One
thing carrying two names in neighbouring sentences is `r04`, *one thing answering to a second name*.

### The owner's reading of a rewrite, 2026-07-27

Later the same day the owner read a first rewrite, drafted in chat and applying these rules, and
stopped at six of its sentences. Two of those six were the rewrite breaking a rule it stated in the
same passage, and those two are the ones this page carries; the other four are out of scope here.

- One sentence stated the rule that a criterion carries one trigger and one response. It stated that
  rule in two words carried over from English rather than said in Russian: «триггер», the English word
  trigger respelled in Russian letters, and «обязанность», the Russian word for an obligation, standing
  where the response belonged.
- Another sentence banned coined names while coining one: «хвост без глагола», a tail with no verb. The
  thing that phrase points at is real, and it already had a plain name — a phrase with no finite verb.
  The writer's page carries it under that plain name, as `r36`, *a criterion closing on a phrase with
  no finite verb*. The coined phrase went, and the class it pointed at stayed.

Both of those sentences broke the rule they were stating. A sentence that states a rule is the first
test of that rule, and it is the sentence to check first in anything written here.

### A cold reader given the rules page and a real job, 2026-07-28

On 2026-07-28 a cold reader was handed `docs/language-rules.md` as it then stood, one page carrying
every rule and every catcher together, with a job to judge it against: write one page of documentation
tomorrow and hold it to this rulebook. That reading is recorded at
`docs/language-reads/2026-07-28-read1-language-rules-reference.md`. A file under `docs/language-reads/`
is one reader's account of a single reading: what the reader was given, what the reader was asked for,
and every place the reading stopped, each stop carrying the guess the reader made there and whether it
kept the reader from going on.

That reader could apply thirty of the sixty rules the source then carried to tomorrow's page. Eight of the thirty need no
judgment at all, because each ships a word list or a fixed shape. The reading names those eight by
identifier, and the other twenty-two turn on the reader's own judgment. All thirty assume an answer to
which surface a documentation page is. Without that answer the count drops to the number of the rules
binding every surface, and the reading puts no exact number on those. The surfaces were the axis the
whole page was organized on, and the page defined none of them.

That finding and the writer's page as it stands today are hours apart on one day rather than in
conflict. The reading happened on 2026-07-28, and the definitions were written later that same day in
answer to it.

Three findings changed the shape of the rules rather than the wording of one entry.

- The reader passed over four things carried in every entry without using any of them, and reported that
  none of them changes a word a writer writes: the file-and-line references, the reach description
  inside each catcher, the text the judging model is handed, and the historical half of the notes. Those
  four sit inside the maintainer's parts named at the top of this page. They now stand on the
  maintainer's page, and the writer's page carries what a writer applies.
- Six rules named a list and gave it nowhere. A script catcher keeps the words it matches in a
  configuration file of its own, beside the script: `guardrails/weak-words.json` beside
  `guardrails/check-weak-words.py` is one, and `guardrails/criterion-readability.json` beside
  `guardrails/check-criterion-readability.py` is another. Every one of those six lists now stands inside
  the rule that names it, read out of such a file at the moment the page is built. Three of the six had
  no such file: their words sat inside a script's regular expressions, where one edit reached the script
  and no edit reached the page. Those three lists moved into a configuration file beside their script,
  and the script now reads its own list from that file, so one edit reaches both.
- Five classes stood spread across twelve entries, each class broken into pieces. The twelve are folded
  back into five, and each survivor's notes name the identifiers that were retired.

### The readings of this page, 2026-07-27 to 2026-07-28

This page has been given to a cold reader ten times and has failed every time. A stop blocks when the
reader cannot go on with the text, or would have acted on the text wrongly; one blocking stop fails the
reading.

- Readings one through four left no file of their own. `JOURNAL.md`, this project's dated log of what
  changed and why, is where those four readings are written down.
- The fifth, on 2026-07-27, is recorded at `docs/language-reads/2026-07-27-read5-language-defects.md`:
  45 stops, 11 of them blocking.
- The sixth, on 2026-07-28, is recorded at
  `docs/language-reads/2026-07-28-read6-language-defects.md`: 34 stops, 8 of them blocking.
- The seventh, on 2026-07-28, is recorded at
  `docs/language-reads/2026-07-28-read7-language-defects.md`: 27 stops, 12 of them blocking.
- The eighth, on 2026-07-28, is recorded at
  `docs/language-reads/2026-07-28-read8-language-defects.md`: 28 stops, 6 of them blocking.
- The ninth, on 2026-07-28, is recorded at
  `docs/language-reads/2026-07-28-read9-language-defects.md`: 31 stops, 5 of them blocking.
- The tenth, on 2026-07-28, is recorded at
  `docs/language-reads/2026-07-28-read10-language-defects.md`: 25 stops, 5 of them blocking. Those 5 are
  what this draft repairs.

The seventh reading returned fewer stops than the sixth and more blocking ones. Between those two
readings this page had taken on instructions for running the catchers and a statement of what a break
costs. Four of the seventh reading's twelve blocking stops sit on that new material: two of them on
`scripts/preshow-register-lint.py`, which the instructions gave as an example of a script catcher and
then described as the model catcher twenty-five lines later; one on a section headed for running the
person catcher that carried no procedure; and one on a command line carrying two placeholders the page
gave no way to fill.

Those instructions rest on three vocabularies this page does not define. The first is the six surfaces.
The maintainer's page defines the other two. One is the words that say whether a catcher runs a rule
today, such as `held` and `stated-only`. The other is the names of the moments a catcher fires, such as
`pre-commit` and `session-stop-hook`. The instructions moved to the maintainer's page to join them. This
page keeps the record, and it sends the reader to the other two pages for the rest.

This page is shown to nobody until two cold readings in a row return nothing blocking. That bar is
itself one of the rules (`r54`, *a changed section shipped before two clean cold readings*). A cold
reader is the one exception to it: a reading is how the bar gets measured, so the reader running the
reading is handed the page while the bar is still unmet.

## One sentence, before and after

Four words in the two quotations below are the spec's own and belong to no rule about writing. A tier
is one price level of the models an agent runs on. The seat is the agent session an instruction is
given to. A law is a requirement the spec states about how the project works, and the four the criterion
names are the orchestration laws. The problem ledger is the home where the running system's failures to
keep those laws are written down. The break-record law is the requirement naming that home.

Requirement, law, and bracketed identifier are three different things, and this is how they relate. The
spec is written as numbered requirements. A law is one of those requirements, the kind stating how the
project itself works. A bracketed identifier such as `INV-241` is the code of a single requirement,
whether that requirement is a law or any other kind.

This page calls one such failure a lapse, and a lapse is a different thing from a break. Both quotations
below call a lapse a break, that being the spec's own word for it. On this page a break stays what it
was defined as above: one place a text falls short of a rule. The older quotation calls the four laws
members; the repaired criterion calls them laws, the spec's own word, and this page calls them laws
throughout. A statement about how a text is written is a rule, on this page and on the writer's page,
and never a law.

The counts below take each bracketed identifier as one word, so the five codes trailing each quotation
add five, and they take a hyphenated name such as pull-unblocked-work as one word. Neither em dash in
the older quotation counts.

Criterion 4 of Requirement 233 in the spec once read as follows, at 105 words:

> The system *shall* judge the orchestration members carrying a reminder-history of two or more —
> worker-routing (each unit of work routed to the cheapest tier its step and kind allow),
> lean-orchestrator (heavy reading dispatched to a worker rather than held inline), pull-unblocked-work
> (the session keeps pulling unblocked queue work rather than idling), and classify-the-subtask (a
> subtask is the person's or the seat's by what the subtask itself needs, never by the heading it sits
> under) — their breaks recorded in the one home the break-record law names, the problem ledger
> (`PROBLEMS.md`), and *shall* leave the single-occurrence members as reminders until they recur.
> [INV-241, INV-108, INV-69, INV-137, INV-143]

The bracketed codes at the end are this project's internal identifiers for requirements stated elsewhere
in the spec, and they count toward the 105 words. The sentence carries three instructions: judge the
laws, record every lapse in the problem ledger, and leave a law with a single occurrence standing as a
reminder. It carries the definitions of the four laws as well. The length is what a reader notices
first, and those four definitions are what made it long.

That criterion now reads as follows. The sentence runs to 35 words with the same codes, and five items
sit in a list below it.

> The system *shall* judge the orchestration laws carrying a reminder history of two or more, and
> *shall* leave a law with a single occurrence as a reminder until it recurs.
> [INV-241, INV-108, INV-69, INV-137, INV-143]
>
> - worker-routing: each unit of work is routed to the cheapest tier its step and kind allow;
> - lean-orchestrator: heavy reading is dispatched to a worker, and none of it is held inline;
> - pull-unblocked-work: the session keeps pulling unblocked queue work instead of idling;
> - classify-the-subtask: a subtask is the person's or the seat's by what the subtask itself needs,
>   never by the heading it sits under;
> - each break is recorded in the problem ledger (`PROBLEMS.md`), the home the break-record law names.

Two of the three instructions stayed in the sentence: judging the laws, and leaving a law with a single
occurrence standing. Five items moved into the list, one to a line. Four of them are the laws, each
carrying the words that had defined it inside the sentence; the fifth is the instruction that records a
lapse in the problem ledger.

The repair took the four definitions out of the sentence and cut it from 105 words to 35, and it closed
nothing else. Two defects stand in the repaired criterion. The verb judge names neither a standard nor
an output: the criterion never says what the judging measures a law against, or what a judgment
produces. The threshold two or more names no unit: a reminder history counts occurrences, and the
criterion leaves the word occurrences out.

## How a class becomes a rule

A class is the shape of a mistake, and one class shows up across many sentences. Repairing the one
sentence in front of a reader leaves every other instance in place. The writer therefore records the
class, and the steps below are how a class becomes a rule.

1. A cold reader stops on a sentence. The writer writes the stop down in that reader's own words,
   including the wrong guess the reader made.
2. The writer traces the wording back to where it was learned: a skill file, a template, a section of
   the spec, or a habit picked up in chat. A class opens once the writer finds the same stop coming out
   of that place again.
3. The writer writes the class into the source as one entry, carrying the ten parts every entry stands
   on and any of the other five the rule has, all fifteen named at the top of this page. The status on a
   new entry says that nothing catches the rule yet. The maintainer then builds or wires a catcher for
   it and records that catcher under the rule.

Every rule on both built pages is one such entry rendered for its reader.

A repair applied to one sentence and nowhere else means step 3 was skipped, since only an entry in the
source carries a repair past the sentence that prompted it.

A list of examples with no class named above it breaks the rule that governs how the source grows
(`r61`, *a defect recorded as examples with no class behind them*).

## What no script and no model finds

No script and no model finds a class nobody has met yet. Both re-catch what a person already caught
once. Every rule on the writer's page exists because a person stopped on a sentence and said so. Cold
reading is therefore a standing cost rather than a one-time check, and a project plans a reading into
every round of revision.

A literal pattern holds only the instances someone already met. The **register** of a text is the level
and tone its language is pitched at, which is the words it reaches for and the sentence shapes it
allows. `scripts/preshow-register-lint.py`, the pre-show lint, reads the register of a document about to
be shown to a person. It makes two passes over that document: a list of literal patterns, and one model
call. Each pattern in that list is recorded in the script beside the date it was folded in, and every one
of them was folded in between 2026-07-05 and 2026-07-10. On 2026-07-17 the list was handed one Russian
sentence carrying two of this project's coined names translated word for word. The list names both
coinages in their English form and holds no Russian rendering of either. The list passed the sentence
clean: it had met the coinage and not this wording of it. The model call was not run on that sentence:
the script makes that call over a document only when it is switched on by hand, it stayed off through
the probe, and the record of the probe carries the pattern pass alone.

That result stands as a test today, in `tests/test_register_judge.py`. Two things there carry names close
enough to be read as one, and each keeps one name on this page. The pre-show lint is
`scripts/preshow-register-lint.py`, the script that reads a document before a person is shown it. The
register judge is the model call that script makes, and `hooks/register_judge_core.py` is the file that
makes it. That one test file holds the tests for both, and its name carries the judge's. In that file the
lint's passes are run for real, and the judge is driven against a written-out model reply, so the test
proves what the judge does with a verdict and never calls a model itself.

A model reads for the class itself, so it catches an instance no list holds. It also reports sentences
that turn out to be no defect at all. A person settles what neither of them can.
