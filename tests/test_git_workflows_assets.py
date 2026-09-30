"""The git-workflows skill's example hooks and workflows work as its references say."""

import os
import re
import subprocess
from pathlib import Path

import pytest
import yaml

ASSETS = Path(__file__).resolve().parent.parent / "skills" / "git-workflows" / "assets"
HOOKS = ASSETS / "githooks"
WORKFLOWS = ASSETS / "workflows"
SHA_PIN = re.compile(r"uses: [\w.-]+/[\w.-]+@[0-9a-f]{40} # v\d+\.\d+\.\d+$")


def run(args, cwd=None, env=None, stdin=""):
    return subprocess.run(
        args, cwd=cwd, env=env, input=stdin, capture_output=True, text=True, check=False
    )


def git(repo: Path, *args: str) -> str:
    result = run(["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args], repo)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


@pytest.mark.parametrize(
    ("subject", "code"),
    [
        ("docs: add a changelog", 0),
        ("core/io, docs: explain why the buffer is reused", 0),
        ("Merge branch 'topic'", 0),
        ("fixed stuff", 1),
        ("docs:no space after the colon", 1),
    ],
)
def test_commit_msg_hook(tmp_path, subject, code):
    message = tmp_path / "COMMIT_EDITMSG"
    message.write_text(subject + "\n\nBody.\n", encoding="utf-8")
    assert run(["sh", HOOKS / "commit-msg", message]).returncode == code


def test_commit_msg_hook_notes_a_long_subject_without_refusing(tmp_path):
    message = tmp_path / "COMMIT_EDITMSG"
    message.write_text("core: " + "x" * 60 + "\n", encoding="utf-8")
    result = run(["sh", HOOKS / "commit-msg", message])
    assert result.returncode == 0
    assert "soft limit is 50" in result.stderr


@pytest.mark.parametrize(
    ("pushed", "code"),
    [
        ("refs/heads/topic 1111 refs/heads/main 2222\n", 1),
        ("refs/heads/main 1111 refs/heads/topic 2222\n", 0),
        ("", 0),
    ],
)
def test_pre_push_hook_reads_the_pushed_refs(pushed, code):
    assert run(["sh", HOOKS / "pre-push", "origin", "url"], stdin=pushed).returncode == code


@pytest.mark.parametrize("path", sorted(WORKFLOWS.glob("*.yml")), ids=lambda p: p.name)
def test_workflow_is_narrow_bounded_and_pinned(path):
    text = path.read_text(encoding="utf-8")
    workflow = yaml.safe_load(text)
    assert workflow["permissions"], "every workflow sets permissions"
    assert all("timeout-minutes" in job for job in workflow["jobs"].values())
    uses = [line.strip().removeprefix("- ") for line in text.splitlines() if "uses:" in line]
    assert uses, "each example checks out code"
    assert all(SHA_PIN.fullmatch(line) for line in uses), uses


def step_script(workflow: str, job: str) -> str:
    steps = yaml.safe_load((WORKFLOWS / workflow).read_text(encoding="utf-8"))["jobs"][job]
    [script] = [step["run"] for step in steps["steps"] if "run" in step]
    return script


@pytest.fixture
def repo(tmp_path):
    work = tmp_path / "work"
    remote = tmp_path / "remote.git"
    run(["git", "init", "-q", "--bare", "-b", "main", remote])
    run(["git", "init", "-q", "-b", "main", work])
    git(work, "remote", "add", "origin", str(remote))
    (work / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
    git(work, "add", ".")
    git(work, "commit", "-q", "-m", "docs: start the changelog")
    return work


def commit(repo: Path, subject: str) -> str:
    git(repo, "commit", "-q", "--allow-empty", "-m", subject)
    return git(repo, "rev-parse", "HEAD")


def check_subjects(repo: Path, base: str, head: str) -> int:
    script = step_script("commit-subjects.yml", "subjects")
    env = {**os.environ, "BASE": base, "HEAD": head}
    return run(["bash", "-e", "-c", script], repo, env).returncode


def test_subject_check_passes_good_commits_and_fails_a_bad_one(repo):
    base = git(repo, "rev-parse", "HEAD")
    good = commit(repo, "core: add the parser")
    assert check_subjects(repo, base, good) == 0
    bad = commit(repo, "fixed stuff")
    assert check_subjects(repo, base, bad) == 1


def test_subject_check_fails_when_it_checked_nothing(repo):
    head = git(repo, "rev-parse", "HEAD")
    assert check_subjects(repo, head, head) == 1
    assert check_subjects(repo, "0" * 40, head) != 0


@pytest.mark.parametrize("version", ["", "1.4.0; echo injected", "v1.4.0"])
def test_release_refuses_a_malformed_version(repo, version):
    env = {**os.environ, "VERSION": version}
    assert run(["bash", "-e", "-c", step_script("release.yml", "tag")], repo, env).returncode == 1


def test_release_refuses_a_version_the_changelog_lacks(repo):
    env = {**os.environ, "VERSION": "1.4.0"}
    assert run(["bash", "-e", "-c", step_script("release.yml", "tag")], repo, env).returncode == 1


def test_release_makes_and_pushes_an_annotated_tag(repo):
    (repo / "CHANGELOG.md").write_text(
        "# Changelog\n\n## [1.4.0] - 2026-09-30\n\n### Added\n\n- A parser.\n", encoding="utf-8"
    )
    git(repo, "commit", "-q", "-am", "docs: changelog for 1.4.0")
    env = {**os.environ, "VERSION": "1.4.0"}
    result = run(["bash", "-e", "-c", step_script("release.yml", "tag")], repo, env)
    assert result.returncode == 0, result.stderr
    assert git(repo, "cat-file", "-t", "v1.4.0") == "tag"
    assert "refs/tags/v1.4.0" in git(repo, "ls-remote", "--tags", "origin")
