"""Agents' worktrees under `.claude/worktrees/` are another checkout (core/paths.py)."""

import pytest

from skillcheck.core import paths
from skillcheck.core.checks import check_repository

# One planted defect per scan that reads `.claude`: a merge's conflict marker, a hidden
# character, and a time of day written without its zone.
DEFECTS = {
    "conflict": "Kept.\n<<<<<<< HEAD\nOurs.\n",
    "unicode": "Text\u200bwith a zero-width space.\n",
    "times": "Merged at 12:34.\n",
}


def write(repo, relative: str, text: str) -> None:
    target = repo.root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def rules(repo) -> list[tuple[str, str]]:
    return [(f.path, f.rule) for f in check_repository(repo.root).findings]


@pytest.mark.parametrize("rule", sorted(DEFECTS))
def test_a_defect_in_an_agents_worktree_is_not_this_repositorys(repo, rule):
    write(repo, ".claude/worktrees/agent-1/docs/notes.md", DEFECTS[rule])
    assert rules(repo) == []


@pytest.mark.parametrize("rule", sorted(DEFECTS))
def test_the_same_defect_elsewhere_in_claude_still_fires(repo, rule):
    write(repo, ".claude/notes.md", DEFECTS[rule])
    assert (".claude/notes.md", rule) in rules(repo)


def test_a_repository_inside_a_worktree_still_scans_itself(tmp_path):
    root = tmp_path / ".claude" / "worktrees" / "agent-1"
    write_at = root / "docs" / "notes.md"
    write_at.parent.mkdir(parents=True)
    write_at.write_text("one\n", encoding="utf-8")
    assert paths.files_under(root, "docs") == [write_at]


def test_a_missing_directory_has_no_files(tmp_path):
    assert paths.files_under(tmp_path, "docs") == []
