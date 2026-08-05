# Reading record — skills/text-audit/SKILL.md, read 2026-08-05

Read on the cheap tier: one cold read done inline by the worker that had just read the reader-prompt, not a fresh isolated session spawned solely for this pass.

Stops: 31 — 8 blocking

1. **"the session's live word, then the host profile, then the personal profile, then the package default"**
   Where: opening blockquote, "Part of the live-spec pack."
   What a stranger cannot tell: what "the session's live word," "the host profile," and "the personal profile" each name. None is defined here or in the two companion files.
   Guess: read "the session's live word" as whatever instruction is active in the current conversation, and the two profiles as configuration layers above the package default.
   Non-blocking.

2. **"read a text as a stranger, fix where they stop"**
   Where: the document's title.
   What a stranger cannot tell: whether "a stranger" names the same role as "the cold reader," defined a few paragraphs later, or a separate idea. No sentence states the two are one word for one role.
   Guess: treated "stranger" and "cold reader" as synonyms throughout.
   Non-blocking.

3. **"the reader it is written for"**
   Where: "The reading step runs two cold readers over the same text…," and again at "the unprompted reader — a cold reader holding the text, the reader it is written for, and the task."
   What a stranger cannot tell: this document uses "reader" for two different things — the cold-reader role doing the audit, and the audience the audited text was written for. The same word carries both senses in the same sentence.
   Guess: read "the reader it is written for" as the text's intended audience, distinct from the cold reader performing the check.
   Non-blocking.

4. **"The loop came from the comprehension gate on spec sections, recorded in `docs/spec-format.md`."**
   Where: paragraph beginning "The loop came from the comprehension gate…"
   What a stranger cannot tell: what that gate actually found, or why it settled on this loop — the document names a file that holds the ground but does not state the ground itself.
   Guess: took the claim on faith without seeing the underlying evidence.
   Non-blocking.

5. **"Those readers found new blocking terms on every pass… This skill packages that loop for any text."**
   Where: same paragraph, continuing after the comprehension-gate sentence.
   What a stranger cannot tell: this paragraph carries several separate points — evidence the loop converges, the definition of a reading record, the scope of `docs/language-defects.md`, and a closing generalization — with no signal that a reader following only the opening sentence will miss a definition further down.
   Guess: split the paragraph mentally into its parts to track them separately.
   Non-blocking.

6. **"the cold reader is never either of them"**
   Where: heading "The roles and the words this skill uses," opening paragraph.
   What a stranger cannot tell: "One person may hold the auditor role and own the text" merges two roles into one person; "them" then has to be read as the two roles, not the one merged person just described.
   Guess: reread it to confirm "them" means the auditor role and the person role, not "the one person."
   Non-blocking.

7. **"a worker brief"**
   Where: "The live-spec repository names six surfaces: a spec body, human prose, chat, a published artifact, a commit message, and a worker brief."
   What a stranger cannot tell: what a worker brief actually is. It is named here and later as an example of machine-read text, but never described.
   Guess: read it as an instruction document handed to an automated worker, by analogy with "worker."
   Non-blocking.

8. **"and its clarity matters"**
   Where: heading "When it fires," "Load this skill when a human-facing text is about to ship and its clarity matters:"
   What a stranger cannot tell: matters by what measure, or to whom. No judge or threshold is given.
   Guess: read it loosely as "whenever the text will be read by someone outside the project."
   Non-blocking.

9. **"whatever writing skills the host installs beside the pack"**
   Where: "Work that belongs elsewhere," the paragraph on taste and voice.
   What a stranger cannot tell: who or what "the host" is — a person, an organization, an environment.
   Guess: read "the host" as the person or team running the project this skill is installed into.
   Non-blocking.

10. **"A worker brief, a checkpoint, and an internal note are machine-read."**
    Where: "Work that belongs elsewhere," closing sentence.
    What a stranger cannot tell: what a checkpoint is here. It does not appear among the six named surfaces, so it is unclear whether it is a seventh, unlisted surface or something else.
    Guess: read it as a save-point or status file no person reads directly.
    Non-blocking.

11. **"On 2026-08-05 a separate review of one repaired skill found four defects inside the repair's own new sections. One was a false claim about where every path resolves."**
    Where: "The loop," step 5, the paragraph "A repair writes text nobody has read."
    What a stranger cannot tell: which review, which skill, or where this is recorded. Unlike the document's other evidence claims, this one names no file, no plan, and no report to check it against.
    Guess: took the claim on faith, with no way to verify it or find the four defects it refers to.
    Blocking.

12. **"a handful of sentences"**
    Where: paragraph after "The loop," "A section-sized run puts one definition and a handful of sentences in front of a reader."
    What a stranger cannot tell: how many sentences "a handful" means.
    Guess: read it as roughly three to six sentences.
    Non-blocking.

13. **"The plan chose that size for two reasons (`docs/plans/2026-07-28-top-level-readability.md`)."**
    Where: "Running it on a spec section," "Ten requirements at a time is the working size…"
    What a stranger cannot tell: what the two reasons actually are, stated on this page. The next sentence gives two clauses, but the text never confirms these are the same two reasons the cited plan names.
    Guess: assumed the two reasons are the next sentence's two clauses.
    Non-blocking.

14. **"A rewrite that moves one of them breaks a test, or one of the two maps below."**
    Where: bolded item "Every mark a machine reads survives the repair."
    What a stranger cannot tell: what "them" refers to. The paragraph names four candidates across three sentences — a requirement's number, its bracket anchors, headings, and any phrase a test quotes — with no single antecedent marked.
    Guess: read "them" as all four items named in the paragraph, taken together.
    Non-blocking.

15. **"whose rows pair one architecture node with one spec fact and pin the test level that covers it"**
    Where: bolded item "The test matrix is `TEST_MATRIX.md`."
    What a stranger cannot tell: what "an architecture node" or "the test level" is. Neither term is defined anywhere in the document, and no test levels are ever named.
    Guess: read "architecture node" as some unit of the architecture document, and "test level" as a rank like unit or integration, without confirmation.
    Non-blocking.

16. **"The architecture document, the recorded decision, and the test matrix hold the answers"**
    Where: bolded item "A fix comes from the spec's own neighbours."
    What a stranger cannot tell, at this point in the page: whether "the architecture document" names the file `ARCHITECTURE.md`, seen only later, in an unrelated freeze command.
    Guess: assumed "the architecture document" means `ARCHITECTURE.md`, confirmed only by a later command line.
    Non-blocking.

17. **"a cold reader who puts the old text and the new text side by side and reports every difference in meaning"**
    Where: the four checks that run after the section is repaired, second bullet.
    What a stranger cannot tell: this reuses the name "the cold reader" for a task the role definition never describes. "The roles and the words this skill uses" says the cold reader "reports where it stopped, and it repairs nothing" — diffing an old and new version for every difference in meaning is a different job. Whether this is one of the two readers from the round, or a third pass, is not stated.
    Guess: read it as a fresh cold-reader pass reused for a diffing task.
    Non-blocking.

18. **"A count above the record fails, and the batch runs again."**
    Where: the census bullet, end of the four post-repair checks.
    What a stranger cannot tell: who reruns the batch — the auditor, an automated process, or the person.
    Guess: assumed the auditor reruns it, by analogy with the rest of the loop.
    Non-blocking.

19. **"the recorded map of a guarded document's anchors, marker lines, numbers, and paths"**
    Where: paragraph defining "the frozen baseline."
    What a stranger cannot tell: what a "marker line" is, as distinct from an anchor or a number. The term appears once and is never defined.
    Guess: read it as a structural line the freeze check watches, such as a heading or a section divider.
    Non-blocking.

20. **"runs the census comparison over every live document"**
    Where: "At the push, `python3 guardrails/check-doc-findings-bound.py` runs the census comparison…"
    What a stranger cannot tell: what makes a document "live" as opposed to some other state. The word is never defined or contrasted with anything in this document.
    Guess: read "live" as "currently tracked in the repository."
    Non-blocking.

21. **"A run over ten documents met four such refusals on 2026-08-05 and read them as coverage."**
    Where: "The mechanical lints," the paragraph after the three-scripts refusal rule.
    What a stranger cannot tell: which run this was, where it is recorded, or what "read them as coverage" cashes out to in practice — did someone count a refusal as if the lint had actually checked the text? No file is named, and no corrective step is spelled out.
    Guess: read it as a cautionary example that a refusal should never be counted as a passing check, without being able to confirm the event or the exact mistake.
    Blocking.

22. **"No sentence names a thing by denying its neighbour, and no adjective grades a result's size."**
    Where: "The mechanical lints," bullet "Style and register."
    What a stranger cannot tell: what "denying its neighbour" means as a rule to apply. The grep fallback for this bullet ("read for those four classes by hand… The last one shows up as *big*, *huge*, *minor*, or *breakthrough*") only illustrates the size-grading class, leaving this one with no example anywhere in the document.
    Guess: could not construct what pattern to search for; guessed it means a sentence defining one thing only by contrast with something else, with no confidence.
    Blocking.

23. **"A human-prose sentence aims at the band of 15 to 25 words."**
    Where: "The mechanical lints," bullet "Style and register," compared against "The register carries the word cap: 25 words for a human-prose sentence" earlier, under "The roles and the words this skill uses."
    What a stranger cannot tell: whether these are the same rule restated (a 25-word cap, informally called a "band" here) or two different constraints, one of which adds a 15-word floor never mentioned at the first statement.
    Guess: read both as the same rule, with 15 as an informal floor added only at the second mention.
    Non-blocking.

24. **"which prints 38 kinds of place to stop"**
    Where: "The cold reader," opening paragraph, "One reads under `references/reader-prompt.md`, which prints 38 kinds of place to stop."
    What a stranger cannot tell, without leaving the page: this number is wrong. Counting the bulleted list in `references/reader-prompt.md` gives 39 items, and that file's own text states the count directly: "This prompt prints every rule bound to human prose whose owner is a skill: 39 of the 66 rules the rule home carries." The two files disagree on their own count.
    Guess: trusted the referenced file's stated "39" over this document's "38."
    Blocking.

25. **"`docs/language-defects.md` holds a narrower list — the places only one of the two readers found, which block nothing."**
    Where: "The loop," opening paragraph, compared against "What each reader is handed, and what each one brings back," "In the same measurement it alone caught whether the document can be used. It found these: … a rule its own evidence contradicts; an arithmetic error in a worked example."
    What a stranger cannot tell: these two passages disagree. The first states that anything found by only one reader is non-blocking by definition. The second describes findings the unprompted reader alone caught — a contradicted rule, an arithmetic error — that read as exactly the blocking-caliber kind the document elsewhere calls out ("a claim with no findable ground").
    Guess: read the later passage as the more reliable one, and treated the opening claim as an overstatement.
    Blocking.

26. **"In a measurement over three documents on 2026-08-05, it alone caught local sentence mechanics."**
    Where: "What each reader is handed, and what each one brings back," paragraph on the prompted reader.
    What a stranger cannot tell: which three documents, or where this measurement is recorded. No file is named anywhere for it, unlike the plan and report files cited elsewhere in the document.
    Guess: took the finding on faith with no way to check it.
    Blocking.

27. **"One reading by the unprompted reader brings back about 26 stops per document, and one reading by the prompted reader about 45."**
    Where: "What the pass costs," paragraph after the two bulleted totals.
    What a stranger cannot tell, without doing the arithmetic: this does not follow from the totals given two sentences earlier for "the three documents read on 2026-08-05" — 227 stops and 128 stops. 227 ÷ 3 ≈ 76 and 128 ÷ 3 ≈ 43, not 45 and 26. Dividing by five instead gives 45.4 and 25.6, matching the stated "about 45" and "about 26" almost exactly, which suggests the totals belong to five documents, not three.
    Guess: read the totals and the "three documents" label as the error, since the per-document math only works out against five documents.
    Blocking.

28. **"A second measurement on the same day read a publish candidate with three readers." / "The unprompted readers alone caught the arithmetic error…"**
    Where: "What the pass costs," closing paragraph.
    What a stranger cannot tell: how "three readers" and a plural "the unprompted readers" square with the process defined everywhere else in the document, which always runs exactly two readers — one prompted, one unprompted ("Hand the text to two fresh sessions," "the reading step runs two cold readers"). Nothing here says whether the loop sometimes runs a third reader, or whether this measurement used a different setup than the one this skill actually prescribes.
    Guess: read it as an exceptional, unexplained third participant added just for this one measurement, not a change to the two-reader process.
    Blocking.

29. **"a dated file written into the reader's repository"**
    Where: "What the pass costs," closing paragraph, list of what the unprompted readers caught.
    What a stranger cannot tell: what "the reader's repository" is. A cold reader is defined as holding no repository of its own — it works from the page and, for the unprompted reader, from the steps it runs. This introduces a new, undefined idea of a reader owning a repository.
    Guess: read it as the checkout the fresh reader session happened to be running in, not a repository the role is defined to hold.
    Non-blocking.

30. **"`docs/spec-style.md` states that separation: a writer or reader holding the project's rules is kept apart from one who does not."**
    Where: "The cold reader," paragraph on zero context.
    What a stranger cannot tell: what that separation actually says or why it holds — the document points to a file rather than stating the reasoning here.
    Guess: took the claim on faith without seeing the source text.
    Non-blocking.

31. **"A passing run prints one line saying that the file is clean."**
    Where: "This skill is held to the rules it lists," paragraph on `preshow-register-lint.py`.
    What a stranger cannot tell: by what measure the script calls a file "clean" — no threshold is stated at this point on the page, only inferable from the mechanical-lints section much earlier.
    Guess: read "clean" as "zero findings from the lints described earlier in the document."
    Non-blocking.

Blocking entries: 11 (undated, unnamed "separate review" claiming four defects), 21 ("read them as coverage" with no citable run or clear meaning), 22 ("denying its neighbour" — a class with no example anywhere in the text), 24 ("38 kinds" contradicts reader-prompt.md's own stated count of 39), 25 (opening claim that solo-found stops "block nothing" contradicted by the unprompted reader's own solo blocking-caliber finds), 26 (ungrounded "measurement over three documents" claim), 27 (per-document averages of 45 and 26 don't follow from totals stated for three documents — the math implies five), 28 ("three readers" / "the unprompted readers" contradicts the document's own two-reader process).
