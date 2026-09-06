# R7 — the inventory of mandated escort documents

Root: Alexander's direction of 2026-08-11 10:23 — "надо понять все такие лишние элементы… выпиливать а не
чинить". The plan line is `.live-spec/culling-plan-v3-2026-08-10.md:65`. This page replaces the earlier D6,
which had asked for a carve-out from the deletion bookkeeping; the plan's line 73 records that the
five-document escort around a removal was itself named invented, and that an inventory should come before
any relief.

An **escort document** here is an accompanying record the rules require a session to write *around an
action* — not the artifact the work produces, but the paperwork that rides beside it. Five actions are
covered: a commit, a push, a deletion, a review, and the completion of a change.

This page reads only. It changes no rule, deletes no file, and retires nothing. The campaign's rule 2
(`.live-spec/culling-plan-v3-2026-08-10.md:33`) holds until Alexander closes it.

## How each origin verdict was reached

Every escort was traced through five sources: the rule's own text in the skill bodies (many rules carry
their provenance inline), then `JOURNAL.md` and its archive, then `DECISIONS.md`, then `ROADMAP.md` and all
four rotated files under `docs/queue-archive/`, and finally the introducing commit's own message where the
document trail ran out.

One fact about this repository shapes every reading. On 2026-07-12 all owner-name attributions were swept
out of the shipped documents and the journal was made their single home
(`docs/queue-archive/JOURNAL-archive-2026-07-29.md:15-23`). So a rule's silence in `PRODUCT_SPEC.md` or a
`SKILL.md` proves nothing about its origin — the queue rows and the journal are the record, and that is
where these verdicts come from.

- **HIS WORD** — Alexander's own dated word created the requirement, and a record names the exchange.
- **DERIVED** — the requirement follows necessarily from a rule he approved; the parent rule is named.
- **INVENTED** — no traceable human word. A session, an audit, or a prover finding grew it on its own.

**The split that decides most verdicts.** Alexander's word very often backs an **activity** — re-check
before every push, review the design, declare a spec delta's class — while the **document filed to prove
the activity happened** was added by a session afterwards. Where his word plainly reaches the document
itself, the verdict is HIS WORD. Where it stops at the activity and the file is the session's convention,
the verdict is DERIVED, with his word named as the parent. INVENTED is reserved for escorts where neither
half traces to him.

---

## 1. A commit

| Escort | Mandating rule (file:line, code) | Origin |
|---|---|---|
| `NEXT_STEPS.md` refreshed inside the landing commit | `guardrails/check-landing-next-steps.py:277,302-310` [INV-242]; the resume duty at `skills/build-pipeline/SKILL.md:561-562` | **HIS WORD** — roadmap row 433, `docs/queue-archive/rotated-ROADMAP-2026-07.md:220`: "A landing that ships a movement refreshes the forward map in the same breath (Alexander's word, 2026-07-19…)". The gate's mechanics are the pack's; the duty is his. **Retired 2026-09-06** with `guardrails/check-landing-next-steps.py` itself: `spec/live-status-reporting.md` Requirement 257 was rewritten so the resume file carries no queue, and his duty moved to the surface that now holds the forward map — `spec/work-board.md` Requirement 309 criterion 88, the work board's update inside the landing's own commit. The pins in the middle column are dead as of that date. |
| A deferral reason on every parked item in `NEXT_STEPS.md` and `docs/decisions/*.md` | `guardrails/check-deferral-marker.py`, wired at `guardrails/pre-commit:33-43`; rule 29, `skills/live-spec-base/SKILL.md:469-490` [INV-152] | **DERIVED** — parent is rule 27's decide-what-you-can posture [INV-143], which rests on his ask-never-guess word. |
| A cleanup notice in the source of anything that ends a process | `guardrails/check-cleanup-notice.sh:48-60,89-97`, gate o [INV-204] | **HIS WORD** — `JOURNAL.md:570` and `:1712-1713`: "His second word, ~16:58 … the minimum owed everywhere is a notice." (2026-07-17). An in-file marker rather than a document. |
| A `.live-spec/plan-v3-delta-<date>.md` page whenever the culling plan is edited | `.live-spec/check-plan-delta.sh:19-29`, wired at `guardrails/pre-commit:88-91` | **HIS WORD** — his plan discipline: one plan is the shared surface and every edit is a named change he can read. |
| Red is never committed; the failing test name becomes the top resume item | rule 6, `skills/live-spec-base/SKILL.md:154-157`; `skills/build-pipeline/SKILL.md:429-431` | **DERIVED** — parent is rule 6's checkpoint duty, which is his (below). Ships in the founding commit with no human cited. No separate file. |

The commit is the lightest of the five actions. Nothing here is a cut candidate.

---

## 2. A push

This is where the escort load actually sits. A single push on this repository can owe six records.

| Escort | Mandating rule (file:line, code) | Origin |
|---|---|---|
| **Prover record** `docs/prover/YYYY-MM-DD.md`, dated today, fresh against both `PRODUCT_SPEC.md` and `ARCHITECTURE.md` | `PRODUCT_SPEC.md:3210` [M-6, INV-11, INV-116]; `skills/build-pipeline/SKILL.md:267`; gate a, `guardrails/check-prover-record.sh:93-98,137-160` | **DERIVED** — his word covers the re-check, quoted at `docs/queue-archive/2026-07-05.md:22`: "Alexander 2026-07-04: «именно для live-spec перепроверять при каждом пуше»". The words "recorded in docs/prover/" on that same line are the row author's framing. Parent: his re-check word plus rule 13. |
| **Push review record** `docs/push-review/YYYY-MM-DD-<slug>.md`, committed, carrying Range / Files read / Checks run / Findings / Blocking | `PRODUCT_SPEC.md:7467-7487` [INV-304]; `docs/push-review/README.md`; gate ac, `guardrails/check-push-review.sh:111-221` | **INVENTED** — see the cut list. No entry in `DECISIONS.md`, no queue row in `ROADMAP.md` or any archive. The introducing commit `cefd11d` (2026-08-05) states the reasoning as the pack's own. |
| **Skill review record** `docs/skill-review/YYYY-MM-DD-<skill>.md` with a `Verdict:` line, fresh against the skill's last commit | `PRODUCT_SPEC.md:1274` [INV-99]; `skills/build-pipeline/SKILL.md:239`; gate s, `guardrails/check-skill-review.sh:117-141` | **HIS WORD** — the strongest provenance in the whole inventory. Row 419, `docs/queue-archive/rotated-ROADMAP-2026-07.md:213`: "(his word, Alexander 2026-07-17 ~18:26: he leans on the session to remember to run Anthropic's skill-creator review whenever a skill is modified, and the session forgets, so a reminder does not hold and **he asks for a blocking gate**)". He asked for the gate by name. |
| **README re-walk** against the pushed truth | `PRODUCT_SPEC.md:3305-3311` [INV-44]; `docs/push-law.md`, the push law's fourth part | **HIS WORD** — "re-read at every push and a resolved issue removed the push it ships (his word 2026-07-10)" (`skills/publish/SKILL.md:60`). Held by no gate. |
| **Queue-archive rotation manifest** — a rotated row must be findable in its archive and named by a live `<!-- rotated-manifest -->` line | `PRODUCT_SPEC.md:5792-5799` [INV-209, INV-276]; gate t, `guardrails/check-doc-rotation.py:186-213` | **DERIVED** — parent is his standing format order of 2026-07-22 (row 480, `docs/queue-archive/rotated-ROADMAP-2026-07.md:238`) plus rule 10. The clause making the delivery report ride along is the pack's, driven by a byte-ceiling problem. |
| **The waiting board** `WAITING.md` — no omitted item, no silent demotion | gate q, `guardrails/check-board.py:161-168,107,134` | **HIS WORD** — the board exists because a question parked for him scrolls away; `WAITING.md:5-9` states it in his terms. |

**The duplication, now sharper.** Gate a and gate ac both demand an adversarial read of the same delta, into
two separate committed files, on the same push. The 2026-08-09 handover already lists "A gate edit merging
the two review records into one review per push" as work waiting on his word
(`.live-spec/handover-2026-08-09.md:118`, item 4). The inventory adds the reason it should be gate ac that
folds into gate a: gate a's record answers to his own 2026-07-04 word, and gate ac's answers to nobody's.

---

## 3. A deletion or removal

This is the action D6 was about. The 2026-08-09 handover names "five artifacts per removed item" as what
makes removal cost more than the thing removed (`.live-spec/handover-2026-08-09.md:117-118`).

| Escort | Mandating rule (file:line, code) | Origin |
|---|---|---|
| **Attic manifest line** — a superseded file moves to `attic/` with one line stating what it was, why it moved, and the date | rule 10, `skills/live-spec-base/SKILL.md:226-228`; `PRODUCT_SPEC.md:4130-4131` [INV-7, A-4] | **HIS WORD** — row 9, `docs/queue-archive/2026-07-05.md:15`: "Superseded old files are ARCHIVED, never deleted — attic/ folder with a manifest (Alexander 2026-07-04)". |
| **Dated REMOVED tombstone in the spec, and matrix rows retired rather than left reading BUILT** | rule 10, `skills/live-spec-base/SKILL.md:227`; `skills/build-pipeline/SKILL.md:193-195` | **INVENTED** — see the cut list. Present in the founding package skeleton (commit `63cc21c`, 2026-07-04) before any wish about it; no owner attribution exists anywhere. |
| **Explicit approval before deleting regenerable junk**, listed with counts and sizes | `PRODUCT_SPEC.md:4136-4137` [A-9] | **HIS WORD** — a human gate of rule 12's family, born of the same 2026-07-04 exchange as the attic. Not paperwork. |
| **Journal entry** naming what was removed and why | rule 9, `skills/live-spec-base/SKILL.md:217-224` | **HIS WORD** — see the landing section. |
| **Delivery report** closing the removal's row | [INV-103, INV-276] — see the landing section | **HIS WORD**. |

**The bypass worth naming.** `guardrails/check-deletion-only-push.sh`, consumed at `guardrails/pre-push:33-40`,
stands the **entire** gate chain down when a push contains only deletions. So no gate reads any escort on a
pure removal. The expense D6 named is not mechanical at all — it is the prose bookkeeping of rules 9 and 10,
which no machine enforces and no gate would catch a session skipping.

**The honest reading for the campaign.** Of the five artifacts a removal owes, four rest on Alexander's own
word: the attic manifest line, the junk-approval gate, the journal entry, and the delivery report. Only the
tombstone-and-retired-rows clause is invented, and it is the cheapest of the five to write. **Cutting the
invented one will not make removal materially cheaper.** If removal must get cheaper, the lever is a
narrower scope for rules 9 and 10 when the thing removed is a piece of the pack's own machinery rather than
something he authored — and that is his word to give, not a cut this inventory can recommend.

---

## 4. A review

| Escort | Mandating rule (file:line, code) | Origin |
|---|---|---|
| **Prover record**, per-finding folded / rejected-with-why column | `skills/build-pipeline/SKILL.md:267-272`; `skills/product-prover/SKILL.md:969-975` | **DERIVED** — see the push section. The defect-versus-recommendation column is owner-adjacent: "Alexander asked straight whether the prover could say which findings are defects and which are recommendations" (`docs/queue-archive/rotated-ROADMAP-2026-07.md:117`). |
| **Architecture prover record** `docs/prover/architecture-prover-record.md` | `skills/build-pipeline/SKILL.md:358-362`; `PRODUCT_SPEC.md:7012` [INV-279] | **INVENTED** — see the cut list. |
| **Design review record** `docs/design-review/YYYY-MM-DD[-suffix].md` | `skills/design-reviewer/SKILL.md:376-382`; `skills/build-pipeline/SKILL.md:284` [INV-141] | **INVENTED** — see the cut list. The *pass* is his wish (`docs/queue-archive/rotated-ROADMAP-2026-07.md:119`); the filed record is not. |
| **Skill review record** with its `Verdict:` line | `PRODUCT_SPEC.md:1274` [INV-99]; gate s | **HIS WORD** — see the push section. |
| **Clean-context release review record**, dated to the release, naming a seat other than the release's | rule 33, `skills/live-spec-base/SKILL.md:605-609`; `PRODUCT_SPEC.md:5170` [INV-237] | **DERIVED** — the law is his, quoted in row 422 (`docs/queue-archive/rotated-ROADMAP-2026-07.md:215`, 2026-07-18). The record is the session's addition and shipped hedged — the spec says the gate "*shall* be able to require" it, and no such gate was ever built. Costs nothing today. |
| **Fresh-context audit verdict** riding the delivery report | `skills/build-pipeline/SKILL.md:441-461` [INV-46]; `PRODUCT_SPEC.md:5118-5126` | **DERIVED** — birth is a prior-art harvest with no human cited (row 110, `docs/queue-archive/rotated-ROADMAP-2026-07.md:13`), but his 2026-07-12 steer set the cadence: "an audit needs to happen constantly — think about how best to write this in" (row 290, `:103`). Writes no file; rides the report. |
| **Norm freeze** — an approved sketch copied to `docs/norms/` with a dated provenance line | `skills/spec-author/SKILL.md:264-268`; `PRODUCT_SPEC.md:2372` [INV-43] | **HIS WORD** — it escorts *his own approval* of a look, and the rule cites the exchange (tlvphotos, 2026-07-05). |
| **Reading-round record** naming each cold reader's supplier | ROADMAP row 559, `ROADMAP.md:234` | **DERIVED** — from rules 21 and 33. Queued, never landed; no cost yet. |
| **Delta record** `docs/deltas/YYYY-MM-DD-<row>.json` | `guardrails/check-delta-record.py:88-92,116-125` | **INVENTED** — see the cut list. |
| **Spec freeze baselines** `.spec-freeze/*.json` | gate k, `guardrails/check-freeze.sh:26-30,48-54` | **INVENTED** — see the cut list. Zero live cost. |

---

## 5. Completing a change — a landing

| Escort | Mandating rule (file:line, code) | Origin |
|---|---|---|
| **The delivery report** | `skills/build-pipeline/SKILL.md:471-499`; `PRODUCT_SPEC.md:5037-5039` [INV-103], `:6930-6931` [INV-276], `:7813-7816` [INV-314] | **HIS WORD** — no single "he asked for a delivery report" sentence exists, because it predates live-spec: it came from his own prior skill repos and playbook, a method "running in production on track-coach for over a year" (`docs/queue-archive/JOURNAL-archive-2026-07-29.md:623`). He then shaped it repeatedly by dated word — row 28 (`docs/queue-archive/2026-07-05.md:31`): "Reports must RETELL, not reference … (Alexander 2026-07-04 night)". |
| **Delegation accounting** — the unit sent, its saving, the reads dispatched | `PRODUCT_SPEC.md:5037,5062` [INV-103, INV-137]; rule 25, `skills/live-spec-base/SKILL.md:433-436` | **HIS WORD** — his own playbook rule, mined on his 2026-07-04 order (row 12); the mechanical check ordered in his 2026-07-12 exchange (row 254, `docs/queue-archive/rotated-ROADMAP-2026-07.md:69`); reads-dispatched from his 2026-07-13 steer (row 301, `:114`). |
| **Root naming** — every work block opens by naming its root | `PRODUCT_SPEC.md:7813-7832` [INV-314] | **HIS WORD** — row 569, `ROADMAP.md:67`: "(Alexander 2026-08-07, 00:17, 00:42, 00:46). Sessions entered long work blocks he could not connect to any request of his." |
| **Footprint note** on every landed feature-or-refactor row | `PRODUCT_SPEC.md:1167,1151` [INV-134, INV-128] | **DERIVED** — from the three-source impact read. |
| **Step accounting** — every door-granted step applied in its kind's form or stood down by name | `PRODUCT_SPEC.md:1290` [INV-22, E-12]; `skills/build-pipeline/SKILL.md:231-236` | **DERIVED** — from rule 15, the door law. |
| **Removal accounting** — every removal of substance listed with one line of judgment | `PRODUCT_SPEC.md:786` [INV-109]; `skills/communicator/SKILL.md:470` | **HIS WORD** — it exists because he lost content to a rewrite. |
| **Estimate beside actual** | `PRODUCT_SPEC.md:770` [INV-93] | **HIS WORD** — row 232; every ask hears its price and the landing settles it. |
| **`JOURNAL.md` entry**, dated with time of day | rule 9, `skills/live-spec-base/SKILL.md:217-224` | **HIS WORD** — logged as such: "rule 9 dated-journal … an Alexander 2026-07-05 decision" (`docs/queue-archive/JOURNAL-archive-2026-07-29.md:23`). The time-of-day half is his in writing, row 46 (`docs/queue-archive/2026-07-05.md:44`). |
| **`CHANGELOG.md` entry** speaking to the user | `skills/build-pipeline/SKILL.md:472-479` | **DERIVED** — parent is rule 9's docs-travel clause, which is his. Ships at founding and was refined by gap-mining; no sentence of his is quoted. The weakest owner link of the writing set, but it inherits a parent he owns. |
| **`DECISIONS.md` anchored entry** whenever a decision is recorded as his | rule 13, `skills/live-spec-base/SKILL.md:246-259`; `PRODUCT_SPEC.md:5692-5699` [INV-207]; gate r | **HIS WORD** — row 415, `docs/queue-archive/rotated-ROADMAP-2026-07.md:209`: born 2026-07-17 ~15:38 when he read a rule quoted back as his own ranking and recognised nothing, then rewritten ~17:09 on his refusal of the first design. |
| **Checkpoint file** under `.live-spec/checkpoints/` | rule 6, `skills/live-spec-base/SKILL.md:150-155`; `PRODUCT_SPEC.md:4962` [ACT-3] | **HIS WORD** — row 24, `docs/queue-archive/2026-07-05.md:28`: "checkpoint discipline stated ONCE, other skills reference not repeat (Alexander 2026-07-04)". |
| **The landing flips its checkpoint to closed** | `PRODUCT_SPEC.md:2849-2850` [INV-107] | **INVENTED** — see the cut list. Row 226 is an audit item, no human cited. |
| **Queue-archive rotation** — the closing commit moves the row and its delivery report to the month's archive | `PRODUCT_SPEC.md:6930-6931` [INV-276]; gate t | **DERIVED** — see the push section. |
| **`MIGRATION.md` dated chapter** on a release that costs a host an action | `PRODUCT_SPEC.md:4152-4153` [INV-91]; rule 32, `skills/live-spec-base/SKILL.md:577-582` | **HIS WORD** — "Alexander's ~12:10 and ~12:21 words extended the section after this review ran … INV-91" (`docs/prover/2026-07-10-row221.md:69-73`). |
| **Release note** — a recorded offer-or-none decision | `guardrails/check-release-note.py:43-75` [INV-228] | **INVENTED** in its escort half — see the cut list. The *feature* (a release note may offer the reader next steps) is his wish, row 402. |
| **Handover** under `docs/handovers/`, ending `-handover.md`, naming transcript / extract / written by | rule 35, `skills/live-spec-base/SKILL.md:623-641` [INV-302] | **HIS WORD** — his own words in `DECISIONS.md:331-341` (2026-07-28 ~21:58): "тогда имеет смысл дешевым воркером всегда читать прошлую сессию? как процесс? всегда?". Note the pack already withdrew the gate that read the record's three lines, on 2026-08-09, "after finding no error the script had ever caught" (`skills/live-spec-base/SKILL.md:637-639`); the withdrawn script rests at `attic/check-handover-provenance.py`. The discipline stands on his word; its machine is already gone. |
| **`PROBLEMS.md` WATCHED line** on first sight of workshop noise | rule 19, `skills/live-spec-base/SKILL.md:324-336`; `PRODUCT_SPEC.md:3694` [INV-23] | **HIS WORD**, verbatim — row 100, `docs/queue-archive/rotated-ROADMAP-2026-07.md:47`: "(Alexander 2026-07-05 ~23:00 … if there's a problem, especially a recurring one, it has to be solved — solved!!)". The four-status vocabulary is the pack's mechanization of that word. |
| **Tier-override log** — proposed tier → chosen tier → why | rule 5, `skills/live-spec-base/SKILL.md:146-148`; `PRODUCT_SPEC.md:5013` [INV-69] | **INVENTED** — see the cut list. |
| **Board line** — "serial by the graph" recorded when independent lanes stand free | `skills/build-pipeline/SKILL.md:601-605` [INV-49, INV-214] | **DERIVED** — from the lanes law. |
| **Worker-halt record** in the row's delivery report | `PRODUCT_SPEC.md:7359` [INV-298, INV-103]; rule 7, `skills/live-spec-base/SKILL.md:197` | **HIS WORD** — born of the 2026-08-05 incident where a worker ran `git stash` against the shared tree (`JOURNAL.md:2127-2131`), on the day he asked for the push. |

**The finding the table hides.** The delivery report is one document carrying roughly twenty mandated
fields. `PRODUCT_SPEC.md` names it 39 times and the skills 25 more. The report itself is unambiguously his,
and so are eight of its fields. But it is the single densest escort in the method, and thinning its field
list — not cutting it — is where the real weight sits.

---

## The candidate-cut list — every INVENTED escort, with what breaks

Nine escorts carry no traceable human word. They are ordered by what cutting them actually buys.

### 1. The delta record — `docs/deltas/YYYY-MM-DD-<row>.json`

- **Action escorted:** a review (a spec-format delivery).
- **Mandating rule:** `guardrails/check-delta-record.py:88-92,116-125`. No spec code, no rule text outside
  the script. The requirement sits inside owner-headed row 445, but the journal's own enumeration of what
  was actually his that day does not include the classifier (`JOURNAL.md:307`).
- **Removal cost: none.** Marked UNARMED at its own line 4, in no hook, and **`docs/deltas/` does not exist
  in the tree** — a required document that has never once been written. `tests/test_delta_classifier.py`
  (11 tests, 82 lines) runs against fixtures only. Deleting the script retires those tests and nothing else.

### 2. The release note's recorded offer-or-none decision

- **Action escorted:** completing a change (a release).
- **Mandating rule:** `guardrails/check-release-note.py:43-75` [INV-228]. His wish was that a release note
  *may* offer the reader next steps (row 402); the duty to **record** the decision either way is the
  script's own addition, stated in its docstring at `:7-11`.
- **Removal cost: low.** In no hook, no gate letter, and its own header states no committed file exists for
  it to scan (`:21-23`). Cutting it means deleting the script, `guardrails/release-note-fixtures`, and
  `tests/test_release_note.py` (12 tests, 121 lines), then removing its key from
  `scripts/check-registry.json` — gate ae reds on a registry key naming a missing file. His feature stays;
  only the bookkeeping goes.

### 3. The landing flips its checkpoint to closed — [INV-107]

- **Action escorted:** completing a change.
- **Mandating rule:** `PRODUCT_SPEC.md:2849-2850`. Row 226, `docs/queue-archive/rotated-ROADMAP-2026-07.md:51`,
  is an audit item: "two engine checkpoints still read 'not started' after everything in them shipped".
  No human cited. The checkpoint *file* itself is his (2026-07-04) and stays.
- **Removal cost: low.** No gate. `tests/test_checkpoint_closes.py` (3 tests, 75 lines) is the only pin,
  plus the [INV-107] matrix rows that `tests/test_traceability.py` requires — an invariant retired without
  its rows reds the suite. Weigh before cutting: the audit that produced it names a real cost, a resuming
  session redoing finished work.

### 4. The tier-override log

- **Action escorted:** completing a change.
- **Mandating rule:** rule 5, `skills/live-spec-base/SKILL.md:146-148`; `PRODUCT_SPEC.md:5013` [INV-69].
  Born of prover finding F1 and decided by the session itself as D-2 on 2026-07-07, with the session's own
  rationale on record (`docs/queue-archive/JOURNAL-archive-2026-07-29.md:600-602`). His later word (row 253)
  is about tiering, not about logging it.
- **Removal cost: low.** No file of its own, no gate, no dedicated test — it is one field of the delivery
  report and one clause of rule 5. Cutting it is an edit to two sentences plus the [INV-69] matrix rows that
  assert it.

### 5. Spec freeze baselines — `.spec-freeze/*.json`

- **Action escorted:** a review (a restyle or restructure).
- **Mandating rule:** gate k, `guardrails/check-freeze.sh`. `scripts/spec-freeze.py:4` states its own
  rationale with no human behind it. Rule 22's convergence-lock is a plausible parent but names four other
  mechanisms and not this one.
- **Removal cost: near zero — and so is the gain.** The baselines are local and gitignored, and an absent
  baseline **skips silently** (`check-freeze.sh:26-30`), so the gate already costs nothing on a fresh clone
  or in CI. Listed for completeness. **Cutting it buys nothing; leave it.**

### 6. The architecture prover record — `docs/prover/architecture-prover-record.md`

- **Action escorted:** a review (a full pass at an M-1 or M-6 gate).
- **Mandating rule:** `skills/build-pipeline/SKILL.md:358-362`; `PRODUCT_SPEC.md:7012` [INV-279]. The owner
  attribution on its row (456) covers only the *scope* of the format conversion, not this record; the
  reasoning is the pack's, at `docs/architecture-format.md:116`.
- **Removal cost: low, but it touches the spec.** No gate reads this file — gate a reads dated records under
  `docs/prover/`, not this one. The architecture pass is **already** recorded by the dated prover record that
  `PRODUCT_SPEC.md:2977` [M-1, INV-116] requires, so this is a second home for a fact that already has one,
  which rule 4 forbids. What breaks: clause 4 of [INV-279] retires, pulling its `TEST_MATRIX.md` rows;
  `tests/test_prover_doc_homes.py` (3 tests, 50 lines) is the closest pin and should be read first.
- **This is the cleanest genuine cut on the list.**

### 7. The design review record — `docs/design-review/YYYY-MM-DD[-suffix].md`

- **Action escorted:** a review.
- **Mandating rule:** `skills/design-reviewer/SKILL.md:376-382`; `skills/build-pipeline/SKILL.md:284`
  [INV-141]. His wish reaches the *pass* — "a senior review that questions the design, not only verifies
  it" (`docs/queue-archive/rotated-ROADMAP-2026-07.md:119`) — and stops there. The record's shape is
  admitted analogy: "It follows the same shape and discipline as the prover's record".
- **Removal cost: moderate.** 15 files, 164 KB on disk. No gate reads the directory. The pass is
  non-blocking by rule (`skills/build-pipeline/SKILL.md:278-279`), so no lane depends on the record. What
  breaks: the record section of the design-reviewer skill and the pointer in build-pipeline — and a skill-body
  edit then owes its own skill-review record under gate s. Weigh before cutting: the record is what lets the
  next run check the previous unfolded rows, which is the same argument the prover record rests on.

### 8. The removal tombstone, and matrix rows retired

- **Action escorted:** a deletion.
- **Mandating rule:** rule 10, `skills/live-spec-base/SKILL.md:227`; `skills/build-pipeline/SKILL.md:193-195`.
  Present in the founding package skeleton, commit `63cc21c` of 2026-07-04, before any wish about it. The
  word "tombstone" appears nowhere in `PRODUCT_SPEC.md`. Its cost is already under challenge in
  `docs/prover/2026-08-09-culling-plan-v2.md:106-124`.
- **Removal cost: low mechanically.** No gate reads for a tombstone; nothing in the suite pins it. Cutting
  it edits one clause of rule 10 and one line of build-pipeline.
- **But it is the wrong target.** It is one of D6's five artifacts and the cheapest of them to write. The
  other four all rest on his word. Cutting the tombstone alone barely moves the cost of a removal, and the
  build-pipeline line records the incident that earned it: "an excision cleaned code + tests but left four
  doc surfaces dangling".

### 9. The push review record — `docs/push-review/YYYY-MM-DD-<slug>.md`

- **Action escorted:** a push.
- **Mandating rule:** `PRODUCT_SPEC.md:7461-7490` [INV-304]; gate ac, `guardrails/check-push-review.sh`.
- **Origin, stated plainly:** nothing in `DECISIONS.md`, `ROADMAP.md`, or any archive attributes it to him,
  and **no queue row for it exists anywhere**. The introducing commit `cefd11d` (2026-08-05) gives the
  pack's own reasoning: an adversarial review had run before two pushes because it was asked for in the
  moment, "Its home was that conversation and nothing else, so the next session would push without one."
  The nearest owner touch is weaker than it looks — `JOURNAL.md:2108`, "Alexander raised the worker cap and
  asked for the push." He asked for a push; a session added the review, the record shape, and the gate.
- **Removal cost: the highest on this list, and cutting it is not recommended.** Wired as gate ac at
  `guardrails/pre-push:240`; pinned by `tests/test_push_review.py` (19 tests, 369 lines); it owns
  Requirement 305 of the spec with its `TEST_MATRIX.md` rows; and it carries entries in
  `guardrails/gate-red-proofs.json` (gate w reds without one), `guardrails/ci-mirror.json` (gate u reds
  without the mirror), and `scripts/check-registry.json` (gate ae).
- **Why it should survive as a merge rather than a cut.** It is one of only six gates out of 31 with a real
  dated catch (`.live-spec/day1-census-checks.md:65`, 2026-08-05), and that catch was substantial: eleven
  findings across 24 unpushed commits, every one repaired the same hour (`JOURNAL.md:2108-2110`), four of
  which are still standing as roadmap rows 562–565. An invented escort that demonstrably works is not the
  same as dead weight. **The right move is the gate edit already waiting on his word since 2026-08-09 —
  fold gate ac into gate a, one adversarial review per push, one record.** Cutting it outright would drop a
  review that has caught more real defects than any other gate in the tree.

---

## What the inventory found

Forty-one escort requirements were traced across the five actions. **Twenty-one rest on Alexander's own
dated word. Eleven derive from a rule he approved. Nine have no traceable human word.**

The nine invented ones are, in the main, cheap and low-yield. Two of them have never produced a single
document (the delta record and the release note's recorded decision). One costs nothing to keep and nothing
to cut (the freeze baselines). One is the lightest of the five artifacts that make a removal expensive (the
tombstone). The two genuinely worth cutting are the architecture prover record — a second home for a fact
the dated prover records already hold, which rule 4 forbids — and, on a closer weighing, the design review
record.

The largest invented escort, the push review record, is also the one that works. It should be merged into
the prover record rather than cut, which is the edit already sitting on his word since 2026-08-09.

Two things this inventory turned up that fall outside its own cut list, and that the campaign should carry
forward. First, the escort cost of a **removal** is almost entirely his own word — rules 9 and 10 — so
making removal cheaper needs a narrower scope for those rules when the thing removed is the pack's own
machinery, and that is a decision only he can give. Second, the **delivery report** carries roughly twenty
mandated fields across 64 references in the spec and skills; the report is his, most of its fields are
derived, and thinning that field list is where the largest remaining weight sits.
