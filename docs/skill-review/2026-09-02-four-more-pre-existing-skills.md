# Skill review — four more skills unreviewed against origin/main

SKILL-REVIEW

Skills: architect, build-pipeline, communicator, director

Date: 2026-09-02

Reviewer: skill-creator quality lens (Progressive Disclosure, Anatomy of a Skill,
frontmatter-description accuracy) applied by hand, against `git diff origin/main..HEAD --
skills/architect/ skills/build-pipeline/ skills/communicator/ skills/director/`.

Verdict: found by checking the earlier five-skill review (`2026-09-02-overnight-run-five-skills.md`)
against the actual push gate, which compares to `origin/main` rather than tonight's own
`534cb16b` starting point — these four carry real, pre-existing unreviewed changes from before
tonight's session, none of them this session's own work. All four hold up.

## What changed, and why each holds

**`architect/SKILL.md`, `build-pipeline/references/minor-bump-gate.md`,
`director/references/delegation-protocol.md`, `director/references/request-kind-table.md`.** The
same small annotation, four places: an existing numeric default (the carve-back rule's "2 no
answers," the design-review gate's "3 asks," the brief-size guidance's "[default]" tag already
present beside "~8 files," the recurring-bug window's "~30 days") gets one clause naming it
plainly — "no incident or source behind the N — an engineering default, not a policy decision."
None of the four numbers changed; each place only stopped implying a history it never had. This is
the same honesty `q-805` argues for tonight, applied earlier today to a different class of number
(a working default openly labeled as one, never a document held to it as a gate). Read each site in
context: the surrounding rule is unchanged and still parses as a complete instruction.

**`communicator/SKILL.md`, `communicator/references/page-lifecycle.md`,
`communicator/references/rule-histories.md`, `communicator/references/writing-register.md`.**
(Corrected in review, `docs/prover/2026-09-02-q805-and-followups-review.md`, finding 5: this record
originally claimed `writing-register.md` was already reviewed elsewhere; it names neither
`communicator` nor that file, so it's reviewed here instead, where it actually belongs.)
`writing-register.md` loses one trailing citation — "(Defined 2026-07-07 after the owner rejected
both a 'confident product pitch' draft and a persona-flavored one; his words, 2026-07-07: ...)" —
off the register's own opening paragraph; the paragraph reads complete without it, and the fact
survives in `JOURNAL.md`'s matching "2026-07-07 — the writing register is defined, after two
rejected drafts" entry. This is `q-803`'s own citation sweep reaching `communicator` proper more
broadly too. Eight rule citations and the intro's glossary
pointer move out of `SKILL.md`'s body; `rule-histories.md` — the file whose own stated job is
holding exactly this ("this file is read when a rule's ORIGIN is wanted") — grows to hold them, each
with a `Where this rule's ... was fixed is in references/rule-histories.md` pointer left at the
rule's own site so a reader can still find it. `page-lifecycle.md` loses a trailing blockquote
citation the same way. Checked: every rule's operational text is intact above its stripped citation;
none of the eight reads as incomplete or dangling. `rule-histories.md`'s own new intro line ("eight
of the twenty-two rules, plus the intro's glossary pointer and one writing-register rule") correctly
counts what actually moved.

## Findings

None. Straightforward, consistent, no rule weakened.
