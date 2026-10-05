"""This repository passes its own checks, and still carries what those checks compare."""

import re
import subprocess
from collections import defaultdict
from pathlib import Path

import pytest
import yaml

from skillcheck.core.checks import check_repository

ROOT = Path(__file__).resolve().parent.parent
# The workflows this repository runs, and the ones its skills ship for other repositories.
RUN = sorted((ROOT / ".github" / "workflows").glob("*.y*ml"))
SHIPPED = sorted(ROOT.glob("skills/*/assets/workflows/*.y*ml"))
USES = re.compile(r"uses: ([\w.-]+/[\w.-]+)@([0-9a-f]{40}) # (v\d+\.\d+\.\d+)$")


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
    # The skill tells every repository to scan its workflows in CI, so this one does, and the
    # ones its skills ship.
    workflows = [str(path) for path in RUN + SHIPPED]
    result = subprocess.run(
        ["zizmor", "--offline", *workflows], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("path", RUN + SHIPPED, ids=lambda path: path.relative_to(ROOT).as_posix())
def test_each_workflow_is_narrow_bounded_and_pinned(path):
    text = path.read_text(encoding="utf-8")
    workflow = yaml.safe_load(text)
    # Wider grants belong to the job that needs them, never to the whole workflow.
    assert workflow["permissions"] == {"contents": "read"}
    assert all("timeout-minutes" in job for job in workflow["jobs"].values())
    uses = [line.strip().removeprefix("- ") for line in text.splitlines() if "uses:" in line]
    assert uses, "each workflow checks out code"
    assert all(USES.fullmatch(line) for line in uses), uses
    steps = [step for job in workflow["jobs"].values() for step in job["steps"]]
    checkouts = [step for step in steps if step.get("uses", "").startswith("actions/checkout@")]
    assert all(step["with"]["persist-credentials"] is False for step in checkouts)


def test_each_action_is_pinned_to_one_commit_everywhere():
    # Dependabot moves the pins in .github/workflows only, so a skill's copies follow by hand.
    pins = defaultdict(set)
    for path in RUN + SHIPPED:
        for line in path.read_text(encoding="utf-8").splitlines():
            found = USES.fullmatch(line.strip().removeprefix("- "))
            if found:
                pins[found[1]].add(found[2] + " # " + found[3])
    assert pins
    split = {action: sorted(found) for action, found in pins.items() if len(found) > 1}
    assert not split, (
        "pin each action to the commit this repository's own workflows use, in the skills' "
        f"assets/workflows too: {split}"
    )
