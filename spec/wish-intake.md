## Requirement 4: A wish is captured as a queue row that is never lost  [feature: F-wish]

**Context:** A wish is one request a person voices in plain words, of any size, at any moment. What a person says is read before anything acts on it, and that reading decides whether they asked for something at all (Requirement 313). A request they asked for becomes a row in the queue, the persistent ordered home of every wish, which lives in `PLAN.md`. The row holds the person's words, the wish's class, its status, and its acceptance criterion. A thought turned over, an idea named for later, and an observation are not wishes and open no row; an idea takes the idea shelf instead (Requirement 315).

**User Story:** As a person who asks for something in passing, I want the ask captured as a durable queue row, so that a request thrown mid-sentence is carried to an end while a passing thought is left where I put it.

### Acceptance Criteria

**Case: a wish becomes a row before the work starts**

1. *when* the first read finds that a person asked for something, the system *shall* record it as one row in the queue before it starts that work, holding the person's words, its size in the class column with the priority mark beside it, its status, and its acceptance criterion. [E-2, E-3, INV-316]
2. *when* a wish is recorded, the system *shall* keep its row existing even *if* the session ends immediately after, since the row is written before anything else proceeds. [E-3]
3. The system *shall* open no row for a question, a musing, an idea for later, or an observation. [INV-316]

**Case: a row is never deleted**

4. The system *shall* never delete a row, and *shall* close a row only with a named exit. [INV-1]
5. The system *shall* carry every wish to a recorded terminal state, so a request captured in passing is never dropped. [INV-1]

**Case: what holds the row's writing and its reading**

6. The system *shall* have the row written by the session that read the message, following the reading skill's own text, and *shall* claim no command that writes a row of its own accord when a person speaks. [INV-317]
7. The system *shall* have every reader of the queue read its rows through the one parser in `scripts/plan_checks.py`, so the list a session prints and the page a person opens hold the same rows. [E-3]
8. The system *shall* draw the queue as a page when somebody runs `bash scripts/render-board.sh`, and *shall* claim no redrawing of that page when a row's state changes. [E-3, INV-321]
9. The system *shall* let a row's mark be written by whoever edits the queue, and *shall* claim no check that reads a closing row's own acceptance before that mark changes. [INV-1, INV-321]

---
