What is to be done: Fix two release-process bugs found in the last push — a hook file the installer never lists, so it goes stale and fails a health check, and a worker-admission rule that blocks a review because it only allows starting on a still-open row — then bump the version to 6.1.1 with a migration note.
Why: Both faults stopped the last push and had to be worked around by hand, so fixing them keeps the next push from costing a hand.
How long: 2 to 4 hours, as stated in the paragraph.
Echo-name placed: Hook drift and admission window
