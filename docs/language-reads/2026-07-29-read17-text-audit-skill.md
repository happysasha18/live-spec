# Cold read of `skills/text-audit/SKILL.md` — 2026-07-29

Stops: 45 — 15 blocking

1. **"Part of the **live-spec pack**"**
   - Where: the block quote under the title, opening words "Part of the live-spec pack."
   - What a stranger cannot tell: what the live-spec pack is, what it contains, and whether a reader needs it to use this file. The last section lists eleven names under "The pack this skill belongs to", but that list arrives at the very end and never says what a pack is.
   - My guess: a bundle of related skill files installed together.
   - Non-blocking.

2. **"together with the settings ladder"**
   - Where: the block quote under the title.
   - What a stranger cannot tell: what the settings ladder is. No definition here and no path to one. The same file, at rule `r67`, prints this exact phrase as its recorded defect, with the repair spelled out ("the four scopes that settle a setting: the session's live word, the host profile, the personal profile, and the package default"). So the document states a rule and breaks it in its own third sentence, with its own fix sitting 400 lines below.
   - My guess: some ordering of configuration scopes, which I only learned by reaching `r67` at the end of the file.
   - Blocking — I cannot trust a rulebook that carries the case its own rule bans, unrepaired, at the top of its page.

3. **"Used on its own, this note is plain advice."**
   - Where: the block quote under the title.
   - What a stranger cannot tell: two readings are open. Either (a) without the base skill loaded, this file has no enforcing machinery and is only guidance, or (b) outside the live-spec project, the file is generic writing advice. I also cannot tell what "on its own" is opposed to, since nothing yet said the file is normally used with something else.
   - My guess: reading (a).
   - Non-blocking.

4. **"The loop came from the spec-format comprehension gate."**
   - Where: heading area of the opening section, paragraph beginning "The loop came from".
   - What a stranger cannot tell: what the spec-format comprehension gate is, when it ran, and who ran it. Everything downstream rests on it — the two-clean-reads stopping rule is justified twice by citing it. The path `docs/spec-format.md` is offered, but at this point in the file no repository has been named (that comes only in "The mechanical lints", 100 lines later), so I cannot open it.
   - My guess: an earlier internal exercise in this same project that read spec text with fresh readers.
   - Blocking — the document's central stopping rule has no ground a reader of this page can reach.

5. **"found new blocking terms on every pass"**
   - Where: same paragraph, "A panel of fresh readers found new blocking terms".
   - What a stranger cannot tell: what "blocking" means here. The definition arrives ~145 lines later in "The cold reader". The word is also load-bearing in the stopping rule stated in this very paragraph. "Pass" is likewise undefined at first use.
   - My guess: a term whose absence stops a reader from going on — confirmed later.
   - Non-blocking.

6. **"(`docs/spec-format.md`)"**
   - Where: same paragraph, at its end.
   - What a stranger cannot tell: which repository or working directory this path is relative to. The file only anchors paths later, and it anchors only `guardrails/` and `scripts/` ("every path below is relative to that repository's root", scoped to the lint list). `docs/…` paths appear four times and are never anchored.
   - My guess: the same live-spec repository named further down.
   - Non-blocking.

7. **"This skill checks whether a stranger understands a text, and repairs the places where they stop."**
   - Where: the first line of the body, above the cold-reader definition.
   - What a stranger cannot tell: who acts. A skill is a file; a file does not check or repair. The same pattern runs through the document — "This skill supplies the stranger", "This skill packages that loop", "the one move this skill forbids", "It grades no voice". Rule `r05` in this file's own rule block bans a predicate applied to a subject that cannot carry it, and `r26` demands a named actor.
   - My guess: the session or agent that has loaded the file does the checking and repairing.
   - Non-blocking.

8. **"a decision page before it goes to the person"**
   - Where: "When it fires", third bullet.
   - What a stranger cannot tell: who "the person" is. The phrase carries a definite article on first use, and it recurs as the pivot of several instructions: "Taste and voice stay with the person", "read a whole page only on the person's word", "Record it as a question for the person". Alongside it the document names an author, an owner ("the person who owns the text"), an auditor, a human, and whoever asked for the audit — and never says whether these are one role or several. Step 3 tells me to hand unresolved findings to "the person", so I have to know.
   - My guess: the human who requested the audit, who may or may not be the author.
   - Blocking — a required step names a recipient the page never identifies.

9. **"a missing state, a false invariant, an unhandled transition"**
   - Where: "Work that belongs elsewhere", first bullet.
   - What a stranger cannot tell: what an invariant or a transition is in this context. They are used to draw the boundary between this skill and product-prover, and nothing on the page defines either, nor points to where they are defined.
   - My guess: formal-specification vocabulary — a property that must always hold, and a move between states.
   - Non-blocking.

10. **"This skill holds a text to the register it lists at the end"**
    - Where: "Work that belongs elsewhere", second bullet.
    - What a stranger cannot tell: what "register" means as this document uses it. It appears again as a heading ("Style and register"), as a script name (`preshow-register-lint.py`), and as "This SKILL.md obeys the register below". It is never defined, and it is doing the work of separating what this skill judges from what it refuses to judge.
    - My guess: the set of writing rules printed in the generated block at the end.
    - Non-blocking.

11. **"The audit runs in four steps and closes on a stated condition."**
    - Where: "The loop", first line.
    - What a stranger cannot tell: which condition, and where it is stated. The sentence announces that something is said elsewhere rather than saying it. The condition turns out to sit inside step 4, so the lead-in adds a lookup and no fact.
    - My guess: the two-clean-reads rule in step 4.
    - Non-blocking.

12. **"A machine catches the cheap classes"**
    - Where: "The loop", step 1.
    - What a stranger cannot tell: cheap by what measure — running time, attention, cost of the fix? And "class" is used here as a project term for the first time; its meaning only becomes clear at rule `r61`, 350 lines later. The next sentence, "the classes no machine knows yet", asserts a boundary between machine-catchable and reader-catchable classes that the page never draws.
    - My guess: cheap = mechanically detectable by a script, so a reader's attention should not be spent on it.
    - Non-blocking.

13. **"It returns the places a stranger stops, each one marked blocking or non-blocking."**
    - Where: "The loop", step 2.
    - What a stranger cannot tell: what "It" points at. The preceding sentence has two candidate subjects — the reader session and the reader-prompt. Rule `r39` in this same file records this exact sentence as its defect case and prints the repair: "That session returns the places a stranger stops." The uncorrected version is still standing in the body.
    - My guess: the fresh reader session.
    - Blocking — the document publishes the fix for this sentence and does not apply it, which puts the whole rule block in doubt.

14. **"the stopping rule the spec-format gate observed"**
    - Where: "The loop", step 4.
    - What a stranger cannot tell: whether "the spec-format gate" is the same thing as "the spec-format comprehension gate" named in the opening section. Rule `r04` on this page forbids one thing answering to a second name. Also, "observed" leaves the actor out — a gate does not observe.
    - My guess: the same thing, shortened.
    - Non-blocking.

15. **"The stream is shown to have thinned to zero when two reads in a row return nothing that blocks (`docs/spec-format.md`)."**
    - Where: "The loop", end of step 4.
    - What a stranger cannot tell: who showed it, and how this differs from the opening section's "The stream of findings reached zero only under two clean reads in a row (`docs/spec-format.md`)". The same fact, with the same citation, is stated in two places — the pattern rule `r56` names.
    - My guess: one fact with one source, written twice.
    - Non-blocking.

16. **"Per changed section the loop is cheap."**
    - Where: paragraph after "The loop", opening words.
    - What a stranger cannot tell: cheap against what — a full-page audit, a human review, no audit at all? No measure, no judge. The document's own `r32` demands both.
    - My guess: it costs one short reader session rather than a whole-document read.
    - Non-blocking.

17. **"A small edit puts one definition and a handful of sentences in front of a reader."**
    - Where: same paragraph.
    - What a stranger cannot tell: how many sentences "a handful" is. Rule `r33`'s recorded case is literally `a few` → `state the exact quantity`. "Small edit" carries the same emptiness — small by what measure.
    - My guess: three to ten sentences.
    - Non-blocking.

18. **"Ten requirements at a time is the working size, which runs to about 250 lines."**
    - Where: "Running it on a spec section", second paragraph.
    - What a stranger cannot tell: where ten comes from, whether it was measured or chosen, and which way is better if I miss it. Rule `r06` requires a number to say what it is compared against and which direction is better. The following sentence adds a second, unexplained number — "a repair inside those lines reaches nothing a hundred lines away" — and I cannot reconcile a hundred-line reach with a 250-line batch: either the batch exceeds the reach of a repair, or "reach" means something else.
    - My guess: ten was chosen by trial, and the hundred-line figure is a loose statement that repairs stay local.
    - Non-blocking.

19. **"Four things change on this surface."**
    - Where: "Running it on a spec section", after the batch-size paragraph.
    - What a stranger cannot tell: what a "surface" is. The word is load-bearing across the file — "any human-facing surface", "It stays under the word cap for its surface", "Every document is written to the rules of its surface", "It is a human-facing surface". Different surfaces apparently take different word caps and different lints, but the page never lists the surfaces or says how to tell which one a given text is.
    - My guess: a kind of text with its own rule set — spec section, README, chat reply, commit message.
    - Blocking — the word caps and the lint selection both depend on it, so I cannot apply the rules without knowing which surface I am on.

20. **"It reads three things a README never owes."**
    - Where: "Running it on a spec section", the requirement-shape paragraph.
    - What a stranger cannot tell: what it means for a text to owe something, and to whom. The verb recurs — "A spec section owes the requirements genre", "the checks a publication owes its reader". It reads as a coined use where "require" or "contain" would say it. The three things that follow ("Context comes before criteria. Each criterion carries one trigger and one response. Every judgment names a judge and a measure.") are then printed a second time, near-verbatim, in the mechanical-lints bullet for the same script.
    - My guess: a README is not held to those three checks.
    - Non-blocking.

21. **"A rule binds a block, so the two never judge one sentence."**
    - Where: "Running it on a spec section", the criterion-versus-prose paragraph.
    - What a stranger cannot tell: which two. Candidates are the two rules just described, the criterion and the Context paragraph, or the person and prose voice. I read it three times.
    - My guess: the two rules — the third-person criterion rule and the direct-address Context rule.
    - Non-blocking.

22. **"A requirement's number and its bracket anchors stay exactly as they were."**
    - Where: "Running it on a spec section", the machine-marks paragraph.
    - What a stranger cannot tell: what a bracket anchor is, and what the "code-to-location table" in the next sentence is. Both are named as things a rewrite can break, so I must recognize them to avoid breaking them.
    - My guess: a short code in square brackets at the end of a line, and a generated index mapping those codes to file positions.
    - Non-blocking.

23. **"the structure checks over requirement shape, the generated index, the matrix references, and the frozen baseline"**
    - Where: "Running it on a spec section", third of the four post-repair checks.
    - What a stranger cannot tell: what the generated index is, what the matrix references are, what the frozen baseline is, and which command runs any of them. The other three checks in this list name a script or describe an action; this one names four artifacts I have never met and no way to run anything.
    - My guess: further guardrail scripts in the same repository, not listed here.
    - Blocking — the document instructs me to run four checks and leaves one of them unperformable.

24. **"the census, `python3 scripts/rule-census.py`, whose count for the file falls, or the batch is redone"**
    - Where: "Running it on a spec section", fourth post-repair check.
    - What a stranger cannot tell: what the census counts, what it is compared against, and by how much it must fall. "Falls" is a relational word with all three slots open — relative to what (the pre-repair count?), by what measure (any drop? a threshold?), against what alternative. Redoing an entire batch of ten requirements is an expensive consequence to hang on an unstated comparison.
    - My guess: it counts rule violations in the file, and any number lower than the pre-repair run passes.
    - Blocking — a stated pass/fail gate with no stated threshold.

25. **"On 2026-07-27 that count was two of six."**
    - Where: "Running it on a spec section", last paragraph, after "The measure of the work is a build test."
    - What a stranger cannot tell: whether two of six is a pass, a failure, or a baseline; what the target is; and what I do with my own number when I run the build test. The sentence is offered as the measure of the work and gives me no direction of better.
    - My guess: two of six is poor, and the target is six of six.
    - Blocking — the page names one measure of whether the whole method worked and never says how to read it.

26. **"list the capitalized and the coined nouns"**
    - Where: "The mechanical lints", grep fallback of the first bullet.
    - What a stranger cannot tell: how to recognize a coined noun without already knowing the project's vocabulary — which is exactly what the cold reader is defined as lacking. The fallback asks the reader to apply the judgment the check exists to make.
    - My guess: a noun that returns no result in ordinary usage, judged by feel.
    - Non-blocking.

27. **"The reader-prompt below repeats the same list."**
    - Where: "The mechanical lints", weak-word bullet.
    - What a stranger cannot tell: why the eleven relational words are printed twice in one file, and which copy wins if they drift. They match today. The judgment-word lists do not: the body's cold-reader section gives no list, and the pasted prompt gives "broken, worth, better, enough, larger-than", where "larger-than" also appears as "larger" in the relational list. Rule `r56` on this page says one fact lives in one home.
    - My guess: the duplication is deliberate so the prompt can be pasted standalone, and the drift is an oversight.
    - Non-blocking.

28. **"A sentence stays between 15 and 25 words, and one past 25 is a hit."**
    - Where: "The mechanical lints", style-and-register bullet.
    - What a stranger cannot tell: whether a sentence under 15 words is a hit. "Stays between 15 and 25" states a floor; "one past 25 is a hit" names only the ceiling. The document itself then runs on short sentences — "Run these before any reader." (5), "No artifact appears under two names." (6), "It repairs nothing." (3), "Four things change on this surface." (6) — so either the floor is not a rule, or the file breaks it on nearly every page. Rule `r09` says the sentence stating a rule is the first place to check that rule.
    - My guess: only the 25-word ceiling is enforced, and the floor is advisory.
    - Blocking — I cannot apply the check without knowing whether short sentences fail it.

29. **"The last one shows up as *big*, *huge*, *minor*, or *breakthrough*."**
    - Where: "The mechanical lints", grep fallback of the style bullet.
    - What a stranger cannot tell: how the examples match the rule they illustrate. The rule is "no adjective grades a result's size", but *minor* and *breakthrough* grade importance rather than size, and *breakthrough* is a noun. So I cannot tell whether the class is size, importance, or both.
    - My guess: the class is any word grading a result, and the rule's wording is narrower than its intent.
    - Non-blocking.

30. **"An undefined term the rest of the text leans on blocks."**
    - Where: "The cold reader", the blocking/non-blocking paragraph.
    - What a stranger cannot tell: on first pass the sentence garden-paths — "leans on blocks" reads as a unit before "blocks" resolves as the verb. I read it twice.
    - My guess: an undefined term that the rest of the text depends on is a blocking finding.
    - Non-blocking.

31. **"a fresh worker with the pack not loaded, reading the text from outside (`docs/spec-style.md`, the clean-agent split)"**
    - Where: "The cold reader", second paragraph.
    - What a stranger cannot tell: what a worker is, what "the pack not loaded" means operationally, and what "the clean-agent split" names. Three unexplained things in one parenthesis, and the citation points at a file I have no anchor for.
    - My guess: a separate agent session started without this skill file in its context.
    - Non-blocking.

32. **"the non-blocking ones queue for a taste call"**
    - Where: "The cold reader", end of the blocking/non-blocking paragraph.
    - What a stranger cannot tell: what a taste call is, who makes it, where the queue lives, and whether anything obliges the call to happen. This is the only stated destination for every non-blocking finding the loop produces.
    - My guess: a later judgment by the person, made outside this loop.
    - Non-blocking.

33. **The reader-prompt's five stop classes**
    - Where: "The reader-prompt — ready to paste", the fenced block, "Mark every place you stop. A stop is any one of these:".
    - What a stranger cannot tell: why the pasted prompt names five classes (undefined term, relational word, twice-read sentence, groundless claim, judgment word) when the rule block at the end of the same file names forty — including classes the prompt never mentions: a paragraph carrying two points, a sentence open to two readings, a pronoun with no antecedent, a thing named by its number, a coined word, a rare word, a fact stated twice, a heading whose body diverges. The document promises the cold reader covers "the classes no machine knows yet", and then hands that reader a list that omits most of them.
    - My guess: the five are a deliberate short list, and the rest are meant to be caught by the "a word the list above does not name … is a real find" escape clause at the bottom of the prompt.
    - Blocking — the loop's output is bounded by the prompt, and as written the prompt cannot produce the coverage the surrounding text claims for it.

34. **"That last instruction keeps the reader catching words the list does not know yet."**
    - Where: the paragraph after the fenced prompt.
    - What a stranger cannot tell: which instruction. The prompt's last block holds two instructions — ask the three questions at every relational word, and report unnamed classes as new finds. Only the second matches the sentence.
    - My guess: the "a word the list above does not name" sentence.
    - Non-blocking.

35. **"the auditor adds it by hand to the weak-word list before the next run"**
    - Where: same paragraph.
    - What a stranger cannot tell: who the auditor is, and how the auditor relates to the person, the author, the owner, the human, and the reader — six role names across one document, with no roster. Rule `r04` forbids one thing under two names, and I cannot tell here whether these are one thing or six.
    - My guess: the session running the audit, which is neither the cold reader nor the person.
    - Non-blocking.

36. **"the project's own copy of the list otherwise"**
    - Where: same paragraph, after "The list is `guardrails/weak-words.json` where the repository is on disk".
    - What a stranger cannot tell: where the project's own copy lives, what it is called, or what to do when no such copy exists — which will be the ordinary case in a project that has never run this skill. The sentence assigns a maintenance step to a file it does not locate.
    - My guess: a project creates one at a path of its choosing on first use.
    - Blocking — a required step with no findable target.

37. **"An invented definition reads clean to the next reader, while the text now states something no source backs."**
    - Where: "Fixes come from the source, never from invention", last line.
    - What a stranger cannot tell: what "reads clean" measures and who judges it — the same empty judgment the document bans. The tense also shifts mid-sentence ("reads" / "now states"), and "while" reads first as simultaneity and then as contrast; I reread it.
    - My guess: an invented definition produces no stop for the next reader, which hides the hole rather than closing it.
    - Non-blocking.

38. **"no coined metaphor does the talking"**
    - Where: "This file is held to the rules it lists", third bullet.
    - What a stranger cannot tell: how this sentence squares with itself, since "does the talking" is a figure standing where "carries the meaning" would say it plainly. The bullet claims the rule shows on every page while enacting the thing it names.
    - My guess: the intent is that no coined term carries meaning the plain word already carries.
    - Non-blocking.

39. **"`scripts/preshow-register-lint.py` is the register check that applies to it, and that run is clean"**
    - Where: "This file is held to the rules it lists", last paragraph.
    - What a stranger cannot tell: when that run happened, against which version of this file, what output it printed, and what "clean" counts as — zero hits, or hits below a threshold. It is a compliance claim about the document I am reading, and its ground sits nowhere on the page. Given the breaks I hit at entries 2, 13, 17 and 28, I cannot square the claim with the text.
    - My guess: the lint was run at some point before the file shipped and printed no hits.
    - Blocking — a self-certification with no date, no output, and no stated criterion, contradicted by the reading.

40. **"A change to this file re-runs that lint, and it runs one cold-reader loop on the changed section before it ships."**
    - Where: "This file is held to the rules it lists", final sentence.
    - What a stranger cannot tell: who acts. A change does not re-run anything, and "it" in the second clause has two candidate antecedents — the change and the file — neither of which can run a loop. This sits inside the one paragraph asserting the file obeys `r26` (named actor, active voice) and `r39` (unambiguous antecedent).
    - My guess: whoever edits the file re-runs the lint and runs one cold-reader loop before shipping.
    - Blocking — the sentence certifying compliance breaks two of the rules it certifies, so I cannot take the certification at face value.

41. **"These are every rule binding human-prose."**
    - Where: "The rules it holds a text to", first line of the generated block.
    - What a stranger cannot tell: whether the claim holds, because the identifiers skip. The block runs r01–r15, then r18, r20, r23, r25, r26, r27, r32, r33, r39, r41, r43, r44, r45, r46, r48, r49, r50, r52, r53, r54, r56, r57, r61, r62, r63, r64, r65, r66, r67, r68. Missing: r16, r17, r19, r21, r22, r24, r28, r29, r30, r31, r34, r35, r36, r37, r38, r40, r42, r47, r51, r55, r58, r59, r60 — twenty-three gaps. Either rules were retired, or rules exist that bind something other than human prose, or the printed set is incomplete. Nothing on the page says which. The sentence also reads awkwardly on first pass ("These are every rule").
    - My guess: the gaps are retired or non-prose rules, and the printed set is complete for prose.
    - Blocking — an explicit completeness claim that the visible evidence contradicts.

42. **Heading "The rules it holds a text to" over bodies that bind other things**
    - Where: the generated block's heading, and rules `r13`, `r18`, `r46`, `r48`, `r49`, `r52`, `r53`, `r57`.
    - What a stranger cannot tell: which of the forty rules apply to the text under audit. The heading, and the closing line "The rules above are the whole set a human-prose audit holds a text to", both promise rules for the audited text. But `r13` judges a reply to a person's remark, `r46` governs how a reply opens, `r48` bans offering work in chat, `r49` governs owning a mistake, `r52` governs a harness task-panel subject line, `r53` governs who drafts a text, `r57` governs review rounds, and `r18` governs commit messages. Applying `r46` or `r52` to a README is meaningless, and the page gives me no way to sort them.
    - My guess: the block prints every rule in the project's rule file, and only a subset binds an audited document — the subset is not marked.
    - Blocking — the heading promises one subject, the body carries several, and the reader is left to guess which rules the audit enforces.

43. **"This skill" / "this note" / "This SKILL.md" / "this file"**
    - Where: throughout — "Used on its own, this note is plain advice", "This skill checks whether", "This SKILL.md obeys the register below", "A change to this file".
    - What a stranger cannot tell: whether these name one thing or several. Rule `r04` on this page requires one name per thing, from first use onward.
    - My guess: all four name this same document.
    - Non-blocking.

44. **"The writer's page `docs/language-rules.md`" and "`docs/language-worked-example.md`"**
    - Where: the closing paragraph of the rules block.
    - What a stranger cannot tell: which repository these sit in. The anchoring sentence in "The mechanical lints" scopes itself to `guardrails/` and `scripts/` ("every path below is relative to that repository's root"), and these `docs/` paths sit outside that scope, as do `docs/spec-format.md` and `docs/spec-style.md` earlier.
    - My guess: the same live-spec repository.
    - Non-blocking.

45. **"One short document walked end to end against these rules, with the rule named at each fix, stands at `docs/language-worked-example.md`."**
    - Where: the closing paragraph of the rules block.
    - What a stranger cannot tell: on first pass the subject and verb are eighteen words apart, and "walked" reads as the main verb before "stands" turns up and reclaims the role. I read it twice.
    - My guess: a worked example document exists at that path.
    - Non-blocking.

---

Blocking entries: 2, 4, 8, 13, 19, 23, 24, 25, 28, 33, 36, 39, 40, 41, 42.
