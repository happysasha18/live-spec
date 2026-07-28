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

Seven words carry the weight on this page, each naming its own thing, and all seven are defined below:
class, break, catcher, home, source, surface, and rule.

A **class** is the shape of a mistake: the form it takes wherever it turns up. A **break** is one place
a text falls short of a rule: a single instance of the class that rule names. A **catcher** is whatever
finds a break: a literal pattern in a script, a model reading for meaning, or a person reading the text.
A **home** is the one file a given fact is written in. The **source** is the home of every rule, the
file `guardrails/language-rules.json`, where each rule is edited and nowhere else.

A **surface** is a kind of text rather than a file, so one file carries several: the numbered criteria
of a spec are one surface and that same file's paragraphs are another. This project names six
surfaces — spec-body, human-prose, chat, artifact, commit, and worker-brief — and each rule binds the
ones it applies to. All six are defined with an example in `docs/language-rules.md`, the writer's page,
and their names stand here because the readings recorded below name them.

A **rule** is one statement about one class, written as one entry in the source. An entry carries
fifteen parts: ten on every entry, and five more where the rule has them. The three groups below name
all fifteen with the field each is written in, and a new entry is written against this list.

- The writer's five, on every entry: a short identifier (`id`); a short name for the defect (`name`);
  the sentence that removes the mistake (`rule`); the question to ask of a sentence (`reader_test`); and
  the surfaces the rule binds (`surfaces`).
- The maintainer's five, on every entry and printed on the maintainer's page: whatever catches a break
  of the rule (`catchers`); the moment each catcher runs at (`armed`); a status saying whether anything
  catches the rule today (`status`); the files that stated the rule in prose before the source existed
  (`sources`); and the maintainer's notes (`notes`), which carry what the entry was folded out of and
  what is still open on it.
- The five that stand only where the rule has them: examples of the defect with their repairs
  (`examples`); exceptions the rule allows (`exceptions`); thresholds it counts against (`thresholds`);
  the lists it names (`lists`); and an override (`personal_override`), which the owner writes to hold
  one rule tighter over their own texts than this project's default holds it. The first four reach the
  writer, and the override is printed on both pages.

Two pages are built from the source, and each has one reader.

- `docs/language-rules.md` is the writer's page. It carries every part of a rule that a writer applies.
- `docs/language-rule-coverage.md` is the maintainer's page. It carries the maintainer's five parts, how
  far each catcher reaches, how to run every kind of catcher by hand, and what a break costs at each
  moment a catcher runs.

Read the writer's page to write. Read the maintainer's page to run or repair a catcher. Read this page
to know why the rules say what they say. Each rule carries a short identifier such as `r02`, and this
page names a rule by that identifier together with the rule's short name in italics, a clause naming the
defect the rule removes. An identifier is never reused: a retired rule takes its identifier out of the
set with it, and no later rule takes it back. The source carries 53 rules and its highest identifier is
`r62`, so nine stand retired: seven went in the fold recorded below,
`r22` was folded into `r01` before that fold, and `r28` left the set with no record of why.

## The people on this page

Five roles appear on this page: the writer, the reader, a cold reader, the maintainer, and the owner.

- **The writer** drafts a text here. The writer is a person, or the agent working for one.
- **The reader** reads that text afterwards, carrying whatever context they happen to have.
- **A cold reader** is given the text alone: no repository, no history of earlier drafts, and no chance
  to ask the writer a question. Every cold reading recorded on this page was made by a model in a fresh
  session with none of this project loaded.
- **The maintainer** builds the catchers and repairs them, and reads the maintainer's page to do it.
- **The owner** is the one person whose project this is. Every project has an owner, and this project's
  owner reads drafts and stops on sentences.

One person often holds more than one of those roles in a day.

A cold reading is run the same way every time. The reader is handed the text under a standing prompt,
and `skills/text-audit/SKILL.md` holds the copy to paste. That prompt asks the reader to read the
text once, straight through, and to mark every place it stopped: a term used before it is defined, a
word such as larger or faster with no measure beside it, a sentence it had to read twice, a claim whose
ground is nowhere on the page. It asks for no repair, and where the text withheld an answer it asks for
the guess the reader made instead, because that guess is what shows the writer where the text sent them.

A reading comes back as a file naming what the reader was given and asked for, followed by a numbered
list of the stops, each carrying five things:

- the phrase the reader stopped on;
- where that phrase sits on the page;
- what a stranger cannot tell from the page alone;
- the guess the reader made in place of the missing answer;
- whether the stop blocked the reader, or the reader noticed it and read on.

A single stop is recorded and opens nothing. A rule enters this project when the place that produced
that stop produces it again, the second occurrence proving the source rather than the sentence. Some
rules came from a cold reader stopping, and some from the owner; the readings below name which produced
what.

## The one obligation

The writer owes the reader every word, number, and list the writing depends on. That debt is measured on
the cold reader defined above, who brings nothing to the text. Each of those words, numbers, and lists
therefore stands where it is used, or in one named place the sentence points to. A text that holds for a
cold reader holds for every other reader, whatever context that reader arrived with.

Every rule on the writer's page names one way a text falls short of that obligation.

## The readings that produced the rules

The last section below holds this page's own readings, which are still going on.

### Two cold readers, 2026-07-27

The English reader was given six requirements from the spec (`PRODUCT_SPEC.md`) with its glossary held
back. The text used ten ordinary English nouns for jobs only this project knows, and used "red" as a
verb meaning to report something as a failure. Four of the
ten — home, seat, law, and tier — turn up again on this page, each defined where it is used. All of them
stand here as instances of the class this reader met, and not as a vocabulary to carry onward. That
finding opened no rule of its own. The class was already in the source as `r01`, *an ordinary word
carrying a private project meaning*, whose entry names the skill and profile files that stated it in
prose before the source existed, so this reading stands as evidence for that rule rather than its
origin.

Of the six requirements, that reader could implement two from the text alone. For a third the reader
wrote down the questions the requirement left unanswered and left it unimplemented, a cold reading
having no channel to ask them. The remaining three went unattempted: they depend on lists and on default
values the text gave nowhere.

The Russian reader was given six paragraphs of working chat, about 250 words meant to be read straight
through, and stopped twenty times. Working chat is what a person and an agent write to each other while
the work is going on. Every word that stopped that reader was made by translating an English term of
this project's own into Russian, one word at a time. The result each time was a real Russian word that
carries none of the meaning this project gives it. The writer's page records those words with their
plain replacements, under `r02`, *a coined, loan-translated, or respelled word standing where a plain
standard word exists*.

That reader also named two habits without being asked, and both are rules today. Actions handed to
things that cannot perform them are `r05`, *a predicate applied to a subject that cannot carry it*. One
thing carrying two names in neighbouring sentences is `r04`, *one thing answering to a second name*.

### The owner's reading of a rewrite, 2026-07-27

Later the same day the owner read a first rewrite, drafted in chat and applying these rules, and
stopped at six of its sentences. Two of the six were the rewrite breaking a rule it stated in the same
passage, and this page carries those two.

- One sentence stated the rule that a criterion carries one trigger and one response, and broke it
  twice over, each time differently. «Триггер» is the English word trigger respelled in Russian letters,
  where Russian already has a plain word for it. «Обязанность» is a plain Russian word standing in the
  wrong slot: it means an obligation, and it stood where the response belonged.
- Another sentence banned coined names while coining one: «хвост без глагола», a tail with no verb. The
  thing that phrase points at is real, and it already had a plain name — a phrase with no finite verb.
  The writer's page carries it under that plain name, as `r36`, *a criterion closing on a phrase with
  no finite verb*. The coined phrase went, and the class it pointed at stayed.

A sentence that states a rule is the first test of that rule, and it is the sentence to check first in
anything written here.

### A cold reader given the rules page and a real job, 2026-07-28

On 2026-07-28 a cold reader was handed `docs/language-rules.md` as it then stood, one page carrying
every rule and every catcher together, with a job to judge it against: write one page of documentation
tomorrow and hold it to this rulebook. That reading is recorded at
`docs/language-reads/2026-07-28-read1-language-rules-reference.md`. Every file under
`docs/language-reads/` carries one reading in the shape described above.

That reader could apply thirty of the sixty rules the source then carried to tomorrow's page. Eight of
the thirty need no judgment at all, because each ships a word list or a fixed shape; the reading names
those eight by identifier, and the other twenty-two turn on the reader's own judgment. All thirty assume
an answer to which surface a documentation page is: it is human-prose, and it carries the artifact
surface as well once it is published outside the project. Without that answer a writer is left with the
four rules that bind every surface: `r10`, *a thing named by denying its neighbour*; `r12`, *a word
grading how important or how good a thing is*; `r18`, *the language each surface is written in*; and
`r61`, *a defect recorded as examples with no class behind them*. The surfaces were the axis the whole page was organized on, and the page defined none of them.
The writer's page carries both today, defining all six surfaces and placing a documentation page among
them, written later that same day in answer to this reading.

Three findings changed the shape of the rules rather than the wording of one entry.

- The reader passed over four things carried in every entry and reported that none of them changes a
  word a writer writes: the files that stated the rule in prose before the source existed; two pieces of
  what catches a break, being how far each catcher reaches and the text the judging model is handed; and
  the half of the notes carrying what the entry was folded out of. All four are the maintainer's
  material, all four now stand on the maintainer's page, and the writer's page carries what a writer
  applies.
- Six rules named a list and gave it nowhere. A script catcher keeps the words it matches in a
  configuration file of its own, beside the script, as `guardrails/weak-words.json` stands beside
  `guardrails/check-weak-words.py`. Every one of those six lists now stands inside the rule that names
  it, read out of such a file at the moment the page is built. Three of the six had
  no such file: their words sat inside a script's regular expressions, where one edit reached the script
  and no edit reached the page. Those three lists moved into a configuration file beside their script,
  and the script now reads its own list from that file, so one edit reaches both.
- Five classes stood spread across twelve entries. The twelve are folded back into five, and each
  survivor's notes name the identifiers retired.

### The readings of this page, 2026-07-27 to 2026-07-28

This page has been given to a cold reader twelve times and has failed every time. A stop blocks when the
reader cannot go on with the text, or would have acted on the text wrongly; one blocking stop fails the
reading. The bar is two readings in a row returning nothing blocking, and that bar is itself one of the
rules (`r54`, *a changed section shipped before two clean cold readings*). Until it is cleared this page
is shown to nobody, with one exception: a reading is how the bar gets measured, so the reader running
one is handed the page while the bar is still unmet.

- Readings one through four left no file of their own. `JOURNAL.md`, this project's dated log of what
  changed and why, carries them in a single sentence: that the page failed four readings and took
  five repair rounds. It gives no stop count and no finding from any of the four.
- Readings five through twelve each left a file under `docs/language-reads/` named for its date and its
  number, the fifth being `2026-07-27-read5-language-defects.md`. The fifth ran on 2026-07-27 and the
  rest on 2026-07-28. In order they returned 45 stops with 11 blocking, then 34 with 8, 27 with 12, 28
  with 6, 31 with 5, 25 with 5, 25 with 6, and 25 with 5. The last reading's five are what this draft
  repairs.

The seventh reading returned fewer stops than the sixth and more blocking ones. Between those two
readings this page had taken on instructions for running the catchers, and four of the seventh reading's
twelve blocking stops sat on that new material: two on one script given as an example of a script
catcher and called the model catcher twenty-five lines later, one on a section headed for running the
person catcher that carried no procedure, and one on a command line carrying two placeholders the page
gave no way to fill. Those instructions also rested on three vocabularies this page does not define: the
six surfaces, the words saying whether a catcher runs a rule today, and the names of the moments a
catcher fires. The instructions moved to the maintainer's page, which defines the last two.

## One sentence, before and after

Six terms in the two quotations below are the spec's own and belong to no rule about writing. A tier is
one price level of the models an agent runs on. The seat is the agent session an instruction is given
to. A law is a requirement the spec states about how the project works, and the four the criterion names
are the orchestration laws. A reminder history is the running count of the times one law has been
broken. The problem ledger is the home where the running system's failures to keep those laws are
written down. The break-record law is the requirement naming that home.

Requirement, law, and bracketed identifier are three different things: the spec is written as numbered
requirements, a law is one of them, and a bracketed identifier such as `INV-241` is the code of a single
requirement, whether that requirement is a law or any other kind.

Both quotations below use break for a failure to keep a law, the spec's own word for it, while on this
page a break stays what it was defined as above: one place a text falls short of a rule. The older
quotation calls the four laws members, the repaired criterion calls
them laws, and this page calls them laws throughout. A statement about how a text is written is a rule
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

The sentence carries three instructions: judge the laws, record every failure to keep one in the problem
ledger, and leave a law with a single occurrence standing as a reminder. It carries the definitions of
the four laws as well. The length is what a reader notices first, and those four definitions are what
made it long.

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
occurrence standing. Five items moved into the list, one to a line — the four laws, each carrying the
words that had defined it inside the sentence, and the instruction that records a failure to keep a law
in the problem ledger. Taking those definitions out cut the sentence from 105 words to 35 and left every
other defect in it standing.

Two of the defects left standing can be named. The verb judge names neither a standard nor an output: the criterion never says what the judging measures a law against, or what a judgment produces.
The threshold two or more names no unit, leaving the word occurrences out. Both fall inside the
rules — `r32`, *a judgment with no judge and no measure*, and `r06`, *a number standing with no
ground* — so both classes are recorded and no entry was owed. What stands open is the criterion itself,
unrepaired in the spec today.

## How a class becomes a rule

One class shows up across many sentences, so repairing the one sentence in front of a reader leaves
every other instance in place. The writer therefore records the class, and the steps below are how a
class becomes a rule.

1. A cold reader stops on a sentence. The writer writes the stop down in that reader's own words,
   including the guess the reader made there.
2. The writer traces the wording back to where it was learned: a skill file, a template, a section of
   the spec, or a habit picked up in chat. A class opens once the writer finds the same stop coming out
   of that place again.
3. The writer writes the class into the source as one entry, carrying the ten parts every entry stands
   on and any of the other five, all fifteen named at the top of this page. The status on a new entry
   says that nothing catches the rule yet. The maintainer then builds or wires a catcher for it and
   records that catcher under the rule.

A repair applied to one sentence and nowhere else means step 3 was skipped, since only an entry in the
source carries a repair past the sentence that prompted it.

A list of examples with no class named above it breaks the rule that governs how the source grows
(`r61`, *a defect recorded as examples with no class behind them*).

## What no script and no model finds

No script and no model finds a class nobody has met yet: both re-catch what a person already caught
once, and every rule on the writer's page exists because a person stopped on a sentence and said so.
Cold reading is therefore a standing cost: a project plans a reading into every round of revision.

A literal pattern holds only the instances someone already met. Two things here carry names close enough
to be read as one, and each keeps one name. The pre-show lint is `scripts/preshow-register-lint.py`, the
script that reads a document about to be shown to a person for the level and tone of its language; it
makes two passes over that document, a list of literal patterns and one model call. The register judge
is that model call, and `hooks/register_judge_core.py` is the code that issues it.

Every pattern in the lint's list is recorded beside the date it was folded in, all of them between
2026-07-05 and 2026-07-10. On 2026-07-17 the list was handed one Russian sentence carrying two of this
project's coined names translated word for word. Neither the sentence nor the two names is reproduced
here, because the same lint gates this page and refuses a coinage shown raw to a reader; both stand in
its pattern list, one pattern each, in their English form and with no Russian rendering of either. The
list passed the sentence clean: it had met the coinage and not this wording of it. The judge was not
run, because the script makes that call only when it is switched on by hand, the maintainer's page shows
how, and the switch stayed off through the probe.

That result stands as a test in `tests/test_register_judge.py`, which holds the tests for both and takes
its name from the judge. There the lint's pattern pass is run for real, and the judge's code is driven
against a written-out model reply, so the test proves what that code does with a verdict and never calls
a model itself.

A model is there to read for the class itself, which is how it reaches an instance no list holds; the
probe above measured the list alone and says nothing about the model. A model also reports sentences
that are no defect at all, and a person settles what neither can.
