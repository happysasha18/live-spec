# Blind read, 2026-07-28 — the language-rules reference, first read

The reader met this text with no context: one file, no repository access, no history. The brief gave
a real task to judge it against — write one page of documentation tomorrow and hold it to this
rulebook — and asked which rules could be applied, which could not, which contradict each other,
and whether an answer could be found when a writer needs it.

Reader: a working software engineer persona, clean context.
Text read: `docs/language-rules.md`, the generated rendering of the rule source, 1534 lines, 60 rules.
Applicable tomorrow: 30 of 60, and about 8 without an answer to which surface a documentation page is.

---

I read the whole file (1534 lines, 60 rule entries: r01–r62 with r22 folded and r28 absent with no note). Below is what happened.

## How I read it, and where I skimmed

I read the header and the two intro paragraphs (lines 1–8) closely, then r01 and r02 in full because I was learning the entry format. From r03 onward I read five fields per entry — **Rule**, **Reader test**, **Binds**, **Examples**, **Exceptions**, **Thresholds** — and skimmed four:

- **Stated at.** in every entry: a list of 5–15 file paths and line numbers. None of it changes a word I write. I skipped these after r02.
- **What catches it.** reach sentences: I read the verdict word (`held` / `partial` / `absent`) and skipped the reach description unless it contained a number or named a list I might need.
- **Law handed to it** blocks (r01, r10, r11, r12, r16, r17, r53, r56): 5–12 lines each restating the Rule line at length for a model. I read the first sentence and moved on.
- The r23 exception list (~70 semicolon-separated tokens): I read about 20, then scanned for shape.
- The four **Also binding** lists (lines 1350–1534): I read the human-prose one, saw it repeats titles already given, and scanned the other three for ids I had not met.
- All Russian text (r16's 15 example pairs, r59's 4 examples, the quoted owner remarks in r03, r59, r60, r61, r62). I do not read Russian. For r59, the Russian pairs are the entire example set.

---

## 1. THE STOPS

**"A rule binds as many surfaces as it governs and is written out once, under the fir…"** (line 7)
Three re-reads. "in that order" points back to a list in the previous sentence. The verb *bind* runs both directions in one paragraph: a rule binds surfaces, and "the rules that bind it" where *it* is a section. I needed one direction fixed and a named home for the ordering rule.

**"**Status.** held, armed at session-stop-hook, manual."** (line 19)
Four vocabulary items in one line — `held`, `stated-only`, `armed at`, and the arm names (`session-stop-hook`, `manual`, `nowhere`, `pre-push`, `pre-commit`, `session-prompt-hook`) — none defined anywhere in the file. I guessed `held` means enforced and `stated-only` means written down with nothing checking it. r47 (line 1398) reads **"stated-only, armed at session-prompt-hook"**, which broke the guess. I needed a four-line legend at the top.

**`pattern` / `model` / `person` — `partial` vs `held` vs `absent`**
Same problem, applied to three catchers per entry, 180 times. I guessed `partial` means the checker covers some of the class. Never stated.

**"The pre-show lint's pattern list grows by nobody's duty, retracted 2026-07-17 at sc…"** (line 31)
Could not parse "grows by nobody's duty." Guessed: no one is assigned to extend it. I needed a plain clause.

**"**person** — absent. Reads: whether the relation between the two nouns is carried i…"** (line 93)
Could not parse. The sentence is "whether X is carried is a short human read, or a model read for volume." Two verbs stacked, and "for volume" is unexplained. The field is also marked `absent` while describing a person doing the reading.

**"**Exceptions.** a criterion counted in the recorded baseline, which passes while the…"** (line 189) with `criterion_baseline_over_cap = 469`
I worked out that 469 existing sentences break the word cap and are grandfathered by count. I could not tell which 469, and for a page I write tomorrow the exception is unusable. I needed the rule stated as "new text has no exception."

**"**Personal layer.** The reader's own layer replaces the rule's `exceptions` with no…"** (line 241)
This field appears once in the file, in r10, and is never defined. It reverses the exception printed four lines above it. I could not tell which of the two is in force for my page. I needed a statement of which layer applies.

**"**Exceptions.** a code anchor; a filename; JSON; CI; HTML; CSS; RFC; API; URL; UI; …"** (line 439)
I stopped partway because I could not see the membership rule. `JSON` and `API` read as acronyms; `DOWN`, `WAITS`, `STANDS`, `CONVERGES`, `EXPLICIT`, `CONSERVATIVE` do not. The membership rule arrives ten lines later at line 449. I needed it before the list.

**"reds"** as a verb (line 5, line 471, line 417, and elsewhere)
Guessed: marks as failing. This is a project word used with no gloss on first appearance. r16's own example table gives «краснеет» → «проваливает проверку», the same word, listed as something to replace.

**"This entry and r25 are one rule split by surface. scripts/spec-style-lint.py reds r…"** (line 471)
Read twice. On the second pass I understood that a checker enforces r24 over territory r25 owns — meaning the file tells me the rule as written and the rule as enforced differ. I needed to know which one I will be held to.

**"The name this rule once carried was itself a minted metaphor; the owner's recorded …"** (line 719)
Unusable. It refers to a name it never gives and a verdict it never quotes.

**"Law handed to it: a fresh agent with the pack not loaded, judging the whole documen…"** (line 909)
A sentence with no main verb. Three undefined terms in one line: "the pack", "hash-pinned rubric", "seeded self-test canary". Skimmed.

**"**pattern** — partial. Lives at docs/language-defects.md:200."** (line 1026)
Re-read: a pattern checker whose home is a Markdown file. I could not tell whether a script exists.

**"**pattern** — absent. Lives at templates/KILL_LIST.template.md."** (line 1342) and **"A ban written down and not scanned for did not hold; the scanner ended it."** (line 1348)
`absent` and `Lives at` in one bullet. Then the Notes say a scanner ended the problem while the same entry says the repository ships "no kill list and no scanner."

**"### r62 — a text carries one interpretation, a visible cause, and its unstated alte…"** (line 1080)
I stopped at this heading trying to find the banned thing. Every other heading names a defect ("a number standing with no ground"). r62 and r58 name the desired state instead. I re-read both entries to work out what a violation looks like.

**"The count-shaped, pointer-shaped, and position-shaped half of this class is held se…"** (line 177, echoed at line 1005)
I had to hold r07 and r58 side by side, 800 lines apart, to see where one ends and the other starts.

**The 62 headings themselves.**
r11 says an internal code trails and never leads. Every heading in the file opens with `r01`, `r02`, … I stopped to decide whether r11 covers headings, and could not decide. r09 ("A text does not ship while it contradicts a rule it states") makes that decision matter.

---

## 2. RULES I COULD NOT APPLY

The largest blocker sits above the rules. The six surfaces — spec-body, human-prose, chat, artifact, commit, worker-brief — are the axis the entire file is organized on, and none of them is defined. **A documentation page: is it human-prose, or artifact, or both?** Different answers change which of 60 rules bind me and which sentence-length numbers apply. I would have to ask this before using anything below.

Then, per rule:

> **r33** — "**Exceptions.** a slot filled by one of the recorded reference cues; a line recorded as a `[GAP: ...]`."
The 20 reference cues are counted at line 649 and never listed. Ask: give me the 20 cues.

> **r35** — "**Thresholds.** max_aside_chars = 25; baseline_hits = 120." and "an aside past 25 characters opening on one of 21 gloss-opening words"
The 21 words are never given. Ask: which 21 words open a gloss?

> **r36** — "over a closing clause of four or more words opening on one of 22 determiners, carrying none of 22 finite markers, and resting on a participle"
Neither list of 22 is given. Ask: both lists.

> **r30** — "A rule is stated in the declarative present tense" / Notes: "The sixteen-verb set lives only in the script; no prose home names it."
I can hold the rule by ear; I cannot predict the checker. Ask: the sixteen verbs.

> **r46** — "**Thresholds.** reply_chars_above_which_a_lead_is_required = 550." / Notes: "The threshold and the three lead signals live only in the script."
Ask: what are the three lead signals? Without them I cannot tell whether my opening block passes.

> **r55** — "A rewrite leaves anchors, structural marker lines, headings, and the literal classes standing verbatim"
"the literal classes" and "structural marker lines" are named and never listed. Ask: both.

> **r10** — "**Exceptions.** a contrast between two things that both genuinely exist…" against "**Personal layer.** The reader's own layer replaces the rule's `exceptions` with nothing."
Ask: which layer is in force for a documentation page.

> **r53** — "Prose a human will read is drafted by a fresh writer with no package rules loaded, working from a plain brief that … lists the register laws."
I have now read the rulebook, so by this rule I am disqualified from drafting the page I was assigned. Ask: who drafts, and which subset is "the register laws"?

> **r54** — "read by fresh readers who carry no project context, until two consecutive reads return zero blocking findings."
"blocking finding" is never defined, and I have no fresh readers. Ask: what makes a finding blocking, and who are the readers?

> **r56** — "One fact lives in one home, and every other place points at that home rather than restating it."
To obey this I need to know where every fact already lives. Ask: is there a registry of homes?

> **r45** — "a long flat run of peer items is gathered under headed parents."
No number for "long". Ask: at how many peers?

> **r38** — "**Exceptions.** a rhetorical triad, which carries no list." with "**person** — partial. Reads: telling a genuine enumeration from a rhetorical triad is a meaning call."
The exception has no test. Ask: give me one passing triad and one failing one.

> **r32** — Examples are the bare words `broken`, `worth`, `better`, `enough`, `larger-than`.
Ask: is every occurrence of "better" a judgment, or only a verdict-shaped one?

> **r20** — "reads like a native technical writer" / "**person** — partial. Reads: a reader hears the register."
No measure other than an ear I do not have. Ask: two passing sentences and two failing ones.

> **r62** — "A reader reaches one interpretation of a sentence, sees what causes what, and can tell what the text leaves out." Notes: "He asks whether these three can be turned into numbers; the question stands open."
The entry says its own measure does not exist.

> **r50** — "Dense working notes are marked so the reader can skip them" / Notes: "The host's mark for a working note is «(себе)»."
The mark is Cyrillic; r18 requires documents in English. Ask: what is the mark on an English page?

> **r08** — three numbers (`criterion_max_words = 35`, `prose_flag_above_words = 25`, `prose_target_band = 15 to 25`) and a surface question I cannot answer.
Ask: for a documentation page, which number binds?

---

## 3. RULES THAT CONTRADICT EACH OTHER

**r24 against r25 — opposite verdicts on the word "you".**
> r24: "A normative sentence writes in the third person and binds a named actor."
> r25: "Explanatory text addresses the reader as `you` for what a person does, and names the component for what software does."

Both entries admit it: "This entry and r25 are one rule split by surface" (lines 471 and 1225), and both add "scripts/spec-style-lint.py reds r25's surface today, because its reach is not scoped to the spec body." So the sentence "You run the migration before the deploy" passes r25 and fails r24, and the checker in the tree fails it. This is the conflict most likely to hit a documentation page.

**r10's package exception against r10's personal layer — opposite verdicts on one sentence.**
> "**Exceptions.** a contrast between two things that both genuinely exist and are both live for the reader."
> "**Personal layer.** The reader's own layer replaces the rule's `exceptions` with nothing."

**r33 as stated against r33 as enforced.** The entry states this itself at line 655:
> "docs/spec-format.md:25 calls an unfilled slot a blocking finding while the script excuses it on any digit, so the excusing rule is looser than the stated rule."

"Retry a few times within 5 seconds" fails the rule and passes the checker.

**r58 against r08 and r60 — opposite verdicts on a naming sentence.**
> r58: "A text that points at part of a set names that part by what its members are, and keeps that name in every later sentence."
> r08: "a sentence past the word cap is rewritten or split." (`prose_flag_above_words = 25`)

r58's own example expands `**Case: the three legs**` into a 12-word member string. A set of eight or ten members cannot be named inside a sentence that stays under 25 words. r60's "A sentence carries one clause of subordination at most" pushes the same way.

**r14 against r51 — opposite verdicts on a closing recap line.**
> r14: "a sentence that only performs a stance, prefaces, restates, softens, or ceremonially opens or closes is cut before sending."
> r51: "A question that went unanswered during the work, or an answer buried inside a long reply, is recapped in one short line at the message's end."

A recap of a buried answer restates what the message already carries. Both bind chat.

**r41 against r61 — opposite verdicts on r15's example block.**
> r41: "An example earns its place by resolving an ambiguity, uses realistic values, and one per rule is enough."
> r61: "A list of examples enters as evidence beneath the class."

r15 carries 17 examples, r16 carries 15, r29 carries 12. Under r41 all but one of each is cut.

---

## 4. RULES I COULD APPLY IMMEDIATELY

r01, r02, r03, r04, r05, r09, r11, r15, r19, r21, r23, r26, r27, r29, r30, r31, r34, r35, r37, r39, r40, r41, r42, r43, r44, r49, r52, r59, r60, and r10 in its strict form.

Thirty of sixty. The eight I could hold with no judgment at all, because they ship a word list or a shape: r02, r10, r11, r15, r23, r29, r30, r42.

---

## 5. THE SHAPE

There is no table of contents, no index, and no keyword list. The handles are the 60 headings, each written as a prose description of a defect ("a relational word leaving its slot empty", "a subject that cannot perform its verb"). To look something up I have to guess the author's phrasing for a defect I have not yet named. Ordering is by id, and ids record when a rule was written, so related rules sit far apart: sentence shape lives at r08, r36, r39, r44 and r60, spread over 850 lines.

I fell back on grep. What follows is what happened with grep available.

**"Can I use the second person?"** — Searched `you`. Landed on r25 under human-prose. Read it, accepted the answer, then hit r24 under spec-body 750 lines earlier with the opposite instruction. I only connected them because r24's Notes say they are one rule. Roughly four minutes, three passes. I do not have the whole answer: the file says the checker enforces the spec-body form over the human-prose surface, and does not say which verdict I will be held to.

**"How long may a sentence be?"** — Searched `words`. r08's heading carries the phrase "running past its word cap", so this landed fast, under a minute. The Thresholds block gives three numbers. Then r60 adds `max_subordinate_clauses = 1` and its Notes say "The word numbers come from r08 and are not repeated here." I found the second half only because r60 pointed back. No single place gives the whole answer, and I still cannot pick between 25 and 35 without knowing my surface.

**"May I define a term in the middle of a sentence?"** — The slowest, about eight minutes. Three entries answer, and they answer differently by location: r01 requires a plain gloss at a term's first use ("picture first, term second"), r35 bans a gloss inside a criterion past 25 characters, r21 puts the definition in the glossary. Reconciled: gloss in prose, glossary entry in a spec, no in-place gloss in a criterion. I am not confident I have all of it — after writing that down I found r43, which requires grounding an abstraction with "a two- or three-item example at its first use", a fourth position on the same question.

Without grep, all three questions mean scanning 60 prose headings.

---

## 6. THE DUPLICATES

- **r24 and r25** — stated in the file: "This entry and r25 are one rule split by surface."
- **r05 and r59** — r59's Notes: "This widens r05 from verbs to any predicate." The reader tests are the same question in different words: "Can the thing this sentence names as its subject actually do what the verb says?" against "Can the thing named as the subject perform this verb, or hold this quality?"
- **r07 and r58** — both Notes say they are two halves of one class.
- **r26 and r42** — the identical example appears in both: "`the verification of the claim occurs` → `the suite verifies the claim`" (lines 485 and 828).
- **r15 and r29** — `of course` appears in both example lists with the same repair, `delete`.
- **r12, r13, r14 and r15** — r14's Notes: "This law governs the classes r12, r13, and r15." Four entries under one law. r49's person field says the same law already reaches r49.
- **r01 and r21** — r01 requires a term to hold "one glossary entry"; r21 requires "one one-sentence glossary entry" for every domain noun. r01 already absorbed r22 on this ground.
- **r02, r16 and r17** — one class (project vocabulary reaching a reader) split three ways by the form the word takes: coined English, loan translation, transliteration.
- **r08, r38 and r60** — the same list instruction three times. r08: "a set of parts is written as a list with one part per line." r38: "a set of parallel parts is written as a bulleted or numbered list under a one-line lead, one part per line." r60: "An enumeration of members is written as a list of short clauses."

Separately: every rule title is printed between two and five times — once as the entry, once in each "Also binding" list. r01's title appears five times.

---

## Answers

**How many could I hold tomorrow, out of the total?** Thirty of sixty, and that number assumes someone tells me whether a documentation page is human-prose, artifact, or both. Without that answer, the count drops to the rules that bind every surface — around eight. Of the thirty, eight run off a word list and need no judgment; the other twenty-two need my own reading, and I would apply them unevenly.

**What I would cut.** The four largest fields in every entry, which together are most of the file's length: **Stated at.** (roughly 600 file-path references, none of which change a word I write), **What catches it.** with its script reach descriptions, the verbatim **Law handed to it** prompt blocks, and the historical half of **Notes.** (folding dates, retracted duties, what a script used to do, which file still states an old form). Those belong to whoever maintains the checkers. I would also cut the six "Also binding" lists, which restate 60 titles four more times.

**What I would add.** A legend for `held` / `stated-only` / `armed at` / `partial` / `absent`, at the top. A one-line definition of each of the six surfaces, with an example document for each. The lists that are named and never given: the 20 reference cues, the 21 gloss-opening words, the 16 spec verbs, the three lead signals, the literal classes, the structural marker lines. A verdict on r24 against r25 for documentation. A statement of which layer is in force. And an index by question — length, person, terms, lists, tense, examples, structure — pointing at rule ids, since the headings are unsearchable by a writer who has not yet met the defect.

**One page for a new colleague.** No existing page-sized chunk works, because the ordering is by id and the sentence-shape rules are scattered. The closest contiguous run is **r26 through r45 under spec-body** — actor, opener, tense, judgment, relational words, lists, pronouns, conditionals, examples, nominalizations, abstraction, paragraph, structure. Most of those entries carry an example pair, most are applicable on sight, and they cover the mistakes a person actually makes in a documentation page. I would hand that run with r10 and r15 stapled on for their word lists.
