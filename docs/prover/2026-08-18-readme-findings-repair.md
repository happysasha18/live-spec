# PUSH-REVIEW — README.md's findings count returns to its record

Date: 2026-08-18 09:36 local. Range: bcdbdbe..5f620c3 — the pushed range: 431138c
the prose rewrite, 5f620c3 this record.

Root: the README layering pass (commit 7c7931b, already on origin/main) rewrote
most of README.md's prose and pushed gate aa (`guardrails/check-doc-findings-bound.py`)
red: the live tree read 23 findings against the file's recorded 4 in
`guardrails/rule-census.json` — 20 sentences over the 25-word cap (rule r08) plus 3
`scripts/spec-style-lint.py --tier full` hits (one caps-shout on "AI", two
contrast-frame "scissors" constructions the rewrite introduced by accident). The
owner's direction was to repair the prose itself, judged by the communicator
skill's writing-register rules (one idea per sentence, one point per paragraph, no
filler, no contrast frame), and to treat the word-count gate as a proxy check
afterward, not the target.

Files read: README.md (every sentence the census and the style lint flagged, in
full, before and after); `guardrails/rule-census.json`'s recorded entry for
README.md; `skills/communicator/references/writing-register.md` (the house rule
this rewrite was held to).

Checks run:
- `python3 scripts/rule-census.py README.md` — before: `long 20, style 3,
  register 0, total 23`. After: `long 4, style 0, register 0, total 4`, matching
  the recorded entry (`long 4, style 0, register 0, total 4`) exactly. The four
  remaining long sentences are the pre-existing baseline (the intro's pipeline
  sentence, the requirement context/user-story/acceptance-criteria line, the
  105-word skills roster, the prior-art credit line) — none introduced by this
  repair, none touched by it.
- `python3 guardrails/check-doc-findings-bound.py` — OK, 146 live documents, 26
  held at zero, none above its record.
- `python3 scripts/spec-style-lint.py --tier full README.md` — OK, no register
  tells found (0 errors, 0 warnings).
- `python3 scripts/preshow-register-lint.py README.md` — OK, no coined metaphor,
  calque, or transliterated pack term found.
- `python3 guardrails/check-tree-counts.py --allow-uncommitted` — OK, matched 3
  of 3 rows (gate-roster, scaffold-checks, skills-lines).
- the host-count regex (`test_host_count_agrees.py`'s own pattern) and the four
  `SURFACES.md` needles — read directly against the file, all still present and
  unmoved from where the layering pass put them.
- `python3 -m pytest -q tests/test_readme_stance.py tests/test_host_count_agrees.py
  tests/test_no_self_certification.py tests/test_published_counts.py
  tests/test_preshow_register_lint.py tests/test_setup_entry.py
  tests/test_scaffold_guardrails.py tests/test_scaffold_install.py
  tests/test_skill_count_agrees.py tests/test_traceability.py::TestPackListParity
  tests/test_doc_findings_bound.py` — 138 passed. One teardown-only error
  (`suite_leaves_no_trace`, a leaked temp file named `row241-host-*`) is a
  cross-process /tmp collision from another concurrent agent's run on this
  shared machine, not from this file or this test; `test_the_real_repository_passes`
  itself passed before that fixture ran.

Findings: none beyond the root above. The regression was mechanical (the layering
pass's new prose ran long and, twice, into the contrast frame the style lint
bans) rather than a wrong record published by hand; the record in
`guardrails/rule-census.json` is untouched by this commit.

Blocking:
- none.
