#!/usr/bin/env python3
"""check-success-measure-feed.py — the success-measure feed's one reader (SPEC INV-324).

A host's own status view is expected to print a shipped feature's live numbers "beside its tasks ...
fetched by the host's own tooling rather than by a person going to look" (PLAN.md row q-48's own
acceptance) — the automatic half of the success-measure promise Requirement 76 opens (`[INV-21]`) and
`spec/success-measure-feed.md`'s Requirement 318 gives its shape. That shape is one small JSON file,
the success-measure feed, any host's own fetch tooling writes. This script is its one reader: it reds
when the fetch was skipped (no feed on disk), when the fetch ran but returned nothing (an empty or
missing metrics list), when the feed has gone stale past the caller's own bound, or when an included
two-variant experiment block is malformed; it passes a well-formed, fresh, non-empty feed.

Writing the fetch tooling itself — reading a host's real analytics account and writing this file — is
each host's own job (Requirement 318, clause 9); so is wiring a host's own status view to run this
checker and print what it confirms (clause 10). This script only reads the feed and says whether it is
fit to print.

THE FEED'S SHAPE, one JSON object:
  generated_at   required, an ISO-8601 timestamp string (`datetime.fromisoformat`-parseable; a
                 trailing "Z" is read as UTC).
  source         required, a non-empty string naming the fetch's own source in plain words (e.g.
                 "ga_report.py against GA4 property 544252011").
  metrics        required, a non-empty list of objects, each carrying "label", "value", and "unit".
  experiment     optional. When present: an object carrying "name" and "variants", "variants" a list
                 of exactly two objects, each carrying "label" and its own non-empty "metrics" list in
                 the same shape as the top-level metrics.

Usage:
  check-success-measure-feed.py <feed.json> <staleness-hours>

Exit 0 and print one OK line naming the metric count (and the experiment, when carried) when the feed
is fresh, well-formed, and non-empty. Exit 1 and print one FAIL line naming the fault — skipped
(no file), malformed (bad JSON or a missing/misshapen required field), empty (no metrics), stale (past
the staleness bound), or a malformed experiment block — when it is not. Stdlib only.
"""
import datetime
import json
import os
import sys

CHECK = "success-measure-feed"


def fail(reason, message):
    print("FAIL (%s.%s): %s" % (CHECK, reason, message))
    return 1


def ok(message):
    print("OK (%s): %s" % (CHECK, message))
    return 0


def parse_timestamp(raw):
    """An ISO-8601 string to an aware datetime, or None on anything unparseable."""
    if not isinstance(raw, str) or not raw:
        return None
    text = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
    try:
        dt = datetime.datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt


def valid_metrics(value):
    """True where `value` is a non-empty list of {label, value, unit} objects."""
    if not isinstance(value, list) or not value:
        return False
    for m in value:
        if not isinstance(m, dict):
            return False
        if not all(k in m for k in ("label", "value", "unit")):
            return False
    return True


def check(feed_path, staleness_hours):
    if not os.path.isfile(feed_path):
        return fail("skipped", "no feed at %s — the fetch never ran" % feed_path)

    try:
        with open(feed_path, encoding="utf-8") as f:
            feed = json.load(f)
    except ValueError as e:
        return fail("malformed", "%s is not valid JSON: %s" % (feed_path, e))
    if not isinstance(feed, dict):
        return fail("malformed", "%s is not a JSON object" % feed_path)

    generated_at = parse_timestamp(feed.get("generated_at"))
    if generated_at is None:
        return fail("malformed",
                     "%s carries no readable generated_at timestamp" % feed_path)

    source = feed.get("source")
    if not isinstance(source, str) or not source.strip():
        return fail("malformed", "%s carries no source naming the fetch" % feed_path)

    if not valid_metrics(feed.get("metrics")):
        return fail("empty",
                     "%s's metrics list is missing or empty — the fetch returned nothing"
                     % feed_path)

    now = datetime.datetime.now(datetime.timezone.utc)
    age_hours = (now - generated_at).total_seconds() / 3600.0

    # A malformed stale_after_hours is a malformed feed whichever caller reads it: validated here,
    # before either branch below decides staleness, rather than only inside the from-feed arm — a
    # caller naming its own bound used to skip this field entirely, so the same feed passed clean
    # for one caller and reddened for the other on the same bytes (F6).
    stated = feed.get("stale_after_hours")
    if stated is not None and (not isinstance(stated, (int, float)) or isinstance(stated, bool)
                                or stated <= 0):
        return fail("malformed",
                    "%s's stale_after_hours must be a positive number, got %r"
                    % (feed_path, stated))

    # The bound belongs to whoever owns the fetch. A caller may name it outright, or pass the
    # literal "from-feed" and let the feed state its own: the tooling that writes a feed is the
    # thing that knows how often it refreshes, and no bound the pack chose for it would mean
    # anything. A feed that states no cadence gets no invented one — the staleness arm stands
    # down by name and every other arm still runs (PLAN q-48).
    if staleness_hours is None:
        if stated is None:
            stale_note = "; the feed states no refresh cadence, so its age is reported and not judged"
        elif age_hours > stated:
            return fail("stale",
                        "%s was generated %.1fh ago, past the %gh cadence the feed itself states"
                        % (feed_path, age_hours, stated))
        else:
            stale_note = ""
    else:
        stale_note = ""
        if age_hours > staleness_hours:
            return fail("stale",
                        "%s was generated %.1fh ago, past the %gh staleness bound"
                        % (feed_path, age_hours, staleness_hours))

    experiment = feed.get("experiment")
    exp_note = ""
    if experiment is not None:
        if not isinstance(experiment, dict):
            return fail("malformed-experiment",
                         "%s's experiment block is not an object" % feed_path)
        variants = experiment.get("variants")
        if not isinstance(variants, list) or len(variants) != 2:
            return fail("malformed-experiment",
                         "%s's experiment carries %s variants, not exactly two"
                         % (feed_path, len(variants) if isinstance(variants, list) else "no"))
        for v in variants:
            if not isinstance(v, dict) or not v.get("label") or not valid_metrics(v.get("metrics")):
                return fail("malformed-experiment",
                             "%s's experiment has a variant with no label or no metrics"
                             % feed_path)
        exp_note = ", experiment %r with %d variants" % (experiment.get("name"), len(variants))

    return ok("%s: %d metric(s) from %r, generated_at %.1fh old%s%s"
              % (feed_path, len(feed["metrics"]), source, age_hours, exp_note, stale_note))


def main(argv):
    if len(argv) != 3:
        print("usage: %s <feed.json> <staleness-hours|from-feed>" % os.path.basename(argv[0]))
        return 2
    if argv[2] == "from-feed":
        return check(argv[1], None)
    try:
        staleness_hours = float(argv[2])
    except ValueError:
        print("staleness-hours must be a number or the word from-feed, got %r" % argv[2])
        return 2
    return check(argv[1], staleness_hours)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
