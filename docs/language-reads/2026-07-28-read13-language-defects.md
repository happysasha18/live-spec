# Blind read, 2026-07-28 — the language-defects document, read thirteen

The reader met this text with no context: one file, no repository access, no history of the
document's earlier rounds. The brief asked for every place the reader stopped, sorted into stops
that blocked the reader and stops the reader noticed and read past.

Reader: a working software engineer persona, clean context.
Text read: `docs/language-defects.md` after round fifteen answered the four questions read twelve
left standing.
Stops: 28 — 8 blocking, 20 non-blocking.

The nine readings of this page, oldest first, by blocking stops: 11, 8, 12, 6, 5, 5, 6, 5, 8. This
is the reading that closed the loop for the night: the count oscillates between five and twelve and
does not approach zero, and several of this reading's eight sit on text the previous round added.

---

I read it once, straight through. Report below.

---

## Stops

**1.** "Seven words carry the weight on this page, each naming its own thing, and all sev…"

Seven get definitions. The word *stop* runs through the whole page — it carries the reading records, the blocking test, and the rule-birth procedure — and never gets a defining sentence. I assembled a meaning from the reading prompt (line 82) and from "A stop blocks when…" (line 200). I needed *stop* defined alongside the seven.

**2.** "A **surface** is a kind of text rather than a file, so one file carries several"

Six surface names arrive; the definitions live in another file. Later the page says every rule binds surfaces, and that thirty of sixty rules depend on knowing which surface a documentation page is. I could not classify any text, so I could not apply any surface-bound rule. I needed the six defined here, or the page to stop leaning on them.

**3.** "An entry carries fifteen parts: ten on every entry, and five more where the rule h…"

I stopped to count the three bullets and check 5+5+5. The bullets are headed "the writer's five" and "the maintainer's five", so the arithmetic works, and I still had to do it. I needed the ten split named as 5+5 in the sentence that announces fifteen.

**4.** "The first four reach the writer, and the override is printed on both pages."

"reach the writer" — I guessed it means "are printed on the writer's page". About 80% sure. I needed the same verb used as the neighbouring sentences use ("printed on").

**5.** "The source carries 53 rules and its highest identifier is `r62`, so nine stand ret…"

I did 62 − 53 = 9 and then noticed the arithmetic only holds if identifiers run from r01 with no gaps ever. That assumption is never stated. I needed it said.

**6.** "seven went in the fold recorded below"

*Fold* arrives here with no explanation; I read to line 196 to learn that twelve entries became five. The same word appears at line 324 — "recorded beside the date it was folded in" — where it means a pattern was added to a list. Two operations, one word. I needed one of them renamed.

**7.** "A cold reader is given the text alone: no repository, no history of earlier drafts…"

Defined by three absences. The page later names `r10`, *a thing named by denying its neighbour*, as a rule binding every surface. I flagged this as a possible instance and read on, at low confidence.

**8.** "A rule enters this project when the place that produced that stop produces it agai…"

*Source* was defined thirty lines earlier as one specific file, `guardrails/language-rules.json`. Here it means the origin of a wording. A third sense sits in the field `sources` — "the files that stated the rule in prose before the source existed". I had to hold three senses of one defined word. I needed the origin sense to carry a different name.

**9.** "The last section below holds this page's own readings, which are still going on."

I scrolled to the end and found two sections after it. It is the last subsection of *The readings that produced the rules*. I needed "the last subsection of this section".

**10.** "Four of the ten — home, seat, law, and tier — turn up again on this page, each def…"

*home* is defined above this line. *seat*, *law*, and *tier* get their definitions at lines 228–232, roughly 110 lines later, and all three are used before that — *law* heavily, inside the owner's reading and the rule descriptions. The claim "each defined where it is used" did not hold for me on a straight read. I needed the three defined at first use, or the claim narrowed.

**11.** 'used "red" as a verb meaning to report something as a failure'

I guessed: a test or a gate marking a result as failed. About 85% sure. The page also says ten nouns were involved and shows four; I could not check the class against the other six.

**12.** "One sentence stated the rule that a criterion carries one trigger and one response…"

"broke it twice over" pointed at the one-trigger-one-response rule. The first break described is a respelled Russian word, which the page files under `r02`. The second break — an obligation standing in the response slot — matches the stated rule. I could not tell whether the sentence broke one rule twice or two rules once each. I needed each break named with its rule.

**13.** "The surfaces were the axis the whole page was organized on, and the page defined n…"

This sits after the list of four surface-independent rules, and reads as the claim the paragraph was built to support. On first pass I took it as a new topic and re-read the paragraph. I needed it at the paragraph's head.

**14.** "The writer's page carries both today, defining all six surfaces and placing a docu…"

"both" — I went back two sentences to resolve it to the definitions and the placement. I needed the antecedent restated.

**15.** "The reader passed over four things carried in every entry and reported that none o…"

Two problems. "passed over" read first as "skipped", then as "went through and considered" — about 60% on the second. Then the four items include "how far each catcher reaches", "the text the judging model is handed", and "the half of the notes carrying what the entry was folded out of". None of those appear in the fifteen-part list at the top of the page; they are sub-parts of `catchers` and `notes` that were never enumerated. If I wrote a new entry against the fifteen-part list as instructed at step 3, I would leave those out. I needed the sub-parts named where the fifteen are named.

**16.** "Every one of those six lists now stands inside the rule that names it, read out of…"

The next sentence says "Three of the six had no such file". I read the two as contradicting each other until the sentence after that supplied the migration. I needed the three-had-no-file case stated before the "every one now stands" claim.

**17.** "In order they returned 45 stops with 11 blocking, then 34 with 8, 27 with 12, 28 w…"

Then: "The seventh reading returned fewer stops than the sixth and more blocking ones." I counted forward from reading five to find that the seventh is the third pair (27 with 12) and the sixth is the second (34 with 8). I needed the two readings' numbers restated in the sentence that compares them.

**18.** "that the page failed four readings and took five repair rounds"

Five rounds against four readings. I looked for the fifth round's trigger and found none. I needed either the count explained or the mismatch acknowledged.

**19.** "Those instructions also rested on three vocabularies this page does not define: th…"

The page names the six surfaces at line 28. Here it says it does not define them. Both are true under different readings of "define", and I re-read to settle which was meant. I needed "names but does not define".

**20.** "The counts below take each bracketed identifier as one word, so the five codes trai…"

The counting rules cover bracketed identifiers, hyphenated names, and em dashes. I counted the older quotation and reached 100 words plus 5 codes only by treating `` `PROBLEMS.md` `` as a single word, which no stated rule covers. I needed the backticked filename included in the counting rules.

**21.** "What stands open is the criterion itself, unrepaired in the spec today."

The section had just shown the criterion in its repaired form at 35 words. I re-read to see that "unrepaired" applies to two named defects inside the repaired text. I needed "the two defects above stand unrepaired".

**22.** "1. A cold reader stops on a sentence."

Line 98 says some rules came from a cold reader and some from the owner. The numbered procedure that produces every rule admits only a cold reader as step 1. Following the procedure as written, an owner's stop opens nothing. I needed step 1 to name both.

**23.** "Two things here carry names close enough to be read as one, and each keeps one name…"

I worked through the pre-show lint and the register judge and found that the judge is one of the lint's two passes — one contains the other. "Two things" set me up to expect two separate objects. I needed the containment stated up front.

**24.** "Neither the sentence nor the two names is reproduced here, because the same lint ga…"

Lines 150–156 reproduce «Триггер», «Обязанность», and «хвост без глагола» in full, and the last is described by the page as a coinage. The gate the page names as the reason for withholding did not stop those. Also, this page states its own one obligation at line 103 — the writer owes the reader every word the writing depends on — and the withheld sentence is the entire evidence for the section's claim. I could not check the claim. I needed the example, or a reason that covers the earlier coinages too.

**25.** "The judge was not run, because the script makes that call only when it is switched…"

Three clauses joined by commas: the switch is manual, the maintainer's page shows how, the switch stayed off. I re-read to separate them. Also "the probe" appears here as a settled name for the 07-17 episode, which was introduced as "the list was handed one Russian sentence". I needed the episode named when it was introduced.

**26.** "the judge's code is driven against a written-out model reply"

I guessed: a model reply stored as text in the test file. About 85% sure. I needed "a recorded reply stored in the test".

**27.** "an override (`personal_override`), which the owner writes to hold one rule tighter…"

Only tightening is described. I could not tell whether an override may loosen a rule. I needed the range stated.

**28.** "`r18`, *the language each surface is written in*"

The rule is named by its subject with no content. This page carries English and Russian both. I could not tell which surface admits which language, so I could not apply the rule to anything I would write. I needed either the languages here or a pointer that says the answer is on the writer's page.

---

## Answers

**1. What is this document for, who reads it, when?**
It records why this project's writing rules exist: the readings that produced them, one repaired spec sentence, and the procedure that turns a repeated reader stop into a rule entry. The page says directly who reads it and when — "Read this page to know why the rules say what they say" — so it serves someone questioning a rule's origin rather than someone applying one. It also says it is currently shown to nobody until it clears two clean readings.

**2. Do I know what the other documents hold and when I would go there?**
For three of them, yes: `docs/language-rules.md` is the writer's page and holds what a writer applies; `docs/language-rule-coverage.md` is the maintainer's page and holds catcher reach, how to run each catcher, and what a break costs; `docs/language-reads/` holds one reading per file in the shape given at lines 88–94. For `guardrails/language-rules.json` I know the fifteen field names and would go there to edit a rule. For `skills/text-audit/SKILL.md` I know only that the cold-reading prompt lives in it. For `JOURNAL.md` and `PRODUCT_SPEC.md` I have one sentence each and would be going in cold.

**3. Could I use this page tomorrow for the job it claims?**
For the "why does this rule exist" job, mostly yes — the readings are dated, attributed, and traceable to files. For the job at step 3 of *How a class becomes a rule*, no: I would write a new entry against the fifteen-part list, and stop 15 shows the list is short of the sub-parts the maintainer's page carries. I would have to ask the author: what are the six surfaces, what does `r18` require, what values `status` and `armed` take, whether identifiers are gapless, and what the withheld 07-17 example was.

**4. What read clearly on the first pass?**
The opening contents list and the definitions of class, break, catcher, and home. The five roles section, including the cold reader's conditions and the shape a reading comes back in. The whole *One sentence, before and after* section past its terminology preamble — the two quotations side by side, the three instructions, and the account of what moved into the list. The three numbered steps of *How a class becomes a rule*, apart from step 1's scope.

**5. Sort**

BLOCKING (8): 2, 8, 10, 12, 15, 22, 24, 28.

NON-BLOCKING (20): 1, 3, 4, 5, 6, 7, 9, 11, 13, 14, 16, 17, 18, 19, 20, 21, 23, 25, 26, 27.

**Total stops: 28.**
