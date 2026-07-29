# Reading record — skills/text-audit/SKILL.md, read 2026-07-29

Stops: 28 — 3 blocking

1. **"a fresh cold reader with zero context on the text's history"**
   Where: YAML frontmatter, `description` field (line 3).
   What a stranger cannot tell: what a "cold reader" is. The term is used here, in the document's very first lines, before any definition appears.
   Guess: that it means an inexperienced reader, resolved a few lines later at "A cold reader meets the text with no knowledge of its history."
   Non-blocking.

2. **"read a text as a stranger, fix where they stop"**
   Where: the document's title (line 8).
   What a stranger cannot tell: whether "a stranger" names the same role as "the cold reader," defined later, or a separate, looser idea. No sentence anywhere in the document states the two are the same word for the same role.
   Guess: treated "stranger" and "cold reader" as synonyms throughout.
   Non-blocking.

3. **"the session's live word first, then the host profile, the personal profile, and the package default"**
   Where: opening blockquote, "Part of the live-spec pack."
   What a stranger cannot tell: what "the session's live word" is — a setting, an instruction, something else. It is never defined here or in either companion file.
   Guess: read it as "whatever instruction is currently active in this conversation."
   Non-blocking.

4. **"The loop came from the comprehension gate on spec sections, recorded in `docs/spec-format.md`."**
   Where: paragraph beginning "The loop came from the comprehension gate…" (after the cold-reader definition).
   What a stranger cannot tell: what that gate actually found, or why it settled on this loop — the document names a file that holds the ground but does not state the ground itself.
   Guess: took the claim on faith without seeing the underlying evidence.
   Non-blocking.

5. **"Those readers found new blocking terms on every pass, and the terms already repaired stayed repaired."**
   Where: same paragraph, continuing "Those readers found new blocking terms…"
   What a stranger cannot tell: this paragraph carries three separate points — evidence that the loop converges, the definition of a "reading record," and a closing claim that this skill packages that loop. A reader following the first sentence is not signaled that a definition and a generalization follow in the same block.
   Guess: split the paragraph mentally into its three parts to track them separately.
   Non-blocking.

6. **"the cold reader is never either of them"**
   Where: heading "The roles and the words this skill uses," opening paragraph.
   What a stranger cannot tell: "One person may hold the auditor role and own the text" merges two roles into one person; the next clause then says the cold reader is "never either of them" as if two separate things were still in view. The sentence needs a second pass to see that "them" means the auditor role and the person role, not the one merged person.
   Guess: reread it to confirm "them" = the two roles, not "the one person" just described.
   Non-blocking.

7. **"a worker brief"**
   Where: "The live-spec repository names six surfaces: a spec body, human prose, chat, a published artifact, a commit message, and a worker brief."
   What a stranger cannot tell: what a worker brief actually is. It is named twice (here, and later as an example of machine-read text) but never described.
   Guess: read it as an instruction document handed to an automated worker, by analogy with "worker."
   Non-blocking.

8. **"A surface is a kind of text."**
   Where: same section, second bolded paragraph beginning "One file carries several kinds."
   What a stranger cannot tell: this is the exact same sentence as the one seven lines above it ("A **surface** is a kind of text."). Nothing distinguishes the two beyond one detail (the artifact-surface addition) that follows.
   Guess: read the second instance as a reminder rather than new information.
   Non-blocking.

9. **"the three words above"**
   Where: end of the same section, "`guardrails/language-rules.json` is the file where the six surfaces, the three words above, and every rule of every register are edited."
   What a stranger cannot tell: which three words are meant. The section has just defined "surface" (twice), "register," and "class" — a reader has to scroll back and count to work out that the three are surface, register, and class.
   Guess: counted the bolded terms above and settled on surface / register / class.
   Non-blocking.

10. **"its clarity matters"**
    Where: heading "When it fires," "Load it when a human-facing text is about to ship and its clarity matters:"
    What a stranger cannot tell: matters by what measure, or to whom. No judge or threshold is given.
    Guess: read it loosely as "whenever the text will be read by someone outside the project."
    Non-blocking.

11. **"A design review of a spec belongs to product-prover" / "design-reviewer — judges the design the spec describes"**
    Where: "Work that belongs elsewhere" ("A design review of a spec belongs to product-prover, at `skills/product-prover/SKILL.md`") against "The pack this skill belongs to" ("**product-prover** reviews the spec as written." / "**design-reviewer** judges the design the spec describes.").
    What a stranger cannot tell: which skill actually owns design review. The first passage sends design-review work to product-prover, described there as arguing with claims (a missing state, a false invariant). The closing list names a *different* skill, design-reviewer, whose one-line job — "judges the design the spec describes" — matches the words "design review" far more closely, and describes product-prover's job differently ("reviews the spec as written"). Nothing in the document reconciles the two skills or says how they relate.
    Guess: could not resolve which skill to send a design-review request to; guessed product-prover only because it was named first, with real doubt.
    Blocking.

12. **"whatever writing skills the host installs beside the pack"**
    Where: "Work that belongs elsewhere," the paragraph on taste and voice.
    What a stranger cannot tell: who or what "the host" is — a person, an organization, an environment. It is not defined anywhere in this document or its two companions.
    Guess: read "the host" as the person or team running the project this skill is installed into.
    Non-blocking.

13. **"a checkpoint"**
    Where: same section, "A worker brief, a checkpoint, and an internal note are machine-read."
    What a stranger cannot tell: what a checkpoint is in this project. It does not appear among the six named surfaces earlier, so it is unclear whether it is a seventh, unlisted surface or something else entirely.
    Guess: read it as a save-point or status file no person reads directly.
    Non-blocking.

14. **"The comprehension gate settled on two reads, and `docs/spec-format.md` records that pattern."**
    Where: "The loop," step 4, "Read again, and close on two clean reads."
    What a stranger cannot tell: this restates, almost word for word, the same pointer-only claim already made near the top of the document (entry 4). No new grounding is added the second time.
    Guess: treated it as confirmation rather than new evidence.
    Non-blocking.

15. **"a handful of sentences"**
    Where: paragraph after "The loop," "A section-sized run puts one definition and a handful of sentences in front of a reader."
    What a stranger cannot tell: how many sentences "a handful" means, or against what this size is being judged.
    Guess: read it as roughly three to six sentences.
    Non-blocking.

16. **"The plan chose that size and gave two reasons for it (`docs/plans/2026-07-28-top-level-readability.md`)."**
    Where: "Running it on a spec section," "Ten requirements at a time is the working size…"
    What a stranger cannot tell: what the two reasons actually are. The document names a plan file that holds them but states neither reason on the page.
    Guess: assumed the reasons match the next sentence's rationale (a reader can hold that much, and a nearby repair cannot break a distant requirement), though the document never says these are the two reasons named in the plan.
    Non-blocking.

17. **"The first rule binds the criterion lines and the second binds the Context paragraphs, so neither one judges the other's sentences."**
    Where: bolded item "A criterion and the prose around it take different rules."
    What a stranger cannot tell on a single pass: which of the two preceding sentences is "the first rule" and which is "the second," since neither was numbered when stated.
    Guess: matched "the first" to the third-person/named-actor sentence and "the second" to the speaks-to-the-reader sentence, by their order.
    Non-blocking.

18. **"A rewrite that moves one of them breaks a test, or one of the two maps below."**
    Where: bolded item "Every mark a machine reads survives the repair."
    What a stranger cannot tell: what "them" refers to. The paragraph names four candidates across three sentences — a requirement's number, its bracket anchors, headings, and any phrase a test quotes — with no single antecedent set clearly marked.
    Guess: read "them" as all four items named in the paragraph, taken together.
    Non-blocking.

19. **"whose rows pair one architecture node with one spec fact and pin the test level that covers it"**
    Where: bolded item "The test matrix is `TEST_MATRIX.md`."
    What a stranger cannot tell: what "an architecture node" or "the test level" is. Neither term is defined anywhere in this document or its two companions, and no test levels are ever named.
    Guess: read "architecture node" as some unit of the architecture document, and "test level" as a rank like unit/integration/manual, without confirmation.
    Non-blocking.

20. **"The architecture document, the recorded decision, and the test matrix hold the answers"**
    Where: bolded item "A fix comes from the spec's own neighbours."
    What a stranger cannot tell: whether "the architecture document" is the file named `ARCHITECTURE.md` a few lines further down (in the spec-freeze command). Unlike "the test matrix," which the document explicitly equates with `TEST_MATRIX.md` two sentences earlier, "the architecture document" is never tied to a filename.
    Guess: assumed "the architecture document" means `ARCHITECTURE.md`, inferred only from a later, unrelated command line.
    Non-blocking.

21. **"a second reader who puts the old text and the new text side by side and reports every difference in meaning"**
    Where: the four checks that "run after the section is repaired," and again at "Two of these four checks run anywhere: the project's own suite and the second reader."
    What a stranger cannot tell: who performs this check. "The roles and the words this skill uses" names exactly three roles — the auditor, the cold reader, and the person — and this document never says whether "a second reader" is one of those three under a new label, a repeat of the closing cold-reader pass, or a fourth participant altogether.
    Guess: guessed it is a fresh cold-reader pass reused for a different purpose, without confirmation.
    Blocking.

22. **"A count above the record fails, and the batch runs again."**
    Where: the census bullet, end of the four post-repair checks.
    What a stranger cannot tell: who reruns the batch — the auditor, an automated process, or the person.
    Guess: assumed the auditor reruns it, by analogy with the rest of the loop.
    Non-blocking.

23. **"the recorded map of a guarded document's anchors, marker lines, numbers, and paths"**
    Where: paragraph defining "the frozen baseline."
    What a stranger cannot tell: what a "marker line" is, as distinct from an anchor or a number. The term appears once and is never defined.
    Guess: read it as a structural line the freeze check watches, such as a heading or a section divider.
    Non-blocking.

24. **"runs the census comparison over every live document"**
    Where: "At the push, `python3 guardrails/check-doc-findings-bound.py` runs the census comparison…"
    What a stranger cannot tell: what makes a document "live" as opposed to some other state. The word is never defined or contrasted with anything in this document.
    Guess: read "live" as "currently tracked in the repository," as opposed to archived or frozen.
    Non-blocking.

25. **"which takes the count before and after each batch, by two different fresh agents"** against **"No record stands behind any build test. … So this skill states no build count."**
    Where: bolded item "The build test measures the work once the audit has closed," immediately followed by the next bolded item, "The method's build-test evidence is owed."
    What a stranger cannot tell: whether the build test described in the first paragraph — with its specific method of "two different fresh agents" taking counts before and after each batch — was ever actually run. The very next paragraph states flatly that no record of any build test exists and names nothing it produced. The two paragraphs read as directly contradicting each other: one describes a measurement as if performed, the other says it was never recorded.
    Guess: treated the build-test method as aspirational only, not as something that happened, based on the second paragraph overriding the first.
    Blocking.

26. **"seeded from the ISO 29148 and INCOSE vague-term lists"**
    Where: the weak-relational-word lint bullet, under "The mechanical lints."
    What a stranger cannot tell: what ISO 29148 or INCOSE are, beyond the document's own gloss ("two published requirements-writing standards"). Neither name is expanded.
    Guess: read them as standards bodies or standard numbers in systems/requirements engineering, without being able to confirm from the page.
    Non-blocking.

27. **"`docs/spec-style.md` states that separation: a writer or reader holding the project's rules is kept apart from one who does not."**
    Where: "The cold reader," paragraph on zero context.
    What a stranger cannot tell: what that separation actually says or why it holds — the document points to a file rather than stating the reasoning here.
    Guess: took the claim on faith without seeing the source text.
    Non-blocking.

28. **"A passing run prints one line saying that the file is clean."**
    Where: "This skill is held to the rules it lists," paragraph on `preshow-register-lint.py`.
    What a stranger cannot tell: by what measure the script calls a file "clean" — no threshold or judge is stated at this specific point (only inferable by piecing together the mechanical-lints section much earlier).
    Guess: read "clean" as "zero findings from the lints described earlier in the document."
    Non-blocking.

Blocking entries: 11 ("A design review of a spec belongs to product-prover" vs. "design-reviewer — judges the design the spec describes"), 21 ("a second reader who puts the old text and the new text side by side…"), 25 ("which takes the count before and after each batch, by two different fresh agents" vs. "No record stands behind any build test… this skill states no build count").
