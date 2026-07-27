# Wish from the promoter (live-spec campaign) — 2026-07-27

## What happened

Alexander read a page I wrote for him and stopped at this sentence: "требование спорит само с собой до того,
как написан код." He said he did not want to read further — the sentence lost him at that point. He named the
class himself, half joking: "чашки не флуоресцируют, спеки не входят, проверки не краснеют."

## The class

A human-facing text gives an inanimate technical noun a predicate only a person can perform. The reader stops
because the sentence asks them to picture something impossible, and the meaning arrives later, if at all.

Examples from my own texts this week:

- "требование спорит само с собой" — the pass reads the requirement and reports holes in it.
- "просьба входит через одну дверь" — every request goes through the same intake step.
- "проверка обязана доказать, что умеет краснеть" — a check ships with a recorded run in which it failed.
- "спека не отстаёт от продукта" — the spec is updated with every change that lands.

The metaphor is fine inside internal documents where the audience is the pack itself. It fails in any text a
person outside the project reads: a README, a page, a report, a decision page, a chat message.

## The ask

Add this to the text-audit skill as a mechanical check plus a reading rule, and let the pre-show lint carry
the mechanical half:

1. Build a list of predicates that require an animate subject (спорит, обижается, помнит, хочет, устал,
   краснеет, ходит, входит, отстаёт, ловит, наказывает, and their English counterparts).
2. Flag any sentence where such a predicate takes an inanimate technical subject from the project's own
   vocabulary (спека, требование, проверка, тест, гейт, скрипт, конвейер, очередь, запись).
3. The fix is stated as a rule, in one line: name the actor that performs the action, or restate the sentence
   as what the mechanism does.

Alexander asked explicitly that this reach the audit skill, since the pack's own texts carry the same habit.

## Who sends this

The promoter, live-spec campaign window. No changes were made to this repository from here.
