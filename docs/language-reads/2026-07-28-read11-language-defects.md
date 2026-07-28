# Blind read, 2026-07-28 — the language-defects document, read eleven

The reader met this text with no context: one file, no repository access, no history of the
document's earlier rounds. The brief asked for every place the reader stopped, sorted into stops
that blocked the reader and stops the reader noticed and read past.

Reader: a working software engineer persona, clean context.
Text read: `docs/language-defects.md` after round thirteen cut the closing section, restated the
parts count, and described how a cold reading is run.
Stops: 25 — 6 blocking, 19 non-blocking.

The seven readings of this page, oldest first, by blocking stops: 11, 8, 12, 6, 5, 5, 6. Three of
this reading's six sit on text round thirteen added: the undefined `layer` and `package`, the
standing prompt asking for no guess against the reading files carrying one, and two shapes given for
a reading entry.

---

I read the file once, straight through. Here is what happened.

**File read:** `/private/tmp/claude-501/-Users-sashaabramovich/14f2fe20-40cb-4760-b709-ef591b5eb05c/scratchpad/text-to-read-I.md`

# Stops

**1.** "Seven words carry the weight on this page: class, break, catcher, home, source, sur…"
I stopped to check the promise. Seven words, "the three paragraphs below define them in that order" — I counted: paragraph one carries five of them, paragraph two carries one, paragraph three carries one. The order holds, but I had to do the arithmetic to trust the sentence.
Needed: the count per paragraph, or no promise about paragraph structure.

**2.** "An entry carries fifteen parts in all: ten stand on every entry, and five more stand…"
Re-read. Three groups of five follow, and "ten stand on every entry" maps to the first two groups. I had to hold three numbers (15, 10, 5) against three bullets to see it was consistent.

**3.** "the sentence that removes the mistake; the question to ask of a sentence"
Guessed. I took "the sentence that removes the mistake" to be the rule's directive — the instruction a writer follows — and "the question to ask of a sentence" to be a self-check prompt. Confidence: medium. Neither is named, and both are single phrases doing the work of a definition.

**4.** "an override recording where one reader's own layer holds the rule tighter than the p…"
Stopped hard. "One reader's own layer" and "the package" are both new here. Nothing on the page says what a layer is, who owns one, or what the package is. I guessed: some per-person configuration that can tighten a rule beyond the default. Confidence: low. I could not tell who writes an override or when.

**5.** "live-spec is this project: a set of skills, scripts, and gates that a person and an a…" against "…holds the rule tighter than the package does."
Two names I suspect mean one thing: **live-spec** and **the package**. The page defines live-spec once at the top and then uses "the package" once, 30 lines later, without connecting them. The page itself records `r04`, *one thing answering to a second name*, as a rule.

**6.** "All six are defined, each with an example, on the writer's page named just below."
Two things. "Just below" turned out to be 22 lines later, and I scanned for it. More importantly: surfaces are the axis every rule binds on, and I cannot apply any rule from this page without them. The page says so itself later. I read on, but I could not have used any rule.

**7.** "Nine identifiers stand retired today: the source carries 53 rules, and the highest id…"
Stopped to verify: 53 + 9 = 62. It checks. Later the page says the source "then carried" sixty rules, and that twelve entries folded into five. 60 − 12 + 5 = 53, and 7 more retired identifiers. That also checks. Three separate counts across 100 lines that only reconcile if a reader does two subtractions.

**8.** "a word such as depends or larger with no measure beside it"
I disagreed. "Larger" wants a measure. "Depends" wants a named dependency, which is a different defect. The two examples are given as one class and I could not see the class that holds both.

**9.** "It asks for no fix and for no guess at a missing answer." against "…each stop carrying the guess the reader made there"
Contradiction. The standing prompt is described as asking for no guess. The reading files are described as carrying the guess the reader made, and step 1 of "How a class becomes a rule" says the writer records "the wrong guess the reader made." If I had run a reading off the first sentence I would have withheld exactly what steps 1 and 3 need.
Needed: one statement of whether a reading records the reader's guesses.

**10.** "The reading comes back as a numbered list, one entry to a stop, and each entry carri…"
Four things per entry: the phrase, its location, what a stranger cannot tell, and blocking-or-not. Later, a file under `docs/language-reads/` is described as carrying "what the reader was given, what the reader was asked for, and every place the reading stopped, each stop carrying the guess the reader made there and whether it kept the reader from going on." Those are two different entry shapes. The second drops "what a stranger cannot tell" and adds the guess.
Needed: one specification of a reading entry.

**11.** "The text used ordinary English nouns for jobs only this project knows: seat, net, doo…"
Ten nouns are named. The page then says four of them turn up again and are defined where used. Six — net, door, walk, lens, handle, frame — appear nowhere else and are never explained. The page states this is deliberate ("not as a vocabulary to carry onward"), so I read on, but I finished the page with six words I cannot attach meaning to.

**12.** "the other four are out of scope here"
Stopped and looked for a pointer. None is given. I do not know whether those four owner stops are recorded anywhere or dropped.

**13.** "It stated that rule in two words carried over from English rather than said in Russia…"
Could not parse on first pass. The sentence claims two words were carried over from English, then describes the second, «обязанность», as "the Russian word for an obligation, standing where the response belonged." That is a native Russian word used in the wrong slot, which is a different defect from a word carried over from English. If I had summarized this finding I would have gotten it wrong.
Needed: the two words named as two different defects, or one class that covers both.

**14.** "All thirty assume an answer to which surface a documentation page is."
A rule I could not apply. The page says that without the surface answer the count drops to "the number of the rules binding every surface, and the reading puts no exact number on those." So I know a fallback exists and I do not know its size. I cannot tell how many rules I could hold a page to.

**15.** "That finding and the writer's page as it stands today are hours apart on one day rat…"
Could not parse on first pass. "Hours apart on one day rather than in conflict" compares a time gap against a logical relation. I read the next sentence to recover the meaning: the finding came first, the definitions came later the same day.

**16.** "The reader passed over four things carried in every entry without using any of them,…"
Re-read. The four named — file-and-line references, the reach description inside each catcher, the text the judging model is handed, the historical half of the notes — do not map one-to-one onto the maintainer's five listed at the top of the page. Two of them sit inside a single one of the five ("whatever catches a break"), one is half of another. The sentence says they "sit inside the maintainer's parts named at the top of this page," and I had to go back and do the mapping myself to believe it.

**17.** "`JOURNAL.md`, this project's dated log of what changed and why, is where those four r…"
A pointer I could not size. Readings five through ten each get a stop count and a blocking count. Readings one through four get neither, and I cannot tell from this page whether `JOURNAL.md` holds counts, findings, or a line each. The claim "has failed every time" covers all ten, and for four of them the page shows nothing.

**18.** "…which the instructions gave as an example of a script catcher and then described as …"
Stopped. This is the page reporting a past defect: one script named as two kinds of catcher twenty-five lines apart. Then at the end the same page presents `scripts/preshow-register-lint.py` as making a pattern pass and a model call — both kinds — before disambiguating it 8 lines later. I re-read to check whether the defect had returned.

**19.** "Four words in the two quotations below are the spec's own and belong to no rule about…"
I counted five terms defined in that paragraph: tier, seat, law, the problem ledger, and the break-record law. All five appear in the quotations. Either "break-record law" is being counted as an instance of "law," or the count is off. I could not tell which.

**20.** "This page calls one such failure a lapse, and a lapse is a different thing from a bre…"
Stopped. A new term arrives 245 lines in, and it exists to separate two meanings of "break" — this page's meaning and the spec's. The quotations below use "break" in the spec's sense. The page warns me, and I still had to hold two senses of one word while reading the two quotations.

**21.** "The system *shall* judge the orchestration members carrying a reminder-history of tw…"
The old quotation has "reminder-history" as one hyphenated word; the repaired one has "reminder history" as two. The counting note explicitly covers hyphenated names as one word, so the change shifts the count by one and is never mentioned. I verified both counts by hand: the old runs to 105 with the five codes, the new to 35. Both hold — the hyphen change is absorbed silently.
Also: "reminder history" is used at line 261 and only explained at the end ("a reminder history counts occurrences").

**22.** "Two defects stand in the repaired criterion."
I disagreed with the choice. The page's one worked example of a repair is shown still carrying two named defects, and nothing says whether they were fixed, queued, or left. As a model of what a repaired criterion looks like, I could not tell what I was supposed to copy.

**23.** "the script makes that call over a document only when it is switched on by hand, it st…"
Stopped. How it is switched on is not given, and no pointer is offered at that sentence. The page earlier says running instructions moved to the maintainer's page, so I inferred that is where to look. The inference is mine.

**24.** "The register judge is the model call that script makes, and `hooks/register_judge_cor…"
Re-read. The judge is a model call; a file makes that call; then "the judge is driven against a written-out model reply," which reads like the judge is code being tested. I could not settle whether "register judge" names the call or the code that issues it.

**25.** "This page has been given to a cold reader ten times and has failed every time."
Stopped, because I was reading it. The tenth reading returned five blocking stops and this draft repairs them, so on the page's own bar this draft has not passed. The exception that makes my reading legitimate arrives 35 lines later under `r54`. Between those two points I was reading a document its own rule says is shown to nobody.

**Total: 25 stops.**

# Answers

**1. What is this document for? Who reads it, and when?**
It is the record behind a set of writing rules: where each rule came from, which reading produced it, and one worked before-and-after repair. The page states its own place in a set of three — the writer's page to write, the maintainer's page to run or repair a catcher, this page to know why the rules say what they say. I would read it when I wanted the provenance of a rule, or when I was about to argue with one.

**2. Does this page tell me what the other documents hold and when to go there?**
For the two built pages, yes. `docs/language-rules.md` carries every part of a rule a writer applies plus the six surface definitions with examples; `docs/language-rule-coverage.md` carries the maintainer's five parts, each catcher's reach, how to run each kind by hand, what a break costs, and the two vocabularies for catcher status and catcher moments. `guardrails/language-rules.json` is where rules are edited and `skills/text-audit/SKILL.md` holds the standing prompt — both clear. `JOURNAL.md` is the one I cannot size: I know it holds readings one through four and not what those entries contain. `PRODUCT_SPEC.md` I know only as "the spec."

**3. Could I use this page tomorrow for the job it claims?**
For tracing why a rule exists, yes, for the rules it covers. I would have to ask the author five things: what the six surfaces are (or accept a trip to the writer's page before any rule is usable); what "the package" and "one reader's own layer" mean in the override part; which shape a reading entry actually takes, and whether it records the reader's guesses; whether readings one through four have stop counts anywhere; and what the four out-of-scope owner stops were.

**4. What read clearly on the first pass?**
The three-page split and the one-line routing for each. The definitions of class, break, catcher, home, and source. The one obligation — every word, number, and list the writing depends on, measured on a reader who brings nothing. The three-step account of how a class becomes a rule, including the test that a repair applied to one sentence means step 3 was skipped. The bullet about six rules naming a list and giving it nowhere, including the three lists that lived inside regular expressions. The closing claim that no script and no model finds a class nobody has met yet.

**5. Blocking and non-blocking**

BLOCKING (I could not proceed, or would have acted wrongly):
4 (layer and package undefined), 6 (surfaces named and undefined — no rule is applicable), 9 (guess vs no guess in the standing prompt), 10 (two different reading-entry shapes), 13 («обязанность» described as carried over from English), 14 (the fallback rule count is not given).

NON-BLOCKING (noticed and read on):
1, 2, 3, 5, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25.
