# The language defects

This document holds the ways live-spec's own texts stop a reader, paired with the rule that closes each
one. It covers every text a person reads: the product spec, the architecture document, the README, a
decision page, a report, a message in chat.

A *defect class* is a mistake that shows up across many sentences. Repairing the sentence in front of a
reader leaves the rest of them standing. Each class below carries one name for the mistake. A writer then
finds every instance, and a reader says which class a stop belongs to.

## Where these came from

Two readers were given text with no context on 2026-07-27 and asked one question: where they stopped.

The English reader was given six requirements from `PRODUCT_SPEC.md`, with its Glossary section held
back. Any host project that adopts live-spec keeps its own glossary the same way, at the head of its own
spec. The grammar held and the structure read as professional. The text ran on ordinary English nouns
carrying jobs only this project knows: seat, net, door, home, walk, lens, handle, frame, law, tier.
It also used "red" as a verb, meaning to report something as a failure. Of the six requirements, the
reader could implement two from the text alone and one after asking the author questions. Three were left
undone, since the lists and default values those rules depend on were never given. Two of the missing
lists are named in class 7 below: the inline pattern list and the six file-dump verbs. This document does
not name the rest. The longest sentence ran 107 words, counting
whitespace-separated tokens including its trailing anchors. That is more than four times the 25-word
length above which a sentence is flagged for a look (class 8, below). It carried four term definitions
inside one instruction.

The Russian reader was given six paragraphs of working chat: twenty stops in about 250 words. The words
guessed wrong or not at all were ноги, руки, полоса, якоря, работники, засеяна, храповик, перебазируется,
живость, ссылки, отступили, остаток. Each is Russian grammar carrying an English dictionary. That reader also
named two habits without being asked: things act like people, and one thing carries two names in
neighbouring sentences.

The owner then read a first rewrite drafted in chat, applying these rules, and stopped six more times.
Two of the six are shown below, under the rule against publishing a text that contradicts a rule it
states.
This document does not carry the other four; the writer records a stop here only once its source keeps
producing it.

## The one demand

A reader owes the text nothing. The writer must give the reader every word, number, or list the writing
depends on.

Every word, number, or list a sentence depends on is given where used, or in one place the sentence
points to by name. The eight classes below hold the named ways writing falls short of that demand.

The first four are about names. The fifth is about who acts. The sixth and seventh are about ground the
text never gave. The eighth is about the shape of a sentence.

---

## 1. An ordinary word carrying a private job

An everyday word is handed a meaning only this project knows. The reader recognises the word, builds the
everyday picture, and reads on. The mistake surfaces three sentences later, or never. The reader does
not know they have stopped, so the writer never learns of it.

| Written | Repair |
| --- | --- |
| `the seat` | the session doing the orchestrating |
| `red a violation after the fact` | report the violation as a failure once the turn ends |
| `the net-liveness meter` | the count of how often each check ran and how often it fired |
| `door` | the entry point a queued request is classified into before any code is written: feature, bug, refactor, docs-only, or skip |
| `walk` | the pipeline's own path for one queued request, from capture to landing |
| `lens` | one named check a document is read against, testing one concern |
| `tier` | the model level a piece of work runs at: a one-shot worker, a multi-step worker, or the session doing the orchestrating |
| `handle` | an internal identifier that trails a human-facing line instead of opening it: a spec code, a row or session number, or a coined name |
| `law` | a standing rule the pack holds conduct to, judged after the fact rather than issued as a one-time instruction |
| `frame` | no single meaning across the project. It appears inside three compound terms: `offering-hedge frame`, `touchpoint-kind frame`, `contrast-frame`. Only `offering-hedge frame` is defined again in this document, below; the other two live only in other project files |
| `храповик записал порог` | the script wrote the threshold down |
| `живость проверок` | how often the checks actually run |
| `ноги` | the acceptance criteria and open items under a requirement |
| `руки` | the parts of a check |
| `якоря` | the bracketed codes trailing a line; the plain Russian is «коды в конце строки» |
| `работники` | the helper processes the session dispatches |
| `засеяна` | the starting numbers were recorded |
| `перебазируется` | the recorded limit is lowered to the new measurement |
| `ссылки` | the branch and tag references kept in git |
| `остаток` | what is still undone on an item |

The Russian list above carries the same defect into another language. Each word there is an
English term translated straight into Russian, one word at a time. The result is a real Russian word
that a Russian reader cannot connect to any meaning this project gives it.

**The rule.** A word keeps its everyday meaning. A term this project needs holds one glossary entry, and
the body then uses it with no definition attached. A sentence carries at most one such term. In another
language, name the thing the way a working engineer in that language names it. Where that language has no
such word, describe the thing in a short phrase. A term is never carried across word for word.

**Caught by.** The known-words list in `guardrails/spec-coinages.json` catches a known word in a second. A model reading can flag a
common noun used as a term of art, with noise. A word nobody has caught yet is found by a person reading
with no context, and by nothing else.

---

## 2. An invented name standing where a working name exists

The project mints a word for a thing the industry already named. The reader who knows the industry word
is now guessing whether this is the same thing or a different one.

| Written | Repair |
| --- | --- |
| `lane` | branch |
| `home` (of a fact) | the file that holds the fact |
| `leg` (of work) | an open item |
| `полоса` | branch |
| `хвост без глагола` | none |

The last one has no repair, because it points to nothing. The owner's answer: there is no such thing as a
tail without a verb; that phrase is invented. A minted name can point at an object that does not exist,
and the writer may never notice.

**The rule.** Where the industry has a word, write the industry's word. Where nothing exists, describe the
thing in plain words. Mint a name only when the description would repeat often enough that the name saves
the reader work. A minted name gets a glossary entry the first time it appears.

**Caught by.** A list of pairs catches a pair already known (`lane` → `branch`). A person decides whether
to keep a minted name and whether it points at a real thing. A model that knows the industry vocabulary
can propose candidates and is wrong often enough to need a reader.

---

## 3. Nouns stacked as a name, with the relation unstated

Two or three nouns are pushed together into a name, and the relation between them is left for the reader
to guess. `chat-law reminder` — a reminder about the chat laws, a reminder the chat laws produce, or a
reminder stored beside them? All three readings are grammatical.

| Written | Repair |
| --- | --- |
| `chat-law reminder` | the text that repeats the chat laws in every prompt |
| `reminder-history` | how many times this law has been broken before |
| `break-record law` | the rule for where a broken law is written down |
| `offering-hedge frame` | a phrase that offers to do something the session could already do |
| `worker-dispatch count` | how many workers the session has dispatched |

**The rule.** A name holds one noun. Where two nouns must appear together, a verb or a preposition
between them carries the relation.

**Caught by.** A machine finds every stacked name that has no glossary entry. That candidate is a
hyphenated compound, or two nouns in a row used as a name. Whether the relation is carried is then a
short human read, or a model read for volume.

---

## 4. Two names for one thing

A writer gives one object a second name a sentence later. The reader then spends effort deciding whether
two things are in play.

Requirement 232 of the product spec uses four words for its objects within three sentences:

- **signal** — the title's category word for both checks, in "Two Stop-hook soft signals"
- **gate** — the title's name for the first check, in "the hedge gate"
- **arm** — the title's name for the second check, in "the lean-orchestrator arm"
- **net** — the glossary's own word for any hook or guard, reused in the user story's "each law backed
  by a cheap literal net"

Three of the four are Requirement 232's own words for two checks: one category and two instances. The
fourth is the whole spec's word for any hook or guard, defined in the glossary and reused here. A reader
who has not read the glossary cannot sort the four into two groups.

The writer repeated the same mistake in the Russian chat, in two neighbouring sentences: «пуш-удаление»
("a deletion push") and «удаляющий пуш» ("the push that deletes").

Repair: keep `net` for the glossary's own term, and use one shared word for the category and its two
instances. `Two Stop-hook checks: the hedge check and the lean-orchestrator check.`

**The rule.** One thing, one name, in every sentence, from the first use onward. A reader takes a
different word as naming a different thing.

**Caught by.** A machine, once the pair of names is known — `guardrails/check-one-name.py` reads the pairs
from `guardrails/one-name-aliases.json` and blocks. A pair nobody has recorded yet is found by a person
reading, or by a model asked to group the nouns in a section.

---

## 5. An action its performer cannot perform

The subject of the sentence cannot do the verb. A document does not remind. A law is not judged. An
anchor does not stand. A number does not show. Every one of these came from the owner reading a sentence
and stopping on it.

| Written | The owner's answer | Repair |
| --- | --- | --- |
| `The system shall judge an orchestration law` | a law is kept, established, or enforced | The conduct judge — the model call reading the turn's action trace against the orchestration laws — reports any law the turn broke |
| `The reminder shall name four laws` | a reminder does not name laws and does not remind them | The prompt carries the four chat laws that `hooks/register_judge_core.py` names in `UNIVERSAL_CHAT_LAW`, written out |
| `The system shall inject a reminder of the chat laws` | how can a reminder be injected, and what for | The hook adds the four chat laws that `hooks/register_judge_core.py` names in `UNIVERSAL_CHAT_LAW` to the start of every prompt |
| `Якорь стоит в конце строки` | an anchor cannot stand | The anchor is written at the end of the line |
| `сегодняшние числа показывают красное` | a number does not show | The measured count stands above its recorded limit |
| «проверки отступили» | no answer recorded | we stopped running the checks |

Here the writer hands a human action to a thing that cannot perform it. The true actor (a hook, a script,
a person) goes unnamed. The repair gives that actor a name.

**The rule.** The subject of a sentence performs the verb. Where a thing cannot perform the verb, name the
actor that can: a person, a script, a hook, a model.

**Caught by.** A model reading each sentence. A machine holds a list of verbs of intention: decides,
wants, remembers, reminds, argues, judges, speaks, retreats, shows. It flags each one whose subject is a
document, a rule, a number, or another thing. That pass finds the common cases and misses the rest, so
the machine stands as a first look and the model does the reading.

---

## 6. A number with no ground

A number arrives with no reference point and no direction. The reader cannot say what it was measured
against, which way is better, or whether anything measured it at all.

- `a reminder-history of two or more` — the owner asked why twice. Repair: *a law broken twice or more.
  One break can be an accident; a second is a pattern. This threshold was chosen, and no measurement
  fixed it.*
- `defaulting to 50 kibibytes` — the reader cannot tell whether that is a lot. Repair: *50 kibibytes of
  file content held in the session. A host changes this value in its config. No measurement chose it.*
- `469 cases` — the Russian reader's stop: the number gives no sense of whether more is better. Repair:
  *469 test cases pass, up from 431 last week; higher is better.*

The same demand covers a rule stated with no reason. The owner asked why a law stays a reminder until it
recurs. That is the same reader asking the same question about a number that was never grounded.

**The rule.** Every number carries what it counts, what it is compared against, and which direction is
better. Where a number was simply chosen, the writer says so.

**Caught by.** A machine finds every bare number and checks its sentence for a reference cue. The
mechanism already runs in `guardrails/check-weak-words.py`, which reads its cue list from
`guardrails/weak-words.json`. Whether the ground given is real ground is a person's or a model's read.

---

## 7. A rule that points at a list it never gives

The sentence refers to a set with a definite article: the pattern list, the six verbs, the threshold, the
standing laws. The members of that set never appear. The reader can follow the grammar and cannot follow
the rule. This is why the English reader could implement two of six requirements and left three undone.

- `matching against an inline universal pattern list` — the patterns are never shown. Repair: give the
  patterns as a list under the criterion.
- `one of six literal file-dump verbs` — the six verbs are never named. Repair: name them.
- `the standing orchestration laws` — repair: list them where the rule stands, or point to the section
  that lists them, by its heading.

**The rule.** A rule that depends on a list gives the list, or points by name to the one place that holds
it. The word "the" in front of a set is a promise to the reader that the set has been given.

**Caught by.** A model reading, since the reference can be phrased any way. A machine can find the shape
"the … list/set/laws/verbs/threshold" and hand every hit to a reader. That is cheap and noisy.

---

## 8. A sentence carrying a rule and its definitions at once

One sentence carries an instruction together with the definitions of the terms it uses, in dashes and
parentheses. Length is the symptom. The cause is that each borrowed word carries its own definition into
the sentence.

The longest such sentence in the whole product spec is criterion 4 of Requirement 233 in
`PRODUCT_SPEC.md`, at 107 words by the count above. It carries four term definitions inside one rule,
quoted here whole so the count and the four terms can both be checked. Each bracketed code such as
`[INV-241]` names one invariant; `PRODUCT_SPEC.md` lists every one in its closing code-to-location table.

> The system *shall* judge the orchestration members carrying a reminder-history of two or more —
> worker-routing (each unit of work routed to the cheapest tier its step and kind allow), lean-orchestrator
> (heavy reading dispatched to a worker rather than held inline), pull-unblocked-work (the session keeps
> pulling unblocked queue work rather than idling), and classify-the-subtask (a subtask is the person's or
> the seat's by what the subtask itself needs, never by the heading it sits under) — their breaks recorded
> in the one home the break-record law names, the problem ledger (`PROBLEMS.md`), and *shall* leave the
> single-occurrence members as reminders until they recur. [INV-241, INV-108, INV-69, INV-137, INV-143]

The owner's own reading of it: could most of this be bullets. It can:

> The judge watches four rules. Each rule is added once it has been broken twice.
>
> - **worker-routing** — each unit of work goes to the cheapest model that can do it.
> - **lean-orchestrator** — a long read goes to a worker.
> - **pull-unblocked-work** — the session takes the next unblocked item while any remains.
> - **classify-the-subtask** — a subtask belongs to whoever the work needs, whatever heading it sits under.
>
> A break is written to `PROBLEMS.md`. A rule broken once stays a reminder.

**The rule.** One sentence carries one rule and no definitions. A sentence over 25 words is flagged for a
look; that number was chosen with no measurement behind it. Definitions live in the glossary. A set of
parts is written as a list, one part per line.

**Caught by.** A machine checks each sentence end to end: word count, dash-bounded spans, and comma-joined
items, against the 25-word mark given above. The document the readers stopped on had its longest sentence
at 107 words.

---

## The writer holds a text to the rule it states

That chat draft contradicted its own rules twice, and the owner caught both.

- One sentence carried the rule "one trigger and one duty per sentence," in private vocabulary of its
  own: «триггер», «обязанность». That sentence belongs to class 1.
- Another sentence carried the rule «Внутри критерия определений нет» ("Inside a criterion there are no
  definitions"). That rule points at an absence, in words the owner could not read. That same passage
  carries a rule against minted names, and a minted name of its own: «хвост без глагола» ("a tail with no
  verb"). The phrase points to a thing that already has an ordinary name: a closing clause with no finite
  verb. The owner's own words: there is no such thing as a tail without a verb. This belongs to class 2.

**The rule.** Do not publish a text that contradicts a rule it states. The sentence carrying a rule is the
first test of that rule.

**Caught by.** A person. A model asked to hold a document against its own stated rules finds some of it. A
literal pattern finds none of it.

## What catches what

| Class | Machine | Model | Person |
| --- | --- | --- | --- |
| 1 — private job for an ordinary word | known words only | candidates, noisy | every new one |
| 2 — invented name for a named thing | known pairs only | candidates | whether to keep it |
| 3 — nouns stacked as a name | finds every candidate | judges the relation | settles a hard case |
| 4 — two names for one thing | recorded pairs, blocking | proposes new pairs | confirms |
| 5 — an action its performer cannot perform | common verbs only | yes, this is its class | confirms |
| 6 — a number with no ground | finds the number and the missing cue | judges the ground | judges the ground |
| 7 — a rule pointing at a list it never gives | noisy shape match | yes, this is its class | confirms |
| 8 — a rule and its definitions in one sentence | yes, end to end | — | confirms the split |
| the rule about a rule | — | partly | yes |

A dash marks a checker that plays no part for that class; every other cell holds an active role.

The honest boundary: no machine and no model finds a *new* class. Both re-catch what a person already
caught once. Every class in this document exists because a human being stopped on a sentence and said so.
That is the only source, so a project must plan and fund human cold-reading time as a standing cost, not
a one-time setup step.

## How a class gets into this document

1. A person reads a text with no context and stops on a sentence. The stop is recorded in their words,
   including the wrong guess they made.
2. The wording is traced back to the artifact that taught it. That source may be a skill file, a
   template, a spec section, or a chat habit the writer picked up. The writer records a class here once
   its source keeps producing the same stop.
3. The class is written here: a name, a definition, and the rule. It also carries the stops that produced
   it, each with its repair beside it, and how the class is caught.

A repair applied to one sentence and nowhere else means step 2 was skipped.

## The word list

`guardrails/spec-coinages.json` holds the caught examples so a known offender is stopped in a second. This
document holds the rule, and the reason it counts as an offender.

## Eight questions for a sentence

1. Does any everyday word here carry a job only this project knows?
2. Does any minted name replace a working name that already exists?
3. Does any name stack two nouns without carrying the relation between them?
4. Does this thing have a different name a few sentences away?
5. Can the subject of each verb perform that verb?
6. Does each number carry what it counts, what against, and which way is better?
7. Does every list this sentence depends on appear, or point somewhere by name?
8. Does this sentence carry one rule and no definitions?
