# Movement durations — the record a forward estimate is read from

Opened 2026-07-27 on Alexander's word: measure and record how long each movement took, so the forecasts
get more accurate over time. The promise half lives in queue row 471 — a report carries a forward estimate
and a landing carries promised against actual. This file is the measurement half those two numbers come
from.

**How a line is written.** One line per movement, appended when the movement lands, never edited
afterwards. `Promised` is the estimate given in the report that opened the work, in the same units it was
given. `Actual` is wall-clock time from the first act of the movement to its landing commit, read from the
git log rather than from memory. A movement that ran across a break records the working stretches only,
and says so in its note.

**How the estimate is read back.** Before promising a time, read the lines whose size matches. The ratio of
actual to promised across the matching lines is the correction factor for the new estimate. Three lines of
a size are enough to state a range; fewer than three is stated as a guess with its thin evidence named.

**What is missing.** Every movement before 2026-07-27 shipped without a measurement. The journal carries
their dates, and a few carry their hours, so a backfill is possible for the large ones and is worth doing
only if a forecast needs it. Nothing here is reconstructed from memory.

| Date | Movement | Size | Promised | Actual | Note |
|---|---|---|---|---|---|
| 2026-07-27 | Suite runtime reading for the tlvphotos window (read-only audit, deposit written) | small | none given | 8.7 min | one reader worker, two trees, 94 suite files; the deposit was written by the lead afterwards |
| 2026-07-27 | Full live-queue sweep, 113 rows classified | small | none given | 6.4 min | one worker, read-only; the estimate that mattered was the row count, guessed at 95 against an actual 113 |
| 2026-07-27 | README opening sample, first draft by a clean writer | small | none given | 1.6 min of work, 12 min of wall clock | the first attempt died on a dropped connection and was relaunched; the note stands as the reason wall clock and work time differ |
| 2026-07-27 | Intake of the morning's ten asks: seven new rows, two widened, tags retired, three commits | surface | none given | 46 min | the intake ran while new asks kept arriving, which is the normal shape of a live intake rather than an interruption |
