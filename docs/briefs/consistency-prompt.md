# Consistency prompt — check that several repaired documents agree

Hand this file to a fresh worker, word for word, with the paths below filled in.

## What the caller fills in

- Document paths: `<the documents to compare, one per line>`
- Report path: `<the file where the findings are written>`

## Your job

You read every document in the list and check that the documents agree with each other.

You repair nothing. You report what disagrees, and you name the place that reads as the home.

Separate workers repaired these documents, and each worker saw one document alone. A word one worker chose can collide with a word another worker chose.

## What you read

Read every document in the list, from its first line to its last.

Read `guardrails/language-rules.json` for the project's writing rules. Read the glossary at the top of `PRODUCT_SPEC.md` for the terms the project has already defined.

## The four agreements you check

1. One name per thing. A component, a script, a document, or a role carries one name across every document in the list.
2. One definition per term. A term defined in two documents carries the same definition in both places.
3. One shape per fact. A fact stated in two documents is written out once, and the second place points at the first.
4. One wording per rule. A rule stated in two documents carries the same trigger, the same obligation, and the same threshold in both.

## How to work

Walk the documents in the order given, and build four lists as you read:

- every named thing, with each name it appears under and each place it appears;
- every defined term, with each definition given for it and each place;
- every claim about the project, with each place that states the claim;
- every rule, with its trigger, its obligation, its threshold, and each place.

Then compare the entries inside each list. A subject appearing under two names, two definitions, two shapes, or two obligations is a finding.

Check these three places, where a disagreement is easy to miss:

- a heading in one document that names the same subject as a differently worded heading in another;
- a number, a threshold, or a count restated in a second document;
- a path, a command, or a script name written two ways.

## What each finding carries

Write one numbered entry per finding, carrying six parts:

1. the subject: the thing, the term, the fact, or the rule;
2. which of the four agreements the finding breaks;
3. every place the subject appears: the file path, the heading, and the quoted sentence;
4. the disagreement, stated in one sentence;
5. the place that reads as the home, with the reason that place reads as the home;
6. blocking or non-blocking.

Blocking means a reader who acts on one document contradicts another document.

Non-blocking means both readings lead a reader to the same act.

Recommend one home for each finding, and change no document.

## Where the report goes

Write the findings to the report path named at the top of this prompt, in this shape:

- a first line naming every document compared and the date;
- one line carrying the count of findings, split across the four agreements;
- the numbered entries, grouped under a heading per agreement;
- a heading naming the agreements that turned up nothing;
- a closing line listing the numbers of the blocking entries.

Say so in one line when the documents agreed everywhere.
