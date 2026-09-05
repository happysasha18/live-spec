# Skill review — live-spec-base (rule 41's history moved to a reference)

SKILL-REVIEW

Skill: live-spec-base

Date: 2026-09-05
Reviewer: Anthropic's skill-creator — `scripts/quick_validate.py` run directly against
`skills/live-spec-base/`, plus the skill-creator SKILL.md's own Skill Writing Guide (Progressive
Disclosure, Anatomy of a Skill, frontmatter-description accuracy, Writing Style) applied by hand.
The eval/iterate loop does not fit this skill, the same carve-out the prior 2026-09-04 records for
this skill already state.

Verdict: PASS (`quick_validate.py`, quoted below). No findings against the edit itself; this
record's own behavioural check ran separately and outside the skill-creator loop (see below), since
that loop grades a gradeable file output this skill does not produce.

## The tool's own verdict

```
$ python3 /Users/sashaabramovich/.claude/skills/skill-creator/scripts/quick_validate.py skills/live-spec-base
Skill is valid!
(exit 0)
```

## What changed

Rule 41's own history paragraph — the 2026-09-04 measurement (two boards, "53 of 106", the
retired `raised`-field attempt) — moved out of `SKILL.md` into a new `## Rule 41` section in
`references/rule-origins.md`, replaced by a one-line pointer. Every operative sentence of the rule
(the door test, the five "opens none" examples, the defect definition, what still gets done in
place of a tracked row) stayed. `SKILL.md`: 35,276 → 34,057 bytes (-1,219). This closes the gap the
2026-09-04 rule-41 review named: rule 40 already had its own `references/rule-origins.md` section,
rule 41 did not; it now does.

## The behavioural check (outside the skill-creator loop, PLAN q-822)

Whether cutting a rule's own text changes what the rule causes an agent to do is not a question
`quick_validate.py` or the Writing Style guide answers — both check the file's shape, not a
producer's behaviour under it. Checked instead the way this pack checks the director (fresh
producer, deterministic read, no self-grading): four scenario pairs, each run once against the full
pre-cut rule-41 text and once against the trimmed text, by eight independent fresh general-purpose
agents holding nothing but the rule text and the scenario.

1. A self-found dead function (`legacy_loader()`, no callers) — expected: no tracked row, fix or
   note inline. Both agents: no row, same disposition (delete in the same diff, mention in report).
2. A self-found crash (`divide(10, 0)`, unhandled) — expected: fix now, no permission asked, no
   tracked row. Both agents: fixed inline, cited the rule's own "do this, and you see that" test,
   no row opened.
3. A teammate's unverified number mismatch (README vs CHANGELOG) — expected: investigate before
   any row, since neither number is yet a defect anyone meets. Both agents: investigate first,
   fix inline if confirmed, no row opened either way.
4. A person's direct request ("add a dark mode toggle") — expected: a row opens normally, rule 41
   does not block a person-sourced request. Both agents: opened a row, named the person as the
   valid source.

All eight decisions matched their pair. This is a lighter check than the director's own 36-scenario
suite (four pairs, not thirty-six; a bare rule extract, not the whole skill in a real session) — it
clears this one rule's own cut, not a standing measurement for the rulebook as a whole. `PLAN.md`'s
q-822 row carries what still stands open: the next three heaviest rules (7, 38, 31, 36) carry no
comparable history paragraph to move, so cutting them further means cutting operative content, which
this check does not clear.

## Frontmatter and size

Rule count unchanged at 27 (rule 41's own number stays; only its body shrank), so the description's
"twenty-seven rules" still holds. `SKILL.md`: 34,057 bytes. `skills/live-spec-base/` whole
directory: 69,750 bytes.
