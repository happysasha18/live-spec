# Cold read of `skills/text-audit/SKILL.md` and its two companion files, 2026-07-29

Read once, straight through: `skills/text-audit/SKILL.md`, then
`skills/text-audit/references/reader-prompt.md`, then
`skills/text-audit/references/human-prose-rules.md`. Nothing else opened.

Stops: 41 — 8 blocking

---

1. **"Part of the live-spec pack."**
   - Where: the blockquote under the title `# text-audit — read a text as a stranger, fix where they stop`.
   - What a stranger cannot tell: what a pack is. A directory of skills? A published plugin? An installable
     bundle? The last section, "The pack this skill belongs to", lists eleven names, but no sentence anywhere
     says what the word means or what holding one gets me.
   - My guess: a bundle of eleven skill files shipped together in one repository.
   - Non-blocking.

2. **"Four scopes settle a setting there: the session's live word first, then the host profile, the personal profile, and the package default."**
   - Where: same blockquote.
   - What a stranger cannot tell: which settings this covers, what a host profile is, what a personal
     profile is, and what "the session's live word" means. Four terms arrive in one sentence and none is
     defined here. I also cannot tell whether any of them affects what I do when I run this audit.
   - My guess: a precedence order for configuration values, defined in `live-spec-base`, and irrelevant to
     someone running the audit by hand.
   - Non-blocking.

3. **"Used on its own, this skill is plain advice a person applies by hand"**
   - Where: same blockquote.
   - What a stranger cannot tell: what the other mode is and what it adds. "The by-hand mode" further down
     covers only the case where no second reader is available, so the split named here is not the split that
     section describes.
   - My guess: "on its own" means without the rest of the pack installed, and the difference is that no other
     skill hands the text over automatically.
   - Non-blocking.

4. **"The loop came from the comprehension gate on spec sections, recorded in `docs/spec-format.md`."**
   - Where: opening of the paragraph "The loop came from the comprehension gate…".
   - What a stranger cannot tell: which loop. The word arrives with a definite article three sections before
     "The loop" section defines it. And the ground for the claim sits in a file I do not hold.
   - My guess: "the loop" is the four-step audit described later, and the file records a gate that predates
     this skill.
   - Non-blocking.

5. **"Those readers found new blocking terms on every pass, and the terms already repaired stayed repaired."**
   - Where: paragraph opening "Those readers found new blocking terms on every pass".
   - What a stranger cannot tell: which readers, how many passes, on what text, and where the record sits.
     This sentence, plus the two after it, is the only evidence offered that the loop works at all — and the
     page later says outright that no record stands behind the build test. So I cannot tell whether this
     claim has a record either.
   - My guess: the readers run during the spec-format comprehension gate, over some unnamed number of passes
     on `PRODUCT_SPEC.md`, with the readings filed under `docs/language-reads/`.
   - Blocking.

6. **"The findings reached zero only after two reads in a row returned nothing that blocks."**
   - Where: same paragraph.
   - What a stranger cannot tell: whether this states a result or restates the closing rule. Read once it
     sounds like an observation; read twice it reads as circular, because "findings reached zero" and "two
     reads returned nothing that blocks" say the same thing. I read it twice.
   - My guess: it reports that the count kept coming back above zero until two consecutive reads came back
     empty.
   - Non-blocking.

7. **"Every reading is written to a dated reading record under `docs/language-reads/`, and `docs/language-defects.md` records what each one returned."**
   - Where: same paragraph.
   - What a stranger cannot tell: who writes the reading record. The cold reader is told to repair nothing and
     to report; the auditor runs lints and writes fixes. Neither role is given this act. I also cannot tell
     whether the reading record *is* the reader's report or a second document made from it, nor what "each
     one" points at — each reading, or each record.
   - My guess: the auditor files the reader's returned report as the reading record, and "each one" means each
     reading.
   - Blocking.

8. **The paragraph running "Those readers found new blocking terms… This skill packages that loop for any text."**
   - Where: the same paragraph, taken whole.
   - What a stranger cannot tell: which point the paragraph is making. It carries five: what past readers
     found, when findings hit zero, where readings are filed, where defects are filed, and what this skill
     does with all of it. The document's own companion rule `r44` says one paragraph carries one point.
   - My guess: the intended point is the first sentence, and the rest is supporting material that should sit
     under it.
   - Non-blocking.

9. **"One person may hold the auditor role and own the text, and the cold reader is never either of them."**
   - Where: "The roles and the words this skill uses", first paragraph.
   - What a stranger cannot tell: how a person holds the auditor role, when the bullet six lines below defines
     the auditor as "the session running this skill". Either the auditor is a person or it is a model session,
     and the two sentences disagree. I also read "never either of them" twice to work out that "them" means
     the auditor role and the text's owner, not two people.
   - My guess: the auditor is whoever or whatever runs the audit — a session in the pack, a person by hand.
   - Non-blocking.

10. **"A surface is a kind of text. One file carries several kinds."**
    - Where: bold paragraph opening "A surface is a kind of text", in "The roles and the words this skill uses".
    - What a stranger cannot tell: why the definition is here twice. Six lines above, the same section already
      says "A **surface** is a kind of text. One file carries several kinds at once", with the spec-versus-prose
      example. The second statement adds only the sentence about naming the primary surface. The companion
      rules state (`r56`) that one fact lives in one home.
    - My guess: an edit left the first statement in place and the second one was written to lead a new paragraph.
    - Non-blocking.

11. **"The auditor names the text's one primary surface, reading it against the surface list in `guardrails/language-rules.json`."**
    - Where: same bold paragraph.
    - What a stranger cannot tell: why I must open that file when the six surfaces are printed on this page
      three lines above it, and what I do when the file is absent. "The mechanical lints" says the audit works
      without the live-spec repository on disk, using grep fallbacks — but this step, which comes before every
      other step, names a file from that repository and offers no fallback. So the first act the skill asks of
      me has no by-hand path.
    - My guess: the printed list of six is enough, and the file is only where the list is edited.
    - Blocking.

12. **"A text published to someone outside the project carries the artifact surface as well. Every rule binding either surface is then in force."**
    - Where: same bold paragraph.
    - What a stranger cannot tell: what the artifact register says. The skill's own description promises it
      "states the register it holds a text to", and only the human-prose register is printed, at
      `references/human-prose-rules.md`. Marketing copy, an article and a release note are named as texts this
      skill runs on, and all three are assigned to the artifact surface — whose rules appear on no page I hold
      and behind no path this document names. I also cannot tell what happens where the two registers disagree:
      the human-prose cap is 25 words, and the artifact cap is never given.
    - My guess: the artifact rules live in `guardrails/language-rules.json` with the rest, and the stricter of
      two caps wins.
    - Blocking.

13. **"The word cap arrives with the register: 25 words for a human-prose sentence, and 35 for a spec-body criterion (rule `r08`)."**
    - Where: paragraph opening "The **register** of a surface is the set of writing rules its text is held to."
    - What a stranger cannot tell: which statement of the cap governs. "The mechanical lints" states the same
      fact in a different shape — "A sentence past the cap for its surface is a hit, and 15 to 25 words is the
      band a human-prose sentence aims at" — and adds a lower bound that this sentence does not carry. Two
      homes, two shapes, one fact.
    - My guess: 25 is the hard cap and 15 is a target with no enforcement.
    - Non-blocking.

14. **"This skill runs on a text standing on any surface a person reads."**
    - Where: paragraph opening "This skill runs on a text standing on any surface a person reads."
    - What a stranger cannot tell: what this adds over "It runs on any text a person will read: a spec section,
      a README, a decision page, marketing copy, an article, a release note", stated two sections earlier with
      the same six examples. The list of examples then appears a third time under "When it fires".
    - My guess: nothing; it is the same fact in a third place.
    - Non-blocking.

15. **"A non-blocking finding waits: it queues for the person's taste call once the blocking ones are gone."**
    - Where: "The loop", step 3.
    - What a stranger cannot tell: what a taste call is. The phrase names some decision the person makes, and
      the document defines neither the term nor who may overrule it. The same fact is then stated again at the
      end of "The cold reader": "The non-blocking ones go to the person as a list, and the person decides which
      of them to spend a rewrite on."
    - My guess: a taste call is the owner's judgment on whether a sharpening is worth the rewrite.
    - Non-blocking.

16. **"The comprehension gate settled on two reads, and `docs/spec-format.md` records that pattern."**
    - Where: "The loop", step 4.
    - What a stranger cannot tell: who settled it, on what evidence, and why two rather than one or three. The
      number is the closing condition of the whole method, and its ground sits in a file the page does not
      summarise.
    - My guess: two consecutive empty reads were the point at which the earlier gate stopped finding new terms.
    - Non-blocking.

17. **"A section-sized run puts one definition and a handful of sentences in front of a reader."**
    - Where: paragraph after "The loop"'s four steps.
    - What a stranger cannot tell: how many sentences a handful is. This matters, because the next sentence
      contrasts it with a whole-page run, and I have to size my own batch. The document's own companion rule
      `r33` carries the case `a few` → `state the exact quantity`, so the page breaks a rule its own reference
      states.
    - My guess: five to fifteen sentences.
    - Non-blocking.

18. **"The plan chose that size and gave two reasons for it (`docs/plans/2026-07-28-top-level-readability.md`)."**
    - Where: "Running it on a spec section", paragraph opening "Ten requirements at a time is the working size".
    - What a stranger cannot tell: which plan, and whether a document can choose anything. "The plan" arrives
      with a definite article and no prior mention, and the actor of "chose" is a file.
    - My guess: a person wrote that plan and chose the size in it.
    - Non-blocking.

19. **"A fresh reader holds that much, and a repair inside those lines cannot break a requirement a hundred lines away."**
    - Where: same paragraph.
    - What a stranger cannot tell: what "holds that much" was measured against, and what makes the second half
      true. Nothing on the page stops a repair from touching a term used a hundred lines away — in fact the
      skill elsewhere says a stop in one place stands for that class everywhere else, which is the opposite.
    - My guess: it means an edit inside a 250-line window is unlikely to alter text outside it, stated as a
      working assumption rather than a proven property.
    - Non-blocking.

20. **"Four things change there, against the human-prose run the sections above describe."**
    - Where: "Running it on a spec section", after the paragraph on batch size.
    - What a stranger cannot tell: which four. Six bold-led paragraphs follow in that section — the
      requirement-shape lint, the criterion-versus-prose split, the machine-read marks, the fix source, the
      build test, and the missing build-test evidence. I counted and had to guess where the four stop.
    - My guess: the first four bold paragraphs are the four, and the last two are separate matter.
    - Non-blocking.

21. **"The code-to-location table is the map a script builds from the body criteria at freeze"**
    - Where: the first of the two bullets under "Every mark a machine reads survives the repair."
    - What a stranger cannot tell: which script, and what "at freeze" means. Freeze is explained four
      paragraphs later, under the frozen baseline; here it arrives cold. The script is never named at all,
      unlike every other check on the page, each of which carries its command.
    - My guess: `guardrails/check-index-generated.py` builds or verifies it, and freeze is the moment
      `scripts/spec-freeze.py` runs.
    - Non-blocking.

22. **"`bash guardrails/check-freeze.sh` — the three guarded documents match the frozen baseline"**
    - Where: the fourth structure check.
    - What a stranger cannot tell: which three documents are guarded. The set is pointed at by its count and
      its members are given nowhere near it; I resolved it two paragraphs later, from the arguments of the
      freeze command.
    - My guess: `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, and `TEST_MATRIX.md`.
    - Non-blocking.

23. **"plus the findings of the style lint and of the register lint"**
    - Where: the census bullet, "Running it on a spec section".
    - What a stranger cannot tell: what those two lints are. Both are named for the first time in "The
      mechanical lints", a section below this one, as `scripts/spec-style-lint.py` and
      `scripts/preshow-register-lint.py`. Here they arrive as defined terms before their definition.
    - My guess: those two scripts.
    - Non-blocking.

24. **"The third is four commands of its own:"**
    - Where: paragraph opening "Four checks run after the section is repaired".
    - What a stranger cannot tell: what the third is, without reading forward into the list and counting. The
      thing is named by its position. The document's own companion rule `r63` names this class.
    - My guess: the structure checks.
    - Non-blocking.

25. **"runs the census comparison over every live document"**
    - Where: paragraph opening "At the push".
    - What a stranger cannot tell: what makes a document live. Every markdown file in the repository? Every
      file with a row in `guardrails/rule-census.json`? The answer decides whether my audited file is in scope
      at push time.
    - My guess: every file recorded in `rule-census.json`.
    - Non-blocking.

26. **"The measure is set out in `docs/plans/2026-07-28-top-level-readability.md`, which takes the count before and after each batch, by two different fresh agents."** against **"No record stands behind any build test."**
    - Where: the bold paragraphs "The build test measures the work once the audit has closed" and "The method's
      build-test evidence is owed", one after the other.
    - What a stranger cannot tell: whether the build test is a step I run or a step nobody has run. The first
      paragraph describes it in the present tense as part of the method, down to who hands what to whom; the
      second says no run of it is recorded and no count exists. I read both twice and still cannot tell whether
      I am being told to run it.
    - My guess: it is a prescribed step that has never been carried out, and I should run it if I can.
    - Blocking.

27. **"Step 4's two clean reads are what close it."**
    - Where: bold paragraph "The build test measures the work once the audit has closed."
    - What a stranger cannot tell: what step 4 is without going back to the list in "The loop". The thing is
      named by its number, which the companion rule `r63` names as a defect.
    - My guess: the second-reading step.
    - Non-blocking.

28. **"A project holding no such file gets one, carrying a `weak_words` list."**
    - Where: the third sub-bullet of "A weak relational word fills the slot it opens."
    - What a stranger cannot tell: who creates the file, where it goes, and in what format. The sentence has no
      actor, and the action sits in "gets".
    - My guess: the auditor writes a `weak-words.json` beside the script it ran, holding a `weak_words` array.
    - Non-blocking.

29. **"A mechanical hit is fixed before the cold reader runs, so no reader spends a finding on a class a machine already owns."** against the five classes in the pasted prompt.
    - Where: the closing line of "The mechanical lints", read against the block inside `references/reader-prompt.md`.
    - What a stranger cannot tell: what the cold reader is supposed to report. The prompt's five stop classes
      are an undefined term, an unfilled relational word, a sentence read twice, an ungrounded claim, and a
      judgment with no judge. Three of those five are exactly what the vocabulary lint, the weak-word lint and
      the requirement-shape lint already own and have already fixed. So either the lints leave residue the
      reader must still catch, or the reader is being asked for classes the sentence above says no reader
      should spend a finding on. The two files instruct in opposite directions.
    - My guess: the lints catch only the mechanically detectable instances, and the reader is expected to
      report the rest — but the page never says that.
    - Blocking. Marked as new: this class is a conflict *between* two files of one set, not a stop inside a
      single document.

30. **"An undefined term the rest of the text leans on blocks."**
    - Where: "The cold reader", paragraph opening "Every finding is marked blocking or non-blocking."
    - What a stranger cannot tell: on a first pass, what "leans on blocks" means. I parsed "leans on blocks"
      as a phrase before working out that "blocks" is the sentence's verb and "the rest of the text leans on"
      is a relative clause. I read it twice.
    - My guess: a term the rest of the text depends on, when left undefined, is a blocking finding.
    - Non-blocking.

31. **"In this pack that means a fresh worker with the pack not loaded, reading the text from outside."**
    - Where: "The cold reader", second paragraph.
    - What a stranger cannot tell: what a worker is, what loading a pack means, and how I verify a pack is not
      loaded. Three terms of this project's own machinery, none defined on the page.
    - My guess: a worker is a subordinate model session, and "not loaded" means its instructions do not include
      these skill files.
    - Non-blocking.

32. **"The non-blocking ones go to the person as a list, and the person decides which of them to spend a rewrite on."**
    - Where: closing paragraph of "The cold reader".
    - What a stranger cannot tell: what this adds over step 3 of "The loop", which already says a non-blocking
      finding queues for the person's call once the blocking ones are gone. One fact, two homes.
    - My guess: nothing new.
    - Non-blocking.

33. **"Paste the block below verbatim into the cold-reader session, under the body's definition of a blocking finding, with the text appended."**
    - Where: `references/reader-prompt.md`, the line above the fenced block.
    - What a stranger cannot tell: which sentence is "the body's definition of a blocking finding", and where
      it goes. The body carries at least three candidates — the one-sentence definition in the paragraph on the
      comprehension gate, the three-sentence account in "The cold reader", and the `r54` reference in the rules
      file. "Under" is also ambiguous: below the block, or below the first line of it, or preceding it as a
      preamble. The whole point of this file is that the block is paste-ready, and the instruction that makes
      it paste-ready cannot be carried out from the page.
    - My guess: paste the two sentences from "The cold reader" beginning "Every finding is marked blocking or
      non-blocking", immediately above the fenced block, then the text.
    - Blocking.

34. **"Judging those classes needs a rulebook the cold reader does not hold. The prompt's last instruction takes every other stop the reader met, so a class outside the five still comes back."**
    - Where: `references/reader-prompt.md`, third paragraph.
    - What a stranger cannot tell: which of two readings holds. Either the reader cannot judge the other
      classes and the catch-all instruction is a partial recovery, or the reader can report them without the
      rulebook and the first sentence is wrong. I read the pair twice.
    - My guess: the reader reports what stopped it without naming a rule code, and the auditor classifies
      afterwards against the rulebook.
    - Non-blocking.

35. **"A new slot-opening word joins the weak-word list, and the skill body's weak-word lint says which copy of that list takes the edit."**
    - Where: `references/reader-prompt.md`, last paragraph.
    - What a stranger cannot tell: what this adds over the body, which already states the same rule twice — once
      as which copy a run reads, once as the auditor adding the word by hand to the file that run just read.
    - My guess: nothing; it is a pointer restating the fact it points at.
    - Non-blocking.

36. **"Two of those pages carry more than this sheet does. `docs/language-rules.md` gives each rule with its examples… `docs/language-worked-example.md` walks one short document end to end."**
    - Where: `references/human-prose-rules.md`, fourth paragraph, read against the four-item list above it.
    - What a stranger cannot tell: how `docs/language-worked-example.md` can be one of "those pages", when the
      list directly above names four artifacts and that file is not among them. The four are
      `docs/language-rules.md`, `docs/language-rule-coverage.md`, `hooks/language-laws.json`, and this block.
      So the claim and the list it points at disagree, and I cannot tell whether the worked example is
      generated from the same source file — which decides whether editing the JSON updates it.
    - My guess: the worked example is written by hand and is not one of the generated four, and "those pages"
      was meant to say "two other pages".
    - Blocking.

37. **"This block prints 48 of the 62 rules the source carries. A code missing from the run below belongs to a rule binding other surfaces only, or to a retired rule whose code left the set."**
    - Where: `references/human-prose-rules.md`, second paragraph of the generated block.
    - What a stranger cannot tell: which of the fourteen missing codes is a retired rule and which binds
      another surface. I counted the printed entries and got 48, so the number holds — but the gaps in the
      sequence (`r16`, `r17`, `r19`, `r21`, `r22`, `r24`, `r28`–`r31`, `r34`–`r38`, `r40`, `r42`, `r47`, `r51`,
      `r55`, `r58`–`r60`) are unresolvable from the page, and the source file is not one I hold.
    - My guess: it does not matter for a human-prose audit, since every rule that binds this surface is printed.
    - Non-blocking.

38. **The 48 rule entries printed as one flat run of peer bullets.**
    - Where: `references/human-prose-rules.md`, under "The rules this audit holds human prose to".
    - What a stranger cannot tell: how to find a rule, or how the rules group. Rule `r45`, printed inside this
      very run, says a long run of peer items is gathered under headed parents. The page breaks the rule it
      prints, at the length of forty-eight items.
    - My guess: the generator emits a flat list and the grouping was never added to the source.
    - Non-blocking.

39. **"A documentation page carries `artifact` as well once it is published outside the project."**
    - Where: `references/human-prose-rules.md`, first paragraph of the generated block.
    - What a stranger cannot tell: whether `artifact` in code font is the same thing the skill body calls "a
      published artifact" in its list of six surfaces. One thing, two names — the class rule `r04`, printed
      four bullets below, names exactly this.
    - My guess: yes, the same surface, written here as its machine identifier.
    - Non-blocking.

40. **"`the door` → `the entry point`"**
    - Where: `references/human-prose-rules.md`, the recorded case under `r02`.
    - What a stranger cannot tell: what "the door" named, so I cannot tell what kind of coinage the class
      catches. The repair gives me the answer word without the thing. Every neighbouring case carries enough
      of its sentence to show the mistake; this one does not.
    - My guess: some component in this project that used to be called the door.
    - Non-blocking.

41. **"`Direct answer: yes, I broke the method... (a paragraph auditing my own failure)`"**
    - Where: `references/human-prose-rules.md`, the recorded case under `r49`.
    - What a stranger cannot tell: who "I" and "my" are, in a file that otherwise never speaks in the first
      person. The case reads as a quotation from a chat message, and nothing marks it as one.
    - My guess: a line from a past session's chat, kept verbatim as the recorded evidence.
    - Non-blocking.

---

Blocking entries: 5, 7, 11, 12, 26, 29, 33, 36.
