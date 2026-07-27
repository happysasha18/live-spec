# Where the language rules came from

This document is the record behind the rules this project states about its own writing. The record
covers four things:

- where the rules came from, and who read what and stopped where;
- the one thing every text owes its reader;
- how a class of mistake becomes a rule;
- what no script and no model will ever find.

live-spec is this project: a set of skills, scripts, and gates that a person and an agent use together
to write, prove, and ship software. A gate is a script that refuses a commit or a push when the thing
it guards is wrong. The texts described below are this project's own documents.

Three words carry the weight on this page, and each names its own thing. A **class** is the shape of a
mistake: the form it takes wherever it turns up. A **rule** is what an entry states about one class —
the sentence that removes it, a question to ask of a sentence, and what finds a break. A **catcher** is
whatever finds that break: a literal pattern in a script, a model reading for meaning, or a person
reading the text.

The rules themselves live elsewhere, on two pages with one reader each. `docs/language-rules.md` is
the writer's page: it gives each rule in a sentence, a question to ask of a sentence, the surfaces the
rule binds, examples, exceptions, thresholds, and every list the rule names.
`docs/language-rule-coverage.md` is the maintainer's page: it gives each rule's catchers with how far
each one reaches, where each is armed, and where the rule was stated before the source became its one
home. Read the writer's page to write, and read this page to know why those rules say what they say.

## The people on this page

Four roles appear on this page: the writer, the reader, a cold reader, and the owner.

- **The writer** drafts a text here. The writer is a person, or the agent working for one.
- **The reader** reads that text afterwards, carrying whatever context they happen to have.
- **A cold reader** is given the text alone: no repository, no history of earlier drafts, and no chance
  to ask the writer a question.
- **The owner** is the person whose project this is. He reads drafts and stops on sentences.

One person often holds more than one of those roles in a day.

A rule enters this project from a read that stopped. Some rules came from a cold reader stopping, and
some from the owner stopping; the readings recorded below name which produced what.

## The one demand

A reader owes the text nothing. The writer gives the reader every word, number, and list the writing
depends on. Each of them appears where it is used, or in one named place the sentence points to.

Every rule in `docs/language-rules.md` names one way a text falls short of that demand.

## Where the rules live, and how to run their catchers

`docs/language-rule-coverage.md` names each rule's catchers and says how far each one reaches. Each
rule also carries a short identifier such as `r02`, and this page names a rule by that identifier.

Five files carry the rules: the file every rule is edited in, the writer's page, the maintainer's page,
the generator behind all three, and the gate over the set. Run every command below from the repository
root, the directory that holds `PRODUCT_SPEC.md`, `guardrails/`, and `scripts/`.

- `guardrails/language-rules.json` — the source. Every rule is edited here and nowhere else.
- `docs/language-rules.md` — the writer's page. A hand edit here is thrown away by the next run of the
  generator.
- `docs/language-rule-coverage.md` — the maintainer's page, generated from the same source and thrown
  away the same way.
- `scripts/gen-language-consumers.py` — the generator. It reads the source and writes both pages, plus
  `hooks/language-laws.json`, the file carrying the rules in the form the judging model reads.
- `guardrails/check-language-rules.py` — the gate. It refuses a page that has drifted from the source,
  and a rule pointing at a file or a line that is gone.

```
python3 scripts/gen-language-consumers.py
python3 guardrails/check-language-rules.py
```

### Running a script catcher

Each rule's entry names the file that carries its own script catcher. Those files are Python scripts,
and each takes the text to read as its argument:

```
python3 guardrails/check-vocabulary.py PRODUCT_SPEC.md
python3 scripts/preshow-register-lint.py docs/language-rules.md
```

Every one of them prints one line naming what it read and how far it looked. A passing run therefore
says how much of the text it covered.

### Running the model catcher

The model catcher is one model call, made by `hooks/register_judge_core.py`. That module is handed the
text together with the rules binding the text's surface, which it reads from `hooks/language-laws.json`,
and it answers with the sentences that break one. Two scripts make the call, one on each surface it
runs on today.

On chat, `hooks/register-judge.py` makes the call. `hooks/register-judge-collect.sh` runs at the
session's Stop event, starts that script in the background and returns at once;
`hooks/register-judge-report.sh` runs when the person sends their next message and prints whatever
verdict landed in the meantime. The reply that broke a rule has been read by then, so the correction
reaches the person one turn later. To make the call by hand, give the script a Stop-hook payload naming
a session transcript on its standard input:

```
printf '{"transcript_path": "%s"}' ~/.claude/projects/PROJECT/SESSION.jsonl \
  | python3 hooks/register-judge.py
```

When the turn breaks a rule, the script prints one JSON line. It names what broke and tells the session
to hold its reply until a correction goes out. A clean turn gets no output.

On a document, `scripts/preshow-register-lint.py` makes the call, at the moment a document is about to
be shown to a person. One call took about 33 seconds when it was measured on 2026-07-17, almost all of
it the harness starting up, so the call stays off unless the environment variable
`PRESHOW_REGISTER_JUDGE` is set to `1`:

```
PRESHOW_REGISTER_JUDGE=1 python3 scripts/preshow-register-lint.py docs/language-defects.md
```

Either script stands down on its own breakage: no `claude` binary on the path, a timeout, or an answer
the script cannot parse leaves the text unjudged, says so on standard error, and blocks nothing.

### Running the person catcher

A person reads the text and says where the reading stopped. The section below on the readings that
produced the rules says how one of those readings is run and what it returns.

## What a break costs you

Each entry in `docs/language-rule-coverage.md` carries a status — whether a catcher runs the rule
today — and the event it runs at. That page defines both sets of words at its top, and what a break
costs is read there: a gate refuses a commit or a push, a session hook holds the reply and asks for a
correction, a manual step waits for a person, and many rules are armed nowhere and bind the writer and
the cold reader alone.

The rules are grouped by the kind of text they bind, which the source calls a surface. A surface is a
kind of text and not a file, so one file carries several: the numbered criteria of a spec are one
surface and that same file's paragraphs are another. `docs/language-rules.md` defines the six surfaces
with an example each, and gives the roster of rules binding each one.

## The readings that produced the rules

### Two cold readers, 2026-07-27

The English reader was given six requirements from the spec (`PRODUCT_SPEC.md`) with its glossary held
back, and was asked to name every place the reading stopped. That reader found no fault with the
grammar and called the structure professional work. The text used ordinary English nouns for jobs only
this project knows: seat, net, door, home, walk, lens, handle, frame, law, tier. It also used "red" as
a verb, meaning to report something as a failure.

Of the six requirements, that reader could build two from the text alone. For a third, the reader wrote
down the questions whose answers the requirement was missing; a cold reading has no channel to ask
them, so that requirement stood unbuilt with its questions beside it. The remaining three the reader
did not attempt. The lists and the default values those three rules depend on were never given anywhere
in the text.

The Russian reader was given six paragraphs of working chat, about 250 words, and stopped twenty times.
That is a stop every thirteen words, in a text meant to be read straight through. Every word that
stopped him was made by translating an English term of this project's own into Russian, one word at a
time. The result each time was a real Russian word that carries none of the meaning this project gives
it. `docs/language-rules.md` records those words with their plain replacements, under the rule about a
word standing where a plain standard word exists (`r02`).

That reader also named two habits without being asked: actions handed to things that cannot perform
them, and one thing carrying two names in neighbouring sentences.

### The owner's read of a rewrite

The owner then read a first rewrite, drafted in chat and applying these rules, and stopped six more
times. Two of those six were the rewrite breaking a rule it stated in the same passage.

- One sentence stated the rule that a criterion carries one trigger and one response. It stated that
  rule in two words carried over from English rather than said in Russian: «триггер», the English word
  trigger respelled in Russian letters, and «обязанность», the Russian word for an obligation, standing
  where the response belonged.
- Another sentence banned coined names while coining one: «хвост без глагола», a tail with no verb. The
  thing that phrase points at is real, and it already had a plain name — a clause with no finite verb.
  `docs/language-rules.md` carries it under that plain name (`r36`). The coined phrase went, and the
  class it pointed at stayed.

### A cold reader given the rules page and a real job

On 2026-07-28 a cold reader was handed `docs/language-rules.md` as it then stood, one page carrying
every rule and every catcher together, with a job to judge it against: write one page of documentation
tomorrow and hold it to this rulebook. That reading is recorded at
`docs/language-reads/2026-07-28-read1-language-rules-reference.md`. The reader could apply 30 of the 60
rules, and about 8 of them without an answer to which surface a documentation page is — the surfaces
were the axis the whole page was organized on, and none of them was defined.

Three findings changed the shape of the rules rather than the wording of one entry.

- The reader skimmed four fields in every entry and reported that none of them changes a word a writer
  writes: the file-and-line references, the catcher reach descriptions, the text the judging model is
  handed, and the historical half of the notes. Those four now stand on
  `docs/language-rule-coverage.md`, and the writer's page carries what a writer applies.
- Six rules named a list and gave it nowhere. Every one of those lists now stands inside the rule that
  names it, read out of the checker's own config file at the moment the page is built. Three of the six
  had no such file: their words sat inside a script's regular expressions, where one edit reached the
  checker and no edit reached the page. Those three moved to a config file beside their script, and the
  script now reads its own list from that file, so one edit reaches both.
- Twelve entries were five classes split apart. They are folded into five, and each survivor's notes
  name the ids that were retired.

### The readings of this page

This page has been given to a cold reader six times and has failed every time. The fifth reading is
recorded at `docs/language-reads/2026-07-27-read5-language-defects.md`: 45 stops, 11 of which stopped
the reader from going on. The sixth reading stopped 34 times, 7 of them blocking, and this draft is the
repair of those 7. Readings one through four left no file of their own, and `JOURNAL.md` counts them.

This page is shown to nobody until two cold readings in a row return nothing blocking. That bar is
itself one of the rules (`r54`). A cold reader is the one exception to it: a reading is how the bar
gets measured, so the reader running the read is handed the page while the bar is still unmet.

## One sentence, before and after

Criterion 4 of Requirement 233 in the spec once read as follows, at 107 words counting the bracketed
codes that trail it:

> The system *shall* judge the orchestration members carrying a reminder-history of two or more —
> worker-routing (each unit of work routed to the cheapest tier its step and kind allow),
> lean-orchestrator (heavy reading dispatched to a worker rather than held inline), pull-unblocked-work
> (the session keeps pulling unblocked queue work rather than idling), and classify-the-subtask (a
> subtask is the person's or the seat's by what the subtask itself needs, never by the heading it sits
> under) — their breaks recorded in the one home the break-record law names, the problem ledger
> (`PROBLEMS.md`), and *shall* leave the single-occurrence members as reminders until they recur.
> [INV-241, INV-108, INV-69, INV-137, INV-143]

The bracketed codes at the end are this project's internal identifiers for requirements stated elsewhere
in the spec, and they count toward the 107 words. The sentence carries one instruction together with the
definitions of the four terms it borrowed. The length is what a reader notices first, and those four
definitions are what made it long.

That criterion now reads as follows. The sentence runs to 35 words with the same codes, and its four
members sit in a list below it.

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

Two names inside that quotation carry the word law, and both are the spec's own names for requirements
it states: the orchestration laws are the four members listed under the sentence, and the break-record
law is the requirement naming where a break is written down. On this page, and in
`docs/language-rules.md`, a statement about how a text is written is a rule.

The instruction stayed in the sentence. The four members moved into a list, one to a line, and the
words that defined them moved with them.

## How a class becomes a rule

A class is the shape of a mistake, and one class shows up across many sentences. Repairing the one
sentence in front of a reader leaves every other instance in place. The writer therefore records the
class, and the steps below are how a class becomes a rule.

1. A cold reader stops on a sentence. The writer writes the stop down in that reader's own words,
   including the wrong guess the reader made.
2. The writer traces the wording back to where it was learned: a skill file, a template, a section of
   the spec, or a habit picked up in chat. A class opens once the writer finds the same stop coming out
   of that place again.
3. The writer writes the class into `guardrails/language-rules.json`. The entry carries a name, the
   rule in one sentence, and a question a reader can ask of one sentence. The entry also names the
   surfaces the rule binds, the files that stated the rule in prose before that one home existed, and a
   status saying that nothing catches it yet. Someone then wires or generates a catcher for it, and
   records the catcher under the rule.

A repair applied to one sentence and nowhere else means step 3 was skipped, since only an entry in the
source carries a repair past the sentence that prompted it. A list of examples with no class named
above it breaks the rule that governs how the source grows (`r61`).

## What no script and no model finds

No script and no model finds a class nobody has met yet. Both re-catch what a person already caught
once. Every rule in `docs/language-rules.md` exists because a person stopped on a sentence and said so.
Cold reading is a standing cost, and a project plans and funds it every round.

A literal pattern holds only the instances someone already met. On 2026-07-17
`scripts/preshow-register-lint.py` was handed a Russian text carrying the same loan-translations its own
list names, and it passed that text clean.

A model reads for the class itself, so it catches an instance no list holds. It also reports sentences
that turn out to be no defect at all. A person settles what neither of them can.

## Using this tomorrow

Open `docs/language-rules.md`, find the surface you are writing on, and read the rules its roster
names. Each rule there carries one question to ask of one sentence. Ask those questions of the
sentences you are least sure of, and of every sentence that states a rule. The sentence carrying a rule
is the first test of that rule.
