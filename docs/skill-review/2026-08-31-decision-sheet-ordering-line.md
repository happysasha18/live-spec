# The decision sheet names what runs next, 2026-08-31

SKILL-REVIEW

Skill: director

Verdict: PASS — one field joins the decision sheet, and the field it joins was already promised by
the task that opened it and by the requirement the same task wrote. Nothing else in the skill moved.

## What changed

`skills/director/SKILL.md`, the decision sheet's field list, gains one line:

> **What runs next** — where other accepted work stands open, which piece runs next and why that
> one, read off the states the plan records rather than composed from memory

It sits between **Evidence** and **Documents that must change**, which keeps the paragraph under the
list true — that paragraph is about the documents line and calls it "the last line", so the new field
had to go above it rather than at the end.

## Why the field belongs in this skill and nowhere else

The ordering law is the reading's own. The owner's word of 27.08 gives it three verbs — bringing work
together, running it side by side, ranking it — and the skill forbade itself from the third in two
places while nothing else owned it. plan-12 gave the law a home in the spec (Requirement 314,
criteria 6 and 7) and a node in the architecture, and read the order itself off the states the plan
records, by command. The sheet's own field was the piece that could not land from a worktree: writing
it makes the installed copies of the skills differ from their source until `scripts/sync-skills.sh`
runs, and that command writes outside the project's tree.

Checked against the alternative homes before writing. The rulebook holds what every skill obeys, and
this is one skill's own artifact. The communicator holds how a report reaches the person, and this is
not a report. The plan holds the states, and it already does — the field reads them rather than
restating them. No second copy of the sentence exists anywhere in the tree; the sheet's fields are
listed in exactly two places, this skill and Requirement 314, and the requirement is the law while
the skill is the form.

## What was checked

- `bash scripts/sync-skills.sh` ran from the main tree in the same pass; ten skills were refreshed
  and `python3 -m pytest -q tests/test_config_health.py` returns 34 passed, so no installed copy
  drifts from its source.
- Requirement 314's criterion 1 lists the field again, and its Context enumeration was brought back
  in step with the criterion in the same change — the criterion had been repaired first and the
  Context left behind, which is the two-homes-for-one-fact shape in miniature.
- The wording is one sentence in the working language: no code, no requirement number, no file name
  in the field itself.
- The skill's own pins in the architecture were re-read after the edit. Two moved and were
  re-pointed; the pin-drift gate returns OK over all 180 pins.
- `tests/test_director_wire_report.py`, the only other reader of the sheet's field names, builds its
  own fixtures and asserts no roster of fields, so it is unaffected. Confirmed by running it.

## What this review did not cover

The skill's other 300 lines were not re-reviewed. The change is one added field inside one list, and
the record of 31.08 for the one-home landing covers the rest of the file as it stood an hour earlier.
