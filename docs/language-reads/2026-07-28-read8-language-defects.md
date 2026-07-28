# Blind read, 2026-07-28 — the language-defects document, read eight

The reader met this text with no context: one file, no repository access, no history of the
document's earlier rounds. The brief asked for every place the reader stopped, sorted into stops
that blocked the reader and stops the reader noticed and read past.

Reader: a working software engineer persona, clean context.
Text read: `docs/language-defects.md` after the runbook material moved to the maintainer's page and
this page went back to being the record.
Stops: 28 — 6 blocking, 22 non-blocking.

The four readings of this page, oldest first: 45 stops with 11 blocking, 34 with 8, 27 with 12, and
28 with 6. The bar is two consecutive readings with no blocking stop.

---

I read the file once, straight through. Here is what happened.

# Stops

**1.** `the one demand a text owes its reader;`
The contents list says the text owes the demand. The section itself says "The writer owes the reader every word…". I re-read to work out whether "demand" is the thing owed or the thing making the claim. I needed one of the two phrasings used in both places.

**2.** `A **rule** is one statement about one class — the sentence that removes the mistake, a q`
The sentence says a rule is one statement, then lists three things it contains, the third being "what finds a break". The next sentence defines "catcher" as its own word for that same third thing. Two paragraphs later the writer's page is described as carrying the sentence, the question, surfaces, examples, exceptions, thresholds and lists — no catcher — and the maintainer's page carries the catchers. So the definition of a rule includes a part that the document later moves out of the rule's own page. I needed the definition to name the parts a rule has and leave the catcher out, or say plainly that a rule has a part that lives elsewhere.

**3.** `A **catcher** is whatever finds that break`
"Break" is used here for the first time and is never defined, while class, rule, catcher and surface each get a sentence. I guessed it means one occurrence of the mistake in a real text — an instance of a rule being violated. Moderately sure. Later "each break is recorded in the problem ledger" is about a project law being broken, which fits the same guess, so I carried it. I needed "break" in the four-word list, since it is load-bearing on this page ("where a break is written down", "what a break costs at each of those moments").

**4.** `This project names six surfaces — spec-body, human-prose, chat, artifact, commit, and w`
Six names, no definitions, with a pointer to the writer's page. I do not know what "artifact" or "worker-brief" cover, and I cannot tell which one a page like this one is. The document reports that exactly this gap blocked a reader on 2026-07-28. I read on because the page states it is deliberate. I needed one clause per surface, or an explicit note that the reader of this page never needs to place a text on a surface.

**5.** `- **The reader** reads that text afterwards, carrying whatever context they happen to ha`
Set against: `The reader brings nothing to the text — no repository, no earlier draft, and no answer given in some conversation`. The roles section gives the reader whatever context they have; the demand section gives the reader nothing, which is the cold reader's definition. I stopped and could not tell which reader the one demand is written for. If the demand is about the cold reader, the roles list separates two things that the demand treats as one. I needed the demand to name which of the two roles it binds.

**6.** `**The owner** is the person whose project this is. He reads drafts and stops on sentence`
"He" arrives with no antecedent beyond "the person". I could not tell whether the owner is one specific named individual whose readings are recorded below, or a role any project fills. It matters, because the readings section says "the owner stopping" produced rules. I needed one clause saying whether the owner is a role or a person.

**7.** `The text used ordinary English nouns for jobs only this project knows: seat, net, door, h`
Ten words. Four of them (seat, home, law, tier) get definitions 130 lines later, in a section about a different topic. Net, door, walk, lens, handle and frame get none anywhere. I guessed nothing for those six; I read them as a list of samples that I am not expected to understand. I needed the sentence to say that the list is illustrative and that none of the ten is used on this page — except four of them are used on this page.

**8.** `Of the six requirements, that reader could build two from the text alone.`
"Build a requirement" — I guessed it means implement the described behaviour in code from the requirement's text alone. Fairly sure, because the next sentences talk about missing lists and default values. I needed the verb once in a form that names the object, such as "could implement two of the six".

**9.** `For a third, the reader wrote down the questions whose answers that requirement was miss`
I re-read this twice. "the questions whose answers that requirement was missing" made me hold three nouns at once before the relation resolved. I needed something like "wrote down the questions the requirement left unanswered".

**10.** `under `r02`, a coined, loan-translated, or respelled word standing where a plain standard`
On first pass I read the trailing phrase as a description of what the writer's page records. It is the rule's short name, per the convention stated at line 41. I re-read to place it. The same shape appears at `r36`, `r54` and `r61` and reads the same way each time. I needed the short name set off, in quotes or italics, so it does not read as continuing prose.

**11.** `it already had a plain name — a clause with no finite verb` against `as `r36`, a criterion closing on a phrase with no finite verb`
"A clause with no finite verb" and "a phrase with no finite verb" appear one sentence apart for what I take to be the same thing. Clause and phrase are not interchangeable in grammar. I could not tell whether the rule name is a loose restatement or whether the rule is deliberately wider than the plain name. I needed the same noun in both places, or a sentence saying why they differ.

**12.** `Without an answer to which surface a documentation page is, about eight of the thirty rem`
Two things. "About eight" is approximate, in a paragraph that otherwise quotes exact counts from a recorded reading (thirty, sixty, 45, 11, 34, 8, 27, 12); the reading file presumably has the exact number. And "remained" needed a re-read to resolve as "remained applicable". I needed the exact count and an explicit verb.

**13.** `The writer's page defines all six surfaces today, and the two statements are one day apar`
I stopped on "the two statements" and went back to find them. They are the claim in this paragraph and the finding in the paragraph before it. I needed them named, for example "the reading's finding and the state of the page today".

**14.** `The reader skimmed four fields in every entry and reported that none of them changes a wo`
"Skimmed" reads as a description of reading speed. From the rest of the sentence I take it to mean the reader passed over those fields without using them. Moderately sure. I needed the intended verb — "skipped", or "read and did not use".

**15.** `Twelve entries split five classes into pieces.`
I parsed this as "twelve entries, which are the pieces of five classes" only on the second read; on the first, "split" read as a past-tense action the entries performed on something else. I needed "Twelve entries were five classes cut into pieces" or similar.

**16.** `Readings one through four left no file of their own, and `JOURNAL.md` counts them.`
Two stops. "Counts them" — I guessed it means JOURNAL.md is where the fact that those readings happened is recorded, so the count of seven can be checked. Not confident; it could also mean the journal holds the stops themselves. And `JOURNAL.md` is the one pointer on this page whose contents I cannot infer — `docs/language-reads/` gets a full sentence describing what a file there holds, the two built pages each get a paragraph, but the journal gets a filename. I needed a clause saying what the journal holds.

**17.** `on the words that say whether a catcher runs a rule today, and on the names of the moment`
Two things I could not picture. "The words that say whether a catcher runs a rule today" — I guessed a status field with values such as armed / not yet wired. "The names of the moments a catcher fires" — I guessed commit time, push time, and before something is shown to a person, because a gate is defined at the top as refusing a commit or a push. Both guesses low confidence.

**18.** `and all three of those stand on the maintainer's page`
The three are: the six surfaces, the status words, and the names of the moments. But the writer's page was described as the place that "defines each of the six surfaces with an example", and the closing section sends me to the writer's page for exactly that. So the surfaces are placed on both pages, in two sentences that contradict each other. Acting on this sentence, I would open the maintainer's page to find out what surface my text is on and not find it. I needed the surfaces removed from this list, or an explanation that they appear on both pages for different purposes.

**19.** `That bar is itself one of the rules (`r54`, a changed section shipped without a cold read`
The bar just stated is two clean readings in a row. The rule's short name names one cold reader. I could not tell whether `r54` requires one reading or two, and the short name is what a writer would carry away. I needed the rule name and the bar to state the same count.

**20.** `The sentence runs to 35 words with the same codes, and its four members sit in a list bel`
The list below has five bullets. The fifth is the break-recording instruction. I counted twice. I needed either "four members and the recording instruction" here, or the fifth bullet folded back.

**21.** `The instruction stayed in the sentence. The four members moved into a list`
In the before version, "their breaks recorded in the one home the break-record law names, the problem ledger" is part of the instruction. In the after version it is bullet five. So part of the instruction moved into the list, which is what this sentence says did not happen. This is the page's one worked example of a repair, and I would have described the repair wrongly from this summary. I needed the summary to match the two quotations.

**22.** `the orchestration members` (before) / `the orchestration laws` (after) / `the orchestration laws are the four members listed under the sentence`
The same four things are called members and laws within one section. The gloss appears fourteen lines after the switch. The document itself lists "one thing carrying two names in neighbouring sentences" as a habit a reader flagged. I needed one name, or the gloss placed at the switch.

**23.** `The bracketed codes at the end are this project's internal identifiers for requirements st`
The lead-in already said "at 107 words counting the bracketed codes that trail it". The fact that the codes count toward 107 is stated twice, eight lines apart. I stopped, went back to check I had not misread the first one.

**24.** `Someone then builds or wires a catcher for it, and records that catcher under the rule.`
"Someone" is the only actor in the three-step procedure who is not one of the four roles the page defines. I could not tell whether this is the writer, the owner, or a fifth party, and the step is the one that closes the loop. I needed the role named.

**25.** ``r61`, a defect recorded as examples with no class behind them` and ``r36``, against `Thirty of the sixty rules`
The identifiers run past 61 while the count given is sixty. I take it that retired identifiers are not reused, since twelve entries were folded into five, but the page never says so, and the two numbers sit in the same document. I needed one sentence saying identifiers are never reused.

**26.** `On 2026-07-17 the pattern pass of `scripts/preshow-register-lint.py` … was handed a Russian text carrying the same loan translations its own list names, and it passed that text clean.`
The loan translations under `r02` come from the Russian cold reader's twenty stops on 2026-07-27, ten days later. So on 2026-07-17 the script's list either did not yet contain those words, or it contained them from some earlier source the page does not mention. As written, the example does not establish what the section claims it establishes — that a literal pattern misses instances it already lists. I needed the provenance of the script's list, or a date after the list was populated.

**27.** `find the one you are writing on and read the rules listed under it, which are the whole se`
Earlier, each rule "binds" a set of surfaces, so a rule binds more than one. Here rules are listed under a surface as the complete governing set. I could not tell whether a rule binding three surfaces appears three times on the writer's page. Non-critical, but I stopped on "the whole set".

**28.** Line 254 in the raw file runs unwrapped to roughly 160 characters while every other line wraps near 100. I noticed it while reading the source. It disappears in a rendered view.

**Stop count: 28.**

# Answers

**1. What is this document for, who reads it, when.**
It is the record of where this project's writing rules came from: which readings stopped, on what, and what rule each stop produced. The page states its own reader in one line — read it to know why the rules say what they say — so its reader is someone questioning a rule, or someone about to add one. It is not the page you open to write; it says so and hands you off.

**2. Do I know what the other documents hold and when to go there.**
For the two built pages, yes. The writer's page holds the rule sentence, the question, the surfaces, examples, exceptions, thresholds and lists, and I go there to write. The maintainer's page holds catchers, their reach, where each is armed, how to run one by hand, what a break costs, and the prose history, and I go there to run or repair a catcher. The split is stated twice, once as a list and once as a two-sentence instruction. `docs/language-reads/` is described well enough that I know what one file there contains. `JOURNAL.md` is a filename only. `guardrails/language-rules.json` I know as the one place a rule is edited. The one place I would go wrong is the surfaces, per stop 18.

**3. Could I use this page tomorrow for the job it claims.**
For its stated job — knowing why a rule exists — yes, for every rule the page traces. For the last section's job, no: the page names six surfaces and defines none, so "find the one you are writing on" runs only after I open the other page. I would ask the author: which page defines the surfaces (stop 18); whether the one demand binds the reader or the cold reader (stop 5); whether the after-list has four members or five and whether the recording instruction moved (stops 20, 21); and where the lint's word list came from on 2026-07-17 (stop 26).

**4. What read clearly on the first pass.**
The opening definition of live-spec and of a gate. The two-page split and the three-line instruction on which to read when. The one demand, taken on its own. The bullet on the six rules that named a list and gave it nowhere, including the three whose words sat inside regular expressions. The three-step procedure for turning a class into a rule, apart from "someone". The two quoted versions of the criterion, read as text. The closing section on what a script and a model cannot find, apart from its dated example.

**5. Blocking and non-blocking.**

BLOCKING — I could not proceed, or I would have acted on the page wrongly: 2 (a rule's parts contradict where the parts are kept), 5 (two definitions of the reader under the page's central claim), 18 (would send me to the wrong page for the surfaces), 20 and 21 (the worked example's summary disagrees with the worked example), 26 (the evidence is dated before the list it depends on).

NON-BLOCKING — noticed and read on: 1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 22, 23, 24, 25, 27, 28.
