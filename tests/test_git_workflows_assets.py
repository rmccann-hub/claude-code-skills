"""The git-workflows skill's example hooks, workflows and rulesets work as its references say."""

import fnmatch
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from skillcheck import release

ASSETS = Path(__file__).resolve().parent.parent / "skills" / "git-workflows" / "assets"
HOOKS = ASSETS / "githooks"
WORKFLOWS = ASSETS / "workflows"
RULESETS = ASSETS / "rulesets"
# What GitHub's starter rulesets carry, and its export less the IDs a repository assigns.
RULESET_FIELDS = {"name", "target", "enforcement", "conditions", "rules", "bypass_actors"}
# The pull request rule's parameters that GitHub's REST API marks required.
PULL_REQUEST_PARAMETERS = {
    "dismiss_stale_reviews_on_push",
    "require_code_owner_review",
    "require_last_push_approval",
    "required_approving_review_count",
    "required_review_thread_resolution",
}
SUBJECTS_STEP = 'Check that each commit subject reads "area: summary"'
RELEASE_CHECK = "Check the version, the commit and its changelog"
RELEASE_CHECKS_PASSED = "Check that every check on the commit has passed"
RELEASE_WORKFLOWS = "Check that a branch has the commit's workflow files"
RELEASE_TAG = "Make the annotated tag and push it"
COMPLETION_GUARD = "Prove the suite ran to the end"


def run(args, cwd=None, env=None, stdin=""):
    return subprocess.run(
        args, cwd=cwd, env=env, input=stdin, capture_output=True, text=True, check=False
    )


def git(repo: Path, *args: str) -> str:
    result = run(["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args], repo)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


@pytest.mark.parametrize(
    ("message", "code"),
    [
        ("docs: add a changelog\n\nBody.\n", 0),
        ("core/io, docs: explain why the buffer is reused\n", 0),
        ("Merge branch 'topic'\n", 0),
        ('Revert "core: add the parser"\n', 0),
        ('Reapply "core: add the parser"\n', 0),
        ("fixup! core: add the parser\n", 0),
        ("fixed stuff\n", 1),
        ("docs:no space after the colon\n", 1),
        # Git hands the hook the message before it strips comments and blank lines.
        ("# From the commit template\n\ncore: add the parser\n", 0),
        ("\n\ncore: add the parser\n", 0),
        ("# From the commit template\nfixed stuff\n", 1),
    ],
)
def test_commit_msg_hook(tmp_path, message, code):
    path = tmp_path / "COMMIT_EDITMSG"
    path.write_text(message, encoding="utf-8")
    assert run(["sh", HOOKS / "commit-msg", path], tmp_path).returncode == code


def test_commit_msg_hook_notes_a_long_subject_without_refusing(tmp_path):
    message = tmp_path / "COMMIT_EDITMSG"
    message.write_text("core: " + "x" * 60 + "\n", encoding="utf-8")
    result = run(["sh", HOOKS / "commit-msg", message], tmp_path)
    assert result.returncode == 0
    assert "soft limit is 50" in result.stderr


def test_commit_msg_hook_works_through_git_commit(tmp_path):
    work = tmp_path / "work"
    run(["git", "init", "-q", "-b", "main", work])
    shutil.copytree(HOOKS, work / ".githooks")
    git(work, "config", "core.hooksPath", ".githooks")
    (work / "a").write_text("a\n", encoding="utf-8")
    git(work, "add", "a")
    refused = run(
        [
            "git",
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@example.com",
            "commit",
            "-q",
            "-m",
            "fixed stuff",
        ],
        work,
    )
    assert refused.returncode == 1
    assert "should read 'area: summary'" in refused.stderr
    # An editor leaves the template's comment first; Git strips it after the hook has run.
    edited = tmp_path / "edited"
    edited.write_text("# From the commit template\n\ncore: add a\n", encoding="utf-8")
    env = {**os.environ, "GIT_EDITOR": f"cp {edited}"}
    accepted = run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-q"], work, env
    )
    assert accepted.returncode == 0, accepted.stderr
    assert git(work, "log", "-1", "--format=%s") == "core: add a"


@pytest.mark.parametrize("hook", sorted(HOOKS.iterdir()), ids=lambda p: p.name)
def test_hooks_are_committed_executable(hook):
    # Git runs no hook that isn't executable, and says so only as a hint.
    assert hook.stat().st_mode & stat.S_IXUSR


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


# Each example is narrow, bounded, pinned and clean under zizmor: tests/test_repository.py
# holds every workflow a skill ships to that, with the ones this repository runs.


def ruleset(name: str) -> dict:
    return json.loads((RULESETS / name).read_text(encoding="utf-8"))


@pytest.mark.parametrize("path", sorted(RULESETS.glob("*.json")), ids=lambda p: p.name)
def test_ruleset_imports_into_any_repository(path):
    rules = json.loads(path.read_text(encoding="utf-8"))
    # No ID, source or required check: each belongs to one repository.
    assert set(rules) == RULESET_FIELDS
    assert rules["enforcement"] == "active"
    assert rules["bypass_actors"] == []
    assert set(rules["conditions"]) == {"ref_name"}
    types = [rule["type"] for rule in rules["rules"]]
    assert len(types) == len(set(types))
    assert {"deletion", "non_fast_forward"} <= set(types)
    assert "required_status_checks" not in types


def test_default_branch_ruleset_requires_a_pull_request_and_no_approval():
    rules = ruleset("default-branch.json")
    assert rules["target"] == "branch"
    assert rules["conditions"]["ref_name"]["include"] == ["~DEFAULT_BRANCH"]
    [parameters] = [r["parameters"] for r in rules["rules"] if r["type"] == "pull_request"]
    assert set(parameters) == PULL_REQUEST_PARAMETERS
    assert parameters.pop("required_approving_review_count") == 0
    assert not any(parameters.values())


def test_release_tag_ruleset_covers_the_tag_the_release_job_makes(repo):
    rules = ruleset("release-tags.json")
    assert rules["target"] == "tag"
    # Creation stays open, or the release job couldn't make the tag at all.
    assert {rule["type"] for rule in rules["rules"]} == {"update", "deletion", "non_fast_forward"}
    sha = changelog_commit(repo)
    result = release_step(repo, RELEASE_TAG, VERSION="1.4.0", SHA=sha, GH_TOKEN="CHANGEME")
    assert result.returncode == 0, result.stderr
    refs = git(repo, "ls-remote", "--tags", "origin").splitlines()
    [made] = [line.split()[1] for line in refs if not line.endswith("^{}")]
    assert any(fnmatch.fnmatchcase(made, p) for p in rules["conditions"]["ref_name"]["include"])


def test_the_kickstart_file_names_each_ruleset_a_release_carries():
    named = set(re.findall(r"ruleset-[\w-]+\.json", release.INSTRUCTIONS.read_text("utf-8")))
    assert named == {f"ruleset-{path.stem}.json" for path in RULESETS.glob("*.json")}


def step_script(workflow: str, job: str, name: str) -> str:
    steps = yaml.safe_load((WORKFLOWS / workflow).read_text(encoding="utf-8"))["jobs"][job]
    [script] = [step["run"] for step in steps["steps"] if step.get("name") == name]
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
    git(work, "push", "-q", "origin", "main")
    return work


def commit(repo: Path, subject: str) -> str:
    git(repo, "commit", "-q", "--allow-empty", "-m", subject)
    return git(repo, "rev-parse", "HEAD")


def check_subjects(repo: Path, base: str, head: str):
    script = step_script("commit-subjects.yml", "subjects", SUBJECTS_STEP)
    env = {**os.environ, "BASE": base, "HEAD": head}
    return run(["bash", "-e", "-c", script], repo, env)


def test_this_repository_runs_the_shipped_subject_check():
    # The repository checks its own commits with the example, unchanged.
    own = ASSETS.parents[2] / ".github" / "workflows" / "commit-subjects.yml"
    assert own.read_bytes() == (WORKFLOWS / "commit-subjects.yml").read_bytes()


def test_subject_check_passes_dependabot_subjects_with_a_prefix(repo):
    base = git(repo, "rev-parse", "HEAD")
    head = commit(repo, "deps: Bump ruff from 0.16.8 to 0.16.10 in the python group")
    assert check_subjects(repo, base, head).returncode == 0
    unprefixed = commit(repo, "Bump ruff from 0.16.10 to 0.16.11")
    assert check_subjects(repo, base, unprefixed).returncode == 1


def test_subject_check_passes_good_commits_and_fails_a_bad_one(repo):
    base = git(repo, "rev-parse", "HEAD")
    good = commit(repo, "core: add the parser")
    assert check_subjects(repo, base, good).returncode == 0
    bad = commit(repo, "fixed stuff")
    assert check_subjects(repo, base, bad).returncode == 1


def test_subject_check_passes_reverts_and_refuses_fixups(repo):
    base = git(repo, "rev-parse", "HEAD")
    reverted = commit(repo, 'Revert "core: add the parser"')
    assert check_subjects(repo, base, reverted).returncode == 0
    fixup = commit(repo, "fixup! core: add the parser")
    result = check_subjects(repo, base, fixup)
    assert result.returncode == 1
    assert "squash this before merging" in result.stdout


def test_subject_check_fails_when_it_checked_nothing(repo):
    head = git(repo, "rev-parse", "HEAD")
    assert check_subjects(repo, head, head).returncode == 1
    assert check_subjects(repo, "0" * 40, head).returncode != 0


def release_step(repo: Path, name: str, **env: str):
    script = step_script("release.yml", "tag", name)
    return run(["bash", "-e", "-c", script], repo, {**os.environ, "DEFAULT_BRANCH": "main", **env})


def changelog_commit(repo: Path, version: str = "1.4.0") -> str:
    (repo / "CHANGELOG.md").write_text(
        f"# Changelog\n\n## [{version}] - 2026-09-30\n\n### Added\n\n- A parser.\n",
        encoding="utf-8",
    )
    git(repo, "commit", "-q", "-am", f"docs: changelog for {version}")
    git(repo, "push", "-q", "origin", "main")
    return git(repo, "rev-parse", "HEAD")


@pytest.mark.parametrize(
    "version",
    ["", "1.4.0; echo injected", "1.4.0\n2.0.0", "v1.4.0", "1..4", ".", "1.", "1.4", "01.02.003"],
)
def test_release_refuses_a_malformed_version(repo, version):
    sha = changelog_commit(repo)
    result = release_step(repo, RELEASE_CHECK, VERSION=version, SHA=sha)
    assert result.returncode == 1
    assert "not a version" in result.stdout


def test_release_takes_a_pre_release_version(repo):
    sha = changelog_commit(repo, "1.4.0-rc.1")
    result = release_step(repo, RELEASE_CHECK, VERSION="1.4.0-rc.1", SHA=sha)
    assert result.returncode == 0, result.stdout


@pytest.mark.parametrize(
    ("sha", "message"),
    [
        ("main", "not a full commit SHA"),
        ("3d3c42e", "not a full commit SHA"),
        ("0" * 40, "no commit"),
    ],
)
def test_release_refuses_anything_but_a_commit_it_has(repo, sha, message):
    changelog_commit(repo)
    result = release_step(repo, RELEASE_CHECK, VERSION="1.4.0", SHA=sha)
    assert result.returncode == 1
    assert message in result.stdout


def test_release_refuses_a_commit_off_the_default_branch(repo):
    changelog_commit(repo)
    git(repo, "switch", "-q", "-c", "topic")
    sha = commit(repo, "core: not merged yet")
    result = release_step(repo, RELEASE_CHECK, VERSION="1.4.0", SHA=sha)
    assert result.returncode == 1
    assert "is not on main" in result.stdout


def test_release_reads_the_changelog_at_the_commit_not_the_working_tree(repo):
    sha = git(repo, "rev-parse", "HEAD")
    (repo / "CHANGELOG.md").write_text("# Changelog\n\n## [1.4.0]\n", encoding="utf-8")
    result = release_step(repo, RELEASE_CHECK, VERSION="1.4.0", SHA=sha)
    assert result.returncode == 1
    assert "has no section for 1.4.0" in result.stdout


def workflow_commit(repo: Path, text: str, branch: str = "main") -> str:
    (repo / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
    (repo / ".github" / "workflows" / "ci.yml").write_text(text, encoding="utf-8")
    git(repo, "add", ".github")
    git(repo, "commit", "-q", "-m", "ci: change the workflow")
    git(repo, "push", "-q", "origin", branch)
    return git(repo, "rev-parse", "HEAD")


def test_release_takes_a_commit_whose_workflows_a_branch_has(repo):
    assert release_step(repo, RELEASE_WORKFLOWS, SHA=git(repo, "rev-parse", "HEAD")).returncode == 0
    sha = workflow_commit(repo, "name: CI\n")
    result = release_step(repo, RELEASE_WORKFLOWS, SHA=sha)
    assert result.returncode == 0, result.stdout + result.stderr


def test_release_refuses_a_commit_whose_workflow_no_branch_still_has(repo):
    old = workflow_commit(repo, "name: CI\n")
    workflow_commit(repo, "name: CI, changed\n")
    result = release_step(repo, RELEASE_WORKFLOWS, SHA=old)
    assert result.returncode == 1
    assert "so GitHub would refuse its tag: .github/workflows/ci.yml" in result.stdout
    # Once any branch has the old file as it was, GitHub takes the tag, and so does the check.
    git(repo, "push", "-q", "origin", f"{old}:refs/heads/release-1.x")
    git(repo, "fetch", "-q", "origin")
    assert release_step(repo, RELEASE_WORKFLOWS, SHA=old).returncode == 0


def test_release_tags_the_named_commit_not_the_branch_tip(repo):
    sha = changelog_commit(repo)
    commit(repo, "core: a later change")
    git(repo, "push", "-q", "origin", "main")
    result = release_step(repo, RELEASE_TAG, VERSION="1.4.0", SHA=sha, GH_TOKEN="CHANGEME")
    assert result.returncode == 0, result.stderr
    assert git(repo, "cat-file", "-t", "v1.4.0") == "tag"
    assert git(repo, "rev-parse", "v1.4.0^{commit}") == sha
    assert "refs/tags/v1.4.0" in git(repo, "ls-remote", "--tags", "origin")


OWN_RUN = "https://github.com/example/repo/actions/runs/4242/job/1"


def check_run(conclusion: str | None, name: str, url: str | None = None) -> dict:
    other = "https://github.com/example/repo/actions/runs/99/job/7"
    return {"name": name, "conclusion": conclusion, "details_url": url or other}


def checks_step(tmp_path: Path, runs: list[dict], code: int = 0):
    """Runs the step with a stand-in gh that applies the step's own jq filter to canned runs."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (tmp_path / "check-runs.json").write_text(json.dumps({"check_runs": runs}), encoding="utf-8")
    gh = bin_dir / "gh"
    gh.write_text(
        f"#!{sys.executable}\n"
        "import subprocess, sys\n"
        "args = sys.argv[1:]\n"
        f"if {code}:\n"
        f"    sys.exit({code})\n"
        "jq = args[args.index('--jq') + 1]\n"
        f"with open({str(tmp_path / 'check-runs.json')!r}) as page:\n"
        "    sys.exit(subprocess.run(['jq', '-r', jq], stdin=page).returncode)\n",
        encoding="utf-8",
    )
    gh.chmod(0o755)
    env = {
        "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        "GITHUB_REPOSITORY": "example/repo",
        "GITHUB_RUN_ID": "4242",
        "SHA": "a" * 40,
        "OWN_JOBS": "Release tag,Release page",
    }
    return release_step(tmp_path, RELEASE_CHECKS_PASSED, **env)


def test_release_goes_on_from_a_tag_an_earlier_attempt_pushed(repo):
    sha = changelog_commit(repo)
    git(repo, "tag", "-a", "v1.4.0", "-m", "Release 1.4.0", sha)
    result = release_step(repo, RELEASE_TAG, VERSION="1.4.0", SHA=sha, GH_TOKEN="CHANGEME")
    assert result.returncode == 0, result.stderr
    assert "already an annotated tag" in result.stdout


@pytest.mark.parametrize("kind", ["elsewhere", "lightweight"])
def test_release_refuses_a_tag_that_is_not_the_one_it_would_make(repo, kind):
    first = changelog_commit(repo)
    sha = commit(repo, "core: a later change")
    if kind == "elsewhere":
        git(repo, "tag", "-a", "v1.4.0", "-m", "Release 1.4.0", first)
    else:
        git(repo, "tag", "v1.4.0", sha)
    result = release_step(repo, RELEASE_TAG, VERSION="1.4.0", SHA=sha, GH_TOKEN="CHANGEME")
    assert result.returncode == 1
    assert "isn't an annotated tag on" in result.stdout


def test_release_passes_when_every_other_check_has_passed(tmp_path):
    runs = [
        check_run("success", "test"),
        check_run("skipped", "docs"),
        check_run(None, "Release tag", OWN_RUN),  # this run's own job, still going
        check_run("failure", "Release tag"),  # an earlier attempt
        check_run("failure", "Release page"),  # another job of the same workflow
    ]
    result = checks_step(tmp_path, runs)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "2 check(s) passed" in result.stdout


@pytest.mark.parametrize(
    ("runs", "message"),
    [
        ([check_run(None, "Release tag", OWN_RUN)], "no checks have run"),
        ([check_run("success", "lint"), check_run("failure", "test")], "not every check"),
        ([check_run("success", "lint"), check_run(None, "test")], "not every check"),
        ([check_run("cancelled", "test")], "not every check"),
    ],
)
def test_release_stops_unless_every_check_has_passed(tmp_path, runs, message):
    result = checks_step(tmp_path, runs)
    assert result.returncode == 1
    assert message in result.stdout


def test_release_stops_when_it_cannot_read_the_checks(tmp_path):
    assert checks_step(tmp_path, [], code=1).returncode != 0


def completion_guard(tmp_path: Path, report: str | None, baseline: int):
    work = tmp_path / "work"
    runner = tmp_path / "runner"
    work.mkdir()
    runner.mkdir()
    (work / ".test-baseline").write_text(f"{baseline}\n", encoding="utf-8")
    if report is not None:
        (runner / "junit.xml").write_text(report, encoding="utf-8")
    script = step_script("tests.yml", "test", COMPLETION_GUARD)
    return run(["bash", "-e", "-c", script], work, {**os.environ, "RUNNER_TEMP": str(runner)})


@pytest.mark.parametrize(
    ("report", "baseline", "code"),
    [
        (None, 1, 1),
        ('<testsuite tests="3"/>', 5, 1),
        ('<testsuite tests="5"/>', 5, 0),
        ('<testsuites><testsuite tests="3"/><testsuite tests="4"/></testsuites>', 7, 0),
    ],
)
def test_completion_guard_needs_a_report_counting_enough_tests(tmp_path, report, baseline, code):
    assert completion_guard(tmp_path, report, baseline).returncode == code
