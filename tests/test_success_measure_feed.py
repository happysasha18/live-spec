"""The success-measure feed's one reader (SPEC INV-324, spec/success-measure-feed.md Requirement 318).

`scripts/check-success-measure-feed.py` passes a fresh, well-formed, non-empty feed and reds a skipped
fetch (no file), an empty fetch (no metrics), a stale feed, a malformed feed, and a malformed
two-variant experiment block. This is the row-q-48 pack-side reading machinery Requirement 76 promises
(`[INV-21]`) — the automatic half beside the human-triggered field-evidence route
(`test_feedback_routes_have_homes`).
"""
import datetime
import json
import os
import subprocess
import tempfile
import unittest

from conftest import ROOT

SCRIPT = os.path.join(ROOT, "scripts", "check-success-measure-feed.py")


def run(*args):
    return subprocess.run(["python3", SCRIPT, *args], capture_output=True, text=True)


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")


def now_iso(hours_ago=0.0):
    return iso(datetime.datetime.now(datetime.timezone.utc)
               - datetime.timedelta(hours=hours_ago))


GOOD_METRICS = [{"label": "sessions (7d)", "value": 21, "unit": "sessions"}]
GOOD_EXPERIMENT = {
    "name": "hero-copy-ab",
    "variants": [
        {"label": "A", "metrics": [{"label": "conversions", "value": 12, "unit": "count"}]},
        {"label": "B", "metrics": [{"label": "conversions", "value": 18, "unit": "count"}]},
    ],
}


class TestSuccessMeasureFeed(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def feed_path(self, name="feed.json"):
        return os.path.join(self.tmp.name, name)

    def write(self, data, name="feed.json"):
        path = self.feed_path(name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        return path

    def test_reds_a_skipped_fetch(self):
        # No file at all — the fetch never ran.
        missing = self.feed_path("nothing-here.json")
        r = run(missing, "24")
        self.assertNotEqual(r.returncode, 0, "passed a missing feed:\n%s" % r.stdout)
        self.assertIn("skipped", r.stdout)

    def test_reds_an_empty_fetch(self):
        path = self.write({"generated_at": now_iso(), "source": "ga_report.py", "metrics": []})
        r = run(path, "24")
        self.assertNotEqual(r.returncode, 0, "passed an empty metrics list:\n%s" % r.stdout)
        self.assertIn("empty", r.stdout)

    def test_reds_a_missing_metrics_field(self):
        path = self.write({"generated_at": now_iso(), "source": "ga_report.py"})
        r = run(path, "24")
        self.assertNotEqual(r.returncode, 0, "passed a feed with no metrics field:\n%s" % r.stdout)
        self.assertIn("empty", r.stdout)

    def test_reds_a_stale_feed(self):
        path = self.write({"generated_at": now_iso(hours_ago=48), "source": "ga_report.py",
                            "metrics": GOOD_METRICS})
        r = run(path, "24")
        self.assertNotEqual(r.returncode, 0, "passed a 48h-old feed against a 24h bound:\n%s"
                            % r.stdout)
        self.assertIn("stale", r.stdout)

    def test_reds_malformed_json(self):
        path = self.feed_path()
        with open(path, "w", encoding="utf-8") as f:
            f.write("{not json")
        r = run(path, "24")
        self.assertNotEqual(r.returncode, 0, "passed unparseable JSON:\n%s" % r.stdout)
        self.assertIn("malformed", r.stdout)

    def test_reds_a_missing_generated_at(self):
        path = self.write({"source": "ga_report.py", "metrics": GOOD_METRICS})
        r = run(path, "24")
        self.assertNotEqual(r.returncode, 0, "passed a feed with no generated_at:\n%s" % r.stdout)
        self.assertIn("malformed", r.stdout)

    def test_reds_a_missing_source(self):
        path = self.write({"generated_at": now_iso(), "metrics": GOOD_METRICS})
        r = run(path, "24")
        self.assertNotEqual(r.returncode, 0, "passed a feed with no source:\n%s" % r.stdout)
        self.assertIn("malformed", r.stdout)

    def test_reds_an_experiment_with_one_variant(self):
        bad = dict(GOOD_EXPERIMENT, variants=GOOD_EXPERIMENT["variants"][:1])
        path = self.write({"generated_at": now_iso(), "source": "ga_report.py",
                            "metrics": GOOD_METRICS, "experiment": bad})
        r = run(path, "24")
        self.assertNotEqual(r.returncode, 0, "passed a one-variant experiment:\n%s" % r.stdout)
        self.assertIn("malformed-experiment", r.stdout)

    def test_reds_an_experiment_variant_with_no_metrics(self):
        bad_variants = [{"label": "A", "metrics": []}, {"label": "B", "metrics": GOOD_METRICS}]
        bad = dict(GOOD_EXPERIMENT, variants=bad_variants)
        path = self.write({"generated_at": now_iso(), "source": "ga_report.py",
                            "metrics": GOOD_METRICS, "experiment": bad})
        r = run(path, "24")
        self.assertNotEqual(r.returncode, 0, "passed an empty-metrics variant:\n%s" % r.stdout)
        self.assertIn("malformed-experiment", r.stdout)

    def test_passes_a_fresh_well_formed_feed(self):
        path = self.write({"generated_at": now_iso(), "source": "ga_report.py against GA4 property "
                                                                  "544252011",
                            "metrics": GOOD_METRICS})
        r = run(path, "24")
        self.assertEqual(r.returncode, 0, "red a well-formed fresh feed:\n%s" % r.stdout)
        self.assertIn("OK", r.stdout)

    def test_passes_a_fresh_feed_carrying_a_two_variant_experiment(self):
        path = self.write({"generated_at": now_iso(), "source": "ga_report.py",
                            "metrics": GOOD_METRICS, "experiment": GOOD_EXPERIMENT})
        r = run(path, "24")
        self.assertEqual(r.returncode, 0, "red a well-formed feed with a valid experiment:\n%s"
                         % r.stdout)
        self.assertIn("experiment", r.stdout)

    def test_a_trailing_z_timestamp_is_read_as_utc(self):
        z = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        path = self.write({"generated_at": z, "source": "ga_report.py", "metrics": GOOD_METRICS})
        r = run(path, "24")
        self.assertEqual(r.returncode, 0, "red a Z-suffixed timestamp:\n%s" % r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
