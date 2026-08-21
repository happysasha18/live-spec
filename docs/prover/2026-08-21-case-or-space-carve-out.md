# Prover record — 2026-08-21 case-or-space-carve-out

PUSH-REVIEW

Range: cbe08f9..2677c56
- 2677c56 Exempt case-only and whitespace-only diffs from gates a and s

Files read: the full diff of 2677c56 (`git show 2677c56`), `guardrails/case_or_space_only.py` in
full (the new file), `guardrails/check-prover-record.sh` (the stand-down marker convention at lines
43-56, the base ladder at 101-116, the inbox-deposit arm at 118-129, the new case-or-space arm, and
the recordless arm at 165-193), `guardrails/check-skill-review.sh` (the base ladder at 53-63 and the
per-file substance scan at 72-101), `guardrails/check-deletion-only-push.sh` and the pre-push block
that calls it (the prior art for a stand-down), `spec/guardrails-freshness.md` (R226 criterion 6 and
R242 in full), `PRODUCT_SPEC.index.md` (the INV-208 row), `tests/test_deletion_only_push.py` (the
EXCEPTION_MECHANISMS map and the marker bijection it holds), `tests/test_skill_review.py` and
`tests/test_guardrails.py` (the carve-out tests, old and new), `guardrails/gates-manifest.json` and
`.github/workflows/gates.yml` (the gate a and gate s law lines, to confirm neither needed to move).

Checks run: eight, listed below — an independent adversarial read of the change by a reviewer who
did not write it, ten hand-built repository probes against the carve-out's boundary, five pytest
runs, six guardrail scripts run directly, and both push gates run against this very commit.

- The adversarial read was delegated to a separate worker, briefed to break the change rather than
  confirm it, and given the diff without the reasoning behind it. It was pointed at ten specific
  attacks — rename, delete, add, word-joining, case changes in case-sensitive positions, binaries,
  non-UTF-8 encodings, a mixed cosmetic-and-real diff, an empty diff, a multi-commit range with the
  cosmetic change last, symlinks, and mode changes — and told to build each one in a throwaway
  repository and run the real script against it, not to reason about it. It found five things.
  Three were real holes and are fixed in this commit; one is this record's own reason to exist; one
  is a pre-existing defect this change did not introduce and does not fix. All five are below.

- FOUND, FIXED: a bare `chmod +x` stood down as cosmetic. The first draft compared blob text only,
  so a file made executable with byte-identical content read as "nothing changed but whitespace".
  Reproduced against the real gate, not just the judge. Fixed by reading `git diff --raw`, which
  carries both sides' modes, and refusing any entry whose mode moved.

- FOUND, FIXED: a symlink whose target was re-cased stood down as cosmetic. A symlink's blob holds
  its target path as text, so `TARGET` becoming `target` normalized identical — a different path on
  a case-sensitive filesystem. Fixed by judging only regular-file modes (100644, 100755); a symlink
  (120000) or a submodule link (160000) now stops the carve-out cold.

- FOUND, FIXED: joining two words stood down as cosmetic. The first draft stripped whitespace to
  nothing, so `call foo bar now` becoming `call foobar now` normalized identical. It is literally a
  whitespace deletion, but it changes the words a reader reads. Fixed by collapsing whitespace runs
  to a single space instead of removing them; re-wrapping and re-indenting still stand down, and a
  test now holds that side of the line so the narrowing cannot be widened back by accident.

- FOUND, NOT FIXED, NOT BLOCKING — a defect this change inherited rather than caused. Gate s has no
  guard against its own HEAD~1 last-resort base. Where neither CI's explicit base nor `origin/main`
  resolves, the range collapses to the final commit; a cosmetic commit laid on top of an unreviewed
  substantive skill change then hides it, and gate s passes. The reviewer confirmed by construction
  that the SAME hole works through the pre-existing version-stamp carve-out, which has been in that
  script since 2026-07-17 — so this is not a hole the case-or-space carve-out opened. Gate a does
  carry the guard, and this commit's arm sits behind it. Recorded rather than fixed: the mandate
  puts the removal of this whole gate family in Package 5, and repairing a construct already
  scheduled for demolition is the kind of work this rebuild exists to stop. It is written into the
  handover as an input to Package 5.

- FOUND, CLOSED BY THIS RECORD: at the time of the adversarial read, this commit reddened gate a
  against itself. It edits `spec/guardrails-freshness.md`, which is part of the assembled spec, so
  gate a demanded a fresh prover record — and the change does not qualify for its own carve-out,
  since it is an ordinary content edit. This record is that record. Verified by running the gate:
  before this file existed, `bash guardrails/check-prover-record.sh --push` printed "the newest
  committed prover record predates the last PRODUCT_SPEC.md change" and exited 1.

- CLEAN on ten further probes, each built and run rather than reasoned about: `git mv` without a
  content change, whole-file deletion, new-file addition, a binary with invalid UTF-8, a latin-1
  file, a diff carrying one cosmetic file beside one real edit, an empty commit, a multi-commit
  range with the real change early and the cosmetic change last, and gate a's refusal to apply the
  carve-out against a HEAD~1 last-resort base — that last one being a claim the commit message
  makes, checked rather than trusted. None stood down. The renumbering of R242's criterion 4 to 5
  was grepped repository-wide for stale references: none live; the only hits are a prover record
  from 2026-08-05 describing the prior state and frozen archival copies under `prototype/`.

- pytest, at this commit: `tests/test_deletion_only_push.py tests/test_skill_review.py
  tests/test_push_review.py` — 63 passed in 17.96s. `tests/test_gates_manifest.py
  tests/test_every_gate_can_fail.py tests/test_requirement_shape.py` — 44 passed in 1.29s.
  `tests/test_guardrails.py -k "record or carve or case or space or inbox or prover or symlink or
  mode or chmod"` — 1 failed, 14 passed, 74 deselected in 4.79s. The one failure is
  `TestGateA_ProverRecord::test_real_repo_passes`, which fails for exactly the reason the arm above
  names: the real repository had no prover record covering this commit at the moment of the run.
  This file's own commit is what turns it green, so the run proving that necessarily happens after
  this text is written; it is reported in the handover rather than claimed here.

- guardrail scripts run directly, all exit 0: `check-tree-counts.py` (the published counts still
  match the tree after a new file landed in guardrails/), `check-gates-manifest.py`,
  `check-ci-mirror.sh`, `check-every-gate-can-fail.py` (gate a and gate s keep their known-red
  proofs; the new arm does not disarm them), `check-named-checks.py`, `check-doc-findings-bound.py`
  (188 live documents, 28 held at zero, none above its record). `check-index-generated.py` was run
  by the reviewer with its required arguments: 393 of 393 codes matched, and a fresh
  `scripts/build-index.py` build was byte-identical to the committed `PRODUCT_SPEC.index.md`.

- Both push gates, run against this commit: gate s stands down correctly and by name — this push
  changes no skill body at all. Gate a is the gate this record answers.

- NOT RUN: the full local suite. It kills itself in this environment (handover Finding 3), and the
  attempt to run `tests/test_guardrails.py` whole stalled past its ten-minute bound and, when
  stopped, left the working tree stashed — a trap now written into the handover as Finding 5. CI
  runs the full 2556-test set on every push and is the authority for that claim; this session did
  not independently reproduce it, and does not claim to have.

Findings: five, listed above with their evidence. Three were real holes in the first draft of the
carve-out and are fixed in this commit, each by making the carve-out narrower — the change now
exempts strictly less than it did when the reviewer opened it. One finding is a pre-existing defect
in gate s that this change inherited without widening, recorded and deliberately left for Package 5.
One is this record's own reason to exist. Nothing was found against the change as it now stands.

The judgment this record carries beyond the machine's reach: the carve-out's boundary is drawn at
what a reader reads, not at what a diff costs. That is the line the three narrowings defend, and it
is the line that must hold if this exception is not to become the "small diff" allowance the mandate
warns against. A future arm that exempts a change because it is short, or because it only touches
documentation, is not this exception grown — it is a different exception, and it owes its own case.

Blocking: none.
