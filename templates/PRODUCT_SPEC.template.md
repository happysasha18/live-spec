# [Project name] — Product Spec (v0.1, [date])

This document is the living statement of what [project name] is right now. The body is a flat list of requirements, each stating one rule of the product. A requirement carries a Context block, a one-sentence User Story, and acceptance criteria grouped into named cases. A requirement whose heading carries a `[feature: F-...]` tag is a person-facing scenario, telling what a person does and what the person sees. Edit history lives in `JOURNAL.md`; this spec states what is true today.

[One paragraph in plain words: what the product does for the person who uses it, and why it exists.]

Bracket codes like `[E-1]` and `[INV-1]` trail a criterion and point to the rule's home in this spec. A reader can ignore them, and a maintainer follows them. The letter before the number names the kind:

- `E-` — an entity, a numbered part of the product;
- `INV-` — an invariant, a numbered rule that always holds;
- `T-` — a transition, a numbered change of state;
- `ACT-` — an actor, one side that owns a call;
- `C-` — a composition-axis rule;
- `D-` — a recorded decision;
- `S-` — a header rule;
- `B-` — a founding answer;
- `F-` — a feature, tagged on a requirement heading as `[feature: F-...]`.

A range such as `[T-1..T-3]` cites its whole run of codes. A `[target]` marker on a line of its own marks a part that is promised and still unbuilt. A `[default]` marker names a value the agent picked that the person may retune. A `[GAP: ...]` line under a criterion records a place where the source leaves the judge, the measure, or the scope unstated.

The keywords *when*, *while*, *if*, *then*, *where*, and *shall* are set in lowercase italics. They carry their standard requirements meaning. *shall* states a duty. *when* and *while* open a situation. *if* and *then* open a condition and its result. *where* scopes a duty to the setting it holds in.

**Founding answers (B-2).** personal-vs-reusable: [personal, or reusable] — asked of the person at founding, or read from their profile. [One line for each further founding answer that shapes this product.]

The glossary below defines every domain noun the requirements use, each term once and under one name.

## Glossary

- **[the product's central noun]** — [one sentence saying what it is].
- **[the second noun the criteria use]** — [one sentence saying what it is].
- **[the third noun the criteria use]** — [one sentence saying what it is].

## Requirement 1: The spec keeps what is built apart from what is planned

**Context:** The spec states what is built and working today apart from what is only planned. A planned part carries the target marker on a line of its own. A reader who meets an unmarked part reads it as working today.

**User Story:** As a reader, I want every planned part marked, so that I never read a promise as a working part.

### Acceptance Criteria

**Case: built and planned are marked apart**

1. The spec *shall* state what is built and working today apart from what is only planned. [S-0]
2. The system *shall* carry the target marker on a line of its own, and *shall* keep it off the prose around it. [S-0]

**Case: a marked part names the work that builds it**

3. The system *shall* tie each target marker to the open queue row that builds it. [S-0]
4. The system *shall* red the suite *if* that row lands with the marker still standing. [S-0]

## Requirement 2: [The ordinary path, named by what the person does]  [feature: F-1]

**Context:** [When this situation arises.] [Who takes part in it.] [What the person sees before acting.]

**User Story:** As [the person in a named position], I want [the one thing they want], so that [the one benefit that follows].

### Acceptance Criteria

**Case: [the ordinary path, named by its situation]**

1. *when* [the person acts], the system *shall* [the response the person sees]. [E-1]
2. *while* [the situation holds], the system *shall* [the duty that holds throughout it]. [INV-1]

**Case: [the state change, named by what moves]**

3. *when* [the trigger occurs], the system *shall* move [the thing] from [one state] to [the next state]. [T-1]
4. The system *shall* give [the thing] a named way out of [that state]. [T-1]

## Requirement 3: [The edge path, named by what goes wrong]

**Context:** [Which failure or interruption this covers.] [How the person meets it.] [What the product still owes them.]

**User Story:** As [the person in a named position], I want [what the product still does], so that [the loss I am spared].

### Acceptance Criteria

**Case: [the failure, named by its trigger]**

1. *if* [the failure happens], *then* the system *shall* [what the person sees]. [T-2]
2. The system *shall* hold [the guarantee that survives the failure]. [INV-2]

**Case: the ordinary path resumes**

3. *when* [the failure clears], the system *shall* return the person to [the ordinary path]. [T-2]

## Requirement 4: The person and the system each own their own calls

**Context:** Some calls belong to the person and some to the system. The person owns taste, the thresholds only they can pick, and any act that cannot be undone. The system owns the work it can carry on its own evidence.

**User Story:** As the person served, I want each call owned by a named side, so that I am asked only for mine.

### Acceptance Criteria

**Case: the person's own calls**

1. The person *shall* own taste, [the thresholds only they can pick], and every act that cannot be undone. [ACT-1]

**Case: the system's own calls**

2. The system *shall* own [the work it can carry on its own evidence]. [ACT-2]
3. The system *shall* bring the person in *where* an answer needs a fact no document holds. [ACT-2]

## Requirement 5: [The stateful surface] behaves the same along every axis

**Context:** [The stateful surface] holds state a person can see and act on. Its behaviour can vary along several axes at once, and a bug hides where two of them meet. The floor axes below hold for every stateful surface this product ships.

**User Story:** As a person acting on [the stateful surface], I want one behaviour along every axis, so that a reopen keeps my work.

### Acceptance Criteria

**Case: the floor axes**

1. The system *shall* review [the stateful surface] against each floor axis below. [C-1]
   - each view the surface appears in;
   - each mode it can stand in;
   - each viewport size it is used at;
   - a close followed by a reopen.
2. The system *shall* state, per axis value, whether [the stateful surface] holds its state, clears it, or hands it on. [C-1]

**Case: the pick that stands while a question is open**

3. The system *shall* [the pick that stands while the open question waits], and the person *shall* stay free to overturn it. [D-1]

## Reference

The code-to-location table below is generated output, built from the body criteria by `scripts/build-index.py`; no one edits it by hand. Feature codes (`F-...`) live on their requirement headings and carry no table row.

| Code | Location |
|---|---|
| ACT-1 | R4.1 |
| ACT-2 | R4.2, R4.3 |
| C-1 | R5.1, R5.2 |
| D-1 | R5.3 |
| E-1 | R2.1 |
| INV-1 | R2.2 |
| INV-2 | R3.2 |
| S-0 | R1.1, R1.2, R1.3, R1.4 |
| T-1 | R2.3, R2.4 |
| T-2 | R3.1, R3.3 |
