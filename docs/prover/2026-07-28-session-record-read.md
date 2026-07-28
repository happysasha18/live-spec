# Prover record — 2026-07-28, Requirement 303 (a session's record read at both ends)

Mode: CROSS-LINK, over the new requirement and its seams with the requirements already in the
document. Run by a fresh seat with no part of the authoring context, briefed from the primary
sources: the requirement itself, Requirements 25, 93, 125, 126, 127, 128, 292 and 298,
`scripts/session-extract.py`, `guardrails/check-handover-provenance.py`, rows M-483 to M-485, and
rule 35 of the base rulebook.

The previous record on this document is `docs/prover/2026-07-28-language-rule-home.md`; it carries no
unfolded row.

## Findings

| # | Severity | Finding | Folded / rejected |
|---|---|---|---|
| 1 | defect | Nothing states when the extract is produced, so criterion 11 assumed a file no criterion creates. | folded — criterion 10 runs the extractor over the closing session's transcript before the handover is written |
| 2 | defect | The opening reader would take the newest transcript, which at a session's open is its own. | folded — criterion 26 takes the extract the previous handover names, closing the loop through the provenance the gate holds |
| 3 | defect | A scratch directory is cleared, and the opening step read a file that may be gone. | folded — criterion 27 re-derives the extract from the previous session's transcript |
| 4 | defect | Criterion 20 read weaker than the gate it describes: it refused only a handover naming none of the three. | folded — the criterion, row M-484 and rule 35 all now refuse a handover naming fewer than all three |
| 5 | defect | The vacuity guard read the directory's whole contents, so a directory of drafts alone passed green over no subject. | folded — criterion 23, the gate and row M-484 read the emptiness over the declared handovers, and `test_a_directory_of_drafts_alone_reds_over_no_subject` holds it |
| 6 | defect | The handover had a producer and no consumer: no criterion made anyone read it. | folded — criterion 25 has the opening reader take the previous handover beside its extract |
| 7 | defect | No criterion said what a handover contains, so its body was undefined. | folded — criterion 17 |
| 8 | defect | The leave-word close and the movement end never named the handover, so a lawful close shipped without one. | folded from this requirement's own side — criterion 13 writes the handover beside the resume file's replacement, and criterion 14 rides the wind-down; the neighbouring requirements are left as they stand, since one home per fact puts the new law's sentence where the law lives |
| 9 | defect | The close needs a fresh agent at the moment the wind-down is halting workers. | folded — criterion 14 spawns the reader before the safe point |
| 10 | defect | "session handover" sits beside the "handoff note" of Requirements 25 and 128, which the glossary never defines. | rejected here, carried to the queue — the two name different things and the new one is now defined in the glossary; renaming an established artifact across two requirements is its own row, and the row's words are in the delivery report |
| 11 | defect | "session lead" is an actor this document does not define. | folded — criterion 30, rule 35 and row M-485 now say the seat, the actor the glossary defines |
| 12 | defect | The Context pointed at a journal entry that does not exist. | folded — the sentence is gone, and the journal line the movement owes is in the delivery report |
| 13 | defect | Two sessions closing on one day would write one handover name. | folded — criterion 16 carries the date and the session identity in the file name |
| 14 | recommendation | The handover directory grows with no ceiling, beside a sibling law that caps the resume file. | rejected here, carried to the queue — a retention rule for a record directory is its own row, and the growable-doc bound governs single documents |
| 15 | recommendation | The privacy split stopped at the extract and said nothing about the committed handover. | folded — criterion 18 keeps the person's own words out of a handover |
| 16 | recommendation | Criterion 9's "each run" was falsified by the listing mode and the failure paths, which print no reach line. | folded — the criterion is scoped to a run that writes an extract |
| 17 | recommendation | Row M-485 claimed a never-side no clause-presence test can reach. | folded — the row's never-side now states the text-presence claim its five checks hold |

## Open decisions

The requirement carries no `⟨DECIDE⟩` marker, and none was raised by this pass.

## The verdict, after the fold

Fifteen of the seventeen findings are folded into the requirement, the gate, the tests, the matrix
rows and the rulebook. Two are carried to the queue with their reason above, and neither blocks the
landing: one is a rename across two neighbouring requirements, and one is a retention rule for a
record directory.
