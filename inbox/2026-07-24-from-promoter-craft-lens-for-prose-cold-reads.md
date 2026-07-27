# Wish (from-promoter): a craft lens for the cold reader, gated to prose and messages

**The item.** Alexander's word on the promoter window, 2026-07-24: the text-audit cold reader checks
whether a stranger UNDERSTANDS a text. He watched two versions of the same social post — the agent's and
his own — both pass comprehension sentence by sentence, yet his landed and the agent's read flat. He asks
whether the cold reader could carry a second lens that fires for prose and messages and stays off for a
spec: "может это хорошо для всех холодных читателей если это НЕ спека. в спеке такое не надо, а если тексты,
или сообщения то иногда надо такое."

**The evidence (today, concrete).** A Telegram teaser for a published essay, written twice.

- The agent's draft and Alexander's rewrite were each clear at the sentence level. An earlier cold-reader
  run on the agent's versions caught real comprehension blockers — an undefined load-bearing term
  ("непрерывной персонализации"), and one act named by three drifting words (верификация → проверит →
  оценить). Those are the classes the audit already owns.
- What no lens caught: the agent's version was understood and still weak. His rewrite beat it on five craft
  moves the current cold reader has no question for:
  1. a concrete image closes every abstraction ("цифровой актив, который мы просто достаём по запросу", not
     a bare "актив");
  2. a claim carries its example in the same breath (cost shifts to verification, shown at once by a table
     booking that is easy to validate and a software architecture that is a bottleneck);
  3. the teaser ends by naming what the essay delivers (which interfaces keep visual form, how the ecosystem
     changes, who controls routing), so a reader has a reason to click;
  4. qualifiers that carry no weight are cut (he deleted the exact undefined term the cold reader had
     flagged);
  5. the opener leads with information in the present tense, with no hedge.

**The proposal.** Add a KIND-gated craft lens to the cold-reader pass. When the text kind is persuasive
prose, a message, or marketing copy, the reader also reports craft stops:

- an abstraction with no concrete image beside it;
- a teaser or opener that concludes the argument in place of naming what the piece delivers;
- a qualifier that adds no weight (the reader can drop it and lose nothing);
- a metaphor that clashes with another image in the same text (a mixed metaphor);
- a low-information or hedged opener where a declarative, high-information one would carry.

For a spec this lens stays off. Dry precision is correct there, and "make it vivid" would be a defect. The
audit already switches on text kind — it skips requirement-shape for a non-spec — so this lens keys off the
same switch.

**Design notes for the pack.**

- A craft stop is usually non-blocking for comprehension and blocking for the text's JOB (to make a reader
  act). The class may want its own severity — "weak for its purpose" — separate from "a stranger cannot
  understand it", so the comprehension loop still closes on its own terms.
- The lens reports; it does not rewrite. Taste and a voice stay the person's, and the marketing skills.
  This lens names mechanical craft classes only (image-for-abstraction, payload-teaser, empty qualifier,
  mixed metaphor, opener), and leaves the rest to the human.
- Home is the pack's call. The lens could live in text-audit behind the kind gate, or as a cold-reader
  variant the communicator and the marketing skills invoke. Alexander framed it as good for "all cold
  readers" on prose, so a shared home fits.

**Why (what was missing).** Comprehension and persuasion are two different failures on one page. The audit
owns the first today. For any text whose job is to make a reader act, the second failure ships silently, and
the human catches it by rewriting many times over — his words this session, "задолбало по 200 раз
переписывать спотыкаясь на каждом слове." A pack that reads the craft failure mechanically, for prose only,
turns those rounds into one pass.

**Who threw it.** The promoter window (cwd ~/promoter-alexander-articles), relaying Alexander's idea.
Authority is his; the concrete evidence and the framing are mine, offered for the pack to think against.
