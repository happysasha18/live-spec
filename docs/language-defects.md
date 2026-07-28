# Where the language rules came from

This document is the record behind the rules this project states about its own writing. It covers:

- the words this page uses, and where the rules themselves are kept;
- the people who write these texts and the people who read them;
- the one demand the writer owes the reader;
- every reading that produced a rule: who read what, when, and where the reading stopped;
- one sentence of the spec before and after its repair;
- how a class of mistake becomes a rule;
- what no script and no model will ever find;
- what a writer does with all of this tomorrow.

live-spec is this project: a set of skills, scripts, and gates that a person and an agent use together
to write, prove, and ship software. A gate is a script that refuses a commit or a push when the thing
it guards is wrong. The texts described below are this project's own documents.

Seven words carry the weight on this page, and each names its own thing.

A **class** is the shape of a mistake: the form it takes wherever it turns up. A **break** is one place
a text falls short of a rule: a single instance of the class that rule names. A **catcher** is whatever
finds a break: a literal pattern in a script, a model reading for meaning, or a person reading the text.
A **home** is the one file a given fact is written in. The **source** is the home of every rule, the
file `guardrails/language-rules.json`, where each rule is edited and nowhere else.

A **surface** is a kind of text rather than a file, so one file carries several: the numbered criteria
of a spec are one surface and that same file's paragraphs are another. This project names six
surfaces — spec-body, human-prose, chat, artifact, commit, and worker-brief — and each rule binds the
ones it applies to. All six are defined, each with an example, on the writer's page named just below,
and a reader who has not met them starts there.

A **rule** is one statement about one class, written as one entry in the source. Every entry carries
nine parts, five of them the writer's and four the maintainer's.

- The writer's five: a short identifier; a short name for the defect; the sentence that removes the
  mistake; the question to ask of a sentence; and the surfaces the rule binds.
- The maintainer's four, printed on the maintainer's page rather than the writer's: whatever catches a
  break of the rule; the moment each catcher runs at; a status saying whether anything catches the rule
  today; and the files that stated the rule in prose before the source existed.

An entry also carries examples, exceptions, thresholds, and the lists the rule names, where the rule has
them. Those reach the writer too.

Two pages are built from the source, and each has one reader.

- `docs/language-rules.md` is the writer's page. It carries every part of a rule that a writer applies.
- `docs/language-rule-coverage.md` is the maintainer's page. It carries the maintainer's four parts, how
  far each catcher reaches, how to run every kind of catcher by hand, and what a break costs at each
  moment a catcher runs.

Read the writer's page to write. Read the maintainer's page to run or repair a catcher. Read this page
to know why the rules say what they say. Each rule carries a short identifier such as `r02`, and this
page names a rule by that identifier together with the rule's short name in italics. A short name is a
clause naming the defect the rule removes, rather than a title. An identifier is never reused: a retired
rule takes its identifier out of the set with it, and no later rule takes it back. The highest identifier
is therefore a larger number than the count of the rules that remain.

## The people on this page

Five roles appear on this page: the writer, the reader, a cold reader, the maintainer, and the owner.

- **The writer** drafts a text here. The writer is a person, or the agent working for one.
- **The reader** reads that text afterwards, carrying whatever context they happen to have.
- **A cold reader** is given the text alone: no repository, no history of earlier drafts, and no chance
  to ask the writer a question.
- **The maintainer** builds the catchers and repairs them, and reads the maintainer's page to do it.
- **The owner** is the one person whose project this is. Every project has an owner, and this project's
  owner reads drafts and stops on sentences.

One person often holds more than one of those roles in a day.

A rule enters this project when a reader stops on a sentence. Some rules came from a cold reader
stopping, and some from the owner stopping; the readings recorded below name which produced what.

## The one demand

The writer owes the reader every word, number, and list the writing depends on. That debt is measured
on a cold reader, the reader who brings nothing to the text: no repository, no earlier draft, and no
answer given in some conversation. Each of those words, numbers, and lists therefore stands where it
is used, or in one named place the sentence points to. A text that holds for a cold reader holds for
every other reader, whatever context that reader arrived with.

Every rule on the writer's page names one way a text falls short of that demand.

## The readings that produced the rules

The first three sections below stand in the order those readings happened. The fourth holds this page's
own readings, which run across both days and are still going on.

### Two cold readers, 2026-07-27

The English reader was given six requirements from the spec (`PRODUCT_SPEC.md`) with its glossary held
back, and was asked to name every place the reading stopped. That reader found no fault with the
grammar and called the structure professional work. The text used ordinary English nouns for jobs only
this project knows: seat, net, door, home, walk, lens, handle, frame, law, tier. It also used "red" as
a verb, meaning to report something as a failure. Those ten nouns stand here as instances of the class
this reader met, and not as a vocabulary to carry onward. Four of them — home, seat, law, and tier —
turn up again on this page, each defined where it is used.

Of the six requirements, that reader could implement two from the text alone. For a third, the reader
wrote down the questions the requirement left unanswered; a cold reading has no channel to ask them, so
the requirement stood unimplemented with its questions beside it. The reader did not attempt the
remaining three. The lists and the default values those three requirements depend on were never given
anywhere in the text.

The Russian reader was given six paragraphs of working chat, about 250 words, and stopped twenty times.
Working chat is what a person and an agent write to each other while the work is going on. Twenty
stops in 250 words is a stop every thirteen words, in a text meant to be read straight through. Every word that stopped that reader was
made by translating an English term of this project's own into Russian, one word at a time. The result
each time was a real Russian word that carries none of the meaning this project gives it. The writer's
page records those words with their plain replacements, under `r02`, *a coined, loan-translated, or
respelled word standing where a plain standard word exists*.

That reader also named two habits without being asked, and both are rules today. Actions handed to
things that cannot perform them are `r05`, *a predicate applied to a subject that cannot carry it*. One
thing carrying two names in neighbouring sentences is `r04`, *one thing answering to a second name*.

### The owner's reading of a rewrite, 2026-07-27

Later the same day the owner read a first rewrite, drafted in chat and applying these rules, and
stopped at six of its sentences. Two of those six were the rewrite breaking a rule it stated in the
same passage.

- One sentence stated the rule that a criterion carries one trigger and one response. It stated that
  rule in two words carried over from English rather than said in Russian: «триггер», the English word
  trigger respelled in Russian letters, and «обязанность», the Russian word for an obligation, standing
  where the response belonged.
- Another sentence banned coined names while coining one: «хвост без глагола», a tail with no verb. The
  thing that phrase points at is real, and it already had a plain name — a phrase with no finite verb.
  The writer's page carries it under that plain name, as `r36`, *a criterion closing on a phrase with
  no finite verb*. The coined phrase went, and the class it pointed at stayed.

### A cold reader given the rules page and a real job, 2026-07-28

On 2026-07-28 a cold reader was handed `docs/language-rules.md` as it then stood, one page carrying
every rule and every catcher together, with a job to judge it against: write one page of documentation
tomorrow and hold it to this rulebook. That reading is recorded at
`docs/language-reads/2026-07-28-read1-language-rules-reference.md`. A file under `docs/language-reads/`
is one reader's account of a single reading: what the reader was given, what the reader was asked for,
and every place the reading stopped, each stop carrying the guess the reader made there and whether it
kept the reader from going on.

That reader could apply thirty of the sixty rules to tomorrow's page. Eight of the thirty need no
judgment at all, because each ships a word list or a fixed shape. The reading names those eight by
identifier, and the other twenty-two turn on the reader's own judgment. All thirty assume an answer to
which surface a documentation page is. Without that answer the count drops to the number of the rules
binding every surface, and the reading puts no exact number on those. The surfaces were the axis the
whole page was organized on, and the page defined none of them.

That finding and the writer's page as it stands today are hours apart on one day rather than in
conflict. The reading happened on 2026-07-28, and the definitions were written later that same day in
answer to it.

Three findings changed the shape of the rules rather than the wording of one entry.

- The reader passed over four fields in every entry without using any of them, and reported that none
  of them changes a word a writer writes: the file-and-line references, the catcher reach descriptions,
  the text the judging model is handed, and the historical half of the notes. Those four now stand on
  the maintainer's page, and the writer's page carries what a writer applies.
- Six rules named a list and gave it nowhere. A script catcher keeps the words it matches in a
  configuration file of its own, beside the script. Every one of those six lists now stands inside the
  rule that names it, read out of that configuration file at the moment the page is built. Three of the
  six had no such file: their words sat inside a script's regular expressions, where one edit reached
  the script and no edit reached the page. Those three lists moved into a configuration file beside
  their script, and the script now reads its own list from that file, so one edit reaches both.
- Five classes stood spread across twelve entries, each class broken into pieces. The twelve are folded
  back into five, and each survivor's notes name the identifiers that were retired.

### The readings of this page, 2026-07-27 to 2026-07-28

This page has been given to a cold reader nine times and has failed every time. A stop blocks when the
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
  `docs/language-reads/2026-07-28-read9-language-defects.md`: 31 stops, 5 of them blocking. Those 5 are
  what this draft repairs.

The seventh reading returned fewer stops than the sixth and more blocking ones. Between those two
readings this page had taken on instructions for running the catchers and a statement of what a break
costs. That material is what raised the blocking count.

Those instructions rest on three vocabularies this page does not define. The first is the six surfaces.
The maintainer's page defines the other two. One is the words that say whether a catcher runs a rule
today, such as `held` and `stated-only`. The other is the names of the moments a catcher fires, such as
`pre-commit` and `session-stop-hook`. The instructions moved to the maintainer's page to join them. This page keeps the record, and it sends the reader to the other two
pages for the rest.

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

This page calls one such failure a lapse, and a lapse is a different thing from a break. Both quotations
below call a lapse a break, that being the spec's own word for it. On this page a break stays what it
was defined as above: one place a text falls short of a rule. The older quotation calls the four laws
members; the repaired criterion calls them laws, the spec's own word, and this page calls them laws
throughout. A statement about how a text is written is a rule, on this page and on the writer's page,
and never a law.

Criterion 4 of Requirement 233 in the spec once read as follows, at 107 words:

> The system *shall* judge the orchestration members carrying a reminder-history of two or more —
> worker-routing (each unit of work routed to the cheapest tier its step and kind allow),
> lean-orchestrator (heavy reading dispatched to a worker rather than held inline), pull-unblocked-work
> (the session keeps pulling unblocked queue work rather than idling), and classify-the-subtask (a
> subtask is the person's or the seat's by what the subtask itself needs, never by the heading it sits
> under) — their breaks recorded in the one home the break-record law names, the problem ledger
> (`PROBLEMS.md`), and *shall* leave the single-occurrence members as reminders until they recur.
> [INV-241, INV-108, INV-69, INV-137, INV-143]

The bracketed codes at the end are this project's internal identifiers for requirements stated elsewhere
in the spec, and they count toward the 107 words. The sentence carries three instructions: judge the
laws, record every lapse in the problem ledger, and leave a law with a single occurrence standing as a
reminder. It carries the definitions of the four laws as well. The length is what a reader notices
first, and those four definitions are what made it long.

That criterion now reads as follows. The sentence runs to 35 words with the same codes, and five items
sit in a list below it. The hyphen went as part of the repair: the older quotation reads
reminder-history and the repaired criterion reads reminder history, two words.

> The system *shall* judge the orchestration laws carrying a reminder history of two or more, and
> *shall* leave a law with a single occurrence as a reminder until it recurs. [INV-241, INV-108,
> INV-69, INV-137, INV-143]
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

The repair took the four definitions out of the sentence and cut it from 107 words to 35, and it closed
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
3. The writer writes the class into the source as one entry, carrying the nine parts stated at the top
   of this page. The status on a new entry says that nothing catches the rule yet. The maintainer then
   builds or wires a catcher for it and records that catcher under the rule.

Every rule on both built pages is one such entry rendered for its reader.

A repair applied to one sentence and nowhere else means step 3 was skipped, since only an entry in the
source carries a repair past the sentence that prompted it.

A list of examples with no class named above it breaks the rule that governs how the source grows
(`r61`, *a defect recorded as examples with no class behind them*).

## What no script and no model finds

No script and no model finds a class nobody has met yet. Both re-catch what a person already caught
once. Every rule on the writer's page exists because a person stopped on a sentence and said so. Cold
reading is therefore a standing cost rather than a one-time check. A project plans a reading into every
round of revision and pays for the reader's hours.

A literal pattern holds only the instances someone already met. `scripts/preshow-register-lint.py` reads
a document about to be shown to a person. It makes two passes over that document: a list of literal
patterns, and one model call. Each pattern in that list is recorded in the script beside the date it was
folded in, and every one of them was folded in between 2026-07-05 and 2026-07-10. On 2026-07-17 the list
was handed one Russian sentence carrying two of this project's coined names translated word for word.
The list names both coinages in their English form and holds no Russian rendering of either. The list
passed the sentence clean: it had met the coinage and not this wording of it.

That result stands as a test today, in `tests/test_register_judge.py`. Two things there carry names
close enough to be read as one. `scripts/preshow-register-lint.py` is the script that reads a document
before a person is shown it. The judge is the model call that script makes, and
`hooks/register_judge_core.py` is where the call is made. That one test file holds the tests for both.

A model reads for the class itself, so it catches an instance no list holds. It also reports sentences
that turn out to be no defect at all. A person settles what neither of them can.

## Using this tomorrow

Open `docs/language-rules.md`. The rules listed under a surface there are the whole set governing a text
of that kind. A rule binding every surface is listed under every one of the six. Each rule carries
one question to ask of one sentence. Ask those questions of the sentences you are least sure of, and of
every sentence that states a rule. The sentence carrying a rule is the first test of that rule.
