"""A project's own live numbers print beside its rows, without a person going to look.

PLAN.md row q-48. The pack's shipped status renderer reads a project's own
`.live-spec/success-measure-feed.json` through the pack's one checker,
`scripts/check-success-measure-feed.py`, and prints only what that checker confirms. A fetch that
was skipped, came back empty, or went stale past the cadence the feed itself states says so in the
checker's own words rather than printing numbers nobody can trust — the red-when-empty half
Requirement 318 promises, now visible where a person actually reads.

Writing the fetch tooling that fills a feed from a real analytics account stays each host's own
job. These cases prove the printing half, which the pack owns.
"""
import datetime
import json
import os
import subprocess
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TheRendererPrintsAProjectsLiveNumbers(unittest.TestCase):
    """A project's own numbers print beside its rows without a person going to look (PLAN q-48).

    The renderer reads `.live-spec/success-measure-feed.json` through the pack's own checker and
    prints only what that checker confirms. A skipped, empty or stale fetch says so in the
    checker's own words instead of printing numbers nobody can trust — the red-when-empty half
    Requirement 318 promises, now visible where a person actually reads.
    """

    PLAN = """# demo — Plan

## Tasks

### ⬜ A row of the host's own — id: d-1
**Group:** G · **Priority:** normal
**Source:** the fixture.
"""

    def _host(self, feed_body, vendor_checker=True):
        host = tempfile.mkdtemp(prefix="livespec-feed-view-")
        subprocess.run(["git", "init", "-q"], cwd=host, check=True)
        os.makedirs(os.path.join(host, "scripts"), exist_ok=True)
        os.makedirs(os.path.join(host, ".live-spec"), exist_ok=True)
        files = [("scaffold/status-view/state-probe.sh", "scripts/state-probe.sh"),
                 ("scripts/plan_checks_core.py", "scripts/plan_checks_core.py"),
                 ("scaffold/status-view/plan_checks.py", "scripts/plan_checks.py")]
        if vendor_checker:
            files.append(("scripts/check-success-measure-feed.py",
                          "scripts/check-success-measure-feed.py"))
        for src, dst in files:
            with open(os.path.join(REPO, src), encoding="utf-8") as fh:
                body = fh.read()
            with open(os.path.join(host, dst), "w", encoding="utf-8") as fh:
                fh.write(body)
        with open(os.path.join(host, "PLAN.md"), "w", encoding="utf-8") as fh:
            fh.write(self.PLAN)
        if feed_body is not None:
            with open(os.path.join(host, ".live-spec", "success-measure-feed.json"),
                      "w", encoding="utf-8") as fh:
                json.dump(feed_body, fh)
        r = subprocess.run(["bash", os.path.join(host, "scripts", "state-probe.sh")],
                           cwd=host, capture_output=True, text=True)
        return r.stdout + r.stderr

    @staticmethod
    def _feed(age_hours=1, cadence=24, metrics=None):
        now = datetime.datetime.now(datetime.timezone.utc)
        body = {"generated_at": (now - datetime.timedelta(hours=age_hours)).isoformat(),
                "source": "ga_report.py against a fixture property",
                "metrics": metrics if metrics is not None
                else [{"label": "visitors", "value": 21, "unit": "sessions/day"}]}
        if cadence is not None:
            body["stale_after_hours"] = cadence
        return body

    def test_a_confirmed_feed_prints_its_numbers_and_its_source(self):
        out = self._host(self._feed())
        self.assertIn("SINCE IT SHIPPED", out)
        self.assertIn("visitors: 21 sessions/day", out)
        self.assertIn("ga_report.py against a fixture property", out)

    def test_a_two_variant_experiment_prints_both_variants(self):
        body = self._feed()
        body["experiment"] = {"name": "hero copy", "variants": [
            {"label": "A", "metrics": [{"label": "signups", "value": 3, "unit": "per day"}]},
            {"label": "B", "metrics": [{"label": "signups", "value": 5, "unit": "per day"}]}]}
        out = self._host(body)
        self.assertIn("experiment hero copy", out)
        self.assertIn("A — signups 3 per day", out)
        self.assertIn("B — signups 5 per day", out)

    def test_a_fetch_that_returned_nothing_says_so_instead_of_printing(self):
        out = self._host(self._feed(metrics=[]))
        self.assertIn("SINCE IT SHIPPED", out)
        self.assertNotIn("visitors", out)
        self.assertIn("empty", out)

    def test_a_feed_past_its_own_cadence_says_so_instead_of_printing(self):
        out = self._host(self._feed(age_hours=48, cadence=24))
        self.assertIn("SINCE IT SHIPPED", out)
        self.assertNotIn("visitors: 21", out)
        self.assertIn("cadence the feed itself states", out)

    def test_a_project_with_no_feed_prints_no_such_section(self):
        out = self._host(None)
        self.assertNotIn("SINCE IT SHIPPED", out)

    def test_a_feed_with_no_checker_vendored_says_so_instead_of_printing_nothing(self):
        # Before F5, an adopting host that never got scripts/check-success-measure-feed.py
        # vendored saw the whole section print nothing at all — indistinguishable from carrying
        # no feed (Requirement 318 clause 12's silence, wrongly reused for a different case).
        out = self._host(self._feed(), vendor_checker=False)
        self.assertIn("SINCE IT SHIPPED", out)
        self.assertNotIn("visitors: 21", out)
        self.assertIn("check-success-measure-feed.py", out)
        self.assertIn("missing", out)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
