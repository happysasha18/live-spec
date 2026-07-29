# The writing register — native open-source technical-writer voice

Everything the pack writes for a human — spec prose, reports, decision cards, READMEs — reads in one
register: a native-English technical writer for a serious open-source project. Neutral, precise, easy
to follow. Never let it read as a marketing or pitch voice, a personal brand, or something quirky. (Defined 2026-07-07 after
the owner rejected both a "confident product pitch" draft and a persona-flavored one; his words, 2026-07-07:
write in the language of a native-speaker technical writer for open source, consistent and easy to read.) Seventeen rules:

## Sentences and paragraphs

How a single sentence and a single paragraph each carry one idea.

- **One idea per sentence.** *(rule 1)* Target 15–25 words. A sentence carrying two clauses joined by a dash and a
   parenthetical gets split into two or three sentences.
- **One paragraph, one point.** *(rule 2)* State the point in the first sentence; the rest supports it. A reader
   who reads only first sentences still follows the section.

## Terms

How a specialized word is introduced and kept consistent.

- **Define every abstract term in plain words at first use, then reuse it unchanged.** *(rule 3)* Picture first,
   term second: "Some parts of a project hold state — a screen, a panel, a saved file. The spec calls
   each of these a *stateful surface*." After that, always say "stateful surface".
- **A term is never bare on its debut.** *(rule 4)* "axis", "surface", "canonical axes", "provenance" met without
   a definition beside them is a defect. For a section readers may jump into directly, give a one-clause
   reminder or a pointer to the defining section.
- **One term per concept, everywhere.** *(rule 5)* If the defining section says "queue", every section says
   "queue". Never "roadmap", "backlog", or "the list" as a casual synonym. Synonym variety is a virtue
   in essays and a bug in a spec.
- **Prefer the concrete noun.** *(rule 6)* "A screen, a panel, a saved file" carries more than "an entity". When
   an abstraction is genuinely required, ground it with a two- or three-item example on first use, then
   use the abstraction alone.

## Voice

Who acts in the sentence, and which words a reader already knows.

- **Active voice, named actor.** *(rule 7)* Say who does what: "the agent re-reads the file", "you approve the
   change", "the suite turns red". Passive voice is acceptable only when the actor is truly irrelevant.
- **Address the reader as "you"** *(rule 8)* for what a person does; name the component ("the installer", "the
   prover") for what software does. Never "one" or "the user is expected to".
- **Use words a reader recognizes without living in your head.** *(rule 13)*
    - Natural, well-understood industry
      language is good, even when it is a metaphor — "pipeline", "software house", "conveyor", "streamline",
      "ships" all land because a developer already holds them.
    - The words to avoid are invented internal
      terms and private interpretations: an abstraction that means something only inside this project.
    - When
      such a term is genuinely needed (for example "stateful surface" or "axis"), define it in plain words
      at first use (rule 3); after that it is safe to reuse.
    - The test: would someone outside the project
      recognize this word naturally? If yes, keep it. If it is your own coinage, define it or replace it.

## Trim and shape

Cut what adds nothing, and shape the whole into a readable structure.

- **Examples earn their place by resolving ambiguity.** *(rule 9)* Add an example where a reader could read a rule
   two ways; cut examples that merely restate a clear rule. Use realistic values; one per rule is enough.
- **Cut nominalizations.** *(rule 10)* "Perform the reconciliation of" becomes "reconcile"; "the verification of
    the claim occurs" becomes "the suite verifies the claim". Verbs carry the meaning.
- **Cut throat-clearing and filler.** *(rule 11)* Delete "It is important to note that", "In practice",
    "Essentially", and intensifiers like "very", "actually", "of course". If deleting a phrase changes
    nothing, delete it.
- **Machine codes stay quiet and trailing.** *(rule 14)* The bracket anchors (`[INV-7]`, `[A-3]`, `[C-1]`) sit at
    the end of the sentence or clause they anchor. Prose never opens with a code or depends on one to be
    understood.
- **A document is a tree of grouped topics, never one flat list.** *(rule 16)*
    - Related rules or sections gather
      under a named parent that says what the group is about, so a reader meets the few big areas first
      and then the specifics under each.
    - A long flat run of peer items at one level is the smell to fix:
      gather them under two to five headed parents.
    - Levels nest without skipping — one document title,
      parts under it, topics under those, rarely deeper than three.
    - Every heading names its group's
      subject in a few plain words, so the outline alone tells a reader the document's shape.
    - A numbered
      item that stands as its own rule opens with a short bold title; a numbered item that is one step in
      a procedure ("read the size, then draft the delta, then queue it") stays a bare ordered list, since
      its order already carries the meaning. (2026-07-09: flat is the defect — structure the
      document, do more than label its items.)


## Framing

Lead with what a thing is, and hold the contrast frame out.

- **State rules positively.** *(rule 12)* Say what happens and when. Reserve negatives for genuine prohibitions
    ("never delete a host file"), stated as a plain imperative. The contrast frame is banned outright by
    rule 15.
- **Never the contrast frame — the hardest rule, and it holds in live chat too.** *(rule 15)* Never name a thing by
    denying its neighbour: stating what something is by pairing it with a denial of the alternative.
    - The
      shapes are an em-dash or a comma leading into the denied neighbour in English, and the parallel Russian
      constructions that set a negated word against the word meant to replace it.
    - This governs casual replies
      inside a running conversation as much as documents and artifacts; the human is allergic to the frame,
      and it stays absent even mid-dialogue.
    - Say what the thing IS in its own sentence. When a boundary
      genuinely needs naming, give it its own plain sentence: "The prototype is the norm. The prose describes
      it."
    - The ban holds even when the frame feels like the sharpest available phrasing; that pull toward it
      is the tell to rewrite.
    - The linter's scissors check holds the floor (`scripts/spec-style-lint.py`); the
      ceiling is a read-aloud that turns every denied-neighbour clause into its own positive sentence.
      (2026-07-09, restated with an explicit allergy: the frame stays out of chat replies to our
      conversations, and every earlier text carrying it is a bug to sweep.)


## Numbers

What a number owes the reader who meets it.

- **A number carries four things.** *(rule 17)* A number stated on its own is a defect.
    - **Why it is measured** — the decision it informs, or the question it answers.
    - **What changes when it moves** — what the project does differently if the number rises or falls.
    - **Its unit** — what is being counted, in what.
    - **Its method** — the command or the procedure that produced it, so a reader reproduces it.
    - The four stand in the number's own sentence or in the paragraph around it. A number quoted from a
      source the text names inherits that source's method.
    - The mechanical floor is the measurement arm of `hooks/midturn-chat-scan.py`. It reads a paragraph
      for a count whose method stands nowhere beside it. The other three parts are meaning, and a person
      or a reading model holds them.
    - The case this rule rests on: a session reported that a reader returned a count of stops. That
      sentence named what a stop is, what the count decides, and how the count was produced, in none of
      its words. `DECISIONS.md` carries the owner's instruction of 2026-07-29 12:08.


**Verify each finished or edited piece of writing** — the checklist a good technical writer runs:

1. **First-use check.** List every specialized term in the piece. Each is defined in plain words at
   first use here, or defined earlier with a reminder/pointer if this is a likely entry point.
2. **Cold-reader check.** Read it pretending you know nothing beyond the opening. Mark every sentence
   that only makes sense with prior system knowledge; each mark is a fix.
3. **Consistency grep.** For each key term, search the whole document for near-synonyms and drifting
   usage. One term per concept; fix strays at the source.
4. **Read-aloud test.** Read it aloud. Anywhere you stumble, run out of breath, or restart a sentence,
   rewrite that sentence.
5. **Actor check.** Every rule sentence answers "who does this, to what, when". Fix missing or hidden
   actors.
6. **Example audit.** Each example resolves a real ambiguity; each ambiguous rule has one.
7. **Deletion pass.** Try deleting each opener phrase, qualifier, and adjective. Keep only what changes
   meaning.
8. **Anchor integrity.** Every bracket code present before the edit is still present, still trailing,
   and still listed correctly in the Formal index.
9. **Scissors scan (rule 15).** Before sending, scan the piece — chat replies to the human included — for
   the contrast frame in every shape: a denied-neighbour clause after an em dash or a comma, and its
   Russian equivalents that set a negated word against its replacement. Rewrite each hit into a positive
   sentence first. Run `scripts/spec-style-lint.py` for the mechanical floor; this scan runs on every
   message to the human, and on documents.
10. **Structure check (rule 16).** Read only the headings and the titles of numbered rules. They alone
    should reveal the document's shape — the few big areas and what groups under each. A long flat run of
    peer items with no parent grouping, a heading that hides its topic, or a skipped level is a fix.
