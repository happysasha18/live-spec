# Cold read of `skills/text-audit/SKILL.md`, 2026-08-05

Read on the strong tier (Opus 5, 1M context), in a session holding no history of this text: no
earlier draft, no project background, no author's intent beyond the page.

Read once, straight through: `skills/text-audit/references/reader-prompt.md` (the brief this reading
runs under), then the text itself, `skills/text-audit/SKILL.md`. Nothing else was opened before the
findings below were fixed. After the reading closed, the first 45 lines of
`docs/language-reads/2026-07-29-read28-text-audit-skill.md` were opened for the record's shape alone.

Stops: 30 — 8 blocking

---

1. **"Part of the **live-spec pack**."**
   - Where: the blockquote under the title `# text-audit — read a text as a stranger, fix where they stop`.
   - What a stranger cannot tell: what a pack is, and what belonging to one obliges this skill to do.
     The closing section lists eleven names under "The pack this skill belongs to", but no sentence
     says what the word names or what changes when the pack is absent.
   - My guess: a set of eleven skill files shipped together from one repository.
   - Non-blocking.

2. **"Four scopes settle a setting there, in this order: the session's live word, then the host profile, then the personal profile, then the package default."**
   - Where: the same blockquote.
   - What a stranger cannot tell: which settings this governs, and what three of the four scopes are.
     "The session's live word" is the hardest — a live word is not a thing I can picture. Nothing later
     in the file turns on any of the four, so I could not test my guess against anything.
   - My guess: a precedence order for configuration values, defined in `live-spec-base`, and untouched
     by anyone running this audit.
   - Non-blocking.

3. **"Those readers found new blocking terms on every pass, and the terms already repaired stayed repaired."**
   - Where: the paragraph opening "Those readers found new blocking terms…".
   - What a stranger cannot tell: which readers, on which text, over how many passes, and where that
     result is written down. Everything nearby carries a file citation; this claim carries none. It also
     switches vocabulary — the rest of the file counts blocking *findings*, and this sentence counts
     blocking *terms*.
   - My guess: the same cold readers described in the previous paragraph, run over `PRODUCT_SPEC.md`
     sections, and "terms" is a loose synonym for "findings".
   - Non-blocking.

4. **"`docs/language-defects.md` holds a narrower list — the places only one of the two readers found, which block nothing."**
   - Where: the paragraph opening "Those readers found new blocking terms…".
   - What a stranger cannot tell: where to file a blocking stop that only one reader found. This
     sentence says a single-reader stop blocks nothing. Step 3 of "The loop" tells me to order the
     merged list as "the stops found by both first, then the remaining blocking stops, then the
     non-blocking ones" — an ordering that only makes sense if a single-reader stop can block. The two
     sentences cannot both be followed.
   - My guess: the sentence here is the loose one, and a stop found by one reader can block; but I would
     have filed a single-reader blocking stop as non-blocking on the strength of this line.
   - **Blocking.**

5. **"Three roles run through this skill"**
   - Where: opening of "The roles and the words this skill uses".
   - What a stranger cannot tell: which three, when the bullet list below it holds five entries at the
     same level — the auditor, the cold reader, the prompted reader, the unprompted reader, the person.
     The cold reader's own bullet says the role is filled twice per round, which resolves it, but only
     after I had already counted five against a stated three and gone back.
   - My guess: the three are the auditor, the cold reader, and the person; the prompted and unprompted
     readers are the two fillers of the cold-reader role, not roles of their own.
   - Non-blocking.

6. **"One person may hold the auditor role and own the text, and the cold reader is never either of them."**
   - Where: opening of "The roles and the words this skill uses".
   - What a stranger cannot tell: what "them" points at. The sentence's nearest plural is "the auditor
     role and the text", and a reader cannot be a text. The intended pair is presumably two people, but
     only one person has been named.
   - My guess: the cold reader is never the auditor and never the text's owner.
   - Non-blocking.

7. **"The register carries the word cap: 25 words for a human-prose sentence, and 35 for a spec-body criterion (rule `r08`)."**
   - Where: the paragraph defining "register".
   - What a stranger cannot tell: what happens at 26 words, and where the second number comes from. The
     mechanical-lints section later says a human-prose sentence "aims at the band of 15 to 25 words",
     and 15 appears nowhere else — I cannot tell whether a 12-word sentence is a hit, a miss, or fine.
     `r08` names a rule by its number only, so I must leave the page to learn what it says.
   - My guess: 25 is the hard cap and 15 is a soft floor that nothing enforces.
   - Non-blocking.

8. **"## When it fires"**
   - Where: the section heading.
   - What a stranger cannot tell: what fires, and what does the firing. Nothing on the page has been
     described as an event or a trigger up to this point; the skill has been described as advice a
     person applies.
   - My guess: "when to load and run this skill".
   - Non-blocking.

9. **"mark a passage both readers stopped on as found by both. Those stops are the strongest"**
   - Where: step 3 of "The loop".
   - What a stranger cannot tell: strongest by what measure, and what the strength buys beyond leading
     the list. A later section gives the measure — those stops survived refutation — but at the point
     where I am told to act on it, the word carries no test.
   - My guess: "most likely to be real", and it changes only the ordering, not the repair.
   - Non-blocking.

10. **"On 2026-08-05 a separate review of one repaired skill found four defects inside the repair's own new sections. One was a false claim about where every path resolves."**
    - Where: step 5 of "The loop", under "A repair writes text nobody has read".
    - What a stranger cannot tell: which skill, which review, and where either is written down. The
      example is the whole ground for the rule that round two earns the closing, and I cannot reach it.
      The detail also unsettles the page I am on, which opens with a claim about where every path in it
      resolves; I have no way to tell whether that is the same claim.
    - My guess: some other skill in the same pack, reviewed the same week, with no record I am meant to
      open.
    - Non-blocking.

11. **"A section-sized run puts one definition and a handful of sentences in front of a reader."**
    - Where: the paragraph closing "The loop".
    - What a stranger cannot tell: how much text a section-sized run is. "One definition and a handful"
      does not square with the next section, which sets the working size at ten requirements and about
      250 lines. I cannot tell whether these describe the same run at two scales or two different runs.
    - My guess: two different scales — a single edited paragraph versus a spec batch.
    - Non-blocking.

12. **"**The requirement-shape lint applies here.** It is the mechanical lint only a spec section runs"**
    - Where: opening of the four points under "Running it on a spec section".
    - What a stranger cannot tell: which lints to skip on a README. This sentence says one lint is
      spec-only. "The mechanical lints" says "Three of these scripts read a spec section and nothing
      else", naming `check-vocabulary.py`, `check-weak-words.py`, and `check-requirement-shape.py`.
      Following the first sentence I would run the vocabulary and weak-word scripts on a README and take
      their exit 1 as a failure of the text.
    - My guess: three scripts are spec-only, and "only a spec section runs" means only this one is
      *listed* under the spec section — but I had to choose between two flat statements.
    - **Blocking.**

13. **"`bash guardrails/check-freeze.sh` — the three guarded documents match the frozen baseline"**
    - Where: the structure checks under "Running it on a spec section".
    - What a stranger cannot tell: which three documents, and what a frozen baseline is. Both arrive
      here and are explained two paragraphs later, after the census, and the paragraph that explains the
      baseline never says the phrase "guarded document" again.
    - My guess: `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, and `TEST_MATRIX.md`, read off the freeze command
      further down.
    - Non-blocking.

14. **"The structure checks, third in the list, are four commands of their own"**
    - Where: the paragraph introducing the four post-repair checks.
    - What a stranger cannot tell: which item is third until they have read the list that this sentence
      introduces. The sentence points forward by position instead of by name.
    - My guess: the third bullet below, and I confirmed it by counting after reading.
    - Non-blocking.

15. **"**The build test is defined, and its first run is still owed.** It measures the work once Step 5's two clean rounds close the audit."**
    - Where: the closing paragraph of "Running it on a spec section".
    - What a stranger cannot tell: what "the work" is that gets measured, and who owes the run. The
      paragraph then explains the build test measures whether the repaired text still supports building,
      which is not "the work" of the audit. It also runs six claims together — the definition, the
      timing, the method, the target count, the plan citation, and the absence of any run.
    - My guess: "the work" means the repair, and nobody in particular owes the run.
    - Non-blocking.

16. **"A run over ten documents met four such refusals on 2026-08-05 and read them as coverage."**
    - Where: the paragraph closing "Three of these scripts read a spec section and nothing else".
    - What a stranger cannot tell: whether that run did the right thing or the wrong thing. The sentence
      states an event with no verdict, at the end of a passage that has just told me to record the
      refusal and move on. Read one way it is a warning: a past run mistook a refusal for a clean pass.
      Read the other way it is a precedent I should follow.
    - My guess: a warning — but the sentence gave me no word to settle it, and the two readings send me
      opposite ways.
    - **Blocking.**

17. **"No sentence names a thing by denying its neighbour"**
    - Where: the "Style and register" bullet under "The mechanical lints".
    - What a stranger cannot tell: what shape of sentence this forbids. I am told, four lines later, to
      "read for those four classes by hand" when the scripts are absent, so I have to be able to apply
      this one. The fourth class gets four example words. This one gets none, and I cannot manufacture
      an instance I am confident the rule catches.
    - My guess: something about defining a thing by what it is not, but I could not say whether it bans
      "a spec, not a plan", or bans comparison to a neighbouring item, or bans negation generally.
    - **Blocking.**

18. **"which prints 38 kinds of place to stop"**
    - Where: opening of "The cold reader".
    - What a stranger cannot tell: nothing is unclear — the number is wrong. The file it points at,
      `references/reader-prompt.md`, carries 39 bullets in its stop list, and its own opening paragraph
      says it "prints every rule bound to human prose whose owner is a skill: 39 of the 66 rules the
      rule home carries". I counted the bullets to check, and got 39.
    - My guess: the count went stale when a rule was added to the prompt and this sentence was not
      swept. I read the prompt's own figure as the true one.
    - **Blocking.**

19. **"Both passes run on every audit, whatever the budget allows."**
    - Where: opening of "The cold reader".
    - What a stranger cannot tell: what to do when the budget does not allow both. Read plainly, the
      sentence says the budget never excuses dropping a pass, which makes "whatever the budget allows"
      an odd thing to say at all — it names a constraint and then ignores it.
    - My guess: both passes are mandatory and cost is not grounds for skipping one.
    - Non-blocking.

20. **"About thirty passages came back from both readers. Those are the strongest stops, and every one of them survived refutation."**
    - Where: the paragraph closing "What each reader is handed, and what each one brings back".
    - What a stranger cannot tell: what refutation is, who performs it, and when. The word arrives here
      as an established step. "The loop" has five numbered steps and none of them is a refutation pass;
      the next section says stops "fall away when a second worker is told to knock them down", which
      describes an act nobody was ever instructed to perform. Following the five steps I would repair
      every blocking stop as it came back, including the 40% the file says get thrown out.
    - My guess: an unwritten sixth step in which a third session argues against each stop before the
      auditor repairs it. I could not tell whether I was meant to run it.
    - **Blocking.**

21. **"an image with no referent"**
    - Where: the list of what the prompted reader alone caught.
    - What a stranger cannot tell: what an image is in a text, and what a referent is here. The three
      items beside it are sentence mechanics I recognize; this one I cannot picture.
    - My guess: a metaphor whose subject is never named.
    - Non-blocking.

22. **"the prompted reader reported 227 stops. 135 survived refutation and 36 blocked."**
    - Where: "What the pass costs".
    - What a stranger cannot tell: where these figures are recorded. Every other measurement in this file
      that matters carries a file path; this section carries none, over two paragraphs and thirteen
      numbers. The three documents are never named either.
    - My guess: a measurement run the same week, written up somewhere under `docs/`.
    - Non-blocking.

23. **"One reading by the unprompted reader brings back about 26 stops per document, and one reading by the prompted reader about 45."**
    - Where: "What the pass costs".
    - What a stranger cannot tell: how these two numbers come from the ones four lines above. Over three
      documents, 128 unprompted stops is about 43 per document, not 26; 227 prompted stops is about 76,
      not 45. Taking surviving stops instead gets 45 for the prompted reader exactly (135 ÷ 3) but 29 for
      the unprompted one, still not 26. No reading of the paragraph makes both figures come out.
    - My guess: the per-document figures came from a different run than the totals above them, and were
      never reconciled. I could not decide which pair to plan against.
    - **Blocking.**

24. **"The two together bring back about 71, so the work of judging them nearly triples."**
    - Where: "What the pass costs".
    - What a stranger cannot tell: triples relative to what. Against the prompted reader alone (45), 71
      is 1.6 times, not nearly triple. Against the unprompted reader alone (26) it is 2.7 times. The
      sentence needs the smaller reader as its baseline to be true, and it does not say so.
    - My guess: the baseline is the unprompted reader alone — the cheaper of the two — so the claim
      holds only for someone who would otherwise have run that one.
    - **Blocking.**

25. **"A second measurement on the same day read a publish candidate with three readers."**
    - Where: "What the pass costs".
    - What a stranger cannot tell: what a publish candidate is, and how three readers square with the
      rule stated twice already that a round is two readers and both run every time. The later phrase
      "the unprompted readers" is plural, which hints at two of them, but no sentence says so.
    - My guess: a text about to be published, read by one prompted and two unprompted readers.
    - Non-blocking.

26. **"That run reproduced the split."**
    - Where: "What the pass costs".
    - What a stranger cannot tell: which split. Two candidates sit in the same paragraph — the division
      of labour between the two kinds of reader, and the proportion of stops thrown out.
    - My guess: the division of labour, since the next two sentences list what each reader alone caught.
    - Non-blocking.

27. **"They also caught a sample path that resolves from one folder alone, and a dated file written into the reader's repository."**
    - Where: "What the pass costs".
    - What a stranger cannot tell: why either is a defect. A path that resolves from one folder sounds
      like a working path; a dated file in a repository sounds like a record. Both are named as faults
      with no word saying what goes wrong.
    - My guess: the path only works if the reader stands in one particular directory, and the file was
      written into someone else's repository without asking.
    - Non-blocking.

28. **"runs the census comparison over every live document"**
    - Where: the paragraph on the push check, under "Running it on a spec section".
    - What a stranger cannot tell: what makes a document live. Nothing on the page divides documents
      into live and otherwise.
    - My guess: every document with a row in `guardrails/rule-census.json`.
    - Non-blocking.

29. **"`guardrails/rule-census.json` records this file at zero findings"**
    - Where: "This skill is held to the rules it lists".
    - What a stranger cannot tell: whether that is still true, and what to do on finding it false. The
      earlier census paragraph already stated the rule that a count above the record fails, so this
      passage restates it against one file. Nothing tells me what happens if my own read of this file
      raises the count.
    - My guess: the census counts only lint findings, not cold-reader stops, so the record survives a
      reading like this one.
    - Non-blocking.

30. **"The loop closes when both readers of a round return zero blocking findings, twice in a row."**
    - Where: "The cold reader".
    - What a stranger cannot tell: nothing new — this is the third statement of the same rule, after
      "The loop" opens with it and step 5 restates it. On the third pass I stopped to check whether the
      wordings differed and carried a distinction.
    - My guess: they are the same rule stated three times, with no difference intended.
    - Non-blocking.

---

## Relational words, and which slot stayed empty

- "a **narrower** list" (entry 4) — narrower than what. Answered by inference: narrower than the
  reading record.
- "Those stops are the **strongest**" (entry 9) — by what measure. Unanswered where it stands;
  answered thirty lines later.
- "nearly **triples**" (entry 24) — relative to what. Unanswered, and the two available baselines give
  different verdicts.
- "A **higher** count is better" (the build test) — than what. Unanswered; no count has ever been taken,
  so there is no prior figure to be higher than.
- "the working size" (ten requirements) — working for whom, judged how. Answered: a fresh reader holds
  that much, and a repair inside those lines cannot break a distant requirement.

## A kind not on the printed list

One stop does not fit any of the 39 kinds the prompt names, and it produced the strongest blocking
finding here (entry 20). The kind is: **a step named only in the evidence, and absent from the
procedure.** Refutation is described as something that happened — 40% of stops were thrown out by a
second worker who was told to knock them down — but the five numbered steps never tell anyone to run
it, and no role in the skill's role list performs it. A reader following the procedure produces a
different process from the one the numbers were measured on. This is not "a claim resting on ground the
reader cannot reach": the ground is stated plainly on the page. It is the procedure that is missing a
step its own evidence assumes.
