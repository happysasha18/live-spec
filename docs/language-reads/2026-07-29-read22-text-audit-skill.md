# Cold read of `skills/text-audit/SKILL.md` (with `references/reader-prompt.md` and `references/human-prose-rules.md`) — 2026-07-29

Stops: 46 — 4 blocking

1. **"Part of the **live-spec pack**"** — opening block quote, above "This skill checks whether a stranger understands a text".
   A stranger cannot tell what a pack is: a folder of skills, an installable package, a team, or a naming convention. The line names a base skill and a file path, but never says what the container itself is or how one "uses" it.
   Guess: a set of skill files installed together, so that "inside the pack" means the other files are loaded and reachable.
   Non-blocking.

2. **"Four scopes settle a setting there: the session's live word first, then the host profile, the personal profile, and the package default."** — opening block quote.
   Four names arrive at once, none of them explained: what a "setting" is here, what a "session's live word" is, what a host profile is against a personal profile. A stranger also cannot tell which settings of *this* skill those scopes decide — the register? the word cap? the number of clean reads?
   Guess: a precedence order for configuration values, and none of it changes how I run the audit today.
   Non-blocking.

3. **"Used on its own, this skill is plain advice a person applies by hand"** — opening block quote.
   The document splits everything into "inside the pack" and "on its own" and hangs real instructions on that split (which reader you get, whether scripts exist, whether the audit closes). It never states what puts me on one side or the other. Is it whether the live-spec repository sits on my disk, or whether other skill files are loaded, or both?
   Guess: "on its own" means I have this file but not the repository's scripts, so I run grep fallbacks.
   Non-blocking.

4. **"a decision page"** — "It runs on any text a person will read: a spec section, a README, a decision page, marketing copy, an article, a release note."
   A decision page is named three times in this file (here, in "When it fires", and in the surface list) and never defined. A stranger cannot tell whether it is a page asking a person to choose something, a record of a decision already made, or a template.
   Guess: a page written to get a decision out of a person, listing options.
   Non-blocking.

5. **"Those readers found new blocking terms on every pass, and the terms already repaired stayed repaired. The findings reached zero only after two reads in a row returned nothing that blocks."** — "The loop came from the comprehension gate on spec sections".
   These two sentences fight. If every pass found new blocking terms, no pass returns zero, and the loop never closes. A stranger cannot tell whether "on every pass" means every pass up to the last two, or a general law about fresh readers. The ground for either reading sits in `docs/spec-format.md` and `docs/language-reads/`, which are not on this page.
   Guess: early passes each found new terms, and the last two found none.
   Non-blocking.

6. **"Three roles run through this skill, and one person often holds more than one of them."** — "The roles and the words this skill uses".
   This says roles combine freely. Three paragraphs earlier the file says "An author cannot be their own cold reader." A stranger cannot tell which pairings are allowed and which are forbidden: may the person be the auditor? may the auditor be the cold reader? The by-hand mode makes this decision live, because there a single person is trying to hold as many roles as the rules permit.
   Guess: the person and the auditor may be one human; the cold reader must be somebody else. Acting on the sentence as written, a lone author would read their own text and count the audit as run.
   **Blocking.**

7. **"the auditor — the session running this skill"** — "The roles and the words this skill uses".
   The auditor is defined as a session, meaning a conversation with a model. The file also describes a by-hand mode where a person applies the skill with no model at all. A stranger cannot tell who the auditor is in that mode, or whether the by-hand mode simply has no auditor.
   Guess: by hand, the person doing the work is the auditor, and "session" is shorthand for the usual case.
   Non-blocking.

8. **"A text declares one primary surface: the kind of text it is written to be."** — "One rule settles the surface a text stands on".
   Nobody declares it. A stranger cannot tell whether the declaration is a line in the file, a field somewhere, or a judgment the auditor makes. Worse, the six named surfaces are a spec body, human prose, chat, a published artifact, a commit message, and a worker brief — and the skill says it runs on marketing copy, an article, and a release note, none of which is obviously any of the six. Human prose is later defined as text a person reads to understand or to decide something, which marketing copy is not. Without a surface I cannot pick a register, and the register decides every rule the audit applies.
   Guess: the auditor picks the closest surface by hand, and marketing copy is treated as human prose plus artifact.
   **Blocking.**

9. **"Every rule binding either surface is then in force."** — "One rule settles the surface a text stands on".
   Two registers can disagree — a word cap, an address to the reader, an allowed shape. A stranger cannot tell what happens when the human-prose rule and the artifact rule pull opposite ways, or whether the union is ever contradictory.
   Guess: the registers never conflict, so the union is safe.
   Non-blocking.

10. **"The word cap arrives with the register: 25 words for a human-prose sentence, and 35 for a spec-body criterion (rule `r08`)."** — "The roles and the words this skill uses".
    The mechanical-lints section states the same fact again, differently: "A sentence past the cap for its surface is a hit, and 15 to 25 words is the band a human-prose sentence aims at." One place gives a cap, the other gives a band with a floor. A stranger cannot tell whether a 12-word sentence is a hit.
    Guess: 25 is the hard cap and 15 is advice, so a 12-word sentence passes the lint.
    Non-blocking.

11. **"the six surfaces, the three words above, and every rule of every register are edited"** — "The roles and the words this skill uses", last line.
    "The three words above" points at a set without naming its members. A stranger has to go back and count bolded terms, and lands on surface, register, class — while cold reader, auditor, person, and batch are bolded too.
    Guess: surface, register, and class.
    Non-blocking.

12. **"Each fresh reader catches a class the reader before it did not reach, so a single clean read can still hide a blocking class."** — "The loop", step 4.
    Stated as a general law, this says every new reader finds something the last one missed — which means two consecutive clean reads cannot happen, and the closing condition in the same step is unreachable. A stranger cannot tell whether this is a claim about all readers or an observation about the early passes, and the sentence is the one that tells me when to stop working.
    Guess: readers differ in what they catch, so two reads are safer than one, and the loop does close in practice.
    **Blocking.**

13. **"A section-sized run puts one definition and a handful of sentences in front of a reader."** — "The loop", closing paragraph.
    "A handful" leaves the quantity open, in a file whose own rule list repairs "a few" into an exact quantity. A stranger sizing a run cannot tell whether that is five sentences or thirty.
    Guess: roughly a paragraph or two, under twenty sentences.
    Non-blocking.

14. **"a repair inside those lines cannot break a requirement a hundred lines away"** — "Running it on a spec section", the batch paragraph.
    Nothing on the page supports this. A renamed term or a dropped definition inside a batch plainly can break a requirement elsewhere in the same file. The number 100 also arrives with no relation to the 250 lines just given: relative to what, and why is 100 the safe distance?
    Guess: a claim about locality that holds for most edits, with the 250-line batch as the real bound.
    Non-blocking.

15. **"Four things change there, against the human-prose run the sections above describe."** — "Running it on a spec section".
    Six bolded statements follow under this heading: the requirement-shape lint, criterion-versus-prose rules, machine-read marks, fixes from neighbours, the build test, and the build-test evidence. A stranger counting cannot tell whether the last two are outside the four on purpose, or whether the count is stale.
    Guess: the four are the first four bolded items, and the two build-test paragraphs are extra material about measurement.
    Non-blocking.

16. **"It reads three things nobody would ask of a README. Context comes before criteria. Each criterion carries one trigger and one response. Every judgment names a judge and a measure."** — "Running it on a spec section", the requirement-shape paragraph.
    The mechanical-lints section states the same three things again in the same words: "Context comes before criteria, each criterion carries one trigger and one response, and every judgment names a judge and a measure." A stranger cannot tell which of the two is the home, and whether one is meant to carry a detail the other lacks.
    Guess: the same lint, written out twice, with no difference intended.
    Non-blocking.

17. **"A rule binds a whole region of the file, so those two rules never both judge one sentence."** — "Running it on a spec section", the criterion-versus-prose paragraph.
    I read this twice. "Region" is not defined, and the causal step does not follow on its own: binding a region prevents overlap only if the regions never intersect and every sentence sits in exactly one. A stranger cannot tell where a region starts and stops — is a Context paragraph a region, or the whole requirement?
    Guess: criteria form one region and the surrounding prose another, and the two do not overlap.
    Non-blocking.

18. **"the map a script builds from the body criteria at freeze"** — "Running it on a spec section", the code-to-location table bullet.
    "Freeze" is used here and defined about thirty lines later, under the frozen baseline. The script is also unnamed: a stranger looking for what builds this map finds only `check-index-generated.py`, which checks it.
    Guess: freeze is the moment `scripts/spec-freeze.py --freeze` runs, and some other script builds the table then.
    Non-blocking.

19. **"whose rows pair one architecture node with one spec fact and pin the test level that covers it"** — "Running it on a spec section", the test matrix bullet.
    "Architecture node", "spec fact", and "test level" all arrive undefined, with no path to a definition. A stranger cannot tell what levels exist or who pins them.
    Guess: nodes are components in an architecture document, and levels are a ladder like unit, DOM, browser, pixel.
    Non-blocking.

20. **"The architecture document, the recorded decision, and the test matrix hold the answers this text rests on."** — "Running it on a spec section", the fix-from-neighbours paragraph.
    "The recorded decision" is definite, as though one known record exists, but no file, folder, or format is named. A stranger repairing a spec sentence cannot find it.
    Guess: a decision log somewhere in the repository, perhaps under `docs/`.
    Non-blocking.

21. **"Run the audited project's own suite command, whatever it is"** — "Running it on a spec section", the four checks list.
    The step tells me to run a command it cannot name, and it never says what to do when the project has no suite. Every other check on the list carries its exact command.
    Guess: skip the check and note that it did not run, by analogy with the paragraph about absent scripts.
    Non-blocking.

22. **"It counts findings per file: sentences past the human-prose word cap, plus the findings of the style lint and of the register lint."** — "Running it on a spec section", the census bullet.
    This check is prescribed for a spec batch, yet it counts against the *human-prose* cap, while the file earlier gives a spec-body criterion a 35-word cap. A stranger cannot tell which cap the census applies to a spec file, or whether a legal 30-word criterion counts as a finding.
    Guess: the census applies one cap to every file regardless of surface, and the script decides.
    Non-blocking.

23. **"run the first two checks, and record that the other two did not run"** — "Running it on a spec section", after the four checks.
    The record has no name, no path, and no shape. The by-hand section repeats the instruction — "Say so in the record, rather than counting the text as read" — with the same gap. A reader who wants to obey cannot, because there is no place to write.
    Guess: the dated file under `docs/language-reads/` that the origin paragraph mentions, though that is described as the reading itself, not a run log.
    **Blocking.**

24. **"`--compaction`"** — "Running it on a spec section", the frozen-baseline paragraph.
    The flag appears inside a command a reader is expected to paste, with no statement of what it does or whether it is optional. A stranger cannot tell whether omitting it produces a different baseline that then fails `check-freeze.sh`.
    Guess: it stores a compact form of the map, and it is required for the check to match.
    Non-blocking.

25. **"runs the census comparison over every live document"** — "At the push".
    "Live document" is new here. A stranger cannot tell which documents are live: every markdown file, only those listed in `rule-census.json`, or only the three guarded ones.
    Guess: every file that has a recorded count in `guardrails/rule-census.json`.
    Non-blocking.

26. **"Hand the repaired requirements to a fresh agent that holds no other context."** — "The build test measures the work once the audit has closed".
    One kind of thing is called a fresh session, a fresh worker, a fresh agent, a fresh reader, and a cold reader across this file. The skill's own "One name per thing" lint forbids exactly this, so the file breaks a rule it states. A stranger cannot tell whether an agent differs from a session, or whether the build test needs a different sort of reader than the audit does.
    Guess: all five phrases name the same thing — a model conversation started empty.
    Non-blocking.

27. **"The method's build-test evidence is owed."** — heading line of that paragraph.
    "Owed" names no debtor and no creditor, and the heading promises evidence while the body says none exists. A stranger cannot tell whether the build test is a step to run or a plan not yet carried out, since the paragraph above it gives instructions for running one.
    Guess: the authors intend to record build tests, have not yet, and the step is optional until they do.
    Non-blocking.

28. **"the reader meets it before the noun's first working use"** — "The mechanical lints", first bullet.
    The rule is stated once as "defined at first use" in the bullet heading and once as "first working use" in the body. A stranger cannot tell what makes a use working, or which uses do not count — a mention in a heading, a use inside an example, a use in a quoted command.
    Guess: the first place the noun carries meaning in a sentence, ignoring headings and titles.
    Non-blocking.

29. **"list the nouns written with an initial capital and the nouns this project coined"** — "The mechanical lints", vocabulary grep fallback.
    The fallback exists for a reader who does not have the repository, and it asks that reader to know which nouns the project coined. A stranger has no way to tell a coined noun from an ordinary one without the project's own vocabulary.
    Guess: treat any noun I could not define from general knowledge as coined.
    Non-blocking.

30. **"Which copy of that list a run reads: the `weak-words.json` sitting beside the `check-weak-words.py` that ran."** — "The mechanical lints", weak-words bullet.
    The sentence opens as a question and finishes as an answer, with a colon holding the two together and no verb governing the whole. I read it twice to see that it was not a heading.
    Guess: it means the run reads the copy sitting beside the script that ran.
    Non-blocking.

31. **"A project holding no such file gets one, carrying a `weak_words` list."** — "The mechanical lints", weak-words bullet.
    No actor creates the file, and no path or filename is given for the new one. A stranger cannot tell where to put it so the script or the `WEAK_WORDS` variable will find it.
    Guess: the auditor creates it, named `weak-words.json`, beside the script or pointed at by `WEAK_WORDS`.
    Non-blocking.

32. **"A mechanical hit is fixed before the cold reader runs, so no reader spends a finding on a class a machine already owns."** — closing line of "The mechanical lints".
    Step 1 of the loop already states this twice: "Fix each hit at this step" and "The cold reader then spends its attention on what no script can judge". This is the third statement of one fact.
    Guess: emphasis, not a new rule.
    Non-blocking.

33. **"a fresh worker with the pack not loaded, reading the text from outside"** — "The cold reader".
    A stranger cannot tell how a pack gets loaded or unloaded, so cannot tell how to produce a worker in this state, or how to verify one is in it.
    Guess: start a conversation in a directory or configuration where the skill files are not read.
    Non-blocking.

34. **"A finding blocks when the reader cannot act on the text, or cannot trust it, until the answer arrives."** — "The cold reader".
    The same definition, in nearly the same words, sits inside the pasteable prompt at `references/reader-prompt.md`. A stranger editing one has no way to know the other exists, and the file's own rule list says one fact lives in one home.
    Guess: the prompt is a copy that must be kept in step by hand.
    Non-blocking.

35. **"A README, an article, or a piece of copy takes a bracketed query in the draft."** — "Where a fix comes from".
    The spec form is given exactly, as `[GAP: what is missing]`. The prose form is described only as "a bracketed query", with no shape, marker word, or example. A stranger cannot write one that a later reader or script would recognize.
    Guess: square brackets with a question inside, in whatever wording suits.
    Non-blocking.

36. **"Four of those rules bind every sentence of this file"** — "This skill is held to the rules it lists".
    The sentence before it says the skill obeys the whole human-prose register, which the reference sheet prints as 48 rules. A stranger cannot tell what the other 44 bind, if not every sentence, or why four of them were singled out.
    Guess: all 48 bind the file, and the four are the ones the author thought most at risk.
    Non-blocking.

37. **"The same editor runs one cold-reader loop over the changed section before the skill ships."** — "This skill is held to the rules it lists".
    A loop is defined as closing on two consecutive clean reads, so "one loop" could mean the whole loop to closure, or a single pass. A stranger cannot tell whether one clean read is enough to ship a change to this file, which would contradict step 4.
    Guess: the full loop, to two clean reads.
    Non-blocking.

38. **"The prompt names five stop classes a stranger judges from the page alone. The rules at [`human-prose-rules.md`] name every other class an audit holds a text to."** — `references/reader-prompt.md`, opening.
    "Every other class" says the two sets do not overlap, but the prompt's relational-word class and judgment-word class are the register's `r33` and `r32`, and the undefined-term class is `r01`/`r67`. A stranger also cannot tell who catches the 40-odd register classes that neither the five lints nor the five prompt classes cover, while the loop closes on the reader alone stopping nowhere.
    Guess: the sets overlap, and the register lint plus the census are meant to cover the remainder.
    Non-blocking.

39. **"A new slot-opening word joins the weak-word list, and the skill body's weak-word lint says which copy of that list takes the edit."** — `references/reader-prompt.md`, closing lines.
    The skill body already states this, at more length, in its weak-words bullet. The same fact now stands in two files.
    Guess: the reference file repeats it so a person holding only the prompt still knows.
    Non-blocking.

40. **"Two of those pages carry more than this sheet does. `docs/language-rules.md` gives each rule with its examples... `docs/language-worked-example.md` walks one short document end to end"** — `references/human-prose-rules.md`, opening.
    "Those pages" points back at the four artifacts just listed, and `docs/language-worked-example.md` is not among them. A stranger cannot tell whether the list of four is incomplete or the phrase means something looser.
    Guess: the worked example is a fifth document, generated or not, and the list of four is about the generator's outputs only.
    Non-blocking.

41. **"A documentation page carries `artifact` as well once it is published outside the project."** — `references/human-prose-rules.md`, generated block, first paragraph.
    The skill body calls this surface "a published artifact"; here it is a bare code-formatted token, `artifact`. A stranger cannot tell whether they are the same surface or two things.
    Guess: one surface, written as its raw key in the rules file.
    Non-blocking.

42. **"Every case the class was built from lives in the rule home."** — `references/human-prose-rules.md`, generated block.
    "The rule home" is used as a defined term and defined nowhere on the page or in the skill body. A stranger cannot tell whether it means `guardrails/language-rules.json`, `docs/language-rules.md`, or a per-rule section somewhere.
    Guess: `guardrails/language-rules.json`, since the paragraph above says that is where each rule is edited.
    Non-blocking.

43. **"The case is written text on the left and its repair on the right."** — `references/human-prose-rules.md`, generated block.
    Many cases put an instruction on the right rather than a repair: `the numbers do not show red` → `name the actor that shows a colour`; `a few` → `state the exact quantity`; `broken` → `name the judge and the measure`. The sheet states a shape and then breaks it in its own entries, so a stranger cannot tell what a repaired sentence for those classes actually looks like.
    Guess: the right-hand side is sometimes a repair and sometimes a note about how to repair.
    Non-blocking.

44. **"`the door` → `the entry point`"** — `references/human-prose-rules.md`, rule `r02`.
    The case shows a substitution with no sentence around it. A stranger cannot tell what "the door" named in the original text, so cannot tell whether "entry point" is the standard word for the same thing or a different concept.
    Guess: a coined name for whatever starts a process, replaced by the ordinary term.
    Non-blocking.

45. **"`X, not Y` → `Say what the thing IS in its own sentence`"** — `references/human-prose-rules.md`, rule `r10`.
    "IS" stands in capitals for emphasis, which rule `r23` on the same page forbids: "Every word is written in ordinary case." A stranger reading the sheet as the authority cannot tell whether the rule has an exception for its own repair text.
    Guess: an oversight, and the capitals are not licensed.
    Non-blocking.

46. **"A long run of peer items is gathered under headed parents."** — `references/human-prose-rules.md`, rule `r45`.
    The block that states this rule is itself a run of 48 peer bullets at one level, under a single heading, with no grouping over them. The page breaks the rule it prints, and a stranger cannot tell whether generated blocks are exempt.
    Guess: the generator is exempt, and the rule is meant for hand-written documents.
    Non-blocking.

Blocking entries: 6, 8, 12, 23.
