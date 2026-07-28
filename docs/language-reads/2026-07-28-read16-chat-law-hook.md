# Read 16, 2026-07-28 — the chat-law hook, carried to measured clean

Text read: `hooks/chat-law-hook.sh`, the paragraphs its `echo` lines speak. A hook runs this script
before every message a person sends, so these paragraphs enter the agent's context on every turn. The
reader of the text is the agent the text governs, so the reading asked one question: can an agent act
on these paragraphs without asking anyone what a phrase means?

The readers were fourteen fresh sessions holding nothing — no repository access, no history, no earlier
draft. Each was handed `docs/briefs/reader-prompt.md` word for word with the paragraphs pasted in.

**State reached: measured clean. Read clean is still owed.** The census reads zero. Fourteen readings
ran, and two consecutive readings with zero blocking stops never arrived. The floor sat at three
blocking stops, and the surviving stops are the three open questions at the end of this record.

---

## The measure

| moment | long | style | register | total |
|---|---:|---:|---:|---:|
| before, at commit HEAD | 9 | 4 | 1 | 13 |
| after | 0 | 0 | 0 | **0** |

The census scored the register reading at zero on the same text the register lint flagged once. The
census reads a finding count off a lint's JSON record, and `preshow-register-lint.py` prints no count
field, so its finding was counted as none. That gap is written up under the checks below.

Longest sentence before: 80 words. Longest after: 25.

## The mechanical findings, by class

- A sentence past the twenty-five-word cap. Nine of the seventeen prose sentences ran over; the
  routing law was one sentence of 80 words.
- An ordinary word shouted in capitals: `OPENS`, `SHOWN`, `IS`.
- The contrast frame written out in the law that bans it. The two example shapes stood as bare text,
  so the style lint read them as an instance rather than a quotation. They now sit in backticks, which
  the lint's scrubber passes over.
- A pack coinage shown raw: `pipeline station`, held by the register lint's `en-pipeline-station`
  pattern. The plain word is `pipeline step`, which is the spec's own vocabulary.
- One artifact under two names: `work item` where the one-name registry pins `backlog item`
  (`guardrails/one-name-aliases.json`).

## The readings

Fourteen readings, each by a session holding nothing. Blocking counts in order:

10, 7, 14, 15, 11, 12, 9, 8, 10, 4, 3, 5, 5, 6.

Total stops fell from 38 on the first reading to 27 on the last. The blocking count fell to three and
then stayed between three and six.

### What each reading found, in classes

**A term used with no path to its definition.** `pack`, `seat`, `wish`, `station`, `marker`, `home`,
`register`, `machine dialect`, `artifact`, `unit`, `turn`, `base rule`, `SPEC code`. Each was given
its definition in the sentence that first uses it, taken from the spec's glossary, the base skill, or
the personal profile.

**A file named with no path.** The queue, the resume file, the decision pages, the base rules, the
spec, the personal profile, and the skills all stood as bare names. Each now carries its path, and the
preamble states once that every relative path hangs off the project root.

**A rule that cannot be executed as written.** A narration line had to name the pipeline step with no
step list in reach; a marker had to be dropped with no marker defined; the register lint had to run
with no argument and no root. Each gained the missing piece from its source.

**A judgment with no measure.** `cheapest sufficient tier`, `lean`, `past a glance`, `judgment-flavoured`.
The routing law now states the one question that decides a tier, the three assignments that answer it,
and the sentence naming that outcome as the cheapest sufficient tier.

**Two rules sending one case to two places.** A read that understands in order to verify was claimed by
the dispatch rule and by the verify rule at once. The law now sorts each read by what the seat needs
back at the moment the read starts.

**A rule the text broke in its own sentences.** The reminder banned the contrast frame and then used it;
it banned a coined word from a sentence to the human and then permitted the same word untranslated in
the next law; it promised every law a closing home line and gave two laws none. Each was repaired, and
the ban now states its own boundary.

**A thing named by its number.** `base rule 5`, `SPEC INV-69`, `row numbers`. The preamble now names
the file each number lives in.

**A new class, from the ninth reading.** A mechanism named without the moment it runs and without the
consequence when it fires. Five scripts were named; two carried a trigger. Each now carries its actor,
its moment, and what its result does.

## What the fourteen readings say about the loop

The loop's rule is two consecutive readings with nothing blocking. On this text it did not converge.
Each fresh reader applies its own bar, and a reader that finds the previous reader's stops repaired
raises a fresh set on sentences the earlier reader passed over. The count of stops fell steadily; the
count of *blocking* stops flattened at three to six and stayed there.

Two properties of this text drive that. It is a compressed pointer to a large body of law it
deliberately does not carry, so a reader holding nothing will always meet a term whose full text lives
elsewhere. And it is a law text, where every unmeasured word is a rule the reader cannot apply, so a
stop that would read as non-blocking in a README reads as blocking here.

## Open questions for the owner

**1. How long is a reply allowed to run before the human has asked for more?** Every reading from the
fifth onward stopped on `going long past it waits for the human to ask`. The personal profile's
`language.answer-first` states the rule in those words and names no measure. No other source names one.

**2. How small is the file a glance may cover?** Base rule 25 bounds a glance to "one small file, or a
handful of targeted lines" and gives no number. Four readings called this the boundary that decides
whether a worker is spawned, and it is set by two unmeasured words.

**3. Do three reasons belong to the human, or four?** Base rule 29's prose names three: a taste, a
policy, and an act irreversible outside git. The mechanical arm the same rule names,
`guardrails/check-deferral-marker.py`, accepts four: taste, policy, irreversible, and device-feel. The
hook now states four, following the shipped checker. The two homes should agree, and the owner decides
which way. A second half of the same question: neither home defines `taste` or `policy`, and the law
requires every marker to name one of them.

## What the checks could have caught

Of the classes above, the census and its two lints caught five: the long sentence, the shouted word,
the written-out contrast frame, the pack coinage, and (through `check-one-name.py`) the two-named
artifact. They caught none of the rest.

Three findings a script could hold:

- **The census undercounts a register finding.** `scripts/rule-census.py` reads a count from each
  lint's JSON record and falls back to counting printed lines. `preshow-register-lint.py` prints a
  record with no `errors` field, so its findings count as zero while its own output names them. One
  register leak in this file was scored as none.
- **A term used with no path to its definition.** A script can hold the arm that matters here: a file
  read on its own that names a glossary term without naming the glossary. The term list already exists
  in `PRODUCT_SPEC.md`.
- **A named script with no trigger and no consequence.** A script path in a human-facing or
  agent-facing instruction, with no sentence nearby naming who runs it and what its result does, is a
  grepable shape.

The classes no script can catch: a rule that cannot be executed, a judgment with no measure, two rules
sending one case to two places, and a text breaking a rule it states. Each of those needs a reader who
holds nothing.

## The tests

Two phrases the tests quoted moved, and both tests were updated to the new phrase carrying the same
duty:

- `tests/test_chat_law_hook.py` — the narration needle `station` became `pipeline step`. The register
  lint's coinage arm retired the phrase `pipeline station`; the duty is unchanged, since every beat
  still names the step of the pipeline the work stands at.
- `tests/test_minor_gate_reconciliations.py` — `base rule 25 (the reading discipline, SPEC INV-137)`
  became `base rule 25 for the reading discipline (SPEC INV-137)`. The routing echo still names base
  rule 25 and INV-137 as its home.

Every other quoted phrase survives byte for byte, including `Answer first (live-spec)`, which
`guardrails/hook-red-proofs.json` requires the hook's output to contain.

The six files that quote this script — `tests/test_install_session_hooks.py`, `tests/test_judge_listed.py`,
`tests/test_config_health.py`, `tests/test_minor_gate_reconciliations.py`, `tests/test_chat_law_hook.py`,
`tests/test_check_hooks_can_fire.py` — run 43 green together, and did so before this work as well.

The full suite closed at `4 failed, 2231 passed, 1 error`. Every one of those four was red before this
work started, measured on the same tree with the pre-repair script restored: two in
`tests/test_config_health.py` and two in `tests/test_guardrails.py`. Another session held uncommitted
work across `tests/`, `guardrails/`, `scripts/` and `docs/` throughout, so the suite's totals moved
under it during the run.

## What was left undone

The installed copy at `~/.claude/hooks/chat-law-hook.sh` still holds the old text. Installing it is a
separate step, and `tests/test_config_health.py::TestConfigHealth::test_this_repo_installed_hooks_match_source`
reds until it runs. That test was already red before this work, on a drifted `text-audit` skill.
