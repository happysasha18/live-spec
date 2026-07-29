# Cold read of `skills/text-audit/SKILL.md` (with `references/reader-prompt.md` and `references/human-prose-rules.md`), read 2026-07-29

Stops: 37 — 6 blocking

1. "no stranger returns to a worker brief, a checkpoint, or an internal note"
   - Where: the frontmatter description, repeated under "Work that belongs elsewhere".
   - What a stranger cannot tell: what a worker brief and a checkpoint are. Both are named as kinds of text the skill refuses, and neither is defined anywhere in the three files. A worker brief also appears in the six-surface list without a gloss.
   - My guess: a worker brief is the instruction text one agent hands another, and a checkpoint is a saved progress note inside a run.
   - Non-blocking.

2. "Four scopes settle a setting there: the session's live word first, then the host profile, the personal profile, and the package default."
   - Where: the blockquote under the title, "Part of the live-spec pack".
   - What a stranger cannot tell: what any of the four scopes is, and which settings of this skill they can move. Nothing later in the document names a setting that a profile could change, so the sentence has no visible effect on the audit.
   - My guess: they are configuration layers somewhere else in the repository, and I can run the whole loop without touching them.
   - Non-blocking.

3. "Part of the **live-spec pack**"
   - Where: the blockquote under the title.
   - What a stranger cannot tell: what a pack is. The word carries weight through the whole document — "inside the pack", "with the pack not loaded" — and the membership list arrives only in the final section, 340 lines later.
   - My guess: a pack is a bundle of skills installed together, and its members are the eleven names at the foot of the file.
   - Non-blocking.

4. "The loop came from the comprehension gate on spec sections, recorded in `docs/spec-format.md`." / "Those readers found new blocking terms on every pass, and the terms already repaired stayed repaired."
   - Where: the two paragraphs before "The roles and the words this skill uses".
   - What a stranger cannot tell: what those readings actually observed — how many passes ran, over what text, and how many terms came back. The page states the outcome and points at a file for the record. `human-prose-rules.md` prints this very sentence as the recorded case for rule `r71`, whose repair is "what that gate observed, stated on the page". The document breaks a rule its own companion file states.
   - My guess: the observation exists in `docs/spec-format.md` and I am expected to take it on faith.
   - Non-blocking.

5. "A finding **blocks** when the reader could not go on, or would have applied the text wrongly."
   - Where: the paragraph beginning "The loop came from the comprehension gate", against "An undefined term the rest of the text leans on blocks. So does a relational word whose slot decides what the reader does, and a claim with no findable ground" under "The cold reader".
   - What a stranger cannot tell: which of the two statements is the definition. They sit 244 lines apart and do not say the same thing: the first is a test of the reader's experience, the second is a list of three finding kinds. A term whose slot did not decide anything, but which the reader still could not pass, passes one test and fails the other. The loop's exit condition — two reads with zero blocking findings — rests entirely on this word.
   - My guess: the second passage is the operative one and the first is a preview, so I judged by the three kinds.
   - Blocking.

6. "Every reading is written to a dated **reading record** under `docs/language-reads/`, and `docs/language-defects.md` records what each one returned."
   - Where: the paragraph beginning "Those readers found new blocking terms".
   - What a stranger cannot tell: what goes in which file. The next sentence says the reading record already "carries every stop", so the second file records the same thing under a second name. An auditor finishing a pass cannot tell whether one output is owed or two, nor what shape the second takes.
   - My guess: the reading record is the per-run file and `docs/language-defects.md` is a rolling summary, so I wrote only the reading record.
   - Blocking.

7. "One person may hold the auditor role and own the text"
   - Where: "The roles and the words this skill uses", against the bullet "**the auditor** — the session running this skill".
   - What a stranger cannot tell: whether the auditor is a person or a model session. The bullet defines it as a session; the sentence above it hands the role to a person. The two readings differ in by-hand mode, where no session runs.
   - My guess: the auditor is whoever runs the steps, model or person, and the bullet is written for the in-pack case.
   - Non-blocking.

8. "**A surface is a kind of text.** One file carries several kinds."
   - Where: the paragraph opening "**A surface is a kind of text.**", six lines below the identical definition "A **surface** is a kind of text. One file carries several kinds at once".
   - What a stranger cannot tell: why the definition is given twice, and whether the second statement adds a distinction I missed. `human-prose-rules.md` states rule `r56`: one fact lives in one home.
   - My guess: an editing leftover, with no difference between the two.
   - Non-blocking.

9. "A README, a report, a decision page, and a skill body stand on human prose."
   - Where: "This skill runs on a text standing on any surface a person reads".
   - What a stranger cannot tell: what a decision page is. It appears four times across the document, always as an example, never with a gloss.
   - My guess: a page written to put a choice in front of a person, with the options laid out.
   - Non-blocking.

10. "The word cap arrives with the register: 25 words for a human-prose sentence, and 35 for a spec-body criterion (rule `r08`)."
    - Where: the paragraph defining the register, against "A sentence past the cap for its surface is a hit, and 15 to 25 words is the band a human-prose sentence aims at" under "The mechanical lints".
    - What a stranger cannot tell: which statement to work from. The first gives a single ceiling, the second gives a band with a floor of 15 that the first never mentions. A 12-word sentence is clean by the first and short of the band by the second.
    - My guess: 25 is the hard cap the lint enforces and 15 is advice, so I treated only the ceiling as a hit.
    - Non-blocking.

11. "the six surfaces, the three words above, and every rule of every register are edited"
    - Where: the last line of "The roles and the words this skill uses".
    - What a stranger cannot tell: which three words. Four bolded terms stand above it — surface, register, class, and the three role names — so the count does not select a set on its own. This is the class rule `r07` names.
    - My guess: surface, register, and class.
    - Non-blocking.

12. "Load it when a human-facing text is about to ship and its clarity matters"
    - Where: "When it fires".
    - What a stranger cannot tell: who decides that clarity matters here and not there, and by what measure. Every text a person reads has some claim on clarity, so the condition selects nothing.
    - My guess: the person asking decides, and the four bullets under the sentence are the real trigger list.
    - Non-blocking.

13. "The comprehension gate settled on two reads, and `docs/spec-format.md` records that pattern."
    - Where: step 4 of "The loop".
    - What a stranger cannot tell: why two and not three, and what "settled on" means — whether someone chose the number or a run produced it. The exit condition of the whole loop rests on it, and its ground is off the page.
    - My guess: two consecutive clean reads was found sufficient in practice and the file records the runs behind it.
    - Non-blocking.

14. "A section-sized run puts one definition and a handful of sentences in front of a reader."
    - Where: the paragraph closing "The loop".
    - What a stranger cannot tell: how much text a section-sized run holds. "A handful" is exactly the vagueness rule `r33` records, whose printed repair is "state the exact quantity". The spec-section section gives a real size (ten requirements, about 250 lines); the human-prose case gets none.
    - My guess: roughly one heading and its paragraphs, five to ten sentences.
    - Non-blocking.

15. "The plan chose that size and gave two reasons for it" / "A fresh reader holds that much"
    - Where: "Running it on a spec section", the paragraph beginning "Ten requirements at a time".
    - What a stranger cannot tell: who chose the batch size — a document cannot choose, which is the class rule `r05` names — and by what measure a fresh reader was found to hold 250 lines. No test or observation is named.
    - My guess: the author chose ten, wrote the plan, and "holds that much" is a judgment from experience rather than a measurement.
    - Non-blocking.

16. "It is the mechanical lint only a spec section runs: `python3 guardrails/check-requirement-shape.py FILE`."
    - Where: "**The requirement-shape lint applies here.**"
    - What a stranger cannot tell: whether the claim is true. Under "The mechanical lints", the style bullet names `python3 scripts/spec-style-lint.py FILE` "for a spec section", so at least two lints are spec-only. Running a spec section, I cannot tell whether the style lint is a second spec-only check or whether one of the two statements is stale.
    - My guess: both scripts are spec-only and the word "only" is wrong, so I ran both.
    - Blocking.

17. "It reads three things nobody would ask of a README. Context comes before criteria. Each criterion carries one trigger and one response. Every judgment names a judge and a measure."
    - Where: "**The requirement-shape lint applies here.**", against the bullet "**A spec section owes the requirements genre.**" under "The mechanical lints", which states the same three clauses again in one sentence.
    - What a stranger cannot tell: whether the second statement is the same rule or a second, similar one. Both name the same script.
    - My guess: one fact written in two places.
    - Non-blocking.

18. "The first rule binds the criterion lines and the second binds the Context paragraphs"
    - Where: "**A criterion and the prose around it take different rules.**"
    - What a stranger cannot tell: which rule is which without going back and counting sentences. The paragraph names them by position, which is the class rule `r63` names. The same move appears twice more: "The third is four commands of its own" and "run the first two checks".
    - My guess: the third-person criterion rule is first, the address-the-reader rule is second.
    - Non-blocking.

19. "the map a script builds from the body criteria at freeze"
    - Where: the bullet defining the code-to-location table.
    - What a stranger cannot tell: which script builds it, and what "freeze" is. The frozen baseline and `scripts/spec-freeze.py` arrive 34 lines later, so the term is used before its definition; and the actor is left as "a script".
    - My guess: freeze is the moment `spec-freeze.py --freeze` runs, and some unnamed generator builds the table around then.
    - Non-blocking.

20. "whose rows pair one architecture node with one spec fact and pin the test level that covers it"
    - Where: the bullet defining the test matrix.
    - What a stranger cannot tell: what an architecture node is, what a spec fact is, and what a test level is. Three undefined terms carry the sentence, and none is defined anywhere in the three files.
    - My guess: a node is a component in the architecture document, a spec fact is one acceptance criterion, and a test level is how deep the test runs.
    - Non-blocking.

21. "Four checks run after the section is repaired, and each one reports what it read."
    - Where: the paragraph introducing the post-repair check list.
    - What a stranger cannot tell: what "reports what it read" asks of me. Two of the four are scripts that print their own output; the second reader is a session; the census compares counts. Whether I must transcribe each output somewhere, and where, is unstated.
    - My guess: each check leaves a visible result I copy into the reading record.
    - Non-blocking.

22. "`bash guardrails/check-freeze.sh` — the three guarded documents match the frozen baseline"
    - Where: the fourth structure-check bullet.
    - What a stranger cannot tell: which three documents are guarded, and what a frozen baseline is, at the moment of reading. Both arrive eleven lines later, in the paragraph beginning "The frozen baseline is the recorded map".
    - My guess: `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, and `TEST_MATRIX.md`, from the freeze command below.
    - Non-blocking.

23. "runs the census comparison over every live document"
    - Where: "At the push, `python3 guardrails/check-doc-findings-bound.py`".
    - What a stranger cannot tell: what makes a document live, and therefore which files the push check covers. The word appears once, undefined.
    - My guess: every document recorded in `guardrails/rule-census.json`.
    - Non-blocking.

24. "The measure is set out in `docs/plans/2026-07-28-top-level-readability.md`, which takes the count before and after each batch, by two different fresh agents." against "No record stands behind any build test."
    - Where: "**The build test measures the work once the audit has closed.**" and the paragraph after it.
    - What a stranger cannot tell: whether the build test is a procedure I must run or a plan nobody has run. The first paragraph describes it in the present tense as something the plan takes before and after each batch; the next says no record names the requirements, the agent, or the output of any run. The heading "The method's build-test evidence is owed" promises evidence and the body reports its absence.
    - My guess: the build test is specified but unrun, so I skipped it and did not treat it as part of closing the audit.
    - Blocking.

25. "Which copy of that list a run reads: the `weak-words.json` sitting beside the `check-weak-words.py` that ran."
    - Where: the third sub-bullet under "**A weak relational word fills the slot it opens.**"
    - What a stranger cannot tell: whether this is a heading, a question, or a statement. It is written as a question with a colon instead of a question mark, and I read it twice to find its verb.
    - My guess: it answers "which copy does a run read", and the answer is the file beside the script.
    - Non-blocking.

26. "A project holding no such file gets one, carrying a `weak_words` list."
    - Where: the fourth sub-bullet under "**A weak relational word fills the slot it opens.**"
    - What a stranger cannot tell: who creates the file, where it goes, and what shape it takes. The action sits in "gets one" with no actor, and the file's format is given as one key with no example.
    - My guess: the auditor writes `weak-words.json` beside the script, holding a JSON object with a `weak_words` array of strings.
    - Non-blocking.

27. "A mechanical hit is fixed before the cold reader runs, so no reader spends a finding on a class a machine already owns."
    - Where: the closing line of "The mechanical lints", against step 1 of "The loop": "Fix each hit at this step. ... The cold reader then spends its attention on what no script can judge".
    - What a stranger cannot tell: whether this adds a rule or repeats one. Both the instruction and its reason already stand in step 1.
    - My guess: a restatement.
    - Non-blocking.

28. "In this pack that means a fresh worker with the pack not loaded"
    - Where: "The cold reader", second paragraph.
    - What a stranger cannot tell: whether a worker and a session are the same thing. The definition near the top says "Inside the pack a cold reader is a fresh session"; here the same thing is a worker. Rule `r04` in the companion file says one thing carries one name.
    - My guess: the same thing under two names.
    - Non-blocking.

29. "Inventing an answer to close a finding is the one move this skill forbids."
    - Where: the closing paragraph of "Where a fix comes from".
    - What a stranger cannot tell: how to square "the one move" with the other prohibitions the document states — the cold reader repairs nothing, the skill grades no voice, a rewrite must not move a bracket anchor or a quoted phrase.
    - My guess: it is the one forbidden move for the fix-writing step, not for the skill as a whole.
    - Non-blocking.

30. "The same editor runs one cold-reader loop over the changed section before the skill ships."
    - Where: "This skill is held to the rules it lists".
    - What a stranger cannot tell: what "one loop" is. "The loop" is defined as running until two consecutive reads return zero blocking findings, so one loop is already several reads; but "one" reads naturally as a single pass. An editor changing this file cannot tell whether one read or two clean reads is owed.
    - My guess: the full loop to its two-clean-reads close, over the changed section only.
    - Blocking.

31. "Paste the block below verbatim into the cold-reader session, under the body's definition of a blocking finding, with the text appended."
    - Where: `references/reader-prompt.md`, the paragraph before the pasted block.
    - What a stranger cannot tell: which passage of the body to paste. The body carries two statements of what blocks (see entry 5), and they do not agree. The instruction is a step I have to carry out and the material it names is ambiguous, so the cold reader receives a different test depending on which passage the auditor picks.
    - My guess: the three-kind passage under "The cold reader".
    - Blocking.

32. "That last instruction keeps a reader catching words the list does not carry yet."
    - Where: `references/reader-prompt.md`, the closing paragraph, against the third paragraph: "The prompt's last instruction takes every other stop the reader met, so a class outside the five still comes back."
    - What a stranger cannot tell: whether the closing paragraph adds anything. Both sentences state the same purpose for the same instruction, twelve lines apart, in a file of 52 lines.
    - My guess: a restatement.
    - Non-blocking.

33. "the skill body's weak-word lint says which copy of that list takes the edit"
    - Where: `references/reader-prompt.md`, the closing paragraph.
    - What a stranger cannot tell: where in the body to look. The body has no item called the weak-word lint; the bullet is titled "A weak relational word fills the slot it opens", and the section is "The mechanical lints". One thing under two names.
    - My guess: the second bullet under "The mechanical lints".
    - Non-blocking.

34. "Two of those pages carry more than this sheet does. `docs/language-rules.md` gives each rule with its examples ... `docs/language-worked-example.md` walks one short document end to end"
    - Where: `references/human-prose-rules.md`, the paragraph after the four-artifact list.
    - What a stranger cannot tell: how `docs/language-worked-example.md` can be one of "those pages" when it is not among the four artifacts the sentence points back to. The list above names `docs/language-rules.md`, `docs/language-rule-coverage.md`, `hooks/language-laws.json`, and the printed block.
    - My guess: the worked example is a separate file the sentence pulls in loosely, and the intended pair was the writer's page and the maintainer's page.
    - Non-blocking.

35. "The right side shows its repair, or an instruction where the repair depends on facts the case does not carry."
    - Where: `references/human-prose-rules.md`, the paragraph beginning "Each entry names the class of mistake".
    - What a stranger cannot tell: what the repair depends on and by what measure the choice is made. "Depends" is on the file's own list of slot-opening words, and rule `r33` printed twelve lines below requires the slot filled where the word stands. The file breaks the rule it prints.
    - My guess: where the case's own text does not fix the value, the entry prints an instruction instead of a rewrite.
    - Non-blocking.

36. "A documentation page carries `artifact` as well once it is published outside the project."
    - Where: `references/human-prose-rules.md`, the first paragraph of the generated block.
    - What a stranger cannot tell: whether `artifact` in code font is the same thing the body calls "a published artifact" and "the artifact surface". Three spellings for one surface, and the code font suggests a key in a file the reader cannot see.
    - My guess: the same surface, named by its identifier in `guardrails/language-rules.json`.
    - Non-blocking.

37. "`the door` → `the entry point`"
    - Where: `references/human-prose-rules.md`, the recorded case under rule `r02`.
    - What a stranger cannot tell: what "the door" referred to, so I cannot see the mistake the case is evidence for. The rule asks whether a standard word already names the thing; the case shows a coined word replaced by a phrase, with the thing itself never named.
    - My guess: "the door" was this project's word for some gate or entry step, and the case shows only the substitution.
    - Non-blocking.

Blocking entries: 5, 6, 16, 24, 30, 31.
