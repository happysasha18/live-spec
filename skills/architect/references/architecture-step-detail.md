# The architecture step in detail

The three long passages of `SKILL.md`'s architecture step, referenced from the step itself. Every line
below reads exactly as it read in the body.

## What is measurable comes from the project's kind (SPEC INV-36)

WHAT is measurable comes from the project's KIND (SPEC INV-36): ask "what does quality MEAN here, in
numbers?" before writing any. A user-facing product measures paint/interaction times ("first image
within 2 s on a cold visit"); a backend service latency, throughput, error rate; a CLI or pipeline run
time on a typical input and per-unit cost; a skill pack its evals' pass rate and suite wall-time; prose
what honestly HAS a number. A quality with no honest number is SAID by name, never given a vanity metric.

## The runtime view and the placement view (SPEC INV-74, INV-75)

**The doc owes two more views beside the node map (SPEC INV-74, INV-75), scaled by kind:** the
**runtime view** walks every flow the spec promises through the nodes — which node serves each step,
what crosses each hop (citing the seam by name; the payload and format stay the seam table's fact),
where the flow can fail; a flow the doc cannot walk end to end is a finding. The **placement view**
states every node's place — build-time on the author's machine · CDN static · client browser · edge
worker · external service — plus the load-bearing technology choice where one exists, first-class (a
node-table column or its own small table), so the reader answers "where does this run" at a glance.
The per-kind flow unit and both section shapes live in the template; a book satisfies each view with
one sentence.

## The three-question fitness test (SPEC INV-122)

The three questions themselves, and how one no and two nos are read, stand in `SKILL.md` at the
architecture step: they are the test's firing condition and belong where the step is walked. What
follows is where the test lives and what a failed carve costs.

The
test's first home is here, the architecture step, where new abstractions are born; a carve that fails it
is folded back into its caller until a real second need or a real testability gain arrives. Its second
home is product-prover, extending the speculative-node flag: a node with one caller and no promised
second is flagged for that answer (the one-no case), never auto-rejected.
