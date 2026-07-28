# Decisions on record — what the pack believes you decided

TOUCHPOINT-KIND: decision-readback
DECISION-RECORD

This is the read-back surface (SPEC INV-207, ROADMAP 415). Every line under **On record** is a
decision the pack has written down AS YOURS, each naming the exchange it came from so you can go back
and check it. Read it on your own clock, and strike anything you never said — move it under **Struck**
with a one-line note. A struck line is retracted, never deleted; nothing here vanishes. The pack
renders this file for you through `scripts/render-doc.py` when you ask. [[teach]]

The rule the gate holds: a decision recorded as yours must name its exchange — at minimum a date. A
line with no exchange is a challengeable judgment moved into the one slot nothing questions, which is
the defect this surface exists to catch. [[wait]]

## On record
<!-- record:on -->
- 2026-07-27 ~11:35 — the repository carries no git tags: you never asked for them, and the four that
  existed had stopped being made eight releases ago, which reads as a machine misfiring. The version
  lives in `VERSION`, the release history in `JOURNAL.md`. The four deleted tags and the commits they
  pointed at are recorded in the journal, so any of them can be restored exactly.
- 2026-07-05 — CLAUDE.md became a thin loader, the working contract moving into the personal profile
  and the method into the live-spec pack (flipped on your OK that day).
- 2026-07-06 — the build-lane cap is three parallel lanes; a fourth opens only on your asked word
  [T-18].
- 2026-07-12 ~00:31 — live-spec runs on Opus as the orchestrator by default, the drafter-applier
  pipeline making the orchestrator seat brief-and-accept work; Fable only on your word for the hard
  passes.
- 2026-07-17 ~15:26 — nothing waits on a roster of agents: a dynamic system's permanent members
  declare themselves, so discovery is a bounded live scan for cards rather than a ratified list.
- 2026-07-17 ~16:07 — every point of contact with the person has a kind, and the kind decides what
  may be said there; you named this the movement's frame.
- 2026-07-17 ~16:58 — a cleanup says what it ended ships first, ahead of the stricter owned-identity
  check, since you run no python yourself and the collision bites only where someone else does.
- 2026-07-20 ~14:34 — every code's plain description follows one form: name the thing in a positive
  sentence, and where the rule governs a class, name the class and give a representative handful of its
  members rather than the exhaustive list; you accepted the form off the 15-code sample and asked to
  keep the class-member lists representative rather than complete [E-35, INV-239].

- The pack's own repository counts as a host of the pack, so three projects run under it: the music
  producer's coach, the photo site, and live-spec itself. Asked 2026-07-27 ~18:09, because the public page
  said two while the architecture and the test matrix named three real hosts; your word at ~18:11 was that
  live-spec is the third, unambiguously. The page now says three.

- 2026-07-28 ~19:55 — a document is clean only once a reader has read it through the audit skill.
  The reading covers every live document in the tree. Your words:

  ```text
  короче если аудита не было, то файл не "чистый", ultimately каждый файл читается именно через аудит. согласен? норм?
  ```

- 2026-07-28 ~20:48 — the queue is ordered by what enters a working context earliest. The entry
  documents and the pack skills stand at the front, and the queue then runs on through the rest of
  the tree. Your words:

  ```text
  давай без "потолка" это должно было отсечься! нет? про то что документы всегда same or better согласен, главное механизмы держать эту марку. порядок документов ты выводил раньше! мы сказали что начнем с тех которые первыми загрязняют твой же контекст. найди их сам. next steps? скиллы аудита (им все проверяем)? потом спеки? какие то вспомогательные файлы потом? понимаешь ход мысли? просто все подряд мы делали это плохо особенно когда походу загрязнается контекст. надо идти всегда из точки где контекст чист максимальной гигиеной.
  ```

- 2026-07-28 ~20:48 — a document leaves an edit the same or better. Mechanisms hold that mark, and a
  session's own care is too thin to hold it. The exchange is the ~20:48 message quoted above, which
  carries both calls in one breath.

- 2026-07-28, at `15:09 UTC` — a reading is owed at a minor version bump, and after a large growth
  in a document's size. The reader is an agent session, and the pack asks a person for no reading.
  You raised the major bump first:

  ```text
  Надо тогда поставить чтение агентом (не человеком как ты ошибаешься и говоришь) когда дибо размер сильно вырос либо когда major version?
  ```

  Hearing that a major bump is rare, you moved the trigger down at `15:12 UTC`:

  ```text
  Минорную ок.
  ```

## Open — carried, awaiting your word
<!-- record:open -->
These are open questions the pack carries with a recommendation, moved here from the old spec body when
the format sent decision history out of the spec. They are not decisions attributed to you, so they
name no exchange and carry no date. Each waits for your word, and the pack runs on the stated
recommendation until then. The spec points to each by its code, as a gap line under the requirement the
question touches.

Before this list reaches you again, every item is re-tested against the tree as it stands. An item an
artifact now answers is closed with that citation, and an item with a trigger of its own names that
trigger. Swept 2026-07-28: all three still stand open, and work is blocked by none of them.

The adoption attic's layout is open: a flat folder with a manifest and a source-directory prefix on a
name collision, against dated subfolders. The pack runs on the flat-with-manifest form and revisits at
the next real adoption run. [D-1]

The pair's queues are open: one reading view stitched across the pair's two queues, or strictly two.
The queues stay per-repo either way. The recommendation is two plain queues with no stitched view, held
until real friction — flipping between two windows to follow one wish's two halves — earns one. [D-6]

The pair instance's spec citation is open: whether the instance's spec may cite engine facts, or only
the content contract. The recommendation is that the instance cites the engine's contract entries by
their handle and nothing deeper, because a contract entry is the engine's versioned public promise
while an internal fact rots at the engine's next refactor. [D-7]

## Struck — recorded as yours, then you struck it
<!-- record:struck -->
- ~~Parallel lanes rank above the communication layer, and they wait for a field run.~~ STRUCK
  2026-07-17: recorded in your voice by a session as your ranking, and read back at ~15:37 you
  recognised nothing — no message of yours, on any day, said it. This is the incident that born
  ROADMAP 415: a session's own judgment moved into the one slot nothing questions.

## Notes
<!-- record:note -->
Nothing here is ever dropped. A struck line stays with its note so the record of what was corrected
outlives the correction.
