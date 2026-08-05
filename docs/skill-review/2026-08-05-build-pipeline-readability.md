# Skill review — build-pipeline names its words, its code homes, and its file paths

SKILL-REVIEW

Skills: build-pipeline.

Date: 2026-08-05
Reviewer: skill-creator (Anthropic), run by this session.

Verdict: passes. The change adds a definitions block and repairs nine pointers that resolved to
nothing or to the wrong place. It removes no instruction and adds no step to the pipeline.

## What changed

A two-reader audit read the whole skill twice, once under the printed rule list and once under the
unprompted brief. Both readers stopped at the same class of place: a step the page names but a
reader cannot carry out.

The repair has two halves. The first is a new section, "Words this skill uses". It states where the
paths point, defines twenty-eight terms the body already used, and names the code families with
their home. The second half is nine pointer fixes, each checked against the tree.

- `ARCHITECTURE.template.md` now reads `templates/ARCHITECTURE.template.md`, which is where the file
  sits. The step 5 template is named for the first time, at `templates/TEST_MATRIX.template.md`.
- "The eight steps are guidance" now reads "The nine steps", matching the nine the page numbers.
- "the work-kind table below" now points at `references/work-kind-table.md`, since no table stands
  below that sentence.
- The reach map is named: the `reach_classes` block of `guardrails.config.json`. The suite command
  is stated for the pack, with the host's own runner named as the alternative.
- The guardrails runner is named: `guardrails/pre-push`, which a project installs as its own hook.
- `test_traceability.py` now reads `tests/test_traceability.py`, its real path.
- "three recorded lines per file" now names the three: current state, what changes, what must
  survive.
- "communicator rule 6" keeps its wording and now says which of that skill's two numberings it means.
- The six excuse-thoughts stand on the page, so the section's own trigger works without opening the
  reference file.
- The closing skill list gained the six pack skills the body leans on and the list left out.

## Why it was worth a change

This skill sequences every change that runs through the pack. A step a reader cannot perform is a
step that gets skipped with nobody noticing, and both readers found several. One reader could not
locate the architecture template at all. Neither could name what a lane, a pen, a door, or a
footprint is from the page. Neither could resolve a single `base rule N` citation.

## What the review looked at

**Does the summary line still trigger correctly?** The line is untouched. Every change sits in the
body.

**Does the body still hold together?** Yes. The definitions block sits between the pack blockquote
and the pipeline order, so a reader meets the words before the first use. The pipeline paragraph
gained a heading of its own, "The pipeline in one line", to keep it out of the definitions section.

**Does it instruct anything new?** No. Every edit either names a path that was already implied,
completes a set the text already claimed, or fills a slot the text left open. Where a repair would
have changed an instruction, the finding was recorded and the text left standing. Nine such
findings are listed in `~/context-slimdown/reports/audit-build-pipeline-two-reader.md`.

**Could any edit break a consumer?** Forty test files read this skill's body. Every literal they pin
was checked before the edit, and `communicator rule 6` was kept verbatim for that reason.

## Findings

None blocking.

Nine findings are recorded and left in the text, because repairing them would change what the skill
instructs. They are the owner's call: the prover-mode count against `product-prover`'s three, the
design-review cadence at FEATURE-FIT intake, the retired coverage checklist in the matrix template,
the redundancy floor of 119 against the page's "zero open pairs", the CHANGELOG the pack does not
keep, the visibility-versus-presentation routing conflict, the base rule 17 citation for a clause
that rule does not carry, the "Order is law" list that stops two steps short of the opening order,
and the visual sample set that names no home.

## Checks run

`python3 scripts/rule-census.py skills/build-pipeline/SKILL.md` — 257 findings before, 256 after.
The count fell by one.

`python3 scripts/preshow-register-lint.py skills/build-pipeline/SKILL.md` — clean.

`python3 guardrails/check-one-name.py skills/build-pipeline/SKILL.md` — no alias present.

`python3 -m pytest tests/test_config_health.py tests/test_traceability.py -q` — 12 failed, 196
passed. The same run against the pre-change skill body failed 13, so this change fixed one and broke
none. Every remaining failure reads `live-spec-base`, `PRODUCT_SPEC.md`, `ARCHITECTURE.md`, or
`TEST_MATRIX.md`, which other sessions hold open right now.

`sh guardrails/check-skill-loadability.sh` — 11 skills load, named, versioned, negative-scoped.

The repository copy and the installed copy under `~/.claude/skills/build-pipeline/` hold the same
bytes, checked file by file.
