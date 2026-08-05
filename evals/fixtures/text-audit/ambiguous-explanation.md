# Record retention

This is a preamble. Bracket codes like `INV-1` trail each criterion and point to the rule's home.

## Glossary

- **record** — one stored item the service keeps for a person.
- **archive** — the store the service moves a record into once it stops being read.

## Requirement 1: The service archives a record that has stopped being read

**Context:** The service keeps records for the people who store them. A record stops being read. The
service moves it into the archive. A person may hold a record out of the archive by marking it.

**User Story:** As a person storing records, I want an unread record archived, so that the store I
read every day stays small.

### Acceptance Criteria

**Case: the service archives a record**

1. *when* a record has gone unread for some time, the system *shall* move it into the archive. [INV-1]
2. *while* a person holds a record marked, the system *shall* keep it out of the archive for an appropriate stretch. [INV-2]
3. *if* an archive run is still going, *then* the system *shall* stop that run and start it again quickly. [INV-3]
