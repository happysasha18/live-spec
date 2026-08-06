# Rotated ROADMAP rows — 2026-08

> One calendar month's closed rows gather here; the live queue stays lean and these rows stay grepable by number. A row's presence here certifies its terminal exit — landed, decided, declined, or superseded stands in its status cell.

| # | Wish (plain words) | Class | Status | Decision / acceptance |
|---|---|---|---|---|
| 571 | **A clean tree reads green at any hour** (cost audit repair b; the after-midnight reds fired their third time at the 00:20 run): the record-freshness check demanded a record dated today, so a clean tree red after midnight until the day's first review record existed. The work road now accepts the newest committed record while it stays fresh for the guarded documents. The push road keeps demanding today's record, per his recorded line. | bug | landed 2026-08-07, the night session's repair commit | Done when a clean-tree run after midnight exits green — met: the 01:15 run shows the after-midnight reds gone |
| 573 | **The suite stops paying for itself twice on ordinary runs** (cost audit repair a): the scratch self-run guard re-fired on every work run while any unpublished commit touched the checks folder, 134 seconds each time. A green self-run now records the checks' content digest and skips while the digest stands. Any changed byte of the machinery re-fires it; a missing record runs it. | bug | landed 2026-08-07, the night session's repair commit | Done when an ordinary run with unchanged machinery skips the self-run by name and a machinery edit re-fires it — met by the digest tests |
