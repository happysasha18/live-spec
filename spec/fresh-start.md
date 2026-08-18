## Requirement 169: Bootstrapping a fresh host  [feature: F-bootstrap]

**Context:** A fresh host starts from the templates the pack ships. The system copies the document set and the suite scaffold, then the first request enters the queue and runs through the ordinary pipeline. The scaffold's green is the starting floor the first delivery builds on.

**User Story:** As a person starting a fresh host, I want the templates and a runnable scaffold in place, so that the first request runs through the ordinary pipeline against a known starting floor. [B-1]

### Acceptance Criteria

**Case: the templates land**

1. *when* the version-control gate has closed, the system *shall* copy the document templates — spec, architecture, test matrix, roadmap, journal, and the resume file — and copy the suite scaffold (`test_scaffold.py`) into `tests/`. [B-1]
2. *when* the templates are in place, the system *shall* offer hooks in plain words, and *shall* impose none. [E-6]
3. *when* the templates are in place, the system *shall* let the first request enter the queue and run from intake through the ordinary pipeline. [B-1]

**Case: the scaffold defines the first green**

4. The scaffold suite *shall* judge the first delivery green by what the shipped scaffold runs. [B-1, INV-274]
   - the six documents stand, and none is an empty shell;
   - the spec's opening carries a version and a date;
   - the matrix carries its generated reference and its coverage teaching;
   - the queue is a table;
   - the resume file holds at most one live-state block.
5. *when* a header holds a leftover template placeholder, the scaffold suite *shall* count that header as red. [B-1]
6. The scaffold green *shall* stand as the starting floor; the first delivery *shall* ship its own first real test beside the scaffold. [B-1]
   [GAP: the spec does not state what content a live-state block must carry for the scaffold suite to count it present.]

**Case: a second founding is safe**

7. *when* a founding runs on a tree a prior founding began, the system *shall* read each phase's precondition from the tree. [INV-89, B-1]
   - a destination that already stands is reported to the person as done, and skipped.
8. The system *shall* overwrite no file it did not create in the running founding. [INV-7, B-1]
   - a destination standing with its template placeholders intact is named to the person, and replaced only where the person says so.

**Case: the host profile carries the host's own lines**

9. *when* a founding writes `.live-spec/profile.md`, the system *shall* write one line for every question in the founding-question set whose key names no path. [B-3, INV-227]
   - the economy rung and the answered set's version stand beside those lines.
10. The system *shall* write no setting about the person into the host profile, and *shall* use no personal-profile template as that file's source. [E-13, B-3]

**Case: the surface registry takes the config's name**

11. *when* a founding creates the surface registry, the system *shall* create it after `guardrails.config.json` exists, and *shall* take its filename from that config's registry path. [INV-97, E-10]

---

