# The cold-reader prompt, ready to paste

This file belongs to the `text-audit` skill, whose body is [`../SKILL.md`](../SKILL.md). The body defines
a blocking finding. Its section "The cold reader" says who reads under this prompt and what to do with
what comes back.

The prompt names five stop classes a stranger judges from the page alone. The rules at
[`human-prose-rules.md`](human-prose-rules.md) name every other class an audit holds a text to. Judging
those classes needs a rulebook the cold reader does not hold. The prompt's last instruction takes every
other stop the reader met, so a class outside the five still comes back.

Paste the block below verbatim into the cold-reader session, under the body's definition of a blocking
finding, with the text appended.

```
You are reading a piece of text for the first time. You have no background on it: no
project history, no earlier draft, no knowledge of what the author meant beyond the words
on the page. Read it once, straight through, as a stranger who needs to understand it and
act on it.

Mark every place you stop. A stop is any one of these:
- a term used before it is defined, or never defined on the page;
- a relational word — depends, related, handles, based on, corresponds to, proportional,
  larger, sufficient, appropriate, fast, easily — with no stated what, how, or how-much
  beside it;
- a sentence you had to read twice to parse;
- a claim whose ground you cannot find anywhere in the text;
- a judgment word — broken, worth, better, enough, important — with no stated judge or
  measure.

For each stop, write one entry with five parts:
1. the quoted phrase;
2. where it sits (the heading or the opening words of its paragraph);
3. what a stranger cannot tell from the page alone;
4. the guess you made in place of the missing answer;
5. blocking or non-blocking.

Do not fix anything. Report only where you stopped and why. Return the entries as a numbered
list. If you stopped nowhere, say so in one line.

At every relational word, ask the three questions and write which one is unanswered: relative
to what? by what measure? or else what alternative? A word the list above does not name, that
still stopped you, is a real find — report it and note that it is new.

--- TEXT ---
<paste the text here>
```

That last instruction keeps a reader catching words the list does not carry yet. A new slot-opening
word joins the weak-word list, and the skill body's weak-word lint says which copy of that list takes
the edit.
