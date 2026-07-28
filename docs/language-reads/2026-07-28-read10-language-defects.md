# Blind read, 2026-07-28 — the language-defects document, read ten

The reader met this text with no context: one file, no repository access, no history of the
document's earlier rounds. The brief asked for every place the reader stopped, sorted into stops
that blocked the reader and stops the reader noticed and read past.

Reader: a working software engineer persona, clean context.
Text read: `docs/language-defects.md` after round twelve closed the five blocking stops read nine
found.
Stops: 25 — 5 blocking, 20 non-blocking.

The six readings of this page, oldest first, by blocking stops: 11, 8, 12, 6, 5, 5. Three of this
reading's five trace to one cause: the page names six surfaces it does not define and then closes by
telling the reader to find the surface they are writing on.

---

I read the file once, straight through. Below is what happened.

## Stops

**1.** "the one demand the writer owes the reader" (line 7, and again at the section heading)
A demand is something one party makes on another; here it is owed by the writer to the reader. I re-read the phrase in the contents list, guessed it meant obligation, and confirmed at line 77. I needed the word "obligation" or the sentence at line 77 to appear first.

**2.** "Seven words carry the weight on this page, and each names its own thing."
I stopped to count the bolded terms across the next three paragraphs to check whether seven was right (class, break, catcher, home, source, surface, rule — seven). I needed the seven listed in one line before they were defined.

**3.** "Every entry carries nine parts, five of them the writer's and four the maintainer's."
Two paragraphs later: "An entry also carries examples, exceptions, thresholds, and the lists the rule names." That is four more things inside an entry, and the count of nine is repeated later at line 274 as a thing to follow when writing a new entry. If I wrote an entry tomorrow I would have written nine fields and left the examples and lists out. I needed a statement of whether examples, exceptions, thresholds and lists are parts or something else.

**4.** "All six are defined, each with an example, on the writer's page named just below"
Later: "The surfaces were the axis the whole page was organized on, and the page defined none of them." I stopped, went back, and found the reconciliation at line 149 (the reading and the definitions are hours apart on one day). The two statements sit 120 lines apart and I resolved them only because the document happened to say so.

**5.** "The highest identifier is therefore a larger number than the count of the rules that remain."
The "therefore" holds only if at least one rule has been retired. Nothing before this sentence says any has been. I disagreed on the first pass, then found the retirements at line 167. I needed the retirement fact stated before the conclusion drawn from it.

**6.** "This project names six surfaces — spec-body, human-prose, chat, artifact, commit, and worker-brief"
I can guess spec-body, chat and commit. I could not tell what "artifact" or "worker-brief" cover, and "human-prose" against "spec-body" and "chat" leaves me unsure where a README lands. The page sends me elsewhere for the definitions, and every rule binds by surface, so this is the index into the whole system. I needed one line per surface here.

**7.** "Those ten nouns stand here as instances of the class this reader met"
The preceding sentences give ten nouns and then "red" used as a verb — eleven items. The count of ten drops the verb without saying so. I re-read to see whether I had miscounted.

**8.** "The lists and the default values those three requirements depend on were never given anywhere in the text."
"Those three" can point at the three the reader did not attempt, or at a set including the third one that got written-down questions. I read it as the un-attempted three, with moderate confidence. I needed the sentence to name which three.

**9.** "Twenty stops in 250 words is a stop every thirteen words"
250 divided by 20 is 12.5, and the word count is given as "about 250". I stopped to do the arithmetic and to decide whether thirteen was a rounding or a different figure.

**10.** "`r05`, *a predicate applied to a subject that cannot carry it*"
"Predicate" and "carry" are both doing unusual work. I guessed this is the ban on giving human actions to inanimate things, from the preceding sentence about actions handed to things that cannot perform them. Confidence high, but I got it from the gloss rather than the rule name.

**11.** "stopped at six of its sentences. Two of those six were the rewrite breaking a rule it stated in the same passage."
Two bullets follow. The other four sentences never appear. I waited for them through the next section. I needed a line saying the remaining four are recorded elsewhere or are out of scope here.

**12.** "All thirty assume an answer to which surface a documentation page is. Without that answer the count drops to the number of the rules binding every surface, and the reading puts no exact number on those."
This is the rule I could not apply. The page tells me my applicable rule set depends on a surface answer, tells me that answer was missing, and does not supply it or the fallback number. The final section then tells me to go read rules "listed under a surface". I needed the surface a documentation page belongs to, or the count of rules binding all six.

**13.** "A script catcher keeps the words it matches in a configuration file of its own, beside the script."
The next sentence but one says three of the six had no such file. I re-read the bullet twice to work out that the first sentence describes the usual arrangement and the exceptions come immediately after. Separately, the configuration file is never named or given a path, so I could not find it tomorrow if I had to add a word to a list.

**14.** "The twelve are folded back into five"
Twelve entries became five, so seven identifiers were retired. The reading that reported "thirty of the sixty rules" happened before or after that fold — I could not tell. The page never states how many rules exist today, which is the number I would want before starting.

**15.** "such as `held` and `stated-only`"
I guessed "stated-only" means the rule is written down with nothing enforcing it. I guessed "held" means something enforces it. Low confidence on "held" — the word suggests a held position rather than an active check. The page sends me to the maintainer's page for these, which I noted and accepted.

**16.** "A law is a requirement the spec states about how the project works"
Then "Criterion 4 of Requirement 233", then "[INV-241, INV-108…] are this project's internal identifiers for requirements stated elsewhere in the spec". So law, requirement, and INV code all sit in the same area. I could not tell whether Requirement 233 is itself a law, or whether every INV code names a law. The page states rule `r04` against one thing answering to a second name, which is what I suspect here.

**17.** "Both quotations below call a lapse a break, that being the spec's own word for it."
"Break" now has two meanings — a text falling short of a rule, and a running system failing to keep a law — and the quoted material uses the other one. I slowed down and re-read the paragraph twice to hold them apart. The page does resolve it in place, so I went on.

**18.** "The sentence runs to 35 words with the same codes"
I counted the repaired sentence and got roughly 34, depending on how the five bracketed codes and the hyphenated names are counted. I stopped, counted twice, and let it go. I needed the counting convention (whether `[INV-241]` is one word, and whether `worker-routing` is one or two).

**19.** "The hyphen went as part of the repair: the older quotation reads reminder-history and the repaired criterion reads reminder history, two words."
No rule is cited and no reason given. I stopped looking for why this mattered enough to state.

**20.** "That material is what raised the blocking count."
The page asserts a cause for the jump from 8 blocking to 12 without giving the evidence that links the added material to the stops. I disagreed on the strength of the claim and read on.

**21.** "The list passed the sentence clean: it had met the coinage and not this wording of it."
Two sentences earlier the script is described as making two passes — the literal patterns and one model call. The story reports only the pattern pass. Whether the model call caught the Russian sentence on 2026-07-17 is never said, and the next section claims a model reads for the class itself. I wanted the model's result on that same sentence.

**22.** "Two things there carry names close enough to be read as one."
Three names are then given — `scripts/preshow-register-lint.py`, "the judge", `hooks/register_judge_core.py` — plus the test file `tests/test_register_judge.py`. The paragraph names the confusion and leaves me still unable to say which of the two things a bare mention of "register judge" refers to. I needed one sentence saying which name to use for which.

**23.** "register" (in `preshow-register-lint.py`, `test_register_judge.py`, "register judge")
The word appears four times and is never defined. I guessed it means the level or tone of the language. Moderate confidence. The page's own demand is that every word the writing depends on stands where it is used or points at one named place; this one does neither.

**24.** "A project plans a reading into every round of revision and pays for the reader's hours."
Paying for hours implies a person. The readings recorded above were plainly produced by language models given a text with context held back. I stopped on whether a cold reader is a person or a model, and on how I would obtain one tomorrow. Nothing on the page says how a cold reading is commissioned or run.

**25.** "Open `docs/language-rules.md`. The rules listed under a surface there are the whole set governing a text of that kind."
This is the section that names the job, and it does not tell me which surface my documentation page is, how to get the two clean cold readings that `r54` requires before shipping, or whether `r54` applies to a page like mine at all. I stopped at the end of the document with the entry step missing.

## Answers

**1. What the document is for.** It records where each language rule came from — which reading, by whom, on what date, and what stop produced it. It says outright that you read it to know why the rules say what they say, so the reader is someone questioning an existing rule or preparing to add one. The writer's page and the maintainer's page carry the working material; this one carries provenance.

**2. The pointers.** For most of them, yes. `docs/language-rules.md` holds the parts a writer applies and is read to write; `docs/language-rule-coverage.md` holds the maintainer's four parts, catcher reach, how to run each catcher, and what a break costs, and is read to run or repair a catcher; `docs/language-reads/` holds one account per reading; `JOURNAL.md` holds readings one through four; `guardrails/language-rules.json` is where a rule is edited. `PRODUCT_SPEC.md` and `PROBLEMS.md` get a sentence each and I know roughly what is in them. The configuration file beside a script catcher gets no name and no path.

**3. Could I use it tomorrow.** For the job it names — write a documentation page and hold it to the rulebook — the page hands off to `docs/language-rules.md` and the handoff does not survive the surface gap: I would not know which rule set applies to me. I would have to ask the author which surface a documentation page is, how many rules bind every surface, how many rules exist today after the twelve-to-five fold, how to obtain a cold reading, and whether the two-clean-readings bar applies to a page I write.

**4. Clear on the first pass.** The definitions of class, break, catcher, home and source, and the sentence separating a surface from a file. The five roles and the note that one person holds several. The definition of a blocking stop. The reading log with its stop and blocking counts, including the seventh-versus-sixth comparison, which I checked and which holds. The before-and-after criterion, the three instructions it carried, and the account of the two defects the repair left standing. The three numbered steps by which a class becomes a rule.

**5. Sorting.**

BLOCKING — stops 3 (nine parts against the four additional fields), 6 (six surfaces named and undefined), 12 (applicable rule count depends on an answer never given), 24 (no route to a cold reading), 25 (the tomorrow section cannot be executed as written).

NON-BLOCKING — stops 1, 2, 4, 5, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23.

**Total stops: 25** (5 blocking, 20 non-blocking).
