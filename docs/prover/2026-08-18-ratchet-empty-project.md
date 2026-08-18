# Prover record — 2026-08-18 ratchet-empty-project

PUSH-REVIEW

Range: 1a98b97c..266e7e7c
- 266e7e7c The record carries the ratchet's clean refusal
- abbb737 adopt/install-ratchet.sh: refuse cleanly when a gated doc doesn't exist yet
Files read: adopt/install-ratchet.sh, adopt/install-scaffold.sh, guardrails.config.json, tests/test_ratchet_kit.py
Findings: a rehearsal of tonight's walk caught this on its first minute, and today's repository identity was overwritten by a test fixture — both are set out below
Blocking: none

The ratchet refuses a fresh project cleanly instead of crashing.

Root: a rehearsal of tonight's stranger walk installed the product into an empty folder,
exactly the way the walk starts, and `adopt/install-ratchet.sh` answered with a raw Python
traceback. The chain: `install-scaffold.sh` seeds `guardrails.config.json` with
`spec_path: PRODUCT_SPEC.md` before that file exists; the ratchet resolved the path,
vendored eight files, then ran the spec lints against the missing document; their
`FileNotFoundError` traceback was captured as if it were output and handed to `json.loads`,
which raised `JSONDecodeError` at the terminal and left the tree half-vendored.

What happened: an existence check now stands immediately after the document is resolved,
before anything is vendored. A missing document is a normal state of a fresh project, not a
breakage, so the script says so in one line in the shape it already uses elsewhere —
`{"severity":"error","code":"ratchet-install",...}` — and exits 1 with nothing vendored.
Behaviour on a project whose document exists is unchanged.

Checks run: `tests/test_ratchet_kit.py` — 19 passed, including three new cases in
`TestRatchetMissingDoc`. The new cases were run against the pre-fix script first and are red
there, so they catch the defect rather than describe the repair. Two neighbouring ratchet
test files were spot-checked, 15 passed, unaffected. The working copy was checked after
every run: no fabricated commits, no missing files.

Findings:
- The rehearsal earned its keep. This crash sits on the first minute of the stranger walk,
  and it would have surfaced in front of the owner tonight rather than here.
- Today's polluter had a fourth face, found while preparing this package: with git's own
  environment inherited, a fixture's `git config user.email` wrote into the real repository,
  so this repository's identity became `gate <gate@example.com>` and five commits pushed to
  main today carry that name instead of the owner's. The local setting is removed and the
  repository reads the owner's identity again; this commit's authorship was reset before the
  push. The five already on main are left as they are, because rewriting shared history costs
  more than the mis-attribution does — but the fact is recorded here rather than left for
  someone to puzzle over later. The environment repair that shipped this morning closes the
  road; no fixture identity has appeared since.

Blocking:
- none.
