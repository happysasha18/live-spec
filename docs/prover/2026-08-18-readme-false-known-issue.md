# PUSH-REVIEW — a false Known Issue leaves README, and gate h goes green

Date: 2026-08-18 late morning. Range: 6152169..HEAD (one content commit + this record).
Root: server run on 6152169 failed gate h (the four host checks): the completeness
check read a surface id "..." out of README's own rendered text and demanded a
registry row for it.

What happened: the layering pass had added a "caught late" Known Issue claiming this
repository's `surface_discovery_pattern` is a dead scaffold placeholder that matches
nothing. Both halves are false. The pattern was deliberately ARMED on 2026-07-11
after a real planted-surface incident, and `tests/test_four_checks_contract.py::
test_own_attach_arms_the_discovery_pattern` locks it set and catching. And the
paragraph's own literal example `<section id="...">` is exactly what the armed
pattern matches — the disclosure triggered the very check it declared inert.

The repair removes the false paragraph (481 bytes). The config is untouched — it is
law-armed and correct. Nothing else in README moves.

Checks run: `scaffold/guardrails/check_completeness.py` — OK, 4 registered surfaces,
nothing unregistered (this is the exact check the server failed);
`check-doc-findings-bound.py` — exit 0; `preshow-register-lint.py README.md` —
exit 0; the contract test's pattern assertion unaffected (config not touched).

Findings: the "hostile disclosure" class needs care — a Known Issue that quotes a
machine-readable literal can arm the machine it describes. Recorded here as a
lesson, not a rule.

Blocking:
- none.
