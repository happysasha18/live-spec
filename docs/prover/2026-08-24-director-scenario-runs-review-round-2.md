# Adversarial review, round 2 — director-scenario-runs

ADVERSARIAL-REVIEW (independent, second round)

Reviewer: same adversarial seat that returned 4 blocking findings on the first attempt at this
slice, re-run after a full rework. Clean re-derivation: every number below was recomputed from
the tree and from `git show`, not read out of the record under review.

Target: `docs/prover/2026-08-24-director-scenario-runs.md` (rewritten; untracked) and the working
tree of `/private/tmp/ls-director/wt` on branch `director/2026-08-21-package-1`.

Scope of this round, as briefed: verify the four original findings are actually fixed, and catch
what the rework itself may have introduced. Not in scope: re-litigating whether 19/35 vs 23/35 is
a good result. It is what it is.

Working-tree state at review time: 35 modified files, all under `evals/director/traces/`, plus one
untracked file (the record). Nothing else modified, nothing committed. `git rev-parse` confirms
`origin/main`, `HEAD` and `23f83047` are all the same commit
(`23f830472b4c16f7889f73baafaf804227c720ac`), so "vs origin/main", "vs HEAD" and "vs the shadow
snapshot" are the same baseline throughout.

---

## The four original findings

### 1. Circular fixture edit inflating the headline — RESOLVED

```
$ git diff origin/main -- evals/director/scenarios.json
[empty]
```

Zero diff. No fixture edit ships. The corrections log was read directly out of the JSON rather
than eyeballed in a diff:

```
$ python3 -c "import json; d=json.load(open('evals/director/scenarios.json')); print(len(d['corrections']))"
2
```

Both entries are the pre-existing ones (`decision-how-to-report`, `decision-a-boundary`); with a
zero diff against `origin/main` no entry could have been added. Nothing in the corrections log
refers to this slice. Confirmed resolved.

### 2. Asymmetric re-rolling with discarded results kept nowhere — RESOLVED

The substantive test is not what the record says, it is which draw is on disk. For all three
scenarios that were re-rolled in the discarded first attempt, the trace now on disk is the
**failing** draw, not the favourable one:

```
FAIL  observation-carrying-its-repair  (2 of 3)
        creates_work: wanted True, got False
        dimensions: missing ['quality, safety, regressions']
FAIL  mixed-plan-and-two-questions  (1 of 3)
        acts: missed ['observation']
FAIL  mixed-you-invented-that-work  (1 of 4)
        creates_work: wanted False, got True
```

The record claims the second draws of `mixed-plan-and-two-questions` and
`mixed-you-invented-that-work` matched the fixture exactly. Those passing draws are demonstrably
**not** what was kept — the cherry-pick is reversed, not repeated. That is the correct direction:
the record keeps the unfavourable draw and reports the favourable one in prose, rather than the
other way round.

Every additional draw is accounted for in the record, with its verdict content stated inline
(`observation-carrying-its-repair` 3 draws, the other three cases 2 draws each), including the
draws that did not help — `mixed-conditional-pause`'s second draw is reported as diverging in a
*third* distinct way, which is evidence against the run, not for it.

On file-level preservation: my original finding was "discarded results not kept anywhere," and the
wrong it named was cherry-picking, not archival policy. Inline reporting of each draw's exact acts
and booleans satisfies what I meant. I am not holding out for a committed archive of every draw.

One residual, non-blocking: shadow was **not** resampled. The "half the gap is single-draw noise"
argument therefore rests on one-sided evidence — the new skill's stability was probed on the four
cases where it lost, and shadow's stability was probed nowhere. That asymmetry no longer
contaminates the headline (both sides' scores are single blind passes), and it cuts toward a
conclusion the record declines to claim, but the record does not flag it. Noted below.

### 3. "12 of 16 reproduced identically" was false (actually 9) — RESOLVED

Recomputed from scratch. I extracted all 35 shadow traces myself via
`git show 23f83047:evals/director/traces/<id>.json` into a scratch directory (35/35, all parsing),
and called `check.grade()` directly per scenario against the same untouched `scenarios.json` for
both trace sets:

```
NEW pass 19/35   SHADOW pass 23/35

fail in BOTH: 12  (identical reason 9, different reason 3)
fail NEW only: 4  -> ['observation-carrying-its-repair', 'mixed-plan-and-two-questions',
                      'mixed-conditional-pause', 'mixed-you-invented-that-work']
fail SHADOW only: 0 -> []

skill_version tally new:    Counter({'5.0.0': 35})
skill_version tally shadow: Counter({'0.3.0': 35})
```

The record's claim — 19/35 vs 23/35; 12 fail in both (9 identical + 3 different-reason); 4 new-only;
0 shadow-only — matches my independent computation **exactly**, including the named membership of
the new-only set and the named membership of the different-reason set (`instruction-a-procedure`,
`mixed-check-now-improve-later`, `observation-a-verdict-on-delivered-work`).

The record's sharpest self-criticism also checks out. It says that on
`observation-a-verdict-on-delivered-work` the new run is strictly worse. Verified:

```
observation-a-verdict-on-delivered-work
   new:    ['creates_work: wanted True, got False',
            "dimensions: missing ['product value and behaviour']"]
   shadow: ["dimensions: missing ['product value and behaviour']"]
```

New fails the exactly-graded boolean plus the by-inclusion dimension; shadow fails only the
dimension. The record volunteered this against itself and stated it accurately.

I also checked the orchestrator's own leftover shadow directories rather than assuming good faith:
`diff -rq` shows `/tmp/shadow-all` and `/tmp/shadow-traces` are byte-identical to my independent
git extraction. The shadow set that was graded was faithful to the commit; no doctoring.

### 4. The fixture correction didn't hold up — RESOLVED

`observation-carrying-its-repair`'s `expect` is identical to `origin/main` (entailed by the zero
diff on `scenarios.json`, and confirmed by reading the scenario object directly). The record no
longer asserts the fixture is wrong. Its own words:

> Three runs converging shows the acting-mode skill *consistently* reads this case one way; it
> does not show that reading is *correct*, and this record does not adjudicate that question.

It is presented as a named, open, unresolved disagreement, with a suggested resolution path
(clarify the situation the way `decision-a-boundary` was clarified) explicitly *not* taken in this
slice. That is what I asked for.

The record's textual argument for *why* the earlier fixture edit failed is load-bearing, so I
verified its three SKILL.md citations rather than trusting them. All three are accurate and in
context:

- `skills/director/SKILL.md:210-213` — "A question, an idea, an observation or a halt gets no
  sheet, per above — and nothing below applies to it. What follows runs only for work that just
  earned a decision sheet". The Execution section really is self-scoped away from an unaccepted
  observation, so the closing-checkpoint rule cannot settle this scenario's classification.
- `skills/director/SKILL.md:84-87` — "The first clause looks like the message, the rest gets read
  as its background... This is the most common way this design fails in practice". Exactly the
  failure mode cited for `mixed-conditional-pause`.
- `skills/director/SKILL.md:189-199` — the export-button worked example is an "Observation whose
  repair follows beyond doubt" and does get a sheet, with no open checkpoint stated.

---

## Additional checks

**Skill untouched.** `git diff origin/main -- skills/director/SKILL.md` — empty.

**Classification section unchanged vs shadow.** The record's methodological claim was re-derived,
not accepted. Extracting the `## First — what did the human just do?` section from both revisions
and hashing:

```
old (ad851b7d~1) len 7515  sha bcec88125283a5aa
new (HEAD)       len 7515  sha bcec88125283a5aa
BYTE-IDENTICAL: True
```

The only section-header change in that diff is `-## Shadow mode` / `+## Execution`. Claim holds.

**Tests.** `python3 -m pytest tests/test_director_scenarios.py -q` → `11 passed in 0.28s`.

**Gate wording.** `JOURNAL.md:3051-3054` reads: "the cutover waits for scenario coverage ... to
confirm the acting Director behaves at least as well as the shadow version did on the same
messages." The record characterises this accurately and concludes, in bold, "that bar is not
cleanly met: 19/35 vs 23/35, same expectations, zero cases where new beats shadow," and
"**This slice does not close the scenario-run completion criterion for package 3.**" No victory is
claimed. It also refuses the inverse laundering — "'no text changed' is not the same claim as
'behaviour is at least as good,' and this record does not launder the second into the first."

**Epistemic statuses kept apart.** The record does not collapse the four new-only failures into one
bucket. Two (`mixed-plan-and-two-questions`, `mixed-you-invented-that-work`) are called
demonstrated single-draw noise on resampling evidence; one (`mixed-conditional-pause`) is called
inherent difficulty, with the skill's own "most common way this design fails" line cited in
support — a citation I verified; one (`observation-carrying-its-repair`) is left explicitly
unresolved. Three distinct statuses, three distinct treatments. It also does not overclaim in the
opposite direction: the zero-shadow-only asymmetry is called "not by itself proof of a real
behavioural shift... but it is also not nothing."

**Trace genuineness.** I read the `reasoning` field of seven traces not examined in round 1
(`halt-without-the-word`, `not-an-act-a-bare-trace`, `correction-shouted-constraint`,
`idea-for-another-project`, `question-what-are-those`, `mixed-conditional-pause`,
`observation-carrying-its-repair`). All are genuine: each reasons from the specific situation, and
each cites skill text that exists (the halt/state rule, "no act absorbs another", "the repair
follows beyond doubt", the idea-shelf rule). None is boilerplate.

**Blinding is real.** All 35 traces carry a distinct opaque `id` of `case-1` .. `case-35` with no
gaps and no duplicates, alongside a separate `scenario` field. No two traces share a `reasoning`
string, so nothing was copy-pasted between cases.

**Structural integrity.** 35 scenarios, 35 trace files, no orphans in either direction; every trace
parses as JSON; all 35 stamped `5.0.0`. The revert missed nothing.

---

## Findings

**F1 (non-blocking, data quality).** `evals/director/traces/mixed-you-invented-that-work.json` is
internally incoherent: `creates_work: true` with `work_items: 0` and
`attaches_to_existing_work: true`. Under this book's own `verdict_shape`, work_items is "how many
NEW separate pieces of work this turn produces", so creating work while producing zero items
cannot both be true. Its `acts`, `work_items` and `attaches_to_existing_work` all match the fixture
exactly; the single failing check is that one incoherent boolean. This is a producer slip, not a
different reading of the message — which strengthens the record's "noise" characterisation of this
case. The record does not mention it, i.e. it under-uses evidence in its own favour. No action
required for this slice; worth knowing when the fourth new-only case is revisited.

**F2 (non-blocking, one-sided evidence).** Shadow was not resampled anywhere. The resampling
argument probes only the four cases the new skill lost, so it can show new-skill instability but
can never show shadow instability, and cannot show whether shadow would drop cases it currently
passes. The record should say so plainly where it introduces step 7. As it stands the headline is
uncontaminated (single blind pass on both sides) and the conclusion drawn is the conservative one,
so this does not revive finding 2.

**F3 (non-blocking, mild overstatement).** "Every disagreement between the two runs, without
exception, favors shadow" is true at pass/fail granularity but not at check granularity: on
`instruction-a-procedure` the new run fails one check (`acts: invented ['halt']`) where shadow
fails two (`acts: missed ['instruction'], invented ['correction']` and `work_items: wanted 1,
got 0`). The record enumerates that case so nothing is hidden, but it points out the one
different-reason case where new is worse and not the one where new is better. The bias runs
against the record's own interest, which is the safe direction — but the sentence as written is
stronger than the data.

**F4 (non-blocking, citation hygiene).** Three pointers in the record do not resolve:
- It cites the round-1 adversarial review as
  `docs/prover/2026-08-24-director-scenario-runs.md, superseded by this file` — that is the
  record's *own* path. The round-1 review is not on disk anywhere under `docs/`. A reader
  following that pointer lands back on the record.
- "See handoff §4 for the carried-forward item" — there is no handoff document in the tree, and
  no numbered §4 to carry it. `JOURNAL.md:3054` only says the comparison is "tracked in the
  handoff", with no such file committed.
- "mandate item 4.1.5" — the string `4.1.5` appears nowhere in the repository. "The mandate" is
  referenced throughout the tree as an external document, so this is plausibly a real reference to
  something outside git rather than an invention; I could not verify it either way, and flag it
  only because a record whose entire value is checkability should not carry unresolvable precise
  identifiers.

None of F1–F4 touches a number, a fixture, or the conclusion. They are accuracy and hygiene items.

## Verdict

All four original findings are genuinely resolved, and resolved in substance rather than in
wording. The fixture is fully reverted with no corrections-log entry; the cherry-picked draws have
been replaced by the failing originals on disk with every additional draw reported including the
unhelpful ones; the overlap figures I recomputed independently match the record item for item,
including the membership of every category; and the disputed scenario is untouched and presented
as an open question the record explicitly declines to settle. The record's self-critical claims —
the strictly-worse case, the byte-identical classification section, the three SKILL.md citations,
the gate wording — all survive independent checking. The gate conclusion is honestly negative in
both directions: it neither claims parity nor declares the acting skill worse as settled fact.

The rework introduced no new blocking problem. No broken JSON, no scenario missed by the revert,
no prose/disk inconsistency on any load-bearing claim.

Blocking: none.
