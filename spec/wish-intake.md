## Requirement 4: A wish is captured as a queue row that is never lost  [feature: F-wish]

**Context:** A wish is one request a person voices in plain words, of any size, at any moment. The moment a person voices one it becomes a row in the queue (ROADMAP.md), the persistent ordered home of every wish. The row holds the person's words, the wish's class, its status, and its acceptance criterion.

**User Story:** As a person who voices a request in passing, I want it captured as a durable queue row the instant I speak it, so that a thought thrown mid-sentence is never lost between intake and its resolution.

### Acceptance Criteria

**Case: a wish becomes a row at once**

1. *when* a person voices a wish, the system *shall* record it as one row in the queue that same moment, holding the person's words, its size in the class column with the priority mark beside it, its status, and its acceptance criterion. [E-2, E-3]
2. *when* a wish is recorded, the system *shall* keep its row existing even *if* the session ends immediately after, since the row is written before anything else proceeds. [E-3]

**Case: a row is never deleted**

3. The system *shall* never delete a row, and *shall* close a row only with a named exit. [INV-1]
4. The system *shall* carry every wish to a recorded terminal state, so a request captured in passing is never dropped. [INV-1]

---

