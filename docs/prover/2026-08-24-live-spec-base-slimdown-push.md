# Prover record — 2026-08-24 live-spec-base-slimdown-push

PUSH-REVIEW

Range: 2579fbe2..65fb3129
- 65fb3129 live-spec-base: four more illustrative chunks leave the body, word for word

Files read: `docs/prover/README.md` in full (the contract this record follows); the model record
`docs/prover/2026-08-24-architecture-reference-gate.md` in full, for shape only; the full diff of
`65fb3129` (`git show 65fb3129 --stat` and `git show 65fb3129` in full — every hunk in
`architecture/pipeline-and-lanes.md`, `architecture/rules-and-settings.md`,
`skills/live-spec-base/SKILL.md`, `skills/live-spec-base/references/glossary.md`,
`skills/live-spec-base/references/worked-examples.md`, `tests/test_live_spec_base_body_thinned.py`);
`docs/skill-review/2026-08-24-live-spec-base-slimdown.md` in full (the independent skill-creator-
discipline review already on file for this same diff); `ARCHITECTURE.md` in full; `guardrails/pre-push`
in full; `guardrails/check-prover-record.sh` in full (to confirm the exact field-parsing this record
must satisfy); `guardrails/check-language-rules.py` (the `check_sources`/`_home_root` functions, to
understand what the `~/.claude/skills/live-spec-base/SKILL.md:N` pins found in `language-rules.json`
actually resolve against); `tests/test_live_spec_base_body_thinned.py` in full; `tests/test_architecture_format.py`
lines 40-70 (to classify a stray `SKILL.md:17` match as a synthetic fixture string, not a real pin).
`PRODUCT_SPEC.md` read via its actual diff against `origin/main` (empty — see Checks run), not assumed
empty from the commit message.

Checks run: `bash guardrails/check-pin-drift.sh` — `OK (pin drift): 181 pin(s) checked`, no failures.
`python3 guardrails/check-architecture-reference.py ARCHITECTURE.md ARCHITECTURE.index.md` — `OK —
matched 23 of 23 rows scanned; committed Reference equals the fresh build; 401 anchors agree
node-to-table`. `git diff origin/main..HEAD -- PRODUCT_SPEC.md | wc -l` — `0` (empty diff, confirmed by
running it, not by trusting the commit message that this delta is architecture-only). `python3 -m
pytest tests/test_live_spec_base_body_thinned.py tests/test_minor_gate_reconciliations.py
tests/test_clean_context_review.py tests/test_worker_restore.py tests/test_live_channel_law.py
tests/test_architecture_format.py tests/test_traceability.py -q` — 346 passed, 2 skipped (pre-existing,
unrelated to this diff). `python3 -m pytest tests/test_communicator_body_thinned.py
tests/test_skill_review.py tests/test_architecture_pins.py -q` — 30 passed (`tests/test_pin_drift.py`
named in the task brief does not exist in this tree; skipped rather than invented).
`bash guardrails/check-skill-loadability.sh` — `OK: 12 skill(s) load, named, versioned,
negative-scoped`. `bash guardrails/check-skill-review.sh` — `OK: skill 'live-spec-base' carries a
fresh review record`. `wc -l skills/live-spec-base/SKILL.md` — 606; `git show
2579fbe2:skills/live-spec-base/SKILL.md | wc -l` — 620 (620→606 independently reproduced, not taken on
the commit message's word). `nl -ba skills/live-spec-base/SKILL.md` spot-checked by hand against all
19 renumbered pins (2 in `pipeline-and-lanes.md`, 17 in `rules-and-settings.md`) plus the
settings-ladder pointer pin at `SKILL.md:588` — every one landed exactly on the line its label names
(detail below). `grep -n " $" .../SKILL.md .../glossary.md .../worked-examples.md` — no trailing
whitespace in the touched files. `grep -rn "live-spec-base/SKILL.md:"` across the repo (excluding
`architecture/*.md` and the skill-review record already read) — three hits classified individually,
none a live, unrepointed pin (detail below). `python3 guardrails/check-language-rules.py` — `OK`, but
confirmed by `grep -n check-language-rules guardrails/pre-push` (no match) that this gate is not wired
into the push chain, so it carries no weight on this push either way.

Findings: four, all non-blocking; three are confirmations independently reproduced rather than taken
on trust, one is a small positive note.

**1 — all 19 renumbered ARCHITECTURE pins verified by hand from a cold read, not by trusting the
skill-review's own spot check.** `architecture/pipeline-and-lanes.md`'s two (`SKILL.md:128` "rule 7's
lanes sub-rules" → "The parallel-lanes rules sit underneath the fence."; `SKILL.md:150` "one row per
landing commit" → "**One row per landing commit.**") and `architecture/rules-and-settings.md`'s
seventeen (55/56, 106, 122, 235, 277, 298, 309, 319, 333, 390, 398, 407, 438, 504, 552, plus the
worker-restore sub-rule pin at 149) all land exactly on the numbered rule head, sub-rule line, or INV
code their parenthetical describes. `check-architecture-reference.py` and `check-pin-drift.sh` both
independently agree (401 anchors, 181 pins, both green). No drift found anywhere in the renumbered set.

**2 — the settings-ladder pin, flagged as loose by the skill-review, is exact in the actual committed
state; the loose value the skill-review reported was never what got committed.**
`architecture/rules-and-settings.md`'s settings-ladder pin read `SKILL.md:597` before this commit
(confirmed via `git show 2579fbe2:architecture/rules-and-settings.md`) and reads `SKILL.md:588` after
it. `docs/skill-review/2026-08-24-live-spec-base-slimdown.md`'s "Pins" section reports finding the pin
at `SKILL.md:589` at review time and calls it "the one pin I'd call loose," one line off the actual
link. The commit as landed does not carry 589 anywhere — the jump was straight from the stale
pre-slimdown 597 to the exact 588, and `SKILL.md:588` today is precisely the markdown link line
(`[references/settings-ladder.md](references/settings-ladder.md), beside this file.`) the pin
describes. So the one open residue item the skill-review's "net" section lists ("the settings-ladder
pin should move from `SKILL.md:589` to `588`") is not, in fact, open in the committed tree — it reads
as already fixed. Not a defect in either record: the skill-review was accurate about the working tree
at the moment it looked, and a small further edit landed before commit. Flagged so a later reader does
not go looking for a line-589-to-588 fix that has nothing left to do.

**3 — all four relocated chunks verified word-for-word directly against the commit diff, independent
of the skill-review's own comparison.** Read the removed and added text for the paths-and-codes
section and rules 23, 33, 35 side by side in `git show 65fb3129`'s own hunks. All four match exactly,
including the deliberate deixis repairs the skill-review names ("This file" → "SKILL.md", "beside this
one" → "beside SKILL.md," "here" → "SKILL.md cites") and the two summary-sentence replacements left in
the body for rules 33 and 35 (compressions of fact, not copies, and not silent drops — checked each
summary against the moved original for a dropped or altered fact; found none). Rule 23's kept sentence
("That is the same cure that killed invented clock stamps") stays in the body exactly where
`tests/test_live_channel_law.py` needs it, confirmed live by the test run above (23 tests including
that assertion, green).

**4 — the three non-architecture `live-spec-base/SKILL.md:N` hits this repo's grep turns up outside
this commit's own reach are each a non-issue, checked individually rather than waved through as
"probably fine."** `guardrails/language-rules.json`'s `~/.claude/skills/live-spec-base/SKILL.md:N`
entries resolve against the user's globally-installed skill copy under `$HOME`, a different file from
this repo's `skills/live-spec-base/SKILL.md`; their own gate, `check-language-rules.py`, runs clean
(102 home pins read, none unread) and is in any case not part of `guardrails/pre-push`'s chain, so it
carries no weight on this push. `prototype/2026-07-22-spec-format/REPIN-LOG.md`'s two hits are a dated
historical log from an old prototype folder, outside `check-pin-drift.sh`'s reach set and untouched by
this commit. `tests/test_architecture_format.py:61`'s `SKILL.md:17` is a synthetic fixture string
inside `test_archformat_refuses_the_retired_table_shape`, testing that a retired 4-column table shape
is rejected — not a real pin, and unaffected by any line renumbering. None of the three needed
repointing and none is broken.

Also checked and clean, not written up as separate findings: frontmatter `description` claims "three
on-demand reference modules under `references/`" and `ls skills/live-spec-base/references/` shows
exactly three files (`glossary.md`, `settings-ladder.md`, `worked-examples.md`) — accurate. Markdown
headings in both touched reference files are well-formed `##` sections at the right level, links
resolve to files that exist, and no trailing whitespace or stray double-space typos were introduced
(checked by grep against the new sections). `tests/test_live_spec_base_body_thinned.py` is a real
conservation floor, not a rubber stamp — read the six assertions in full; none is vacuous, and the
"body has not regrown" ratchet (615) sits nine lines above the real 606.

Blocking: none

## What I went looking for and did not find

An adversarial pass on this range is mostly a pass against the possibility that the pin repoint or the
word-for-word move has a silent defect the green gates miss, since the gates (`check-pin-drift.sh`,
`check-architecture-reference.py`) trust their own ±2-line tolerance and their own reach sets rather
than reading prose. I did not stop at green: I re-derived, from a cold `nl -ba`, every one of the 19
renumbered pins' target lines myself rather than accepting the skill-review's table, and found the same
exact-hit result independently — including the one place (finding 2) where my own check disagreed with
the skill-review's account of a specific line number, which is the kind of thing a read that only
skimmed the skill-review's conclusion would have missed. I looked for stale `SKILL.md:N` citations
anywhere else in the tree a pin-repointing pass could have missed (finding 4) and found none live. I
diffed `PRODUCT_SPEC.md` myself rather than accepting "this commit doesn't touch it." I did not find a
lost rule, a broken link, a mismatched frontmatter claim, or a pin that fails to prove — the range is
clean.

Reviewer note: `tests/test_guardrails.py` was not run, per this session's standing warning that it
`git stash`es the tree without restoring on an interrupted run; its two gate-adjacent needles were not
separately spot-checked in this pass since neither `guardrails/pre-push` nor `guardrails/README.md` was
touched by this commit (only `architecture/*.md`, the skill files, and the test/review additions were),
so nothing in this range exercises that suite's subject matter. The full `pytest -q` suite was likewise
not run, per this session's standing warning that it hangs in this environment; the targeted suites run
above cover every file this commit's diff touches or that touches it back (pins, architecture format,
the skill's own conservation test, the live-channel law, traceability, communicator's sibling
conservation test, skill-review, and architecture pins).
