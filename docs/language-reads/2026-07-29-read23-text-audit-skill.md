# Cold read of `skills/text-audit/SKILL.md` and its two reference files — 2026-07-29

Read straight through, once: `skills/text-audit/SKILL.md`, then
`skills/text-audit/references/reader-prompt.md`, then
`skills/text-audit/references/human-prose-rules.md`. Nothing else opened.

Stops: 33 — 7 blocking

---

## SKILL.md

1. **"Four scopes settle a setting there: the session's live word first, then the host profile, the personal profile, and the package default."**
   - Where: the blockquote under the heading `# text-audit — read a text as a stranger, fix where they stop`.
   - What a stranger cannot tell: what a "setting" is in this skill (nothing in this file is ever called a setting), what "the session's live word" means, and where a host profile or a personal profile lives.
   - My guess: settings are configuration values like language and cadence, and "the session's live word" means an instruction the person typed during this conversation.
   - Non-blocking. The file names `skills/live-spec-base/SKILL.md` as the home.

2. **"The loop came from the comprehension gate on spec sections, recorded in `docs/spec-format.md`."**
   - Where: paragraph opening "The loop came from the comprehension gate…".
   - What a stranger cannot tell: "the loop" arrives here with no definition; the section that defines it, "The loop", sits about eighty lines further down. On first pass I did not know whether "the loop" was this skill's procedure or something inside the comprehension gate.
   - My guess: "the loop" is this skill's four-step audit procedure.
   - Non-blocking.

3. **"Those readers found new blocking terms on every pass, and the terms already repaired stayed repaired."**
   - Where: paragraph opening "Those readers found new blocking terms…".
   - What a stranger cannot tell: what "blocking" means. The word is used here, then again in "The audit runs in four steps. It closes when two consecutive cold reads return zero blocking findings", and it is only defined much later, under "The cold reader": "A finding blocks when the reader cannot act on the text, or cannot trust it, until the answer arrives." Everything the loop's closing condition depends on rests on a word the reader does not yet hold.
   - My guess: blocking means severe enough to stop the reader.
   - **Blocking.**

4. **"Those readers found new blocking terms on every pass"**
   - Where: same paragraph.
   - What a stranger cannot tell: how many passes, over what text, judged by whom. The claim is the whole evidence offered for the method, and its ground sits off the page. The later paragraph "The method's build-test evidence is owed" makes a point of saying no record stands behind the build test, which made me distrust this unrecorded claim too.
   - My guess: a handful of readings over `PRODUCT_SPEC.md` sections in July 2026.
   - Non-blocking.

5. **"Every reading is written to a dated **reading record** under `docs/language-reads/`, and `docs/language-defects.md` records what each one returned."**
   - Where: same paragraph.
   - What a stranger cannot tell: what each file holds that the other does not. A reading record "carries every stop", and the defects file "records what each one returned" — those read as the same fact living in two places.
   - My guess: the reading record holds the full entries, and the defects file holds a one-line summary per reading.
   - Non-blocking.

6. **"One rule settles the surface a text stands on. The auditor names the text's one primary surface, reading it against the surface list in `guardrails/language-rules.json`. … That rule stands in the same file, in the note over the surface list."**
   - Where: heading "The roles and the words this skill uses", paragraph opening "**One rule settles the surface a text stands on.**".
   - What a stranger cannot tell: what the rule actually says. The rule that decides which surface a text stands on is named, pointed at, and never stated. A reader working from this page alone cannot pick a surface, and picking a surface decides the whole register the audit applies.
   - My guess: the primary surface is the one the text's own genre matches, and the paragraph two below ("A README, a report, a decision page, and a skill body stand on human prose…") is standing in for that rule.
   - **Blocking.**

7. **"The word cap arrives with the register: 25 words for a human-prose sentence, and 35 for a spec-body criterion (rule `r08`)."** and **"A sentence past the cap for its surface is a hit, and 15 to 25 words is the band a human-prose sentence aims at."**
   - Where: the first under "The roles and the words this skill uses"; the second under "The mechanical lints", in the "Style and register" bullet.
   - What a stranger cannot tell: whether the number to hold is a cap of 25 or a band of 15 to 25, and why the fact is stated in two places at all. The second statement adds a lower bound that the first never mentions.
   - My guess: 25 is the hard cap and 15 to 25 is the aim, so a 12-word sentence passes the lint.
   - Non-blocking.

8. **"The two passes read different failures on the same page, so run each for its own."**
   - Where: "Work that belongs elsewhere", first bullet.
   - What a stranger cannot tell: what "its own" stands for. The sentence trails off into an empty slot — run each for its own *what*.
   - My guess: run each pass for the class of failure only that pass finds.
   - Non-blocking.

9. **"A section-sized run puts one definition and a handful of sentences in front of a reader."**
   - Where: "The loop", the paragraph after the four numbered steps.
   - What a stranger cannot tell: how many sentences "a handful" is. This file's own companion prints rule `r33` with the recorded case `a few` → `state the exact quantity`, so the text uses the shape its rulebook forbids.
   - My guess: three to ten sentences.
   - Non-blocking.

10. **"A short run of such requirements is also a section."**
    - Where: "Running it on a spec section", first paragraph.
    - What a stranger cannot tell: how short a short run is. The very next paragraph says ten requirements is the working size, which left me unsure whether ten is short or already too long for a "section".
    - My guess: two or three requirements.
    - Non-blocking.

11. **"a repair inside those lines cannot break a requirement a hundred lines away"**
    - Where: "Running it on a spec section", paragraph opening "Ten requirements at a time is the working size".
    - What a stranger cannot tell: where a hundred comes from, and what it is measured against. The paragraph has just said a batch is about 250 lines, so a hundred lines is inside the batch, which contradicts the sentence's own point.
    - My guess: the sentence means a requirement outside the batch, and "a hundred lines" is a loose stand-in for "outside these 250 lines".
    - Non-blocking.

12. **"A rule binds a whole region of the file, so those two rules never both judge one sentence."**
    - Where: paragraph opening "**A criterion and the prose around it take different rules.**".
    - What a stranger cannot tell: what a region is, where one starts and ends, and how a lint or a person decides which region a given sentence sits in. The paragraph asserts the two rules never collide, and gives the reader no way to check that.
    - My guess: a region is a labelled block such as "Context" or "Acceptance criteria", recognised by its heading.
    - **Blocking.**

13. **"the map a script builds from the body criteria at freeze"**
    - Where: the bullet defining "the **code-to-location table**".
    - What a stranger cannot tell: what "freeze" is as a moment. "The frozen baseline" is defined four paragraphs later as a recorded map, but the event of freezing, who triggers it, and when, are never stated.
    - My guess: freeze is the moment `scripts/spec-freeze.py --freeze` is run, before a push.
    - Non-blocking.

14. **"whose rows pair one architecture node with one spec fact"**
    - Where: the bullet defining "the **test matrix**".
    - What a stranger cannot tell: what an architecture node is. No architecture document is described anywhere in this file, though `ARCHITECTURE.md` appears later inside a command line.
    - My guess: a component or module named in `ARCHITECTURE.md`.
    - Non-blocking.

15. **"Four checks run after the section is repaired, and each one reports what it read. The third is four commands of its own:"**
    - Where: paragraph opening "Four checks run after the section is repaired".
    - What a stranger cannot tell: which check "the third" is, before reading ahead into the list to count. The document's own companion prints rule `r63` against naming a thing by its position. I had to read the list, count to three, and come back.
    - My guess: the structure checks.
    - Non-blocking.

16. **"Run the audited project's own suite command, whatever it is"**
    - Where: the first bullet of the four post-repair checks.
    - What a stranger cannot tell: how to find that command. This is one of two checks the document says run anywhere, and it is the check that catches a dropped phrase, so a reader who cannot find the command cannot run the required verification. The companion's rule `r69` names exactly this class: a step naming a check with no way to run it.
    - My guess: look for a `test` script in the project's build file, or ask the person.
    - **Blocking.**

17. **"a second reader who puts the old text and the new text side by side and reports every difference in meaning"**
    - Where: the second bullet of the four post-repair checks.
    - What a stranger cannot tell: who this reader is and what prompt it works under. The cold reader gets a whole reference file of its own; this second reader gets one clause. I could not tell whether it must also hold zero context, or whether the auditor may play it.
    - My guess: another fresh session, briefed ad hoc by the auditor.
    - **Blocking.**

18. **"`python3 scripts/spec-freeze.py --freeze PRODUCT_SPEC.md ARCHITECTURE.md TEST_MATRIX.md --compaction`"**
    - Where: paragraph opening "The frozen baseline is the recorded map".
    - What a stranger cannot tell: what `--compaction` does or why it is there. Every other element of the command is explained in the sentences around it.
    - My guess: it records a compacted form of the map.
    - Non-blocking.

19. **"runs the census comparison over every live document"**
    - Where: paragraph opening "At the push".
    - What a stranger cannot tell: what makes a document live, and therefore which documents the push gate measures.
    - My guess: every document with a row in `guardrails/rule-census.json`.
    - Non-blocking.

20. **"**The method's build-test evidence is owed.**"**
    - Where: the bolded lead of the last paragraph under "Running it on a spec section".
    - What a stranger cannot tell: owed to whom, and by whom. The sentence names no actor and buries its action in a noun. I read it twice before working out that it means no build test has ever been recorded.
    - My guess: it means the evidence is missing and someone still has to produce it.
    - Non-blocking.

21. **"**Every term is defined at first use.** Every domain noun the text uses carries a one-sentence definition, and the reader meets it before the noun's first working use."**
    - Where: "The mechanical lints", first bullet. Also restated under "This skill is held to the rules it lists" as "every term is defined at its first use".
    - What a stranger cannot tell: how this squares with rule `r01` in the companion sheet, which says a project term "holds one glossary entry, written in plain words. The body then uses that term unchanged, with no definition attached." One file tells the writer to define at first use, the other tells the writer to define once in a glossary and never again in the body. Reading both, I could not tell which to apply, and the skill claims to obey the second.
    - My guess: the glossary rule governs a spec body, and the define-at-first-use rule governs a standalone document that carries no glossary.
    - **Blocking.**

22. **"Which copy of that list a run reads: the `weak-words.json` sitting beside the `check-weak-words.py` that ran."**
    - Where: the weak-relational-word bullet under "The mechanical lints".
    - What a stranger cannot tell: this is a heading and an answer glued into one line with a colon, with no verb joining them. I read it twice to parse.
    - My guess: it means the run reads the copy of the list that sits in the same directory as the script.
    - Non-blocking.

23. **"A project holding no such file gets one, carrying a `weak_words` list."**
    - Where: the same bullet.
    - What a stranger cannot tell: who creates the file, where in the project it goes, and what shape it takes beyond holding a `weak_words` key. The sentence has no actor.
    - My guess: the auditor creates it, at the project root.
    - Non-blocking.

24. **"`python3 scripts/preshow-register-lint.py FILE`"**
    - Where: the "Style and register" bullet.
    - What a stranger cannot tell: what "preshow" means. It reads as a coined prefix, and nothing on the page unpacks it.
    - My guess: it runs before work is shown to a person.
    - Non-blocking.

25. **"no adjective grades a result's size"**
    - Where: the same bullet.
    - What a stranger cannot tell: what "a result's size" covers. The grep fallback lists *big*, *huge*, *minor*, *breakthrough* — but *breakthrough* is not a size, so the class name and its examples do not agree.
    - My guess: the class is really "an adjective grading how big or how important a result is".
    - Non-blocking.

26. **"In this pack that means a fresh worker with the pack not loaded"**
    - Where: "The cold reader", paragraph opening "The reader holds **zero context on the text's history**".
    - What a stranger cannot tell: whether "a fresh worker" is the same thing as "a fresh session" (used at the top of the file), "a fresh cold reader" (step 2), and "a fresh agent" (the build test). Four names appear where one thing seems to stand, and the companion's rule `r04` forbids exactly that.
    - My guess: they are all one thing — a new conversation with a model, started empty.
    - Non-blocking.

27. **"Four of those rules bind every sentence of this file:"**
    - Where: "This skill is held to the rules it lists".
    - What a stranger cannot tell: whether the other rules in the printed register bind this file too. The sentence before says the skill obeys the whole human-prose register; the companion prints 48 rules; then four are singled out as binding *every* sentence, which implies the rest bind only some.
    - My guess: all 48 apply, and these four are being highlighted rather than narrowed.
    - Non-blocking.

28. **"It queues for the person's taste call once the blocking ones are gone."**
    - Where: "The loop", step 3.
    - What a stranger cannot tell: what a "taste call" is. It reads as project shorthand where "decision" would carry the meaning.
    - My guess: the person decides which non-blocking findings are worth a rewrite.
    - Non-blocking.

29. **"Run `python3 guardrails/check-requirement-shape.py FILE` beside the other lints."**
    - Where: paragraph opening "**The requirement-shape lint applies here.**", and again as the first of the four structure checks, and again as the third bullet under "The mechanical lints".
    - What a stranger cannot tell: whether this is one check run once, or the same script run at three different moments. Its three descriptions carry the same three points ("Context comes before criteria. Each criterion carries one trigger and one response. Every judgment names a judge and a measure.") word for word in two of the three places.
    - My guess: one script, run once at step 1 and once again after repairs.
    - Non-blocking.

## references/reader-prompt.md

30. **"A new slot-opening word joins the weak-word list, and the skill body's weak-word lint says which copy of that list takes the edit."**
    - Where: the closing paragraph, after the pasteable block.
    - What a stranger cannot tell: what "slot-opening" means, if this file is read on its own. The term is built in `SKILL.md` ("Words such as *depends*… open a slot"), and this file's opening does point at `../SKILL.md`, but the pointer is general and does not name where the term is defined.
    - My guess: a word that opens an unfilled comparison slot, such as *faster* or *sufficient*.
    - Non-blocking.

31. **"a judgment word — broken, worth, better, enough, important — with no stated judge or measure"**
    - Where: inside the pasteable prompt block.
    - What a stranger cannot tell: where this list comes from. `SKILL.md` ships a scripted list for relational words (`guardrails/weak-words.json`) and describes how a new one is added; the judgment words get a hard-coded list in the prompt with no home and no path for growth, though the closing paragraph promises new words join "the weak-word list".
    - My guess: judgment words are meant to join `weak-words.json` too, and the file does not say so.
    - Non-blocking. **New class** — a growth path stated for one list and silently missing for its sibling.

## references/human-prose-rules.md

32. **"Two of those pages carry more than this sheet does. `docs/language-rules.md` gives each rule with its examples, its exceptions, and its thresholds. `docs/language-worked-example.md` walks one short document end to end…"**
    - Where: the paragraph after the four-artifact list.
    - What a stranger cannot tell: "those pages" points back at the list of four artifacts, and `docs/language-worked-example.md` is not in that list. So one of the "two of those pages" is not one of those pages. I reread the list to check.
    - My guess: the worked example is a fifth document, generated or not, and the sentence should not have claimed it as a member.
    - Non-blocking.

33. **"The case is written text on the left and its repair on the right."**
    - Where: the paragraph opening "Each entry names the class of mistake".
    - What a stranger cannot tell: why several entries put an instruction on the right instead of a repair. `r05` gives `→ name the actor that shows a colour, or state what the numbers do`; `r08` gives `→ state the law in one short sentence, and put its parts in a list`; `r10`, `r13`, `r32`, `r33` and `r49` do the same. The sheet states a rule about its own shape and then breaks it in seven of its 48 entries, and rule `r09` in that same sheet is "a text breaking a rule it states". For those seven I cannot see what the repaired sentence looks like, which is the one thing the case was there to show.
    - My guess: those seven classes were recorded before the left/right shape was fixed, and nobody swept them.
    - **Blocking.**

---

Blocking entries: 3, 6, 12, 16, 17, 21, 33.
