## Requirement 313: What a person just said is read before anything acts on it  [feature: F-first-read]

**Context:** A person writes a sentence. Before anything is answered, built or changed, the system works out what the person just did. Seven readings are open to it: a question or a thought turned over, an idea named for later, an observation, a decision that settles an open choice, a correction to work already running, an instruction to do something, and a halt. That reading is the door, and work starts only behind a reading that asked for work. The Director owns this reading and stops at a route contract; a separate accepted-work pipeline owns admission and execution. What makes the reading happen today is the text of the pack's reading skill, which a session loads and follows; the pack ships no command that puts a message through it, and none that reports a session which skipped it.

**User Story:** As a person who talks to the system in ordinary sentences, I want it to work out what I just did before it acts, so that a question comes back answered and a thought said in passing never turns into work I did not ask for.

### Acceptance Criteria

**Case: the message is read as one of seven acts**

1. *when* a person sends a message, the system *shall* read it as one or more of the seven acts before it answers, opens a document, or changes a file. [E-36]
   - the seven acts are a question or musing, an idea for later, an observation, a decision, a correction, an instruction, and a halt;
   - a message carrying several acts is read as each of them, and one act never absorbs another.
2. The system *shall* read the act from what the person meant in the exchange it stands in, and *shall* read no act from the wording alone. [E-36]
3. *if* the message leaves its act unreadable, *then* the system *shall* ask the person which it is and *shall* start no work *while* that question stands. [E-36, INV-4]

**Case: work starts only behind an act that asked for it**

4. The system *shall* route work only behind an instruction, a correction to work already running, a decision that changes such work, or an observation that carries a promised behaviour's repair beyond doubt. [INV-316]
5. *when* the act is a question, a musing, an idea, or an observation with no such repair, the system *shall* answer it and *shall* open no task, no document, and no branch for it. [INV-316]
6. *when* the system has read the act, the system *shall* say back in one line what it took the message to be, in the person's own words. [INV-316, INV-28]

**Case: the first reader stops at a route**

6a. The Director *shall* return the acts, whether the turn proposes new work or changes existing work, the count of new pieces, the touched dimensions, the possible specialists and the source, and *shall* stop without writing the plan, creating a checkpoint, running a specialist, verifying or closing work. [INV-316, INV-318]
6b. The system *shall* load the accepted-work pipeline only for a route that proposes new work or changes existing work, and *shall* leave it unloaded for a question, musing or conversation. [INV-316]

**Case: what holds the first read**

7. The system *shall* hold the first read as the reading skill's own text, which a session reads and follows, and *shall* claim no command, gate, or hook that puts a message through it. [INV-317]
8. The system *shall* judge the reading against recorded runs of it, one run to a written scenario, and *shall* read a run recorded against an earlier version of the skill as saying nothing about the skill as it stands. [INV-317]

---

## Requirement 314: The accepted-work pipeline carries a decision sheet a later session picks up

**Context:** Once Director has returned a work route, the accepted-work pipeline writes down what was understood before it calls anyone in. That writing is the decision sheet: the source, the goal in the person's own words, the state the work leaves behind it, its definition of done, the dimensions the work touches, what is already known, what has to be found out, what cannot be undone, which working skills are needed, what shows the goal was reached, which piece runs next where other accepted work stands open, and which documents change. The sheet lives inside the work's own checkpoint file, so a session starting fresh reads the sheet and the conversation behind it can be gone. One piece of work keeps one checkpoint for its whole life.

No state a plan row records says that one piece of work waits on another, so nothing orders on such a wait and nothing claims to.

**User Story:** As a person whose work outlives the conversation that started it, I want what was understood written where the next session reads it, so that taking the work up again costs me no retelling.

### Acceptance Criteria

**Case: the sheet is written before the first working skill is called**

1. *when* Director routes work, the accepted-work pipeline *shall* write the decision sheet before it calls any working skill. [INV-318]
   - the sheet holds the source, the goal in the person's words, the outcome observable afterwards, the definition of done, the dimensions the work touches with a reason for each, what is known, what has to be found out, what cannot be undone, the working skills needed, the evidence that shows the goal was reached, which piece runs next where other accepted work stands open, and the documents whose sentences change.
   - new work reaches the board only after `scripts/task-admission.py` confirms a person's source or a reproduced outside defect, an observable outcome, a definition of done, an independent verification, its project and scope, and no existing task; a review opinion cannot mint work. [INV-318, INV-316]
2. The system *shall* write the sheet into the work's own checkpoint file and *shall* keep no second copy of it. [INV-318, INV-4]
3. *while* one piece of work runs, the system *shall* keep it on the one checkpoint it opened and *shall* open no second checkpoint for it. [INV-318]

**Case: the checkpoint refuses a sheet that is not there**

4. *when* a checkpoint names the accepted-work pipeline as its owner, the checkpoint command *shall* refuse to create that checkpoint without a decision sheet in it, and *shall* report an existing one unfit while it holds none. Legacy Director-owned checkpoints keep the same validation while they remain. [INV-318]
5. *when* the work closes, the system *shall* close its checkpoint in the same step, and the checkpoint command *shall* refuse a close *while* the file still names work in progress. [INV-318]

**Case: which accepted work runs next**

The printed account of open work reads at a glance: a row whose own name comes first, in one column, then its state, then what the row gives the person. A row that was closed and stopped passing its check stands among the live work under its own state. The leading figure is the work still open.

6. *when* several pieces of accepted work stand open at once, the system *shall* name which one runs next, read by `scripts/state-probe.sh` from the states the plan records rather than composed from memory. [INV-319]
7. The system *shall* order the open work by the states the plan records — what needs the person's eyes, what is in hand, what is reopened, what is blocked, what is queued, and what stands critical inside each — and *shall* claim no ordering read from anywhere else. [INV-319]
8. The system *shall* lead the printed account of open work with a count of the rows not done, and *shall* carry no count of finished work in that account. A running total of finished rows only grows, and it answers nothing without a window over which to read it. [INV-319]
   - the count of rows not done covers every row the plan holds that is not done, a row the person postponed and a row folded into another among them. Those two drop out of the ranking above, which decides what runs next; they stay in this count, which answers how much work is left. [INV-319]
9. The system *shall* print each shown row's own id before its state mark and its title, padded to the width of the longest id `PLAN.md` declares, so the state marks form one readable column down the printed list. [INV-319]
10. The system *shall* give a row closed since the last push its own line in that account, under the done state, and *shall* drop the line once the push lands — so what was just finished reads in the same words as the work still open, and leaves on its own. [INV-319]

**Case: what holds one piece of work to one checkpoint**

11. The system *shall* hold the one-checkpoint rule above as the accepted-work pipeline's own text, which a session reads and follows, and *shall* claim no check that counts a piece of work's checkpoints or refuses a second one. [INV-318, INV-317]
12. The checkpoint command *shall* carry the mechanical half of that rule. Its update operation edits the sections of a checkpoint already on disk, in place, leaving every section it was not asked to change as it found it, so a correction to work already running lands on that work's own file. Its create operation writes a blank template over whatever its path already holds, so a second create against one piece of work overwrites that work's own record. [INV-318]

---
