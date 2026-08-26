# Safe spec readability + compaction — the meaning-preserving protocol (2026-07-15)

The rewrite must not change what any rule REQUIRES. A sentence can read cleaner while quietly dropping a
condition, flipping a default, weakening a "never", narrowing a scope, or losing a boundary. Nice words, a
broken law. This protocol is the machine that catches that. Hardened by an independent Fable design pass
(2026-07-15) that found five holes in the first-cut plan and two nets missing entirely. It is the reusable
compaction machine every project runs; its mechanical parts wire into the push gate as the compaction gate.

## Phase 0 — Freeze and extract (before any rewrite)

- **0.1 Anchor OCCURRENCE map, not just the unique set.** A dropped trailing citation mid-paragraph passes
  a unique-set check yet loses the sentence's governing law — a meaning change. Freeze per-anchor
  occurrence counts AND per-section anchor sets. A per-anchor count decrease is legal only on a rewrite-log
  line naming the deleted duplicate restatement it came from.
- **0.2 Anchor regex covers the variants.** `[INV-28 kin]` (kinship, distinct from a governing citation) and range
  tokens `T-1..T-7` (the traceability suite's `expand()` depends on that exact syntax) are frozen as exact
  strings; normalizing `kin` to a bare citation converts an analogy into law, splitting a range breaks
  index extraction.
- **0.3 Structural marker lines are law, preserved verbatim.** `[target]` (its placement is itself a law, tied to an
  open row by S-0), `[default]` (the human's revisit handle, INV-31), and H3 heading tags
  (`[feature: F-x]` / `[not a scenario]`, INV-132) are frozen verbatim. Heading lines are never rewritten.
- **0.4 Freeze the literal classes** and diff after each section: numbers with units (lane cap, question
  cap, round cap, the legibility ratios and sizes); backticked paths and script
  names; closed vocabularies (bug/small/surface/large; landed/declined/superseded; the problem-ledger
  statuses; CONVERGES/WAITS/STANDS DOWN); quoted sentinels whose exact string is a legal value
  (INV-20's `"nothing left out" is valid`).
- **0.5 Check-phrases with LOCATION.** A phrase can survive in the index row while the prose clause drops
  the condition — test green, law gone from its home. Record each check-phrase's home clause; verify it
  survives in the SAME clause after rewrite, or the re-point log says why it moved.

## Phase 1 — Duplicate-site census (the redundancy is asymmetric)

Duplicated copies of one law DIFFER. INV-130's decision-page copy and its index copy each carry a condition
the other lacks. **The law is the union of the copies.** Before removing a restatement, union-diff its sites;
every condition present only in the doomed copy is moved into the survivor or logged as an intentional drop
with the owner's word. All sites of one anchor change in ONE commit — a reworded lone copy drops below the
redundancy detector's threshold and escapes while now disagreeing with its twin.

## Phase 2 — Index compaction runs LAST, after fact-relocation

Index rows have accreted requirement content the prose lacks: the T-18 row's `his 2026-07-06 word`
provenance lives nowhere else; the INV-139 row's homes enumeration is absent from its clause; the INV-141
row's `enumerated at the M-1 gate` is in a different section. Per row: (1) tokenize into atomic facts;
(2) find a prose sentence stating each at least as strongly; (3) a homeless fact is MOVED into the anchor's
home clause first, own commit; (4) only then shrink the row to a true one-liner; (5) the one-liner still
satisfies every `| INV-x |`-shaped test assertion and any check-phrase pinned inside index rows. Mega-rows
one at a time; the already-one-line band needs no change.

## Phase 3 — Rewrite order and unit

Meaning unit = one anchor clause (the paragraph ending in its trailing anchor). Edit/commit unit = one
section. Order: (1) low-anchor-density narrative first (calibrates the checker cheaply); (2) medium-density
rule sections; (3) the mega-clauses individually, one commit each, full ceremony; (4) the Formal index last
(Phase 2); (5) the header block, S-0, heading lines, marker lines: never rewritten. Full suite + anchor map
+ literal-class diff after each section commit. Suite green is necessary but never sufficient — most sentences
carry no phrase test.

## Phase 4 — The per-clause meaning-diff (extraction → entailment → reverse-entailment)

1. **Extract from OLD only** (checker has not seen NEW): atomic obligations, each tagged MODALITY
   (must/never/may/default) · ACTOR · ACTION · OBJECT · CONDITION · QUANTIFIER (each/every/only/at most N/
   exactly one) · EXCEPTION · TIMING · HOME/net.
2. **Per item, judge NEW:** entailed-exactly / weakened / strengthened / dropped / moved (with target).
   Strengthened is a flag too — a rewrite has no license to add law.
3. **Reverse pass:** extract obligations from NEW alone; any with no OLD counterpart is invented law. The
   direction side-by-side reads skip.
4. **Analogy-import check:** every load-bearing comparison ("the same as", "the way X does", "mirrors",
   "sibling of", "kin", "already has", "rides the same path") imports meaning from another clause; the
   checker receives the final text of every clause such a phrase cites.
5. **Canary per checker batch:** 2–3 planted broken rewrites (a dropped condition, a may↔must flip, a
   quantifier change); a run that misses any plant is INVALID and reruns. Batches ≤10 clauses per fresh
   context; two independent runs, union of flags.

## Phase 5 — The scissors/boundary rewrite rule

The test before turning "X, never Y" into a positive sentence: **is Y the complement of X?** Complement case
("picked by a graph, never by mood") → "picked only by the graph" carries the whole boundary; "only" does
the work "never" did. Non-complement case (the pen law: "one pen at a time" does NOT entail "foreign
sessions never share a pen") → the prohibition survives as its own plain sentence. The ban targets the
rhetorical contrast frame; the modal words never/no/only/exactly-one are load-bearing and always survive.

## Stop conditions — keep the original, park the section

1. Anchor unique-set delta, or an occurrence-count drop with no log line.
2. A checker verdict of weakened/dropped/strengthened "resolved" by argument alone, without restoring the
   condition or the owner's word.
3. A checker canary missed (halt everything — the checker is broken; the section is fine).
4. A red test "fixed" by editing the test phrase with no logged re-point naming the same law; and >~5
   re-points in one section means the phrasing itself is load-bearing — keep the original.
5. A clause whose obligations the checker cannot enumerate with confidence (the mega-clauses): fallback is
   sentence-internal simplification only — shorten sentences, keep every clause boundary and modal word —
   or no touch.
6. Index-row compaction where a homeless fact's relocation is contested — the row keeps its length until
   the owner rules.
7. Two duplicate copies found to disagree pre-rewrite: a pre-existing spec defect, queued, never "fixed"
   inside a readability pass.

## Scope

The living spec-family docs: PRODUCT_SPEC.md, ARCHITECTURE.md, TEST_MATRIX.md, ROADMAP.md, the skill docs.
The dated history (JOURNAL.md) is a record and is not rewritten. NEXT_STEPS is bounded by rule already.
The mechanical parts (Phase 0 freezes, the redundancy and style floors, the anchor/occurrence guard) wire
into the push gate as the compaction gate, ratcheted so a doc can only get cleaner, so no project re-bloats.
