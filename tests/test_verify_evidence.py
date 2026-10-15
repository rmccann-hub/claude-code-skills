"""The standard's evidence verifier passes a correct split and fails each kind of wrong one."""

import contextlib
import hashlib
import importlib.util
import io
import os
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "project-bootstrap-and-audit"
    / "scripts"
    / "verify_evidence.py"
)
IDENTITY = "evidence <evidence@invalid>"
INSTANT = "2026-10-14T20:00:00Z"
FILES = {
    "runs/r1/README.md": b"index\n",
    "runs/r1/app.log": b"line one\nline two\n",
    "runs/r1/caf\xc3\xa9 \xe2\x88\xb6 take.log": b"non-ascii name\n",
    "src/main.py": b"print('hi')\n",
}


def load():
    spec = importlib.util.spec_from_file_location("verify_evidence", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def git(repo: Path, *args: str, env: dict | None = None, data: bytes | None = None) -> str:
    full = {
        **os.environ,
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        **(env or {}),
    }
    res = subprocess.run(
        ["git", "-C", str(repo), *args], env=full, input=data, capture_output=True, check=True
    )
    return res.stdout.decode().strip()


def pinned() -> dict:
    name, email = "evidence", "evidence@invalid"
    return {
        "GIT_AUTHOR_NAME": name,
        "GIT_AUTHOR_EMAIL": email,
        "GIT_AUTHOR_DATE": INSTANT,
        "GIT_COMMITTER_NAME": name,
        "GIT_COMMITTER_EMAIL": email,
        "GIT_COMMITTER_DATE": INSTANT,
    }


def manifest(rows: list[list[str]]) -> bytes:
    header = "path\tbytes\tsha256\tevidence_commit\tlast_default_commit\n"
    return (header + "".join("\t".join(r) + "\n" for r in rows)).encode()


@pytest.fixture
def split(tmp_path: Path):
    """A repository whose `runs/r1` folder moved to an orphan `evidence` branch, done right."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", "t")
    git(repo, "config", "user.email", "t@example.com")
    for path, body in FILES.items():
        (repo / path).parent.mkdir(parents=True, exist_ok=True)
        (repo / path).write_bytes(body)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "base")
    base = git(repo, "rev-parse", "HEAD")
    # The move: an orphan commit of the folder's tree, identity and instant pinned.
    index = {"GIT_INDEX_FILE": str(tmp_path / "index")}
    git(repo, "read-tree", "--empty", env=index)
    listing = subprocess.run(
        ["git", "-C", str(repo), "ls-tree", "-r", "-z", base, "--", "runs/r1"],
        capture_output=True,
        check=True,
    ).stdout
    git(repo, "update-index", "-z", "--index-info", env=index, data=listing)
    tree = git(repo, "write-tree", env=index)
    ev = git(repo, "commit-tree", tree, "-m", "evidence: move", env=pinned())
    git(repo, "update-ref", "refs/heads/evidence", ev)
    # The removal: moved files leave main, the README stays, the manifest arrives.
    rows = []
    for path, body in sorted(FILES.items()):
        if path.startswith("runs/"):
            rows.append([path, str(len(body)), hashlib.sha256(body).hexdigest(), ev, base])
            if not path.endswith("README.md"):
                git(repo, "rm", "-q", "--", path)
    (repo / "docs").mkdir()
    (repo / "docs" / "evidence-manifest.tsv").write_bytes(manifest(rows))
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "remove the moved evidence")
    return repo, ev, base, rows


def run(repo: Path, *extra: str) -> tuple[int, str]:
    """Run the script's main in this process, so coverage sees every line it takes."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = load().main(["--repo", str(repo), *extra])
    return code, out.getvalue() + err.getvalue()


def rewrite_manifest(repo: Path, rows: list[list[str]]) -> None:
    (repo / "docs" / "evidence-manifest.tsv").write_bytes(manifest(rows))
    git(repo, "commit", "-q", "-am", "edit the manifest")


def test_a_correct_split_passes(split):
    repo, *_ = split
    code, out = run(repo, "--identity", IDENTITY, "--instant", INSTANT)
    assert code == 0, out
    assert "every check passed" in out
    assert "1 file(s) on both branches" in out


def test_a_non_ascii_path_matches_its_row(split):
    repo, *_ = split
    code, out = run(repo)
    assert code == 0, out
    assert "every row's file is in its evidence commit" in out


def test_a_wrong_hash_fails(split):
    repo, ev, base, rows = split
    rows[1][2] = rows[1][2][:-1] + ("0" if rows[1][2][-1] != "0" else "1")
    rewrite_manifest(repo, rows)
    code, out = run(repo)
    assert code == 1
    assert "FAIL every row's SHA-256 matches its file" in out


def test_a_wrong_size_fails(split):
    repo, ev, base, rows = split
    rows[0][1] = str(int(rows[0][1]) + 1)
    rewrite_manifest(repo, rows)
    code, out = run(repo)
    assert code == 1
    assert "FAIL every row's size matches its file" in out


def test_a_row_for_a_missing_file_fails(split):
    repo, ev, base, rows = split
    rows.append(["runs/r1/zz-missing.log", "1", "0" * 64, ev, base])
    rewrite_manifest(repo, rows)
    code, out = run(repo)
    assert code == 1
    assert "FAIL every row's file is in its evidence commit" in out


def test_unsorted_and_duplicate_rows_fail(split):
    repo, ev, base, rows = split
    rewrite_manifest(repo, [rows[1], rows[0], rows[1]])
    code, out = run(repo)
    assert code == 1
    assert "FAIL the manifest is sorted by path" in out
    assert "FAIL one manifest row per path" in out


def test_a_short_row_and_a_foreign_commit_fail(split):
    repo, ev, base, rows = split
    rows[0][3] = base
    rewrite_manifest(repo, [*rows, ["runs/z", "1"]])
    code, out = run(repo)
    assert code == 1
    assert "FAIL every manifest row has five fields" in out
    assert "FAIL every row's evidence commit is on the branch" in out


def test_a_changed_source_and_a_changed_default_fail(split):
    repo, ev, base, rows = split
    (repo / "runs" / "r1" / "README.md").write_bytes(b"edited after the move\n")
    git(repo, "commit", "-q", "-am", "edit a kept file")
    edited = git(repo, "rev-parse", "HEAD")
    rows[0][4] = edited
    rewrite_manifest(repo, rows)
    code, out = run(repo)
    assert code == 1
    assert "FAIL every moved file is the same blob as in its source commit" in out
    assert "FAIL no row's path holds a different file on the default branch" in out


def test_a_tag_on_evidence_fails(split):
    repo, ev, *_ = split
    git(repo, "tag", "oops", ev)
    code, out = run(repo)
    assert code == 1
    assert "FAIL no tag reaches the evidence branch" in out


def test_shared_history_and_a_parent_fail(split):
    repo, ev, base, rows = split
    child = git(repo, "commit-tree", f"{ev}^{{tree}}", "-p", base, "-m", "rooted", env=pinned())
    git(repo, "update-ref", "refs/heads/evidence", child)
    for row in rows:
        row[3] = child
    rewrite_manifest(repo, rows)
    code, out = run(repo)
    assert code == 1
    assert "FAIL the first evidence commit has no parent" in out
    assert "FAIL the evidence branch shares no history with the default branch" in out


def test_a_later_commit_off_the_chain_fails(split, tmp_path):
    repo, ev, base, rows = split
    other = git(repo, "commit-tree", f"{ev}^{{tree}}", "-m", "second root", env=pinned())
    merged = git(
        repo, "commit-tree", f"{ev}^{{tree}}", "-p", ev, "-p", other, "-m", "merge", env=pinned()
    )
    git(repo, "update-ref", "refs/heads/evidence", merged)
    code, out = run(repo)
    assert code == 1
    assert "FAIL each later evidence commit has the one before as its only parent" in out


def test_the_wrong_identity_and_instant_fail(split):
    repo, *_ = split
    code, out = run(repo, "--identity", "someone <x@y>", "--instant", "2026-01-01T00:00:00Z")
    assert code == 1
    assert "FAIL the move commit's author and committer are the pinned identity" in out
    assert "FAIL the move commit's dates are the pinned instant" in out


def test_a_wrong_header_fails_and_stops(split):
    repo, *_ = split
    (repo / "docs" / "evidence-manifest.tsv").write_bytes(b"path\tbytes\n")
    git(repo, "commit", "-q", "-am", "break the header")
    code, out = run(repo)
    assert code == 1
    assert "FAIL the manifest's header" in out
    assert "SHA-256" not in out


@pytest.mark.parametrize(
    ("args", "message"),
    [
        (["--evidence", "nowhere"], "no commit at nowhere"),
        (["--manifest", "docs/none.tsv"], "no docs/none.tsv on main"),
    ],
)
def test_couldnt_check_exits_2(split, args, message):
    repo, *_ = split
    code, out = run(repo, *args)
    assert code == 2
    assert message in out


def test_an_empty_manifest_couldnt_be_checked(split):
    repo, *_ = split
    (repo / "docs" / "evidence-manifest.tsv").write_bytes(b"")
    git(repo, "commit", "-q", "-am", "empty")
    code, out = run(repo)
    assert code == 2
    assert "is empty" in out


def test_a_git_failure_couldnt_be_checked(tmp_path):
    module = load()
    with pytest.raises(module.CannotCheck):
        module.Git(tmp_path).run("rev-parse", "HEAD")


def test_a_tree_spec_reads_as_missing(split):
    repo, *_ = split
    module = load()
    found = module.Git(repo).blobs(["main:runs", "main:src/main.py"])
    assert found["main:runs"] is None
    assert found["main:src/main.py"][1] == FILES["src/main.py"]


def test_the_script_runs_as_a_command(split):
    repo, *_ = split
    res = subprocess.run(
        [sys.executable, str(SCRIPT), "--repo", str(repo)], capture_output=True, check=False
    )
    assert res.returncode == 0, res.stderr.decode()
    assert b"every check passed" in res.stdout


def test_an_evidence_ref_inside_the_default_branch_couldnt_be_checked(split):
    repo, *_ = split
    git(repo, "update-ref", "refs/heads/evidence", "main~1")
    code, out = run(repo)
    assert code == 2
    assert "has no commits of its own" in out


@pytest.mark.parametrize("extra", [["--identity", IDENTITY], ["--instant", INSTANT]])
def test_identity_and_instant_are_each_checked_alone(split, extra):
    repo, *_ = split
    code, out = run(repo, *extra)
    assert code == 0, out
    assert ("pinned identity" in out) == ("--identity" in extra)
    assert ("pinned instant" in out) == ("--instant" in extra)
