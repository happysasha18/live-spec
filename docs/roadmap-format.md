# The roadmap format — definition

This page defines the format a project's plan/queue is written in — the shape `templates/PLAN.template.md` hands a newly founded project. The queue is a member of the same format family as the spec, and this page states only what is particular to it. The shared family laws live once in `docs/spec-format.md`, and this page inherits them by reference rather than restating them.

## What the queue inherits from the family

The queue is written in the requirements genre `docs/spec-format.md` defines, and every law that page states holds here unchanged:

- the closed-vocabulary glossary, so every domain noun the queue uses carries one glossary entry under one name;
- the keyword form, so the keywords *when*, *while*, *if*, *then*, and *shall* are set in lowercase italics;
- the no-capitals rule, so no word stands in all capitals outside a code anchor;
- the trailing code anchor, so a code points to its home at the line's end and a reader may ignore it;
- the no-history law, so the record of finished work — its dates, its delivery reports, the reasons behind past choices — lives in the archive and the journal, and the body states only the live queue;
- the generated-section gating, so a section a script builds is output only and a gate reds a hand edit of it (to red is to fail the suite), where the queue carries such a section;
- the comprehension gate, so a changed section clears the mechanical lints and then a panel of cold readers, passing only after two consecutive reads return zero blocking findings.

A reader who needs any of these consults `docs/spec-format.md`. The rest of this page adds the parts the queue carries that the spec does not.

## What the queue is

The queue is the live record of what is asked of the product and where each ask stands. A wish is a request for a change the product does not yet carry, and a wish lands when the delivery that completes it ships. Intake is continuous, a wish entering the moment it is spoken; execution runs at most the lane cap of independent landings at once — three by default, so up to three rows may read *in-work* — and a landing finishes before a colliding next starts; two landings collide when they rewrite one clause or one behaviour's rule. The spec keeps sole authority over what is true of the product, and the queue holds the asks. Its reading job: a stranger reads the body and knows the live work state on the first pass.

## Document structure

A queue document opens with a short preamble, the same shape the family gives it: what the document covers, what the bracket codes are, and how the keywords read. The body follows — one table, its header `| # | Wish (plain words) | Class | Status | Decision / acceptance |`, one row per live wish, the rows standing in ascending id order with a new wish appending at the tail. A rotated-manifest block sits above the body, one line per monthly archive file naming the rows moved and the file that received them; the rotation script maintains it and a gate cross-checks it against the archive.

## The live-body law

The body holds live rows only. When a wish lands, its row moves to the dated archive under `docs/queue-archive/` in the same commit that lands it, carried verbatim with its delivery report, and the rotated-manifest block records the move. A row whose wish ends without landing — declined or superseded — moves the same way in the commit that closes it, and a row that exists to settle a question exits as decided. Those four words are the whole terminal vocabulary, and this sentence is their one home: a row's status carries one of them the moment it reaches an archive, so a row still open there is caught by name (the rotation gate reads this list). An archive file gathers one calendar month's moved rows and is named by year and month, so the manifest grows one line per archive file rather than one line per landing. The word *landed* therefore names a transition a row makes, and a body row never carries it as a status. The archive keeps every moved row, grepable by number, under the project's nothing-lost rule, so the history of the work stands in the archive and the journal.

This is how the family's no-history law reaches a queue document: the body stays the live queue, and the record of finished work moves out to the archive. A row with an open leg — a leg is one separable part of the wish's delivery — keeps its landed legs' record in its own cells until the row closes whole; the archive receives the whole story at the terminal exit. The conversion normalized the row form and the status vocabulary; wish and acceptance prose kept its pre-conversion words verbatim, capitals included, and lowers as rows are edited in the normal course. The queue's no-history net is therefore the live-body law and the doc-rotation gate; the family's no-history gate does not scan the queue, since a live row carries its status date and its provenance date by design. The status cell is the sole authority on a row's current state; narration a live row carried before the format conversion is kept verbatim in the archive's status-notes file. Archive files made before this format kept their day-named form, and they stand as legal legacy archives.

## The status vocabulary

The status vocabulary is closed — five words, each set in lowercase italics and each carrying a date:

- *queued* — the wish is accepted and waiting its turn. Its task statement has not passed validation yet.
- *ready* — the wish's task statement has passed validation and its wording is frozen, so the row may be taken up as it stands. The row keeps this status until a session claims it, when it reads *in-work*.
- *in-work* — the wish is claimed by a session. A landing that leaves any leg open keeps its row live with the open leg named, since a row closes only whole; the row reads *in-work* while a session still drives the open leg, and *deferred* on a named trigger when that leg waits on an outside event. A stale claim is re-read at queue-take — the moment a session takes its next wish from the queue: an *in-work* row with no commit citing it for seven days joins the staleness review list for the human's word. The mechanical sweep behind that list has not been built yet; until it lands, the taking session runs the re-read itself.
- *deferred* — the wish is parked on a named revisit trigger, the trigger written in the status cell and re-read at queue-take and at the next milestone review — the whole-project re-check the pack runs at each version milestone.
- *far* — the wish is parked with no near trigger, re-read at the milestone reviews.

Anything else a row needs to say about its state lives in the wish cell or the acceptance cell.

## The class vocabulary

The class vocabulary is closed and held by a lint, one vocabulary shared with the spec. The class cell carries exactly one of four words: *bug* — something shipped is wrong, and it cuts the queue ahead of any size — or one of the three sizes *small*, *surface*, and *large*, whose meanings live in the spec glossary's size entry.

## The queue row

One queue row is one live wish, exactly five cells, matching the header: the id, the wish, the class, the status, and the acceptance.

The wish cell carries the ask in plain words, its provenance, and the intake notes. The provenance is whose word asked for the wish and the date — a queue's load-bearing fact, carried on the row because an unfinished ask's origin governs how it is handled. The intake notes are the wish's door (feature · bug · refactor · docs-only · skip), its kind (product · infra · skill · prose), its footprint, its placement on the architecture map, and an entry condition where one was declared. A priority mark rides the intake notes when the wish's priority is other than normal — a critical bug lands before everything, and a quick win may bubble up between landings with the jump named in its row.

The acceptance cell carries the Done-when criteria and the non-goals, with code anchors trailing at the line ends.

The spec's Context blocks and User Stories stand down from the row the way the matrix's rows stand them down: the spec owns them, and the row points at the spec by anchor rather than restating them.

## The row lint

Every body row clears a row lint that runs in the suite. The lint reds a row that does not carry exactly five cells, a row whose status is outside the closed set or missing its date, a row whose class is outside the closed set, a *deferred* row that names no trigger, and a body whose row ids do not ascend. Its home is the suite's traceability tests, extended rather than duplicated, the way the matrix's row lint is homed, so no new standalone script is built. It states its reach on the green line — how many body rows it read — the reach every gate in this family states.

## The conversion delivery

One delivery converts the whole roadmap to this format, and everything that reads the old shape moves in that same delivery:

- **Landed rows move to a dated archive file verbatim**, the biggest named delta: the body shrinks to its live rows, each moved row carrying its delivery report unchanged, and the rotated-manifest and the archive together preserve every row.
- **The statuses lowercase and lose their decoration** as a declared delta, each free-form status becoming one of the four closed words with its date.
- **The sixth drift cell is removed** as a declared delta: the newest rows drifted into a sixth cell holding a bare dash, and the conversion returns every row to the five the header declares.
- **The two class values outside the vocabulary move** as declared deltas: a class reading *big* reads *large*, and the one row carrying *far* in its class cell moves that word to its status cell, the moved *far* displacing the free-form status that stood there (row 411 resolves to *far 2026-07-17*).
- **The rotation machinery learns the monthly append** as a named delta: the archive file is named by year and month (`rotated-ROADMAP-YYYY-MM.md`), and `guardrails/check-doc-rotation.py` reads one manifest line whose row-set grows across commits. That delivery taught the same append to the rotation tool `scripts/rotate-doc.py`, which has since retired to `attic/rotate-doc.py` along with the live document it read; a row moves by hand now, and the gate is what proves the move lost nothing. The one-time converter and its content-preservation proof lived under `prototype/2026-07-23-roadmap-format/`, the matrix conversion's own precedent, deleted whole in the 26.08 approved prototype cleanup (`61a77841`) once its reading was over.
- **Every parsing consumer is repointed** in the same delivery. `guardrails/check-doc-rotation.py` keeps cross-checking the rotated-manifest against the archive, continuing to prove nothing was lost as rows move. `guardrails/check-landing-next-steps.py` re-keys from "a Status cell flipped to landed" to "a body row moved to the archive whose archived status reads *landed*" — the gate reads the moved row's status from the archive side of the diff, a row moving out as *declined* or *superseded* owing no refresh — and it still reds a landing commit that leaves `NEXT_STEPS.md` untouched. `tests/test_delegation_line.py` reads landed rows and their delivery reports from the archive, its non-empty-input guard counting archive rows scanned. The in-work lane-cap check in the traceability suite reads the status through the new lowercase-italic form. `guardrails/crosscut_counter.py` keeps grepping the cells for `footprint: cross-cutting`, reading the footprint from the wish cell's intake notes.

## The comprehension gate

A changed queue section clears the comprehension gate the family defines, stated once in `docs/spec-format.md`: the mechanical lints first, then a panel of cold readers, passing only after two consecutive reads return zero blocking findings. The queue adds the row lint above to that first layer, running beside the family's vocabulary, one-name, weak-word, and style lints. The conversion's cold reads cover the preamble and this definition page and a sample of body rows, never all of them.
