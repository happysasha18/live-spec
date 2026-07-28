# Blind read, 2026-07-28 — the language-defects document, read seven

The reader met this text with no context: one file, no repository access, no history of the
document's earlier rounds. The brief asked for every place the reader stopped, sorted into stops
that blocked the reader and stops the reader noticed and read past.

Reader: a working software engineer persona, clean context.
Text read: `docs/language-defects.md` after the round-eight rewrite, when the rules had moved to a
writer's page and a maintainer's page and this page had taken on how to run the catchers.
Stops: 27 — 12 blocking, 15 non-blocking.

Read five recorded 45 stops with 11 blocking; read six recorded 34 with 8. The total fell and the
blocking count rose, and this reading names the cause: the page had taken on runbook material whose
terms live on the other two pages.

---

I read the file once, straight through. Report follows.

---

## STOPS

**1.** "A **rule** is what an entry states about one class"
I did not know what an entry was. The word arrives inside a definition of a key term, and nothing before it says what an entry is or where entries live. I found out 45 lines later that entries live in `guardrails/language-rules.json`. I needed the entry named before it was used to define something else.

**2.** "where each is armed, and where the rule was stated before the source became its one home"
Two problems in one line. I guessed "armed" means wired into some event so it actually runs; moderately sure, and the guess held up later at "many rules are armed nowhere". "The source" was not defined at that point — I guessed it meant some origin document, and I was wrong; it turned out to be a specific JSON file named 30 lines later. I needed "the source" introduced before its first use.

**3.** "The record covers four things:" followed by four bullets
I read those four bullets as the map of the document and used them to navigate. Three later sections do not sit under any of the four: how to run the catchers, what a break costs, and "Using this tomorrow". I needed the list to cover the document, or a note saying it covers part of it.

**4.** "A reader owes the text nothing."
I could not parse this on the first pass. I read it as the reader having no obligation to the text and then could not tell what work the sentence was doing. The next sentence made it clear. I needed the demand stated as a demand on the writer, without the inversion.

**5.** "Five files carry the rules: the file every rule is edited in, the writer's page, the maintainer's page, the generator behind all three, and the gate over the set."
I counted. Two pages precede "the generator behind all three", so I could not tell what the third thing was. Then the bullet for the generator names a sixth file, `hooks/language-laws.json`, which is not in the five. I needed the count and the list to agree.

**6.** "Each rule's entry names the file that carries its own script catcher." — followed by `python3 scripts/preshow-register-lint.py docs/language-rules.md`
`preshow-register-lint.py` is given here as an example of a **script** catcher. Twenty-five lines later the same file is "the model catcher" on documents. I could not tell whether it is one thing or two, or whether it does both. I needed one statement of what that script is.

**7.** "Two scripts make the call, one on each surface it runs on today."
I did not know what a surface was. "Surface" had already appeared at "the rules binding the text's surface" a line earlier. It is defined 45 lines further down. I needed the definition before the first use.

**8.** "The reply that broke a rule has been read by then, so the correction reaches the person one turn later."
I re-read this three times. "Has been read by then" gave me no actor. I eventually decided it means the person has already seen the bad reply before the verdict arrives. I needed the actor named.

**9.** `printf '{"transcript_path": "%s"}' ~/.claude/projects/PROJECT/SESSION.jsonl`
`PROJECT` and `SESSION` are placeholders and nothing tells me how to find the real values. If I ran the command tomorrow I would guess at a path. I needed either a way to find the transcript or a note that these are placeholders.

**10.** "almost all of it the harness starting up"
"Harness" is undefined. I guessed it means the process that hosts the model call, low confidence. I needed the word defined or replaced.

**11.** "Either script stands down on its own breakage"
I guessed "stands down" means stops and reports rather than failing the run; the rest of the sentence confirmed it. Moderately sure on first contact.

**12.** "The section below on the readings that produced the rules says how one of those readings is run and what it returns."
I went to that section looking for the procedure. It reports what readings found. The only thing resembling a procedure is one clause much later: the reader is handed the page. I could not run a person catcher from this. This is the section titled "Running the person catcher", so I expected to be able to. I needed the actual procedure, or the pointer removed.

**13.** "That page defines both sets of words at its top, and what a break costs is read there"
I had to re-read to work out that "both sets" means the status vocabulary and the event vocabulary. The section is called "What a break costs you" and it tells me the answer is somewhere else. I needed the two vocabularies named on this page, at least by name.

**14.** "`docs/language-rules.md` defines the six surfaces with an example each"
Surfaces are the axis everything is organized on, and the six are never listed here. The last section tells me to "find the surface you are writing on", which I cannot begin without the other page. I needed the six named.

**15.** "The text used ordinary English nouns for jobs only this project knows: seat, net, door, home, walk, lens, handle, frame, law, tier."
This page uses at least four of those words for its own jobs and defines only one. It says "one named place the sentence points to", "the cheapest tier", "the person's or the seat's", "the break-record law". "Law" is explained late, at line 246. "Seat", "tier" and "home" are not. This is the document doing the thing it is reporting as a defect, in a section that reports it as a defect. I needed those words defined or replaced here.

**16.** "Of the six requirements, that reader could build two from the text alone."
I guessed "build" means implement the requirement in code. Moderately sure. I needed the verb that names the actual task.

**17.** "The lists and the default values those three rules depend on were never given anywhere in the text."
Two sentences earlier those same three things were requirements. Here they are rules. The document later reserves "rule" for a statement about how a text is written and "requirement" for a statement in the spec ("a statement about how a text is written is a rule"). So this sentence uses the word the document itself rules out. I suspect requirement and rule are being used for one thing here.

**18.** "The reader could apply 30 of the 60 rules, and about 8 of them without an answer to which surface a documentation page is"
I could not parse this on the first pass. "About 8 of them without an answer" reads either as eight that survived the missing definition or eight that died on it. I still do not know which. I needed the sentence split in two.

**19.** "the surfaces were the axis the whole page was organized on, and none of them was defined"
This contradicts the earlier line saying `docs/language-rules.md` defines the six surfaces with an example each. I assume the reading came first and the definitions were added after, but the page never says so, and the reading is dated 2026-07-28, which is the newest date on the page. I needed the tense or the repair stated.

**20.** "The reader skimmed four fields in every entry and reported that none of them changes a word a writer writes"
I stopped on "skimmed". I could not tell whether the reader skimmed them because they looked irrelevant, or the finding was that they are skippable. Those are different findings. I needed the one that happened.

**21.** "read out of the checker's own config file"
"The checker" is a new name. I have already been given "gate", "catcher", "script catcher", and "generator". I suspect checker and script catcher are the same thing. I needed one name.

**22.** "Twelve entries were five classes split apart."
I could not parse this on the first pass. Second pass I read it as twelve entries that were really five classes each broken into pieces. I needed a verb that carries the meaning.

**23.** Section ordering and dates: "Two cold readers, 2026-07-27" → "The owner's read of a rewrite" (no date) → "On 2026-07-28 a cold reader was handed" → "The fifth reading is recorded at `docs/language-reads/2026-07-27-read5...`"
I was reading these as a sequence and the dates run forward then back. The owner's read carries no date at all, so I could not place it. I needed a date on every reading.

**24.** "On 2026-07-17 `scripts/preshow-register-lint.py` was handed a Russian text carrying the same loan-translations its own list names, and it passed that text clean."
This describes the script as a literal-pattern catcher holding a list. The earlier section describes the same script as the one that makes the model call. I disagreed with one of the two descriptions being complete. Combined with stop 6, I do not know what that file is.

**25.** "This page is shown to nobody until two cold readings in a row return nothing blocking."
I disagreed with the reachability of this claim as written, given the sentence two lines above says the page has been read six times and failed six times. The exception clause resolves it, and I read on. Recording it as a place I argued back.

**26.** Pointers I could not size: `docs/language-reads/2026-07-28-read1-language-rules-reference.md`, `docs/language-reads/2026-07-27-read5-language-defects.md`, `JOURNAL.md`, `PROBLEMS.md`, `hooks/language-laws.json`
For the two reading files I know roughly what I would find, because the surrounding sentences summarize them. For `JOURNAL.md` I know only that it counts something. `PROBLEMS.md` is glossed as the problem ledger inside a quotation. I needed one line saying what a reading file contains as a genre, and whether I would ever need to open one.

**27.** Rule identifiers `r02`, `r36`, `r54`, `r61`
The page says it names a rule by its identifier. Each time one appeared I had no way to resolve it from this page and no ordering to infer from. I needed either the rule's short name beside the identifier every time, or a note that identifiers are only useful once the other page is open. The document does give the rule's substance in prose next to `r02` and `r36`; it gives only the identifier for `r54` and `r61`.

---

## ANSWERS

**1. What is this document for, who reads it, when.**
It is the history behind a set of writing rules that live on two other pages: which readings produced which rules, and how a repeated mistake becomes a rule. The stated reader is someone who wants to know why the rules say what they say, and the page names the writer's page as the thing to read in order to write. The last section and the middle sections point in a different direction: they hand me commands to run and tell me what to do tomorrow, so the page is also operating as a runbook.

**2. Do I know what the other document holds and when to go there.**
For `docs/language-rules.md` I know it holds each rule as a sentence, a question to ask, the surfaces it binds, examples, exceptions, thresholds, and the lists each rule names, and I know to go there when I am about to write. For `docs/language-rule-coverage.md` I know it holds catchers, reach, arming, and history, and I go there to find out whether a rule is enforced and what a break costs. I could not tell what the reading files under `docs/language-reads/` hold beyond a stop count.

**3. Could I use this page tomorrow for the job it claims.**
I could not do the last section's instruction from this page, because it starts with finding the surface I am writing on and the six surfaces are never listed here. I could run the generator and the gate. I could not run the model catcher by hand, because I do not know how to fill in `PROJECT` and `SESSION`, and I could not run a person catcher at all. I would have to ask the author: what are the six surfaces; what is a seat, a tier, a home, a walk; is `preshow-register-lint.py` the model catcher or a pattern checker or both; how do I find a transcript path; and what procedure and prompt does a cold reading use.

**4. What read clearly on the first pass.**
The three definitions of class, rule, and catcher, once I got past "an entry". The five-file list read clearly as bullets, whatever the count problem. The before-and-after sentence pair — I could see the change and I agreed with it, and I did not need to understand the content of the criterion to see it. The three numbered steps under "How a class becomes a rule". The closing section on what a script and a model cannot find, which was the clearest prose on the page.

**5. Blocking versus non-blocking.**

BLOCKING — I could not proceed, or I would have acted wrongly: 2 (the source undefined at first use), 5 (five files, six named, "all three" unresolvable), 6 and 24 (what `preshow-register-lint.py` is — I would have run it expecting the wrong behaviour), 7 and 14 (surface used before definition and never listed, which stops the last section outright), 9 (placeholders with no way to fill them), 12 ("Running the person catcher" contains no procedure), 15 (seat, tier, home used undefined in the section reporting them as defects), 18 (the 30-of-60 sentence, still unparsed), 21 (checker versus catcher, unclear whether one thing or two), 27 (`r54` and `r61` are unresolvable from this page).

NON-BLOCKING — I noticed and read on: 1, 3, 4, 8, 10, 11, 13, 16, 17, 19, 20, 22, 23, 25, 26.

---

**Stop count: 27.**
