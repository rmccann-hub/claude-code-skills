"""A merge's conflict markers fail the check wherever a commit here could carry them."""

import pytest

from skillcheck.core.checks import check_repository


def write(repo, relative: str, text: str) -> None:
    path = repo.root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def findings(report) -> list[tuple[str, str]]:
    return [(f.path, f.rule) for f in report.findings]


@pytest.mark.parametrize("marker", ["<<<<<<< HEAD", ">>>>>>> topic", "||||||| base", "<<<<<<<"])
@pytest.mark.parametrize(
    "relative",
    [
        "README.md",
        "docs/guide.md",
        "research/runs/r.md",
        ".github/workflows/ci.yml",
        "src/package/module.py",
        "tests/fixtures/sample.md",
    ],
)
def test_a_conflict_marker_fires(repo, relative, marker):
    write(repo, relative, f"Kept.\n{marker}\nOurs.\n")
    assert findings(check_repository(repo.root)) == [(relative, "conflict")]


def test_the_message_names_the_first_marker_line(repo):
    write(repo, "docs/guide.md", "one\ntwo\n<<<<<<< HEAD\nours\n=======\ntheirs\n>>>>>>> topic\n")
    [finding] = check_repository(repo.root).findings
    assert finding.message == "line 3 is a merge's conflict marker"


@pytest.mark.parametrize(
    "text",
    [
        "Title\n=======\n",  # a Markdown heading underline
        "Inline <<<<<<< HEAD is prose.\n",
        "<<<<<<<< eight is not a marker\n",
    ],
)
def test_lookalikes_pass(repo, text):
    write(repo, "docs/guide.md", text)
    assert check_repository(repo.root).findings == []


def test_a_binary_file_is_skipped(repo):
    path = repo.root / "docs" / "figure.bin"
    path.parent.mkdir(parents=True)
    path.write_bytes(b"\xff\xfe\n<<<<<<< HEAD\n")
    assert check_repository(repo.root).findings == []


def test_a_directory_outside_the_scan_is_not_checked(repo):
    write(repo, "scratch/notes.md", "<<<<<<< HEAD\n")
    assert check_repository(repo.root).findings == []
