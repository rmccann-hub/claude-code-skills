"""This repository passes its own checks, and still carries what those checks compare."""

from pathlib import Path

from skillcheck.core.checks import check_repository

ROOT = Path(__file__).resolve().parent.parent


def test_this_repository_passes_its_own_checks():
    report = check_repository(ROOT)
    assert report.findings == []
    # Deleting the roadmap, the README's skill table or the standard would otherwise switch
    # their checks off silently, which reads exactly like passing them.
    assert report.roadmap_entries
    assert report.readme_entries
    assert report.standard_version is not None
