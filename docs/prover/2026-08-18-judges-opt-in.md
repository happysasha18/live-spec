# Prover record — 2026-08-18 judges-opt-in

PUSH-REVIEW

Range: dc9340a0..175a3c7d
- f092fa5 The review record carries both passes
- d432fca The dedup keeps the mechanism and names the personal profile
- fa799b8 The skill-creator review of the communicator
- f7ccd80 The published skill-line counts follow the bodies the dedup shortened
- 99050f5 Dedup surviving chat-law paraphrases into pointers
- ae4e760 Merge origin/main into morning/2026-08-18-judges
- c525a59 The spec carries no dates, and the last read's findings close
- 02e4770 The front door stops promising wiring the installer no longer does
- 624bd4b The second read's blockers are answered
- bd78d98 The reviews' findings are repaired
- 3a9915b The tests prove the opt-in wiring, and the declaration keeps each surface
- 1e7119f Two local overrides go, since the copies they excused are identical again
- 9e43c3e The spec, the architecture and the journal say six judges are opt-in
- 6c91f2a The declaration and the installers carry six judges as opt-in
- f294b14 The rules drop the Stop arm their judge no longer carries
Files read: guardrails/judge-hooks.json, guardrails/language-rules.json, guardrails/local-overrides.json, hooks/language-laws.json, scripts/install-pack-hooks.sh, scripts/install-session-hooks.sh, PRODUCT_SPEC.md, ARCHITECTURE.md, README.md, adopt/ADOPT.md, skills/communicator/SKILL.md, skills/communicator/references/writing-register.md
Findings: the declaration promised wiring the installers no longer do, and the dedup this package was sized for turned out to be mostly already done — both are set out below
Blocking: none

Six judges become opt-in, and the paraphrases that survived the night become pointers.

Root: the declaration said six chat judges were wired into the host's settings, and the
installers no longer wire them. A host reading the front door was told the pack arms
itself. It does not: the files ship, and a host that wants one adds its command by hand.
Separately, the seven chat laws were retold in several places at once, so a reader could
meet a law's text in a skill body and never learn which page owns it.

What happened: `guardrails/judge-hooks.json` moves the six from `wired` to `library` and
gains an opt-in surface map. Both installers say the same, and both stop implying they
arm anything. The spec gains requirement 311 with its closing criteria, and the
architecture and the journal follow. Two local overrides go, because the copies they
excused are identical again. The rules drop the Stop arm their judge no longer carries.
Four adversarial reviews ran over this package — PASS, FAIL, FAIL, PASS — and every
blocker they raised is closed: README and `adopt/ADOPT.md` promised wiring; requirement
294 handed its class to a judge that had itself become optional; requirement 298, whose
subject is this very installer, had been left unamended. Two tests that the change had
emptied were restored with mutation proofs rather than deleted.

The dedup is small and honestly so. Four paraphrases survived the night's plainer passes
— the calque item and the no-contrast-frame item in the communicator's body, rule 15
twice in its writing register, and R293's Context in the spec — and they become pointers
to the page that owns each law: −772 bytes. The rest of the dedup map did not survive
contact with the tree. Its line numbers were measured before the night rewrote those
skills, and most of its sites had already been cleared by that rewrite. One class was
refused outright by two workers independently: the `law_text` fields in
`guardrails/language-rules.json` are not a retelling of a law, they are the operational
prompt a live judge runs on, generated onward into `hooks/language-laws.json`. Folding
them into a pointer would have quietly disarmed the audit, so they stand untouched, as
does the personal profile that owns laws one and four and lives outside this repository.

The skill-creator review refused this package once, and the refusal earned its keep. It
found that the dedup had cut the mechanism of rule 15, not only its retelling, out of the
one section that promises a reader meets these rules without opening another file; and
that both new pointers said "profile.md" without saying which, when the law lives only in
the personal profile outside this repository and the in-repo file of that name carries no
such key. Both were repaired — the mechanism restored word for word, the pointers naming
the personal profile the way the rest of the pack names it — and the record
docs/skill-review/2026-08-18-communicator.md keeps the first REJECT with its findings
beside the second pass and its ALLOW. The communicator ends at 45,839 bytes against
45,985 before the dedup: a smaller saving than the cut that broke it.

Checks run: targeted suites across every touched area — 414 passed. `-k PinDrift`
returned 13 of 13 green in an isolated re-run; an earlier 12 of 13 was a flake from a
concurrent full suite (`printf: write error: Interrupted system call`). The register lint
and the spec style lint at full tier ran clean over the edited bodies. The working copy
was checked after every run: no fabricated commits, no missing files.

Findings:
- A declaration that describes machinery is not evidence of it. This one outlived the
  installers by weeks, and no gate compared the two — the reviews found it, not a check.
- The dedup was sized at −15.6 KB from a map, and delivered −772 bytes. The map was not
  wrong when written; it was measured against a tree that changed underneath it overnight.
  A map of byte savings is perishable, and quoting its total onward is how a plan acquires
  a number nobody can reproduce.
- Two independent workers refused the same instruction — to fold `law_text` into pointers
  — and both gave the same reason. An instruction that survives review by being refused
  twice is a design fault in the instruction, not diligence in the workers.

Blocking:
- none.
