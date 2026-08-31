## Requirement 313: What a person just said is read before anything acts on it  [feature: F-first-read]

**Context:** A person writes a sentence. Before anything is answered, built or changed, the system works out what the person just did. Seven readings are open to it: a question or a thought turned over, an idea named for later, an observation, a decision that settles an open choice, a correction to work already running, an instruction to do something, and a halt. That reading is the door, and work starts only behind a reading that asked for work. What makes the reading happen today is the text of the pack's reading skill, which a session loads and follows; the pack ships no command that puts a message through it, and none that reports a session which skipped it.

**User Story:** As a person who talks to the system in ordinary sentences, I want it to work out what I just did before it acts, so that a question comes back answered and a thought said in passing never turns into work I did not ask for.

### Acceptance Criteria

**Case: the message is read as one of seven acts**

1. *when* a person sends a message, the system *shall* read it as one or more of the seven acts before it answers, opens a document, or changes a file. [E-36]
   - the seven acts are a question or musing, an idea for later, an observation, a decision, a correction, an instruction, and a halt;
   - a message carrying several acts is read as each of them, and one act never absorbs another.
2. The system *shall* read the act from what the person meant in the exchange it stands in, and *shall* read no act from the wording alone. [E-36]
3. *if* the message leaves its act unreadable, *then* the system *shall* ask the person which it is and *shall* start no work *while* that question stands. [E-36, INV-4]

**Case: work starts only behind an act that asked for it**

4. The system *shall* start work only on an instruction, on a correction to work already running, or on a decision that changes such work. [INV-316]
5. *when* the act is a question, a musing, an idea, or an observation, the system *shall* answer it and *shall* open no task, no document, and no branch for it. [INV-316]
6. *when* the system has read the act, the system *shall* say back in one line what it took the message to be, in the person's own words. [INV-316, INV-28]

**Case: what holds the first read**

7. The system *shall* hold the first read as the reading skill's own text, which a session reads and follows, and *shall* claim no command, gate, or hook that puts a message through it. [INV-317]
8. The system *shall* judge the reading against recorded runs of it, one run to a written scenario, and *shall* read a run recorded against an earlier version of the skill as saying nothing about the skill as it stands. [INV-317]

---

## Requirement 314: Accepted work carries a decision sheet a later session picks up

**Context:** Once a message has been read as work, the system writes down what it understood before it calls anyone in. That writing is the decision sheet: the goal in the person's own words, the state the work leaves behind it, what is already known, what has to be found out, what cannot be undone, which working skills are needed, what shows the goal was reached, and which documents change. The sheet lives inside the work's own checkpoint file, so a session starting fresh reads the sheet and the conversation behind it can be gone. One piece of work keeps one checkpoint for its whole life.

No state a plan row records says that one piece of work waits on another, so nothing orders on such a wait and nothing claims to.

**User Story:** As a person whose work outlives the conversation that started it, I want what was understood written where the next session reads it, so that taking the work up again costs me no retelling.

### Acceptance Criteria

**Case: the sheet is written before the first working skill is called**

1. *when* work is accepted, the system *shall* write the decision sheet before it calls any working skill. [INV-318]
   - the sheet holds the goal in the person's words, the outcome observable afterwards, the dimensions the work touches with a reason for each, what is known, what has to be found out, what cannot be undone, the working skills needed, the evidence that shows the goal was reached, which piece runs next where other accepted work stands open, and the documents whose sentences change.
2. The system *shall* write the sheet into the work's own checkpoint file and *shall* keep no second copy of it. [INV-318, INV-4]
3. *while* one piece of work runs, the system *shall* keep it on the one checkpoint it opened and *shall* open no second checkpoint for it. [INV-318]

**Case: the checkpoint refuses a sheet that is not there**

4. *when* a checkpoint names the first read as its owner, the checkpoint command *shall* refuse to create that checkpoint without a decision sheet in it, and *shall* report an existing one unfit while it holds none. [INV-318]
5. *when* the work closes, the system *shall* close its checkpoint in the same step, and the checkpoint command *shall* refuse a close *while* the file still names work in progress. [INV-318]

**Case: which accepted work runs next**

6. *when* several pieces of accepted work stand open at once, the system *shall* name which one runs next, read by `scripts/state-probe.sh` from the states the plan records rather than composed from memory. [INV-319]
7. The system *shall* order the open work by the states the plan records — what needs the person's eyes, what is in hand, what is blocked, what is queued, and what stands critical inside each — and *shall* claim no ordering read from anywhere else. [INV-319]

---

## Requirement 315: An idea named in passing is kept in the person's own words
   [target]

**Context:** In the middle of a conversation about something else, a person names a possibility they are not asking for now. The reading calls that an idea, and an idea earns a home of its own and no task: it is kept in the person's own wording, with no identifier, no priority, and no estimate, and one line comes back saying it was kept. Days later the person asks what they proposed and the wording comes back as they said it. The home this requirement names stands nowhere in the tree: no file holds it, no command writes to it, and no test reads it, so an idea said aloud lives as long as the conversation and no longer.

**User Story:** As a person who thinks aloud while working on something else, I want a passing idea kept in my own words, so that I find it again days later without its having become work.

### Acceptance Criteria

**Case: an idea is kept, and never started**

1. *when* the act is an idea for later, the system *shall* keep the person's own wording on the idea shelf and *shall* say in one line that it was kept. [E-37]
2. The system *shall* give a kept idea no identifier, no priority, and no estimate, and *shall* never start work on it. [E-37]
3. *when* the person later asks what they proposed, the system *shall* give back the kept wording as it was said. [INV-320]

**Case: the shelf and the work are one fork**

4. *when* one message both names an idea and asks for work, the system *shall* take the work and shelve the idea as two separate outcomes. [E-37, INV-316]
5. The system *shall* never place one item on the shelf and into the work at once. [E-37, INV-320]

---
