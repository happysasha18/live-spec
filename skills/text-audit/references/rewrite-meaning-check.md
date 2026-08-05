# Checking that a rewrite still instructs the same thing

This file belongs to the `text-audit` skill, whose body is [`../SKILL.md`](../SKILL.md). The body's
loop asks whether a stranger understands a text. This file asks a second question of a rewrite: does
the new text still tell its reader to do the same thing?

Run these steps over any rewrite of text that binds someone. A skill body, a guardrail's printed
message, a spec criterion, an installed file, and a step a reader follows all bind someone.

Why the steps exist: a rewrite of eleven skill files dropped phrases the test suite required. Nobody
read the old and the new version side by side. The audit loop in the skill body reads how the new
text lands on a stranger. It reports nothing about the eight fields in step 1.

Every path below is relative to the root of the live-spec repository, which is the directory holding
`PRODUCT_SPEC.md`, `guardrails/`, and `scripts/`. A path opening with `references/` names a file in
this skill's own directory, beside this one.

## Step 1 — put each changed unit beside the version it replaces

Take the rewrite one unit at a time. A unit is one criterion, one paragraph, or one list item. Put it
beside the text it replaces, and answer all eight questions. Write each answer on its own line.

| Field | The question to answer |
|---|---|
| Actor | Does the same person or the same part of the system act? |
| Force | Do must, should, may, and any prohibition carry the same weight? |
| Condition | Does the rule apply under the same trigger? |
| Scope | Does it bind the same text, system, people, and stretch of time? |
| Threshold | Are the quantities, units, direction, and comparison unchanged? |
| Exception | Does every carve-out and every fallback survive? |
| Output | Are the names, formats, destinations, and generated files unchanged? |
| Side effect | Does the same action change the same state? |

A change made on purpose gets its own line under the field it moved. Keep those lines apart from the
readability findings, so whoever reads the record can tell the two apart.

## Step 2 — resolve every path and run every command the text teaches

- Open every path, link, and file name the changed text carries, and confirm each one resolves.
- Run every command the text teaches, from the working directory the text names.
- Carry out each taught step in a temporary directory, and read what it produced.
- Run the suite from the repository root: `python3 -m pytest -q`.

The suite pins exact phrases out of these documents, so a dropped phrase turns a test red. When a test
fails on a phrase, say which of three kinds that phrase is:

- the phrase carries the rule, so the rewrite changed the rule and the rewrite goes back;
- the phrase names something another file depends on, so both move in one change;
- the phrase is incidental wording, and the test may take the new words.

A test takes new words only in the third case.

## Step 3 — edit the source of a generated file, then regenerate

Find the source and the generator before touching anything. `scripts/gen-language-consumers.py` builds
four files out of `guardrails/language-rules.json`:

- `docs/language-rules.md`;
- `docs/language-rule-coverage.md`;
- `hooks/language-laws.json`;
- [`references/reader-prompt.md`](reader-prompt.md), and the rule block inside
  [`references/human-prose-rules.md`](human-prose-rules.md).

A hand edit to any of them turns `python3 guardrails/check-language-rules.py` red. Edit the source, run
the generator, and compare every one of those files against a fresh build.

To read a fresh build without writing into the tree, send the generator to a scratch directory:

```bash
out_dir="$(mktemp -d)"
python3 scripts/gen-language-consumers.py --out-dir "$out_dir"
```

`PRODUCT_SPEC.index.md` is generated the same way, by `python3 scripts/build-index.py PRODUCT_SPEC.md
-o PRODUCT_SPEC.index.md`. Its gate is `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md
PRODUCT_SPEC.index.md`.

## Step 4 — install into a temporary home and compare

`install.sh` copies every directory under `skills/` into `$HOME/.claude/skills`. Point it at a
throwaway home, so a live copy on the machine stays untouched:

```bash
tmp_home="$(mktemp -d)"
HOME="$tmp_home" bash install.sh
diff -r skills/text-audit "$tmp_home/.claude/skills/text-audit"
```

The copy carries the reference files as well, so a reference the rewrite added shows up in the diff.

## Step 5 — report what a session pays to read the rewrite

Give the sizes separately, so whoever reads the report can see where the words went:

```bash
wc -c skills/text-audit/SKILL.md skills/text-audit/references/*.md
```

The frontmatter at the top of `SKILL.md` is indexed in every session. The body loads when the skill
loads. Each file under `references/` loads only for the task that needs it.

## Step 6 — hold the recorded finding count

`python3 scripts/rule-census.py` counts findings per file. It counts prose sentences past the 25-word
human-prose cap, plus the findings of `scripts/spec-style-lint.py`, plus the findings of
`scripts/preshow-register-lint.py`. `guardrails/rule-census.json` records the count each file is
allowed to carry.

`python3 guardrails/check-doc-findings-bound.py` refuses a push where a file stands above its recorded
count. A file recorded at zero reds on its first finding. A file the record has never heard of also
reds, so a new file is measured and recorded before it can pass.

## The texts that prove a step catches something

`evals/fixtures/text-audit/` holds three short texts, each carrying one known defect. The test
`tests/test_text_audit_fixtures.py` names the planted defect of each one, and it says which shipped
check reports that defect.

Hand `evals/fixtures/text-audit/rewrite-weakens-the-rule.md` to any worker that claims to verify a
rewrite. A worker that misses the changed actor, the softened force, or the dropped exception has
failed before it touches a real document.
