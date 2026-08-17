# `SKILL-REVIEW` — live-spec-base, the reading key returns to the body

Skill: live-spec-base. Date: 2026-08-17. Range: 9efe559..HEAD.

This record supersedes `docs/skill-review/2026-08-17-live-spec-base-slimdown.md`. That first-pass
record was written against commit 5295b06 and is now stale: commit 94ae4c3 landed after it and
changed `skills/live-spec-base/SKILL.md` again, so the push gate (`guardrails/check-skill-review.sh`,
SPEC INV-208) no longer accepts the first record as covering the file's current state — its own
commit sits before the skill's last change, not at or after it. This is a fresh, independent
re-review of the current body, not an amendment of the old one.

Commits of the range touching `skills/live-spec-base/`:

    5295b06 live-spec-base: the glossary and the worked examples move to references, word for word
    94ae4c3 The reviews' findings land: firing conditions and the reading key return to the bodies, and the orphaned reference is reachable again

Verdict: ALLOW WITH FINDINGS. The one serious defect the first-pass record raised — the body's own
reading key for "seat / senior / orchestrator / lead" sitting behind an unmotivated pointer — is
fixed. What remains open is smaller and was already named once: a stale frontmatter description, two
weak reference pointers, and a leftover deictic slip inside the moved glossary text. None of it is a
lost rule.

## The delta, confirmed directly

I did not take the brief's word for what 94ae4c3 changed. `git show 94ae4c3 -- skills/live-spec-base/`
touches exactly one file, `skills/live-spec-base/SKILL.md`, and the diff is a pure three-line
insertion right after the glossary pointer, before "Open that module when a term is being resolved":

    +One term is stated here rather than there, because the rules below use all four of its names: the seat,
    +the senior, the orchestrator and the lead. The four names mean the one session.

Nothing else in the skill's body, frontmatter, or references directory moved in this commit. The
wider commit also touched `ARCHITECTURE.md`, `guardrails/rule-census.json`, and files under
`build-pipeline` and `communicator` — those two skills are outside this review's subject and are not
assessed here.

This is not a literal restoration of the sentence that left the body in 5295b06. The original glossary
entry for "the seat" (still verbatim in `references/glossary.md:15-18`) says "the glossary keeps the
one name seat throughout. It records the senior and the orchestrator as the source's other names for
it, and this file adds a fourth, the lead." The new body sentence is fresh prose that states the same
fact — four names, one session — in the body's own voice, not a copy-paste of the glossary's. That is
the right move: the glossary's "this file adds a fourth" already only made sense from inside the old
body, so re-pasting it verbatim would have re-imported the very deixis problem noted below. Restating
the fact in new words that are true from the reference file's new home is the correct fix, not a
shortcut.

## What this fixes

The first-pass record's most-argued finding was that "senior," "the lead," "the orchestrator," and
"the seat" are used throughout the body (senior at rule 5, 7's Brief-time-disjointness bullet, and
elsewhere; the lead through rules 5, 6, 25; the orchestrator titling rules 25 and 27; the seat running
throughout) with no statement anywhere in the body itself that they name one session — the only such
statement lived in the reference file, reachable only by a reader who already knew a term needed
resolving. That gap is now closed. The sentence sits at body lines 49-50, immediately under the
glossary pointer, so a reader who opens `SKILL.md` and hits "the lead" at rule 5 or "the orchestrator"
at rule 25's heading has already passed the sentence that ties the four names together, five lines
into the file past the glossary link. I read rules 5, 6, 7, 25, and 27 again with this in place: each
now parses on a first read without needing the glossary at all.

## References and pointers, re-checked

All three reference files still resolve and none is orphaned. `references/glossary.md`,
`references/worked-examples.md`, and `references/settings-ladder.md` are each pointed at from the
body (lines 46, 68/367/527, and 595 respectively), and I ran `guardrails/check-skill-loadability.sh`,
which reports "11 skill(s) load, named, versioned, negative-scoped" — OK, no regression.

The two findings the first-pass record raised here are unchanged by 94ae4c3, since it touched none of
this text. The two worked-examples pointers ("See references/worked-examples.md for the per-kind
illustration of both" at rule 24, and rule 32's "written out in references/worked-examples.md") still
say what is there but not which of the file's three headed sections to land on — a reader still walks
past the register-guard case to find rule 24's, or past both to find rule 32's. And the frontmatter
`description` still names only `references/settings-ladder.md` as "the settings ladder... opened when
a setting is being resolved," with no mention that the skill now carries two more on-demand modules.
Metadata is the layer that is always in context; this sentence has been inaccurate since 5295b06 and
94ae4c3 did not touch it.

## Trigger and description

I re-ran the check this skill's own test suite performs. `tests/test_minor_gate_reconciliations.py`
derives the rule count from the body's numbered heads (`re.findall(r"^\d+\. \*\*", base, re.M)`) and
asserts the description states that same number; `tests/test_clean_context_review.py` separately
asserts the literal string "thirty-four rules in the body" appears. I counted independently with the
same regex and got 34 — rules 1 through 29 and 31 through 35, with 30 retired and skipped, matching
the body's own "Rule 30 was cut whole from this rulebook; its number is retired and stays open." Both
tests pass (`pytest tests/test_minor_gate_reconciliations.py tests/test_clean_context_review.py -q` →
11 passed, 2 skipped). The description's rule count still agrees with the body. Nothing in 94ae4c3
added or removed a numbered rule head, so this was never at risk from this delta, but it was worth
re-confirming since it is machine-checked and I had the body open regardless.

The description otherwise still does what a trigger needs: it names all ten sibling skills, gives
three firing contexts, and is appropriately pushy per skill-creator's guidance. The stale
settings-ladder-only sentence noted above is the one blemish, unchanged since the first-pass record.

## ARCHITECTURE.md pins

The task brief flagged that a block of `ARCHITECTURE.md` pins into this body was renumbered by
94ae4c3 and asked me to check honestly whether they land. They do. `git show 94ae4c3 -- ARCHITECTURE.md`
shows every `skills/live-spec-base/SKILL.md:<N>` pin shifting by exactly +3 (68→71, 117→120, 133→136,
244→247, 286→289, 307→310, 318→321, 328→331, 342→345, 397→400, 405→408, 414→417, 451→454, 517→520,
160→163, 561→564, 140→143, 161→164, and the settings-ladder pointer note 585→588) — the arithmetic
consequence of the three lines inserted before all of them. I spot-checked eight of these directly
against the current file with `awk`: line 71 and line 136 and line 400 are blank lines immediately
before "## The shared rules," rule 7, and rule 26 respectively (this file's pre-existing convention of
pinning one line ahead of a heading); line 120 lands inside rule 6's checkpoint text near its INV-107
clause; line 163 lands on the last line of the preceding bullet, one line before the worker-restore
sub-rule it labels at 164; line 454 lands inside rule 31's card-scanning sentence; line 520 lands
inside rule 32's major-release clause; line 564 lands inside rule 35's session-extract sentence. Every
one is on-topic for its label. I then ran `guardrails/check-pin-drift.sh`, which checks all 207 pins
in the repository against a ±2-line tolerance and reported "OK (pin drift): 207 pin(s) checked" with
no failures — an independent, mechanical confirmation covering every pin I did not hand-check too.

## What is still open, honestly

Four items from the first-pass record are untouched by 94ae4c3, because it never edited that text.
Naming them again rather than re-arguing them:

1. The `reds` idiom ("Where a sentence here says a check *reds* something, it means the check fails on
   it") is still only in `references/glossary.md:37`, while the body uses the verb at line 16, well
   before the glossary pointer at line 46.
2. The glossary's own prose still carries the dangling deixis the first-pass record found:
   `references/glossary.md:16` opens "The words this file uses" as a copied section heading where
   "this file" meant `SKILL.md`, and line 18's "this file adds a fourth" and line 29's "This file
   calls it a row" have the same problem. These are cosmetic, not load-bearing — no fact is now
   unreachable — but they were not cleaned up in this pass.
3. The two worked-examples pointers still don't name a section (noted above).
4. No conservation test exists for this skill's body-thinning, unlike `communicator`'s
   `tests/test_communicator_body_thinned.py`. Nothing reds today if a later edit silently drops one of
   the three reference pointers or empties a reference file.

None of these is new, and none is a lost rule or a broken pointer — I checked each again rather than
assuming the first-pass record still held, and each is exactly where it was left.

## The net

The one thing this review most needed to confirm — that the body's reading key for its own four
session-names actually returned, in working prose, at a place a reader meets before the names — is
true. I read the diff, read the new sentence in place against the rules that use all four names, and
confirm it resolves the gap. The pin renumbering is arithmetically uniform and independently verified
green by `check-pin-drift.sh` at 207/207. The loadability gate is green at 11/11. The rule-count claim
in the description is machine-verified true today. What is left outstanding is the same short list the
first-pass record already named and none of it was touched by 94ae4c3, so none of it is a new
regression — it is simply not yet done. That combination, a real fix landed and a known small residue
left open, is ALLOW WITH FINDINGS rather than a clean ALLOW or a BLOCK.

Reviewer: an independent adversarial re-read of the current `skills/live-spec-base/` body against
9efe559 and against the first-pass record at `docs/skill-review/2026-08-17-live-spec-base-slimdown.md`,
performed by a dedicated reviewer agent working from the skill-creator discipline installed at
`~/.claude/skills/skill-creator`. No file under `skills/`, `ARCHITECTURE.md`, `guardrails/`, or
`tests/` was modified during this review; only this record was written.
