# Blind read, 2026-07-28 — the language-rules reference, second read

The reader met this text with no context: one file, no repository access, no history. The brief gave
the same task the first read used — write one page of documentation tomorrow and hold it to this
rulebook — and asked how many rules could be applied with no further questions, which contradict each
other, and whether an answer could be found when a writer needs it.

Reader: a working software engineer persona, clean context.
Text read: `docs/language-rules.md` after the folds and the surface definitions, 809 lines, 53 rules.
Applicable tomorrow with no further questions: 33 of the 39 rules that bind a documentation page,
and 40 of 46 if that page also carries the artifact surface.

The first read, over the 1534-line shape with 60 rules, could apply 30 of 60, and about 8 without an
answer to which surface a documentation page is. This read found that answer stated outright.

---

I read the file end to end, then went back through it as a person who has to write a documentation page tomorrow.

---

# 1. THE COUNT THAT MATTERS

The file states 53 rules. A documentation page is human-prose (line 23 says so outright), and the human-prose roster names 39 of them. Of those 39, I could hold myself to **33 tomorrow with no further questions**.

If the page also carries `artifact` — which I could not determine, see §5 — the roster becomes the union of the two, 46 rules, and I could hold myself to 40 of them. The 7 that `artifact` adds (r19, r29, r30, r31, r34, r40, r55) are all applicable as written.

The 6 I could not apply:

| id | The one question I would have to ask |
|---|---|
| **r08** | The rule says a sentence "stays under the word cap for its surface"; the threshold for my surface is named `human_prose_flag_above_words = 25` with a `human_prose_target_band = 15 to 25`. Is a 30-word sentence in human-prose a break, or a flag a reviewer weighs? And does the band's lower bound mean a 9-word sentence is also a break? |
| **r14** | (shares one question with r46) — see below |
| **r45** | "a long flat run of peer items is gathered under headed parents" — how many peer items make a run long? r33, which binds the same surface, forbids exactly this kind of unfilled slot in my writing. |
| **r46** | r46 requires an opening block that carries the answer; r14 cuts a sentence that restates and whose deletion loses no fact. A section lead that summarizes what follows is required by one and cut by the other. Which wins on a documentation page? (r14's exception names r51's closing recap and does not name r46's lead.) Also: is "a reply" the whole page, one section, or does r46 not reach a page at all? Its threshold is measured in `reply_chars`. |
| **r52** | This rule governs "the session's task list on the human's screen." Its Binds line names human-prose. A documentation page has no task list. Does r52 reach my page, or does human-prose appear in its Binds line to cover the task-list text itself? |
| **r53** | I have read this rulebook, so r53 says I may not write the first draft — I write a brief and hand it to "a fresh writer with no package rules loaded." Who is that writer when I am the only one on the task, and what does the rule mean by "package"? The word appears once and nowhere else on the page. |

Everything else I could pick up and use: the coinage list under r02, the 17 inflating words under r15, the weak-word and reference-cue lists under r33, the all-caps exception list under r23, the anchor rules of r11, r25's `you`, r26's active voice, r39's pronoun test, r43's concrete noun, r44's one point per paragraph, r56's one home per fact, r62's single reading.

---

# 2. THE STOPS

**1.** `A surface is a KIND of text, not a file, and one file carries several. The numbered`
The organizing idea of the whole page is defined by denying its neighbour, and r10 bans that construction on this page's own surface with its exceptions removed for this reader (line 242). `KIND` is in all capitals, and r23's exception list does not carry `KIND`. r09 says a text does not ship while it contradicts a rule it states. I stopped because I could not tell whether the sentence was a deliberate exception or a break, and nothing on the page settles it. What I needed: the definition stated positively, in the form the rules require.

**2.** `Binds 42 of the 53 rules: r01 · r02 · r03 · r04 · r05 · r06 · r07 · r08 · r09 · r10`
The roster runs r15 to r18 with no r16 or r17. Nine ids never appear anywhere on the page: r16, r17, r22, r28, r38, r42, r58, r59, r60. I scrolled back twice looking for a section I had missed, then copied all four rosters into a scratch file and counted them to confirm the totals were internally consistent. They are. What I needed: one line saying the gaps are retired or moved.

**3.** `spec_body_criterion_max_words = 35; human_prose_flag_above_words = 25; human_prose_`
The rule body says "cap." The threshold says "flag." I read the pair three times and could not decide whether 25 is a boundary or a signal. What I needed: one word used in both places.

**4.** `a spec-body criterion counted in the recorded baseline of 469, which passes while t`
Two exceptions joined by a semicolon inside one line, the second reading `a rhetorical triad, which carries no list`. I guessed this means a three-part rhetorical sentence is exempt from r08's requirement to become a bulleted list. What I needed: the two exceptions on two lines.

**5.** `No rule on this page carries a status, and that is deliberate: a rule binds a text `
This comes after twenty lines defining `held` / `stated-only` / `claimed-but-absent`, three catcher statuses, and seven `armed at` values. I had read them carefully, then learned none of them applies to anything on this page. What I needed: that sentence first, or the vocabulary on the coverage page it belongs to.

**6.** `` `PreToolUse` — the next tool call is denied, so the correction reaches the reader i``
The clause "a rule armed here records it in its notes, since the `armed` field's vocabulary holds no word for the event" took two reads. No rule on this page shows a `notes` field, so I could not check the claim against anything.

**7.** `The reader's own layer replaces the rule's `exceptions` with nothing, and that repl`
"This reader" is a different reader from the one every reader test on the page speaks of. "Layer" appears once and is not defined. I guessed: the human who owns this project has removed r10's exceptions, so r10 admits none. What I needed: "r10 admits no exceptions here."

**8.** `15 members, read at build time from `guardrails/spec-coinages.json` under `coinages`
The clause continues into the history of two scripts and a date. r31 says the date and the case behind a rule live in the journal. This sits inside a rule entry on a page that binds r31 on the artifact surface. It also gave me nothing to apply to a sentence.

**9.** `The first draft of prose a human will read is written by a fresh writer with no pac`
"Package rules" — the page calls itself the project's rules and never uses "package" again. I guessed it means this rulebook and whatever loads with it.

**10.** `the cold reader running a read is handed the section while the bar is still unmet, `
The exception explains that a cold reader may be handed text that has not yet passed the cold-reader bar. I parsed it on the third read.

**Where I skimmed, and why.**

- Lines 51–75, the status vocabulary — I read it closely, then line 75 told me it governs nothing here, so I stopped holding it in mind.
- The 15 Russian-to-Russian pairs under r02 (lines 99–113) — r18 pins my document to English, so no example in that block can fire on my page.
- r21, r24, r35, r36, r37 in full — their Binds lines name spec-body only, and my page is not spec-body. I read the titles and moved on. This is where the surface rosters paid off: five entries dismissed in ten seconds.
- r47 and r51 — chat only, skipped the same way.
- The word lists under r35 and r36 (gloss openers, noun-phrase openers, finite markers, 66 tokens) — spec-body machinery.
- The r23 exception list, about 70 tokens — I read its shape and decided to search it when a capitalized word actually comes up.
- The index of questions at the end — I read the nine question headings and one entry list, not all of them.

---

# 3. THE RULES THAT CONTRADICT EACH OTHER

The page anticipates this at line 13: "Two rules that would give opposite verdicts on one word therefore never meet on one sentence: they govern different blocks of the file." Three pairs meet on one sentence on one surface.

**Pair A — r01 against r08, both binding human-prose, spec-body and artifact.**

> **r01.** "A word keeps its everyday meaning, and a term this project needs is defined in plain words at its first use — picture first, term second"

> **r08.** "One sentence carries one rule and no definitions, it stays under the word cap for its surface"

Take a sentence on my page that both states a rule and contains a term's first use: *A ratchet — a limit that does not grow — is checked before every push.* r01 requires the definition to sit at that first use. r08 forbids that sentence from carrying a definition. I can escape by splitting the sentence, and I only found that escape by deciding r08's "no definitions" is scoped to sentences that carry a rule. That reading is mine, and the text does not confirm it.

**Pair B — r14 against r46, both binding human-prose, chat and artifact.**

> **r14.** "a sentence that only performs a stance, prefaces, restates, softens, or ceremonially opens or closes is cut before sending. The ban is on a sentence carrying no fact of its own"

> **r46.** "A reply opens with the answer — the outcome, the decision, or the finding — in a few lines the reader may stop at, and puts reasoning, evidence, and options underneath."

A lead line that states the finding and is then supported by the material underneath carries no fact the reader would otherwise lose — r14 cuts it, and r14's reader test ("Would the reader lose a fact if this sentence were deleted?") returns no. r46 requires it. r14 carries an exception for r51's closing recap and none for r46's opening.

**Pair C — r41 against r43, both binding human-prose, spec-body and artifact.**

> **r41.** "An example inside prose a person reads earns its place by resolving an ambiguity, uses realistic values, and one worked case per rule is enough."

> **r43.** "The text prefers the concrete noun, and grounds a genuinely required abstraction with a two- or three-item example at its first use."

An abstraction that a reader would read only one way still takes a two-or-three-item example under r43; r41 cuts an example that resolves no ambiguity. Both fire on the same phrase.

One near-pair I resolved and want to record, because resolving it cost me a pass: r41's "one worked case per rule is enough" against r61's "an entry carries as many as the class earned." r41's reader test carves out rule entries, so they do not collide. The rule bodies alone do collide.

---

# 4. FINDING AN ANSWER

**"Can I use the second person?"** — Found, about 30 seconds. I went to the index at the end, took the heading "Which person do I write in, and may I say `you`?", got r24, r25, r26, and read r25: explanatory text addresses the reader as `you` for what a person does, and names the component for what software does. r24 says third person, and its Binds line names spec-body only, so it does not reach my page. Clean answer.

I was not confident I had all of it, and I did not. If my page carries `artifact`, r29 also governs `you` sentences and lists `you can ignore`, `you don't have to`, `no need to`, and `feel free` as deletions. r29 does not appear under that index heading. I found it only because I was reading every artifact-bound rule for §1.

**"How long may a sentence be?"** — Found a number in about one minute, and I do not trust it. Index heading "How long may a sentence be, and how much may it carry?" gave r08, r44, r45, r46. r08's Thresholds line carries `human_prose_flag_above_words = 25` and `human_prose_target_band = 15 to 25`, plus `max_subordinate_clauses = 1`. So my working number is 25 words and one subordinate clause. Whether 26 words is a break or a flag, and what the lower bound of 15 obliges, I would have to ask. Complete for my surface as far as I can tell, since r44, r45 and r46 govern paragraphs, nesting and leads.

**"May I define a term in the middle of a sentence?"** — Found in about two minutes, with a residue. Index heading "May I define a term, and where does the definition go?" gave five ids: r01, r02, r21, r35, r43. I checked each Binds line. r35, which forbids in-place definition in a dash-pair aside or a parenthetical, binds spec-body only. r21, the glossary rule, binds spec-body only. So on a documentation page the answer is yes: define at first use, in plain words, picture before term (r01), grounding an abstraction with two or three items (r43).

I was not confident I had all of it, and I did not — r08 says "One sentence carries one rule and no definitions," it binds human-prose, and the index does not name it under this question. That is Pair A above. The index sent me to five rules and the sixth is the one that changes the answer.

---

# 5. THE ORGANIZING IDEA

**What a surface is, in my words.** A surface is a category of text defined by who reads it and what they do with it. It names a class of writing, so one file holds blocks belonging to several surfaces at once — the numbered criteria in a spec file are one surface, the explanatory paragraphs around them another. Each surface owns a roster of rule ids, and that roster is the complete set of rules binding text of that class.

**Which one a documentation page is.** human-prose. Line 23 names "a documentation page" in the human-prose list and then says it again: "A documentation page is human-prose, and it carries `artifact` as well once it is published outside the project."

**How I worked it out.** Line 13 defines the term and line 23 names my case by name, so this took no inference. The rosters then earned their keep immediately: five rule entries dropped out on a Binds line before I read a word of their bodies.

**Confidence.** Confident on human-prose. Not confident on `artifact`, and the gap is not decorative — it moves the roster from 39 rules to 46, and the 7 it adds include r29 (no reassuring or inviting the reader) and r30 (no future tense), which are the two things a documentation page does by habit. "Published to someone outside the project" is never given a test. A `docs/` file committed to a public repository is readable by anyone; the artifact section's own example is "the project's public README as it stands on its repository page," which does not tell me whether the repository or the README is what makes it published.

**What would have made it certain.** One sentence giving a test for publication — for example, a text is an artifact when it reaches a reader who cannot commit to this repository. And a statement of where a text declares its surface: line 13 says "A text declares one primary surface" and no rule anywhere says how or where that declaration is written.

---

# 6. WHAT I WOULD CUT AND WHAT I WOULD ADD

**Cut**

- Lines 51–75, the status and catcher and armed-at vocabulary. Line 75 states that no rule on the page carries a status. Twenty-five lines of vocabulary govern nothing on this page and belong on the coverage page that uses them.
- The script history inside r02's list note ("until 2026-07-28 they kept a list each, and a word added to either was invisible to the other"). It changes no sentence I write.
- The second clause of the `PreToolUse` entry, about the `armed` field's vocabulary.
- The 15 Russian-to-Russian pairs under r02, or a line placing them on the chat surface. r18 pins documents to English, so a document writer cannot use them.

**Add**

- One worked page, end to end: a short documentation page as it failed and as it passed, with the rule ids named at each fix. Every rule here is stated alone; nothing shows the 39 applied to one text at once, and that is the thing I have to do tomorrow.
- A test for "published outside the project," and a statement of where a text declares its surface.
- One line explaining the nine absent ids.
- An order of work per surface. The rosters are id runs with no grouping and no sequence. If I have an hour, nothing tells me which of the 39 to check first. A grouping into what to fix while drafting, what to fix while revising, and what needs another person (r53, r54) would make the roster usable as a pass rather than a lookup.
- The tie-breaks for the three pairs in §3, and "cap" or "flag" chosen in r08.

---

# 7. THE ONE PAGE

**"## The surfaces, and which rules bind each one"** — lines 11 through 49.

Nothing else on the page can be used before it. Every rule entry carries a Binds line, and the Binds line is only meaningful once you know what a surface is; without that section, a new colleague reads 53 entries and has no way to learn that 14 of them do not touch their file. With it, they find their surface, take the roster, and drop everything else in a minute. It is also where the human-prose entry names a documentation page directly, which is the routing answer most new people arrive needing.

The index of questions at the end is the second candidate, since it is the only entry point for someone who has a question rather than a defect to name. It points at ids, so it cannot be used without the surfaces section — and on two of the three questions I ran through it in §4, the list it gave was missing a rule that changed the answer.

**Source file:** `/private/tmp/claude-501/-Users-sashaabramovich/14f2fe20-40cb-4760-b709-ef591b5eb05c/scratchpad/text-to-read-D.md`
