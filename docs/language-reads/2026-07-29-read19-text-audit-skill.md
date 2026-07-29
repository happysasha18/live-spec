# Cold read of `skills/text-audit/SKILL.md` — 2026-07-29

Stops: 44 — 5 blocking

1. **"It states the register it holds a text to"** — frontmatter `description`, near its end.
   A stranger cannot tell what a register is. The word arrives in the very sentence that promises the skill will state one, and the description never says what kind of thing gets stated.
   Guess: a named set of writing rules for a kind of text. (The body confirms this much later, but the description is the first text a reader meets.)
   Non-blocking.

2. **"The shared working rules live once in the pack's base skill, `live-spec-base` (v4.3.0)."** — the blockquote under the title.
   A stranger cannot tell where `live-spec-base` sits. Every other artifact in this document carries a path (`guardrails/…`, `scripts/…`, a repository URL); this one carries only a name and a version. A reader who wants "the shared working rules" has nowhere to go.
   Guess: another `SKILL.md` in the same repository, probably `skills/live-spec-base/SKILL.md`.
   Non-blocking.

3. **"Four scopes settle a setting there: the session's live word first, then the host profile, the personal profile, and the package default."** — same blockquote.
   A stranger cannot tell which settings this refers to. Nothing in this document names a single setting that varies, and "the session's live word", "the host profile", and "the personal profile" are three undefined terms in one sentence.
   Guess: things like the language of the output and how often the loop runs; the four names are places a value can be written, checked in that order.
   Non-blocking.

4. **"Used on its own, this skill is plain advice a person applies by hand."** — the blockquote, last sentence.
   Set against "An author cannot be their own cold reader" three paragraphs down, a stranger cannot tell how a lone person runs step 2. The loop's whole engine is a fresh session with no history, and the by-hand route names no substitute — no colleague, no second machine, no way to fake a cold read. The document offers a mode of use and then removes its central step.
   Guess: "by hand" means the person still needs a second reader from somewhere, and the sentence only means the scripts and the pack's automation are absent.
   Blocking.

5. **"The loop came from the comprehension gate on spec sections, recorded in `docs/spec-format.md`."** — "This skill checks whether a stranger understands…", fourth paragraph.
   A stranger cannot tell what a comprehension gate is. The term is used, never defined, and its home file is named but not summarised. The next sentence describes what the gate does, so the definition arrives one sentence late.
   Guess: a required check that a changed spec section passes before it ships.
   Non-blocking.

6. **"Those readers found new blocking terms on every pass, and the terms already repaired stayed repaired."** — same paragraph.
   "Blocking" is used here as if already known; the document defines it about two hundred lines later, under "The cold reader". A stranger also cannot tell how many passes ran, over how many sections, or where that record lives.
   Guess: blocking means a stop that halts the reader; the passes are the ones recorded in `docs/spec-format.md`.
   Non-blocking.

7. **"A **surface** is a kind of text, and one file carries several kinds at once. This project names six surfaces… This skill audits human prose, the surface a README, a report, a decision page, and a skill body stand on."** — the paragraph opening "A **surface** is a kind of text".
   One paragraph carries four separate points: what a surface is, the list of six, how a text is assigned to one, and which surface this skill covers. A stranger reading only the first sentence does not reach the fourth point, which is the one that governs the whole skill.
   Guess: the definition and the six-item list belong together, and the assignment rule plus the skill's own scope want their own paragraph.
   Non-blocking.

8. **"one file carries several kinds at once"** — same paragraph, first sentence.
   Two readings: either every file carries several kinds, or a file may. If it is "may", the sentence sits oddly as a flat statement of fact right beside a definition.
   Guess: a file may carry several kinds — a spec file holds both spec bodies and prose paragraphs.
   Non-blocking.

9. **"This project names six surfaces"** — same paragraph.
   A stranger cannot tell which project "this project" is. The skill is offered for use in any project (see the weak-word section, which tells the auditor to edit "that project's own `guardrails/weak-words.json`"), so "this project" could be the audited one or the live-spec one.
   Guess: live-spec, the repository the scripts live in.
   Non-blocking.

10. **"A text stands on one surface by what it is for, and a text published outside the project stands on the artifact surface as well."** — same paragraph.
    The sentence states a rule and breaks it in its own second half: one surface, then a second surface "as well". A stranger cannot tell which register wins for a published README — human prose, artifact, or both stacked.
    Guess: both apply, and the artifact rules are added on top of the surface's own.
    Non-blocking.

11. **"This skill audits human prose, the surface a README, a report, a decision page, and a skill body stand on."** — same paragraph — set against the whole section **"Running it on a spec section"** and against "It runs on any text a person will read: a spec section, a README, a decision page, marketing copy, an article, a release note."
    A stranger cannot tell what this skill's scope is. One sentence says it audits human prose and lists four document kinds. Another sentence lists six kinds, three of which (a spec section, marketing copy, an article, a release note) are absent from the human-prose list. A whole later section runs the skill on a spec section, which the document has just placed on a different surface with a different register and a different word cap. The scope decides which lints run, which cap applies, and whether the requirement-shape check is owed — so a reader cannot start without it.
    Guess: the skill runs on any of them, and "audits human prose" means only that human prose is its default register, with the spec-section section listing the four overrides.
    Blocking.

12. **"This skill holds a text to the human-prose register, printed in full at the end of this file."** — the paragraph opening "The **register** of a surface".
    Set against "This block prints 48 of the 62 rules the source carries", a stranger cannot tell whether the printed register is complete. "In full" and "48 of 62" read as a contradiction on first pass.
    Guess: all 48 human-prose rules are printed in full; the missing 14 bind other surfaces only.
    Non-blocking.

13. **"A **class** is the shape of a mistake: the form it takes wherever it turns up."** — the paragraph defining a class.
    The definition is circular for a stranger: shape is explained by form, and neither is grounded in an example at that point. I had to read it twice and then wait for `r61` at the very end of the file, which gives the worked case that makes it land.
    Guess: a class is the general pattern behind a group of individual mistakes.
    Non-blocking.

14. **"`guardrails/language-rules.json` is where the six surfaces, these words, and every rule below are edited."** — end of "The roles and the words this skill uses".
    "These words" points at a set whose members are never enumerated — the roles? the three defined terms? both? And the path carries no root at this point in the document; the root arrives only under "The mechanical lints", about a hundred lines later.
    Guess: "these words" means surface, register, and class; the root is the live-spec repository.
    Non-blocking.

15. **"Run every check a script or a grep settles, before a reader spends attention on it."** — step 1 of "The loop".
    "It" has no antecedent in its own sentence. A stranger reads it first as the check, then as the class, then settles on the text — three readings for one pronoun.
    Guess: "it" is the text.
    Non-blocking.

16. **"A script catches the classes a pattern can settle. Three of them are an undefined term, a known weak word, and a sentence that names a thing by denying its neighbour."** — step 1.
    A stranger cannot tell how many such classes there are, so "three of them" points at a set whose size and members are withheld. The mechanical-lints section further down lists five lints, not three, which makes the count look like a different set again.
    Guess: three examples out of five lints; the number three carries no meaning beyond "here are some".
    Non-blocking.

17. **"The audit runs in four steps and closes on a stated condition."** — opening line of "The loop".
    "A stated condition" stands where the condition itself would fit, in a sentence with room for it. A stranger has to read four steps to learn what it is.
    Guess: two consecutive reads with zero blocking findings.
    Non-blocking.

18. **"Per changed section the loop is cheap."** — the paragraph after step 4.
    A judgment word with no judge and no measure. Cheap in what — money, tokens, minutes, attention? Cheap against which alternative — auditing the whole page, or not auditing? The document's own printed rules (`r12`, `r32`) forbid exactly this, so the text breaks a rule it prints.
    Guess: cheap in reader attention, because only a few sentences go in front of a reader.
    Non-blocking.

19. **"Ten requirements at a time is the working size, which runs to about 250 lines. A fresh reader holds that much, and a repair inside those lines reaches nothing a hundred lines away."** — "Running it on a spec section".
    Three numbers with no ground: a stranger cannot tell what ten, 250, and a hundred were measured against, or which direction is better. The second sentence has two readings — either a repair's effects do not propagate a hundred lines away (a safety claim), or a repair fails to fix problems a hundred lines away (a limitation). Those are opposite meanings.
    Guess: the second reading — a fix here does not fix a related defect far away, so batching keeps the reader's span honest.
    Non-blocking.

20. **"A spec section stands on the spec-body surface, and four things change there."** — same section.
    "Change" relative to what baseline? The document never states what the default run looks like against which these four are deltas.
    Guess: relative to running the loop on human prose, described in the sections above.
    Non-blocking.

21. **"It reads three things a README never owes."** — "The requirement-shape lint applies here."
    "Owes" takes a document as its subject and a genre obligation as its object; a stranger reads it twice. A README also cannot owe anything — no actor is named.
    Guess: three things nobody would demand of a README.
    Non-blocking.

22. **"A rule binds a block, so the two never judge one sentence."** — "A criterion and the prose around it take different rules."
    "Block" is undefined and appears nowhere else in the document. "The two" points back across a sentence boundary to the criterion and the Context paragraph. I read this three times.
    Guess: a rule applies to a whole region of text, so the criterion's rules and the Context paragraph's rules never both apply to the same sentence.
    Non-blocking.

23. **"the test suite, which pins exact phrases from the spec, so a dropped phrase fails a test"** — the bulleted list of four checks after "Four checks run after the section is repaired, and each one prints what it read".
    Every other item in this list names a command. This one names no command, no path, and no suite. A stranger cannot run it. The lead sentence also says each check "prints what it read", but the second item is a human or agent reader, which does not print.
    Guess: whatever test command the audited project already uses.
    Non-blocking.

24. **"the census, `python3 scripts/rule-census.py`, whose count for the file is read against the count recorded for it in `guardrails/rule-census.json`. A count at the record or below it passes. A count above the record fails, and the batch runs again."** — same list, last item.
    A stranger cannot tell what the census counts. Rule violations? Findings? Occurrences of a term? The pass/fail verdict of an audit hangs on this number, and the document never says what the number is a number of. The word "census" is used as if already defined; it appears here for the first time.
    Guess: the number of rule violations the checker finds in that file.
    Blocking.

25. **The whole post-repair machinery — the four checks, the frozen baseline, `check-doc-findings-bound.py` at the push** — the second half of "Running it on a spec section".
    The mechanical-lints section promises a grep fallback for every lint, "so the audit never waits on a download". No such fallback exists for these checks, and a stranger working outside the live-spec repository cannot run one of them, cannot produce a frozen baseline, and has no `rule-census.json` to read a count against. The document does not say whether the spec-section route requires that repository or what to do without it.
    Guess: the whole spec-section route assumes the live-spec repository is on disk, and the section is written for a live-spec project only.
    Blocking.

26. **"`python3 scripts/spec-freeze.py --freeze … --compaction` writes it under `.spec-freeze/`, and a tree carrying no baseline there skips the check."** — the paragraph defining the frozen baseline.
    "It" has no antecedent in its own sentence — the document's own rule `r39` requires one. "A tree" is undefined: a repository checkout, a directory, a git worktree? And `--compaction` appears in a command with no word about what it does or whether it may be dropped.
    Guess: "it" is the frozen baseline; "a tree" is a repository checkout; `--compaction` is required, since the document shows no other form.
    Non-blocking.

27. **"On 2026-07-27 six requirements went to a fresh agent, and it built two of them"** — "The measure of the work is a build test", followed immediately by **"[Open question: no record names which six requirements that run used, which agent read them, or what it produced…]"**.
    The document offers a measured result and then, in the next paragraph, states that no record supports it. A stranger cannot tell whether the two-of-six figure is a fact, an estimate, or a mistake — and this is the document's single piece of evidence that the audit loop improves anything.
    Guess: the figure came from a plan document and was never verified, so it should be read as unconfirmed.
    Blocking.

28. **"[Open question: no record names which six requirements that run used…]"** — same section.
    An open question written with no question mark, and a self-audit note left in text a reader is meant to act on. A stranger cannot tell whether this is a note to the reader, a note to the maintainer, or a standing warning about the paragraph above it.
    Guess: a maintainer's note that should have been resolved before the file shipped.
    Non-blocking.

29. **"The count is taken before and after each batch, by two different fresh agents."** — same section.
    "Batch" is used here without definition; it appeared once earlier ("the batch runs again") also undefined. A stranger cannot tell whether a batch is the ten-requirement working size, one audit loop, or one push.
    Guess: the ten requirements audited together.
    Non-blocking.

30. **"When that repository is on your disk, run the scripts from its root, whatever project the audited text belongs to."** — "The mechanical lints", second paragraph.
    A stranger cannot tell how a script run from one repository's root reaches a file in another project. Does `FILE` take an absolute path? Does the rule data travel with the script or with the audited project? The weak-word paragraph much later says the project's own `guardrails/weak-words.json` gets edited, which points the other way.
    Guess: `FILE` takes an absolute path into the other project, and the rule data comes from the live-spec repository.
    Non-blocking.

31. **"Every domain noun the text uses carries a one-sentence definition"** — the first mechanical lint.
    "Domain noun" is undefined. A stranger cannot tell which nouns qualify — every noun belongs to some domain.
    Guess: a noun that carries a meaning specific to this project or field, as opposed to an everyday noun.
    Non-blocking.

32. **"list the capitalized and the coined nouns"** — grep fallback of the first lint.
    Set against rule `r23` ("No word stands in capitals for emphasis"), a stranger cannot tell whether "capitalized" means an initial capital or all capitals. In a document that bans the second, listing capitalized nouns as a discovery tactic reads as a contradiction on first pass.
    Guess: initial capital, as a rough signal that a word is a defined term.
    Non-blocking.

33. **"A human-prose sentence runs to 25 words at most, and one past 25 is a hit. A sentence shorter than 15 words passes, and 15 to 25 words is the band to aim at."** — "Style and register".
    Two readings for a 12-word sentence: it passes, but it is outside the band to aim at. A stranger cannot tell whether being outside the band matters, or whether "the band to aim at" is advice with no verdict behind it.
    Guess: under 15 words is fine and only the 25-word cap produces a hit.
    Non-blocking.

34. **"The reader-prompt below repeats the same list."** — grep fallback of the weak-word lint.
    The document prints the weak-word list twice and says so. Its own rule `r56` states that one fact lives in one home and every other place points at that home. A stranger cannot tell which copy is authoritative when the two drift.
    Guess: `guardrails/weak-words.json` is authoritative and both printed lists are copies.
    Non-blocking.

35. **"reading the text from outside (`docs/spec-style.md`, the clean-agent split)"** — "The cold reader", second paragraph.
    Two stops in one parenthesis. `docs/spec-style.md` sits beside `docs/spec-format.md` used twice earlier, and a stranger cannot tell whether these are two files or one file under two names. "The clean-agent split" is a coined name introduced with no gloss.
    Guess: two different files; the clean-agent split is the practice of using an agent with no project context.
    Non-blocking.

36. **"the non-blocking ones queue for a taste call"** — end of "The cold reader".
    "Taste call" is undefined and "queue" names no queue — no file, no list, no owner. A stranger who finishes an audit with eleven non-blocking findings does not know where to put them.
    Guess: a judgment the person makes later, parked wherever the project tracks such things.
    Non-blocking.

37. **"The rules at the end of this file name more classes, and most of them need a rulebook the cold reader does not hold."** — "The reader-prompt — ready to paste".
    "Most of them" gives no count and no measure. A stranger cannot tell which classes the reader can judge unaided beyond the five, which matters because the prompt's last instruction asks the reader for exactly those.
    Guess: roughly 40 of the 48, with the five in the prompt as the unaided set.
    Non-blocking.

38. **"a judgment word — broken, worth, better, enough, larger-than — with no stated judge or measure"** — inside the pasteable prompt.
    "Larger-than" is not a word a stranger recognises as written, and "larger" already stands in the relational list four bullets above. A reader of the prompt cannot tell whether a bare "larger" belongs to the relational class or the judgment class.
    Guess: a typo for "larger than", and the overlap is unintentional.
    Non-blocking.

39. **"In any other project, the auditor edits that project's own `guardrails/weak-words.json`, and creates that file carrying a `weak_words` list where the project holds none."** — the paragraph after the prompt.
    Set against "That list is `guardrails/weak-words.json`", a stranger cannot tell how many weak-word lists exist or which wins when both are present. The instruction also creates a second home for a fact the document elsewhere insists lives in one home.
    Guess: the list is read from the directory holding the script, so exactly one applies per run, and the two never merge.
    Non-blocking.

40. **"A fix comes from the material the text rests on, and from nowhere else."** — "Fixes come from the source, never from invention".
    The same instruction stands in three places: step 3 of the loop, the "A fix comes from the spec's own neighbours" paragraph, and this whole section. The `[GAP: what is missing]` marker is likewise given twice. A stranger rereads to check whether the third statement adds a new rule or repeats the first two.
    Guess: it repeats them, and only the sentence about the marker taking the text's own form is new.
    Non-blocking.

41. **"A passing run prints one line, naming no coined metaphor, no loan translation, and no transliterated pack term."** — "This skill is held to the rules it lists".
    The sentence tells the reader what a passing line does not name, which is the shape the document's own rule `r10` forbids. "Loan translation" and "transliterated pack term" are both undefined; a stranger with no Russian-and-English background cannot picture either.
    Guess: the line reports zero findings in three named categories, and the two terms describe words carried over from another language.
    Non-blocking.

42. **"Four of those rules show throughout it"** — same section.
    A stranger cannot tell why these four out of 48, or what "show throughout" means as a testable claim. No measure, no judge.
    Guess: the author picked four illustrative rules, and the list is not exhaustive.
    Non-blocking.

43. **"This block prints 48 of the 62 rules the source carries."** — the generated rules block, second paragraph.
    A stranger cannot verify either number without counting by hand, and the printed codes run from `r01` to `r71` with visible gaps (`r16`, `r17`, `r19`, `r21`, `r22`, `r24`, and others), so the code range agrees with neither 48 nor 62. The claim and the printed evidence do not obviously match.
    Guess: 48 entries are printed, 62 rules are live across all six surfaces, and the code numbers run past 71 because retired rules keep their codes.
    Non-blocking.

44. **"`INV-141` gives the design review a pass of its own." → "The design review runs as a pass of its own [INV-141]."** — the recorded case under `r11`, and the parallel `[INV-241]` under `r63`.
    A stranger cannot tell what an `INV-` code names. The cases teach where such a code sits in a sentence, while the thing itself stays unexplained, and the same examples are the ones a reader studies most closely.
    Guess: an invariant identifier from a project spec.
    Non-blocking.

Blocking entries: 4, 11, 24, 25, 27.
