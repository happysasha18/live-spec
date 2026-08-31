# Feature names retired from the roster, 2026-08-31

The roster is the list of names the product gives a person for the things it does. It is the tags
`[feature: F-...]` on requirement headings in the spec, and the coverage table in
`architecture/feature-coverage.md` that maps each name to the nodes implementing it and a test
exercising it. Seventeen names stood on it. Six leave here, and one arrives that is not in this file.

Nothing was deleted. Every requirement below still stands in the spec, with its criteria unchanged
except where this file says otherwise. What left is the NAME, and a name comes back the moment the
thing it names is something a person can be given.

## Two names that stood on nothing

A name says the product gives a person this thing. Both names below stood on a requirement that also
carried the `[target]` marker, which says the thing is specified and not built. A reader met the name
and believed the thing; the coverage table then had to name a node and a test for a surface that does
not exist, and one of them did that by borrowing its neighbour's test.

- `F-contract` -> Requirement 194, `spec/public-contract.md` * a published contract read on the
  reader's own clock. No agent on this machine has ever published one: the pack's own card and the
  photo site's card each say, in their own words, that they publish none, and no contract artifact
  exists in either tree. The requirement's own criterion 15 holds its enforcing gate promised "until
  a host's first real contract". Its named test asserted that the requirement's sentences were still
  in the spec file and nothing else. * 2026-08-31
- `F-work-board` -> Requirement 309, `spec/work-board.md` * the standing page showing the whole queue
  in columns. The page, its source file, its generator and its statement-validation check are all
  specified and none is built; the requirement's heading carries the `[target]` marker, the
  architecture node carries it too and pins no code, and every one of the twenty-six matrix rows
  reads *todo*. The coverage row named `test_capture_echo_and_board`, which belongs to `F-wish` and
  exercises the capture echo the board would grow out of. * 2026-08-31

A rule now holds this class rather than these two instances: a feature name stands only on a scenario
the product performs today, and `tests/test_traceability.py` reds a tagged requirement that also
carries the `[target]` marker (Requirement 224, INV-132; the rule's home moved with it).

## Four names for one thing a person is given

Five names described five entry conditions into one procedure — attaching the pack to a project. All
five named the same architecture node, `attach`, and the architecture had already written them as one
responsibility. They converge on `F-attach`, whose coverage row names every test that exercises one of
the entries, so nothing that was proven stops being proven.

- `F-bootstrap` -> `F-attach` * Requirement 169: attaching to an empty tree * 2026-08-31
- `F-adoption` -> `F-attach` * Requirement 177: attaching to a project already running * 2026-08-31
- `F-catchup` -> `F-attach` * Requirement 180: re-attaching a project to a newer pack * 2026-08-31
- `F-pair` -> `F-attach` * Requirement 187: attaching to two repositories taken as a pair * 2026-08-31
- `F-onboarding` -> `F-attach` * Requirement 186: the settings card that closes any of the four, and
  which fires only when founding ends or adoption's orient ends, so it has no trigger of its own *
  2026-08-31

## Two names that stayed, with their requirements repaired

Named here because a reader of this file will ask why they are not above.

- `F-wish` stayed. Its requirement had ordered the opposite of what the first read allows: it said
  every wish a person voices becomes a queue row "that same moment", while the reading skill forbids
  giving a musing a row and forbids giving an idea an identifier, a priority or an estimate. Its
  Context also named `ROADMAP.md`, a file that no longer exists. The requirement now says a row opens
  behind an act that asked for work, names `PLAN.md` as the queue's home, and says plainly that no
  command writes a row when a person speaks.
- `F-feature-map` stayed. Its requirement had promised a map covering the spec's scenario sections
  "one to one" and called that the whole product. The requirement now says the map lists the
  requirements carrying a feature name, says that a requirement without one states machinery, and
  says the map is drawn when a person asks with no command producing it.
