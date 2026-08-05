# Where the language rules came from

This document is the record behind the rules this project states about its own writing. It answers one
question: why does a given rule say what it says. It covers the readings that produced the rules, and
the procedure that turns a repeated reader stop into a rule.

live-spec is this project: a set of skills, scripts, and gates that a person and an agent use together
to write, prove, and ship software. A gate is a script that refuses a commit or a push when the thing
it guards is wrong. The texts described below are this project's own documents.

Three pages carry these rules, and each has one reader.

- `docs/language-rules.md` is the writer's page. It states every rule in the words a writer applies to
  a sentence, and it defines the six surfaces with an example of each.
- `docs/language-rule-coverage.md` is the maintainer's page. It carries what catches a break of each
  rule, how far that catcher reaches, where it is armed, and how to run each kind of catcher by hand.
- This page is the record. Read it to know why a rule exists.

Each rule carries a short identifier such as `r02`, and this page names a rule by that identifier
together with the rule's short name in italics, a clause naming the defect the rule removes. An
identifier is never reused: a retired rule takes its identifier out of the set, and no later rule takes
it back.

<!-- generated:rule-home-totals — scripts/gen-language-consumers.py owns the block below -->

The rule home carries 66 rules and its highest identifier is `r75`, so nine stand retired.

<!-- /generated:rule-home-totals -->

Of those, seven went in the fold recorded below, `r22` was folded into `r01` earlier, and `r28` left
with no record of why.

<!-- generated:vocabulary — scripts/gen-language-consumers.py owns the block below -->

## The words on this page

The words these rules are stated in. Every page built from this home carries this block, so a reader holding one page holds every word that page uses. A word is defined here when two or more pages need it; a word one page alone needs is defined on that page.

- **class** — the shape of a mistake: the form it takes wherever it turns up.
- **break** — one place a text falls short of a rule, being a single instance of the class that rule names.
- **catcher** — whatever finds a break: a literal pattern in a script, a model reading for meaning, or a person reading the text.
- **home** — the one file a given fact is written in.
- **the rule home** — the file `guardrails/language-rules.json`, where every rule is edited and nowhere else, and from which every page here is built.
- **rule** — one statement about one class, written as one entry in the rule home.
- **surface** — a kind of text rather than a file, so one file carries several; this project names six, and each rule binds the ones it applies to.
- **stop** — one place a reader could not go on, had to read twice, or had to guess.
- **a blocking stop** — a stop where the reader could not go on with the text, or would have acted on the text wrongly; every other stop is one the reader noticed and read past.
- **register** — the rules a surface's text is held to: which words, which sentence shapes, and how it addresses its reader.

Five roles appear wherever these rules are discussed.

- **the writer** — whoever drafts a text: a person, or the agent working for one.
- **the reader** — whoever reads that text afterwards, carrying whatever context they happen to have.
- **a cold reader** — a reader given the text alone, with no repository, no earlier drafts, and no way to ask the writer a question.
- **the maintainer** — whoever builds the catchers and repairs them.
- **the owner** — the one person whose project this is.

One person often holds more than one of these roles in a day.

<!-- /generated:vocabulary -->

Three words on this page name three different things, and one of them was long written as one word for
all three. The **rule home** is the file every rule is edited in. **Where a wording was learned** is the
skill file, template, or habit a defect came out of, and this page says that in full each time. The
`sources` field on a rule entry is neither: it lists the files that stated that rule in prose before the
rule home existed, and the maintainer's page prints it.

## How a cold reading is run

Every cold reading recorded below was made by a model in a fresh session with none of this project
loaded. The procedure stands in `skills/text-audit/SKILL.md`, and the prompt handed to the reader
stands beside it in `skills/text-audit/references/reader-prompt.md`; a reading comes back as a file
under `docs/language-reads/`, named for its date and its number.

A single stop is written down and opens nothing. A rule enters this project when the place that produced
that stop produces it again, the second occurrence proving the wording's origin rather than the one
sentence. Some rules came from a cold reader stopping and some from the owner; the readings below name
which produced what.

## The one obligation

The writer owes the reader every word, number, and list the writing depends on. That debt is measured on
a cold reader, who brings nothing to the text. Each of those words, numbers, and lists therefore stands
where it is used, or in one named place the sentence points to. A text that holds for a cold reader
holds for every other reader, whatever context that reader arrived with.

Every rule on the writer's page names one way a text falls short of that obligation.

## The readings that produced the rules

The last section below holds this page's own readings, which are still going on.

### Two cold readers, 2026-07-27

The English reader was given six requirements from the spec (`PRODUCT_SPEC.md`) with its glossary held
back. The text used ten ordinary English nouns for jobs only this project knows, and used "red" as a
verb meaning to report something as a failure. Four of the ten — home, seat, law, and tier — turn up
again on this page. All of them stand here as instances of the class this reader met, and not as a
vocabulary to carry onward. That finding opened no rule of its own. The class was already in the rule
home as `r01`, *an ordinary word carrying a private project meaning*, whose entry names the skill and
profile files that stated it in prose before the rule home existed, so this reading stands as evidence
for that rule rather than its origin.

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
stopped at six of its sentences. Two of the six were the rewrite breaking a rule in the same passage
that stated it, and this page carries those two.

- One sentence stated the rule that a criterion carries one trigger and one response, and broke two
  rules while stating it. «Триггер» is the English word trigger respelled in Russian letters, where
  Russian already has a plain word for it, which is `r02`. «Обязанность» is a plain Russian word
  standing in the wrong slot: it means an obligation, and it stood where the response belonged, which
  is the one-trigger-one-response rule the sentence had just stated.
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
`docs/language-reads/2026-07-28-read1-language-rules-reference.md`.

That reader could apply thirty of the sixty rules the rule home then carried to tomorrow's page. Eight
of the thirty need no judgment at all, because each ships a word list or a fixed shape; the reading
names those eight by identifier, and the other twenty-two turn on the reader's own judgment. All thirty
assume an answer to which surface a documentation page is: it is human-prose, and it carries the
artifact surface as well once it is published outside the project. Without that answer a writer is left
with the four rules that bind every surface: `r10`, *a thing named by denying its neighbour*; `r12`, *a
word grading how important or how good a thing is*; `r18`, *the language each surface is written in*,
which puts documents and published pages in English and conversation in the owner's own language; and
`r61`, *a defect recorded as examples with no class behind them*. The surfaces were the axis the whole
page was organized on, and the page defined none of them. The writer's page carries all six today,
placing a documentation page among them, written later that same day in answer to this reading.

Three findings changed the shape of the rules rather than the wording of one entry.

- The reader passed over four things carried in every entry and reported that none of them changes a
  word a writer writes: the files that stated the rule in prose before the rule home existed; two
  pieces of what catches a break, being how far each catcher reaches and the text the judging model is
  handed; and the half of the notes carrying what the entry was folded out of. All four are the
  maintainer's material, all four now stand on the maintainer's page, and the writer's page carries what
  a writer applies.
- Six rules named a list and gave it nowhere. A script catcher keeps the words it matches in a
  configuration file of its own, beside the script, as `guardrails/weak-words.json` stands beside
  `guardrails/check-weak-words.py`. Every one of those six lists now stands inside the rule that names
  it, read out of such a file at the moment the page is built. Three of the six had no such file: their
  words sat inside a script's regular expressions, where one edit reached the script and no edit reached
  the page. Those three lists moved into a configuration file beside their script, and the script now
  reads its own list from that file, so one edit reaches both.
- Five classes stood spread across twelve entries. The twelve are folded back into five, and each
  survivor's notes name the identifiers retired.

### The readings of this page, 2026-07-27 to 2026-07-28

This page has been given to a cold reader thirteen times and has failed every time. The bar is two
readings in a row returning nothing blocking, and that bar is itself one of the rules (`r54`, *a changed
section shipped before two clean cold readings*). Until it is cleared this page is shown to nobody, with
one exception: a reading is how the bar gets measured, so the reader running one is handed the page
while the bar is still unmet.

- Readings one through four left no file of their own. `JOURNAL.md`, this project's dated log of what
  changed and why, carries them in a single sentence: that the page failed four readings and took five
  repair rounds. It gives no stop count and no finding from any of the four.
- Readings five through thirteen each left a file under `docs/language-reads/` named for its date and
  its number, the fifth being `2026-07-27-read5-language-defects.md`. The fifth ran on 2026-07-27 and
  the rest on 2026-07-28. In order they returned 45 stops with 11 blocking, then 34 with 8, 27 with 12,
  28 with 6, 31 with 5, 25 with 5, 25 with 6, 25 with 5, and 28 with 8.

The blocking count over those nine readings ran 11, 8, 12, 6, 5, 5, 6, 5, 8, and never approached zero.
Two things kept it there, and both are visible in the readings themselves.

The seventh reading returned fewer stops than the sixth, at 27 against 34, and more blocking ones, at 12
against 8. Between those two readings this page had taken on instructions for running the catchers, and
four of the seventh reading's twelve blocking stops sat on that new material: two on one script given as
an example of a script catcher and called the model catcher twenty-five lines later, one on a section
headed for running the person catcher that carried no procedure, and one on a command line carrying two
placeholders the page gave no way to fill. Every repair round had been adding words, and each new reader
met the seam where the newest words joined the old. Those instructions moved to the maintainer's page,
which defines the words they rest on.

The thirteenth reading's eight blocking stops were then read as one set rather than eight repairs, and
seven of the eight were one class: the page used a word, a list, or a claim whose ground stood a hundred
lines further down, in another file, or in three senses at once. Six surface names arrived with their
definitions on the writer's page. The words seat, law, and tier were used from the top of the page and
defined near its end. One word, source, carried the rule home, the origin of a wording, and the name of
a field. A list of the fifteen parts of a rule entry was given as the list to write a new entry against,
while three parts the page later relied on stood nowhere in it.

The repair was structural. The shared words moved into the rule home and are generated into this page
and both others, so each page carries every word it uses. The list of the fifteen parts of an entry
moved to the maintainer's page, whose reader is the one who writes entries. The runbook for the
catchers had already gone there. The worked example of one repaired spec sentence moved to
`docs/language-worked-example.md`, the home for a rule shown applied to a real text. The procedure for
running a cold reading stayed in `skills/text-audit/SKILL.md` and this page now points at it. What is
left here is the record itself, at half the length it stood at.

### The readings of the text-audit skill, 2026-07-29

Readings twenty-one and twenty-two ran on `skills/text-audit/SKILL.md` and its two reference files.
Both stand under `docs/language-reads/`. Each returned 46 stops, nine blocking in the first and four in
the second. The repair round closed four of them: the undeclared surface, the unnamed record, the roles
sentence, and the law about fresh readers. Every stop below still stands, with the reading that found it.

The stops still marked blocking:

- "Every rule binding either surface is then in force" — 21, and 22 as non-blocking
- "25 words for a human-prose sentence, and 35 for a spec-body criterion" — 21, 22
- "its Context paragraph, its User Story, and its acceptance criteria" — 21
- "A rule binds a whole region of the file" — 21, 22
- "Run the audited project's own suite command, whatever it is" — 21, 22
- "It counts findings per file", read against a README — 21, 22
- "The method's build-test evidence is owed" — 21, 22

The stops both readings made, marked non-blocking:

- "Part of the live-spec pack" — 21, 22
- "Four scopes settle a setting there" — 21, 22
- "Used on its own, this skill is plain advice a person applies by hand" — 21, 22
- "It runs on any text a person will read" — 21 on the pronoun, 22 on "a decision page"
- "Those readers found new blocking terms on every pass" — 21, 22
- "the three words above" — 21, 22
- "a handful of sentences" — 21, 22
- "the map a script builds from the body criteria at freeze" — 21, 22
- "one architecture node with one spec fact", and the test level beside it — 21, 22
- "runs the census comparison over every live document" — 21, 22
- "A project holding no such file gets one" — 21, 22
- "Which copy of that list a run reads" — 21, 22
- "a fresh worker with the pack not loaded", one role under five names — 21, 22
- "a bracketed query in the draft" — 21, 22
- "Four of those rules bind every sentence of this file" — 21, 22
- "A new slot-opening word joins the weak-word list" — 21, 22
- "Two of those pages carry more than this sheet does" — 21, 22
- "The case is written text on the left and its repair on the right" — 21, 22
- "the rule home", used as a defined term — 21, 22

The stops reading twenty-one made alone:

- "The loop came from the comprehension gate on spec sections" — 21
- "its clarity matters" — 21
- "whatever writing skills the host installs beside the pack" — 21
- "no stranger returns to it" — 21
- "The five lints under The mechanical lints are that whole set" — 21
- "A fresh reader holds that much" — 21
- "A rewrite that moves one of them" — 21
- "The third is four commands of its own" — 21
- "the three guarded documents match the frozen baseline" — 21
- "Each lint names a script and a grep fallback", against two scripts below — 21
- the eleven weak words run inline in one sentence — 21
- "The last one shows up as" — 21
- "No named thing appears under two names" — 21
- "An undefined term the rest of the text leans on blocks" — 21
- "A passing run prints one line saying that the file is clean" — 21
- the census fact stated a second time — 21
- "ask the three questions", in the reader prompt — 21
- "The harness task panel" and "package rules", in the printed rule sheet — 21

The stops reading twenty-two made alone:

- "the auditor — the session running this skill", read in the by-hand mode — 22
- "a repair inside those lines cannot break a requirement a hundred lines away" — 22
- "Four things change there", against six statements below — 22
- "It reads three things nobody would ask of a README", stated twice — 22
- "The architecture document, the recorded decision, and the test matrix" — 22
- "`--compaction`" — 22
- "the reader meets it before the noun's first working use" — 22
- "the nouns this project coined", asked of a reader without the project — 22
- "A mechanical hit is fixed before the cold reader runs", a third statement — 22
- how a pack gets loaded or unloaded — 22
- "A finding blocks when the reader cannot act on the text", copied into the prompt — 22
- "The same editor runs one cold-reader loop" — 22
- "The prompt names five stop classes", against "every other class" — 22
- "A documentation page carries `artifact` as well" — 22
- "`the door` → `the entry point`", a substitution with no sentence around it — 22
- the repair text under `r10`, written in capitals against `r23` — 22
- "A long run of peer items is gathered under headed parents", under 48 peer bullets — 22

Readings twenty-five and twenty-six ran on the same three files, and both stand under
`docs/language-reads/`. They returned 53 and 38 stops, eight blocking in the first and five in the
second. The round closed three: how much of the register the sheet prints, the test for a blocking
finding, and where the requirement-shape lint sits. Every stop below still stands, with the reading that
found it.

- "It states the register it holds a text to", in the description — 25
- "Part of the live-spec pack" — 25, 26
- "Four scopes settle a setting there" — 25, 26
- "settle", read as decides, as fixes, and as arrived at — 26
- "Used on its own, this skill is plain advice a person applies by hand" — 26
- "repairs the places where they stop", with "stop" undefined — 25
- "The loop came from the comprehension gate on spec sections" — 25
- "The findings reached zero only after two reads in a row" — 25, 26
- "Every reading is written to a dated reading record", against the defects file — 25, 26
- "the cold reader is never either of them" — 25
- "the auditor — the session running this skill", read in the by-hand mode — 26
- "A surface is a kind of text", stated twice — 25, 26
- "The auditor names the text's one primary surface" — 25
- "It holds that text to the register of the text's own primary surface" — 26
- "25 words for a human-prose sentence, and 35 for a spec-body criterion" — 25, 26
- "a stop in one place stands for that class everywhere else" — 25
- "the three words above" — 25
- "its clarity matters" — 25
- "it queues for the person's taste call" — 25, 26
- "The comprehension gate settled on two reads" — 25
- "a handful of sentences" — 25, 26
- "A whole-page run puts every sentence of that page in front of one" — 25, 26
- "its Context paragraph, its User Story, and its acceptance criteria" — 25
- "a repair inside those lines cannot break a requirement a hundred lines away" — 25, 26
- "Four things change there", against six statements below — 25
- "plus the findings of the style lint and of the register lint" — 26
- "the map a script builds from the body criteria at freeze" — 25, 26
- "one architecture node with one spec fact", and the test level beside it — 25
- "The third is four commands of its own" — 25, 26
- "Run the audited project's own suite command, whatever it is" — 25
- "the three guarded documents match the frozen baseline" — 25, 26
- "the frozen baseline", met before it is defined — 26
- "runs the census comparison over every live document" — 25, 26
- "The build test measures the work once the audit has closed" — 26
- "which takes the count before and after each batch" — 26
- "Nothing names the requirements one ran on" — 26
- "The method's build-test evidence is owed" — 25, 26
- "the mechanical layer", a second name for the mechanical lints — 25
- "Which copy of that list a run reads" — 25
- "Context comes before criteria", stated twice — 25
- "A sentence past the cap for its surface is a hit" — 25
- "No named thing appears under two names" — 25
- "so no reader spends a finding on a class a machine already owns" — 25
- "a fresh worker with the pack not loaded" — 25, 26
- "a writer or reader holding the project's rules is kept apart from one who does not" — 26
- "An undefined term the rest of the text leans on blocks" — 25
- "a bracketed query in the draft" — 25
- "Inventing an answer to close a finding is the one move this skill forbids" — 25
- "A passing run prints one line saying that the file is clean" — 26
- the census gate stated a second time — 26
- "The same editor runs one cold-reader loop" — 25, 26
- "The prompt's last instruction takes every other stop the reader met" — 25, 26
- where the reader's report goes, absent from the pasted block — 25
- "A word the list above does not name", carrying no blocking mark — 25
- the eleven weak words standing in two files — 25
- "A new slot-opening word joins the weak-word list" — 26
- "Two of those pages carry more than this sheet does" — 25, 26
- "the rule text the judging model reads" — 26
- "Every case the class was built from lives in the rule home" — 25
- "The case is written text on the left and its repair on the right" — 25, 26
- "`the door` → `the entry point`", a substitution with no sentence around it — 26
- the repair under `r09`, 41 words against the 25-word cap it states — 26
- "A long run of peer items is gathered under headed parents", under 48 peer bullets — 25, 26
- the repair under `r64`, running its four items along one line — 25
- "the harness task panel" and "pinned language", in the printed sheet — 25

### The readings of the text-audit skill, 2026-08-05

Readings thirty and thirty-one ran on `skills/text-audit/SKILL.md`, and both stand under
`docs/language-reads/`. They returned 30 and 31 stops, eight blocking in each. The repair round closed
eight passages. Both readings marked five of those eight blocking. The other three blocked in reading
thirty-one alone, and reading thirty stopped on two of the three without marking them blocking. One of
the five repairs also closed a stop reading thirty alone marked blocking, since both stops sat in one
paragraph. A later commit closed the two passages left. Reading thirty alone marked each one blocking:
the lints a spec section alone runs, and refutation as a step of the loop. Every stop below stands,
with the reading that found it.

The stops one reading made alone:

- "Part of the live-spec pack", with no word for what a pack obliges — 30
- "Three roles run through this skill", against five bullets below — 30
- "When it fires", where nothing above has been named an event — 30
- "Those stops are the strongest", carrying no measure where it stands — 30
- "the three guarded documents match the frozen baseline", both terms unmet — 30
- "The structure checks, third in the list", pointing by position — 30
- "It measures the work once Step 5's two clean rounds close the audit" — 30
- "Both passes run on every audit, whatever the budget allows" — 30
- "an image with no referent" — 30
- "That run reproduced the split", with two splits standing nearby — 30
- "records this file at zero findings", the census rule stated a second time — 30
- "The loop closes when both readers of a round return zero blocking findings", a third statement — 30
- "read a text as a stranger", against the cold reader named below it — 31
- "the reader it is written for", a second sense of reader — 31
- "The loop came from the comprehension gate on spec sections", the ground left unstated — 31
- "a worker brief", named twice and never described — 31
- "its clarity matters", carrying no measure and no judge — 31
- "whatever writing skills the host installs beside the pack" — 31
- "a checkpoint", absent from the six named surfaces — 31
- "The plan chose that size for two reasons", the two never confirmed — 31
- "A rewrite that moves one of them breaks a test", with four candidates for them — 31
- "one architecture node with one spec fact and pin the test level that covers it" — 31
- "The architecture document, the recorded decision, and the test matrix", met before the file is
  named — 31
- "a cold reader who puts the old text and the new text side by side", a task the role never carries — 31
- "A count above the record fails, and the batch runs again", with no owner for the rerun — 31
- "marker lines", never told apart from anchors — 31
- "`docs/spec-style.md` states that separation", the separation left unstated — 31
- "A passing run prints one line saying that the file is clean", with clean unmeasured — 31

The stops both readings made, marked non-blocking:

- "Four scopes settle a setting there" — 30, 31
- "Those readers found new blocking terms on every pass" — 30, 31
- "the cold reader is never either of them" — 30, 31
- "25 words for a human-prose sentence, and 35 for a spec-body criterion" — 30, 31
- "a handful of sentences" — 30, 31
- "runs the census comparison over every live document" — 30, 31

## How a class becomes a rule

One class shows up across many sentences, so repairing the one sentence in front of a reader leaves
every other instance in place. The writer therefore records the class, and the steps below are how a
class becomes a rule.

1. A reader stops on a sentence. That reader is a cold reader or the owner, and both have opened rules.
   The writer writes the stop down in that reader's own words, including the guess the reader made
   there.
2. The writer traces the wording back to where it was learned: a skill file, a template, a section of
   the spec, or a habit picked up in chat. A class opens once the writer finds the same stop coming out
   of that place again.
3. The writer writes the class into the rule home as one entry. The maintainer's page states every part
   an entry carries and is the list to write a new entry against. The status on a new entry says that
   nothing catches the rule yet. The maintainer then builds or wires a catcher for it and records that
   catcher under the rule.

A repair applied to one sentence and nowhere else means step 3 was skipped, since only an entry in the
rule home carries a repair past the sentence that prompted it.

A list of examples with no class named above it breaks the rule that governs how the rule home grows
(`r61`, *a defect recorded as examples with no class behind them*).

## What no script and no model finds

No script and no model finds a class nobody has met yet: both re-catch what a person already caught
once, and every rule on the writer's page exists because a person stopped on a sentence and said so.
Cold reading is therefore a standing cost, and a project plans a reading into every round of revision.

A literal pattern holds only the instances someone already met, and one measurement on this project's
own lint says how narrow that is. The pre-show lint is `scripts/preshow-register-lint.py`, the script
that reads a document about to be shown to a person for the level and tone of its language. It makes
two passes over that document: a list of literal patterns, and one model call. Every pattern in that
list was folded in between 2026-07-05 and 2026-07-10, each beside its date.

On 2026-07-17 the list was handed one Russian sentence carrying two of this project's coined names
translated word for word. Both coinages already stood in the pattern list in their English form, one
pattern each. The list passed the sentence clean, because it had met the coinage and not that wording of
it. The model call was not made: the script issues it only when it is switched on by hand, the
maintainer's page shows how, and the switch stayed off through the probe. That result stands as a test
in `tests/test_register_judge.py`, where the pattern pass is run for real and the model call is driven
against a written-out reply, so the test proves what the code does with a verdict and never calls a
model itself.

A model is there to read for the class itself, which is how it reaches an instance no list holds; the
probe above measured the list alone and says nothing about the model. A model also reports sentences
that are no defect at all, and a person settles what neither can.
