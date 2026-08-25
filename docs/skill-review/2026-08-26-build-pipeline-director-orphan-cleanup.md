# Skill review — build-pipeline, director

SKILL-REVIEW

Skill: build-pipeline
Skill: director

Date: 2026-08-26
Reviewer: skill-creator quality lens (Anthropic's skill-creator SKILL.md's own writing guide —
Progressive Disclosure, Anatomy of a Skill, frontmatter-description accuracy — applied by hand;
the tool's own eval/iterate loop is reserved for Полоса B п.10, after the whole build-pipeline
cutover completes, per the owner's explicit instruction not to skip that step)

Verdict: no blocking findings; both skills' bodies and frontmatter are unchanged, only their
`references/` sets were corrected — coherence checked below.

## What changed

Полоса B п.7 (classify tests pinned to build-pipeline's now-shrunk prose) surfaced two orphaned
files left behind by earlier reference-file moves: `skills/build-pipeline/references/
drafter-applier-example.md` was still physically only in build-pipeline even though
`skills/director/references/lanes-and-pen.md` (moved there in Полоса B п.1) already linked to it
by a relative path that resolved nowhere, and `skills/build-pipeline/references/
verify-step-detail.md` was a stale duplicate of the already-canonical, since-expanded
`skills/director/references/verify-step-detail.md`. Fix: `git mv` the drafter-applier worked
example into `director/references/` (fixing the dead link, and correcting the file's own
"referenced from" pointer to name `references/lanes-and-pen.md` instead of `SKILL.md`), and
`git rm` the dead verify-step-detail.md duplicate. Two tests that depended on the orphaned
files surviving only through `read_all`'s `references/*.md` glob were redirected to their real
current home (`tests/test_drafter_applier_form.py`'s `HOME`, and `tests/test_traceability.py`'s
`test_adversarial_verify_option`, whose director-side needles needed two of four rewording to
match director's actual, since-expanded phrasing rather than a bare path swap).

Neither skill's `SKILL.md` body or frontmatter changed — only their `references/` directory
contents.

## Findings

None blocking. Per-skill check:

- **build-pipeline** — frontmatter `description` (unchanged) already names the narrow
  transitional-adapter scope; this cleanup only removes a `references/` file the body never
  pointed at, so the skill's readable surface loses nothing a reader could reach. The remaining
  two reference files (`minor-bump-gate.md`, `project-setup.md`) are both still named from the
  body and confirmed current by `tests/test_setup_entry.py`. No dangling references introduced.
- **director** — frontmatter `description` (unchanged) already covers the drafter-applier lane
  form as part of the lane law. Adding `drafter-applier-example.md` to `director/references/`
  matches the established Progressive Disclosure pattern already used for `lanes-and-pen.md`'s
  other worked-example offloads — a large table or worked example lives in `references/`, a short
  pointer stays in the body. The file's self-description now correctly names its one caller.

Independent adversarial review (a fresh reviewer instructed to find grounds to reject, not
confirm) returned ALLOW WITH FINDINGS: the substantive fix (link resolution, needle wording,
byte-identical move modulo the one corrected pointer sentence) verified correct; two
non-blocking findings noted for a future, separate pass — `docs/PROGRESS.md` (an auto-generated
snapshot dated 2026-08-19, outside today's change) and `docs/director/capability-map.md` (already
flagged in the working handoff as unsynced since the Полоса B п.6 cutover, not this change's
scope) still cite the pre-move path. Neither touches a skill body, a test, or a guardrail, so
neither blocks this push; tracked in the handoff for a later docs-sync pass.

## Fast-follow (same push range): the third orphaned test CI caught

The first push (commit `ccb3d9fb`) missed that `tests/test_periodic_full_audit.py::
test_audit_is_defined_adversarial_by_nature_once` also depended on the deleted
`build-pipeline/references/verify-step-detail.md` surviving via `read_all`'s glob — it searched
for the sentence "An audit is adversarial by nature: a whole-read that sets out to break the
work, refute its claims, and find its holes." CI's full suite caught this; the local targeted
run (scoped to the files the classification named) did not include this test file.

That exact sentence had quietly dropped out of `director/references/verify-step-detail.md`
during the Полоса B п.6 rewrite (a real, pre-existing content loss the dead build-pipeline
duplicate had been silently masking) — not a text this fix invented. Restored it verbatim into
`director/references/verify-step-detail.md`'s "The audit protocol, once it has fired" section
(confirmed character-for-character against `git show ccb3d9fb^:skills/build-pipeline/
references/verify-step-detail.md`, by the second independent reviewer, not taken on the first
reviewer's word), and redirected the test's read path and docstring from build-pipeline to
director. A second independent adversarial review (a different fresh reviewer, same instruction
to find grounds to reject) returned **ALLOW**: diff scope matched exactly what was claimed,
restoration verified verbatim against the pre-deletion source, line-wrap quality checked, test
logic verified correct, targeted re-run (342 passed) and both local guardrail scripts
(pin-drift, skill-loadability) green, and a fresh grep swept for any other place "adversarial
audit"/"An audit is adversarial by nature" might now collide or duplicate — none found; the
phrase is defined in exactly one normative place, per INV-46/C8's "once" requirement. One
non-blocking stylistic nit (`read_all` instead of the more explicit `_read` on a non-SKILL.md
path — behaviourally identical, matching a nit the first reviewer raised on a different file in
this same range) was left as-is by design, consistent with the first round's disposition of the
same nit.
