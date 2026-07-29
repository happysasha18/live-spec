# Cold read of `skills/text-audit/SKILL.md` and its two reference files — 2026-07-29

Stops: 38 — 5 blocking

Read in one pass: `skills/text-audit/SKILL.md`, then `references/reader-prompt.md`, then
`references/human-prose-rules.md`. Nothing else was opened.

---

## In `SKILL.md`

1. **"Part of the **live-spec pack**"**
   - Where: the block quote under the heading `# text-audit — read a text as a stranger, fix where they stop`.
   - What a stranger cannot tell: what a pack is. The word carries weight through the whole file ("Inside
     the pack", "a fresh worker with the pack not loaded", "The pack this skill belongs to"), and the
     closing section lists eleven members without ever saying what kind of thing they are members of.
   - My guess: a bundle of skills installed together into an agent.
   - Non-blocking.

2. **"Four scopes settle a setting there: the session's live word first, then the host profile, the personal profile, and the package default."**
   - Where: same block quote.
   - What a stranger cannot tell: what a setting is here, which settings this skill has, and what any of
     the four scopes are. The sentence names four things and defines none. A path to
     `skills/live-spec-base/SKILL.md` is given, so the definition is reachable, but nothing on this page
     tells me whether I need it before running an audit.
   - My guess: a precedence order for configuration values, and none of it affects a first run.
   - Non-blocking.

3. **"settle" as a verb, first met in "Four scopes settle a setting there"**
   - Where: same block quote, then recurring — "Run every check a script or a grep settles", "It settles
     which words a text takes", "The comprehension gate settled on two reads".
   - What a stranger cannot tell: which everyday verb this stands for. In "a check a script settles" it
     seems to mean *decides the outcome of*; in "settles which words a text takes" it means *fixes*; in
     "settled on two reads" it means *arrived at*. An ordinary word is carrying a private meaning that
     shifts between sentences.
   - My guess: "decides" in the first two, "arrived at" in the third.
   - Non-blocking. (Marked as an instance of the class the companion file records as `r01`.)

4. **"Used on its own, this skill is plain advice a person applies by hand"**
   - Where: same block quote.
   - What a stranger cannot tell: on its own of *what*, and what "by hand" means at this point in the
     document. Both are explained much later, under "The by-hand mode" on the last third of the page.
   - My guess: used without the rest of the pack installed, a person runs the steps themselves.
   - Non-blocking.

5. **"Those readers found new blocking terms on every pass, and the terms already repaired stayed repaired."**
   - Where: the paragraph opening "Those readers found new blocking terms".
   - What a stranger cannot tell: two things. First, "blocking" is load-bearing here and is defined only
     near the end of the file, under "The cold reader". Second, the claim has no ground on the page —
     how many passes, over what text, how many terms. The document builds its central rule (two clean
     reads) on this observation, and I cannot see what the observation was.
   - My guess: some unrecorded number of readings over `PRODUCT_SPEC.md` sections, where the count of new
     findings fell to zero.
   - Non-blocking.

6. **"Every reading is written to a dated **reading record** under `docs/language-reads/`, and `docs/language-defects.md` records what each one returned."**
   - Where: same paragraph.
   - What a stranger cannot tell: what the second file holds that the first does not. The reading record
     is defined one sentence later as carrying "every stop and any check that did not run" — which is
     already what a reading returned. Two files appear to hold one fact.
   - My guess: the record is the full report, the defects file is a rolled-up index.
   - Non-blocking.

7. **"One person may hold the auditor role and own the text"** against **"the auditor — the session running this skill"**
   - Where: "The roles and the words this skill uses".
   - What a stranger cannot tell: whether the auditor is a person or a software session. The bullet
     defines it as a session; the sentence above it says a person may hold the role. In the by-hand mode
     there is no session at all, so the definition cannot be right there.
   - My guess: the auditor is whoever runs the steps, software or person.
   - Non-blocking.

8. **"**A surface is a kind of text.** One file carries several kinds."**
   - Where: the bolded paragraph opening "A surface is a kind of text", four lines below the bullet list.
   - What a stranger cannot tell: why the definition is given twice. Six lines earlier the same file
     says "A **surface** is a kind of text. One file carries several kinds at once". The second printing
     adds nothing except the sentences that follow it. This is the one-fact-one-home rule the companion
     file prints as `r56`, broken by the document that points at it.
   - My guess: an editing leftover, and the second copy is the live one.
   - Non-blocking.

9. **"The word cap arrives with the register: 25 words for a human-prose sentence, and 35 for a spec-body criterion (rule `r08`)."** — **BLOCKING**
   - Where: the paragraph opening "The **register** of a surface is the set of writing rules".
   - What a stranger cannot tell: which cap applies when. Three statements of the cap sit in this file
     and its companion, and they do not agree. Here it is a flat 25. Under "The mechanical lints" it
     becomes "A sentence past the cap for its surface is a hit, and 15 to 25 words is the band a
     human-prose sentence aims at" — a cap and a target band, with the difference between them unstated.
     Then the census, which runs on a *spec* batch, is said to count "sentences past the human-prose word
     cap" — the wrong cap for the surface being audited, if 35 is really the spec-body number. The
     companion's `r08` prints no number at all, and `r06`'s recorded case gives "between 15 and 25 words,
     and one past 25 is a hit".
   - My guess: 25 is the human-prose cap, 15 is a soft floor, 35 is the spec-body cap, and the census
     sentence is wrong. I cannot check any of that from the page, and a census failure decides whether a
     batch must run again.
   - Blocking.

10. **"It holds that text to the register of the text's own primary surface."**
    - Where: the paragraph opening "This skill runs on a text standing on any surface a person reads".
    - What a stranger cannot tell: what a register is. The word is used here and in the sentence before
      it, and defined two paragraphs later. The file lists "every term is defined at its first use" as one
      of four rules binding every sentence of itself, so the rule is stated and then broken.
    - My guess: the set of writing rules for that surface — which the later definition confirms.
    - Non-blocking.

11. **"The five lints under "The mechanical lints" are that whole set."**
    - Where: step 1 of "The loop".
    - What a stranger cannot tell: whether the count is right, without scrolling past two other sections
      to the list. When I got there I counted five bullets — but the fourth bullet, "Style and register",
      names two scripts and is later referred to as two separate things ("the findings of the style lint
      and of the register lint"). So the set is five or six depending on which sentence I trust.
    - My guess: five bullets, six scripts.
    - Non-blocking.

12. **"it queues for the person's taste call once the blocking ones are gone"**
    - Where: step 3 of "The loop".
    - What a stranger cannot tell: what a taste call is, and where the queue is. Neither is defined here
      or anywhere on the page. "Taste and voice stay with the person" appears earlier under work that
      belongs elsewhere, which hints but does not define.
    - My guess: the person reads the non-blocking list and picks which ones to fix.
    - Non-blocking.

13. **"A section-sized run puts one definition and a handful of sentences in front of a reader."**
    - Where: the paragraph after step 4.
    - What a stranger cannot tell: how many sentences. "A handful" is exactly the empty slot the
      companion file records under `r33`, whose repair reads "state the exact quantity". The document
      breaks the rule it ships. The next sentence adds "puts every sentence of that page in front of
      one" — one *what*, only recoverable from the sentence before.
    - My guess: five to ten sentences, and "one" means one reader.
    - Non-blocking.

14. **"Run `python3 guardrails/check-requirement-shape.py FILE` beside the other lints."**
    - Where: "**The requirement-shape lint applies here.**" under "Running it on a spec section".
    - What a stranger cannot tell: what the other lints are. They are listed in the section *after* this
      one. Reading straight through, I am told to run something beside a set I have not met.
    - My guess: the five listed later, which turned out to include this same script again as its own
      bullet — so the lint is stated twice.
    - Non-blocking.

15. **"plus the findings of the style lint and of the register lint"**
    - Where: the census bullet under "Running it on a spec section".
    - What a stranger cannot tell: which two checks these are. Both are named only in the later section
      as `scripts/spec-style-lint.py` and `scripts/preshow-register-lint.py`.
    - My guess: those two scripts.
    - Non-blocking.

16. **"a repair inside those lines cannot break a requirement a hundred lines away"**
    - Where: the paragraph opening "Ten requirements at a time is the working size".
    - What a stranger cannot tell: why not. Nothing on the page says requirements are independent across
      that distance — and the file elsewhere warns that a rewrite moving a bracket anchor "breaks a test,
      or one of the two maps". Those two claims pull against each other. "A hundred lines" is also a
      number with nothing behind it.
    - My guess: the claim means a *textual* repair stays local, while anchors are the exception already
      called out.
    - Non-blocking.

17. **"The third is four commands of its own"**
    - Where: the lead-in to the four post-repair checks.
    - What a stranger cannot tell: which check that is, without counting bullets that have not appeared
      yet. The sentence names a thing by its position and makes me leave it to find out what it is.
    - My guess: the structure checks — confirmed by counting.
    - Non-blocking.

18. **"the three guarded documents match the frozen baseline"**
    - Where: the `check-freeze.sh` line in the structure-check list.
    - What a stranger cannot tell: which three documents. They appear about fifteen lines later inside a
      command line, as `PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md`. A set is pointed at by its count
      with its members withheld.
    - My guess: those three, since they are the only three the file ever guards together.
    - Non-blocking.

19. **"the frozen baseline"**
    - Where: same line, then defined in the paragraph opening "The frozen baseline is the recorded map".
    - What a stranger cannot tell: what it is at the point I first meet it. Same for "at freeze" in the
      code-to-location table bullet a few lines above.
    - My guess: a saved snapshot of the document's structural marks.
    - Non-blocking.

20. **"runs the census comparison over every live document"**
    - Where: the paragraph opening "At the push".
    - What a stranger cannot tell: what makes a document live. Nothing on the page distinguishes a live
      document from any other, so I cannot tell what this gate covers or whether my audited file is in it.
    - My guess: every document listed in `guardrails/rule-census.json`.
    - Non-blocking.

21. **"The build test measures the work once the audit has closed."** against **"So this skill states no build count."** — **BLOCKING**
    - Where: the two bolded paragraphs closing "Running it on a spec section".
    - What a stranger cannot tell: whether the build test is a step I am supposed to run. The first
      paragraph is written as instructions — hand the requirements to a fresh agent, ask it to implement
      them, count how many it builds without asking. The second paragraph says no such run has ever been
      recorded and the loop's only evidence is the cold readings. I cannot tell whether I am reading a
      required step, an optional measure, or an unproven proposal. The heading "The method's build-test
      evidence is owed" also promises evidence over a body that says there is none, and "is owed" leaves
      out who owes it to whom.
    - My guess: optional, and skipped in practice.
    - Blocking.

22. **"which takes the count before and after each batch, by two different fresh agents"**
    - Where: the same build-test paragraph, describing `docs/plans/2026-07-28-top-level-readability.md`.
    - What a stranger cannot tell: who takes the count. A plan document is the subject of an act only a
      person or a script can perform, and the sentence's real actor is missing.
    - My guess: whoever runs the batch takes the count, following what that plan lays out.
    - Non-blocking.

23. **"Nothing names the requirements one ran on, the agent that read them, or what it produced"**
    - Where: "**The method's build-test evidence is owed.**"
    - What a stranger cannot tell: what "one" points at. It has to mean "one build test", but the noun is
      three sentences back. The companion file's `r25` records exactly this substitution, with the repair
      "one → you".
    - My guess: "the requirements a given build test ran on".
    - Non-blocking.

24. **"a fresh worker with the pack not loaded"**
    - Where: "The cold reader".
    - What a stranger cannot tell: whether a worker is the same thing as the "fresh session" the file
      defines at the top, or the "fresh agent" the build test hands requirements to, or the "reader
      session" of step 2. Four words for what looks like one thing, and the companion prints "one thing
      carries one name in every sentence" as `r04`.
    - My guess: all four name one thing — a new conversation with a model.
    - Non-blocking.

25. **"a writer or reader holding the project's rules is kept apart from one who does not"**
    - Where: "The cold reader", quoting `docs/spec-style.md`.
    - What a stranger cannot tell: what the trailing "does not" completes — the verb it needs ("hold") was
      inflected as "holding" and cannot be carried over. I read the clause twice. Who does the keeping is
      also unnamed.
    - My guess: "one who does not hold them", and the separation is enforced by whoever briefs the reader.
    - Non-blocking.

26. **"A passing run prints one line saying that the file is clean."**
    - Where: "This skill is held to the rules it lists".
    - What a stranger cannot tell: what clean means here — zero findings, or findings at or under a
      recorded number. The census two sections earlier passes a count that is at the record rather than
      at zero, so the two notions of passing differ. "Clean" is a judgment word with no measure beside it.
    - My guess: zero findings from that one script.
    - Non-blocking.

27. **"Four of those rules bind every sentence of this file"** — **BLOCKING**
    - Where: "This skill is held to the rules it lists", directly after "This skill obeys the human-prose
      register printed in `references/human-prose-rules.md`".
    - What a stranger cannot tell: whether four rules bind this file or forty-eight. The sentence before
      says the skill obeys the whole register; the companion file states that its block prints 48 rules
      binding human prose. Then four are singled out as binding "every sentence", which implies the other
      forty-four bind something less than every sentence — and nothing says what. An editor changing this
      file cannot tell what to check.
    - My guess: all 48 bind it, and the four are the ones most often broken.
    - Blocking.

28. **"`guardrails/rule-census.json` records this file at zero findings, and `python3 guardrails/check-doc-findings-bound.py` refuses a push that raises that count."**
    - Where: "This skill is held to the rules it lists".
    - What a stranger cannot tell: why this is here twice. The same gate and the same behaviour are
      already stated under "Running it on a spec section": "At the push, `python3
      guardrails/check-doc-findings-bound.py` runs the census comparison over every live document, and a
      document recorded at zero fails on its first finding."
    - My guess: one of the two is the home and the other should point at it.
    - Non-blocking.

29. **"The same editor runs one cold-reader loop over the changed section before the skill ships."**
    - Where: the last line of "This skill is held to the rules it lists".
    - What a stranger cannot tell: what "one loop" means when the loop is defined as running until two
      consecutive reads come back with nothing blocking. One loop could be one read, or the whole
      repeat-until-clean cycle.
    - My guess: the whole cycle, ending on two clean reads.
    - Non-blocking.

## In `references/reader-prompt.md`

30. **"The prompt's last instruction takes every other stop the reader met"**
    - Where: the paragraph opening "The prompt names five stop classes".
    - What a stranger cannot tell: which instruction that is. Inside the pasted block, the closing
      instruction ("Return the entries as a numbered list. If you stopped nowhere, say so in one line.")
      is followed by a further paragraph, so the sentence that catches unlisted stops is not the last
      thing a reader of the block meets. Naming it by position sent me hunting.
    - My guess: the final paragraph, "A word the list above does not name, that still stopped you, is a
      real find".
    - Non-blocking.

31. **"A new slot-opening word joins the weak-word list"**
    - Where: the closing paragraph of the file.
    - What a stranger cannot tell: what a slot-opening word is, reading this file on its own. The term is
      defined only in `SKILL.md`, in the weak-relational-word lint. This file does link to `../SKILL.md`
      at its top, but not at this sentence, and the companion's `r67` asks that a file read alone reach
      its terms' definitions.
    - My guess: a relational word that opens an empty slot, per the skill body's lint.
    - Non-blocking.

## In `references/human-prose-rules.md`

32. **"Two of those pages carry more than this sheet does."**
    - Where: the paragraph following the four-artifact list.
    - What a stranger cannot tell: which two. The sentence points back at a list of four artifacts, then
      names `docs/language-rules.md` — which is on that list — and `docs/language-worked-example.md`,
      which is not. So "those pages" covers a page the list never carried. The claim and the list beneath
      it disagree.
    - My guess: the worked example is a fifth file, built by something else or written by hand.
    - Non-blocking.

33. **"the rule text the judging model reads, `hooks/language-laws.json`"**
    - Where: the four-artifact list.
    - What a stranger cannot tell: what the judging model is. It appears once, judges something unnamed,
      and never returns. Nothing in the three files I read says a model judges anything.
    - My guess: a model behind a hook that checks text against these rules automatically.
    - Non-blocking.

34. **"The case is written text on the left and its repair on the right."** — **BLOCKING**
    - Where: the paragraph opening "Each entry names the class of mistake".
    - What a stranger cannot tell: how to read the right-hand side, because it holds two different kinds
      of thing. Under `r01` the right side is a repaired sentence. Under `r05` it is `name the actor that
      shows a colour, or state what the numbers do` — an instruction to a writer, not a repair. The same
      happens at `r08`, `r10`, `r13`, `r15`, `r32`, `r33`, `r49`, `r70` and `r71`. Roughly a fifth of the
      cases break the format the block states one paragraph above them. A reader who came for a model to
      copy cannot use those entries, and the stated rule about the format cannot be trusted.
    - My guess: the instruction-shaped entries are unfinished, and a real repaired sentence was intended.
    - Blocking.

35. **"`the door` → `the entry point`"**
    - Where: the recorded case under `r02`.
    - What a stranger cannot tell: what "the door" was the name of, or what sentence either phrase stood
      in. Two bare noun phrases with no surrounding text leave the class unillustrated for anyone who
      does not already know the project.
    - My guess: a coined project name for whatever component receives incoming work.
    - Non-blocking.

36. **"`a 62-word sentence inside the file that states the 25-word cap` → `the same rule in three sentences, the longest of them 41 words`"**
    - Where: the recorded case under `r09`, the rule against a text breaking a rule it states.
    - What a stranger cannot tell: how a 41-word sentence is a repair when the cap named in the same case
      is 25. The example teaches the reader to break the rule the entry exists to enforce. If a different
      cap applies to that file, the case does not say so.
    - My guess: the repair is partial, or the file it came from is a spec body with a 35-word cap — which
      41 still exceeds.
    - Non-blocking.

37. **"A finding blocks when the reader could not go on, or would have applied the text wrongly."** — **BLOCKING**
    - Where: rule `r54` in the printed block.
    - What a stranger cannot tell: which definition of blocking to use. `SKILL.md` says a finding blocks
      "when the reader cannot act on the text, or cannot trust it, until the answer arrives", and the
      pasted reader-prompt repeats that wording. This rule gives a different test: could not go on, or
      would have applied the text wrongly. "Cannot trust it" and "would have applied it wrongly" are not
      the same test, and every finding I mark rides on which one I apply. The loop's close condition —
      two reads with zero blocking findings — is decided by this word.
    - My guess: the two are meant as one test, and the `SKILL.md` wording is the live one because the
      reader-prompt agrees with it.
    - Blocking.

38. **"A long run of peer items is gathered under headed parents."**
    - Where: rule `r45`.
    - What a stranger cannot tell: how the rule squares with the page printing it. The block runs 48 peer
      bullets at one level under a single heading, with no grouping over them, which is the longest flat
      run in any of the three files. The rule is stated and broken where it stands.
    - My guess: generated blocks are exempt, though nothing says so.
    - Non-blocking.

---

Blocking entries: 9, 21, 27, 34, 37.
