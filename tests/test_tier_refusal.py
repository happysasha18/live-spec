"""A dispatch to the expensive tier proves its own need — its red proof (ROADMAP row 507).

The evening of 2026-07-27 spent about a fifth of the weekly budget in half a day, with six of twelve
helper runs on the expensive tier for mechanical work. Comparing task strings tells nobody which tier
a task needs, so the run itself answers first. Three steps, and money is spent only on the middle one:
patterns learned from past refusals turn a task away before any model call; a dispatch that gets
through opens with one instruction — read the task, and stop when a cheaper tier does it as briefed,
naming that tier — and the orchestrator re-runs a refused brief a tier down; the full run proceeds
when both let it through.

The record is the whole evidence. `docs/measure/tier-refusals.md` holds one row per refusal with its
task text, its named tier, its reason, and its date, and `guardrails/tier-refusal.json` holds the
instruction as data plus the phrases promoted from three agreeing refusals.
`guardrails/check-tier-refusal.py` reds a refusal that names no tier or no reason, a pattern promoted
on thin evidence, and a record whose shape broke, and its `--brief` mode is the free step-one check.

Red-first: against a tree without the gate every assertion below fails, the script being absent.
"""
import json
import os
import subprocess
import sys

import pytest

from conftest import ROOT, read

GATE = os.path.join(ROOT, "guardrails", "check-tier-refusal.py")
CONFIG = os.path.join(ROOT, "guardrails", "tier-refusal.json")
RECORD = os.path.join(ROOT, "docs", "measure", "tier-refusals.md")

COLUMNS = ["Id", "Date", "Task", "Named tier", "Reason"]

# Three refusals that agree: the same tier, and one run of words standing in every task text.
AGREEING = [
    ("TR-001", "2026-07-28", "Rename the helper across the tests and report the count",
     "sonnet", "mechanical rename over named files, no design call in it"),
    ("TR-002", "2026-07-28", "Rename the fixture across the tests and update the matrix row",
     "sonnet", "mechanical rename over named files with a stated end state"),
    ("TR-003", "2026-07-29", "Rename the flag across the tests, leaving the prose alone",
     "sonnet", "mechanical rename over named files, the brief names every one"),
]

PROMOTED = {
    "phrase": "rename the",
    "tier": "sonnet",
    "refusals": ["TR-001", "TR-002", "TR-003"],
    "promoted": "2026-07-29",
    "note": "a rename over files the brief names",
}


def _gate(*args):
    return subprocess.run([sys.executable, GATE, *args], capture_output=True, text=True)


def _write(tmp_path, rows=(), patterns=(), columns=COLUMNS, tail=""):
    """A config and a record on disk, at the shape the shipped pair carries."""
    config = json.loads(read("guardrails/tier-refusal.json"))
    config["patterns"] = list(patterns)
    config_path = tmp_path / "tier-refusal.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")

    lines = ["# Fixture record", "", "| " + " | ".join(columns) + " |",
             "|" + "|".join(["---"] * len(columns)) + "|"]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    record_path = tmp_path / "tier-refusals.md"
    record_path.write_text("\n".join(lines) + "\n" + tail, encoding="utf-8")
    return str(config_path), str(record_path)


def _run(tmp_path, rows=(), patterns=(), **kw):
    config, record = _write(tmp_path, rows, patterns, **kw)
    return _gate("--config", config, "--record", record)


def _typed_lines(stdout):
    return [json.loads(line) for line in stdout.splitlines()
            if line.startswith("{") and line.rstrip().endswith("}")]


class TestARefusalOwesItsTierAndItsReason:

    def test_a_refusal_naming_no_tier_reds(self, tmp_path):
        row = ("TR-001", "2026-07-28", "Rename the helper across the tests", "",
               "mechanical rename over named files")
        res = _run(tmp_path, rows=[row])
        assert res.returncode == 1, res.stdout + res.stderr
        assert "names no tier" in res.stdout
        assert "TR-001" in res.stdout

    def test_a_refusal_naming_no_reason_reds(self, tmp_path):
        row = ("TR-001", "2026-07-28", "Rename the helper across the tests", "sonnet", "-")
        res = _run(tmp_path, rows=[row])
        assert res.returncode == 1, res.stdout
        assert "names no reason" in res.stdout

    def test_a_tier_outside_the_ladder_reds(self, tmp_path):
        row = ("TR-001", "2026-07-28", "Rename the helper across the tests", "cheapest",
               "mechanical rename over named files")
        res = _run(tmp_path, rows=[row])
        assert res.returncode == 1, res.stdout
        assert "outside the declared ladder" in res.stdout


class TestAPatternOwesThreeAgreeingRefusals:

    def test_a_pattern_promoted_on_two_refusals_reds(self, tmp_path):
        thin = dict(PROMOTED, refusals=["TR-001", "TR-002"])
        res = _run(tmp_path, rows=AGREEING[:2], patterns=[thin])
        assert res.returncode == 1, res.stdout
        assert "cites 2 refusals where 3 agreeing refusals are required" in res.stdout

    def test_a_pattern_citing_a_row_the_record_lacks_reds(self, tmp_path):
        res = _run(tmp_path, rows=AGREEING[:2], patterns=[PROMOTED])
        assert res.returncode == 1, res.stdout
        assert "TR-003, which the record does not hold" in res.stdout

    def test_a_pattern_whose_refusals_disagree_on_the_tier_reds(self, tmp_path):
        rows = list(AGREEING)
        rows[2] = (rows[2][0], rows[2][1], rows[2][2], "haiku", rows[2][4])
        res = _run(tmp_path, rows=rows, patterns=[PROMOTED])
        assert res.returncode == 1, res.stdout
        assert "while its refusal TR-003 named" in res.stdout

    def test_a_phrase_absent_from_a_cited_task_text_reds(self, tmp_path):
        odd = dict(PROMOTED, phrase="rewrite the glossary")
        res = _run(tmp_path, rows=AGREEING, patterns=[odd])
        assert res.returncode == 1, res.stdout
        assert "carries words the task text of its refusal" in res.stdout


class TestAWellFormedRecordStaysSilent:

    def test_three_agreeing_refusals_and_their_pattern_pass(self, tmp_path):
        res = _run(tmp_path, rows=AGREEING, patterns=[PROMOTED])
        assert res.returncode == 0, res.stdout + res.stderr
        assert "OK (check-tier-refusal)" in res.stdout
        assert "3 recorded refusals and 1 promoted pattern" in res.stdout

    def test_an_empty_record_passes_and_names_its_zero(self, tmp_path):
        """The pattern list starts empty and grows from the record, so zero rows is the declared
        start state and is named rather than passed over (SPEC INV-218)."""
        res = _run(tmp_path)
        assert res.returncode == 0, res.stdout
        assert "the record holds zero refusals" in res.stdout
        assert "permitted empty set" in res.stdout

    def test_the_shipped_record_and_patterns_pass(self):
        res = _gate()
        assert res.returncode == 0, res.stdout + res.stderr
        assert "OK (check-tier-refusal)" in res.stdout


class TestAnUndeclaredPhraseWidthIsNamedRatherThanInvented:
    """A config that omits its phrase width used to fall back to an invented 1-to-99, which passed
    almost any phrase silently. The width is the config's to declare; an absent one is a config
    defect the gate names, the way it already names an absent `refusals_required`."""

    def _config_without_bounds(self, tmp_path, rows, patterns):
        config = json.loads(read("guardrails/tier-refusal.json"))
        config["patterns"] = list(patterns)
        config["promotion"].pop("phrase_min_words")
        config["promotion"].pop("phrase_max_words")
        path = tmp_path / "tier-refusal.json"
        path.write_text(json.dumps(config), encoding="utf-8")
        _, record = _write(tmp_path / "rec", rows=rows)
        return _gate("--config", str(path), "--record", record)

    def test_a_config_with_no_declared_width_reds(self, tmp_path):
        (tmp_path / "rec").mkdir()
        res = self._config_without_bounds(tmp_path, AGREEING, [PROMOTED])
        assert res.returncode == 1, res.stdout
        assert "name no phrase width" in res.stdout

    def test_the_declared_width_still_bounds_a_promoted_phrase(self, tmp_path):
        long_phrase = dict(PROMOTED, phrase=" ".join(["word"] * 12))
        res = _run(tmp_path, rows=AGREEING, patterns=[long_phrase])
        assert res.returncode == 1, res.stdout
        assert "outside the declared 2 to 8" in res.stdout


class TestABrokenRecordReds:

    def test_a_row_with_a_missing_cell_reds(self, tmp_path):
        config, record = _write(tmp_path, rows=AGREEING[:1])
        with open(record, "a", encoding="utf-8") as f:
            f.write("| TR-002 | 2026-07-28 | Rename the fixture | sonnet |\n")
        res = _gate("--config", config, "--record", record)
        assert res.returncode == 1, res.stdout
        assert "cells where the record declares 5" in res.stdout

    def test_a_moved_header_reds(self, tmp_path):
        res = _run(tmp_path, rows=AGREEING, columns=["Id", "Day", "Task", "Tier", "Why"])
        assert res.returncode == 1, res.stdout
        assert "header row naming" in res.stdout

    def test_an_unreadable_date_reds(self, tmp_path):
        row = ("TR-001", "last Tuesday", "Rename the helper across the tests", "sonnet",
               "mechanical rename over named files")
        res = _run(tmp_path, rows=[row])
        assert res.returncode == 1, res.stdout
        assert "unreadable as YYYY-MM-DD" in res.stdout

    def test_a_repeated_id_reds(self, tmp_path):
        rows = list(AGREEING)
        rows[1] = ("TR-001",) + rows[1][1:]
        res = _run(tmp_path, rows=rows, patterns=[])
        assert res.returncode == 1, res.stdout
        assert "used twice" in res.stdout

    def test_an_absent_record_reds(self, tmp_path):
        config, _ = _write(tmp_path)
        res = _gate("--config", config, "--record", str(tmp_path / "no-such-record.md"))
        assert res.returncode == 1, res.stdout
        assert "could not be read" in res.stdout


class TestTheLearnedPatternStep:

    def test_a_matching_task_is_turned_away_with_its_tier_named(self, tmp_path):
        config, _ = _write(tmp_path, rows=AGREEING, patterns=[PROMOTED])
        res = _gate("--config", config, "--brief",
                    "Rename the counter across the tests and report what moved")
        assert res.returncode == 0, res.stdout + res.stderr
        verdict = _typed_lines(res.stdout)[0]
        assert verdict["tier"] == "sonnet"
        assert verdict["phrase"] == "rename the"
        assert verdict["refusals"] == ["TR-001", "TR-002", "TR-003"]
        assert "before any model call" in res.stdout

    def test_the_match_ignores_case_and_punctuation(self, tmp_path):
        config, _ = _write(tmp_path, rows=AGREEING, patterns=[PROMOTED])
        res = _gate("--config", config, "--brief", "RENAME, the counter across every test file")
        assert _typed_lines(res.stdout)[0]["tier"] == "sonnet"

    def test_a_task_matching_nothing_passes_through(self, tmp_path):
        config, _ = _write(tmp_path, rows=AGREEING, patterns=[PROMOTED])
        res = _gate("--config", config, "--brief",
                    "Design the composition axes for a new project kind and argue the trade-offs")
        assert res.returncode == 0, res.stdout
        verdict = _typed_lines(res.stdout)[0]
        assert verdict["tier"] is None
        assert "goes on to the instruction step" in res.stdout

    def test_an_empty_pattern_list_turns_nothing_away(self, tmp_path):
        config, _ = _write(tmp_path)
        res = _gate("--config", config, "--brief", "Rename the counter across the tests")
        assert _typed_lines(res.stdout)[0]["tier"] is None


class TestTheInstructionIsStatedAsData:

    def _config(self):
        return json.loads(read("guardrails/tier-refusal.json"))

    def test_the_instruction_is_one_line_a_brief_pastes(self):
        instruction = self._config()["instruction"]
        assert "\n" not in instruction
        assert instruction.strip() == instruction

    def test_the_instruction_states_the_cheap_tier_as_the_default(self):
        """A run judging its own need leans toward yes, so the line opens on the cheap assumption."""
        instruction = self._config()["instruction"].lower()
        assert instruction.startswith("assume a cheaper tier")

    def test_the_instruction_asks_for_the_tier_and_the_reason(self):
        instruction = self._config()["instruction"]
        assert "REFUSE <tier>:" in instruction
        assert "reason" in instruction

    def test_the_instruction_asks_the_run_to_stop_before_working(self):
        assert "stop before any other work" in self._config()["instruction"]

    def test_the_pattern_list_starts_empty_and_the_record_is_its_source(self):
        config = self._config()
        assert config["patterns"] == []
        assert config["record"] == "docs/measure/tier-refusals.md"

    def test_the_promotion_threshold_is_three_agreeing_refusals(self):
        assert self._config()["promotion"]["refusals_required"] == 3

    def test_the_ladder_runs_cheapest_first(self):
        assert self._config()["tiers"][-1] == "opus"


class TestTheRecordSaysHowARowIsWritten:

    def test_the_record_carries_the_declared_header(self):
        header = "| " + " | ".join(COLUMNS) + " |"
        assert header in read("docs/measure/tier-refusals.md")

    @pytest.mark.parametrize("needle", [
        "One row per refusal",
        "re-runs the same brief a tier down",
        "guardrails/tier-refusal.json",
        "docs/measure/2026-07-28-tier-routing-experiment.md",
    ])
    def test_the_record_states_its_own_shape(self, needle):
        assert needle in read("docs/measure/tier-refusals.md")


class TestTheGateContract:

    def test_the_header_declares_the_gate_blocking(self):
        assert "BLOCKING" in read("guardrails/check-tier-refusal.py")[:4000]

    def test_a_red_carries_one_typed_line(self, tmp_path):
        row = ("TR-001", "2026-07-28", "Rename the helper across the tests", "",
               "mechanical rename over named files")
        res = _run(tmp_path, rows=[row])
        objects = _typed_lines(res.stdout)
        assert len(objects) == 1, "a blocking red emits exactly one JSON object"
        record = objects[0]
        assert record["severity"] == "error"
        assert record["code"].startswith("tier-refusal-")
        assert "TR-001" in record["message"]
        assert record["fix"]

    def test_the_green_line_declares_its_reach(self, tmp_path):
        res = _run(tmp_path, rows=AGREEING, patterns=[PROMOTED])
        assert "Id, Date, Task, Named tier, Reason" in res.stdout, "the columns it read"
        assert "calls no model" in res.stdout, "and what stays outside the reach"


class TestTheExperimentRecord:

    DOC = "docs/measure/2026-07-28-tier-routing-experiment.md"

    @pytest.mark.parametrize("needle", [
        "Hypothesis",
        "Measures",
        "Baseline",
        "Decision rule",
        "2026-08-04",
    ])
    def test_the_experiment_states_itself_before_the_data(self, needle):
        assert needle in read(self.DOC)

    def test_the_baseline_the_row_recorded_is_carried(self):
        text = read(self.DOC).lower()
        assert "twelve helper runs" in text
        assert "two million output units" in text
        assert "zero refusals" in text
