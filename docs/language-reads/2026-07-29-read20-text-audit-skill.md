# Cold read of `skills/text-audit/SKILL.md` — 2026-07-29

Stops: 59 — 8 blocking

I read the file once, straight through, from its first line to its last. It is 547 lines and I held it
in one reading, so its length is not itself a stop.

---

1. **"Part of the **live-spec pack**."**
   - Where: the blockquote under the title.
   - Cannot tell: what a "pack" is, what belongs to it, and what changes for me because this file is part
     of one. The list at the end names eleven skills, but that list arrives 530 lines later.
   - Guess: a bundle of related skill files shipped together.
   - Non-blocking.

2. **"Four scopes settle a setting there: the session's live word first, then the host profile, the personal profile, and the package default."**
   - Where: the blockquote under the title.
   - Cannot tell: which settings this governs, what "the session's live word" is, what a "host profile" is
     as against a "personal profile", or where any of the four live. Nothing in this file uses a setting
     resolved this way, so I cannot tell why the sentence is here.
   - Guess: a precedence order for configuration, inherited from a file I do not have.
   - Non-blocking.

3. **"Used on its own, this skill is plain advice a person applies by hand."**
   - Where: the blockquote under the title.
   - Cannot tell: what it is when it is *not* used on its own. The sentence names the fallback and leaves
     the main case unstated, so I do not know whether anything in this file runs automatically.
   - Guess: inside the pack something enforces these steps; alone, nothing does.
   - Non-blocking.

4. **"A **cold reader** is a fresh session that reads the text with no knowledge of its history."**
   - Where: "This skill checks whether a stranger understands a text".
   - Cannot tell: what a "session" is. The word carries the definition of the file's central term and is
     never defined itself. Later text says "a fresh worker", "a fresh agent", and "a new fresh reader" for
     what looks like the same thing.
   - Guess: one conversation with a language model, started empty.
   - Non-blocking.

5. **"This skill supplies the stranger."**
   - Where: "A **cold reader** is a fresh session".
   - Cannot tell: how. At this point nothing has said whether the file supplies a prompt, a script, a
     person, or a procedure. The mechanism arrives 200 lines later.
   - Guess: it gives you a prompt to paste into a new session.
   - Non-blocking.

6. **"the comprehension gate on spec sections, recorded in `docs/spec-format.md`"**
   - Where: "The loop came from the comprehension gate on spec sections".
   - Cannot tell: what a "comprehension gate" is, and where `docs/spec-format.md` lives. This is the
     first of roughly thirty paths in the file, and no repository is named until line 175. Reading from
     outside, I cannot open it, and the whole method's origin sits behind it.
   - Guess: a rule in some other document of the same project requiring a section to be understood before
     it ships; the path is relative to a repository I would have to be told about.
   - **Blocking.**

7. **"That gate has a changed section pass two layers before it ships"**
   - Where: "The loop came from the comprehension gate".
   - Cannot tell: I read this twice to find the verb. "has ... pass" is a causative, but "a changed
     section pass two layers" reads at first as a noun phrase. Also, "layers" appears once and never
     again; step 1 and step 2 call them steps.
   - Guess: the gate requires a changed section to go through two stages.
   - Non-blocking.

8. **"Those readers found new blocking terms on every pass, and the terms already repaired stayed repaired."**
   - Where: "The loop came from the comprehension gate".
   - Cannot tell: how many readers, over how many passes, on what text, and who observed it. This is the
     only evidence offered for the whole method — that repeated cold reads keep paying and that repairs
     hold. The page states it and points at no record I can reach.
   - Guess: an internal run on this project's spec, recorded somewhere I cannot see.
   - **Blocking.**

9. **"the mechanical lints first, then fresh cold readers"**
   - Where: "The loop came from the comprehension gate".
   - Cannot tell: what a "mechanical lint" is. The term does its work here, in step 1, and in the roles
     section, and is only explained under "The mechanical lints" at line 171. The file's own first rule is
     that every term is defined before its first working use.
   - Guess: automated checks a script performs.
   - Non-blocking.

10. **"This project names six surfaces"**
    - Where: "A **surface** is a kind of text".
    - Cannot tell: which project. I am reading one file; "this project" could be live-spec, or the project
      whose text I am auditing. The distinction matters later, where the file tells me to edit "that
      project's own" configuration.
    - Guess: live-spec, the repository this skill ships from.
    - Non-blocking.

11. **"A text stands on one surface by what it is for, and a text published outside the project stands on the artifact surface as well."**
    - Where: "A **surface** is a kind of text, and one file carries several kinds at once."
    - Cannot tell: whether a text stands on one surface or on more than one. The paragraph's first sentence
      says one file carries several kinds at once; the second says a text stands on one surface; the same
      sentence then adds a second surface with "as well". Three claims, and I cannot pick the rule. Since
      the surface settles which rules bind the text, I cannot tell which rules bind mine.
    - Guess: a text has one primary surface and picks up the artifact rules in addition when it is
      published.
    - **Blocking.**

12. **"stands on the artifact surface as well"**
    - Where: "A **surface** is a kind of text".
    - Cannot tell: whether "the artifact surface" is the same thing as "a published artifact", the name in
      the six-item list one sentence earlier. Two names, one thing, in adjacent sentences.
    - Guess: same thing.
    - Non-blocking.

13. **"This skill audits human prose, the surface a README, a report, a decision page, and a skill body stand on."**
    - Where: "A **surface** is a kind of text".
    - Cannot tell: I read this twice. The appositive runs four subjects before its verb, so on first pass
      "the surface a README" read as one noun phrase.
    - Guess: human prose is the surface those four kinds of text stand on.
    - Non-blocking.

14. **"`guardrails/language-rules.json` is where the six surfaces, these words, and every rule below are edited."**
    - Where: "A **class** is the shape of a mistake".
    - Cannot tell: which tree that path sits in, and who does the editing. The sentence hides its actor in
      a passive, which is the class rule `r26` names later in this same file.
    - Guess: whoever maintains the pack edits it in the live-spec repository.
    - Non-blocking.

15. **"Load it when a human-facing text is about to ship and its clarity matters"**
    - Where: "When it fires".
    - Cannot tell: what "load" means as an act I perform, and who does it. Nowhere does the file say how a
      skill is loaded, or by whom. The heading says "When it fires", which suggests the skill loads itself.
    - Guess: an agent reads this file into its context when the trigger phrases appear.
    - Non-blocking.

16. **"**A design review of a spec** belongs to product-prover."**
    - Where: "Work that belongs elsewhere".
    - Cannot tell: what product-prover is or where to find it. The final list gives it one line —
      "reviews it" — 470 lines later, with no path.
    - Guess: a sibling skill file in the same pack directory.
    - Non-blocking.

17. **"**Taste and voice** stay with the person and with the marketing skills."**
    - Where: "Work that belongs elsewhere".
    - Cannot tell: which marketing skills. No such skill appears in the pack list at the end of the file,
      so the set has no members anywhere on the page.
    - Guess: skills outside this pack, in whatever host the pack is installed into.
    - Non-blocking.

18. **"Run every check a script or a grep settles"**
    - Where: step 1 of "The loop".
    - Cannot tell: what "settles" means here. The file uses the word four ways — a scope settles a setting,
      a register settles which words a text takes, a script settles a check, the gate settled on two reads.
      An ordinary word is carrying a private meaning, which is the class `r01` names later.
    - Guess: "decides mechanically", so a check whose verdict a machine can reach unaided.
    - Non-blocking.

19. **"A script catches the classes a pattern can settle. Three of them are an undefined term, a known weak word, and a sentence that names a thing by denying its neighbour."**
    - Where: step 1 of "The loop".
    - Cannot tell: how many classes there are in total, since "three of them" says the set is larger and
      never gives it. The lints section lists five lints, not three or four. Also, "known weak word" —
      known to whom, and against what list, at this point on the page.
    - Guess: the five lints below are the full set, and these three are examples.
    - Non-blocking.

20. **"For a blocking finding, take the fix from the material the text already rests on."**
    - Where: step 3 of "The loop".
    - Cannot tell: what happens to a non-blocking finding at this step. The loop never says. The answer —
      that they queue for a taste call — sits 130 lines later, in the cold-reader section.
    - Guess: they are left alone until the blocking ones are gone.
    - Non-blocking.

21. **"The comprehension gate settled on two reads, and `docs/spec-format.md` records that pattern."**
    - Where: step 4 of "The loop".
    - Cannot tell: whether this adds anything to the intro's paragraph, which already said the gate came
      from `docs/spec-format.md` and that findings reached zero after two clean reads. The same fact, with
      the same source, stated in a second place.
    - Guess: it is a restatement.
    - Non-blocking.

22. **"Per changed section the loop is cheap."**
    - Where: "Per changed section the loop is cheap."
    - Cannot tell: cheap by what measure, judged by whom, and against what alternative. Two fresh reader
      sessions per section is the only cost the page describes, and it is never priced in time, money, or
      tokens.
    - Guess: cheap in wall-clock time, compared with auditing the whole document.
    - Non-blocking.

23. **"Ten requirements at a time is the working size, which runs to about 250 lines. A fresh reader holds that much"**
    - Where: "Running it on a spec section".
    - Cannot tell: where ten comes from, what "runs to about 250 lines" is measured against, and on what
      ground a fresh reader is said to hold that much and not more. The file's own rule `r06` requires a
      number to say what it is compared against.
    - Guess: an observed working figure from this project, not a derived limit.
    - Non-blocking.

24. **"A spec section stands on the spec-body surface, and four things change there."**
    - Where: "Running it on a spec section".
    - Cannot tell: change relative to what. The four bold paragraphs read as differences from the human-prose
      case, but the sentence never names the baseline.
    - Guess: relative to auditing human prose, the default this file describes.
    - Non-blocking.

25. **"It reads three things a README never owes."**
    - Where: "**The requirement-shape lint applies here.**"
    - Cannot tell: what it means for a document to "owe" something. The verb recurs — "A spec section owes
      the requirements genre", "what the publication owes its reader" — and is never defined.
    - Guess: obligations the genre places on the text.
    - Non-blocking.

26. **"A rule binds a block, so the two never judge one sentence."**
    - Where: "**A criterion and the prose around it take different rules.**"
    - Cannot tell: I read this twice. "the two" points back at two rules or at two kinds of text — the
      paragraph names a criterion and a Context paragraph, and also names two rules. "binds a block" is
      unexplained: what a block is, and what binding does.
    - Guess: each rule applies to a whole region of the document, so the criterion rule and the prose rule
      never both apply to the same sentence.
    - Non-blocking.

27. **"A requirement's number and its bracket anchors stay exactly as they were."**
    - Where: "**Every mark a machine reads survives the repair.**"
    - Cannot tell: what a "bracket anchor" is, what the "code-to-location table" is, or what "the test
      matrix" is. This is a preservation instruction I am supposed to obey while rewriting, and I cannot
      obey it without knowing which marks it names. The consequence stated — that a rewrite breaks a test
      — makes the gap costly.
    - Guess: short codes in square brackets at the ends of lines, like the `[INV-241]` shown much later in
      a rule case.
    - **Blocking.**

28. **"Four checks run after the section is repaired, and each one prints what it read"**
    - Where: "Four checks run after the section is repaired".
    - Cannot tell: whether there are four checks or seven. The list has four bullets, but its third bullet
      is "the four structure checks" holding four commands of its own. I counted twice.
    - Guess: four groups, seven commands.
    - Non-blocking.

29. **"the three guarded documents match the frozen baseline"**
    - Where: the `check-freeze.sh` bullet.
    - Cannot tell: which three documents, at the point of reading. The freeze command two paragraphs later
      names three filenames, and I inferred the set from there.
    - Guess: PRODUCT_SPEC.md, ARCHITECTURE.md, TEST_MATRIX.md.
    - Non-blocking.

30. **"the census, `python3 scripts/rule-census.py`, whose count for the file is read against the count recorded for it in `guardrails/rule-census.json`"**
    - Where: the last bullet of the four checks.
    - Cannot tell: what the census counts. "A count at the record or below it passes. A count above the
      record fails" tells me how the comparison goes and never tells me what is being counted — findings,
      rule breaches, hits per rule, or something else. This is a gate I must pass to ship, and I cannot tell
      what it measures or how to lower it. The same mechanism reappears twice more (at the push, and for
      this skill's own file at zero) without ever saying.
    - Guess: the number of rule breaches the linters find in that file.
    - **Blocking.**

31. **"A count above the record fails, and the batch runs again."**
    - Where: the census bullet.
    - Cannot tell: what "the batch" names. The word arrives here with no introduction, and returns twice in
      the build-test paragraph.
    - Guess: the group of requirements being audited in this pass — the ten named earlier.
    - Non-blocking.

32. **"a tree carrying no baseline there skips the check"**
    - Where: "The frozen baseline is the recorded map".
    - Cannot tell: what "a tree" is here (a directory tree, a git working tree, a repository?), and whether
      the skip is announced or silent. A check that disappears when a file is absent is worth knowing about.
    - Guess: a checkout without a `.spec-freeze/` directory passes the check silently.
    - Non-blocking.

33. **"a document recorded at zero fails on its first finding"**
    - Where: "At the push".
    - Cannot tell: I read this twice. "recorded at zero" and "its first finding" both lean on the census
      semantics that stop 30 leaves open.
    - Guess: a document whose recorded count is 0 fails the push as soon as any lint reports anything on it.
    - Non-blocking.

34. **"The measure of the work is a build test."**
    - Where: "The measure of the work is a build test."
    - Cannot tell: how this stands against "The loop ends when two consecutive reads return zero blocking
      findings" in step 4. Two different closing conditions are stated for the same work, and the page never
      says which one governs, or whether the build test is a gate at all. It also says "the count to reach
      is every requirement in the batch", which reads as a requirement, while the recorded run reached two
      out of six and shipped.
    - Guess: the two clean reads close the loop, and the build test is an outcome measure taken alongside it.
    - **Blocking.**

35. **"On 2026-07-27 six requirements went to a fresh agent, and it built two of them"**
    - Where: "The measure of the work is a build test."
    - Cannot tell: whether to believe it. The bracketed note directly underneath says no record names which
      six requirements, which agent read them, or what it produced. The page states its one piece of
      outcome evidence and then withdraws its ground in the next paragraph, so I cannot tell what the
      two-of-six figure is worth or whether the method it supports works.
    - Guess: the figure comes from a plan document's own assertion and has no run behind it that I can check.
    - **Blocking.**

36. **"[Open question: no record names which six requirements that run used ...]"**
    - Where: after the build-test paragraph.
    - Cannot tell: it is called an open question and is written as three statements with no question mark,
      no owner, and no date by which it closes. I cannot tell who is meant to answer it, or what I do with
      it while it stands.
    - Guess: a note to the file's own maintainer, left in the shipped text.
    - Non-blocking.

37. **"The scripts live in the live-spec repository, whose public home is `github.com/happysasha18/live-spec`."**
    - Where: "The mechanical lints".
    - Cannot tell: why this arrives here. Roughly a dozen paths appear before it — `docs/spec-format.md`,
      `guardrails/language-rules.json`, four structure checks, the census, the freeze — and I had already
      guessed at their home twice. Also, this sentence covers `guardrails/` and `scripts/` only, while the
      file also cites `docs/…` paths.
    - Guess: every path in the file is relative to that repository's root.
    - Non-blocking.

38. **"Grep fallback: list the capitalized and the coined nouns"**
    - Where: "**Every term is defined at first use.**"
    - Cannot tell: how I recognize a coined noun in a project I do not know. That is exactly the judgment a
      stranger cannot make, and the fallback exists for the case where I have no script to make it for me.
    - Guess: any noun that looks like a term of art and that I cannot find in a dictionary.
    - Non-blocking.

39. **"A human-prose sentence runs to 25 words at most, and one past 25 is a hit. A sentence shorter than 15 words passes, and 15 to 25 words is the band to aim at. Rule `r08` sets the cap by surface: 35 words for a spec-body criterion, and 25 for human prose."**
    - Where: "**Style and register.**"
    - Cannot tell: why the same cap is stated three times in three sentences, and which one is the home of
      the fact. `r08` is named by its code, so I have to leave the sentence to learn what the rule is — and
      when I reach `r08` in the printed block, it states no numbers at all, so this passage is the only home
      of the caps after all.
    - Guess: the caps live here, and the `r08` reference is decoration.
    - Non-blocking.

40. **"no adjective grades a result's size. ... The last one shows up as *big*, *huge*, *minor*, or *breakthrough*."**
    - Where: "**Style and register.**"
    - Cannot tell: whether the rule is about adjectives or about a wider class, since "breakthrough" is a
      noun and does not grade size. The rule and its example disagree.
    - Guess: the class is any word inflating how large or how important a result is, whatever its part of
      speech.
    - Non-blocking.

41. **"**One name per thing.** No artifact appears under two names."**
    - Where: the last mechanical lint.
    - Cannot tell: what "artifact" means in this sentence. Earlier the file makes "a published artifact" one
      of the six surfaces, so the word already carries a defined project meaning. Here it seems to mean any
      named thing at all.
    - Guess: here it means any named thing — a file, a script, a concept — not the surface.
    - Non-blocking.

42. **"reading the text from outside (`docs/spec-style.md`, the clean-agent split)"**
    - Where: "The cold reader".
    - Cannot tell: what "the clean-agent split" is. It appears once, in a parenthesis, with no definition and
      only a path to carry it.
    - Guess: a rule elsewhere that separates a writer or reader holding the project's rules from one who
      does not.
    - Non-blocking.

43. **"The rules at the end of this file name more classes, and most of them need a rulebook the cold reader does not hold."**
    - Where: "### The reader-prompt — ready to paste".
    - Cannot tell: how many "most of them" is, and which ones a cold reader *can* judge beyond the five in
      the prompt. Since the point is which classes survive into the prompt, the unmeasured word sits on the
      decision.
    - Guess: the great majority; the prompt's five are the exceptions.
    - Non-blocking.

44. **"a judgment word — broken, worth, better, enough, larger-than — with no stated judge or measure"**
    - Where: inside the pasted reader-prompt.
    - Cannot tell: what "larger-than" is as a word I look for in a text — nobody writes it with the hyphen —
      and why "larger" appears here when it is already in the relational-word list four lines above. One
      word, two classes, and I cannot tell which entry to file a hit under.
    - Guess: a typo for "larger than", duplicated from the relational list.
    - Non-blocking.

45. **"At every relational word, ask the three questions and write which one is unanswered: relative to what? by what measure? or else what alternatives?"**
    - Where: inside the pasted reader-prompt.
    - Cannot tell: "the three questions" names a set by its count and gives it in the same sentence, so I
      read forward to resolve it. And the third question differs from rule `r33`'s own wording later in the
      file, which asks "or else what alternative?" — I cannot tell whether one alternative or several is
      meant.
    - Guess: same question, worded loosely twice.
    - Non-blocking.

46. **"Where the live-spec repository stands on disk, the auditor edits the copy there. In any other project, the auditor edits that project's own `guardrails/weak-words.json`"**
    - Where: "That last instruction keeps the reader catching words".
    - Cannot tell: which copy to edit when both conditions hold — the live-spec repository is on disk *and*
      I am auditing another project's text. That is the ordinary case the lints section describes at line
      176, where I run live-spec's scripts over a text belonging to any project. Two sentences give two
      different destinations for the same edit, and the newly caught word ends up in only one of them.
    - Guess: the first sentence wins, so the live-spec copy takes the edit whenever it is present.
    - **Blocking.**

47. **"## Fixes come from the source, never from invention"**
    - Where: the section heading.
    - Cannot tell: the file states a rule twice — "No sentence names a thing by denying its neighbour" in
      the lints, and "no sentence names a thing by denying its neighbour" among the four rules it says it
      obeys — and this heading names its subject by denying the neighbouring thing. Rule `r10` printed
      below repeats it. I could not tell whether the rule has exceptions I was not told about.
    - Guess: headings are exempt, or the breach was not noticed.
    - Non-blocking.

48. **"An invented definition reads clean to the next reader, while the text now states something no source backs."**
    - Where: "Inventing an answer to close a finding is the one move this skill forbids."
    - Cannot tell: I read this twice. The two halves sit in different times — a general present and a "now"
      — joined by "while", which reads first as simultaneity and then as contrast.
    - Guess: the invention hides the hole from the next reader while leaving the text unsupported.
    - Non-blocking.

49. **"A passing run prints one line, naming no coined metaphor, no loan translation, and no transliterated pack term."**
    - Where: "This skill is held to the rules it lists".
    - Cannot tell: what a "loan translation" or a "transliterated pack term" is, and what the one line
      actually says. The sentence describes the output by three things it does not contain.
    - Guess: the linter prints a pass line, and those three are the classes it checks.
    - Non-blocking.

50. **"Whoever changes this skill runs that lint again. The same editor runs one cold-reader loop over the changed section before the skill ships."**
    - Where: "This skill is held to the rules it lists".
    - Cannot tell: which lint "that lint" points at — the paragraph above names `preshow-register-lint.py`
      and also `check-doc-findings-bound.py`. And nothing says what enforces this on someone who skips it.
    - Guess: the register lint, and the enforcement is the push-time census check.
    - Non-blocking.

51. **"This block prints 48 of the 62 rules the source carries."**
    - Where: the generated rules block.
    - Cannot tell: what the other 14 rules are or which surfaces they bind. The highest code printed is
      `r71`, so 62 does not follow from the numbering either, and I had to accept the retired-code sentence
      on trust.
    - Guess: the 14 bind spec bodies, chat, commits, or briefs, and some codes between r01 and r71 are dead.
    - Non-blocking.

52. **"The case is written text on the left and its repair on the right."**
    - Where: the generated rules block, its introduction.
    - Cannot tell: why many right-hand sides are instructions rather than repaired text — `r05` gives "name
      the actor that shows a colour", `r13` gives "answer it, and say what follows from the answer", `r32`
      gives "name the judge and the measure". The block states a rule about its own shape and then departs
      from it in roughly a fifth of its entries.
    - Guess: those entries record the repair's method where no single repaired sentence existed.
    - Non-blocking.

53. **"`Grep fallback: read for the four classes by hand - sentences past ~25 words ...` → `Grep fallback: read for those four classes by hand. The last one shows up as big, huge, minor, or breakthrough.`"**
    - Where: the case under `r41`.
    - Cannot tell: whether this is meant to be the same sentence I already read at line 207 of the lints
      section. It is — the repaired half is that sentence verbatim. The file's own `r56` says one fact lives
      in one home.
    - Guess: the rule block was generated from a record that happened to use this file's own text as its
      example.
    - Non-blocking.

54. **"Every case the class was built from lives in the rule home."**
    - Where: the generated rules block, its introduction.
    - Cannot tell: what "the rule home" is. The phrase appears twice — here and in `r61` — and is never
      defined. `guardrails/language-rules.json` is named two sentences later as where each rule is edited,
      which may or may not be the same place.
    - Guess: `guardrails/language-rules.json`.
    - Non-blocking.

55. **"The rules above are the whole set a human-prose audit holds a text to."**
    - Where: after the generated block.
    - Cannot tell: how this squares with "This block prints 48 of the 62 rules the source carries" 200 lines
      earlier. One says the set is partial, the other says it is whole. The reconciliation — that the 14
      absent rules bind other surfaces — has to be carried forward by the reader.
    - Guess: whole for human prose, partial as against the full 62.
    - Non-blocking.

56. **"Every page and every checker in the pack is built from that file, so one edit reaches all of them."**
    - Where: after the generated block.
    - Cannot tell: on what ground. Nothing on the page shows the generation covering every page and every
      checker; the one generator named, `scripts/gen-language-consumers.py`, owns a single block in this
      file.
    - Guess: the same generator writes all the consumer files.
    - Non-blocking.

57. **"the person"** (as the standing name for the human)
    - Where: "The roles and the words this skill uses", and throughout.
    - Cannot tell: whether "the person" is a defined role or a general word, since the auditor and the cold
      reader are also people, and the file says one person often holds more than one role. The file's own
      `r68` bans a general word standing where the thing's name fits.
    - Guess: it means the human who owns the text, as the roles list says, and no other human in the loop.
    - Non-blocking.

58. **"read a whole page only on the person's word"**
    - Where: "Per changed section the loop is cheap."
    - Cannot tell: what "on the person's word" requires — a request, an approval, a written instruction —
      and what I do if the person says nothing.
    - Guess: only when they explicitly ask for it.
    - Non-blocking.

59. **"**product-prover** reviews it. **design-reviewer** judges the design behind it."**
    - Where: "The pack this skill belongs to".
    - Cannot tell: what separates the two, especially since the "Work that belongs elsewhere" section sends
      "a design review of a spec" to product-prover, not to design-reviewer. The two lines pull in opposite
      directions.
    - Guess: product-prover checks the spec as written, design-reviewer questions the design choices, and
      the earlier section is loose about which is which.
    - Non-blocking.

---

Blocking entries: 6, 8, 11, 27, 30, 34, 35, 46.
