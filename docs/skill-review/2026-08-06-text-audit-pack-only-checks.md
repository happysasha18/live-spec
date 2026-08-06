# Skill review — text-audit

SKILL-REVIEW

Skill: text-audit

Date: 2026-08-06
Reviewer: skill-creator (Anthropic)

Verdict: passes; body reviewed under the skill-creator writing guide. Five edits land, the body's own
counts agree with its list again, and two commands that measure this pack's own document set leave the
steps an agent follows. One finding stands open against a reference page, with its owner named below.

## What changed

`skills/text-audit/SKILL.md` — the post-repair check list drops the census bullet and the push-time
census comparison, the lead sentence and the follow-up paragraph count three checks where they counted
four, and the maintenance sentence names the doc-findings gate in prose. Five edits, all inside the
body; no reference page changed, and no frontmatter field changed.

## Why the change was owed

The body walked an agent auditing any human-facing text through `python3 scripts/rule-census.py` and
`python3 guardrails/check-doc-findings-bound.py`. The census reads `guardrails/language-rules.json`, the
rules this pack states about its own texts, and counts findings across this pack's live documents. The
push-time comparison reads `guardrails/rule-census.json`, the per-document counts recorded for this
pack's files. An agent auditing a stranger's README and following the body as written ran both against
whichever tree it could reach and reported a number about this pack. The registry records both checks as
kit `pack-only`, and gate ae reds a skill body that names a pack-only check in command position.

## Review pass

**Frontmatter.** `name`, `description` and `metadata.version` stand unchanged, so the skill's triggering
is untouched by this landing.

**Progressive disclosure.** The body stands at 477 lines, down from 481, inside the guide's 500-line working range,
with four reference pages carrying the reader prompts, the meaning-check fields, and the printed rule
list. The edits shorten the body by four lines and add no new layer.

**Internal consistency.** The body's three count claims now agree: the lead sentence counts three
checks, the list holds three bullets, and the follow-up paragraph names which two of the three run
anywhere. The structure-checks bullet list keeps its four commands and now closes with a full stop.

**The replacement prose.** Every replacement sentence sits under the 25-word human-prose cap. The file
measures 0 sentences past the cap, 0 style findings and 0 register findings, which is the count
`guardrails/rule-census.json` records for it.

**The paths that stayed.** `guardrails/language-rules.json` at two places and `guardrails/rule-census.json`
at two places are named in prose describing where a rule and a record live. Prose keeps its paths, so
those four mentions are untouched and correct where they stand.

**The checks the body still names.** The mechanical-lints section names six checks — vocabulary,
weak-words, requirement-shape, spec-style-lint, preshow-register-lint and one-name. The registry records
all six as kit `ships`: each takes the audited file's path on the command line, so each runs over any
project's text. The structure-checks list names requirement-shape, index-generated, matrix-reference and
freeze; the first three are `ships` and freeze is `host-optional`, which the paragraph beneath the list
now states in plain words.

## Findings

1. **`skills/text-audit/references/rewrite-meaning-check.md` still names both pack-only checks in
   command position** — line 104 runs `python3 scripts/rule-census.py` and line 109 runs
   `python3 guardrails/check-doc-findings-bound.py`. Not folded here: this landing's write set holds the
   skill body alone, and gate ae reads `skills/*/SKILL.md` bodies today. Owner: the reference-pages row
   of the host-scripts design (section 9, later row 4), which widens arms G and H to skill reference
   pages and carries the rule that a command line takes a check name while a prose line keeps its path.

2. **The `description` field is terse against the skill-creator guide**, which asks a description to
   name the triggering contexts as well as the job. Not folded: a description edit is a substantive
   skill change of its own and would owe its own review and its own triggering measurement. Recorded as
   a recommendation for a later row.

3. **No eval run accompanies this review.** The change removes two commands and repairs three count
   claims; it adds no instruction and changes no step's method, so a with-skill against without-skill
   comparison would measure nothing this review does not already read. Stated plainly rather than
   implied.
