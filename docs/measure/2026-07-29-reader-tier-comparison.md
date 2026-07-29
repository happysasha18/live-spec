# The cheap reader against the strong reader — 2026-07-29

## The answer

A cheap reader misses places two strong readers agree on, and it finds real places neither strong
reader reaches. It replaces a strong reader nowhere. It earns a seat beside one.

The recommendation: run each round as one strong reader and one cheap reader, and keep counting a
place against the text when both stopped there. Agreement across two tiers carries more than
agreement inside one, because two readers of one tier share one bias.

## What was measured

Three readers read `skills/text-audit/SKILL.md` and its two companion files on the same version, each
holding only those files and the same list of questions. Two ran on the strong tier and one on the
cheap tier. Their records are readings 27, 28 and 29 under `docs/language-reads/`.

| reader | tier | stops | blocking |
|---|---|---:|---:|
| 27 | strong | 37 | 6 |
| 28 | strong | 41 | 8 |
| 29 | cheap | 28 | 3 |

## What each tier found

The two strong readers agreed on three places:

- one fact recorded in two files, with no division of labour stated between them;
- the build-test paragraph describing a measurement, with the next paragraph stating that no record
  stands behind any build test;
- an instruction pointing at the body's definition of a blocking finding, where the body carries two
  such definitions.

The cheap reader found one of those three: the build-test contradiction, which both strong readers
also found. So the cheap reader reached a third of the agreed set.

The cheap reader found two places neither strong reader named, and both are checkable against the
text:

- the skill assigns design review to one sibling skill, and the closing list assigns it to another;
- one of the four checks after a repair names a second reader who sits in none of the three roles the
  document defines.

## What this changes

The campaign plan says one tier is chosen after this measurement, and the measurement answers a
different question. Neither tier covers the other.

Cost falls anyway. A round of one strong reader and one cheap reader costs less than two strong
readers, and this measurement shows it loses no coverage the agreement rule uses.

The next document tests that shape: run round one as a mixed pair, and compare its agreed set against
the five rounds of same-tier pairs recorded for this file.
