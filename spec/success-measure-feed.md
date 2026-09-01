## Requirement 318: A host's status view reads a fetched success-measure feed

**Context:** A feature's success measure (Requirement 76) stays a written promise a person checks by
eye until its reading machinery ships. The human-triggered half of that promise already ships: a
person's own reaction lands as field evidence in the feedback ledger, citing the feature's scenario
(Requirement 154, clause 4). This requirement gives the automatic half its shape — a small file any
host's own fetch tooling writes, called the success-measure feed, and one checker the pack ships that
reads a feed and reds when the fetch never ran or came back empty. Writing the fetch tooling itself
against a host's own analytics account, and wiring a host's own status view to print the feed's
numbers beside its tasks, are each host's own job, the pack-to-host split Requirement 267's own pole
question already draws: the feed's shape is one body every host can run identically against, so it
centralizes here; the fetch tooling reads a host's own account and its own data, so each host owns
the instance that fills it.

**User Story:** As a person who wants a shipped feature's live numbers printed beside its tasks
without going to look, I want the pack to state one feed shape any host's fetch tooling writes and
one checker that reds when the fetch is skipped or empty, so that a host's own status view has one
fixed contract to wire against.

### Acceptance Criteria

**Case: the feed's shape**

1. The system *shall* define the success-measure feed as one JSON file a host's own fetch tooling writes, carrying a generation timestamp, the fetch's own source named in plain words, and a list of one or more named metrics, each metric carrying a label, a value, and a unit. [INV-324]
2. *when* a two-variant experiment is running, the system *shall* let the feed carry it as one named experiment block holding exactly two variants, each variant its own label and its own non-empty metrics list. [INV-324]
3. The system *shall* have `scripts/check-success-measure-feed.py` be the one reader of the feed's shape, run by any host that wants a feed checked before its status view prints it. [INV-324]

**Case: the checker reds on a skipped or empty fetch**

4. *when* the feed's file is absent, the system *shall* red and name the fetch as skipped. [INV-324, INV-21]
5. *when* the feed's metrics list is missing or empty, the system *shall* red and name the fetch as having returned nothing. [INV-324, INV-21]
6. *when* the feed's generation timestamp is older than the staleness bound the caller states, the system *shall* red and name the feed stale. [INV-324]
7. *when* an experiment block carries other than exactly two variants, or a variant with an empty metrics list, the system *shall* red and name the malformed block. [INV-324]
8. The system *shall* pass a feed carrying a valid generation timestamp within its staleness bound, one or more metrics, and, where present, a two-variant experiment whose every variant is non-empty. [INV-324]

**Case: what stays each host's own job**

9. The system *shall* leave writing the fetch tooling that produces a feed from a real source — a host's own analytics account, a host's own traffic log — to each host, the host pole Requirement 267 draws for host-specific data. [INV-324, INV-163]
10. The system *shall* leave a host's own status view printing a checked feed's numbers beside its tasks unasked to each host. [INV-324]

---
