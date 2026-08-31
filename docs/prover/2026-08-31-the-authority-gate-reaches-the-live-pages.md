# Prover record — 2026-08-31 the authority gate reaches the live pages

PUSH-REVIEW

Range: 6cbec19d..HEAD (5 commits, q-497). The commits:

- `a4cb80d1` the authority gate reaches every text page the project tracks
- `4420abb1` an instruction's authority and how a conflict over it is spoken get one home
- `71ab9bb1` q-497 lands: the row and the resume file record what reds where
- `45a50927` the architecture pins follow rule 13's new paragraph down the file
- the head commit, which carries the corrections this record's adversarial read demanded

## What this range is

`guardrails/check-authority-anchor.py` gained a second hard-block arm. Its standing block reached
only files carrying a `DECISION-RECORD` marker, which in this tree is the read-back page and its
template, so a sentence crediting the owner with an instruction he never gave passed anywhere else —
including the class of page the founding fabrication of 2026-07-17 was actually written on. The new
arm reds, on every tracked text page outside the spared set, a sentence crediting a person the
config roster NAMES with a decision, word, ruling or instruction that names no calendar date.

Base rule 13 in `skills/live-spec-base/SKILL.md` gained the half of its own law that was nowhere: a
session's instructions arrive from the person, the tooling and a wrapper at once, only the person's
own messages and profile carry the person's authority, and where a tooling line and the person's
standing word conflict the reply states both and the standing word decides. That is q-497's founding
incident stated as a rule. `tests/test_one_home_per_rule.py` takes it as its fourth entry.

## The spec delta, which is what this record is owed for

`spec/owner-questions-drafts.md`, requirement 238 (INV-207), gained criterion 6 and one sub-clause.
No existing criterion changed meaning, no code was added or retired, and the requirement's Context
and User Story are untouched. The criterion states the new arm's duty and, in the same sentence, the
boundary the pack decided on 2026-07-17 and has not moved: the person-agnostic role forms stay a
reported candidate, since only meaning separates those from the pack's own rule language. The
sub-clause makes the gate owe a statement of its own reach, which is finding B2 below turned into a
duty rather than a promise.

`architecture/rules-and-settings.md` changed in six pin lines and nothing else. Rule 13 grew by
sixteen lines and every line pin below it followed. No fact entered or left the node.

## The adversarial read, and why this record is honest rather than clean

A reviewer with a clean context was briefed to REFUSE the range, and did. Three blocking findings,
all real, all now closed in the head commit:

**B1 — the arm passed the commonest ways to put words in his mouth.** Seven planted sentences on an
ordinary page, gate exit 0: the possessive with a copula after it (`<name>'s ruling was that …`), the
same possessive behind a preposition (`set by <name>'s ruling`), a word between the name and the verb
(`<name> himself asked`, `<name> has asked`, `<name> later decided`), and `according to <name>`. Two
causes. The name-and-verb pattern demanded the two words sit adjacent. And the arm had been given
`tight=True`, inheriting the copula and instrument exemptions — which exist to spare role-word rule
language and, once a roster name is in the sentence, key on exactly the shapes a fabricated
instruction is written in. Closed: the verb arm takes the same two-word gap the possessive arm
already had, `according to` joins `per`, and the arm takes no rule-frame exemption at all. Eight of
the nine plants now red; the ninth is below.

**B2 — "every text page the project tracks" was false by 86%.** 1067 of the tree's 1245 tracked text
files are spared, 900 of them `docs/`, and 152 roster-named unanchored attributions sit inside that
spared set — every one of them a dated record narrating what already happened, which is why the set
is spared and stays spared. The overclaim stood in four places, one of them a *shall*. All four now
name the reach and the exclusion: the spec criterion, the rulebook's rule 13, the matrix row, and
`NEXT_STEPS.md`. The gate's own opening carries a section headed by what it does not reach, and a
test reds if that section is deleted.

**B3 — a host's honest credit lines hard-block.** With a host's own roster, an ordinary changelog
line ("Priya asked for it after the beta round") reds. By INV-207 that line is an unanchored
attribution and owes its date, so the red is the law working; what was missing was any way for a host
to find the dials. The gate's failure message and the config's own note now name them: `person_names`
says whose word is guarded, emptying it stands the arm down, and `waivers` exempts a file-and-snippet
pair with its reason.

Two non-blocking findings, both taken. The "twenty-four role-form sentences" figure compared two
different detectors; re-derived over the reached pages it is 164 under the wide matcher, 125 with the
rule frames exempted, 24 under the tight matcher the advisory pass uses, against two for the named
form. Every place that quoted it now says which. And the first test proved only the one shape that
worked; it now carries all eight.

## The escape that stays open, named rather than buried

`The lane order came from <name>` reds nowhere. It carries no authority word beside the name, so no
pattern keyed on the roster can reach it. It is written in the gate's own opening, in the matrix
row, in the plan row and in `NEXT_STEPS.md`, and `test_the_reach_the_named_arm_does_not_cover_is_written_down`
holds both the escape and the sentence that admits it. The read-back page is its defence, which is
the same answer INV-207 has always given for a fabrication a text gate cannot see.

Files read: `guardrails/check-authority-anchor.py` whole, `guardrails/authority-anchor.json`,
`tests/test_authority_anchor.py`, `tests/test_one_home_per_rule.py`, `skills/live-spec-base/SKILL.md`
rule 13, `spec/owner-questions-drafts.md` requirement 238, `matrix/guardrails.md` row M-388,
`architecture/rules-and-settings.md`, `PLAN.md`'s q-497 row, `NEXT_STEPS.md`,
`docs/prover/2026-07-17-row415-authority-anchor.md` for the scope decision this range had to hold to.

Checks run: `python3 guardrails/check-authority-anchor.py` (exit 0, nine advisory candidates, the
same nine as before this range); the nine planted sentences above, each in its own scratch
repository (eight red, the dated one green, the bare-name one green and recorded);
`python3 -m pytest -q tests/test_authority_anchor.py tests/test_one_home_per_rule.py` (41 passed, 1
skipped); the suite in two parts, since a machine running four other lanes' suites starved the
nested one — `python3 -m pytest -q --ignore=tests/test_guardrails.py` (2473 passed, 55 skipped, 2
failed, both `tests/test_config_health.py`, standing, below) and `python3 -m pytest -q
tests/test_guardrails.py` (96 passed in 16m43s), so 2569 passed, 55 skipped, 2 standing failures
over the whole suite; `bash guardrails/check-pin-drift.sh`
(180 pins, OK, after it named this range's own drift); `python3 guardrails/check-index-generated.py`
(OK, index rebuilt); `python3 guardrails/check-matrix-reference.py` (OK, 551 rows);
`python3 guardrails/check-architecture-reference.py` (OK); `bash guardrails/check-skill-review.sh`
(OK, the record at `docs/skill-review/2026-08-31-live-spec-base-instruction-authority.md`);
`python3 guardrails/check-landing-next-steps.py` (OK); `python3 scripts/check-shipped-language.py`
(OK); `python3 guardrails/check-board.py` (OK); `python3 guardrails/check-doc-rotation.py` (OK);
`python3 scripts/spec-style-lint.py spec/owner-questions-drafts.md` (OK).

Findings: the three blocking and two non-blocking above, all closed in the head commit. A separate
clean-context skill-creator review of the rulebook edit found the dated incident sentence describing
a window-to-window relay, which is the one case the rule's own four sources do not cover; corrected
before that record was written.

Blocking: none. B1 closed by the widened patterns and the dropped exemption, red-proven by the eight
plants. B2 closed by the four corrected statements and the gate's own reach section, held by a test.
B3 closed by naming the host's two dials in the failure message and the config note.

Standing, and not this record's to clear: `tests/test_config_health.py` reds on two cases while the
installed skills and hooks under the machine's own home differ from this branch's sources, which is
what editing a skill on a lane branch looks like until the merged tree is synced. Untouched by this
range, which changes no hook, no installed script and no settings file.
