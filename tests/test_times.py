"""UTC is the stamp, and local times are derived from it (core/times.py)."""

import pytest

from skillcheck.cli import main
from skillcheck.core import times
from skillcheck.core.checks import check_repository

NEW_YORK = "America/New_York"


def findings(repo):
    return [(f.path, f.rule, f.message) for f in check_repository(repo.root).findings]


def written(repo, path: str, text: str) -> None:
    target = repo.root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


@pytest.mark.parametrize(
    ("text", "zone", "expected"),
    [
        ("2026-10-17T00:55Z", NEW_YORK, "2026-10-17 00:55 UTC (8:55 PM EDT, Fri Oct 16)"),
        ("2026-10-17T02:55+02:00", NEW_YORK, "2026-10-17 00:55 UTC (8:55 PM EDT, Fri Oct 16)"),
        ("2026-11-14T23:59:59Z", NEW_YORK, "2026-11-14 23:59 UTC (6:59 PM EST, Sat Nov 14)"),
        # The hour New York's clocks repeat: the same local time, a different zone.
        ("2026-11-01T05:30Z", NEW_YORK, "2026-11-01 05:30 UTC (1:30 AM EDT, Sun Nov 1)"),
        ("2026-11-01T06:30Z", NEW_YORK, "2026-11-01 06:30 UTC (1:30 AM EST, Sun Nov 1)"),
        ("2026-10-19T12:05Z", NEW_YORK, "2026-10-19 12:05 UTC (8:05 AM EDT, Mon Oct 19)"),
        ("2026-10-19T12:05Z", None, "2026-10-19 12:05 UTC"),
    ],
)
def test_a_stamp_is_given_in_utc_and_derived_in_the_zone(text, zone, expected):
    assert times.stamp(text, zone) == expected


@pytest.mark.parametrize(
    ("text", "zone", "message"),
    [
        ("2026-10-17T00:55", NEW_YORK, "names no zone"),
        ("yesterday", NEW_YORK, "not an ISO 8601 time"),
        ("2026-10-17T00:55Z", "Mars/Base", "no time zone named"),
    ],
)
def test_a_stamp_without_its_zone_or_an_unknown_zone_is_refused(text, zone, message):
    with pytest.raises(times.TimeError, match=message):
        times.stamp(text, zone)


def test_the_command_prints_both_or_refuses(capsys):
    assert main(["--time", "2026-10-17T00:55Z", NEW_YORK]) == 0
    assert capsys.readouterr().out == "2026-10-17 00:55 UTC (8:55 PM EDT, Fri Oct 16)\n"
    assert main(["--time", "2026-10-17T00:55"]) == 2
    assert "names no zone" in capsys.readouterr().out
    assert main(["--time", "2026-10-17T00:55Z", NEW_YORK, "extra"]) == 2
    assert "at most one zone" in capsys.readouterr().out
    assert main(["--time", "now"]) == 0
    assert capsys.readouterr().out.endswith(" UTC\n")


def test_times_with_their_zone_pass(repo):
    written(
        repo,
        "docs/notes.md",
        "Merged at 14:05 UTC, released at 2026-10-17T00:55Z, and tagged at 23:59:59 GMT.\n"
        "Seen at 00:55 UTC (8:55 PM EDT, Fri Oct 16).\n"
        "`12:34` in code is left alone.\n\n```text\nat 09:30\n```\n",
    )
    assert findings(repo) == []


def test_a_time_with_no_zone_fires_alone(repo):
    written(repo, "docs/notes.md", "# Notes\n\nIt ran at 12:34 that day.\n")
    assert findings(repo) == [
        (
            "docs/notes.md",
            "times",
            "line 3: 12:34 names no zone; write the stamp in UTC, such as 12:34 UTC",
        )
    ]


def test_each_time_on_a_line_is_checked(repo):
    written(repo, "README.md", "Opened 09:10 UTC, closed 10:20 that day, (8:55 PM EDT) after.\n")
    assert [message for _, _, message in findings(repo)] == [
        "line 1: 10:20 names no zone; write the stamp in UTC, such as 10:20 UTC"
    ]


def test_a_local_time_without_its_utc_stamp_fires(repo):
    written(repo, "README.md", "It closes at 6:59 PM EST, Sat Nov 14.\n")
    assert findings(repo) == [
        (
            "README.md",
            "times",
            "line 1: 6:59 is a local time with no UTC stamp before it on its line",
        )
    ]


def test_past_decisions_and_dated_research_keep_their_words(repo):
    written(
        repo,
        times.DECISIONS,
        "# Decisions\n\n## 2026-10-19 — New\n\nAt 10:00 UTC.\n\n"
        "## 2026-10-18 — Old\n\nRead back at 12:34 that day.\n",
    )
    written(repo, "research/runs/2026-09-23-R01.md", "Released at 09:00 local.\n")
    assert findings(repo) == []
    written(repo, times.DECISIONS, "# Decisions\n\n## 2026-10-19 — New\n\nAt 10:00 that day.\n")
    assert [message for _, _, message in findings(repo)] == [
        "line 5: 10:00 names no zone; write the stamp in UTC, such as 10:00 UTC"
    ]
