# One list for a new project — the queue file leaves the teaching, 2026-08-31

SKILL-REVIEW

Skill: spec-author
Skill: design-reviewer
Skill: director
Skill: communicator
Skill: live-spec-base
Skill: product-prover-pack

Date: 2026-08-31
Reviewer: skill-creator (Anthropic)

Verdict: PASS — every change repoints one sentence from a queue file to the one list the pack now
teaches. No skill gained a rule, lost a rule, or changed what it does; six of them stopped naming a
document this project retired on 2026-08-28.

## What changed

`q-801`. The pack taught a joining project to keep a separate queue file, `ROADMAP.md`, as the place
a wish lands, and four of those sentences said "in this pack", which stopped being true here when
the queue merged into `PLAN.md`. Two questions were decided before the rewording (both are written
out in `MIGRATION.md`'s 6.1.0 chapter): a project founded today gets the one-list shape rather than
the two-file shape this project just left, and a host that already carries a separate queue file is
asked to change nothing.

- **spec-author.** `SKILL.md`'s fence sentence and `references/glossary.md`'s **Queue row** entry and
  host-path list name the one list. The fence rule itself — name the fences by cited anchor in the
  wish's row — is unchanged.
- **design-reviewer.** The **Queue row** glossary entry names the one list. Reworded so the parked
  item stays the subject; the earlier draft carried two "holding" clauses in one sentence.
- **director.** The shared-document list in the parallel-work paragraph names `PLAN.md`. This is the
  list of documents whose sharing does not make two lanes dependent, and the judgment it states is
  untouched.
- **communicator.** `references/words.md`'s "where the codes resolve" paragraph now sends a row
  number to the one list. The archive lookup it teaches is unchanged.
- **live-spec-base.** Rule 9's current-truth list names `PLAN.md`; `references/glossary.md`'s **a
  queue row** entry, its host-document list, and its row-number sentence do the same. The row's shape
  still resolves to `docs/roadmap-format.md`, which did not move.
- **product-prover-pack.** The path map's queue line names the one list. The map's job — telling the
  external prover where this pack keeps each document it speaks of — is unchanged.

## Findings

- **Two names for one thing (base rule 3).** The word *queue* survives in every skill, and the file
  it used to name does not. Checked that the surviving uses read as the concept rather than the
  retired file: "queue row", "queue-take", "queue archive". Each names a row, a moment, or the
  archive directory, none of which moved. Nothing folded.
- **A pointer left dangling.** `references/glossary.md` said the queue row's home *is*
  `docs/roadmap-format.md`. That page defines the row's shape and did not retire, so the sentence now
  says the shape is defined there rather than that the row lives there. Folded.
- **Reach.** `git grep -n "in this pack" -- skills/ templates/ adopt/` returns four lines, none of
  which names a queue file as the place a wish lands: a communicator rule history about coinages, and
  three that point at this pack's own `PRODUCT_SPEC.md`. Those three are true as written.
- **Line pins.** `adopt/ADOPT.md`'s canonical-set bullet grew by two lines, so the five architecture
  pins into that file moved with it; `guardrails/check-pin-drift.sh` reads green over all 180 pins
  after the repoint. No skill file changed its line count where a pin reads it.
- **Rejected:** widening any of these edits into the skills' surrounding prose. Six sentences named
  the retired file, and six sentences changed.
