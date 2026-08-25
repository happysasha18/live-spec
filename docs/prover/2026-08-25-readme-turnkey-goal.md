# Prover record — 2026-08-25 readme-turnkey-goal

PUSH-REVIEW

Range: c6c7b51b..9a34436a (1 commit)
- 9a34436a README: state the pack's actual end goal, not only the spec-code gap

Files read: `README.md` (full diff), `~/Documents/Codex/2026-08-20/live-spec-completion/outputs/
LIVESPEC_DIRECTOR_REBUILD_PLAN.md` lines 1-30 (the mandate the new paragraph paraphrases),
`tests/test_readme_stance.py` (full, the existing pinning pattern this follows), the rest of
`README.md` grepped for related claims (specialist/taste/strategy/authority/irreversible/
self-running/goal — no other mention, no duplication).

Checks run: independent adversarial review (a different agent than the author), briefed to find
reasons to refuse. Found two real issues, both fixed in the same commit before push:

- The paragraph read as present-tense shipped fact ("it assembles… does… and asks…") rather
  than a stated goal — house style elsewhere in README.md flags aspiration explicitly ("Not yet
  installed," "still leaks," "has no independent check yet," "is young and has run on one
  project"), and this addition's only hedge was a soft "is only the first step." Fixed: added
  "still under construction" and closed the paragraph with "What ships today is the first
  working piece of that goal."
- `scaffold/guardrails/check_tests_present.py` treats `README.md` as a `user_facing_globs` entry
  and reds any such change with nothing under `tests/` — the same gate that blocked a
  near-identical README-only push on 2026-07-12 (per `test_readme_stance.py`'s own docstring).
  Fixed: added `TestReadmeTurnkeyGoalParagraph` to `tests/test_readme_stance.py`, pinning the new
  paragraph's wording and its explicit not-yet-delivered framing, mirroring the file's existing
  pattern.

`python3 scripts/spec-style-lint.py README.md` — caught two real "X, not Y" scissors-register
violations across two rewrite passes (the pack's own permanent ban on naming a thing by denying
its neighbour), both rewritten clean; final state: 0 errors, 0 warnings.
`python3 -m pytest tests/test_readme_stance.py tests/test_traceability.py -q` — 189 passed, run
by the orchestrator directly after the reviewer's fixes, re-verifying independently.

Findings: content accuracy confirmed against the mandate — the paragraph is a close paraphrase,
nothing invented or oversold beyond what the mandate itself states as the goal. Both review
findings (framing, missing test) closed in this commit. No duplication or contradiction with the
rest of README.md.

Blocking: none
