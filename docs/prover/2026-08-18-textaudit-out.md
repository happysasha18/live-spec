# Prover record — 2026-08-18 textaudit-out

PUSH-REVIEW

Range: 63cfa511..RANGE9
- 9f11c3a3 The record carries the skill's move to its own home
- aa923a0a The record names the repairs the gates asked for
- f1caf3b8 The record names the review's second pass
- 79da8a34 The record names the ceilings this push removes
- 8b337fd5 The record names the installer fix this push carries
- d919396b guardrails/install.sh resolves the hooks dir with git rev-parse
- 2e2f167 Every invented ceiling goes, and the watcher that enforced them
- 412ef72 The adapter's review carries its second pass
- 02f63e4 Reviews and pins follow the extraction, and two long sentences come down
- 80e7f07 The architecture pin and the adapter's own section follow the skill out
- fe49396 Merge origin/main: the stale usage pin lands under the extraction
- dc42c6f Merge lane/2026-08-18-textaudit-out: text-audit moves to its own repository
- 34f02ab text-audit moves to its own repository; a thin adapter and the pack's lint contract stay
Files read: skills/text-audit/, skills/text-audit-pack/SKILL.md, scripts/gen-language-consumers.py, guardrails/check-language-rules.py, scripts/check-registry.json, OVERVIEW.md, README.md, PRODUCT_SPEC.md, tests/test_traceability.py
Findings: the home was generating part of the skill it was about to hand over, and the extraction's own trimming stopped short of its target on purpose — both are set out below
Blocking: none

The text-audit skill leaves home, and a thin adapter stays in its place.

Root: text-audit had grown into the pack it lives in. It was the largest skill body at
30,895 bytes, and it reached back into the home for things a standalone repository would
not have. The owner's word to give it its own home was already given; what was missing was
the unpicking.

What happened: thirteen seams were cut. The deepest was not on anyone's list — 
`scripts/gen-language-consumers.py` was *generating* part of the skill from
`guardrails/language-rules.json`: its reader prompt, and a block spliced into its prose
rules. Removing the skill without cutting that link would have hard-failed
`check-language-rules.py`, and no classification had noticed it, because a file that is
generated looks exactly like a file that is written. The generation link is cut, the gate
and the check registry follow it, the mechanical-lints contract now lives at
`.text-audit/lints.json`, the pack rosters across eight files agree again, and the working
skill floor drops from nine to eight with the reason written down.

What stays home is an adapter, `skills/text-audit-pack/SKILL.md` at 5,263 bytes, built on
the pattern the prover pack already uses. The body of the skill and its tools are staged
for the new repository outside this tree; the repository itself is the owner's to create,
and nothing was published outward here. The same package carries the line the owner asked
for on 18.08: a cheap reader is a reader with none of this pack's own skills or rules
loaded.

The merge onto today's main met one conflict of substance: this package removes
`tests/test_text_audit_fixtures.py`, and main had just repaired a stale pin inside it. The
removal stands, and nothing is lost — the copy travelling to the new home had already
dropped that pin on purpose, because it named this repository's index builder and the skill
now runs on any project.

Checks run: `tests/test_traceability.py`, `tests/test_language_rules.py`,
`tests/test_check_registry.py` — 224 passed; the pack-roster parity tests — 3 passed;
`tests/test_traceability.py` and `tests/test_check_registry.py` again after the merge — 198
passed. Gates run by hand and green: doc findings bound, named checks, language rules,
index generated, freeze, and the style lint over the new adapter. The working copy was
checked after every run: no fabricated commits, no missing files.

Findings:
- A home that generates part of a skill cannot hand that skill over, and nobody knew.
  Twelve seams were on the reviewer's list; the thirteenth was found only by trying to
  leave. A dependency you can read is easy to name — one that writes the file for you is
  invisible until the file has to stand alone.
- The body came down to 16,048 bytes against a target of about 11,000. The worker stopped
  when further cuts began removing substance and wrote the gap down rather than hitting the
  number. A target missed with a reason is worth more than a number met by deleting
  meaning.
- Not closed, and named rather than left quiet: the external-skill installer still takes one
  skill at a time, CI is not extended to fetch text-audit, the real repository does not
  exist yet, and a few prose mentions of the old path remain where no gate reads them.

Blocking:
- none.
