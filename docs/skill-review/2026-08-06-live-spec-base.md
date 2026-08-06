# Skill review — live-spec-base (the budget subsection, read by a fresh head)

`SKILL-REVIEW`

Skill: live-spec-base
Date: 2026-08-06 08:42
Reviewer: a worker session raised for this review alone. It did not author the change under review.
It read the file from its own reading. Base rule 33 asks for that fresh head, and this record answers.

Verdict: the law stands as written, and its home is defensible. Two findings go to the seat. A reader
hunting the numbered rules does not reach the law. The sentence carrying the owner's word states one
permission he did not give, and no surface he reads carries the decision. Nothing was repaired here.
Every finding below is a recommendation.

## What was reviewed

The whole of `skills/live-spec-base/SKILL.md`, with today's delta in focus.

Commit `df4a56d` added the subsection "A budget moves the pace, and never the standard" under "The
settings ladder". It also pointed the `budget.pressure` row of the package-defaults table at it.
Commit `35ced57` rewrote the subsection's closing attribution. It replaced "2026-08-05 ~23:00" with
"2026-08-05 at 22:12 and 22:52", and split the closing clause into two sentences.

## Finding 1 — the numbered rules do not reach the law

The placement is sound in one respect. The law governs one named setting, and that setting's home is
the settings ladder. A reader who looks up `budget.pressure` meets the law in the same section, with
no jump. Rule 4 holds: the law has one home and the table cell points at it.

The reach of the law is wider than the setting. It binds every check the method calls for. It binds
every fresh agent the method asks for. A skill that never opens the settings table is bound by it.

A reader hunting the numbered rules does not find it. The frontmatter promises thirty-five rules in
the body, and the section "The shared rules" holds them. No rule among the thirty-five points at the
subsection. The one pointer sits in a table cell for a single setting. That cell is read by someone
looking up that setting. A reader walking the rules never opens it.

The file's own precedent shows what is missing. "The rule of thinking, above all the rest" is an
unnumbered law too. It sits directly above the rules. It states its standing over them in its own
words, and it names rule 14 as its mechanism inside a code change. The budget subsection does
neither. It sits at the file's end and claims no standing.

The subsection calls itself a rule in its own text: the never-bend list "this rule joins". So the file
names it a rule and places it outside the numbered set, without telling a reader that it did.

Recommendation. Keep the subsection as the law's one home. Add one pointer inside "The shared rules",
at rule 33, whose fresh-head law the subsection leans on. A pointer is not a rule, so the count claim
stays true. The two tests and the four files that assert thirty-five stay green.

On the numbered form. The prior record gave the sweep cost as its reason against rule 36. That cost is
a fact about one worker's write-set. It settles nothing about the right home. If the seat judges the
numbered form right, the sweep is a lane of its own. Base rule 14 already says a class is swept whole.

One accuracy note rides here. `README.md` tells a reader that the pack holds thirty-five shared rules
across the skill set. A shared law now stands outside that count. The number is true of the numbered
set, and the sentence reads as the whole set.

## Finding 2 — the attribution states one permission he did not give

I read the session transcript through `scripts/session-extract.py`, session `e1225a25`. It returned 44
human turns, and his turns at both cited moments are in it.

At 22:12 he named the smaller plan and asked the session to move carefully on the smaller sum. He
asked for new workers where they save context and where they pay for themselves. A required fresh
worker he called no question at all, his own example being an adversarial review. Quality would suffer
otherwise, he said. At 22:52 he said that quality never suffers, whatever else does.

So two parts of the attributed clause are his. The smaller plan costs less is his. Quality never drops
is his, close to the words he used. "May run slower" is in neither turn. It is the session's own
inference, and it sits inside the colon clause that a reader takes as his word. INV-207 asks for a
sentence the pack reasoned out to stand in the pack's own voice.

Recommendation. Drop the pace clause from the attributed sentence, or move it into the paragraph's own
voice. The paragraph already says that a rung sets how fast and how cheaply the work runs, so the law
loses nothing.

Two moments and one sentence. A reader cannot tell which clause came from which moment. `DECISIONS.md`
already assigns his 22:52 turn to the ship-bar decision. Recommendation: one clause per moment, so
each timestamp carries what was said at it.

The parts the session derived are correctly outside the attribution, and that is the delta's strongest
move. Three of the four named asks are the session's own: a cold reading, a release re-prove, and a
deep spec-and-architecture audit. Only the adversarial review is his example. All four stand in the
pack's voice, where a reader may challenge them.

## Finding 3 — the decision reaches no surface he reads

INV-207 names the read-back as the real defence against a dated attribution. `DECISIONS.md` shows him
what the pack believes he decided, on his own clock, and he strikes what he never said. The gate
catches an attribution with no anchor, and it cannot catch a wrong one that carries a real date.

No entry in `DECISIONS.md` records this decision. The only place his word carries this law is the
skill body, and the read-back never shows him the skill body. So the one correction path INV-207
relies on cannot reach the sentence finding 2 flags.

Recommendation: an entry on the decision record for the budget law, naming its exchange.

Roadmap row 550 was queued this morning on his own word. It asks an entry recording his word to carry
the words themselves and a pointer to the exchange. This sentence carries neither. When the row lands,
this line is among the entries it reaches. His words were Russian and the pack writes its documents in
English, so the row's landing owes a form that serves both. Naming it here so the row's owner meets
the question early.

## Notes

The four asks read as a closed set. The sentence before them states the class, and then "Four such
asks are" reads as the whole of it. The file's own opening law says a list is the wrong answer to a
class. A wording such as "Among such asks are" would keep the four as examples.

The fresh-agent sentence carries no code. Rule 33 and INV-46 own the fresh-head law, and the
subsection restates a piece of it without pointing home. A pointer there also closes finding 1.

The word ladder now carries three senses in one file: the settings ladder, the economy ladder, and a
test ladder with rungs of its own. This is older than the delta, and a reader hunting one of them
meets three.

The frontmatter description still says the file is the one home for the rules and for the settings
ladder. The ladder now holds a law as well as its settings. A skill's description is its trigger
surface, so the line is worth revisiting once the placement question closes.

Standing, and not this delta's doing: the body runs past 745 lines, and the skill-creator guide holds
a body near 500. A split into reference files is a milestone's question, and no landing closes it.

## Checks run

- `git show df4a56d` and `git show 35ced57`, both scoped to the skill — the delta read in full.
- `scripts/session-extract.py --session e1225a25` — 44 human turns; the turns at 22:12 and 22:52 read.
- A grep for pointers into the subsection — the `budget.pressure` cell is the only one.
- A grep for the count claim — two tests, `README.md`, and three skill files assert thirty-five.
- `DECISIONS.md` read for an entry on the budget law — none stands.
- `python3 scripts/rule-census.py` over this record — zero findings.
