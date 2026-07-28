# Owner read, 2026-07-28 — the text-audit skill, read one

The reader was this project's owner, reading `skills/text-audit/SKILL.md` in a browser. He holds the
project's whole history, so he is no cold reader. English is his second language, and he read it as a
working professional reads a document handed to him.

This reading counts as findings and counts toward no clean read. The two clean readings the audit
loop closes on are still owed, and they need readers who hold nothing.

Text read: `skills/text-audit/SKILL.md` at commit 84f74bd, measuring zero on the mechanical floor.
Stops: 6, all blocking. One rule proposal came back with them.

The file had never been read by anyone. Its own loop has four steps, and step one, the mechanical
lints, is the only step that ever ran on it. The file that defines the reading loop went to a reader
without going through that loop.

---

## Stops

**1.** "together with the settings ladder"

The reader asked whether this group of four has a name, and whether that name sits in the glossary.
Both are true: `settings ladder` is defined in `PRODUCT_SPEC.md` at line 212 as the four nested
scopes that resolve a setting. A skill file is read on its own, and its reader never opens
`PRODUCT_SPEC.md`. The term stands with no path to the place that defines it.

Class: a glossary term used in a file that is read apart from the glossary.

**2.** "This skill points at them and covers only its own subject."

The sentence before it already places the shared rules in the base skill. The reader asked whether
this sentence carries anything more.

Class: one fact stated a second time in another place (rule r56).

**3.** "When it fires"

The reader named the heading wrong. `fires` is this project's verb for a skill triggering, and the
heading hands it to a reader who has met it nowhere.

Class: a coined word standing where a plain standard word exists (rule r02).

**4.** "The trigger is a person asking whether a reader will understand the text"

The reader asked whether an agent triggers it too. Line 30 of the same file says "Load it when a
human-facing text is about to ship", and that is an agent's trigger.
`skills/communicator/SKILL.md` points at this skill as the home of the reading loop. The file names
two triggers and lists one.

Class: a text breaking a rule it states (rule r09).

**5.** "It grades no voice, and it rewrites no style beyond those rules."

The reader could not tell what the sentence rules out. `grades` and `voice` both leave the reader
guessing, and the sentence names the skill's boundary by denying a neighbour.

Class: a thing named by denying its neighbour (rule r10), carrying two words with private meanings
(rule r01).

**6.** "Per changed section the loop is cheap."

The reader stopped on `cheap` and asked what it is measured against. He stated the rule behind the
stop: a criterion goes into a text with its limits and its range, or it stays out.

Class: a judgment with no judge and no measure (rule r32).

---

## The rule the reader proposed

A sentence takes the everyday word where an everyday word carries the meaning. A rare or bookish word
stands only where no everyday word says the same thing. The reader of these documents is a working
professional whose first language is something other than English.

The lower bound belongs in the rule as well. A term of the profession stays a term: requirement,
invariant, gate, criterion. The words around the term are the ones that come down.

The reader set one condition on the mechanism: no word list maintained by hand. A published frequency
list of English is acceptable, because nobody updates it here.

---

## Answers

**1. What did this reading prove about the machine floor?**

A file measuring zero on the floor stopped its reader six times. The floor counts sentence length,
style patterns, and register patterns. It counts none of the six classes above.

**2. Which of the six were already written as rules?**

Five: r56, r02, r09, r10 with r01, and r32. One is new, the vocabulary rule the reader proposed.

**3. Why did the five written rules catch nothing?**

The rule file holds 55 rules. 23 of them are held by a catcher, and almost every catcher runs on chat
text through a session hook. Over a file that ships, the same rules are run by a person by hand.

**4. Sort**

BLOCKING (6): 1, 2, 3, 4, 5, 6.

**Total stops: 6.**
