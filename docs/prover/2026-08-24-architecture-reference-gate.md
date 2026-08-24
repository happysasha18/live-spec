# Prover record — 2026-08-24 architecture-reference-gate

PUSH-REVIEW

Range: 004578c4..b3100e8f
- b3100e8f Add the architecture-reference gate: gate z

Files read: the full diff (`git show b3100e8f --stat`, 14 files); `guardrails/archformat.py` in full
(the shared reader the builder and gate both go through — `owns` is the only field `anchors`/
`anchors_expanded` read, `pins` is never read for anchors, confirmed at its own lines 89–101);
`scripts/build-matrix-reference.py` and `guardrails/check-matrix-reference.py` in full, as the sibling
being copied; `tests/test_matrix_reference.py` and `tests/test_build_index.py` in full, as the test-shape
precedent; `docs/test-matrix-format.md` (the "generated Reference" section, to confirm the separate-file
committed-index pattern this delivery follows is the one already live, not an invention); `PRODUCT_SPEC.md`
and `ARCHITECTURE.md` at every line this delta touches, plus the `guardrails` node's full `owns`/`pins`
lists around the edit to confirm placement; `spec/doc-order-generated.md` in full (its Parts map row,
R283–R291 for style, R284 and R289 as the direct siblings R312 combines); `guardrails/pre-push` and
`.github/workflows/gates.yml` in full, to confirm gate z is the only new letter and nothing else moved;
`guardrails/README.md` in full, including the "Notes on some of the gates" section (confirmed gates x
and y — the two immediate un-noted precedents — carry no individual note either, so gate z following
that same precedent is not an omission); `tests/conftest.py` in full (see F1 below); `matrix/guardrails.md`
around M-449 and the Parts map row in `TEST_MATRIX.md`.

Checks run: `python3 -m pytest tests/test_architecture_reference.py tests/test_build_index.py
tests/test_index_generated.py tests/test_matrix_reference.py tests/test_formal_index.py
tests/test_spec_parts.py tests/test_traceability.py tests/test_guardrails_unit.py
tests/test_architecture_format.py tests/test_delta_classifier.py -q` — 315 passed, 1 skipped (the skip is
pre-existing and unrelated: `test_spec_parts.py:64`, a before-the-parts-move byte-identity check the
current parts-map shape no longer applies to). `python3 guardrails/check-architecture-reference.py
ARCHITECTURE.md ARCHITECTURE.index.md` — exit 0, reach `matched 23 of 23 rows scanned; committed Reference
equals the fresh build; 401 anchors agree node-to-table`. `python3 guardrails/check-matrix-reference.py
TEST_MATRIX.md ... TEST_MATRIX.index.md` and `python3 guardrails/check-index-generated.py PRODUCT_SPEC.md
PRODUCT_SPEC.index.md` — both still exit 0 after the rebuild this delta triggered. `python3
guardrails/check-pin-drift.sh` — exit 0, 181 pins checked, the new `check-architecture-reference.py:1` pin
proved by the file's existence (unlabelled `:1` form is `guardrails/check-matrix-reference.py:1`'s own
shape, so the sibling pin follows the same proof path). `python3 guardrails/check-requirement-shape.py`,
`check-vocabulary.py`, `check-one-name.py`, `check-weak-words.py`, `check-no-history.py`, all against
`PRODUCT_SPEC.md` — all five exit 0 (1749 criteria well-shaped, glossary closed with the two new entries
used and no dead entry, no alias collision, no unfilled weak word, no history marker). `bash -n
guardrails/pre-push` — clean. `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/gates.yml'))"`
— clean. `grep -cE '^\| M-[0-9]+ \|' matrix/guardrails.md` — 123, matching the Parts map row this delta
edited from 122 to 123.

Findings: two, both notes — no blocking defect.

**F1 — `tests/conftest.py`'s spec/matrix "read as one document" synthesis has no architecture sibling; not
a defect today, worth a name for whoever adds the architecture's second generated table.**
`tests/conftest.py:113-119`'s `read()` special-cases `SPEC` and `MATRIX`, appending the committed
`PRODUCT_SPEC.index.md` / `TEST_MATRIX.index.md` under a synthesized `## Reference` heading so a caller
reading `read("PRODUCT_SPEC.md")` / `read("TEST_MATRIX.md")` sees the document as one whole, table
included, the way it read before the table moved to its own file. `read("ARCHITECTURE.md")` falls through
to the generic branch (a plain `open().read()`) and returns the node sections alone, with no
`ARCHITECTURE.index.md` synthesis. This is not a defect against anything this delta needs: no test reads
the architecture expecting its Reference table inline (`test_architecture_format.py::_nodes()` calls
`archformat.parse_nodes(_read("ARCHITECTURE.md"))`, and parsing nodes needs no Reference tail — verified
green, 233 lines of that suite read in full). It is a structural asymmetry with the two siblings that a
later reader might trip on if a second architecture-generated table is ever added and a test wants "the
architecture as one document." Filed as a note rather than folded, since folding it here means writing
test-infrastructure code with no test that would fail without it — the shape this delivery's own
`tests/test_architecture_reference.py` avoids by testing the gate/builder against the real committed files
directly rather than through a synthesized read.

`recommendation · not-actioned (deferred, no test demands it)`

**F2 — the "reach" line's fixed wording says "rows scanned" for a count of nodes, matching the family's
existing shared-function shape rather than reading oddly on its own.** `guardrails/specformat.py`'s
`green_reach()` prints `"matched %d of %d rows scanned"` unconditionally; `check-index-generated.py`
already calls it over a count of spec CRITERIA (not literal rows) with the same fixed wording, so gate z's
`23 of 23 rows scanned` over a count of NODES is the same established, mildly generic phrasing every family
gate uses, not a fresh looseness this delta introduces. Confirmed by reading `check-index-generated.py`'s
own call site. No fix proposed — changing the shared function's wording would be an unrelated, wider
change affecting every gate in the family.

`note · not a finding`

Blocking: none

## What was verified beyond the checks above

Numbering: R312 was free in `PRODUCT_SPEC.md`'s Parts map and in every `spec/*.md`/`matrix/*.md` file
before this delta (`grep -roE "Requirement [0-9]+" spec/*.md PRODUCT_SPEC.md | sort -n | tail` topped out
at 311); INV-315 was free (`grep -roE "INV-[0-9]+" ... | sort -n | tail -3` topped out at 314); M-602 was
free (`grep -roE "M-[0-9]+" matrix/*.md TEST_MATRIX.md | sort -n | uniq | tail` topped out at 601). Gate
letter z was free and is now the 23rd letter, confirmed by counting `-- gate [a-z]{1,2}:` markers in
`guardrails/pre-push` before and after (22 -> 23) and cross-checking against `guardrails/README.md`'s own
roster, which now lists the same 23. Letters u/v/w are absent from both files (retired at commit e61b29b7,
"Remove the checks whose only subject was another check") and were not reused.

Placement: R312 was drafted once between R284 and R285 (the numerically-adjacent, thematically-identical
sibling) and then moved to the end of `spec/doc-order-generated.md`, after R291 — the file's own numbering
is non-contiguous by construction (R223-224, R244-250, R277-291, R297 already sit as disjoint blocks, each
one an appended-at-the-time delivery, not a resorted sequence), so appending at the file's end matches the
convention every prior block in this file already follows, and interleaving by number would have been the
one placement decision this record would need to defend.

INV-315's owns bullet was likewise moved once: drafted next to INV-273/274 (its nearest sibling by
subject) and then moved after INV-304, the list's actual last bullet — the guardrails node's owns list is
not numerically sorted (INV-301, INV-299, INV-305, INV-306, INV-304 appear in landing order, not ascending
order), so appending after the true last entry matches that list's own convention.

Glossary: two entries added ("architecture Reference", "architecture-reference gate"), mirroring the
matrix's "matrix Reference" / "matrix-reference gate" pair exactly, in their alphabetically-correct slot
(between "architecture node" and "artifact inventory"). Not explicitly requested by the task brief, but
added on the row-477-minor-gate precedent (`docs/prover/2026-07-23-row477-minor-gate.md` F1: a documentation
fan-out miss, there `guardrails/README.md`'s gate-d paragraph, is exactly the class of finding this record
would otherwise have had to file against itself). `check-vocabulary.py` confirms both are used and no dead
entry survives.

README fan-out (the named risk in the task brief, after row-477-minor-gate's F1 missed exactly this file
for gate d): `guardrails/README.md`'s gate count and roster line were both updated in this same delivery,
verified by the mechanical self-check the README itself documents
(`grep -oE -- '-- gate [a-z]{1,2}:' guardrails/pre-push | sort -u | wc -l` → 23, matching the stated count).

ARCHITECTURE.md's own Reference-table convention: confirmed via `docs/test-matrix-format.md` that the
matrix's generated Reference already lives in a separate committed file (`TEST_MATRIX.index.md`), not
spliced into the body — the same pattern `PRODUCT_SPEC.index.md` set for the spec. `ARCHITECTURE.index.md`
as a new, separate committed file (never spliced into `ARCHITECTURE.md`'s own body) follows that live
precedent rather than the more literal "then the generated tables" phrasing in R289.2's Context, which
predates any architecture-generated table existing at all and is not falsified by a separate-file
implementation — the matrix's identical R283.2 phrasing already coexists with `TEST_MATRIX.index.md` living
apart from `TEST_MATRIX.md`.

Skill-review gate (s): the diff touches no path under `skills/`; `guardrails/check-skill-review.sh`'s own
law (a review record is owed only when a file under `skills/` is substantively changed) means no record is
owed for this push, confirmed by reading the script's header and by `git diff --stat` showing no
`skills/*` path in this delta.

`tests/test_guardrails.py` was deliberately not run as a whole (it `git stash`es the working tree and does
not restore it on an interrupted run, per the task brief's own warning); its two gate-adjacent assertions
(`test_readme_ships`, `test_workflow_ships_and_mirrors_the_gates`, `test_readme_carries_the_mirror_guidance`)
were instead verified by direct inspection of the same needles the tests check for, all present.

Overall: the delivery lands the third generated-reference family member end to end — spec law, architecture
owns/pin, builder, gate, wiring, README, coverage row, rebuilt indices, and a red-proven test suite — with
no blocking finding.
