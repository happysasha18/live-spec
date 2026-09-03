# Retired: `spec/message-first-read.md` Requirement 315 — the idea shelf

Retired 2026-09-03 under `PLAN.md` row `q-813`, on the owner's word of that morning: no second
list beside `PLAN.md`, not even a shelf, and no section inside `PLAN.md` for it either
(`DECISIONS.md`, 2026-09-03 ~10:20). The requirement had carried its `[target]` marker from the day
it was written, and its own Context said the home it named stood nowhere in the tree.

What stands in its place is a judgement rather than a place. `skills/director/SKILL.md` has the
Director weigh an idea when it hears one: an idea it finds real and understood well enough to say
why the work is queued becomes an ordinary row in `PLAN.md`, an idea still unclear draws one
question asked there and then, and a thought said in passing is answered with nothing recorded
anywhere.

Retired with it: the entity `E-37` and the invariant `INV-320`, both withdrawn rather than
re-owned; the matrix rows `M-610` and `M-611`, which named this requirement's landing rather than a
test; and the glossary entry **idea shelf** in `PRODUCT_SPEC.md`. `INV-320`'s number stays empty in
`tests/test_formal_index.py`'s pinned gaps, so an older citation still means what it said.

The text below is the requirement exactly as it stood in `spec/message-first-read.md` before the
retirement.

---

## Requirement 315: An idea named in passing is kept in the person's own words
   [target]

**Context:** In the middle of a conversation about something else, a person names a possibility they are not asking for now. The reading calls that an idea, and an idea earns a home of its own and no task: it is kept in the person's own wording, with no identifier, no priority, and no estimate, and one line comes back saying it was kept. Days later the person asks what they proposed and the wording comes back as they said it. The home this requirement names stands nowhere in the tree: no file holds it, no command writes to it, and no test reads it, so an idea said aloud lives as long as the conversation and no longer.

**User Story:** As a person who thinks aloud while working on something else, I want a passing idea kept in my own words, so that I find it again days later without its having become work.

### Acceptance Criteria

**Case: an idea is kept, and never started**

1. *when* the act is an idea for later, the system *shall* keep the person's own wording on the idea shelf and *shall* say in one line that it was kept. [E-37]
2. The system *shall* give a kept idea no identifier, no priority, and no estimate, and *shall* never start work on it. [E-37]
3. *when* the person later asks what they proposed, the system *shall* give back the kept wording as it was said. [INV-320]

**Case: the shelf and the work are one fork**

4. *when* one message both names an idea and asks for work, the system *shall* take the work and shelve the idea as two separate outcomes. [E-37, INV-316]
5. The system *shall* never place one item on the shelf and into the work at once. [E-37, INV-320]

---

## The two matrix rows retired with it

These stood in `matrix/director.md`, both *todo*, both naming the landing rather than a test.

| ID | Fact (from spec) | Test level | Owning test | Status |
|---|---|---|---|---|
| M-610 | An idea named without being asked for is kept in the person's own wording with no identifier, no priority and no estimate, one line comes back saying it was kept, and the wording comes back as it was said when the person later asks; never an idea given a task id or an estimate, and never a kept idea returned in the system's words rather than the person's [E-37] | string | lands with the idea shelf | *todo* |
| M-611 | A message that both names an idea and asks for work takes the work and shelves the idea as two separate outcomes; never one item standing on the shelf and inside the work at once [E-37, INV-320] | string | lands with the idea shelf | *todo* |

## The glossary entry retired with it

- **idea shelf** — the home an idea named without being asked for is kept in, holding the person's own wording with no identifier, no priority, and no estimate.
