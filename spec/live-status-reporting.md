## Requirement 18: Anything shown to a person passes a register lint first

**Context:** Anything shown to a person passes a register lint before it is shown. The check reads the text for machine dialect — a coined internal metaphor shown raw, an English pack term calqued into another language, or a transliterated pack term. A red result blocks the showing until the text reads in the reader's own plain words.

**User Story:** As a person about to read a shown surface, I want its machine dialect caught and blocked before it reaches me, so that a coined metaphor or a calque never reaches my eyes as nonsense.

### Acceptance Criteria

**Case: the lint blocks the showing**

1. Before a human-facing surface is shown, the system *shall* have `scripts/preshow-register-lint.py` read its text and block the showing on a red result until the flagged text is rewritten into the reader's plain words. [INV-83]
2. The system *shall* treat this as a hard block, and *shall* scope its reach to the shown artifact — a rendered page, a mockup, a decision page, or a report page. [INV-83, INV-34]

**Case: the class the list cannot hold**

3. The system *shall* keep the literal pattern set as the free first pass and *shall* grow it by nobody's duty, since a growing list stays one escape behind the next word. [INV-83]
4. The system *shall* hand the residual machine-dialect class to the register judge, the model that reads meaning at the cheapest tier the routing rule names, standing as the ceiling the literal list cannot reach. [INV-83, INV-203, INV-69]
5. The system *shall* hold the chat line by the register judge's chat arm, the mechanical gate for the chat surface. [INV-203]

---

## Requirement 19: No line certifies its own sincerity

**Context:** No line certifies its own sincerity. A sentence that praises its author's honesty, directness, or diligence carries no information, since naming a quality informs only where its absence stood as a live alternative. The content carries the honesty; the label comes off.

**User Story:** As a person reading the pack's reports, I want a self-praising sincerity label stripped from every line, so that the honesty stays in the content rather than in a phrase that distinguishes nothing.

### Acceptance Criteria

**Case: the label comes off every surface**

1. The system *shall* strip a sentence that praises its author's honesty, directness, or diligence, since a report whose every line is meant to be true distinguishes nothing by saying so. [INV-94]
2. The system *shall* bind this across every surface — a shown artifact through the register lint, and the chat through the session's own read and the hook's reminder. [INV-94, INV-83]

**Case: the register judge holds the class**

3. The system *shall* have the register judge hold this class, a caught phrase informing the judge and the literal first pass while the pattern list grows by nobody's duty. [INV-94, INV-203]

---

## Requirement 20: The report law is walked as a live step

**Context:** The report law is walked as a live step each time, since chat has no suite to enforce it. Before any movement-end or milestone report reaches the person, the agent re-reads the communicator rules and passes the draft phrase by phrase through one question: does this sentence stand for a reader who does not live inside the pack?

**User Story:** As a reader outside the pack, I want every report walked phrase by phrase before it reaches me, so that a report I read lands understood rather than making me ask what a named surface is.

### Acceptance Criteria

**Case: the walk before every report**

1. Before any movement-end or milestone report reaches the person, the system *shall* re-read the communicator rules and pass the draft phrase by phrase through the outside-reader question. [INV-34]
2. The system *shall* explain any pack surface the draft names in the reader's own words or drop it, while quiet trailing anchors stay legal. [INV-34]
3. The system *shall* read a report that makes the reader ask what a thing is as the walk not walked, its acceptance belonging to the reader. [INV-34]

---

## Requirement 21: A question walks the same scan and one gate more

**Context:** A question to the person walks the same phrase-by-phrase scan a report walks, and one gate more, asked first: can I decide or verify this myself? A question that fails that gate is work, done instead of asked. A question that survives it arrives with its recommendation attached.

**User Story:** As a person asked only what I alone can settle, I want every question gated by can-the-agent-decide-this-first, so that a question the agent could answer itself becomes work done and a surviving question arrives with a recommendation.

### Acceptance Criteria

**Case: the scan and the extra gate**

1. Before any question is asked — in a report's batched tail, on a decision page, or as a lone ask in chat — the system *shall* pass it through the same phrase-by-phrase read, every term grounded in the reader's own words. [INV-81, INV-34]
2. The system *shall* ask first whether it can decide or verify the answer itself, and *shall* turn a question that fails that gate into work done rather than asked. [INV-81, INV-4, INV-5]
3. The system *shall* have a question that survives the gate arrive with its recommendation attached. [INV-81, INV-60]

---

## Requirement 22: Work is narrated while it runs

**Context:** Work is narrated while it runs, the third voice between the capture echo and the delivery report. The person leads many windows at once, so otherwise silence is all they get. While work runs, the agent says each beat worth a sentence — a stage passed, a load-bearing find, a change of direction — in the roadmap's terms and the reports' voice.

**User Story:** As a person leading many windows, I want each beat of running work narrated in plain roadmap terms, so that a silent stretch never reads to me as lost work.

### Acceptance Criteria

**Case: beats are narrated as they happen**

1. *while* work runs, the system *shall* say each beat worth a sentence in one or two plain sentences in the roadmap's terms, and *shall* keep the mechanical grind quiet. [INV-35]
2. The system *shall* name in every beat the work it belongs to — which wish is in hand and which pipeline stage it stands at, and whether it mends something broken or builds something new. [INV-35]
3. *when* a station completes, the system *shall* make its line a beat carrying a short digest of what the station produced in the work's own words. [INV-35]

**Case: the heartbeat and the detached run**

4. *when* a stretch runs long with no beat, the system *shall* say what is grinding and why the stretch runs long, owing this heartbeat past a beatless stretch of about 10 minutes as a default. [INV-35]
5. *when* an operation runs detached past about 2 minutes, the system *shall* open with a start line naming what runs, where its log lives, and an honest range, keep a beat landing about every 2 minutes or at each stage, and close with a done digest. [INV-35, INV-93]

**Case: the offline window**

6. *when* the coming stretch needs nothing from the person, the system *shall* say so before it starts — that the person may step away, an honest range for how long, and what the person is needed for at its end — stating an unknown duration as unknown. [INV-35]
7. *when* the person is needed again, the system *shall* say so plainly as a beat naming the gate or decision that waits, batching questions born inside the window to its end. [INV-35, INV-4]

**Case: narration is chat-register**

8. The system *shall* keep a narration line an informal chat message that walks no pre-report walk, asks nothing, and replaces no report, while every human-facing-line law still binds. [INV-35, INV-27, INV-28]

**Case: the delegated beat and the time accounting**

9. *when* a delegated worker closes a station, the system *shall* fold it into the trail, a station a delegated worker closed becomes the senior's beat the moment it lands, the trail the session's time accounting where token and test counts stay bookkeeping. [INV-35, INV-28]

**Case: the offline window's honest edges**

10. *when* the offline window runs, the system *shall* keep its edges honest, never a guess dressed as a promise, a window off its spoken range saying so, overrun, done sooner, or blocked on the human's word alone, the needed-again beat a chat line awaiting his return, never a summons, and no offline sentence fires when the very next beat needs the human. [INV-35, INV-4]

---

## Requirement 23: Every ask hears its price in time, and the landing settles it

**Context:** Every ask hears its price in time, and the landing settles it. The capture echo carries an honest time range read from the work's known shape or observed runs, an unknown stated as unknown. Work expected to run an hour or more is explained up front in plain steps. The delivery report states the estimate beside the actual.

**User Story:** As a person who owes time to a task, I want an honest range at capture and the estimate settled against the actual at landing, so that I know what a task costs before it starts and how the guess held afterward.

### Acceptance Criteria

**Case: the range at capture and the settling at landing**

1. The system *shall* carry in the capture echo an honest time range read from the work's known shape or observed runs, stating an unknown as unknown. [INV-93, INV-27, INV-35]
2. *when* work is expected to run an hour or more, the system *shall* explain it up front in plain steps — what has to happen and why it takes that long — and *shall* say on the heartbeat how much time remains as the stretch runs. [INV-93, INV-35]
3. *when* a wish lands, the system *shall* state the estimate beside the actual in the delivery report, saying an overrun or an under plainly. [INV-93]
4. *when* a direct command holds the session for more than a beat, the system *shall* have it hear its range even though it registers no row. [INV-93]
   [GAP: the beat's duration for a direct command's range announcement is unstated in the source.]

---

## Requirement 24: A rewrite that removes substance accounts for it

**Context:** A rewrite that removes substance accounts for it in the delivery report. A restyle or a restructure drops content as it tightens, and some of what it drops carries weight — a section, an argument, a rationale, a worked example. The rule scopes to substance and leaves line-level wording free.

**User Story:** As a person whose document a rewrite tightened, I want every removed piece of substance accounted for in the report, so that deleted content is kept and cited, killed by my own word, or raised as a question rather than cut silently.

### Acceptance Criteria

**Case: every removal is accounted for**

1. *when* a rewrite or restyle removes substance — a section, an argument, a rationale, or a worked example — the system *shall* list every removal in the delivery report with one line of judgment each: the fact was kept and where, the person killed it by name, or the rewriter proposes dropping it and asks. [INV-109]
2. The system *shall* turn a removal the rewriter cannot justify into a question before the report closes, and *shall* not cut substance silently. [INV-109]

**Case: line-level wording stays free**

3. The system *shall* scope this accounting to substance and *shall* leave a tightened sentence or a reordered clause needing no account. [INV-109]

---

## Requirement 25: One spoken leave-word winds the session down to a safe stop

**Context:** One spoken leave-word winds the session down to a shutdown-safe stop. When the person says they are leaving, the session stops taking new work and walks what is open to a safe point: background workers halt or run to their landing, every open lane reaches its checkpoint, green work is committed under its gates, and the resume file says what resumes where.

**User Story:** As a person about to close or sleep the machine, I want one leave-word to bring the session to a shutdown-safe stop, so that no worker dies mid-write, no red work is committed, and I am told plainly when it is safe to power off.

### Acceptance Criteria

**Case: the wind-down to a safe point**

1. *when* the person says they are leaving, the system *shall* stop taking new work and *shall* halt background workers or run them to their landing, recording any worker that cannot halt in time by the handoff discipline — a note carrying the worker's id, the exact files its brief lets it write, and the liveness checks a resuming session runs before touching them. [INV-95, INV-76]
2. The system *shall* bring every open lane to its checkpoint, committing green work under its standing gates and committing no red work, with the failing test name and hypothesis topping the resume file. [INV-95]
3. The system *shall* have the resume file say what resumes where. [INV-95]

**Case: the closing line and its timing**

4. The system *shall* answer in the first beat roughly how many minutes remain to the safe point, and *shall* give as its last a single closing line — safe to power off, plus what resumes where on return — said only *when* every point above holds. [INV-95, INV-93]
5. The system *shall* ride the remaining-minutes habit on long work even before any leave-word, and *shall* never guess from silence that the person is leaving. [INV-95, INV-35]

---

## Requirement 26: Anything handed to the person opens with a one-line identifier

**Context:** Anything handed to the person opens with a one-line identifier. A page that opens in the browser states two things: which project it belongs to, and whether it needs the person's attention. A page that states neither reads as noise.

**User Story:** As a person who finds a page open in my browser, I want it to name its project and say what it needs of me, so that I always know what I am looking at and what it asks.

### Acceptance Criteria

**Case: the identifier states project and need**

1. The system *shall* show the project's name in a handed page's visible content, not only in its URL. [INV-51]
2. The system *shall* state what the page needs from the person — a word, with what and by when, or that it is only an update with no action. [INV-51]
3. The system *shall* lead every handed or opened artifact — a report page, a decision page, a rendered doc, or a standing rendered surface the person opens — with that identifier, and *shall* carry the same two facts in the chat line that announces it. [INV-51]

---

## Requirement 27: During an away-stretch, artifacts accumulate on one page

**Context:** During an away-stretch, artifacts accumulate and one window opens at the end. When the person has stepped away for an overnight loop or an offline window, the agent does not open a browser window mid-stretch. Artifacts accumulate on one page.

**User Story:** As a person who stepped away, I want artifacts gathered on one page that opens once at the end, so that an overnight stretch never scatters windows across my screen.

### Acceptance Criteria

**Case: one page for the away-stretch**

1. *while* the person is away for an overnight loop or an offline window, the system *shall* not open a browser window mid-stretch and *shall* accumulate the stretch's decisions and report on one page. [INV-52, INV-35]
2. The system *shall* allow a mid-stretch re-open only as that same page refreshed in place. [INV-52]

---

## Requirement 28: The showing channel matches where the session runs

**Context:** The showing channel matches where the session runs. A session on the person's own machine shows a rendered artifact as a local page in a browser window. A remote session runs in the cloud, is read through a browser, and cannot open a local page, so it shows the same content through its own channel.

**User Story:** As a person reading a session that may run locally or in the cloud, I want it to show through the channel its seat can reach, so that a remote session never hands me a local file path that opens into nowhere.

### Acceptance Criteria

**Case: the seat picks the channel**

1. The system *shall* read where the session runs from what it can reach — the platform, the display, and whose filesystem it sees — and *shall* name the channel it picked. [INV-67]
2. The system *shall* show a local session's artifact as a local page in a browser window, and *shall* show a remote session's artifact through its own channel — an artifact page the host renders, or the chat itself — carrying the same identifier and the same round-trip. [INV-67, INV-51]
3. The system *shall* re-read the seat after any move between machines, and *shall* read handing a local file path to a remote reader as a defect of the exchange. [INV-67]

---

## Requirement 29: The current state of the work is answerable in any setting

**Context:** The current state of the work is answerable at any moment, in any setting. The harness's own task panel and activity line are a convenience of the local terminal, absent in a browser and stalling on a long run of tool calls. So the live status lives in the chat, the one surface present in every setting.

**User Story:** As a person who looks in at any moment, I want the work's state kept current in the chat, so that a glance answers what we are working on and what comes next whatever setting I read from.

### Acceptance Criteria

**Case: the status lives in the chat**

1. The system *shall* keep a short status current in the chat — a Now line naming the work in hand and its pipeline stage, and a Next line naming what the queue holds next. [INV-71, INV-67]
2. The system *shall* refresh the status at every stage change and *shall* carry a heartbeat on a long stretch. [INV-71, INV-35]

**Case: the harness panel is a courtesy view**

3. The system *shall* keep the harness task panel, where a setting shows it, in plain product words as a courtesy, and *shall* not make it the home of the status. [INV-71, INV-28]
4. The system *shall* offer a rendered status page as an optional richer view of the same Now and Next on a local session, and *shall* apply this to every project the pack runs. [INV-71, INV-67]

---

## Requirement 30: The end of a stretch is delivered so the person cannot miss it

**Context:** The end of a stretch is delivered so the person cannot miss it. A report that exists but sits above tool noise counts as undelivered. When a stretch ends, the last rendered thing is one short final line.

**User Story:** As a person who might miss a report buried above tool output, I want one short final line as the very last thing rendered, so that I can never miss where the run ended.

### Acceptance Criteria

**Case: the final line comes last**

1. *when* a stretch ends — a loop iteration going to sleep, an away-stretch closing, or a session ending — the system *shall* render as the last thing one short final line carrying what closed, what is next, what is needed from the person, and when the agent wakes. [INV-57]
2. The system *shall* place the long report above that line and *shall* render the final line last, after every tool call. [INV-57]
3. The system *shall* repeat a page deliverable's identifier in that final line. [INV-57, INV-51]

---

## Requirement 129: Human-facing prose is drafted by a clean writer

**Context:** Any text a human will read is drafted by a fresh writer session that does not have the package rules loaded — documentation pages, product-spec prose, reports, decision pages, product copy, and the package's own rule texts while being edited. The rules-loaded session writes a plain brief carrying the facts, the reader, and the register laws; the writer returns the draft; the rules-loaded session reviews and lands it. A blanket rewrite of settled text is refused.

**User Story:** As a person reading the pack's durable prose, I want it drafted by a fresh writer from a plain brief, so that human-facing writing stays clear of the insider register and settled text stays stable.

### Acceptance Criteria

**Case: the clean-writer road**

1. *when* durable human-facing prose is written or a section of it is edited, the system *shall* have a fresh writer session draft it from a plain brief carrying the facts, the intended reader, and the register laws, then review and land it in the rules-loaded session. [INV-84]
2. The system *shall* bind the road to the section the edit touches and *shall* redraft a whole page only on the human's word. [INV-84]

**Case: what rides the ordinary hand**

3. The system *shall* let a report typed live in chat stay the session's own words under the register laws, and *shall* let a mechanical correction ride the ordinary hand as no drafting. [INV-84]
   - a mechanical correction is a typo, a broken link, or a version number.
4. The system *shall* refuse a blanket rewrite of settled text, since meaning can shift during a bulk restructure. [INV-84]

---

## Requirement 236: Every point of contact with the person has a kind

**Context:** A moment of contact is synchronous when the person is present and the work waits on the person, and asynchronous when the person reads on the person's own clock while the work keeps running. The kind licenses the traffic: an interruption belongs on a synchronous point, a teaching line on a point the person opens, and waiting traffic on every point. Each touchpoint declares its kind in one manifest, and a gate reds a surface that speaks in a kind its touchpoint lacks.

**User Story:** As a person met by the pack at many points, I want each touchpoint's kind declared and enforced, so that an interruption never rises from a point I read on my own clock and a teaching line only reaches a point I opened.

### Acceptance Criteria

**Case: the kind licenses the traffic**

1. The system *shall* declare each touchpoint's kind in the manifest `guardrails/touchpoints.json`, holding whether the person opens it and what traffic it affords. [INV-205]
2. The system *shall* afford an interruption only on a synchronous point, a teaching line only on a point the person opens, and waiting traffic on every point. [INV-205]

**Case: the gate reds a mismatch**

3. *when* a surface speaks in a kind its touchpoint lacks — an interruption from an asynchronous point, or a teaching line on a point the person did not open — the system *shall* red it. [INV-205]
4. *when* a surface interrupts through wording the marker cannot read, the system *shall* leave the declaration to the author, the same bound the cleanup-notice and muted-launch nets keep. [INV-205, INV-204, INV-157]

---

## Requirement 237: The waiting board outlives the scroll

**Context:** Chat is a display and it scrolls, so a question parked for the person and an answer the person never saw both evaporate. One small file at the host root, the waiting board, holds them, and chat renders it on occasion. An item clears on the person's acknowledgement alone and is never auto-expired, since expiring an item the person never read is a silent loss.

**User Story:** As a person who reads on my own clock, I want everything waiting for me kept in one board that never auto-expires, so that a parked question or an unseen answer is there when I open it, held safe from the scroll.

### Acceptance Criteria

**Case: the board holds what waits**

1. The system *shall* hold every item waiting for the person in the board `WAITING.md`, and *shall* clear an item on the person's acknowledgement alone. [INV-206]
2. The system *shall* never auto-expire an item, moving a superseded one to the attic with a manifest line rather than deleting it. [INV-206]

**Case: the shown cap and its demotion**

3. The system *shall* show at most 12 items to the person at once, and *when* a new item arrives to a full shown set *shall* demote the oldest shown item into the list below, whole. [INV-206]
4. *if* a thirteenth item stands in the shown set, *then* the system *shall* read it as an over-cap defect. [INV-206]

**Case: the gate reds a silent loss**

5. *when* a closing report omits a still-open board item, or an item is demoted with no matching line, or the shown set runs over cap, the system *shall* red the board gate. [INV-206]

---

## Requirement 239: The far backlog surfaces itself rarely and unasked

**Context:** Answering when the person asks is the far tier's floor; above it, the tier shows itself on its own once in a while, so a thought parked there is met again without the person having to remember it exists. The status report carries a rare line naming that a far backlog is kept, at a cadence that is a settings-ladder default, and records the last self-surfacing so the window is readable.

**User Story:** As a person keeping a far backlog, I want it to surface itself rarely and unasked on a report I already read, so that a parked thought returns to me without waiting on my memory and without a second offer inside its window.

### Acceptance Criteria

**Case: the rare self-surfacing**

1. The system *shall* answer the far tier when the person asks, and above that floor *shall* carry a rare status-report line naming that a far backlog is kept. [INV-222, INV-223]
2. The system *shall* propose at most one such offer per 14 days as a settings-ladder default, movable by the person's word, and *shall* record the last self-surfacing in a dated marker. [INV-223, E-13]

**Case: it rides an asynchronous point**

3. *when* the far-tier line rides the status report, the system *shall* treat it as an asynchronous touchpoint that may only wait, holding the entry `far-tier-surfacing` in the manifest. [INV-223, INV-205]
4. *when* a second offer would fall inside the last surfacing's window, the system *shall* red the report-shape check, and *shall* pass a first offer once the window has passed. [INV-223]

---

## Requirement 240: A release note may offer the reader next-step choices

**Context:** A release note is a surface the person opens on the person's own clock, and on it the pack may offer appealing things to do next, phrased as free choices. The offers section is optional, so a release with no worthwhile next step owes none; what the walk owes is a recorded decision, so the offer-or-none choice is never silently skipped.

**User Story:** As a person reading a release note, I want the pack free to offer me next steps and made to record whether it did, so that a worthwhile choice reaches me while the offer-or-none decision is never silently skipped.

### Acceptance Criteria

**Case: the recorded offer-or-none decision**

1. *when* the publish walk prepares a release note, the system *shall* record the offer-or-none decision on the note, carrying the optional offers section. [INV-228]
2. *when* a release-note record neither offers a next step nor records a no-offer marker, the system *shall* red the release-note check, and *shall* pass a record that offers a choice or records none by name. [INV-228, INV-83]

**Case: it rides an asynchronous point**

3. The system *shall* treat the release note as an asynchronous, person-opened touchpoint that affords an offer and not an interruption, holding the entry `release-note` in the manifest. [INV-228, INV-205]

---

## Requirement 257: A delivery that closes a roadmap row refreshes the forward map

**Context:** The movement-end report law asks the seat to refresh the forward map and report after every big movement without being asked; left as once-read prose it fired only on a reminder. Its checkable face is a commit: a delivery is a commit that moves a roadmap row from the queue's body to the archive with its status naming *landed* and its date, and such a commit that does not also touch the forward map reds. A commit that closes no row is not a delivery and owes nothing.

**User Story:** As a person relying on an up-to-date forward map, I want a delivery commit made to refresh the forward map in the same breath, so that a movement that ends never leaves the map stale.

### Acceptance Criteria

**Case: a delivery commit refreshes the map**

1. *when* a commit's diff moves a roadmap row from the body to the archive with its status naming *landed*, the system *shall* require the same commit to touch `NEXT_STEPS.md`. [INV-242, INV-276]
   - the commit range is read through the same base ladder the other range checks use: the declared base, then `origin/main`, then the previous commit.
2. *if* such a delivery commit does not touch the forward map, *then* the system *shall* red and name the one fix. [INV-242]

**Case: what is not a delivery owes nothing**

3. The system *shall* leave a commit that closes no row, and a row closed to *declined*, *deferred*, or *superseded*, owing no refresh. [INV-242]
4. *when* the push-gate letters are exhausted, the system *shall* ride this check on the suite, so a red here reds the suite gate and blocks the push. [INV-242, INV-222]

**Case: a missed landing heals forward**

5. *when* a landing commit misses the refresh, the system *shall* let a later commit in the same range heal it. The healer *shall* touch `NEXT_STEPS.md` and name the missed landing by its commit id. A heal predating its landing heals nothing, and the system *shall* warn rather than red once healed, keeping the miss on record. [INV-242]

## Requirement 293: A naked internal code in live prose reds

**Context:** The plain-language law asks a human-facing sentence to stand in the product's own words, with an internal handle — a queue row number, a spec code — trailing in parentheses for a reader who wants to follow it. A sentence that leads with a bare handle gives the reader a number he has no way to resolve. The law had no machine and decayed for want of one, so a Stop-hook scan now reads the turn against it and asks for the naming in plain words one message later.

**User Story:** As a person reading the seat's replies, I want an internal code left standing outside its anchor flagged, so that the sentence comes back in plain words I can resolve on sight.

### Acceptance Criteria

**Case: a code outside its anchor reds**

1. *when* any message the seat showed since the last human turn carries an internal code — a queue row named by its number in either working language, or a bracket code the documents use — standing outside a trailing anchor, the system *shall* block the stop and ask for the naming in plain words one message later. [INV-283, INV-28]
2. The system *shall* pass a code sitting inside parentheses or square brackets, the lawful trailing anchor the plain-language law names. [INV-283, INV-28]

**Case: a code the sentence talks about**

3. The system *shall* pass a code inside a fenced block, an inline backtick span, or a quoted span, and *shall* pass a table row, whose neighbouring cell carries the plain words. [INV-283]
4. The system *shall* read a naming word and the number it carries, so a bare number with no naming word before it passes. [INV-283]

**Case: honest about its reach**

5. The system *shall* judge only whether a code was left standing outside an anchor, and *shall* leave whether the plain words that replace it are the right words to the person. [INV-283]

**Case: the code forms the scan reads**

6. The system *shall* read a document's own name run against a number as a code standing outside its anchor, a form handing the reader a location he can resolve only by opening the document. [INV-283]
7. The system *shall* read a multi-letter code spoken with a space as the equal of its dash form, and *shall* hold the multi-letter form and the single-letter dash form to the capital shape the documents write them in. [INV-283]
   - an ordinary word carrying a letter and a number in lower case passes.
8. The system *shall* pass a naming word and its number *where* the same line carries a file name or a file word, the shape a reference to a line inside a source file takes. [INV-283]

---

## Requirement 294: Empty validation aimed at the person reds

**Context:** A line telling the person he is right, praising his question or his intuition, or framing the seat's own work as superior costs the reader attention and returns nothing: the reply owes the finding or the act, and nothing else leads before them. The rule stood as a personal setting with a machine behind it on one host alone. The pack ships that machine as a Stop-hook scan in the two-tier shape the scissors scan carries, a universal list plus a host's own overlay.

**User Story:** As a person reading the seat's replies, I want an empty validation line caught, so that a reply opens with the finding and never with praise for the person who asked.

### Acceptance Criteria

**Case: the validation gate**

1. *when* any message the seat showed since the last human turn carries an empty-validation phrase, the system *shall* block the stop in the after-the-fact shape the scissors scan and the hedge gate take. [INV-284, INV-238]
   - the scan strips a quoted, backticked, or fenced span from the message before it matches the pattern list.
2. The system *shall* match against an inline universal pattern list plus an optional personal-overlay file a host tunes, as the scissors scan carries one, and *shall* stand on the universal list alone *where* the overlay is absent or unreadable. [INV-284, INV-203]
3. The system *shall* catch only the phrases it lists, so a paraphrase it does not carry stays with the register judge that reads the class in meaning. [INV-284, INV-203]

**Case: shipped as a pack hook**

4. The system *shall* install the scan by the setup walk beside the scissors scan, *shall* have it covered by the config-health check and classified in the wired-hook declaration, and *shall* have its runs and fires read by the net-liveness meter. [INV-284, INV-173, INV-175, INV-211, INV-202]


---

## Requirement 310: A work block is grounded in the person's sight before it runs

**Context:** Sessions entered long work blocks the person could not connect to any request of theirs. A block and every line reporting it open by naming their root, so the person can correct the state by eye.

**User Story:** As a person leading the work, I want every work block and report line to open by naming the request it serves. Then I can judge at a glance why the session does what it does.

### Acceptance Criteria

**Case: the root is named before work runs**

1. *when* a work block starts, the system *shall* open it by naming its root beside the pipeline stage, the demanding rule, and the estimate. [INV-314]
2. A root *shall* be the person's dated request, a standing instruction of theirs, or a reason stated plainly enough for the person to judge. [INV-314]
3. The system *shall* start no work block whose root it cannot name. [INV-314]
4. The system *shall* name no machinery — an alarm, a gate, a scheduled reminder — as a root. [INV-314]
5. The system *shall* name instead the person's instruction the machinery carries. [INV-314]

**Case: reports carry the same root**

6. The system *shall* open every report line with its block's root, and *shall* count a report line missing its root a defect. [INV-314, INV-28]

**Case: a step outside the plan**

7. *when* a running block is about to step outside its announced plan, the system *shall* stop. [INV-314]
8. The system *shall* announce the out-of-plan step and its root before taking it. [INV-314]

**Case: the plan is the account**

9. The system *shall* keep each task's plan as the home a block is announced against. [INV-314, INV-308]
10. That home *shall* be the work board's per-task plan once the board ships, and the written plan page until then. [INV-314, INV-308]
11. The system *shall* account each block against its plan line in the delivery report. [INV-314, INV-103]


