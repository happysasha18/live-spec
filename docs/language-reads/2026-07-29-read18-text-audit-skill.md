# Cold read of `skills/text-audit/SKILL.md` — read 2026-07-29

Stops: 56 — 10 blocking

1. **"Part of the **live-spec pack**"** — under the opening blockquote, first line of the note.
   A stranger cannot tell what a "pack" is: a plugin, a directory of files, a set of skills, or a product.
   I guessed it is a bundle of related skill files shipped together, because the last section lists ten named members.
   Non-blocking.

2. **"together with the settings ladder"** — opening blockquote, "The shared working rules live once in the pack's base skill".
   A stranger cannot tell what the settings ladder is, what settings it covers, or what its rungs are. Nothing on this page defines it, and no path to a definition is given beyond the skill's name. This same phrase appears at the end of the document as the recorded defect under rule `r67`, with the repair spelled out — so the document breaks a rule it prints.
   I guessed it is an order of precedence for configuration values, because rule `r67`'s repair names four scopes.
   Blocking.

3. **"Used on its own, this note is plain advice."** — opening blockquote, last sentence.
   A stranger cannot tell what "on its own" is being contrasted with, or what changes: is the advice non-binding, unenforced, or simply unautomated? Nor what it is when *not* used on its own.
   I guessed it means that without the rest of the pack installed, nothing here is checked by a script, so the reader follows it by hand.
   Non-blocking.

4. **"The loop came from the spec-format comprehension gate."** — "This skill checks whether a stranger understands a text".
   A stranger cannot tell what a "gate" is here (a script, a review step, a policy) or what "spec-format" names.
   I guessed it is a check that had to pass before a spec-format document shipped.
   Non-blocking.

5. **"A panel of fresh readers found new blocking terms on every pass"** — same paragraph.
   A stranger cannot tell how many readers, over how many passes, on how much text. The claim that carries the whole stopping rule rests on a set whose members are never given.
   I guessed three to five readers over a handful of passes.
   Non-blocking.

6. **"(`docs/spec-format.md`)"** — same paragraph.
   A stranger cannot tell which root this path is relative to. The document only states a root two sections later, under the mechanical lints, and that statement is scoped to the scripts.
   I guessed it is relative to the live-spec repository named later.
   Non-blocking.

7. **"a decision page before it goes to the person"** — "When it fires", third bullet.
   A stranger cannot tell what a decision page is: a document, a rendered web page, a chat message. "The person" is also unnamed here (see entry 20).
   I guessed a written page that asks a human to choose between stated options.
   Non-blocking.

8. **"A design review of a spec belongs to product-prover."** — "Work that belongs elsewhere", first bullet.
   A stranger meeting `product-prover` here cannot tell whether it is a person, a script, or another skill. The one-line answer sits at the very bottom of the file.
   I guessed it is a sibling skill, from the typography.
   Non-blocking.

9. **"a missing state, a false invariant, an unhandled transition"** — same bullet.
   A stranger cannot tell what an invariant or a transition is in this project's sense; they carry the weight of the boundary between the two skills.
   I guessed the vocabulary of formal state machines.
   Non-blocking.

10. **"Taste and voice stay with the person and with the marketing skills."** — "Work that belongs elsewhere", second bullet.
    A stranger cannot name the members of "the marketing skills", and none of the ten skills listed at the bottom is a marketing skill.
    I guessed a separate family of skills outside this pack.
    Non-blocking.

11. **"This skill holds a text to the register it lists at the end"** — "Work that belongs elsewhere", second bullet.
    A stranger cannot tell what "register" means. The word carries the skill's entire standard, appears in the frontmatter, in a heading ("Style and register"), in a script name, and in "This SKILL.md obeys the register below", and it is never defined. Relative to what is a register judged, and by what measure?
    I guessed it means the printed rule set at the end, treated as a style standard.
    Blocking.

12. **"A worker brief, a checkpoint, and an internal note are machine-read."** — "Work that belongs elsewhere", third bullet.
    A stranger cannot tell what a worker brief or a checkpoint is, and the sentence is the only test offered for whether a given text needs an audit at all. It also reads as circular: these three are machine-read because the document says so.
    I guessed a worker brief is a task handed to an automated agent, and a checkpoint is a saved state note.
    Non-blocking.

13. **"The audit runs in four steps and closes on a stated condition."** — "The loop", first line.
    A stranger cannot tell what the condition is until step 4, and the sentence announces a shape rather than saying anything. This is a class outside the list I was given — an announcement sentence standing before the concrete content it announces — so I mark it **new**.
    I guessed the condition is the two-clean-reads rule, and read on.
    Non-blocking. (new class)

14. **"Run every check a script or a grep settles"** — "The loop", step 1.
    A stranger cannot tell what makes a check settleable by a script, nor how to judge that for a class not on the list below.
    I guessed it means any check with a mechanical test, and that the list of five lints is the whole set.
    Non-blocking.

15. **"A machine catches the cheap classes"** — "The loop", step 1.
    "Cheap" is a judgment with no judge and no measure: cheap in what, tokens, reader attention, wall time? A stranger also meets "class" here as a term for the first time, and it is not defined until rule `r61` at the bottom.
    I guessed cheap means low in reader attention, since the next sentence talks about attention.
    Non-blocking.

16. **"The cold reader then spends its whole attention on the classes no machine knows yet."** — "The loop", step 1.
    A machine that "knows" is a predicate the subject cannot carry, which the document's own rule `r05` forbids. A stranger also cannot tell which classes those are.
    I guessed it means the classes no script in the list below tests for.
    Non-blocking.

17. **"It returns the places a stranger stops, each one marked blocking or non-blocking. It repairs nothing."** — "The loop", step 2.
    The antecedent of "It" sits in the previous sentence, not this one. Rule `r39` at the bottom prints this exact sentence as its recorded defect, with the repair "That session returns the places a stranger stops" — so the document states a rule and then breaks it.
    I guessed "It" is the cold-reader session.
    Non-blocking.

18. **"The stream is shown to have thinned to zero when two reads in a row return nothing that blocks"** — "The loop", step 4.
    Shown by whom, and to whom? The sentence has no actor and its action sits inside a passive. A stranger also cannot tell whether "thinned to zero" is a measured result or a working assumption.
    I guessed it is an assumption the spec-format gate adopted after observing it once.
    Non-blocking.

19. **"Per changed section the loop is cheap."** — paragraph after step 4.
    I read this twice to parse the opening. "Cheap" is again a judgment with no measure: cheap against what alternative — auditing the whole page, or not auditing at all?
    I guessed it means one section costs one reader session rather than many.
    Non-blocking.

20. **"read a whole page only on the person's word"** — paragraph after step 4.
    A stranger cannot tell who "the person" is. The phrase recurs — "stay with the person", "a question for the person who owns the text", "every sentence shown to the person" — and it is the gate on a real action here: you may not audit a whole page without this unnamed person's approval.
    I guessed it is whoever asked for the audit, from the later phrase "whoever asked for the audit".
    Blocking.

21. **"one requirement with its Context paragraph, its User Story, and its acceptance criteria"** — "Running it on a spec section".
    Three capitalized terms arrive undefined, and they are the parts the reader must identify to slice a section correctly.
    I guessed the conventional requirements-document meanings.
    Non-blocking.

22. **"Four things change on this surface."** — "Running it on a spec section".
    "Surface" is used throughout as a load-bearing term — "any human-facing surface", "the word cap for its surface", "the language its surface is pinned to", "the rules binding the surface" — and it is never defined. The word cap and the language rule both depend on knowing which surface a text belongs to, and no list of surfaces appears anywhere.
    I guessed a surface is a kind of destination for text (a spec, a README, chat, a commit message), each with its own rules.
    Blocking.

23. **"Ten requirements at a time is the working size, which runs to about 250 lines. A fresh reader holds that much"** — "Running it on a spec section".
    A stranger cannot tell what the 250 lines is measured against, which direction is better, or on what ground a reader is known to hold that much and not more.
    I guessed the number came from practice on this project and is a rule of thumb.
    Non-blocking.

24. **"a repair inside those lines reaches nothing a hundred lines away"** — same paragraph.
    I read this twice. "Reaches" opens a slot: reaches in what sense — a change of meaning, a broken reference, a test failure? And a hundred lines relative to what boundary?
    I guessed it means edits inside a section do not change meaning elsewhere in the file.
    Non-blocking.

25. **"It reads three things a README never owes."** — "The requirement-shape lint applies here".
    "Owes" is used here and four more times ("A spec section owes the requirements genre", "the checks a publication owes its reader") as though a document could hold an obligation. A stranger cannot tell who is owed, and the everyday word ("a README does not need") says the same thing.
    I guessed it means these three checks do not apply to a README.
    Non-blocking.

26. **"A rule binds a block, so the two never judge one sentence."** — "A criterion and the prose around it take different rules".
    I read this twice and still hesitated on "the two": the two rules, the two blocks, or the criterion and the paragraph? "Block" is also undefined.
    I guessed "the two" means the two rules just described.
    Non-blocking.

27. **"breaks the code-to-location table, the test matrix, or a test"** — "Every mark a machine reads survives the repair".
    Three artifacts arrive undefined — the code-to-location table, the test matrix, and "bracket anchors" a sentence earlier — and the reader is asked to preserve marks it cannot identify.
    I guessed bracket anchors are short codes in square brackets, from the examples under `r11`.
    Non-blocking.

28. **"the structure checks over requirement shape, the generated index, the matrix references, and the frozen baseline"** — "Four checks run after the section is repaired".
    Every other item in this list of four names a command or a concrete act; this one names four checks with no command, and "the frozen baseline" is undefined anywhere on the page. A reader cannot run this check.
    I guessed there is a script per check somewhere in the repository, and that a frozen baseline is a stored copy of the file used for comparison.
    Blocking.

29. **"the census, `python3 scripts/rule-census.py`, whose count for the file falls, or the batch is redone"** — same list.
    Falls relative to what — the count before the repair, a target, zero? I read the clause twice and still cannot tell what it counts. The consequence is concrete (redo the batch), so the missing reference point decides real work.
    I guessed it counts rule violations and must be lower than the pre-repair count.
    Blocking.

30. **"On 2026-07-27 that count was two of six."** — "The measure of the work is a build test".
    A stranger cannot tell whether two of six is a pass, a failure, or a baseline, nor which direction is better, nor what follows from it.
    I guessed higher is better and that two of six is reported as a poor result.
    Non-blocking.

31. **"list the capitalized and the coined nouns"** — "Every term is defined at first use", grep fallback.
    A stranger cannot tell how to recognize a coined noun in a project they have never seen — that is precisely the knowledge a cold reader is defined as lacking.
    I guessed any noun that reads as project-specific.
    Non-blocking.

32. **"The reader-prompt below repeats the same list."** — "A weak relational word fills the slot it opens", grep fallback.
    The weak-word list is printed twice on this page, and the document says so plainly. Rule `r56` at the bottom states that one fact lives in one home and every other place points at it, so the page breaks a rule it prints.
    I guessed the duplication is deliberate because the prompt must be pasteable on its own.
    Non-blocking.

33. **"Context comes before criteria, each criterion carries one trigger and one response, and every judgment names a judge and a measure."** — "A spec section owes the requirements genre".
    This states, a second time, what "The requirement-shape lint applies here" already stated in the previous section, down to the same three points and the same script name. Against `r56`.
    I guessed the mechanical-lints section is meant to stand alone as a checklist.
    Non-blocking.

34. **"A sentence stays between 15 and 25 words, and one past 25 is a hit."** — "Style and register".
    Two readings: either a sentence shorter than 15 words is also a violation, or only sentences past 25 are flagged. The two halves of the sentence disagree. This document's own sentences run to five words ("This skill supplies the stranger."), which suggests short sentences pass — so the stated range misdescribes the rule the page itself follows.
    I guessed only the upper bound is enforced.
    Blocking.

35. **"It stays under the word cap for its surface"** — rule `r08` in the printed rule block.
    Rule `r08` says the cap varies by surface; the "Style and register" lint states one cap of 25 words for everything. A reader auditing a README cannot tell which cap applies, and no table of per-surface caps appears.
    I guessed 25 words is the default and other surfaces have caps recorded elsewhere.
    Blocking.

36. **"The last one shows up as *big*, *huge*, *minor*, or *breakthrough*."** — "Style and register", grep fallback.
    The rule it illustrates is "no adjective grades a result's size", but *breakthrough* is a noun and grades importance, not size. The example does not match its rule.
    I guessed the rule is meant to cover both size and importance, as rule `r12` does.
    Non-blocking.

37. **"No artifact appears under two names."** — "One name per thing".
    "Artifact" is undefined and could mean a file, a product, a build output, or any named thing. The scope of the check turns on it.
    I guessed it means any named thing the text refers to.
    Non-blocking.

38. **"The reader holds **zero context on the text's history**"** — "The cold reader".
    This states, a third time, what the second paragraph of the document and step 2 of the loop already state. Against `r56`.
    I guessed the repetition is for readers who jump straight to this section.
    Non-blocking.

39. **"(`docs/spec-style.md`, the clean-agent split)"** — "The cold reader".
    "The clean-agent split" is a named thing with no definition on this page; the citation points to a file, not to a definition of the term.
    I guessed it is a practice of keeping the drafting session separate from the reviewing session, from rule `r53`.
    Non-blocking.

40. **"An undefined term the rest of the text leans on blocks."** — "Every finding is marked blocking or non-blocking".
    I read this twice: "leans on blocks" first parsed as a verb plus its object. The sentence's verb is the last word.
    I guessed it means an undefined term that the rest of the text depends on is a blocking finding.
    Non-blocking.

41. **"the non-blocking ones queue for a taste call"** — same paragraph.
    "Taste call" is a coined phrase where "a judgment by the person" says the same thing. A stranger cannot tell who makes it, when, or where the queue lives.
    I guessed the unnamed person decides later whether to apply non-blocking fixes.
    Non-blocking.

42. **"a judgment word — broken, worth, better, enough, larger-than — with no stated judge or measure"** — inside the reader-prompt.
    "larger-than" is not a word a reader will find in a text, and "larger" is listed three lines above as a *relational* word. The prompt's two lists put the same word in two classes.
    I guessed it is a slip for "larger than X".
    Non-blocking.

43. **"keeps the reader catching words the list does not know yet"** — paragraph after the reader-prompt.
    A list that "knows" is a predicate the subject cannot carry, which rule `r05` forbids.
    I guessed it means words the list does not contain.
    Non-blocking.

44. **"the auditor adds it by hand to the weak-word list"** — same paragraph.
    "The auditor" appears once, here, as an actor never introduced. Elsewhere the actors are "the person", "the author", "this skill", and "a fresh session".
    I guessed the auditor is whoever runs this skill, which may be the same as "the person".
    Non-blocking.

45. **"and the project's own copy of the list otherwise"** — same paragraph.
    When the live-spec repository is not on disk, the reader is told to update "the project's own copy" and given no path, no filename, and no way to know whether one exists. The branch that applies to every project except one is the branch with no address.
    I guessed a file of the same name somewhere under the current project.
    Blocking.

46. **"This SKILL.md obeys the register below. Four of those rules show on every page of it"** — "This file is held to the rules it lists".
    A stranger cannot tell why these four of roughly fifty are singled out, nor what "every page" means for a single file with no pages.
    I guessed "page" is loose for "throughout".
    Non-blocking.

47. **"no coined metaphor does the talking"** — same list.
    The sentence claiming there is no metaphor uses one: rules that "do the talking". A rule broken inside the sentence stating it.
    I guessed it means no coined term stands where a plain word works.
    Non-blocking.

48. **"that run is clean"** — "This file is held to the rules it lists".
    A claim whose ground sits nowhere: no date, no output, no version of the file it was run against. Reading the page, I met the settings-ladder phrase that rule `r67` prints as a defect (entry 2), the pronoun sentence rule `r39` prints as a defect (entry 17), three restatements of the cold-reader definition against `r56` (entries 32, 33, 38), and a metaphor inside the no-metaphor line (entry 47) — so the claim of a clean run is one I cannot trust as written.
    I guessed the lint checks a narrower set of classes than the printed rule block.
    Blocking.

49. **"These are every rule binding human-prose."** — "The rules it holds a text to".
    I read this twice; "These are every rule" does not parse on the first pass.
    I guessed it means the block below is the complete set.
    Non-blocking.

50. **"Every case the class was built from lives in the rule home."** — same paragraph.
    "The rule home" is a coined term for a place the same paragraph has already named as `guardrails/language-rules.json`. One thing under two names, against rule `r04` printed twelve lines later.
    I guessed the rule home is that JSON file.
    Non-blocking.

51. **"The case is written text on the left and its repair on the right."** — same paragraph.
    Many cases below carry an instruction on the right rather than repaired text: "name the actor that shows a colour", "state the exact quantity", "delete", "do the act and report it done", "name the fix in one line, make it, and go on". The rule is stated and then broken by the block it describes.
    I guessed the instruction form is used where the repair depends on facts the case does not carry.
    Non-blocking.

52. **"(`r01`) … (`r68`)"** — the printed rule block, throughout.
    The codes skip: `r16`, `r17`, `r19`, `r21`, `r22`, `r24`, `r28`–`r31`, `r34`–`r38`, `r40`, `r42`, `r47`, `r51`, `r55`, `r58`–`r60` are absent, while the lead-in says "These are every rule binding human-prose". A stranger cannot tell whether rules were dropped, renumbered, or filtered out.
    I guessed the missing codes bind surfaces other than human prose and are filtered by the generator.
    Non-blocking.

53. **"`the door` → `the entry point`"** — rule `r02`, its recorded case.
    The case gives no context, so a stranger cannot tell what "the door" named or why "entry point" is the standard word for it.
    I guessed "the door" was this project's coined name for the place work enters.
    Non-blocking.

54. **"a fresh writer with no package rules loaded"** — rule `r53`.
    "Package" appears here and in `r67`'s repair ("the package default") for what the rest of the document calls "the pack". One thing under two names, against `r04`.
    I guessed package and pack are the same thing.
    Non-blocking.

55. **"`The system shall refuse each of the four faults below. - a branch behind main's tip; - a lane with no open row; …`"** — rule `r64`, its recorded case.
    The repair demonstrating "one item per line" prints its four items run together on one line. The example contradicts the rule it exists to show. The case also uses "lane", "open row", and "worktree line", none of them defined.
    I guessed the line breaks were lost when the block was generated.
    Non-blocking.

56. **"One short document walked end to end against these rules"** — closing paragraph before the pack list.
    A document that walks is an actor that cannot carry the verb, and the sentence hides who did the walking. I also read "walked end to end against these rules" twice.
    I guessed a person applied every rule to that document in order and recorded each fix.
    Non-blocking.

Blocking entries: 2, 11, 20, 22, 28, 29, 34, 35, 45, 48.
