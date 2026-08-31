"""What holds the first read of a person's message (SPEC INV-317, matrix M-606).

The spec now says, in its own words, that the first read stands on the reading skill's text and that
no command, gate or hook puts a message through it. Two things must stay true for that sentence to be
worth reading.

The claim must stay honest about the tree. `PRODUCT_SPEC.md`'s criterion says the pack ships no
message-arrival wiring; this file holds the other half — the one arm that DOES execute, so a reader
who takes the criterion at its word finds the arm where the criterion says it is.

And the arm must not lie in the other direction. `scripts/state-probe.sh` prints a score for the
reading at every session's start, computed from runs recorded earlier and stored on disk. A score
whose runs are older than the skill says nothing about the skill as it stands, and the probe marks
it a replay when that is so. Without this proof the probe could quietly lose the comparison and go on
printing a number that reads like a fresh measurement.
"""
import os
import re
import subprocess
import unittest

from conftest import ROOT

PROBE = os.path.join(ROOT, "scripts", "state-probe.sh")
SKILL_PATH = "skills/director/SKILL.md"
TRACES_PATH = "evals/director/traces"
TRACES = os.path.join("evals", "director", "traces")


def probe_text():
    with open(PROBE, encoding="utf-8") as f:
        return f.read()


class TestTheReplayMarker(unittest.TestCase):
    def test_the_probe_compares_the_recorded_runs_against_the_skill(self):
        text = probe_text()
        self.assertIn("evals/director/check.py", text,
                      "the probe no longer runs the grader over the recorded runs")
        self.assertIn("skills/director/SKILL.md", text,
                      "the probe no longer reads the skill it is scoring")
        self.assertIn("evals/director/traces", text,
                      "the probe no longer reads when the runs were recorded")
        # The comparison itself: both commit times are read, so one can be held against the other.
        read_times = set(re.findall(r"git log -1 --format=%ct -- (skills/director/SKILL\.md|"
                                    r"evals/director/traces)", text))
        self.assertEqual(read_times, {SKILL_PATH, TRACES_PATH},
                         "the probe stopped reading both commit times, so nothing can tell a "
                         "replay from a fresh run")

    def test_a_score_over_older_runs_is_printed_as_a_replay(self):
        text = probe_text()
        self.assertIn("REPLAY OF OLD TRACES", text,
                      "the probe prints a score with no word about whether the runs behind it are "
                      "older than the skill")
        self.assertIn("says nothing about today's skill", text,
                      "the replay marker no longer says what a stale score is worth")

    def test_the_label_follows_the_comparison_and_not_the_text_around_it(self):
        """The branch itself, run both ways.

        Every other check in this class reads the probe's source, and source is what a defect leaves
        standing: reversing the comparison keeps both commit-time reads, both marker strings and the
        `$SCORE` line exactly where they are, so a stale score would print bare and a fresh one would
        print as a replay with nothing here going red. So this one lifts the branch out of the script
        and runs it, once with the skill newer than the runs and once the other way. The block is
        found by walking up from the line that prints the marker to the `if` that guards it, which
        keeps this test from naming the operator and re-becoming a source check.
        """
        lines = probe_text().splitlines()
        marker = [i for i, l in enumerate(lines) if "REPLAY OF OLD TRACES" in l]
        self.assertEqual(len(marker), 1, "the replay marker is written in %d places" % len(marker))
        start = next(i for i in range(marker[0], -1, -1) if lines[i].lstrip().startswith("if "))
        end = next(i for i in range(marker[0], len(lines))
                   if lines[i].strip() == "fi" or lines[i].strip().startswith("fi "))
        block_lines = lines[start:end + 1]
        # the branch closes inside a `case` arm, so its `fi` carries the arm's `;;` — that belongs
        # to the enclosing statement, which is not what this test is running
        block_lines[-1] = block_lines[-1].split(";;")[0]
        block = "\n".join(block_lines)

        def run(skill_time, traces_time):
            script = 'SCORE="33 of 35 recorded runs pass"\nSD=%d\nED=%d\n%s\n' % (
                skill_time, traces_time, block)
            return subprocess.run(["bash", "-c", script],
                                  capture_output=True, text=True).stdout

        stale = run(200, 100)
        fresh = run(100, 200)
        self.assertIn("REPLAY OF OLD TRACES", stale,
                      "runs older than the skill printed without the replay label")
        self.assertNotIn("REPLAY OF OLD TRACES", fresh,
                         "runs newer than the skill were labelled a replay, so the label says "
                         "nothing about whether the score is worth reading")
        self.assertIn("33 of 35", fresh, "the score itself stopped reaching the person")

    def test_the_replay_wording_reaches_the_person_beside_the_number(self):
        # The marker rides the same line as the score. Split across two lines it could be printed
        # and scrolled past while the bare number stood in the person's Canon.
        line = [l for l in probe_text().splitlines() if "REPLAY OF OLD TRACES" in l]
        self.assertEqual(len(line), 1, "the replay marker is written in %d places" % len(line))
        self.assertIn("$SCORE", line[0],
                      "the replay marker stands apart from the number it qualifies")


class TestTheOneArmThatExecutes(unittest.TestCase):
    def test_the_grader_runs_without_a_model_call(self):
        # The criterion calls the grader deterministic. A deterministic grader is one a test can run
        # here, offline, and get the same answer from — so run it.
        first = subprocess.run(["python3", os.path.join(ROOT, "evals", "director", "check.py"),
                                "--all"], capture_output=True, text=True, cwd=ROOT)
        second = subprocess.run(["python3", os.path.join(ROOT, "evals", "director", "check.py"),
                                 "--all"], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(first.stdout, second.stdout,
                         "two runs of the grader over the same recorded runs disagree")
        self.assertRegex(first.stdout.strip().splitlines()[-1], r"\d+ of \d+ recorded runs pass",
                         "the grader no longer reports how many recorded runs passed")

    def test_the_recorded_runs_each_answer_a_written_scenario(self):
        traces = os.path.join(ROOT, TRACES)
        self.assertTrue(os.path.isdir(traces), "the recorded runs are gone")
        self.assertTrue([f for f in os.listdir(traces) if f.endswith(".json")],
                        "no run is recorded, so the score the probe prints stands on nothing")
        # The name says EACH scenario, and the count is what makes that true. The grader already
        # says how many scenarios it found no run for, on the same line the probe reads for the
        # score; without this the file could hold one run out of thirty-five and still pass here
        # while the probe went on printing a number the person would read as a measurement.
        result = subprocess.run(["python3", os.path.join(ROOT, "evals", "director", "check.py"),
                                 "--all"], capture_output=True, text=True, cwd=ROOT)
        last = result.stdout.strip().splitlines()[-1]
        self.assertNotIn("no run", last,
                         "a written scenario has no recorded run behind it, so the score speaks "
                         "for fewer scenarios than the number suggests: %s" % last)


if __name__ == "__main__":
    unittest.main()
