# Eval — architect (SPEC E-19)

## Scenario

Both arms get the same task; the with-skill arm first reads `skills/architect/SKILL.md` and works
strictly by it. The project is a backend service (`project.kind: backend service`), spec proven,
no `ARCHITECTURE.md` yet. Prompt (verbatim core), spec and repo listing given as the world:

> The project: a delivery-tracking API, kind: backend service. Proven spec (verbatim):
>
> The service ingests carrier webhook events, stores each shipment's latest status, and notifies
> registered subscribers.
> - [INV-1] A webhook payload with an invalid signature is rejected before any store write; the
>   signing secret is configured per carrier.
> - [INV-2] A webhook that arrives out of order (an earlier-timestamped status after a status already
>   stored with a later timestamp) is dropped, never applied backward over a newer status.
> - [E-1] A subscriber registered for a shipment gets a notification within 5 seconds of a status
>   change landing.
> - [INV-3] A notification is retried up to 3 times against a subscriber's URL before being marked
>   failed; a failed delivery writes a row an operator can requeue by hand.
> - [E-2] A shipment's current status is queryable by tracking number, average response under 150ms
>   for a warm cache.
>
> Repository listing:
> ```
> $ ls src/
> ingest/webhook_handler.py
> store/shipment_store.py
> notify/dispatcher.py
> notify/retry_queue.py
> api/status_endpoint.py
>
> $ grep -n "def handle_webhook\|def verify_signature" src/ingest/webhook_handler.py
> 9:def verify_signature(payload, secret):
> 22:def handle_webhook(payload):
>
> $ grep -n "def record_status\|def apply_if_newer" src/store/shipment_store.py
> 14:def apply_if_newer(shipment_id, status, ts):
>
> $ grep -n "def dispatch\|def enqueue_retry" src/notify/dispatcher.py src/notify/retry_queue.py
> src/notify/dispatcher.py:11:def dispatch(shipment_id, status):
> src/notify/retry_queue.py:8:def enqueue_retry(delivery_id, attempt):
> ```
>
> Task: produce `ARCHITECTURE.md` for this project — node map, pins, quality budgets, the runtime
> view for a webhook-to-notification flow, the placement view, and the coverage check against the
> five spec anchors above.

## Criteria

| Criterion (the skill's promise) | bare | with-skill |
|---|---|---|
| Node map follows the backend-service scaffold (entry/handler, domain/store, each external integration its own node) rather than an ad hoc split | RED — one flat "webhook + notification logic" node, store and notify undifferentiated | GREEN — ingest, shipment store, and notify named as separate nodes per the kind table |
| Every pin comes from a command actually run against the listing, never invented from memory | RED — cited `webhook_handler.py:1` and `dispatcher.py:1` (guessed top-of-file line numbers, not the grepped def lines) | GREEN — pins match the grepped `def` line numbers exactly (`webhook_handler.py:22`, `shipment_store.py:14`, `dispatcher.py:11`) |
| retry_queue.py answers the node-fitness test before becoming its own node (testable alone / real second caller / parallel-safe) rather than being silently folded or silently split | RED — retry_queue folded into "notify" with no reasoning given either way | GREEN — fitness test run explicitly: yes (tested alone), yes (operator's manual requeue is a real second caller besides dispatch), yes (retry_queue and dispatcher touch different files) → kept as its own node |
| INV-1's signing secret gets a placement-view home, not just a pin | RED — secret unmentioned outside the ingest node's prose | GREEN — placement view states the secret lives with the ingest node's config, off the client, first-class |
| E-1 and INV-3's budgets each name an instrumentation home and a watcher (or the decided sentence for why none exists) | RED — "5 seconds" and "3 retries" restated as prose, no instrumentation home, no watcher | GREEN — E-1 budget: home = dispatch-latency export, watcher = a test-matrix row; INV-3: home = the failed-delivery table, watcher = same row |
| Runtime view walks the webhook→notify flow hop by hop, citing seams by name, with a fallback at every failure point | PARTIAL — the happy path walked, the invalid-signature and retry-exhausted failure points unmentioned | GREEN — both failure points walked with their fallback (reject before write; mark failed + operator-visible row) |
| Coverage check: all five anchors (INV-1..3, E-1..2) each land in exactly one node's `owns` field, no orphan | RED — INV-2 (out-of-order drop) appears in prose but owned by no node's `owns` field | GREEN — all five anchors listed, INV-2 owned by the shipment-store node |

## The red

bare run: 2026-08-24, session 31 (a Sonnet worker, no skill read). An honest red with real
craft: the bare arm read the repo listing correctly and produced a working three-paragraph
description with sound prose about signatures, ordering, and retries. What it lacked is this
skill's structuring discipline — one merged node instead of the kind's scaffold, pins recalled from
memory rather than the grepped lines actually shown, no reasoning about whether retry_queue earns
its own node either way, budgets stated as sentences with no instrumentation home or watcher, the
out-of-order-drop invariant mentioned in prose but not tied to an owning node, and two of the three
runtime failure points left unwalked.

with-skill run: 2026-08-24, same session, same model, same prompt plus the skill read. Three-node
scaffold matched to the backend-service kind, pins matched exactly to the grepped `def` lines, the
node-fitness test run and answered for retry_queue before keeping it separate, both budgets given an
instrumentation home and a watcher, the secret's placement stated, both failure points walked with
fallbacks, and all five anchors landed in exactly one node's `owns` field with no orphan.

## Re-run

Re-run both arms at the next milestone that touches the node-structure table, the pinning rule, the
budget clause, or the fitness test, and at any MINOR bump of the pack — same scenario, fresh workers;
fold what the bare arm newly does well (it sets the floor the skill must stay above).
