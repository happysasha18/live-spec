# Cold read of `skills/text-audit/SKILL.md` and its two companion files, 2026-07-29

Read as a stranger: `skills/text-audit/SKILL.md`, plus the two files its body sends the reader to,
`references/reader-prompt.md` and `references/human-prose-rules.md`. Nothing else was opened.

Stops: 46 — 9 blocking

1. **"Part of the **live-spec pack**"**
   - Where: the blockquote under the heading `# text-audit — read a text as a stranger, fix where they stop`.
   - What a stranger cannot tell: what a pack is. The last section lists eleven named skills under
     "The pack this skill belongs to", but no sentence says what a pack is, how one is installed, or
     whether a reader needs the others on disk to use this one.
   - My guess: a pack is a bundle of skills shipped together, and this skill can be read alone.
   - Non-blocking.

2. **"Four scopes settle a setting there: the session's live word first, then the host profile, the personal profile, and the package default."**
   - Where: same blockquote.
   - What a stranger cannot tell: what a setting is here, what any of the four scopes is, or which
     setting of this skill they ever change. None of the four names returns anywhere in the document.
   - My guess: they govern options like language and cadence, and nothing in this audit depends on them.
   - Non-blocking.

3. **"Used on its own, this skill is plain advice a person applies by hand"**
   - Where: same blockquote.
   - What a stranger cannot tell: on its own relative to what. The alternative is unnamed at this point;
     "The by-hand mode" arrives twelve screens later.
   - My guess: on its own means without the rest of the pack installed.
   - Non-blocking.

4. **"It runs on any text a person will read: a spec section, a README, a decision page, marketing copy, an article, a release note."**
   - Where: the paragraph opening "An author cannot be their own cold reader."
   - What a stranger cannot tell: what `It` points at. The nearest previous subject is "The prompt",
     one sentence back; the intended subject appears to be the skill.
   - My guess: `It` means this skill, not the prompt.
   - Non-blocking.

5. **"The loop came from the comprehension gate on spec sections, recorded in `docs/spec-format.md`."**
   - Where: the paragraph opening "The loop came from".
   - What a stranger cannot tell: which loop. "The loop" arrives as a definite thing before any loop has
     been described; the section named "The loop" comes later. The ground for the claim sits in a file
     this page does not carry.
   - My guess: the loop is the four-step audit described further down.
   - Non-blocking.

6. **"Those readers found new blocking terms on every pass, and the terms already repaired stayed repaired."**
   - Where: the paragraph opening "Those readers found".
   - What a stranger cannot tell: what blocking means — the word is used here and defined only in
     "The cold reader", far below. Nor how many passes ran, on what text, or where a reader sees the
     record. "Every pass" counts something the page never sizes.
   - My guess: several passes over spec sections, with the readings filed under `docs/language-reads/`.
   - Non-blocking.

7. **"Three roles run through this skill, and one person often holds more than one of them."**
   - Where: "The roles and the words this skill uses".
   - What a stranger cannot tell: how a person holds the auditor role, when the same list defines the
     auditor as "the session running this skill" and the cold reader as "the fresh reader" that is a
     fresh session. Two of the three roles are named as software; the sentence over them says person.
   - My guess: in the by-hand mode a person plays all three, and the definitions describe the in-pack case.
   - Non-blocking.

8. **"A text declares one primary surface: the kind of text it is written to be."**
   - Where: the bold lead "**One rule settles the surface a text stands on.**"
   - What a stranger cannot tell: who declares it, where the declaration is written, and what a reader
     does when nothing declares it. Everything downstream — which register binds, which word cap
     applies, which lints run — hangs on this answer, and the page gives no way to reach it.
   - My guess: the auditor decides the surface by eye, matching the text against the six named surfaces.
   - Blocking.

9. **"Every rule binding either surface is then in force."**
   - Where: same bold lead, one sentence after the artifact sentence.
   - What a stranger cannot tell: how this squares with the next paragraph, "It holds that text to the
     register of the text's own primary surface." One sentence says two registers bind a published
     text; the other says one. A published README lands in both readings at once, and they disagree.
   - My guess: both bind, and the later sentence is a loose restatement that forgot the artifact case.
   - Blocking.

10. **"The word cap arrives with the register: 25 words for a human-prose sentence, and 35 for a spec-body criterion (rule `r08`)."**
    - Where: the paragraph defining register.
    - What a stranger cannot tell: where either number comes from. The cited `r08`, printed in
      `human-prose-rules.md`, states "It stays under the word cap for its surface" and carries no
      number at all. The number that does appear in that file sits under `r06` as 15 to 25, and the
      skill body later writes the band as "15 to 25 words". A reader chasing 35 finds nothing. The
      citation also names the rule by its code, so I had to leave the sentence to learn what r08 says.
    - My guess: 25 and 35 are set in `guardrails/language-rules.json`, which the printed sheet does not
      reproduce.
    - Blocking.

11. **"`guardrails/language-rules.json` is the file where the six surfaces, the three words above, and every rule of every register are edited."**
    - Where: end of "The roles and the words this skill uses".
    - What a stranger cannot tell: which three words. I had to scroll back and count bolded terms —
      surface, register, class — and I am still unsure whether the three roles were meant instead.
    - My guess: surface, register, class.
    - Non-blocking.

12. **"Load it when a human-facing text is about to ship and its clarity matters"**
    - Where: "When it fires".
    - What a stranger cannot tell: who judges that clarity matters, and by what measure. Every text a
      person reads would seem to qualify, which makes the condition carry nothing.
    - My guess: the person asking for the audit decides, and the condition is decoration.
    - Non-blocking.

13. **"with whatever writing skills the host installs beside the pack"**
    - Where: "Work that belongs elsewhere", the "Taste and voice" bullet.
    - What a stranger cannot tell: what a host is. The word returns once more, in "host profile", also
      undefined.
    - My guess: the host is the organisation or machine the pack is installed into.
    - Non-blocking.

14. **"Machine-read text needs no cold reader, because no stranger returns to it. A worker brief, a checkpoint, and an internal note are machine-read."**
    - Where: "Work that belongs elsewhere", last bullet.
    - What a stranger cannot tell: what "returns to" means — returns as in comes back to a text, or as
      in reports back? I read the sentence twice. A worker brief and a checkpoint are also undefined.
    - My guess: no stranger ever reads such a text, so no comprehension check is owed.
    - Non-blocking.

15. **"The five lints under "The mechanical lints" are that whole set."**
    - Where: step 1 of "The loop".
    - What a stranger cannot tell: whether the set really closes. The sentence before it says "Run every
      check a script or a grep settles", which is an open description, and the sentence after declares
      exactly five. A reader with a sixth script on disk cannot tell whether to run it.
    - My guess: the five listed lints are the complete required set, and any other script is optional.
    - Non-blocking.

16. **"Each fresh reader catches a class the reader before it did not reach, so a single clean read can still hide a blocking class."**
    - Where: step 4 of "The loop".
    - What a stranger cannot tell: what this rests on. It is stated as a general law about readers, and
      the page offers no observation, count, or record behind it.
    - My guess: it comes from the same spec-format gate history mentioned earlier.
    - Non-blocking.

17. **"A section-sized run puts one definition and a handful of sentences in front of a reader."**
    - Where: the paragraph after the four numbered steps.
    - What a stranger cannot tell: how many sentences a handful is. The document's own rulebook, `r33`,
      carries the case `a few` → `state the exact quantity`, so the text breaks a rule it ships.
    - My guess: roughly five to fifteen sentences.
    - Non-blocking.

18. **"A spec section here is one requirement with its Context paragraph, its User Story, and its acceptance criteria."**
    - Where: "Running it on a spec section".
    - What a stranger cannot tell: what a Context paragraph, a User Story, or an acceptance criterion is.
      All three are capitalised names of parts, and none is defined anywhere in the three files. The
      whole section instructs a reader to check that Context comes before criteria and that each
      criterion carries one trigger and one response, which cannot be done without the definitions.
    - My guess: they are the fixed parts of a requirement in this project's spec format, defined in
      `docs/spec-format.md`.
    - Blocking.

19. **"Ten requirements at a time is the working size ... A fresh reader holds that much"**
    - Where: "Running it on a spec section", second paragraph.
    - What a stranger cannot tell: what holds means, and by what measure ten was found to be the limit
      rather than eight or twenty. "The plan chose that size and gave two reasons for it" names a count
      before the reasons, and points at a plan file the page does not carry.
    - My guess: ten fits comfortably in one reading, and the plan file records the trial that settled it.
    - Non-blocking.

20. **"A rule binds a whole region of the file, so those two rules never both judge one sentence."**
    - Where: the bold lead "**A criterion and the prose around it take different rules.**"
    - What a stranger cannot tell: what a region is and where one ends. The paragraph gives two opposite
      rules — third person for a criterion, direct address for a Context paragraph — and this sentence
      is the only thing that keeps them from colliding. I reread it twice and still cannot say which
      rule judges a sentence sitting inside a criterion's sub-bullet.
    - My guess: a region means a contiguous block such as one Context paragraph or one criteria list,
      and its boundaries are the spec format's own headings.
    - Blocking.

21. **"A rewrite that moves one of them breaks a test, or one of the two maps below."**
    - Where: the bold lead "**Every mark a machine reads survives the repair.**"
    - What a stranger cannot tell: what "them" covers. Four things were named above — the requirement's
      number, the bracket anchors, the headings, and any phrase a test quotes — and the sentence points
      back at some subset of them.
    - My guess: all four.
    - Non-blocking.

22. **"the map a script builds from the body criteria at freeze"**
    - Where: the "code-to-location table" bullet.
    - What a stranger cannot tell: what freeze is. The word arrives here as a known event; the frozen
      baseline is explained only two pages later. "Body criteria" is also undefined, as is which script
      builds the map.
    - My guess: freeze is the moment `scripts/spec-freeze.py --freeze` runs.
    - Non-blocking.

23. **"whose rows pair one architecture node with one spec fact and pin the test level that covers it"**
    - Where: the "test matrix" bullet.
    - What a stranger cannot tell: what an architecture node is, what a test level is, or what values a
      level takes. Neither term is defined in any of the three files.
    - My guess: a node is a component in an architecture document, and a level is something like unit,
      DOM, or browser.
    - Non-blocking.

24. **"The third is four commands of its own:"**
    - Where: the lead-in to the four post-repair checks.
    - What a stranger cannot tell: which check is the third, without reading ahead into the list and
      counting. The thing is named by its position instead of by what it is.
    - My guess: the structure checks.
    - Non-blocking.

25. **"Run the audited project's own suite command, whatever it is"**
    - Where: the first bullet of the four post-repair checks.
    - What a stranger cannot tell: how to find that command. Every other check on the page names an
      exact command line; this one names none and offers no way to discover it. A reader auditing a
      project they did not write cannot carry out the step.
    - My guess: read the project's README or its package manifest and hope a test command is written
      there.
    - Blocking.

26. **"It counts findings per file: sentences past the human-prose word cap, plus the findings of the style lint and of the register lint."**
    - Where: the census bullet.
    - What a stranger cannot tell: how the census applies to a README. The lints section says
      `scripts/spec-style-lint.py` is "for a spec section" and the register lint is "for any
      human-facing surface", so a README has no style-lint count to add. Yet the census total is what
      the push gate compares, and a missing component would change the number.
    - My guess: on a non-spec file the style-lint contribution is zero, and the sentence describes the
      spec case only.
    - Blocking.

27. **"`bash guardrails/check-freeze.sh` — the three guarded documents match the frozen baseline"**
    - Where: the structure-checks list.
    - What a stranger cannot tell: which three documents, and what makes a document guarded. The three
      names appear only later, as arguments to a different command.
    - My guess: `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, and `TEST_MATRIX.md`.
    - Non-blocking.

28. **"runs the census comparison over every live document"**
    - Where: the paragraph opening "At the push".
    - What a stranger cannot tell: what makes a document live, and how one is distinguished from a
      document that is not. The word appears once and is never defined.
    - My guess: every document currently tracked in `guardrails/rule-census.json`.
    - Non-blocking.

29. **"**The method's build-test evidence is owed.** No record stands behind any build test."**
    - Where: the last two bold leads of "Running it on a spec section".
    - What a stranger cannot tell: whether to run the build test at all. The paragraph above it
      prescribes the test as a measure with a target count, and this paragraph says no such run was
      ever recorded and the skill states no build count. I cannot tell whether I am reading a required
      step, a proposed step, or a step withdrawn. "Is owed" also reads two ways: owed by whom, to whom.
    - My guess: the build test is optional and unproven, and skipping it costs the audit nothing.
    - Blocking.

30. **"Each lint names a script and a grep fallback."**
    - Where: opening of "The mechanical lints".
    - What a stranger cannot tell: why the "Style and register" bullet then names two scripts, under a
      plural heading "Scripts". The document states a rule and breaks it four bullets later.
    - My guess: that bullet covers two lints folded into one entry.
    - Non-blocking.

31. **"Words such as *depends*, *related*, *handles*, *based on*, *corresponds to*, *proportional*, *larger*, *sufficient*, *appropriate*, *fast*, and *easily* open a slot."**
    - Where: the weak-relational-word bullet.
    - What a stranger cannot tell: nothing is missing, but eleven parallel items run inside one
      sentence, and the rulebook this skill ships (`r64`) says such items become a list, one per line.
      I lost the thread twice while parsing it. The same shape appears at "The live-spec repository
      names six surfaces:".
    - My guess: the list was left inline for compactness.
    - Non-blocking.

32. **"A project holding no such file gets one, carrying a `weak_words` list."**
    - Where: the weak-relational-word bullet, third sub-bullet.
    - What a stranger cannot tell: who creates the file, where it is placed, and what its name is. The
      key is written `weak_words` and the file elsewhere is `weak-words.json`, so I cannot tell which
      of the two the sentence is naming.
    - My guess: the auditor writes a `weak-words.json` holding a `weak_words` array, beside the script.
    - Non-blocking.

33. **"Which copy of that list a run reads: the `weak-words.json` sitting beside the `check-weak-words.py` that ran."**
    - Where: the weak-relational-word bullet, second sub-bullet.
    - What a stranger cannot tell: this is a question written without a question mark, and I read the
      colon as a definition before realising the first half is the question. "Sitting beside" is also
      unmeasured — same directory, or anywhere on the same path?
    - My guess: same directory.
    - Non-blocking.

34. **"The last one shows up as *big*, *huge*, *minor*, or *breakthrough*."**
    - Where: the grep fallback of the "Style and register" bullet.
    - What a stranger cannot tell: which class is the last one, without going back and counting the four
      classes in the bullet above. The thing is named by its position.
    - My guess: the adjective that grades a result's size.
    - Non-blocking.

35. **"No named thing appears under two names: a file, a script, a command, or a concept."**
    - Where: the "One name per thing" bullet.
    - What a stranger cannot tell: what the colon list attaches to. On first reading I took the four
      items as the two names; they are kinds of named thing.
    - My guess: a file, a script, a command, and a concept each carry one name.
    - Non-blocking.

36. **"In this pack that means a fresh worker with the pack not loaded, reading the text from outside."**
    - Where: "The cold reader", second paragraph.
    - What a stranger cannot tell: whether a worker is the same thing as the fresh session defined at
      the top and the fresh reader of step 4. One role now carries four names across the page: cold
      reader, fresh session, reader session, fresh worker. A second reader also appears among the
      post-repair checks, outside the list of three roles.
    - My guess: all of them are one role, and the second reader is a fourth role the roles list omits.
    - Non-blocking.

37. **"An undefined term the rest of the text leans on blocks."**
    - Where: "The cold reader", third paragraph.
    - What a stranger cannot tell: on first pass I read "blocks" as a noun. The sentence needs a second
      reading before the verb lands.
    - My guess: such a term counts as a blocking finding.
    - Non-blocking.

38. **"Say so in the record, rather than counting the text as read."**
    - Where: "The by-hand mode", last sentence.
    - What a stranger cannot tell: what the record is, where it lives, and what shape an entry takes.
      The earlier text names `docs/language-reads/` and `docs/language-defects.md` for in-pack runs, but
      the by-hand mode is defined as the case where the repository may be absent. This is the step that
      closes an incomplete audit, and I cannot carry it out.
    - My guess: whatever log the person keeps, with a line saying the cold read did not run.
    - Blocking.

39. **"A README, an article, or a piece of copy takes a bracketed query in the draft."**
    - Where: "Where a fix comes from", the paragraph on a genuine hole.
    - What a stranger cannot tell: what a bracketed query looks like. The spec case gets an exact form,
      `[GAP: what is missing]`; this one gets a description and no example, and I cannot tell whether
      the same `GAP:` marker is meant or a different one.
    - My guess: square brackets holding the open question, without the `GAP:` marker.
    - Non-blocking.

40. **"Four of those rules bind every sentence of this file"**
    - Where: "This skill is held to the rules it lists".
    - What a stranger cannot tell: what the other forty-four do. `human-prose-rules.md` prints 48 rules
      and says every one of them binds human prose, and this file declares itself human prose. Either
      the four are a highlight, or the other forty-four bind something less than every sentence.
    - My guess: all 48 bind, and these four are called out as the ones most often broken.
    - Non-blocking.

41. **"A passing run prints one line saying that the file is clean."**
    - Where: same section.
    - What a stranger cannot tell: what clean means as an output — zero findings, or findings at or
      below the recorded count. The census paragraph allows a passing run with findings, so the two
      sentences describe passing differently.
    - My guess: the register lint prints clean only at zero findings, and the census is the one that
      allows a count.
    - Non-blocking.

42. **"`guardrails/rule-census.json` records this file at zero findings, and `python3 guardrails/check-doc-findings-bound.py` refuses a push that raises that count."**
    - Where: same section.
    - What a stranger cannot tell: why this arrives a second time. The census bullet and the paragraph
      opening "At the push" already state both facts, and the rulebook's `r56` says one fact lives in
      one home with every other place pointing at it.
    - My guess: the repetition is deliberate emphasis for this file's own maintainer.
    - Non-blocking.

43. **"A new slot-opening word joins the weak-word list, and the skill body's weak-word lint says which copy of that list takes the edit."**
    - Where: `references/reader-prompt.md`, the closing paragraph.
    - What a stranger cannot tell: who adds the word. The action sits in a verb with the word itself as
      its actor, and a word cannot join a list. The list is also named three ways across the two files:
      the weak-word list, `weak-words.json`, and a `weak_words` list.
    - My guess: the auditor edits the file by hand, as the skill body's third sub-bullet says.
    - Non-blocking.

44. **"At every relational word, ask the three questions and write which one is unanswered"**
    - Where: `references/reader-prompt.md`, inside the pasted block.
    - What a stranger cannot tell: which three questions, at the moment of reading. They follow in the
      same sentence, but the count comes first and I stopped to look for an earlier list.
    - My guess: relative to what, by what measure, and against what alternative.
    - Non-blocking.

45. **"Two of those pages carry more than this sheet does. `docs/language-rules.md` gives each rule with its examples... `docs/language-worked-example.md` walks one short document end to end"**
    - Where: `references/human-prose-rules.md`, before the generated block.
    - What a stranger cannot tell: how `docs/language-worked-example.md` is one of "those pages". The
      list above names four artifacts, and that file is not among them. The pointer names a member
      outside the set it points into. I marked this as a class the prompt's list does not carry.
    - My guess: the worked example is a fifth page the list forgot, and "those pages" was meant loosely.
    - Non-blocking. Marked new.

46. **"The case is written text on the left and its repair on the right."**
    - Where: `references/human-prose-rules.md`, the paragraph introducing the entries.
    - What a stranger cannot tell: why several right-hand sides are instructions rather than repairs.
      Under `r05` the right side reads "name the actor that shows a colour, or state what the numbers
      do"; under `r32` it reads "name the judge and the measure". Those are directions to a writer, not
      repaired text, so the file breaks the shape it states. Related stops in the same file: "the rule
      home" (`r61`, `r41`) is used as a defined thing and never defined; "The harness task panel"
      (`r52`) is undefined; and `r53` writes "package rules" where the skill body writes pack.
    - My guess: some cases were recorded as review notes and never rewritten into repairs.
    - Non-blocking.

Blocking entries: 8, 9, 10, 18, 20, 25, 26, 29, 38.
