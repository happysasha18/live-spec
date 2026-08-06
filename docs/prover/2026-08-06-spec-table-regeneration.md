# Prover check — the spec's embedded table catches up, 2026-08-06 10:12

Independent check of commit `10f450d` to `PRODUCT_SPEC.md`. This record is written by a seat that
did not make the edit (SPEC INV-237). Claim to verify: the commit changed only the generated
code-to-location table under the `## Reference` heading. No requirement, criterion, or prose
sentence moved.

## Method

Read `git show 10f450d -- PRODUCT_SPEC.md` whole. Located the `## Reference` heading with
`grep -n "^## Reference" PRODUCT_SPEC.md`. Checked every changed hunk's line number against it.
Read the sentence above the table and `scripts/build-index.py`'s own header, to confirm the table
is declared generated output. Ran `guardrails/check-index-generated.py` against the committed
file. Diffed the file's span above `## Reference`, before the commit against after. Traced the
criterion split the commit catches up to, reading the three commits around it in full.

## What was checked

- The full diff of `10f450d` against `PRODUCT_SPEC.md`: 11 hunks, 22 changed lines.
- The `## Reference` heading and the sentence introducing the table.
- `scripts/build-index.py`'s module docstring.
- The gate `guardrails/check-index-generated.py`, run against `PRODUCT_SPEC.md` and
  `PRODUCT_SPEC.index.md`.
- The file's full span from line 1 through `## Reference`, at both `10f450d^` and `10f450d`.
- Commit `b3373ac`. It split Requirement 220 criterion 8 into new criteria 8 and 9. The old
  criterion 9 became criterion 10.
- Commit `cb9f062`. It rebuilt `PRODUCT_SPEC.index.md` off that split.

## Findings

None. Every check below matches the claim.

| # | Claim element | Check run | Result |
|---|---|---|---|
| 1 | Every changed line sits under `## Reference` | `## Reference` stands at line 7476; the diff's 11 hunks all open at line 7575 or later | holds |
| 2 | Every changed line is a table row | each of the 22 changed lines reads `\| CODE \| locations \|`, naming an `INV-` or `T-` code and its location list | holds |
| 3 | No requirement, criterion, or prose sentence moved | no hunk touches a requirement heading, a criterion sentence, or a Context paragraph | holds |
| 4 | The table is generated output | the sentence above the table names `scripts/build-index.py` as its builder; the script's own header calls itself the builder and says the table carries locations only | holds |
| 5 | The committed table matches a fresh build | `check-index-generated.py` exits 0 | holds |
| 6 | The body above `## Reference` is untouched | `diff` of that span, before vs. after, produced no output | holds |

**Check 5, the gate's own line:**

    check-index-generated: OK — reach: files=[PRODUCT_SPEC.md, PRODUCT_SPEC.index.md]; matched 388
    of 388 rows scanned; committed index equals the fresh build; 388 codes agree body-to-table

Exit code 0.

**Check 6, the command run:**

    diff <(git show 10f450d^:PRODUCT_SPEC.md | sed -n '1,/^## Reference/p') \
         <(sed -n '1,/^## Reference/p' PRODUCT_SPEC.md)

Output: empty. Exit code 0.

## What the change corrects

Commit `b3373ac`, twenty-nine minutes before `10f450d`, split Requirement 220's criterion 8. The
old criterion 8 was one sentence. It named four protections: a fresh clean-context agent for an
adversarial review, a cold reading, a release re-prove, and a deep audit. Its codes were
`[INV-40, INV-46]`.

The rewrite kept criterion 8 as the rung-scope clause alone. It moved the four-protections clause
into a new criterion 9. The old criterion 9, the economy-purchase clause, became criterion 10.

That renumbering changed which codes several rows carry. `INV-40` drops `R220.9` and gains
`R220.10`. `INV-46`, `INV-145`, `INV-237`, and `INV-266` each gain the new `R220.9`. `INV-69` and
`T-19` drop `R220.9` and gain `R220.10`.

Ten minutes later, `cb9f062` rebuilt the standalone `PRODUCT_SPEC.index.md` off the split. Its
diff carries the same renumbering `10f450d` later applies inside `PRODUCT_SPEC.md`. `cb9f062` left
the spec's own embedded table alone. The standalone index reflected the split. The embedded table
still carried the pre-split numbering. The two disagreed until `10f450d` rebuilt the embedded
table to match.

## Verdict

Confirmed as claimed. `10f450d` changes only rows of the generated `## Reference` table, each in
the shape `| CODE | locations |`. Nothing above that heading moved. The gate
`check-index-generated.py` passes on the committed result.

The change corrects a stale embedded table. `b3373ac` split Requirement 220 criterion 8 into
criteria 8 and 9, and renumbered the old criterion 9 to criterion 10. `cb9f062` rebuilt the
standalone index off that split. It left the copy inside `PRODUCT_SPEC.md` behind. `10f450d`
closes that gap.

## Reach

Files read directly:

- `PRODUCT_SPEC.md` — the `10f450d` diff; the `## Reference` heading and its introducing sentence;
  the full span through that heading, at two commits.
- `PRODUCT_SPEC.index.md` — as the gate's second input.
- `scripts/build-index.py` — module docstring.
- `guardrails/check-index-generated.py` — run; its output is pasted above.

Commits read whole: `10f450d`, `b3373ac`, `cb9f062`.

Read for form and precedent: `docs/prover/2026-08-05-pin-repoint-check.md`.
