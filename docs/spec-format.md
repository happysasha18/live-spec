# The spec format — definition

This page defines the requirements genre the spec is written in. A section that follows this page can be read by a stranger on first pass.

## Document structure

A spec document opens with a short preamble: what the document covers, what the bracket codes are, and how the keywords read. A glossary follows. The body is a list of requirements.

Each requirement has three parts, in this order:

1. **Context** — two to four short sentences: when the situation arises, who is involved, what the reader sees.
2. **User Story** — one sentence: as a person in a named position, I want one thing, so that one stated benefit follows.
3. **Acceptance Criteria** — the behaviour, grouped into named cases. A case is one bold line naming a situation, followed by two to six numbered criteria. Every criterion sits in exactly one case, and the numbering runs continuously through the requirement.

## The criterion form

One criterion carries one trigger and one response. The keywords *when*, *while*, *if*, *then*, and *shall* are set in lowercase italics; no word in the document is written in all capitals. The code anchor — `[INV-x]`, `[T-x]`, `[E-x]`, `[M-x]` — trails at the line's end and points to the rule's home in the project spec. A reader can ignore the anchors; a maintainer follows them.

A criterion may carry the pieces of its rule its own line leaves as an indented bullet sub-list under that line. A bullet holds an enumeration of members, a scope note, or a permitted exception — the material that would otherwise weld a second clause onto the line. Each bullet carries one complete clause with its own subject and finite verb, and carries no code anchor: the anchor belongs at the criterion line's end, and a bracket code inside a bullet is a defect. The sub-list ends at the next criterion, the next case heading, the next requirement, or a blank line followed by unindented text. The bullets belong to their criterion, so every gate that reads a criterion's prose reads them too, each bullet as a sentence of its own.

## One criterion, before and after

The example below is one real criterion of this project's own spec, quoted as it stood and as it reads after its repair. Six of its terms belong to the spec's domain and not to the format: a tier is one price level of the models an agent runs on; the seat is the agent session an instruction is given to; a law is a requirement the spec states about how the project works, and the four this criterion names are the orchestration laws; a reminder history is the running count of the times one law has been broken; the problem ledger is the home where those breaks are written down; and the break-record law is the requirement naming that home. The counts below take each bracketed code as one word and a hyphenated name such as pull-unblocked-work as one word.

Criterion 4 of Requirement 233 once read as follows, at 105 words:

> The system *shall* judge the orchestration members carrying a reminder-history of two or more —
> worker-routing (each unit of work routed to the cheapest tier its step and kind allow),
> lean-orchestrator (heavy reading dispatched to a worker rather than held inline), pull-unblocked-work
> (the session keeps pulling unblocked queue work rather than idling), and classify-the-subtask (a
> subtask is the person's or the seat's by what the subtask itself needs, never by the heading it sits
> under) — their breaks recorded in the one home the break-record law names, the problem ledger
> (`PROBLEMS.md`), and *shall* leave the single-occurrence members as reminders until they recur.
> [INV-241, INV-108, INV-69, INV-137, INV-143]

That sentence carries three instructions — judge the laws, record every break in the problem ledger, and leave a law with a single occurrence standing as a reminder — and the definitions of the four laws besides. The definitions are what made it long.

It now reads as follows, at 35 words with the same codes and five items in a list below:

> The system *shall* judge the orchestration laws carrying a reminder history of two or more, and
> *shall* leave a law with a single occurrence as a reminder until it recurs.
> [INV-241, INV-108, INV-69, INV-137, INV-143]
>
> - worker-routing: each unit of work is routed to the cheapest tier its step and kind allow;
> - lean-orchestrator: heavy reading is dispatched to a worker, and none of it is held inline;
> - pull-unblocked-work: the session keeps pulling unblocked queue work instead of idling;
> - classify-the-subtask: a subtask is the person's or the seat's by what the subtask itself needs,
>   never by the heading it sits under;
> - each break is recorded in the problem ledger (`PROBLEMS.md`), the home the break-record law names.

Two instructions stayed in the sentence. Five items moved into the list, one to a line: the four laws, each carrying the words that had defined it inside the sentence, and the instruction that records a break. Taking those definitions out cut the sentence from 105 words to 35.

The repair left every other defect standing, and two of those can be named. The verb judge names neither a standard nor an output, so the criterion never says what the judging measures a law against or what a judgment produces. The threshold two or more names no unit, leaving the word occurrences out. Both classes are recorded as rules of writing — `r32`, a judgment with no judge and no measure, and `r06`, a number standing with no ground — and the criterion itself stands unrepaired in the spec today.

## The laws

1. **Closed vocabulary.** Every domain noun used anywhere in the document has a one-sentence definition in the glossary. A word of ordinary English needs no entry. A coined word is translated to a defined standard term before it enters the document.
2. **One name per thing.** One artifact carries one name everywhere. An artifact referenced twice under two names is a defect.
3. **Context before criteria.** A reader meets the situation and the people in it before the first rule. A term is introduced before its rules use it.
4. **Every judgment names its judge and its inputs.** An evaluative phrase in a criterion — broken, larger than, worth — says who judges and by what. Where the source spec never answers, the criterion names the plainest honest actor and carries a `[GAP: ...]` line under it. Inventing behaviour is forbidden; a gap line is the correct output for a real hole.
5. **Every relational word fills its slots.** Words like proportional, larger, sufficient, appropriate, fast, easily, worth, and adjusted open empty slots: proportional — to what; larger — than what; sufficient — for what. A sentence fills every slot its words open, right where the word stands — the reference point, the measure, or the reason. A slot that cannot be filled gets the alternatives named or a `[GAP]` line. An unfilled slot is a blocking finding.
6. **No history in the spec.** The spec states today's behaviour. Dates, provenance, and the reasons behind past choices live in the journal.

## The comprehension gate

A changed section passes two layers before it ships.

**Mechanical lints first**, each a free script run before any reader:

- the vocabulary check — every domain noun in the text has its glossary entry;
- the one-name check — no artifact appears under two names;
- the style lint — sentence length, no all-capital words outside code anchors, no contrast-by-denial frames, no grading adjectives;
- the criterion-readability ratchet — five arms over the acceptance criteria, one per reading defect the body survey measured: a criterion past the word cap, a term defined in place in a dash-pair aside or a parenthetical, a closing clause with no finite verb, an anchor that competes with the prose, and a criterion whose line and bullets summed run past the total word cap. That fifth arm reads the whole criterion — its line plus every bullet of its sub-list — and reds a criterion carrying several rules while each piece alone reads short. Each arm carries its own threshold and its own recorded count in `guardrails/criterion-readability.json`; a count above the recorded one is red, and a count below it re-baselines;
- the weak-word check — a list of slot-opening words, seeded from the ISO 29148 and INCOSE vague-term lists (appropriate, sufficient, adequate, fast, easily, efficient, flexible, as required, if necessary, proportional, reasonable, robust, seamless, timely, user-friendly, minimal, maximal, several, some) plus the project's own additions; a hit without its reference point nearby is red.

**Then a panel of fresh cold readers**, applied per changed section, until two consecutive reads return zero blocking findings. Each reader reads without project context. At every relational word the reader asks: relative to what? by what measure? else what alternatives? — catching the words the list does not know yet, and each new catch joins the list. The measured pattern behind this gate: every fresh reader finds new blocking terms, fixed items stay fixed, and the finding stream thins toward zero only under consecutive clean reads. Per changed section the gate is cheap: a small delta puts one glossary entry and a handful of criteria in front of a reader, not the whole document.
