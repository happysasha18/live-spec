# Blind read, 2026-07-28 — the language-defects document, read nine

The reader met this text with no context: one file, no repository access, no history of the
document's earlier rounds. The brief asked for every place the reader stopped, sorted into stops
that blocked the reader and stops the reader noticed and read past.

Reader: a working software engineer persona, clean context.
Text read: `docs/language-defects.md` after round eleven closed the six blocking stops read eight
found.
Stops: 31 — 5 blocking, 26 non-blocking.

The five readings of this page, oldest first: 45 stops with 11 blocking, 34 with 8, 27 with 12, 28
with 6, 31 with 5. The bar is two consecutive readings with no blocking stop.

---

I read the file once, straight through. Here is what happened.

**File read:** `/private/tmp/claude-501/-Users-sashaabramovich/14f2fe20-40cb-4760-b709-ef591b5eb05c/scratchpad/text-to-read-G.md` (281 lines)

---

## Stops

**1.** "It has three parts: the sentence that removes the mistake, the question to ask of a s…"
I built a three-part model of a rule, then two sentences later read "so every rule has a fourth part that lives away from the other three" and had to go back and rebuild it. I needed the count stated once, as four parts with one of them living elsewhere.

**2.** "This project names six surfaces — spec-body, human-prose, chat, artifact, commit, and w…"
Six labels arrive with no definitions and I am told at line 36 that defining them is another page's job. Everything downstream turns on which surface a text is. I read on holding six words I could not attach meaning to. I needed one clause per surface here, or one sentence telling me I cannot use the surface axis without opening the other page.

**3.** "A **rule** is one statement about one class."
Clear. No stop. (Recording that the glossary paragraph as a whole read fine apart from stop 1.)

**4.** "A retired rule takes its identifier out of the set with it, so the highest identifier ru…"
Second pass to parse "runs ahead of." Then I checked it against the rest: the page says sixty rules, says twelve entries folded into five (seven identifiers retired), and cites `r61`. With sixty live rules and seven retirements the highest identifier must be at least 67, so `r61` is not the highest. Nothing contradicts, but I spent time proving that.

**5.** "The text used ordinary English nouns for jobs only this project knows: seat, net, door, h…"
Ten words. Four of them (seat, law, home, tier) get defined a hundred lines later in a different section; net, door, walk, lens, handle, frame are never defined anywhere on this page. I stopped trying to decide whether I was supposed to know them. I needed a marker that this is a list of symptoms rather than vocabulary I must carry.

**6.** "The remaining three the reader did not attempt."
Fronted object. Re-read once to attach "three" to "requirements."

**7.** "The Russian reader was given six paragraphs of working chat, about 250 words, and stopp…"
I guessed "working chat" means the message log between the person and the agent during a work session — about 70% sure. Also: this reader becomes "him" one sentence later, where the English reader stayed "that reader" throughout. I checked whether two different people were being discussed.

**8.** "That reader also named two habits without being asked: actions handed to things that ca…"
Every other class on this page carries an identifier (`r02`, `r36`, `r54`, `r61`). These two carry none. I could not tell whether they became rules, were rejected, or are still pending. I needed the identifiers or a sentence saying they have none yet.

**9.** "Without that answer the count drops to the rules binding every surface, and the reading…"
Could not parse on the first pass. Second pass: the count drops to however many rules bind all six surfaces. I needed "drops to the number of rules that bind every surface."

**10.** "That definition and the reading's finding stand hours apart on one day rather than in c…"
I stopped to reconstruct a timeline the page had not laid out: the 07-28 reader found the surfaces undefined, and the definitions were written later on 07-28. The sentence defends against a contradiction before I had noticed one, which made me go back and look for it.

**11.** "Every one of those lists now stands inside the rule that names it, read out of the scrip…"
Two passes. "the script catcher's own configuration file" is the first appearance of configuration files on this page, and it arrives inside a subordinate clause about build time. I needed the configuration file introduced before it was used.

**12.** "Twelve entries carried five classes between them, each class broken into pieces."
Re-read to work out that each of the five classes had been split across two or three entries. Then I did arithmetic against the sixty total and the identifier rule (see stop 4).

**13.** "Readings one through four left no file of their own, and `JOURNAL.md` counts them."
I guessed "counts them" means JOURNAL.md is where the evidence that those four happened lives — about 60% sure. It could also mean the four are included in the count of eight. I needed "records them" or "is the only record of them."

**14.** "The maintainer's page defines the other two: the words that say whether a catcher runs …"
Two vocabularies are named by their function and never by name. I guessed the first is a status field like active/planned/none, and the second is a set of moment names like commit, push, pre-show — both guesses under 50%. This is the one place the page points at another document and I could not tell what I would find. I needed one example value from each.

**15.** "The seventh reading returned fewer stops than the sixth and more blocking ones, and the…"
Re-read. "the material that had landed here in between" — I guessed: content added to this page between reading six and reading seven. The clause does the causal work of the paragraph and I had to hold it unresolved for two sentences.

**16.** "A law is a requirement the spec states about how the project works: the four the criteri…"
One sentence introduces four orchestration laws plus a break-record law, and I counted five laws while the surrounding paragraph promised four words. Re-read twice.

**17.** "…their breaks recorded in the one home the break-record law names, the problem ledger…"
Line 21 defines a break as "one place a text falls short of a rule." Here, and again in the repaired list ("each break is recorded in the problem ledger"), a break is an orchestration law being violated by the running system, which is not a text falling short of a writing rule. The defined word is used outside its own definition. If I had gone to write something down, I would have filed it in the wrong place. I needed either a second sense stated, or a different word for one of them.

**18.** "…carrying a reminder-history of two or more…" versus "…carrying a reminder history of tw…"
Hyphenated in the old quotation, unhyphenated in the repaired one, with no comment. I stopped to check whether the hyphen was one of the repairs.

**19.** "The system *shall* judge the orchestration laws carrying a reminder history of two or m…"
"Judge" is never given an object or an output — judge them against what, producing what. And "two or more" gives no unit; I guessed occurrences. This is true of both the old and the repaired version, and the page presents the repair as complete. I disagreed that the repair is finished; it fixed the length and left the instruction unactionable.

**20.** "The bracketed codes at the end are this project's internal identifiers for requirements …"
The sentence ends "and they count toward the 107 words," which line 196 already said ("at 107 words counting the bracketed codes that trail it"). I re-read to check whether a second, different claim was being made.

**21.** "That entry carries a name, the rule in one sentence, and a question a reader can ask of …"
This lists an entry's parts as: name, rule sentence, question, surfaces, prior prose files, status. Line 20 listed a rule's parts as: sentence, question, surfaces, plus catchers as a fourth. Two different part-lists for what I believe is one object. If I were adding an entry to `guardrails/language-rules.json` tomorrow I would not know which shape to write. Also, the clause "and every rule on both built pages is one such entry rendered for its reader" is spliced into the middle of the list and made me lose the list.

**22.** "A list of examples with no class named above it breaks the rule that governs how the sou…"
This follows a sentence about skipping step 3, and I read the two as one thought before realising they are two separate failures. I needed a break between them.

**23.** "Cold reading is a standing cost, and a project plans and funds it every round."
I guessed "round" means each development cycle or each release — about 50%. "Funds" I could not tell: money for a person's time, or budget for model calls. I needed the unit named.

**24.** "…reads a document about to be shown to a person, and its first pass is a list of litera…"
"First pass" tells me there are later passes and none are described. I stopped waiting for the second pass, which never came.

**25.** "It passed the sentence clean: the list had met the coinage and not this wording of it."
On first read I attached "passed" to the wrong subject and thought the sentence had passed some other check. Second pass: the lint reported no defect on that sentence. I needed "The lint reported no defect."

**26.** "That result stands as a test today, in `tests/test_register_judge.py`."
The script is `preshow-register-lint.py`; the test is `test_register_judge.py`. Line 176 also mentions "the text the judging model is handed." I suspect lint and judge are two names for one piece of machinery, or for two halves of it, and I could not tell which.

**27.** "…find the one you are writing on and read the rules listed under it, which are the whole…"
This claims the rules listed under my surface are the complete set governing my text. Stop 9 said some rules bind every surface. I cannot tell whether an all-surface rule is repeated under each surface heading or listed once somewhere else. Acting on this sentence, I would read one section and believe I had the whole set. I needed a statement of how all-surface rules appear on that page.

**28.** "A rule enters this project from a reading that stopped."
A reading does not stop; a reader does. Re-read once to attach the action to a person.

**29.** "…this page names a rule by that identifier together with the rule's short name in itali…"
The italic names that follow are full clauses — *a coined, loan-translated, or respelled word standing where a plain standard word exists*. I stopped to check whether I had missed a shorter name somewhere.

**30.** "…and where the rule was stated in prose before the source became the only place it is e…"
Re-read. I guessed it means: the older files that used to carry this rule as prose, kept as pointers. About 70% sure.

**31.** "Every rule is edited in one file, `guardrails/language-rules.json`, which this page calls…"
Line 18 says five words carry the weight on this page. "Source" is a sixth term this page coins for itself, and "home" is a seventh, introduced at line 193. I stopped to check whether I had miscounted the glossary.

Also, one term I had to guess and got: "loan-translated" — translated word by word from English. The Russian-reader paragraph gives the mechanic before the word appears, so I was confident.

---

## Answers

**1. What is this document for, who reads it, when?**
It is the provenance record for one project's writing rules: which reading by which reader produced which rule, on which date. The page states its own audience at line 42 — you come here to find out why the rules say what they say, after you have been to the writer's page to write or the maintainer's page to fix a catcher. I read it as something you open when you want to change or challenge a rule, rather than when you are writing.

**2. Do I know what the other documents hold and when to go there?**
For `docs/language-rules.md` and `docs/language-rule-coverage.md`, yes — lines 33 to 42 give contents and a one-line routing rule for each, and I could act on that. For `docs/language-reads/`, yes — line 124 defines the file shape. For `JOURNAL.md`, `PROBLEMS.md`, and `guardrails/language-rules.json`, yes. The one I could not picture is the maintainer's page's two vocabularies at lines 176 to 177: I know they exist and I know their function, and I do not know what a single value looks like.

**3. Could I use this page tomorrow for the job it claims?**
For the job of understanding why a rule exists, yes — the readings are dated, attributed, and each one names what it produced. I would have to ask the author three things: what a break means when it is an orchestration law rather than a text (stop 17); which part-list for a rule entry is correct, line 20 or line 246 (stop 21); and whether the rules binding every surface appear under each surface heading on the writer's page, because line 276 tells me one section is the whole set (stop 27).

**4. What read clearly on the first pass?**
The opening definitions of live-spec and of a gate. The five roles section, including the cold reader's three deprivations. The one-demand section. The eight-readings list with its counts and file paths. The `r54` bar and its stated exception for the reader who measures it. The three-step account of how a class becomes a rule, apart from the spliced clause in step 3. The closing section on what scripts and models cannot find, which lands its point with the 2026-07-17 example.

**5. Blocking and non-blocking**

BLOCKING (5): 2 (six surfaces named, none defined, and the whole rule set is organised on that axis), 14 (two vocabularies I cannot picture, on the page I would go to for repairs), 17 (break used in two senses, so I would file one in the wrong home), 21 (two conflicting part-lists for a rule entry), 27 (completeness claim I cannot reconcile with the all-surface rules).

NON-BLOCKING (26): 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 18, 19, 20, 22, 23, 24, 25, 26, 28, 29, 30, 31.

**Total stops: 31.**
