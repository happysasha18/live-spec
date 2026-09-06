#!/usr/bin/env python3
"""The ticket state machine: one deterministic operation per transition, run against PLAN.md
and the work's own checkpoint, refusing the illegal move.

`admit` is T1+T2 of the product contract's section 4 table
(`.live-spec/turnkey-contract-composed.md`): an accepted route becomes one row and one
checkpoint. The subcommands below are the rest of that table — `correct` (T3's queued half),
`block` (T4), `unblock` (T5), `park` (T6), `close` (T7), `reopen` (T8), `abandon` (T9), plus
`hold`, the half of T2 that names a holder on a ticket admitted earlier. `brief` is not a
transition: it hands a worker the ticket's own stored text, which is what makes the brief a
brief rather than a retelling.

The checkpoint half of every transition goes through `scripts/checkpoint.py`; the plan half is
read through the one plan parser this project has. Nothing here reads a message: the Director
decides which transition runs, and this file decides whether it may.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

import checkpoint


REQUIRED_NEW = ("title", "observable_outcome", "done_when", "verification", "project", "scope")
# A definition of done that ends at somebody's eye cannot be re-run, so nothing can tell a
# finished row from an unfinished one tomorrow. Both word orders are the same gate — "the owner
# approved it" and "confirmed by the owner" — and so is the looking shape, which is that gate
# under a softer verb. No name is hardcoded: the person's own name in a regex made the refusal
# hold on one machine and nowhere else. An artifact-proven done ("the test passes", "the page
# renders") names no person and is admitted.
_GATE_WHO = r"(?:owner|user|person|human)"
_GATE_ACT = (r"(?:approves?|approved|checks?|checked|confirms?|confirmed|accepts?|accepted"
             r"|signs?\s+off|signed\s+off|looks?\s+at|looked\s+at|eyeballs?|eyeballed)")
HUMAN_GATE = re.compile(
    r"(?i)\b%(who)s\b.{0,30}?\b%(act)s\b"
    r"|\b%(act)s\b.{0,20}?\bby\b.{0,20}?\b%(who)s\b" % {"who": _GATE_WHO, "act": _GATE_ACT}
)
TASK_HEADER = re.compile(r"(?m)^###\s+[^\n]*?—\s+id:\s*([a-z]+)-(\d+)\s*$")


class AdmissionError(ValueError):
    pass


def validate_route(route: dict) -> str:
    action = route.get("action")
    creates = route.get("creates_work")
    if action == "none":
        if creates is not False:
            raise AdmissionError("action none requires creates_work=false")
        return "none"
    if action == "existing":
        if creates is not False or not route.get("existing_task"):
            raise AdmissionError("existing work requires creates_work=false and existing_task")
        return "existing"
    if action != "new" or creates is not True:
        raise AdmissionError("new work requires action=new and creates_work=true")

    missing = [field for field in REQUIRED_NEW if not str(route.get(field, "")).strip()]
    if missing:
        raise AdmissionError("new work is missing: %s" % ", ".join(missing))
    if route.get("existing_task"):
        raise AdmissionError("new work must state no existing_task")
    if HUMAN_GATE.search(str(route["done_when"])):
        raise AdmissionError("done_when makes the person the ordinary delivery gate")
    _pointers(route)

    source = route.get("source")
    if not isinstance(source, dict) or source.get("kind") not in {"person", "external_defect"}:
        raise AdmissionError("new work source must be person or external_defect")
    if not str(source.get("detail", "")).strip():
        raise AdmissionError("source.detail is required")
    if source["kind"] == "external_defect":
        missing_defect = [name for name in ("promised_behavior", "reproduction", "observed_by")
                          if not str(source.get(name, "")).strip()]
        if missing_defect:
            raise AdmissionError("external_defect is missing: %s" % ", ".join(missing_defect))
    return "new"


# The four statuses of the contract's section 3, in the one spelling every reader compares
# against (`scripts/plan_checks_core.py` normalizes the same four).
QUEUED, IN_HAND, BLOCKED, DONE = "\u2b1c", "\U0001f504", "\u26d4", "\u2705"

# The three reason kinds a block may name, closed set (contract section 3 and T4). A fourth
# word is refused; so is a reason that only says the work is hard, which names none of them.
BLOCK_KINDS = ("technical limit", "outside dependency", "owner action")
DIFFICULTY = re.compile(
    r"(?i)\b(hard|difficult|difficulty|complex|complicated|tricky|messy|unclear|"
    r"confusing|too big|too much|takes too long)\b"
)
# T5's own words: never "assumed cleared". A block clears against a fact somebody can look up.
ASSUMED = re.compile(r"(?i)\b(assum\w+|probabl\w+|presumabl\w+|should be|likely|by now)\b")

ROW_HEADER = "### %s %s \u2014 id: %s"


def _row_span(plan: str, task_id: str):
    """(start, end, mark, title) of one ticket's block in PLAN.md, or a refusal."""
    m = re.search(r"(?m)^### (\S+) (.+?) \u2014 id: %s$" % re.escape(task_id), plan)
    if not m:
        raise AdmissionError("no ticket with id %s in the plan" % task_id)
    nxt = re.search(r"(?m)^#{2,6} ", plan[m.end():])
    end = m.end() + nxt.start() if nxt else len(plan)
    return m.start(), end, m.group(1), m.group(2)


def _set_paragraph(block: str, prefix: str, value):
    """Set, replace or (value=None) drop the one paragraph of a row that starts with `prefix`."""
    paras = block.split("\n\n")
    for i, para in enumerate(paras):
        if para.startswith(prefix):
            if value is None:
                paras.pop(i)
            else:
                paras[i] = prefix + " " + value
            return "\n\n".join(paras)
    if value is None:
        return block
    paras.insert(1, prefix + " " + value)
    return "\n\n".join(paras)


def _holder(block: str):
    m = re.search(r"(?m)^\*\*Holder:\*\*\s*(.+)$", block)
    return m.group(1).strip() if m else None


def _rewrite_row(plan_path: Path, task_id: str, mark=None, title=None, edits=()):
    """The one writer of a ticket's own block: a new mark, a new title, paragraph edits."""
    plan = plan_path.read_text(encoding="utf-8")
    start, end, cur_mark, cur_title = _row_span(plan, task_id)
    block = plan[start:end]
    header_end = block.index("\n")
    block = (ROW_HEADER % (mark or cur_mark, title or cur_title, task_id)) + block[header_end:]
    for prefix, value in edits:
        block = _set_paragraph(block, prefix, value)
    checkpoint.write_atomic(plan_path, plan[:start] + block + plan[end:])


def _checkpoint_path(checkpoints_dir: Path, task_id: str) -> Path:
    return Path(checkpoints_dir) / (task_id + ".md")


def _pointers(route: dict) -> str:
    """The ticket's context pointers, each an exact address into a document that exists.

    Contract section 2: a spec code, an architecture node name, a matrix row id, a `path:line`,
    a test name, a commit hash — never a pasted copy. A ticket that carries none cannot be
    resumed by anyone but the session that wrote it, which is the whole failure this refusal
    exists to stop, so admission refuses it rather than admitting a ticket nobody else can read.
    """
    raw = route.get("context_pointers")
    if isinstance(raw, str):
        raw = [raw]
    pointers = [str(p).strip() for p in (raw or []) if str(p).strip()]
    if not pointers:
        raise AdmissionError("a ticket carries at least one context pointer")
    return "; ".join(pointers)


def next_task_id(plan: str) -> str:
    nums = [int(num) for prefix, num in TASK_HEADER.findall(plan) if prefix == "q"]
    return "q-%d" % ((max(nums) if nums else 0) + 1)


def render_task(route: dict, task_id: str) -> str:
    source = route["source"]["detail"].strip()
    return (
        "### ⬜ {title} — id: {task_id}\n"
        "**Group:** {scope} · **Priority:** normal\n"
        "**Source:** {source}\n\n"
        "**Outcome:** {outcome}\n\n"
        "**Done when:** {done}\n\n"
        "**Verification:** {verification}\n\n"
        "**Context pointers.** {pointers}\n"
    ).format(
        title=route["title"].strip(), task_id=task_id, scope=route["scope"].strip(),
        source=source, outcome=route["observable_outcome"].strip(),
        done=route["done_when"].strip(), verification=route["verification"].strip(),
        pointers=_pointers(route),
    )


def decision_sheet(route: dict) -> str:
    return "\n".join((
        "Goal: %s" % route["title"].strip(),
        "Observable outcome: %s" % route["observable_outcome"].strip(),
        "Definition of done: %s" % route["done_when"].strip(),
        "Verification: %s" % route["verification"].strip(),
        "Project: %s" % route["project"].strip(),
        "Scope: %s" % route["scope"].strip(),
        "Source: %s" % route["source"]["detail"].strip(),
    ))


def insert_row(plan: str, task: str) -> str:
    """Put the row at the end of `## Tasks`, the one section every reader of the plan looks in.

    Anchored on the section the row belongs to rather than on the section that happens to follow
    it. This used to append before `## Blockers`, falling back to the foot of the file — and a
    plan with no `## Blockers` section (this project's own, 2026-09-06) got its row written past
    the end of `## Tasks`, where the plan's parser stops reading: the row existed on the page and
    in no reader, no probe line, no board column, no next-action candidate.
    """
    start = plan.find("\n## Tasks")
    if start != -1:
        end = plan.find("\n## ", start + 1)
        if end != -1:
            return plan[:end] + "\n" + task + plan[end:]
    return plan.rstrip() + "\n\n" + task


def admit(route: dict, plan_path: Path, checkpoints_dir: Path) -> dict:
    verdict = validate_route(route)
    if verdict != "new":
        return {"action": verdict, "writes": []}

    plan = plan_path.read_text(encoding="utf-8")
    normalized_title = " ".join(route["title"].lower().split())
    for header in re.findall(r"(?m)^###\s+[^\n]*?\s+(.*?)\s+—\s+id:\s*\S+\s*$", plan):
        if " ".join(header.lower().split()) == normalized_title:
            raise AdmissionError("an existing task already has this title")

    task_id = str(route.get("task_id") or next_task_id(plan)).strip()
    if not re.fullmatch(r"[a-z]+-\d+", task_id):
        raise AdmissionError("task_id must look like q-12")
    if re.search(r"(?m)—\s+id:\s*%s\s*$" % re.escape(task_id), plan):
        raise AdmissionError("task id already exists: %s" % task_id)
    cp_path = checkpoints_dir / (task_id + ".md")
    if cp_path.exists():
        raise AdmissionError("checkpoint already exists: %s" % cp_path)
    task = render_task(route, task_id)
    new_plan = insert_row(plan, task)

    # Validate the checkpoint completely in a temporary location before either durable write.
    with tempfile.TemporaryDirectory(prefix="live-spec-admission-") as tmp:
        staged = Path(tmp) / cp_path.name
        checkpoint.new_checkpoint(staged, route["title"].strip(), "pipeline", decision_sheet(route))
        issues = checkpoint.validate_checkpoint(staged)
        if issues:
            raise AdmissionError("invalid staged checkpoint: %s" % "; ".join(issues))
        checkpoint.write_atomic(plan_path, new_plan)
        cp_path.parent.mkdir(parents=True, exist_ok=True)
        checkpoint.write_atomic(cp_path, staged.read_text(encoding="utf-8"))
    return {"action": "new", "task_id": task_id,
            "writes": [str(plan_path), str(cp_path)]}


# ---------------------------------------------------------------- T3..T9, one per transition


def hold(plan_path: Path, task_id: str, holder: str) -> None:
    """T2's naming half: a holder takes a ticket that was admitted earlier.

    The checkpoint is already there — `admit` opens it — so this writes the one thing the plan
    itself has to carry while work is in hand: who holds it. T5 and T6 both read it back.
    """
    holder = str(holder).strip()
    if not holder:
        raise AdmissionError("taking a ticket in hand names its holder")
    plan = Path(plan_path).read_text(encoding="utf-8")
    start, end, mark, _ = _row_span(plan, task_id)
    # Every other transition here reads the mark it is about to overwrite; this one did not, so
    # `hold` would quietly walk a closed row back into work, and would rename the holder of work
    # somebody else was already running — the second lane then reports on a ticket it does not
    # hold, and the first one's name is gone from the plan.
    if mark == DONE:
        raise AdmissionError(
            "%s is done: reopen it before taking it in hand" % task_id)
    current = _holder(plan[start:end])
    if mark == IN_HAND and current and current != holder:
        raise AdmissionError(
            "%s is already in hand, held by %s — park it before another holder takes it"
            % (task_id, current))
    _rewrite_row(plan_path, task_id, mark=IN_HAND, edits=[("**Holder:**", holder)])


def correct(plan_path: Path, checkpoints_dir: Path, task_id: str, goal=None, done=None) -> None:
    """T3, the queued half: a queued ticket's goal and done are rewritten where they live.

    A correction to work already in hand belongs on that work's own checkpoint
    (`checkpoint.py update`), which is why this refuses one: two homes for one correction is
    how the plan and the sheet start disagreeing about what the work is.
    """
    if goal is None and done is None:
        raise AdmissionError("a correction rewrites the goal, the done, or both")
    plan = Path(plan_path).read_text(encoding="utf-8")
    _, _, mark, _ = _row_span(plan, task_id)
    if mark != QUEUED:
        raise AdmissionError(
            "%s is not queued: a ticket in hand is corrected on its own checkpoint" % task_id)
    edits = []
    if done is not None:
        edits.append(("**Done when:**", str(done).strip()))
    _rewrite_row(plan_path, task_id, title=(goal.strip() if goal else None), edits=edits)


def block(plan_path: Path, checkpoints_dir: Path, task_id: str, kind: str, reason: str) -> None:
    """T4: the ticket goes blocked, and only for one of the three named kinds.

    The refusal that matters is the second one. "This is complicated" is not a blocker, it is
    the work; a real blocker names the failing command, the outside dependency, or the one owner
    action, and a reason that only says how hard the thing is names none of them.
    """
    kind = str(kind).strip().lower()
    if kind not in BLOCK_KINDS:
        raise AdmissionError("a blocker names one of: %s" % ", ".join(BLOCK_KINDS))
    reason = str(reason).strip()
    if not reason:
        raise AdmissionError("a blocker names the concrete thing that stopped the work")
    if DIFFICULTY.search(reason):
        raise AdmissionError(
            "a blocker names the failing command, the dependency or the owner action — "
            "not how hard the work is")

    plan = Path(plan_path).read_text(encoding="utf-8")
    _, _, mark, _ = _row_span(plan, task_id)
    # Same missing read as `hold` had: a closed row could be marked blocked without ever being
    # reopened, and a second block over an already-blocked row overwrote the first blocker's
    # own line, losing the cause that is the whole point of the mark.
    if mark == DONE:
        raise AdmissionError("%s is done: reopen it before blocking it" % task_id)
    if mark == BLOCKED:
        raise AdmissionError(
            "%s is already blocked: clear the block before naming another" % task_id)

    line = "%s: %s" % (kind, reason)
    cp = _checkpoint_path(checkpoints_dir, task_id)
    if cp.exists() and checkpoint.read_checkpoint(cp)["status"] == "open":
        body = checkpoint.read_checkpoint(cp)["sections"].get("IN PROGRESS", "").strip()
        checkpoint.update_checkpoint(cp, in_progress=(body + "\nBlocked: " + line).strip())
    _rewrite_row(plan_path, task_id, mark=BLOCKED, edits=[("**Blocked by:**", line)])


def unblock(plan_path: Path, checkpoints_dir: Path, task_id: str, cleared_by: str) -> None:
    """T5: the block clears against a named fact, and the ticket lands where its holder says.

    In hand if the ticket still names one, queued otherwise — a block can clear with nobody
    holding the work, and landing it in hand would name a holder who went home.
    """
    cleared_by = str(cleared_by).strip()
    if not cleared_by or ASSUMED.search(cleared_by):
        raise AdmissionError(
            "a block clears against a named fact — a commit, a reply, a dependency — "
            "never an assumption")
    plan = Path(plan_path).read_text(encoding="utf-8")
    start, end, mark, _ = _row_span(plan, task_id)
    if mark != BLOCKED:
        raise AdmissionError("%s is not blocked" % task_id)

    cp = _checkpoint_path(checkpoints_dir, task_id)
    if cp.exists() and checkpoint.read_checkpoint(cp)["status"] == "open":
        body = checkpoint.read_checkpoint(cp)["sections"].get("IN PROGRESS", "")
        kept = [ln for ln in body.splitlines() if not ln.startswith("Blocked: ")]
        checkpoint.update_checkpoint(cp, in_progress="\n".join(kept).strip() or "(nothing yet)")
    landing = IN_HAND if _holder(plan[start:end]) else QUEUED
    _rewrite_row(plan_path, task_id, mark=landing, edits=[("**Blocked by:**", None)])


def park(plan_path: Path, checkpoints_dir: Path, task_id: str, next_: str) -> None:
    """T6: a halt that parks. The holder goes, the checkpoint stays open, NEXT says what remains.

    Closing the checkpoint here is what would lose the work — a parked ticket is resumed from
    its own NEXT by whoever picks it up next, and a closed checkpoint has nothing to resume.
    """
    next_ = str(next_).strip()
    if not next_:
        raise AdmissionError("parking records what remains, in NEXT")
    plan = Path(plan_path).read_text(encoding="utf-8")
    start, end, _, _ = _row_span(plan, task_id)
    if not _holder(plan[start:end]):
        raise AdmissionError("nothing to park: %s names no holder" % task_id)
    cp = _checkpoint_path(checkpoints_dir, task_id)
    checkpoint.update_checkpoint(cp, next=next_)
    _rewrite_row(plan_path, task_id, mark=QUEUED, edits=[("**Holder:**", None)])


def close(plan_path: Path, checkpoints_dir: Path, task_id: str) -> None:
    """T7: the checkpoint closes, and THEN the mark is written. Two writes, in that order.

    The order is the whole crash-recovery rule. A crash between the two leaves a closed
    checkpoint on a ticket still marked in hand, and running this again finishes it: a
    checkpoint already closed is a no-op that only (re)writes the mark. The other way round —
    mark first — a crash would leave a ticket marked done with its work still open.
    """
    plan = Path(plan_path).read_text(encoding="utf-8")
    _, _, mark, _ = _row_span(plan, task_id)
    if mark == BLOCKED:
        raise AdmissionError("%s is blocked: clear the block before closing" % task_id)
    cp = _checkpoint_path(checkpoints_dir, task_id)
    if cp.exists() and checkpoint.read_checkpoint(cp)["status"] == "open":
        try:
            checkpoint.close_checkpoint(cp)
        except ValueError as exc:
            raise AdmissionError(str(exc))
    # The holder stays on the row. T8's fork reads it — a done that turns out false comes back
    # in hand where somebody still holds it, and queued where nobody does.
    _rewrite_row(plan_path, task_id, mark=DONE)


def reopen(plan_path: Path, checkpoints_dir: Path, task_id: str,
           false_condition: str, evidence: str) -> None:
    """T8: a done that turned out false reopens the same id, never a copy."""
    false_condition, evidence = str(false_condition).strip(), str(evidence).strip()
    if not false_condition or not evidence:
        raise AdmissionError("reopening names the false condition and the evidence for it")
    plan = Path(plan_path).read_text(encoding="utf-8")
    start, end, mark, _ = _row_span(plan, task_id)
    if mark != DONE:
        raise AdmissionError("only a done ticket reopens: %s is marked %s" % (task_id, mark))

    cp = _checkpoint_path(checkpoints_dir, task_id)
    # T8 reopens the SAME checkpoint, never a copy — so with no checkpoint there is nothing to
    # reopen, and proceeding would leave a row marked in hand with no record of what the work is.
    if not cp.exists():
        raise AdmissionError("%s has no checkpoint to reopen" % task_id)
    if checkpoint.read_checkpoint(cp)["status"] == "closed":
        checkpoint.reopen_checkpoint(cp)
    checkpoint.update_checkpoint(
        cp, next="Reopened: %s was not true — %s" % (false_condition, evidence))
    _rewrite_row(plan_path, task_id, mark=IN_HAND if _holder(plan[start:end]) else QUEUED)


def abandon(plan_path: Path, checkpoints_dir: Path, task_id: str, reason: str) -> None:
    """T9: a halt that abandons. IN PROGRESS and NEXT are cleared with the halt's reason as
    their last line, and the checkpoint closes in the same step.

    The reason stays because a ticket abandoned without one comes back next month as a fresh
    idea. The close is in the same step because the alternative — an abandoned ticket with an
    open checkpoint — reads to the next session as work in hand that nobody is holding. The row
    itself leaves the list by a person's hand, under the plan's existing archive rule.
    """
    reason = str(reason).strip()
    if not reason:
        raise AdmissionError("abandoning records the halt's reason")
    cp = _checkpoint_path(checkpoints_dir, task_id)
    if cp.exists() and checkpoint.read_checkpoint(cp)["status"] == "open":
        cleared = "(nothing \u2014 abandoned: %s)" % reason
        checkpoint.update_checkpoint(cp, in_progress=cleared, next=cleared)
        checkpoint.close_checkpoint(cp)
    _rewrite_row(plan_path, task_id, mark=QUEUED, edits=[("**Holder:**", None)])


def worker_brief(plan_path: Path, checkpoints_dir: Path, task_id: str) -> str:
    """The brief a worker is handed: the ticket entry, then its checkpoint's NEXT. Verbatim.

    Not a transition and not a summary. Both halves are copied out of the two files that
    already hold them, so a worker reads the same words the plan and the sheet do; a brief
    that paraphrases either one is a third statement of the work, and the third statement is
    the one that turns out to be wrong.
    """
    plan = Path(plan_path).read_text(encoding="utf-8")
    start, end, _, _ = _row_span(plan, task_id)
    cp = _checkpoint_path(checkpoints_dir, task_id)
    if not cp.exists():
        raise AdmissionError("%s has no checkpoint to brief from" % task_id)
    nxt = checkpoint.read_checkpoint(cp)["sections"].get("NEXT", "").strip()
    return plan[start:end].strip() + "\n\n## NEXT\n\n" + nxt + "\n"


def main() -> int:
    """One CLI surface: `admit` for T1+T2, one subcommand per transition after it.

    `--route` with no subcommand still runs admission, the shape the pipeline's own execution
    reference already documents.
    """
    argv = list(sys.argv[1:])
    if "--route" in argv and (not argv or argv[0].startswith("-")):
        argv.insert(0, "admit")

    parser = argparse.ArgumentParser(prog="task-admission.py")
    sub = parser.add_subparsers(dest="op", required=True)

    def op(name, *args, **kwargs):
        sp = sub.add_parser(name, **kwargs)
        if name != "admit":
            sp.add_argument("id")
        for flag, required in args:
            sp.add_argument(flag, required=required)
        sp.add_argument("--plan", default="PLAN.md", type=Path)
        sp.add_argument("--checkpoints", default=".live-spec/checkpoints", type=Path)
        return sp

    op("admit", help="T1+T2 — one accepted route becomes one row and one checkpoint"
       ).add_argument("--route", required=True, type=Path)
    op("hold", ("--holder", True), help="T2 — name the holder of a ticket already admitted")
    op("correct", ("--goal", False), ("--done", False),
       help="T3 — rewrite a queued ticket's goal and done in place")
    op("block", ("--kind", True), ("--reason", True), help="T4 — mark blocked, reason named")
    op("unblock", ("--cleared-by", True), help="T5 — clear a block against a named fact")
    op("park", ("--next", True), help="T6 — clear the holder, leave the checkpoint open")
    op("close", help="T7 — close the checkpoint, then write the done mark")
    op("reopen", ("--false-condition", True), ("--evidence", True),
       help="T8 — reopen the same id against a named false condition")
    op("abandon", ("--reason", True), help="T9 — clear and close the checkpoint with the reason")
    op("brief", help="hand a worker the ticket entry plus its checkpoint's NEXT, verbatim")

    args = parser.parse_args(argv)
    plan, cps = args.plan, args.checkpoints
    try:
        if args.op == "admit":
            route = json.loads(args.route.read_text(encoding="utf-8"))
            result = admit(route, plan, cps)
            print(json.dumps({"status": "ok", **result}, ensure_ascii=False))
            return 0
        if args.op == "brief":
            print(worker_brief(plan, cps, args.id), end="")
            return 0
        if args.op == "hold":
            hold(plan, args.id, args.holder)
        elif args.op == "correct":
            correct(plan, cps, args.id, goal=args.goal, done=args.done)
        elif args.op == "block":
            block(plan, cps, args.id, args.kind, args.reason)
        elif args.op == "unblock":
            unblock(plan, cps, args.id, args.cleared_by)
        elif args.op == "park":
            park(plan, cps, args.id, args.next)
        elif args.op == "close":
            close(plan, cps, args.id)
        elif args.op == "reopen":
            reopen(plan, cps, args.id, args.false_condition, args.evidence)
        elif args.op == "abandon":
            abandon(plan, cps, args.id, args.reason)
    except (OSError, json.JSONDecodeError, AdmissionError, ValueError) as exc:
        print(json.dumps({"status": "red", "error": str(exc)}, ensure_ascii=False))
        return 1
    print("%s: %s" % (args.op, args.id))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
