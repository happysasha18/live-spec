# The rules a human-prose audit holds a text to

This file belongs to the `text-audit` skill, whose body is [`../SKILL.md`](../SKILL.md). That body
defines a surface and a register, and it says when a text is held to the rules below.

The rules below are the whole set a human-prose audit holds a text to. They are edited in one file,
`guardrails/language-rules.json`, in the live-spec repository.

`scripts/gen-language-consumers.py` builds four artifacts from that one file:

- the writer's page, `docs/language-rules.md`;
- the maintainer's page, `docs/language-rule-coverage.md`;
- the rule text the judging model reads, `hooks/language-laws.json`;
- the block below.

Two of those pages carry more than this sheet does. `docs/language-rules.md` gives each rule with its
examples, its exceptions, and its thresholds. `docs/language-worked-example.md` walks one short document
end to end against these rules, and names the rule at each fix.

<!-- generated:human-prose-rules — scripts/gen-language-consumers.py owns the block below -->

## The rules this audit holds human prose to

Every rule below binds human prose, which is text a person reads to understand something or to decide something. A README, a decision page, a report, a skill's own body, and a documentation page carry it. So do the prose paragraphs inside a spec. A documentation page carries `artifact` as well once it is published outside the project.

This block prints 48 of the 62 rules the source carries. A code missing from the run below belongs to a rule binding other surfaces only, or to a retired rule whose code left the set. A rule binding human prose may also bind chat, a commit message, or a worker brief. Its recorded case may come from one of those surfaces.

They are printed here out of `guardrails/language-rules.json`, which is where each one is edited. A change made in this block is overwritten by the next run of `scripts/gen-language-consumers.py`.

Each entry names the class of mistake, states the rule, gives the question to ask of a sentence, and carries one recorded case under it. The case shows written text on the left. The right side shows its repair, or an instruction where the repair depends on facts the case does not carry. Every case the class was built from lives in the rule home.

- **an ordinary word carrying a private project meaning** (`r01`)
  A word keeps its everyday meaning. A term this project needs holds one glossary entry, written in plain words. The body then uses that term unchanged, with no definition attached.
  *Ask:* Would a person outside this project recognize this word, or does the text gloss it in plain words where it first appears?
    - `The system shall red a branch whose merge-base sits behind main's tip.` → `The system shall refuse a branch whose merge-base sits behind main's tip.`
- **a coined, loan-translated, or respelled word standing where a plain standard word exists** (`r02`)
  Where the industry has a word, the text writes the industry's word. A term this project coined is replaced by the standard word, or defined where it first appears. In the reader's own language, a term is written as a real word of that language.
  *Ask:* Does a standard word already name this thing? Is the word used here that standard word, written as a real word of the reader's own language?
    - `the door` → `the entry point`
- **a name stacking two nouns with no relation between them** (`r03`)
  A name holds one noun. Where two nouns belong together, a verb or a preposition between them carries the relation.
  *Ask:* Does this name run two nouns together, and can a reader say how the second relates to the first?
    - `chat-law reminder` → `the reminder that carries the chat laws`
- **one thing answering to a second name** (`r04`)
  One thing carries one name in every sentence, from its first use onward.
  *Ask:* Does any thing named here appear under a different word somewhere else in this document or its neighbours?
    - `the mechanical checks, in the README, for the step the skill body calls the mechanical lints` → `the mechanical lints, in both places`
- **a predicate applied to a subject that cannot carry it** (`r05`)
  A verb or an adjective attaches to a subject that can carry it. Where the subject cannot act, the sentence names the actor that can: a person, a script, a hook, or a model.
  *Ask:* Can the thing this sentence names as its subject perform this verb, or hold this quality?
    - `the numbers do not show red` → `name the actor that shows a colour, or state what the numbers do`
- **a number standing with no ground** (`r06`)
  Every number says what it counts, what it is compared against, and which direction is better. A number chosen rather than derived says that it was chosen.
  *Ask:* Can a reader say what this number is measured against and which way is better?
    - `the register targets 15-25 words, and a sentence past ~25 words is a hit` → `a sentence stays between 15 and 25 words, and one past 25 is a hit`
- **a set pointed at by a count, a pointer, or a position, with its members never given** (`r07`)
  A sentence that depends on a set gives that set, or points by name to the one place holding it. A part of a set is named by what its members are.
  *Ask:* Can a person who reads this sentence alone name the members of the set it points at?
    - `**Case: the three legs**` → `**Case: the prototype-reference leg, the completeness scan, and the behaviour-traces-to-spec check**`
- **a sentence carrying more than one rule, running past its word cap, or piling up clauses** (`r08`)
  One sentence carries one rule and no definitions. It stays under the word cap for its surface, and it holds at most one subordinate clause.
  *Ask:* Does this sentence state one rule a reader could cite on its own? Does it stay under the cap for its surface? Does it hold its subject in view from its first word to its last?
    - `the orchestration law that the session keeps pulling unblocked queue work while any remains.` → `state the law in one short sentence, and put its parts in a list`
- **a text breaking a rule it states** (`r09`)
  A text ships once it obeys every rule it states. The sentence stating a rule is the first place to check that rule.
  *Ask:* Does the sentence stating this rule obey the rule it states?
    - `a 62-word sentence inside the file that states the 25-word cap` → `the same rule in three sentences, the longest of them 41 words`
- **a thing named by denying its neighbour** (`r10`)
  A sentence says what a thing is, in its own words. A boundary worth naming gets its own plain sentence.
  *Ask:* Does the denied half give the reader anything the reader did not already have?
    - `X, not Y` → `Say what the thing IS in its own sentence`
- **an internal code leading a sentence to the reader** (`r11`)
  Plain words carry the meaning, and an internal code trails. In chat the code sits in parentheses at the sentence's end. In a document it sits in square brackets at the line's end.
  *Ask:* Does the sentence still carry its meaning with the code removed, and does the code stand anywhere other than at the end?
    - `INV-141 gives the design review a pass of its own.` → `The design review runs as a pass of its own [INV-141].`
- **a word grading how important or how good a thing is** (`r12`)
  A text states what a thing is or does, and lets the reader weigh it. A word grading importance or quality stands only beside a concrete fact.
  *Ask:* Does this sentence tell the reader how much to care about what it reports?
    - `Two constraints, and they are hard ones.` → `Two constraints.`
- **a sentence grading the person, or grading the writer's own act** (`r13`)
  A remark from the person is answered, and the answer says what follows from it. A text lets its own honesty and rigour show through what it reports.
  *Ask:* Does this sentence carry a fact, or a verdict on the person's remark or on the writer's own work?
    - `good question` → `answer it, and say what follows from the answer`
- **a sentence carrying no information** (`r14`)
  Every sentence shown to the person advances the finding, the decision, or the action. A sentence carrying a fact the reader would otherwise lose stays, however short.
  *Ask:* Does the reader do anything differently because this sentence is here?
    - `Its whole job is to mark where it stopped, what it guessed, and why.` → `deleted, since the two sentences above it already say this`
- **a word inflating a statement while adding nothing** (`r15`)
  A word earns its place by adding information. A phrase whose deletion changes nothing is deleted.
  *Ask:* Does removing this word change what the sentence says?
    - `really` → `delete`
- **the language each surface is written in** (`r18`)
  Documents, commits, code, and artifacts are written in English, and conversation runs in the human's pinned language.
  *Ask:* Is this text in the language its surface is pinned to?
    - `a commit message in Russian, in a repository whose documents are pinned to English` → `the message in English, with the conversation about it staying Russian`
- **English that reads as compressed or poetic** (`r20`)
  English in a document or an artifact reads like a native technical writer: short subject-verb-object sentences, common words, and no poetic compression.
  *Ask:* Could a native technical writer have written this sentence for an open-source project?
    - `the sketch itself carries the look` → `name the actor and say plainly what it does`
- **a word standing in all capitals** (`r23`)
  Every word is written in ordinary case. Force comes from the declarative statement itself.
  *Ask:* Is this word in capitals because it is a name the project has defined, or to make the sentence louder?
    - `CHANGES` → `changes`
- **the person an explanatory sentence speaks in** (`r25`)
  Explanatory text addresses the reader as `you` for what a person does, and names the component for what software does.
  *Ask:* Does this sentence tell the reader what they do, in words spoken to them?
    - `one` → `you`
- **a sentence with no actor, or its action buried in a noun** (`r26`)
  A rule sentence says who does what and when, in the active voice with a named actor. Its action lives in a verb.
  *Ask:* Does this sentence answer who does this, to what, and when? Does its action live in a verb?
    - `the verification of the claim occurs` → `the suite verifies the claim`
- **an opener saying what a thing is not** (`r27`)
  A sentence opens with what a thing is.
  *Ask:* Does the opening clause say what the thing is before it says what it is not?
    - `It doesn't know what a PRD is. It knows entities, states, transitions, invariants.` → `It works from entities, states, transitions, and invariants, rather than from a document's genre.`
- **a judgment with no judge and no measure** (`r32`)
  Every judgment names its judge and its inputs.
  *Ask:* Who decides whether this is true, and by what measure?
    - `broken` → `name the judge and the measure`
- **a relational word leaving its slot empty** (`r33`)
  A relational word fills every slot it opens, right where the word stands.
  *Ask:* Relative to what, by what measure, or else what alternative?
    - `a few` → `state the exact quantity`
- **a pronoun with no antecedent in its own sentence** (`r39`)
  `it`, `this`, and `they` stand with an unambiguous antecedent in the same sentence. Where none stands, the noun is repeated.
  *Ask:* Can a reader say which thing this pronoun points at without looking back a sentence?
    - `It returns the places a stranger stops.` → `That session returns the places a stranger stops.`
- **an example restating a rule that was already clear** (`r41`)
  An example earns its place by resolving an ambiguity, and it uses realistic values. One worked case per rule is enough.
  *Ask:* Could a reader have read this rule two ways without this example? Does this example stand in prose, outside a rule entry in the rule home?
    - `Grep fallback: read for the four classes by hand - sentences past ~25 words, all-capital words used for emphasis, denial frames, and adjectives that grade a result's size.` → `Grep fallback: read for those four classes by hand. The last one shows up as big, huge, minor, or breakthrough.`
- **an abstraction standing where a concrete noun would do** (`r43`)
  The text prefers the concrete noun. A required abstraction is grounded with a two- or three-item example at its first use.
  *Ask:* Can the reader picture the thing this noun names?
    - `an entity` → `A screen, a panel, a saved file`
- **a paragraph carrying more than one point** (`r44`)
  One paragraph carries one point, stated in its first sentence, with the rest supporting it.
  *Ask:* Does a reader who reads only the first sentences of this section still follow it?
    - `one paragraph carrying the author's blindness, three example defects, and the loop's origin` → `the author's blindness in its own paragraph, the three defects as a list, and the origin in a paragraph after them`
- **a long flat run of peer items at one level** (`r45`)
  A document is a tree of grouped topics, and its levels nest without skipping. A long run of peer items is gathered under headed parents.
  *Ask:* Does this level hold a run of peer items with no grouping over them?
    - `a bullet running the rule, its script, and its grep fallback together in one paragraph` → `the rule as the bullet, with the script and the grep fallback nested under it`
- **a reply that buries its answer** (`r46`)
  A reply opens with the answer: the outcome, the decision, or the finding. The opening runs a few lines, and the reader may stop there. Reasoning, evidence, and options stand underneath.
  *Ask:* Can the reader stop after the opening block and still hold the answer?
    - `a report opening with the method it ran, and the finding in its last paragraph` → `the finding in the opening lines, and the method underneath it`
- **an offer to do work the writer could already derive** (`r48`)
  A derivable act is done and reported done. A backlog item is parked for the human only after a fresh test of whether the answer can be derived now.
  *Ask:* Does this sentence offer to do something the writer already has everything to do?
    - `just say the word` → `do the act and report it done`
- **a mistake expanded into a self-audit paragraph** (`r49`)
  A mistake is owned in one line and fixed.
  *Ask:* Does this passage explain the writer's own failure at more length than the fix takes?
    - `Direct answer: yes, I broke the method... (a paragraph auditing my own failure)` → `name the fix in one line, make it, and go on`
- **a working note handed to the reader unmarked, or a choice with no open answer** (`r50`)
  Dense working notes are marked so the reader can skip them, and they carry one idea per line. Every choice offered leaves room for a free-form answer.
  *Ask:* Can the reader tell at a glance which lines are notes, and can they answer outside the options given?
    - `a dense working note handed to the reader with no mark on it` → `the same note opening with a marker that says it is a working note, one idea per line`
- **a task subject written in machine words** (`r52`)
  The harness task panel on the human's screen speaks plain product words in the documents' language, understandable at a glance.
  *Ask:* Does a person glancing at this task subject know what is being done?
    - `run gen-language-consumers.py and splice AUDIT_SKILL_REL` → `print the writing rules into the audit skill`
- **human-facing prose drafted by a writer holding the project's own vocabulary** (`r53`)
  The first draft of prose a human will read is written by a fresh writer with no package rules loaded, working from a plain brief. The brief states the facts, names the intended reader, and lists the rules binding the surface. A person who has read the rulebook then reviews and revises that draft.
  *Ask:* Was this sentence first written by someone who had never read this project's skills, working from a brief?
    - `a paragraph drafted by the session that held the whole pack loaded` → `the paragraph drafted by a fresh writer from a plain brief, then revised by someone who has read the rules`
- **a changed section shipped before two clean cold readings** (`r54`)
  A changed section is read by fresh readers who carry no project context, until two consecutive reads return zero blocking findings. `skills/text-audit/SKILL.md` defines a blocking finding.
  *Ask:* Did a reader with no project context read this section and stop nowhere?
    - `a section shipped after one reading that returned five stops` → `the section read again after the repairs, and shipped once two readings in a row returned nothing that blocks`
- **one fact stated a second time in another place** (`r56`)
  One fact lives in one home. Every other place points at that home.
  *Ask:* Does another place in this project already state this fact?
    - `the writing rules written out a second time inside another skill` → `the rules in one file, and the second skill pointing at that file`
- **a phrase the human cut returning in a later draft** (`r57`)
  A phrasing the human cut in a review round stays out of every later draft of that artifact. An approved text takes exactly the correction the human named.
  *Ask:* Has the human already cut this wording from this artifact?
    - `«X — not Y» returning in a later draft, after the human cut it` → `the sentence saying what the thing is, in its own words`
- **a defect recorded as examples with no class behind them** (`r61`)
  When a text stops a reader, the writer names the class of mistake, defines it, and enters that class in the rule home. The examples under an entry are the recorded evidence that produced the class.
  *Ask:* Does the entry state what the mistake is, so a writer can find an instance nobody has met yet?
    - `a list of banned words: leg, goes red, station, door` → `the class - a coined word standing where a standard word exists - with those four as its recorded evidence`
- **a sentence open to two readings, or hiding its cause or what it leaves out** (`r62`)
  A reader reaches one interpretation of a sentence, sees what causes what, and can tell what the text leaves out.
  *Ask:* Can a reader read this sentence one way only, name what it makes happen, and say which alternatives it passed over?
    - `it hands the text to a fresh reader who has no knowledge of its history and marks every place a stranger stops` → `it hands the text to a fresh reader who knows nothing of its history, and that reader marks every place a stranger stops`
- **a thing named by its number, so the reader must leave the sentence to learn what it is** (`r63`)
  A sentence names a thing by what it is, and its number trails at the line's end.
  *Ask:* Does this sentence say what the thing is? Does it give only a number, a position, or a count the reader must go and resolve?
    - `Requirement 233 states the orchestration laws.` → `The requirement on how work is routed between tiers states the orchestration laws [INV-241].`
- **parallel items run together inside one sentence** (`r64`)
  Two or more parallel items become a bulleted or numbered list under a one-line lead, one item per line.
  *Ask:* Does this sentence run several items together where a list would put one on each line?
    - `The system shall refuse a branch behind main's tip, a lane with no open row, a host with no worktree line, and a lane past the cap.` → `The system shall refuse each of the four faults below. - a branch behind main's tip; - a lane with no open row; - a host with no worktree line; - a lane past the cap.`
- **a rare word standing where an everyday word says the same thing** (`r65`)
  A sentence takes the everyday word wherever an everyday word carries the meaning. A rare or bookish word stands only where no everyday word says the same thing. A term of the profession stays as it is, and the words around it come down.
  *Ask:* Would a professional reader whose first language is other than English reach for a dictionary on this word?
    - `a writer marinated in this project's own vocabulary` → `a writer who has already read this project's rules`
- **a document written in the register of the message that asked for it** (`r66`)
  The register of a request settles nothing about the register of the document. A person writes a request however is fastest for them. Every document is written to the rules of its surface, whatever the request looked like.
  *Ask:* Did this sentence take its tone from the message that asked for the work?
    - `ok so the gate basically checks the counts and yells when something is off` → `The gate measures every live document and refuses a push where a count stands above its record.`
- **a defined term standing in a file that is read apart from its definition** (`r67`)
  A term defined in one home stands in another file only where that file gives its reader a path to the definition. A file read on its own carries the terms it uses, or it names where each one is defined.
  *Ask:* Reading this file alone, could I reach the definition of this term?
    - `together with the settings ladder` → `together with the four scopes that settle a setting: the session's live word, the host profile, the personal profile, and the package default`
- **a placeholder word standing where the thing's own name fits** (`r68`)
  A sentence carries the name of the thing it is about. A pronoun or a general word stands only where the name would clutter the sentence. A status word stands only where the sentence has already stated the condition behind it.
  *Ask:* Does this word name the thing, or does the reader have to carry the name in from an earlier sentence?
    - `This keeps the leading context clear enough to hold the campaign.` → `The leading session then holds enough room to carry the campaign.`
- **a step naming a check, a file, or an act with no way to run it or find it** (`r69`)
  A step the reader has to carry out names the command that runs it, or the path that holds it. Where the text can name neither, it says so and names what the reader does instead.
  *Ask:* Could a reader carry out this step from the page alone, with nothing else on hand?
    - `the structure checks over requirement shape, the generated index, the matrix references, and the frozen baseline` → `each of the four checks on its own line, with the command that runs it`
- **a set claimed whole while the text carries members outside it, or leaves members out with no reason** (`r70`)
  A claim that a set is complete states what the set covers and what it leaves out. The list printed under such a claim carries every member the claim names.
  *Ask:* Does the text's own list agree with the claim made over it?
    - `These are every rule binding human-prose.` → `the rules binding human prose, with the printed count and the reason a code is missing`
- **a claim resting on ground the reader of the page cannot reach** (`r71`)
  A claim carries its ground on the page that makes it. A file named beside the claim holds the record, and the page still states what the reader needs.
  *Ask:* Can a reader holding this page alone see what this claim rests on?
    - `The loop came from the spec-format comprehension gate.` → `what that gate observed, stated on the page, with the file that records it named beside it`

<!-- /generated:human-prose-rules -->
