---
name: text-audit-pack
description: 'Pack-side bindings for the external text-audit skill inside the live-spec pack. It carries what the audit body no longer does: the pack''s own mechanical lints (declared in .text-audit/lints.json), the reading-record home, and what a cheap reader means run inside this pack. Load it whenever text-audit runs inside a live-spec project. It audits nothing itself.'
metadata:
  version: 5.0.0
  requires: text-audit >= 1.0.0 (github.com/happysasha18/text-audit)
---

# text-audit — pack bindings

text-audit is an external skill with its own repository and version line. This page binds it to the
live-spec pack. An audit run inside a live-spec project reads the audit skill's own SKILL.md first and
this page beside it. An audit run anywhere else needs nothing from this page.

## Work that belongs elsewhere

This page binds the external text-audit skill to the pack; it runs no cold read and fixes no line
itself. Skip it for:

- reading a text as a stranger and fixing what a reader stops on, round by round — that is the
  external `text-audit` skill's own body, loaded first, not this page;
- judging whether a spec or architecture document holds together as written — the `product-prover`
  pass;
- judging the design behind a proven spec — the `design-reviewer` pass.

This page alone cannot run the audit loop: without the external skill's own SKILL.md loaded beside
it, its lint table names commands but starts none, and its "cheap reader" definition has no loop to
apply to. Load both together, the external body first.

## The mechanical lints this pack declares

`text-audit`'s Step 1 runs every command a host names in `.text-audit/lints.json` before it falls back
to its own bundled grep. This pack's copy, at the repository root, names the six scripts that carried
these classes when the audit body still lived here:

| Script | Class it catches | Surface |
| ------ | ----------------- | ------- |
| `guardrails/check-vocabulary.py` | a term used with no definition at first use | spec body |
| `guardrails/check-weak-words.py` | a weak relational word with an unfilled slot | spec body |
| `guardrails/check-requirement-shape.py` | a spec section missing the requirements genre | spec body |
| `scripts/spec-style-lint.py` | style and register, spec-body word cap | spec body |
| `scripts/preshow-register-lint.py` | style and register, any human-facing surface | any |
| `guardrails/check-one-name.py` | one thing answering to two names | any |

`guardrails/check-language-rules.py` is this pack's own gate over `guardrails/language-rules.json` and
the pages generated from it, a separate document from the six above. It takes no audited-file argument
and reports nothing about a text under audit. Before the 2026-08-18 extraction it also held two of
text-audit's own reference pages to a generated-drift test. That arm is retired (see "Where the rule
home moved," below), and this gate now checks only this pack's own documents.

## Pack paths

- the reading record home — `docs/language-reads/`, one dated file per reading, matching the record
  shape `docs/language-defects.md` and `docs/language-rule-coverage.md` already describe;
- the comprehension gate that calls this loop — `spec-author`'s "The comprehension gate" section,
  which names text-audit by skill reference and names no path;
- `docs/language-defects.md` — this pack's own record of why each language rule says what it says,
  written before text-audit existed as a general-purpose skill; it still cites text-audit's reading
  loop as evidence, and a reader following that citation now leaves the pack.

## Where the rule home moved

Before the extraction, `guardrails/language-rules.json` was the one editable home for the human-prose
rules. `scripts/gen-language-consumers.py` built text-audit's `references/reader-prompt.md` and
`references/human-prose-rules.md` off it on every run. Both files now ship as a static, hand-kept
snapshot inside the external skill's own repository, frozen as of 2026-08-18. A rule added to
`guardrails/language-rules.json` after that date still reaches this pack's own writer's and
maintainer's pages (`docs/language-rules.md`, `docs/language-rule-coverage.md`) and the model judge's
law bodies (`hooks/language-laws.json`). It no longer reaches the audit skill's bundled rule sheet. A
project that wants the fuller, moving rule set points its own `.text-audit/lints.json` at a script
reading this pack's rule home directly. None does yet, so the bundled snapshot is what a text-audit
run inside this pack holds a text to today.

## What a cheap reader means run inside this pack

A **reading round**, as text-audit's own body defines it, is one pass by each of its two readers, and
both readers of a round are cheap readers. Run inside this pack, that definition takes one more line.
The owner's word on 2026-08-18 settles it, following rule 74ef247, which first split a round into one
strong and one cheap reader: **a cheap reader is a reader with none of this pack's own skills or rules
loaded** — no `live-spec-base`, no working skill, no base rule, nothing this pack would hand a worker
starting ordinary pipeline work. A fresh session still carrying this pack's skills or rules is not
cheap by this pack's own accounting, whatever budget tier ran it. A reading run under one does not
count toward the two clean rounds this pack's comprehension gate closes on.

## Version discipline

`scripts/install-external-skills.sh` is single-skill today and does not yet install text-audit. A
checkout under `skills/text-audit/` (gitignored, matching `skills/product-prover/`) is manual until
that installer grows a second target. Once it does, the same discipline as product-prover-pack applies:
the installer refuses a version below the minimum in this page's metadata, and the installed copy is
never tracked by this repository. The external repository is its only source of truth, and raising the
minimum here is a pack change that lands as one.
