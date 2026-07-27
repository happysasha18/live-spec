# Blind read, 2026-07-27 — the language-defects document, read five

The reader met this text with no context: one file, no repository access, no history of the
document's earlier rounds. The brief asked for every place the reader stopped, sorted into stops
that blocked the reader and stops the reader noticed and read past.

Reader: a working software engineer persona, clean context.
Text read: `docs/language-defects.md` as it stood at 2026-07-27 23:35.
Stops: 45 — 11 blocking, 34 non-blocking.

---

I read the file once, straight through. Below is what happened.

File: `/private/tmp/claude-501/-Users-sashaabramovich/14f2fe20-40cb-4760-b709-ef591b5eb05c/scratchpad/text-to-read-A.md`

# Stops

## Undefined terms I had to guess at

**1.** `"This document holds the ways live-spec's own texts stop a reader"` — "live-spec" is the first proper noun in the document and is never defined. I guessed: the name of the project or framework whose texts these are. Confidence: high on the guess, but I have no idea whether it is a product, a repo, a method, or a team. I needed one clause on first use.

**2.** `"The owner then read a first rewrite drafted in chat"` — "the owner" arrives with a definite article at line 34 and is never introduced. I guessed: the human who owns the project, the person the readers report to. Medium confidence. This is the document's own class 7 — "the" in front of a set is a promise the set has been given.

**3.** `"the reader could implement two from the text alone and one after asking the author questions"` — "the author" appears here, "the writer" throughout, "the owner" from line 34, and "the same reader" for the owner at line 221. I spent effort deciding whether these are two people or four. I now believe writer = author = owner, and that reader is someone else. I needed a sentence naming the cast once.

**4.** `"counting whitespace-separated tokens including its trailing anchors"` — "anchors" is used here with no gloss. Later, `якоря` is glossed as "the bracketed codes trailing a line" and `handle` as "an internal identifier that trails a human-facing line instead of opening it." I read those as the same object under two names. Two names for one thing, inside the document that owns that class.

**5.** `"an internal identifier that trails a human-facing line instead of opening it"` — "opening" as a verb for "appearing at the start." I guessed correctly on the second pass. High confidence, one re-read.

**6.** `"Each bracketed code such as [INV-241] names one invariant"` — "invariant" is undefined. I guessed: a condition the system holds true at all times. Medium-high confidence, from prior industry use rather than from this document.

**7.** `"The conduct judge — the model call reading the turn's action trace against the orchestration laws"` — "the turn" and "action trace" both undefined. I guessed a turn is one exchange with the model and an action trace is the log of tool calls it made. Medium confidence.

**8.** `"a model read for volume"` — I re-read. Guessed: use a model when there are too many candidates for a person to read. Medium confidence.

**9.** `"can flag a common noun used as a term of art, with noise"` — "with noise" as a trailing qualifier. Guessed: produces false positives. High confidence, one re-read.

## Names I suspect point at one thing

**10.** `seat` is defined as "the session doing the orchestrating." `tier` is defined as "the model level a piece of work runs at: a one-shot worker, a multi-step worker, or the session doing the orchestrating." The third tier and `seat` carry identical wording. I could not tell whether they are the same object.

**11.** `net` is "the glossary's own word for any hook or guard." The class 4 repair reads `Two Stop-hook checks: the hedge check and the lean-orchestrator check.` A Stop-hook check is a hook, so by the glossary it is a net. The repair keeps `net` and introduces `check` for the same objects. I would have applied this and created the collision the class exists to remove.

**12.** The file `guardrails/spec-coinages.json` is called "the known-words list" at line 91, "The word list" as a section heading at line 343, and described as holding "the caught examples" at line 345. Three names in one document.

**13.** The section titled "The writer holds a text to the rule it states" is referred to as "the rule about a rule" in the What-catches-what table. Third name for the same thing, counting the earlier "the rule against publishing a text that contradicts a rule it states."

**14.** `PRODUCT_SPEC.md`, "the product spec," "the whole spec," and "the spec" all appear.

## Places the document breaks a rule it states

**15.** `"Two of the missing lists are named in class 7 below: the inline pattern list and the six file-dump verbs. This document does not name the rest."` — class 7 carries three bullets. The third, `the standing orchestration laws`, is also a missing list and is also named. The count in the intro and the content of class 7 disagree.

**16.** `"A sentence carries at most one such term."` (class 1's rule) — the document's own sentence at lines 156-158 names signal, gate, arm and net in one construction; line 22 carries "the inline pattern list" and "the six file-dump verbs." I could not apply this rule and could not find it applied.

**17.** `"A name holds one noun."` (class 3's rule) — the document's own names include code-to-location table, known-words list, cue list, break-record law, file-dump verbs, pattern list, defect class, problem ledger, word count. `file-dump verbs` is quoted as a class 7 defect while itself being a stacked name. I could not tell which of my own compound names the rule would reject.

**18.** `"An anchor does not stand."` (class 5) — and the repair three rows below reads `The measured count stands above its recorded limit.` The same verb is rejected for one thing and used in a repair for another. Line 203 also reads "the machine stands as a first look," and line 241 "list them where the rule stands." I could not tell whether "stands" is available to me.

**19.** `"The conduct judge — the model call reading the turn's action trace against the orchestration laws — reports any law the turn broke"` — this repair carries a definition of its subject inside dashes, which is class 8's defect, in the cell repairing class 5. It also runs past the 25-word mark the document sets.

**20.** The `frame` row of class 1 runs to roughly 55 words under a column headed Repair, and carries three compound terms plus a statement about where they are defined. Same two rules.

**21.** `"twenty stops in about 250 words"` — a number with no reference point, no comparison, and no direction, in the paragraph that supplies the document's central evidence. Class 6's own demand. I could not say whether twenty stops in 250 words is unusual.

**22.** `"catches a known word in a second"` (twice: lines 91 and 345) — a timing claim with no ground.

**23.** Class 7's three examples supply no lists. The repairs read "give the patterns as a list," "name them," "list them where the rule stands." I read this as possibly deliberate, and it still means the document reproduces the defect it names.

## Contradictions between two places

**24.** `хвост без глагола` gets the repair "none" in class 2, with the reason "it points to nothing... there is no such thing as a tail without a verb; that phrase is invented." Line 302 then says "The phrase points to a thing that already has an ordinary name: a closing clause with no finite verb." One place says the object does not exist; the other names it. I disagree with the class 2 verdict and I could not tell which one to follow when I hit a minted name of my own.

**25.** `"Every one of these came from the owner reading a sentence and stopping on it."` — the table's last row is «проверки отступили», and отступили appears in the Russian reader's list at line 30. The provenance claim and the earlier list disagree.

## Rules I could not apply

**26.** The guardrail files — `guardrails/spec-coinages.json`, `guardrails/check-one-name.py`, `guardrails/one-name-aliases.json`, `guardrails/check-weak-words.py`, `guardrails/weak-words.json`, `hooks/register_judge_core.py` — are named with no repo root and no invocation. I cannot run any of the Caught-by half.

**27.** `"The mechanism already runs in guardrails/check-weak-words.py"` for class 6 — the file name says weak words and the described job is grounding a bare number. I stopped on the mismatch and could not tell whether the file does two jobs or the sentence points at the wrong file.

**28.** Only class 4 says what happens on a hit: "reads the pairs... and blocks." No other class says whether a hit blocks a commit, opens a note, or is advisory. I could not apply the document as a gate.

**29.** The closing checklist has eight questions and omits the rule about a text contradicting itself. If I ran the checklist tomorrow I would not catch a self-contradiction, which is the one class the document says only a person finds.

**30.** `"The eight classes below hold the named ways..."` — the body carries eight numbered classes plus a ninth unnumbered rule, which the What-catches-what table lists as a row. I could not tell whether the ninth is a class.

**31.** Class 5's machine verb list is "decides, wants, remembers, reminds, argues, judges, speaks, retreats, shows." The class's own six examples use judge, name, inject, стоит/stand, показывают/show, отступили/retreat. Three of the six would be missed. The document says the pass "finds the common cases and misses the rest," and I still expected the list to cover the examples printed above it.

## Sentences I could not parse on the first pass

**32.** `"Two readers were given text with no context on 2026-07-27 and asked one question"` — I first attached "on 2026-07-27" to "no context." Re-read to attach it to "were given."

**33.** `"Each class below carries one name for the mistake. A writer then finds every instance, and a reader says which class a stop belongs to."` — "then" reads as consequence and I could not find the causal link. Re-read twice.

**34.** `"Each is Russian grammar carrying an English dictionary."` — a compressed figure. I guessed: the word is Russian in form and its meaning is a word-for-word translation of an English term. Confirmed at lines 82-84, so the guess held, and I stopped on the way through.

**35.** `"the writer records a stop here only once its source keeps producing it"` — "its source" bound to the stop or to the class. Re-read.

**36.** `"A reader who has not read the glossary cannot sort the four into two groups."` — four words, and the text describes one category word, two instance names, and one glossary term. That reads as three groups to me. Did not land.

**37.** `"An action its performer cannot perform"` (class 5 heading) — as written, the performer is defined as the one performing. I parsed it on the second pass as an action given to a subject that cannot perform it.

**38.** `"The owner's own reading of it: could most of this be bullets. It can:"` — a question printed with no question mark, answered by a subject that does not match it. Re-read.

**39.** `"One thing, one name, in every sentence, from the first use onward."` — three trailing phrases with no verb between them. Re-read.

## Places I disagreed

**40.** `"Two Stop-hook checks: the hedge check and the lean-orchestrator check."` — this repair uses "Stop-hook," "hedge," and "lean-orchestrator," none defined at that point. Hedge is glossed later under `offering-hedge frame`; lean-orchestrator only in class 8's rewrite; Stop-hook never. The repair for the class about naming is written in three unglossed names.

**41.** The rewrite in class 8 reads `A rule broken once stays a reminder.` — class 5 rejects the word reminder as an actor and class 6 flags `reminder-history`. The model rewrite keeps the noun. I could not tell whether the noun is available.

**42.** `"469 test cases pass, up from 431 last week; higher is better."` — I could not tell whether 431 is a measurement or an example number invented for the repair. Class 6 asks the writer to say when a number was chosen; this repair does not.

**43.** The What-catches-what row for class 6 holds "judges the ground" in both the Model column and the Person column. I re-read to check for a copy error, and I still cannot tell whether both are required or either will do.

**44.** The What-catches-what row for class 8 has a dash in the Model column, and line 324 says a dash marks a checker that plays no part. Deciding whether a dash-bounded span is a definition or an aside reads to me as model work. I disagree with the dash.

**45.** `"Requirement 232 of the product spec uses four words for its objects within three sentences"` — the bullets below attribute three words to "the title" and one to "the user story," which is two locations. I could not verify the claim in any case, since Requirement 232 is not reproduced. The same holds for Requirement 233, whose criterion 4 is reproduced and whose 107-word count I did not verify.

# Answers

**1. What is this document for, who uses it, when.**
It names eight recurring ways this project's human-facing texts stop a reader, and for each one gives a rule that removes the defect and a note on whether a script, a model, or a person catches it. The users are whoever writes or reviews the project's spec, architecture document, README, decision pages, reports and chat messages, at drafting time and at review time. A second audience is whoever maintains the guardrail scripts, since each class states what its checker can and cannot reach.

**2. Could I apply it to my own writing tomorrow.**
Partly. Classes 3, 5, 6 and 8 and the two-names class I could apply to a README of mine today using only the eight questions at the end. I would have to ask the author: what "at most one such term" means when a sentence legitimately involves two glossary terms; whether "stands" is a banned verb, given that it is both rejected and used in a repair; where the guardrails directory lives and how the scripts are invoked; whether a hit blocks or annotates; whether `seat` and the orchestrating `tier` are one thing; and what live-spec, the owner, the turn, and Stop-hook are.

**3. Which parts read clearly.**
The one-demand paragraph — "A reader owes the text nothing. The writer must give the reader every word, number, or list the writing depends on" — landed on the first pass and carried the rest of the document. Class 6's three worked examples and class 8's full before-and-after, including the bullet rewrite, are the two places where I could see the defect and the repair side by side and knew what to do. The closing paragraph on human cold-reading being a standing cost, the three-step account of how a class gets in, and the line "A repair applied to one sentence and nowhere else means step 2 was skipped" all read once and held.

**4. Sorted.**

BLOCKING — I could not proceed, or I would have applied the document wrongly: 11 (net/check collision created by the repair itself), 16 (at most one term), 17 (one noun per name, against the document's own names), 18 (stands, rejected and used), 23 (class 7 gives no lists), 24 (two incompatible verdicts on one phrase), 26 (guardrail files unlocatable), 28 (no verdict semantics), 29 (checklist omits the ninth rule), 30 (eight classes or nine), 40 (repair written in three undefined names).

NON-BLOCKING — I noticed and read on: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 19, 20, 21, 22, 25, 27, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45.

**Stop count: 45.** Eleven blocking, thirty-four non-blocking.
