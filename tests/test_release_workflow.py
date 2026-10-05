"""This repository's release workflow publishes its page from the tag, and can run again."""

import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "release.yml"
PUBLISH = "Publish the release page from the tag"


def publish(tmp_path: Path, page_exists: bool) -> list[list[str]]:
    """Run the step with a stand-in gh that records each call; return the calls."""
    jobs = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))["jobs"]
    [script] = [s["run"] for s in jobs["page"]["steps"] if s.get("name") == PUBLISH]
    files = tmp_path / "release"
    files.mkdir()
    for name in ("KICKSTART.md", "bom.json", "notes.md", "one.zip", "two.zip"):
        (files / name).write_text(name, encoding="utf-8")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    log = tmp_path / "calls.txt"
    gh = bin_dir / "gh"
    gh.write_text(
        f"#!{sys.executable}\n"
        "import sys\n"
        f"with open({str(log)!r}, 'a') as calls:\n"
        "    calls.write('\\t'.join(sys.argv[1:]) + '\\n')\n"
        f"if sys.argv[1:3] == ['release', 'view'] and not {page_exists}:\n"
        "    sys.exit(1)\n",
        encoding="utf-8",
    )
    gh.chmod(0o755)
    env = {
        **os.environ,
        "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        "GITHUB_REPOSITORY": "example/repo",
        "VERSION": "1.4.0",
    }
    result = subprocess.run(
        ["bash", "-e", "-c", script], cwd=tmp_path, env=env, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    return [line.split("\t") for line in log.read_text(encoding="utf-8").splitlines()]


FILES = ["release/KICKSTART.md", "release/bom.json", "release/one.zip", "release/two.zip"]
REPO = ["--repo", "example/repo"]


@pytest.mark.parametrize(
    ("page_exists", "after_view"),
    [
        (
            False,
            [
                ["release", "create", "v1.4.0", *FILES, *REPO, "--verify-tag", "--title", "v1.4.0"]
                + ["--notes-file", "release/notes.md"]
            ],
        ),
        (
            True,
            [
                ["release", "upload", "v1.4.0", *FILES, *REPO, "--clobber"],
                ["release", "edit", "v1.4.0", *REPO, "--notes-file", "release/notes.md"],
            ],
        ),
    ],
)
def test_the_page_is_made_from_the_tag_or_updated_by_a_second_attempt(
    tmp_path, page_exists, after_view
):
    calls = publish(tmp_path, page_exists)
    assert calls[0] == ["release", "view", "v1.4.0", *REPO]
    assert calls[1:] == after_view
