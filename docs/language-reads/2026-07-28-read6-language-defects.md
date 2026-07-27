# Blind read, 2026-07-28 — the language-defects document, read six

The reader met this text with no context: one file, no repository access, no history of the
document's earlier rounds. The brief asked for every place the reader stopped, sorted into stops
that blocked the reader and stops the reader noticed and read past.

Reader: a working software engineer persona, clean context.
Text read: `docs/language-defects.md` as it stood after the round-six repair, when the rules had
moved to their own home and this page had become the record behind them.
Stops: 34 — 8 blocking, 26 non-blocking (the blocking list holds six bullets, two of which each carry two stop numbers).

Read five, on the previous shape of this page, recorded 45 stops with 11 blocking.

---

I read it once, straight through. Here is what happened.

# Stops

**1.** "An entry gives the rule in a sentence, a question to ask of a sentence, examples, ex…"
"what catches the rule" read to me as catching the rule itself, and I had to re-read to get that it means catching a *break* of the rule. Also, "catcher" is used here as a known noun; its definition arrives four sections later. I needed the definition at first use, or wording like "what catches a break of it".

**2.** "the one thing every text owes its reader;"
The section this points to says the opposite direction of obligation: "A reader owes the text nothing. The writer gives the reader every word…". The bullet puts the debt on the text, the section puts it on the writer and denies the reader owes anything. I re-read both to decide they were the same idea stated from two ends.

**3.** "A reader owes the text nothing."
I stopped and guessed this means: the reader is not obliged to bring outside knowledge, so anything the sentence depends on must be on the page. Confidence medium. It reads as a moral claim before it reads as a rule.

**4.** "Each of them appears where it is used, or in one named place the sentence points to."
"Each of them" — I had to go back a sentence to bind it to "every word, number, and list". Two sentences with different subjects sit between the noun and the pronoun.

**5.** "Four roles appear on this page: the writer, the reader, a cold reader, and the owner."
Then: "**The owner** is the person whose project this is. He reads drafts and stops on sentences." A specific man arrives with no introduction. Later, "The owner then read a first rewrite… and stopped six more times" — six more than what? The count before it belongs to a different person (the Russian reader, twenty stops). I could not tell whether the counts accumulate across people.

**6.** "Every rule rests on what cold readers stopped on."
This is contradicted later: rule `r36` came from the owner's read of a rewrite, and the owner is defined as a separate role who reads drafts with full context. So a rule exists that no cold reader produced. I disagreed with the sentence as written.

**7.** "A cold reader is given the text alone: no repository, no history of earlier drafts, and no cha…"
Against: "Of the six requirements, that reader could build two from the text alone and one after asking the writer questions." The cold reader asked the writer questions, which the definition says cannot happen. The document breaks its own definition three sections later. I could not tell which one governs.

**8.** "plus the laws handed to the model that judges each kind of text."
"laws" appears with no definition and never gets one. I guessed it means the instruction text given to a judging model — the same content as the rules, in a form a model reads. Confidence low. It is the same word the document later reports a cold reader stopping on ("seat, net, door, home, walk, lens, handle, frame, law, tier").

**9.** "law" vs "rule" — two names I suspect mean one thing.
"the break-record law", "the orchestration laws", "the laws handed to the model", against "rule", "the 61 rules", "the rule about loan-translating a term". The document itself reports a reader naming the habit of "one thing carrying two names in neighbouring sentences" as a defect. I could not tell whether a law is a rule, a rule of a different kind, or an unrelated thing.

**10.** "class" vs "rule" — same problem.
The intro promises "how a new rule gets in", and the section delivering it is "How a class gets into the rules", whose step 3 writes the class into the rules file as an entry. I read the section twice to settle that a class becomes a rule.

**11.** "`guardrails/check-language-rules.py` — the gate. It refuses a page that has drifted from t…"
Parsed as "refuses a page … and refuses a rule pointing at a file or a line that is gone." Refusing a rule is a different action from refusing a page, and I re-read to work out that it means the gate fails when a rule's file reference is stale.

**12.** "Four files carry the rules: the file every rule is edited in, the page a person reads, the…"
"the gate over both" — over which two of the four? I settled on the source and the page. Re-read once.

**13.** Section title: "Where the rules live, and how to run their catchers".
Two commands are given for the generator and the gate, and two for per-rule script catchers. No command, event, or entry point is given for the model catcher, which the same page introduces as one of the three kinds. I could not run the catcher family the title promises.

**14.** "Every one of them prints one line naming what it read and how far it looked. A passing run…"
I stopped on "how far it looked" — I guessed it prints something like a file count or a line range. Confidence medium. Nothing shows the shape of that line, and the claim about coverage rests entirely on it.

**15.** "Each entry in `docs/language-rules.md` carries a status: whether a catcher runs the rule to…"
The status is described as "the event it runs at", and then one of the four values is `nowhere`, which is not an event. `manual` is also closer to a mode than an event. I had to re-read the list to accept it as a mixed set.

**16.** "**`session-stop-hook`, `session-prompt-hook`** — the session holds its own reply, names wha…"
"the session holds its own reply" — I guessed the agent's outgoing message is blocked until the writer fixes the text. Confidence medium. "The session" acts as an agent here and is not one of the four roles introduced earlier.

**17.** "Of the 61 rules, 34 are armed nowhere today, and that count falls as catchers are built."
"armed" arrives without definition; I guessed it means a catcher is wired up for the rule. Confidence high from the surrounding list. "armed nowhere" still made me stop, because `nowhere` was just defined as a status value, so the sentence reads as both a status name and a location.

**18.** "A rule binds as many surfaces as it governs, and `docs/language-rules.md` writes it out on…"
This is the rule I could not apply. "the first surface it binds" — first in what order? No ordering is stated anywhere. The six-item list may or may not be the order. Without it, I cannot predict which section holds a given rule.

**19.** "Read the section of `docs/language-rules.md` named for the surface you are writing."
This is the closing instruction, and it collides with stop 18. If a rule binding both `spec-body` and `chat` is written only under `spec-body`, then reading the `chat` section alone misses rules that bind me. Following the closing instruction, I would write chat text while unaware of rules that govern it. I would have acted on the document wrongly.

**20.** "Three were left undone. The lists and the default values those three rules depend on were n…"
The six items were called "requirements" one sentence earlier and are "rules" here. "Rule" already carries the language-rule meaning throughout the page. I re-read to work out that these are spec requirements, a different population from the 61.

**21.** "That is a stop every thirteen words, in a text meant to be read straight through."
I stopped to check: 250 divided by 20 is 12.5. The figure holds if you round. The stop was the arithmetic, not the claim.

**22.** "It stated that rule in two loan-translated words: «триггер», «обязанность»."
Two Russian words with no gloss. The very next bullet does gloss its Russian ("«хвост без глагола», a tail with no verb"), so the page treats two neighbouring cases differently. Without the gloss I cannot see what made these two words a defect, which is the whole point of the example. I needed the English behind each word.

**23.** "One sentence stated the rule that a criterion carries one trigger and one response."
"criterion" is used as a known unit of a spec. I guessed it means one acceptance criterion inside a numbered requirement. Confidence medium, confirmed two sections later by "Criterion 4 of Requirement 233".

**24.** "This page is shown to nobody until two cold readings in a row return nothing blocking."
The record above says the fifth reading failed with 11 blocking stops, and the page was handed to me. Either cold readers are excluded from "nobody", or the page is in front of me against its own stated bar. The exclusion is never stated. As written, the page breaks the rule it states in the same passage.

**25.** "The fifth reading is recorded at `docs/language-reads/2026-07-27-read5-language-defects.md…"
I can guess that file holds a list of stops. "`JOURNAL.md` counts them" — I could not tell what I would find in `JOURNAL.md`, what form the count takes, or whether it holds anything else I would need. It is named once and never described.

**26.** "The sentence runs to 35 words with the same codes, and its four members sit in a list below…"
I disagreed. The 107-word figure counts the four definitions; the 35-word figure excludes them because they moved to a list that is part of the same criterion. The comparison sets a whole against a part. The prose is straightforward about the move — "The four members moved into a list… and the words that defined them moved with them" — which is what made the number comparison stand out.

**27.** "The instruction stayed in the sentence. The four members moved into a list, one to a line, …"
The list below has five bullets. The fifth — "each break is recorded in the problem ledger (`PROBLEMS.md`), the home the break-record law names" — is an instruction, and it sits in the list rather than in the sentence. I counted the bullets twice.

**28.** "The system *shall* judge the orchestration members carrying a reminder-history of two or mo…" against "The system *shall* judge the orchestration laws carrying a reminder history of two or more…"
The same things are "members" in the before and "laws" in the after. The page names this exact habit as a defect a reader caught. I could not tell whether the rename was part of the repair or an accident.

**29.** "A class opens once that artifact keeps producing the same stop."
"artifact" here means the source that taught the wording (a skill file, a template). Fourteen lines earlier, `artifact` is one of the six surfaces: "a page or a report published for someone outside the project". One word, two meanings, both load-bearing. I re-read the step to pick the right one.

**30.** "The entry also names the surfaces the rule binds, the places that already state it, and a s…"
"the places that already state it" — I could not work out what these are. My guess: other project documents where the rule is already written in prose, so the entry can point at them. Confidence low. Nothing else on the page mentions such places.

**31.** "A repair applied to one sentence and nowhere else means step 2 was skipped."
I disagreed on which step. Step 2 is tracing the wording to its source; step 3 is writing the class down. A one-sentence repair skips both, and skipping step 3 is the one that leaves nothing behind. I would name step 3.

**32.** "On 2026-07-17 `scripts/preshow-register-lint.py` was handed a Russian text carrying the sam…"
The example is offered as proof that a literal pattern holds only the instances someone already met. What it shows is a script failing on words its own list already holds, which is a different failure — the instance was met, and the script still missed it. Either the list is English-side only, or the script skipped that file. The page gives neither. I needed the reason it passed.

**33.** "live-spec is this project: a set of skills, scripts, and gates that a person and an agent us…"
"gate" gets a definition in the next clause. "skills" does not. I guessed it means instruction files an agent loads. Confidence medium.

**34.** Section heading "The people on this page", whose first paragraph defines the project and the word "gate".
I looked for people and got a project definition. Small, but I re-read the heading.

**Count: 34 stops.**

# Answers

**1. What is this document for? Who reads it, and when?**
It records the evidence and the process behind a set of 61 writing rules that live in another file, and it explains how those rules are stored, generated, and enforced. Its own line names the audience split: "Read `docs/language-rules.md` to write. Read this page to know why those rules say what they say." So it is for a writer on this project who wants the reasoning, or someone deciding whether a new rule is warranted, read once rather than at each writing session.

**2. Do you know what `docs/language-rules.md` holds and when you would go there?**
Yes for the contents: 61 entries, each with the rule in one sentence, a question to ask of a sentence, examples, exceptions, the surfaces it binds, its catchers with their reach, and a status. I would go there before writing any text on this project. What I could not determine is how to find a given rule inside it, because the filing convention ("under the first surface it binds") has no stated order, and the closing instruction to read only my own surface's section would leave rules unread.

**3. Could you use this page tomorrow for the job it claims?**
Partly. I could run the generator and the gate, I could identify which surface my text is, and I could follow the class-recording steps. To actually read the rules that bind me, I would have to ask the author: what order "first surface" refers to, and whether reading one surface's section is sufficient. I would also ask what a "law" is and how it differs from a rule, what the model catcher is invoked by, and what `JOURNAL.md` contains.

**4. Which parts read clearly on the first pass?**
The four-file layout with the commands, the six surfaces with their one-line definitions, the four status values with what a break costs at each, the definition of a catcher as one of three things, the definition of a class as a mistake across many sentences, the three numbered steps for opening a class, and the closing section on what a script and a model each miss. The before/after example was clear as prose; my stop there was on the word counts, not on what changed.

**5. Blocking and non-blocking**

BLOCKING — I could not proceed, or I would have acted wrongly:
- 18 and 19 (the filing order for multi-surface rules, and the closing instruction that assumes single-surface filing). Together these would make me write to an incomplete rule set.
- 13 (no way to run the model catcher, in the section that promises how to run catchers).
- 7 (the cold-reader definition forbids asking the writer; the record has a cold reader asking). If I run a reading, I do not know which procedure to follow.
- 22 (Russian examples with no gloss — the example cannot teach what it is there to teach).
- 8 and 9 ("law" undefined, and possibly the same thing as "rule"). It appears in the rules-generation pipeline, so I cannot tell what the generator produces.
- 30 ("the places that already state it" — a required field of an entry I would have to fill).

NON-BLOCKING — I noticed and read on:
1, 2, 3, 4, 5, 6, 10, 11, 12, 14, 15, 16, 17, 20, 21, 23, 24, 25, 26, 27, 28, 29, 31, 32, 33, 34.
