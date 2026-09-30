"""This repository passes its own checks, and still carries what those checks compare."""

import subprocess
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
    assert report.facts


def test_this_repositorys_workflows_pass_zizmor():
    # The skill tells every repository to scan its workflows in CI, so this one does.
    workflows = sorted(str(path) for path in (ROOT / ".github" / "workflows").glob("*.y*ml"))
    result = subprocess.run(
        ["zizmor", "--offline", *workflows], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stdout + result.stderr
