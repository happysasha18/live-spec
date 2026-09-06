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
import datetime
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import checkpoint
import plan_checks_core


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


def _set_paragraph(block: str, prefix: str, value, after: str = None):
    """Set, replace or (value=None) drop the one paragraph of a row that starts with `prefix`.

    A new paragraph lands after the paragraph `after` names when that one is there, so the
    validation record stands under the statement it judges rather than at the row's head.
    """
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
    at = 1
    if after:
        for i, para in enumerate(paras):
            if para.startswith(after):
                at = i + 1
                break
    paras.insert(at, prefix + " " + value)
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
    for edit in edits:
        block = _set_paragraph(*((block,) + tuple(edit)))
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


# ------------------------------------------------- the statement, its validation, its freeze
# Requirement 309 criteria 41-62. A task carries one statement — echo-name, description, plan,
# time estimate — and enters work only after that statement passes a mechanical floor and a
# clean-context reader. The statement and its validation record live in the task's own PLAN.md
# entry, keyed by the row's id: PLAN.md is the work board's own source file today, and a second
# store would be the "two homes for one fact" this project already forbids.

PARALLEL = "\u2225"          # before a step: the plan expects it to run beside the previous one
EN_DASH = "\u2013"           # the estimate's range separator
STATEMENT = "**Statement.**"
VALIDATION = "**Validation.**"
FROZEN = "**Frozen at take-up"

_STATEMENT_RE = re.compile(
    r"Echo-name:\s*(?P<echo>.+?)\.\s+"
    r"Description:\s*(?P<description>.+?)\s+"
    r"Plan:\s*(?P<plan>.+?)\s+"
    r"Estimate:\s*(?P<low>[\d.]+)\s*[\u2013\u2014-]\s*(?P<high>[\d.]+)\s+(?P<unit>[A-Za-z]+)"
    r"\s*[\u2014\u2013-]+\s*basis:\s*(?P<basis>.+?)\s*$", re.S)
_STEP_RE = re.compile(
    r"(?P<par>%s\s*)?(?P<n>\d+)\)\s*(?P<text>.*?)(?=\s*(?:%s\s*)?\d+\)|$)"
    % (PARALLEL, PARALLEL), re.S)
_VALIDATION_RE = re.compile(
    r"(?P<date>\d{4}-\d\d-\d\d)\s*\u00b7\s*floor:\s*(?P<floor>[^\u00b7]+?)\s*\u00b7\s*"
    r"reader:\s*(?P<reader>[^\u00b7]+?)\s*\u00b7\s*echo-name placed:\s*(?P<placed>[^\u00b7]+?)"
    r"\s*\u00b7\s*status:\s*(?P<status>\w+)", re.S)
READER_FIELDS = ("What is to be done", "Why", "How long", "Echo-name placed")


def _paragraph(block: str, prefix: str):
    for para in block.split("\n\n"):
        if para.startswith(prefix):
            return para
    return None


def read_statement(block: str):
    """The row's statement, parsed, or None when it carries none that reads."""
    para = _paragraph(block, STATEMENT)
    if not para:
        return None
    m = _STATEMENT_RE.search(" ".join(para[len(STATEMENT):].split()))
    if not m:
        return None
    out = m.groupdict()
    out["steps"] = [(int(st.group("n")), bool(st.group("par")), st.group("text").strip())
                    for st in _STEP_RE.finditer(out["plan"]) if st.group("text").strip()]
    return out


def read_validation(block: str):
    para = _paragraph(block, VALIDATION)
    if not para:
        return None
    m = _VALIDATION_RE.search(" ".join(para[len(VALIDATION):].split()))
    return {k: v.strip() for k, v in m.groupdict().items()} if m else None


def parallel_expectation(steps) -> int:
    """How many of the plan's steps stand side by side at its widest — the plan's expectation,
    never the lane decision, which take-up makes and the LANES line records beside it."""
    best = run = 0
    for _, parallel, _ in steps:
        run = run + 1 if parallel else 1
        best = max(best, run)
    return best or 1


_REGISTER = None


def _register_hits(text: str):
    """The repo's own register lint, run on the statement's words (criterion 49's clean check)."""
    global _REGISTER
    if _REGISTER is None:
        path = Path(__file__).resolve().with_name("preshow-register-lint.py")
        if not path.exists():
            _REGISTER = False
        else:
            spec = importlib.util.spec_from_file_location("preshow_register_lint", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            _REGISTER = mod
    return _REGISTER.scan(text) if _REGISTER else []


def floor_issues(block: str) -> list:
    """The mechanical floor: the four fields present, the register clean, the steps in order."""
    statement = read_statement(block)
    if not statement:
        return ["the row carries no statement with an echo-name, a description, "
                "a plan and an estimate"]
    issues = []
    words = statement["echo"].split()
    if not 2 <= len(words) <= 5:
        issues.append("an echo-name runs two to five plain words")
    if not statement["description"].strip():
        issues.append("the description is empty")
    if not statement["steps"]:
        issues.append("the plan names no step")
    elif [n for n, _, _ in statement["steps"]] != list(range(1, len(statement["steps"]) + 1)):
        issues.append("the plan's steps are not numbered in the order they run")
    if not statement["basis"].strip():
        issues.append("the estimate names no basis")
    hits = _register_hits(_paragraph(block, STATEMENT) or "")
    if hits:
        issues.append("the register check reads %s in the statement" % hits[0][1])
    return issues


def read_reader_record(path) -> dict:
    """The fresh reader's own answers, as a file of `Field: answer` lines.

    Who writes it is the pipeline skill's sentence: an agent with no project vocabulary, given
    only the Statement paragraph and the three questions. What this reads is whether the record
    is complete and which name the reader placed.
    """
    text = Path(path).read_text(encoding="utf-8")
    got = {}
    for line in text.splitlines():
        key, sep, value = line.partition(":")
        if sep and key.strip() in READER_FIELDS:
            got[key.strip()] = value.strip()
    missing = [f for f in READER_FIELDS if not got.get(f)]
    if missing:
        raise AdmissionError("the reader's record answers nothing for: %s" % ", ".join(missing))
    # Criterion 50: a question the reader cannot answer fails the statement. The reader is told
    # to write "cannot tell from this" rather than guess, so that answer is the failure itself.
    unanswered = [f for f in READER_FIELDS if "cannot tell" in got[f].lower()]
    if unanswered:
        raise AdmissionError(
            "the reader could not answer from the statement alone: %s" % ", ".join(unanswered))
    return got


def _same_name(one: str, two: str) -> bool:
    norm = lambda s: " ".join(s.lower().replace(".", " ").split())  # noqa: E731
    return norm(one) == norm(two)


def validate(plan_path, task_id: str, reader=None) -> dict:
    """Run the statement's validation and write its record onto the row.

    A failed floor or a failed reader leaves the record at `status: rewritten`, which is what
    `hold` refuses on — so the task stays out of work until the statement is rewritten and
    validated again (criterion 53).
    """
    plan = Path(plan_path).read_text(encoding="utf-8")
    start, end, _, _ = _row_span(plan, task_id)
    block = plan[start:end]
    issues = floor_issues(block)
    floor = "passed" if not issues else "failed (%s)" % issues[0]

    placed, reader_note = "no", "not run"
    if not issues:
        if reader is None:
            reader_note = "not run"
        else:
            try:
                record = read_reader_record(reader)
            except (AdmissionError, OSError) as exc:
                reader_note = "failed (%s)" % exc
            else:
                if _same_name(record["Echo-name placed"], read_statement(block)["echo"]):
                    placed, reader_note = "yes", "passed"
                else:
                    reader_note = ("failed (the reader placed the name on %r)"
                                   % record["Echo-name placed"])

    status = "ready" if floor == "passed" and reader_note == "passed" else "rewritten"
    line = "%s \u00b7 floor: %s \u00b7 reader: %s \u00b7 echo-name placed: %s \u00b7 status: %s" % (
        datetime.date.today().isoformat(), floor, reader_note, placed, status)
    _rewrite_row(plan_path, task_id, edits=[(VALIDATION, line, STATEMENT)])
    return {"status": status, "floor": issues, "reader": reader_note, "placed": placed}


# ------------------------------------------------------------------ deriving one at admission

def _echo_name(route: dict) -> str:
    echo = str(route.get("echo_name") or "").strip()
    if not echo:
        echo = " ".join(str(route["title"]).split()[:5])
    if not 2 <= len(echo.split()) <= 5:
        raise AdmissionError("an echo-name runs two to five plain words: %r" % echo)
    return echo.rstrip(".")


def _plan_steps(route: dict) -> list:
    """The plan, in the order the steps run. Given on the route, or read off the definition of
    done — whose conditions are already the slices of the change, written when the row opens."""
    raw = route.get("plan")
    if not raw:
        raw = [part.strip() for part in str(route["done_when"]).split(";") if part.strip()]
    steps = []
    for i, step in enumerate(raw, 1):
        step = str(step).strip()
        parallel = step.startswith(PARALLEL)
        steps.append((i, parallel, step.lstrip(PARALLEL).strip().rstrip(".")))
    if not steps:
        raise AdmissionError("a statement carries a plan: the steps in the order they run")
    return steps


def _span(minutes: float):
    if minutes >= 90:
        return round(minutes / 60.0, 1), "hours"
    return round(minutes), "minutes"


def comparable_durations(scope: str, plan: str, checkpoints_dir) -> list:
    """Closed rows of the same group whose own checkpoint stamps give a real duration.

    This is the only history this tree records: the checkpoint file is created when the ticket is
    admitted and written again at every transition through the close, so its birth and its last
    write are the two ends of the work. Nothing invents a number where there are no such rows.
    """
    out = []
    if not checkpoints_dir:
        return out
    for m in re.finditer(r"(?m)^### (\S+) .+? \u2014 id: (\S+)$", plan):
        if m.group(1) != DONE:
            continue
        nxt = re.search(r"(?m)^#{2,6} ", plan[m.end():])
        block = plan[m.start():m.end() + nxt.start() if nxt else len(plan)]
        group = re.search(r"(?m)^\*\*Group:\*\*\s*([^\u00b7\n]+)", block)
        if not group or group.group(1).strip() != str(scope).strip():
            continue
        cp = _checkpoint_path(checkpoints_dir, m.group(2))
        if not cp.exists():
            continue
        st = cp.stat()
        born = getattr(st, "st_birthtime", st.st_ctime)
        out.append((m.group(2), max(0.0, (st.st_mtime - born) / 60.0)))
    return out


def _estimate(route: dict, plan: str, checkpoints_dir):
    history = comparable_durations(route.get("scope", ""), plan, checkpoints_dir)
    if history:
        low, unit = _span(min(m for _, m in history))
        high, _unit = _span(max(m for _, m in history))
        if _unit != unit:
            low, unit = round(min(m for _, m in history) / 60.0, 1), "hours"
        return low, high, unit, (
            "closed rows %s in the same group, timed off their own checkpoint stamps"
            % ", ".join(i for i, _ in history))
    raw = " ".join(str(route.get("estimate") or "").split())
    m = re.fullmatch(r"([\d.]+)\s*[\u2013\u2014-]\s*([\d.]+)\s+([A-Za-z]+)", raw)
    if not m:
        raise AdmissionError(
            "no comparable closed row in this tree gives an estimate, so the route carries one: "
            "a range with a unit, as \"2%s4 hours\" \u2014 never an invented default" % EN_DASH)
    return m.group(1), m.group(2), m.group(3), (
        "no comparable history in this tree; the range is read off the plan's steps")


def derive_statement(route: dict, plan: str = "", checkpoints_dir=None) -> str:
    """The statement, derived from the route the pipeline already carries — its title, its
    observable outcome, its definition of done — never typed by the person."""
    echo = _echo_name(route)
    description = str(route["observable_outcome"]).strip().rstrip(".")
    steps = _plan_steps(route)
    low, high, unit, basis = _estimate(route, plan, checkpoints_dir)
    written = " ".join(("%s%d) %s" % (PARALLEL + " " if parallel else "", n, text))
                       for n, parallel, text in steps)
    return ("Echo-name: %s. Description: %s. Plan: %s. Estimate: %s%s%s %s \u2014 basis: %s."
            % (echo, description, written, low, EN_DASH, high, unit, basis.rstrip(".")))


def next_task_id(plan: str) -> str:
    nums = [int(num) for prefix, num in TASK_HEADER.findall(plan) if prefix == "q"]
    return "q-%d" % ((max(nums) if nums else 0) + 1)


def render_task(route: dict, task_id: str, statement: str) -> str:
    source = route["source"]["detail"].strip()
    return (
        "### ⬜ {title} — id: {task_id}\n"
        "**Group:** {scope} · **Priority:** normal\n"
        "**Source:** {source}\n\n"
        "**Outcome:** {outcome}\n\n"
        "{statement_prefix} {statement}\n\n"
        "**Done when:** {done}\n\n"
        "{dod_hash_prefix} {dod_hash}\n\n"
        "**Verification:** {verification}\n\n"
        "**Context pointers.** {pointers}\n"
    ).format(
        title=route["title"].strip(), task_id=task_id, scope=route["scope"].strip(),
        source=source, outcome=route["observable_outcome"].strip(),
        statement_prefix=STATEMENT, statement=statement,
        done=route["done_when"].strip(), verification=route["verification"].strip(),
        dod_hash_prefix=DOD_HASH, dod_hash=dod_digest(route["done_when"]),
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
    task = render_task(route, task_id, derive_statement(route, plan, checkpoints_dir))
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


# ------------------------------------------------- the definition of done, and its acceptance
# The closure kernel. The done is fixed when the row is admitted; changing it is its own
# operation that keeps the previous text and hash; the executor gives evidence and a verifier
# who is not the holder issues the verdict; and the close reads that receipt rather than any
# agent's sentence. The hash lives on the row, beside the text it hashes — the one place the
# row parser already reads, so there is no second store.

DONE_WHEN = "**Done when:**"
DOD_HASH = "**DOD hash.**"
DOD_HISTORY = "**DOD changed.**"
RECEIPT = "RECEIPT: "
# The heuristic, said plainly here and in `verify --surface`'s own help: a done written in these
# words promises something rendered or published, and a fixture passing is not that thing.
SURFACE_WORDS = re.compile(
    r"(?i)\b(page|board\.html|link|published|publishes|rendered|renders|url)\b")


def dod_digest(text: str) -> str:
    """The done's sha256, over its own words with runs of whitespace collapsed — so a rewrap
    is not a change and a reworded condition is."""
    return hashlib.sha256(" ".join(str(text).split()).encode("utf-8")).hexdigest()


def read_dod(block: str):
    """(the row's definition of done, the hash recorded beside it or None)."""
    para = _paragraph(block, DONE_WHEN)
    text = " ".join(para[len(DONE_WHEN):].split()) if para else ""
    recorded = _paragraph(block, DOD_HASH)
    return text, (recorded[len(DOD_HASH):].strip() if recorded else None)


def tree_hash(root, exclude=None):
    """(tree, HEAD) — `git write-tree` over a temporary index of the working tree, plus the
    commit it stands on.

    The temporary index is the point: the receipt pins the tree the verifier actually ran
    against, including what is not committed yet, and the real index is never touched. The
    checkpoint directory is left out of the count, because the receipt is written into it — a
    tree that counted its own ledger would differ from itself the moment it was recorded.
    """
    root = Path(root)
    with tempfile.TemporaryDirectory(prefix="live-spec-tree-") as tmp:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(tmp) / "index"))
        run = lambda *a: subprocess.run(("git",) + a, cwd=str(root), env=env,  # noqa: E731
                                        capture_output=True, text=True)
        if run("add", "-A").returncode:
            raise AdmissionError(
                "no git tree at %s: an acceptance receipt pins the exact tree it was written "
                "against, and there is none to pin" % root)
        if exclude:
            try:
                rel = Path(exclude).resolve().relative_to(root.resolve())
            except ValueError:
                rel = None
            if rel:
                run("rm", "--cached", "-r", "-q", "--ignore-unmatch", str(rel))
        written = run("write-tree")
        if written.returncode:
            raise AdmissionError(
                "no git tree at %s: an acceptance receipt pins the exact tree it was written "
                "against, and there is none to pin" % root)
        head = run("rev-parse", "HEAD")
        return written.stdout.strip(), (head.stdout.strip() if not head.returncode else "none")


def read_receipt(cp):
    """The last acceptance receipt written into the checkpoint's DONE section, or None."""
    body = checkpoint.read_checkpoint(cp)["sections"].get("DONE", "")
    for line in reversed(body.splitlines()):
        if line.startswith(RECEIPT):
            try:
                return json.loads(line[len(RECEIPT):])
            except json.JSONDecodeError:
                return None
    return None


def verify(plan_path: Path, checkpoints_dir: Path, task_id: str, by: str,
           commands=(), surfaces=()) -> dict:
    """Write the acceptance receipt: who accepted, when, the tree, the frozen done, the
    commands and the exit code each one actually returned.

    Not a transition. It is the evidence `close` reads instead of an agent's claim, and the one
    thing the producer may not write: `--by` naming the row's own holder is refused.
    """
    by = str(by).strip()
    if not by:
        raise AdmissionError("an acceptance receipt names its verifier: verify --by <name>")
    plan = Path(plan_path).read_text(encoding="utf-8")
    start, end, _, _ = _row_span(plan, task_id)
    block = plan[start:end]

    holder = _holder(block)
    if holder and _same_name(holder, by):
        raise AdmissionError(
            "%s produced this work: the executor may hand over evidence and never issues the "
            "acceptance verdict itself \u2014 verify --by someone who did not hold the row" % by)

    dod, recorded = read_dod(block)
    if recorded and dod_digest(dod) != recorded:
        raise AdmissionError(
            "the definition of done no longer matches the one admitted: the verifier is handed "
            "the frozen done, so correct it as its own operation before accepting anything")
    if SURFACE_WORDS.search(dod) and not surfaces:
        raise AdmissionError(
            "this done names a rendered or published surface, so the receipt names the surface "
            "it was read on: verify --surface <path-or-url>. A fixture passing is not the "
            "surface rendering")
    commands = [str(c) for c in commands if str(c).strip()]
    if not commands:
        raise AdmissionError(
            "an acceptance receipt records the checks it ran: verify --command \"<cmd>\"")

    cp = _checkpoint_path(checkpoints_dir, task_id)
    if not cp.exists() or checkpoint.read_checkpoint(cp)["status"] != "open":
        raise AdmissionError("%s has no open checkpoint to accept" % task_id)

    checks = [[cmd, plan_checks_core.run_key(cmd).returncode] for cmd in commands]
    tree, head = tree_hash(Path(plan_path).resolve().parent, checkpoints_dir)
    receipt = {
        "by": by,
        "at": datetime.datetime.now().isoformat(timespec="seconds"),
        "tree": tree, "head": head, "dod_hash": dod_digest(dod),
        "surfaces": [str(s) for s in surfaces], "checks": checks,
        # The presence of a check is not success. One non-zero exit is a failed verdict.
        "verdict": "passed" if all(code == 0 for _, code in checks) else "failed",
    }
    body = checkpoint.read_checkpoint(cp)["sections"].get("DONE", "")
    kept = [ln for ln in body.splitlines()
            if not ln.startswith(RECEIPT) and not checkpoint._is_empty_body(ln)]
    line = RECEIPT + json.dumps(receipt, ensure_ascii=False)
    checkpoint.update_checkpoint(cp, done="\n".join(kept + [line]).strip())
    return receipt


# ---------------------------------------------------------------- T3..T9, one per transition


def hold(plan_path: Path, task_id: str, holder: str, checkpoints_dir=None, lanes=None) -> None:
    """T2's naming half: a holder takes a ticket that was admitted earlier.

    The checkpoint is already there — `admit` opens it — so this writes the one thing the plan
    itself has to carry while work is in hand: who holds it. T5 and T6 both read it back.

    Take-up is also where three of Requirement 309's clauses land. A row whose statement has not
    passed validation is refused (criterion 49). The wording freezes here, and the row records the
    date it froze (criteria 58-59), which is what `correct` refuses against afterwards. And the
    plan's own parallel expectation meets the lane decision take-up actually makes, the two
    written onto the checkpoint's own LANES line with their divergence named (criterion 46).
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
    block = plan[start:end]
    record = read_validation(block)
    if not record or record["status"] != "ready":
        raise AdmissionError(
            "%s has not passed statement validation: run `validate` (and rewrite the statement "
            "where it failed) before taking it up" % task_id)

    edits = [("**Holder:**", holder)]
    if not _paragraph(block, FROZEN):
        edits.append((FROZEN, "%s.**" % datetime.date.today().isoformat(), VALIDATION))
    _rewrite_row(plan_path, task_id, mark=IN_HAND, edits=edits)

    statement = read_statement(block)
    cp = _checkpoint_path(checkpoints_dir, task_id) if checkpoints_dir else None
    if statement and cp and cp.exists() and checkpoint.read_checkpoint(cp)["status"] == "open":
        expects = parallel_expectation(statement["steps"])
        runs = int(lanes) if lanes else expects
        line = ("LANES: plan expects %d steps side by side; lane decision runs %d; divergence: %s"
                % (expects, runs, "none" if runs == expects else
                   "the plan expected %d side by side and the lane decision runs %d"
                   % (expects, runs)))
        # The line goes in DONE, the delivery trail the close writes into, and not in IN PROGRESS:
        # a close refuses over a non-empty IN PROGRESS, so a lane decision parked there would
        # either block every close or be wiped by whoever cleared the section to get past it —
        # and the divergence it records is exactly what the close has to carry.
        body = checkpoint.read_checkpoint(cp)["sections"].get("DONE", "")
        kept = [ln for ln in body.splitlines()
                if not ln.startswith("LANES:") and not checkpoint._is_empty_body(ln)]
        checkpoint.update_checkpoint(cp, done="\n".join(kept + [line]).strip())


def correct(plan_path: Path, checkpoints_dir: Path, task_id: str,
            goal=None, done=None, statement=None, source=None, reason=None) -> None:
    """T3, the queued half: a queued ticket's goal and done are rewritten where they live.

    A correction to work already in hand belongs on that work's own checkpoint
    (`checkpoint.py update`), which is why this refuses one: two homes for one correction is
    how the plan and the sheet start disagreeing about what the work is.
    """
    if goal is None and done is None and statement is None:
        raise AdmissionError("a correction rewrites the goal, the done, the statement, or several")
    plan = Path(plan_path).read_text(encoding="utf-8")
    start, end, mark, _ = _row_span(plan, task_id)
    if mark != QUEUED:
        frozen = read_statement(plan[start:end])
        raise AdmissionError(
            "%s is not queued: a ticket in hand is corrected on its own checkpoint%s" % (
                task_id,
                "" if not frozen else
                " \u2014 its statement is frozen at take-up and its echo-name stands as \u00ab%s\u00bb"
                % frozen["echo"]))
    edits = []
    if done is not None:
        # The one door through a fixed definition of done, and it leaves a trail: the previous
        # text, the previous hash, who asked and why. Without both flags the change is refused,
        # which is what makes "the DOD cannot be silently changed" a fact rather than a wish.
        if not str(source or "").strip() or not str(reason or "").strip():
            raise AdmissionError(
                "changing the definition of done is its own operation: it names --source (who "
                "asked) and --reason (why), and keeps the previous text and hash on the row")
        old_text, old_hash = read_dod(plan[start:end])
        prior = _paragraph(plan[start:end], DOD_HISTORY)
        prior = prior[len(DOD_HISTORY):].strip() if prior else ""
        entry = ("%s \u00b7 previous: %s \u00b7 previous hash: %s \u00b7 source: %s "
                 "\u00b7 reason: %s"
                 % (datetime.date.today().isoformat(), old_text or "(none)",
                    old_hash or "(none recorded)", str(source).strip(), str(reason).strip()))
        edits.append((DONE_WHEN, str(done).strip()))
        edits.append((DOD_HASH, dod_digest(done), DONE_WHEN))
        edits.append((DOD_HISTORY, (prior + " " + entry).strip(), DOD_HASH))
    if statement is not None:
        # Criterion 61: a revision before take-up runs statement validation again, so the record
        # of the validation the OLD wording passed goes with the wording it judged.
        edits.append((STATEMENT, str(statement).strip()))
        edits.append((VALIDATION, None))
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
    start, end, mark, _ = _row_span(plan, task_id)
    if mark == BLOCKED:
        raise AdmissionError("%s is blocked: clear the block before closing" % task_id)
    cp = _checkpoint_path(checkpoints_dir, task_id)
    if cp.exists() and checkpoint.read_checkpoint(cp)["status"] == "open":
        dod, recorded = read_dod(plan[start:end])
        now = dod_digest(dod)
        if recorded and now != recorded:
            raise AdmissionError(
                "the definition of done changed since it was admitted: rewrite it through "
                "`correct %s --done ... --source ... --reason ...`, never at closing" % task_id)
        receipt = read_receipt(cp)
        if not receipt:
            raise AdmissionError(
                "%s carries no acceptance receipt: close is a state transition against one, not "
                "a claim \u2014 run `verify %s --by <someone who did not hold the row>` first"
                % (task_id, task_id))
        if receipt.get("verdict") != "passed":
            failed = [cmd for cmd, code in receipt.get("checks", []) if code != 0]
            raise AdmissionError(
                "the acceptance receipt is a failed verdict: %s did not pass. The presence of a "
                "check is not success" % ", ".join(failed))
        if receipt.get("dod_hash") != now:
            raise AdmissionError(
                "the definition of done changed after it was verified: the evidence is void, "
                "and %s is verified again against the done as it now reads" % task_id)
        if receipt.get("tree") != tree_hash(Path(plan_path).resolve().parent,
                                           checkpoints_dir)[0]:
            raise AdmissionError(
                "the tree changed after it was verified: the evidence is void, and %s is "
                "verified again against the tree as it now stands" % task_id)
        _write_delivery_trail(plan, task_id, cp)
        try:
            checkpoint.close_checkpoint(cp)
        except ValueError as exc:
            raise AdmissionError(str(exc))
    # The holder stays on the row. T8's fork reads it — a done that turns out false comes back
    # in hand where somebody still holds it, and queued where nobody does.
    _rewrite_row(plan_path, task_id, mark=DONE)


def _write_delivery_trail(plan: str, task_id: str, cp: Path) -> None:
    """Criteria 46 and 63-65: the close writes the time the task was given beside the time it
    took, and the lane divergence take-up recorded, into the trail the delivery report draws on.

    The actual is read off the checkpoint's own stamps — the file is created when the ticket is
    admitted and written again at every transition, the last of which is this close.
    """
    start, end, _, _ = _row_span(plan, task_id)
    statement = read_statement(plan[start:end])
    if not statement:
        return
    st = cp.stat()
    born = getattr(st, "st_birthtime", st.st_ctime)
    minutes = max(0.0, (st.st_mtime - born) / 60.0)
    unit = statement["unit"]
    if unit.lower().startswith("hour"):
        actual = "%.1f %s" % (minutes / 60.0, unit)
    elif unit.lower().startswith("day"):
        actual = "%.1f %s" % (minutes / 1440.0, unit)
    else:
        actual = "%d %s" % (round(minutes), unit)
    body = checkpoint.read_checkpoint(cp)["sections"].get("DONE", "")
    lanes = [ln for ln in body.splitlines() if ln.startswith("LANES:")]
    divergence = lanes[0].split("divergence:")[-1].strip() if lanes \
        else "no lane decision was recorded at take-up"
    trail = ["estimate %s%s%s %s \u2192 actual %s" % (
        statement["low"], EN_DASH, statement["high"], unit, actual),
        "divergence: %s" % divergence]
    kept = [ln for ln in body.splitlines()
            if not ln.startswith("estimate ") and not ln.startswith("divergence: ")]
    checkpoint.update_checkpoint(cp, done="\n".join(kept + trail).strip())


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
    op("hold", ("--holder", True), help="T2 — name the holder of a ticket already admitted"
       ).add_argument("--lanes", type=int,
                      help="how many steps the lane decision actually runs side by side")
    op("validate", ("--reader", False),
       help="run the statement's floor and its clean-context reader, and write the record")
    op("correct", ("--goal", False), ("--done", False), ("--statement", False),
       ("--source", False), ("--reason", False),
       help="T3 — rewrite a queued ticket's goal, done and statement in place; --done also "
            "names --source and --reason, and keeps the previous text and hash")
    accept = op("verify", ("--by", True),
                help="write the acceptance receipt: the frozen done, the exact tree, and the "
                     "exit code each check actually returned")
    accept.add_argument("--command", action="append", default=[], dest="command",
                        help="a check to run, repeatable; any non-zero exit is a failed verdict")
    accept.add_argument("--surface", action="append", default=[], dest="surface",
                        help="a path or URL the acceptance was read on, repeatable. Required "
                             "when the done names a rendered or published surface — the "
                             "words page, board.html, link, published, rendered, url — "
                             "because a fixture passing is not the surface rendering")
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
            hold(plan, args.id, args.holder, checkpoints_dir=cps, lanes=args.lanes)
        elif args.op == "validate":
            print(json.dumps({"status": "ok", **validate(plan, args.id, reader=args.reader)},
                             ensure_ascii=False))
            return 0
        elif args.op == "correct":
            correct(plan, cps, args.id, goal=args.goal, done=args.done,
                    statement=args.statement, source=args.source, reason=args.reason)
        elif args.op == "verify":
            print(json.dumps({"status": "ok", "receipt": verify(
                plan, cps, args.id, args.by, commands=args.command, surfaces=args.surface)},
                ensure_ascii=False))
            return 0
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
        # Every refusal: one plain reason, exit 2, and the row's mark exactly where it was.
        print(json.dumps({"status": "red", "error": str(exc)}, ensure_ascii=False))
        return 2
    print("%s: %s" % (args.op, args.id))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
