# Prover record — 2026-08-25 live-spec-base-lenses-extraction

PUSH-REVIEW

Range: b7ad8f73..1d2ce1f2 (1 commit: `1d2ce1f2` "live-spec-base: five bare dated citations
move to docs/lenses.md, no pointer left behind"). Four files changed:
`skills/live-spec-base/SKILL.md`, `docs/lenses.md`,
`docs/skill-review/2026-08-25-live-spec-base-lenses-extraction.md` (new),
`tests/test_live_spec_base_body_thinned.py`.

The same commit also answers gate h (tests-present), which wants a `tests/` change alongside
any `skills/live-spec-base/SKILL.md` edit. The honest answer here is not a cosmetic touch: the
ratchet ceiling (`CURRENT_MAX_LINES`) drops from 615 to 608, tightened to match the real
`-5` line reduction rather than left at its old, now-stale headroom — this is the same
"cap only ratchets down" principle rule 22 itself states. `python3 -m pytest
tests/test_live_spec_base_body_thinned.py -v` re-run after this second commit: 6 passed.

## What this is

`skills/live-spec-base/SKILL.md` sits near its line-count ratchet ceiling
(`tests/test_live_spec_base_body_thinned.py`). A prior attempt at thinning it
(`docs/prover/2026-08-25-live-spec-base-second-pass.md`, fully reverted) found the real
byte-positive move by accident: deleting a rule's bare dated citation ("the owner's word,
DATE: ...", no narrated worked case) with NO pointer left behind, filed instead in
`docs/lenses.md` — a file that calls itself the pack's provenance home and that no skill
session ever loads, so needs no pointer sentence back. That attempt did this for 2 of ~9
such citations, by accident, and those 2 produced 197 of its 259 saved bytes; the other 9
edits added pointer sentences to `references/worked-examples.md` and net LOST bytes.

This slice repeats the working pattern deliberately, for the remaining 5 bare citations
(rules 22, 31's first sub-bullet, 33, 34, 35 — INV-98, INV-189, INV-237, INV-247, INV-302),
re-derived by a fresh full read of the file rather than trusting the prior count.

## What was checked before committing

Each of the 5 removed sentences was pure dated provenance whose substantive claim is
independently stated elsewhere in the same rule — verified rule by rule, not assumed
(full accounting in the accompanying skill-review record,
`docs/skill-review/2026-08-25-live-spec-base-lenses-extraction.md`). Each new
`docs/lenses.md` entry is keyed by its INV code, checked against no existing duplicate.

An independent adversarial reviewer (separate agent, briefed to reject not confirm) checked:
paragraph integrity of all 5 cuts (no dangling connective, no lost `INV-` substance);
`docs/lenses.md` entry placement (no duplicate code, correct section, no fabricated fact
beyond the removed text's own claim); the byte/line delta directly (`607→602` lines,
`52202→51705` bytes, confirmed exact); the two narrow test files; a fresh lint run diffed
byte-for-byte against `HEAD`'s lint output (14 errors both sides, identical list — no new
`scissors` or other register violation, unlike the prior attempt's regression); and a broad
grep of `tests/` for all 5 removed phrases (one docstring-only mention in
`tests/test_convergence_rule.py`, no assertion on it). Verdict: CONFIRMED-SAFE-TO-COMMIT.

`bash scripts/sync-skills.sh` run after the edit — `live-spec-base: synced: 5.0.0 -> 5.0.0`
(content changed, version unchanged, correct per this pack's one-version-per-package rule,
not a per-skill semver bump).

## Result

`skills/live-spec-base/SKILL.md`: 607 → 602 lines, 52,202 → 51,705 bytes (−497 bytes, ~124
tokens). Genuinely larger than the prior attempt's net −57 bytes, and unlike that attempt,
every byte saved here came from the proven-safe pattern — zero pointer sentences added.
Ratchet ceiling untouched (`CURRENT_MAX_LINES` in the test file), margin widened, not
narrowed. This does not close the file's larger goal (skill-creator's <500-line ideal) —
that still needs the "second, more structural pass" (perigroup normative rules, not just
extract citations) the prior investigation named and deferred; recorded as still open.

Files read: `skills/live-spec-base/SKILL.md` (full, both before and after), `docs/lenses.md`
(full, both before and after), `docs/prover/2026-08-25-live-spec-base-second-pass.md` (the
prior reverted attempt's record, in full, for the working pattern and its failure modes),
`docs/spec-style.md` R15 (provenance-home rule), `docs/skill-review/2026-08-17-live-spec-base-slimdown-2.md`
(format precedent for the accompanying skill-review record), `guardrails/check-skill-review.sh`
(gate s's exact requirements — freshness, marker, verdict line).

Checks run: `python3 -m pytest tests/test_live_spec_base_body_thinned.py -v` — 6 passed.
`python3 -m pytest tests/test_convergence_rule.py -q` — 4 passed. `python3
scripts/spec-style-lint.py --tier full skills/live-spec-base/SKILL.md` — 14 errors, byte-
identical to `HEAD`'s output (compared via `git stash`/`git stash pop`, working tree
confirmed restored exactly by `git status` after). `wc -lc skills/live-spec-base/SKILL.md`
before (`git show HEAD:...`) and after — confirmed exact delta above. `grep -rl` across
`tests/` for all 5 removed phrases — one non-assertion docstring hit, no test broken.
`bash scripts/sync-skills.sh` — 1 skill synced, version unchanged as expected.

Findings: none blocking. One genuine, verified net reduction, following the one pattern this
corpus has already proven safe rather than repeating the prior attempt's mistake.

Blocking: none
