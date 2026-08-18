"""Chat clock's mechanical hand (row 134, SPEC INV-24 chat face).

The reply-leading [HH:MM] stops being handwritten: a harness hook script reads
the wall clock at write time and prints it into the prompt context, so the
stamp is read off the machine, never continued or extrapolated from an
earlier stamp (INV-24). This test proves the script on disk, its output
carrying the live machine time, and the law it states in its own words.

Zero dependencies beyond the stdlib; run from the repo root:
  python3 -m pytest -q tests
"""

import datetime
import os
import re
import subprocess
import unittest

from conftest import ROOT
SCRIPT = os.path.join(ROOT, "hooks", "clock-hook.sh")


def run(args, *, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


class TestClockHookScript(unittest.TestCase):
    def test_script_exists_and_executable(self):
        self.assertTrue(os.path.isfile(SCRIPT), "missing script: %s" % SCRIPT)
        self.assertTrue(os.access(SCRIPT, os.X_OK), "%s is not executable" % SCRIPT)

    def test_output_carries_current_machine_time(self):
        result = run([SCRIPT], cwd=ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        stdout = result.stdout

        time_match = re.search(r"(\d{2}):(\d{2})", stdout)
        self.assertIsNotNone(time_match, "no HH:MM found in output: %r" % stdout)
        hour, minute = int(time_match.group(1)), int(time_match.group(2))

        date_match = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", stdout)
        self.assertIsNotNone(date_match, "no DD.MM.YYYY found in output: %r" % stdout)
        day, month, year = (
            int(date_match.group(1)),
            int(date_match.group(2)),
            int(date_match.group(3)),
        )

        now = datetime.datetime.now()
        self.assertEqual((year, month, day), (now.year, now.month, now.day),
                          "script date does not match today")

        script_minutes = hour * 60 + minute
        now_minutes = now.hour * 60 + now.minute
        diff = abs(script_minutes - now_minutes)
        wrap_diff = min(diff, 1440 - diff)  # wrap-tolerant (e.g. 00:00 vs 23:59)
        self.assertLessEqual(wrap_diff, 1,
                              "script time %02d:%02d not within 1 minute of now %02d:%02d"
                              % (hour, minute, now.hour, now.minute))

    def test_output_carries_the_law(self):
        result = run([SCRIPT], cwd=ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("[HH:MM]", result.stdout)
        self.assertIn("never a continued or extrapolated stamp", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
