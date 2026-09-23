"""Files agents read outside skills/ get the same hidden-character scan as a skill (A30)."""

import pytest

from skillcheck.core.checks import check_repository

RLO = "‮"  # right-to-left override, the Trojan Source character


def write(repo, relative: str, text: str) -> None:
    path = repo.root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def findings(report) -> list[tuple[str, str]]:
    return [(f.path, f.rule) for f in report.findings]


def test_clean_agent_and_research_files_pass(repo):
    write(repo, "AGENTS.md", "# Fixture\n")
    write(repo, "CLAUDE.md", "@AGENTS.md\n")
    write(repo, ".claude/rules/python.md", "Rules.\n")
    write(repo, "research/runs/2026-01-01-R99.md", "A result.\n")
    assert check_repository(repo.root).findings == []


@pytest.mark.parametrize(
    "relative",
    [
        "AGENTS.md",
        "CLAUDE.md",
        ".claude/rules/python.md",
        ".claude/settings.json",
        "research/runs/2026-01-01-R99.md",
        "research/prompts/R99.md",
    ],
)
def test_a_hidden_character_in_an_agent_or_research_file_fires(repo, relative):
    write(repo, relative, f"Looks{RLO} harmless.\n")
    assert findings(check_repository(repo.root)) == [(relative, "unicode")]


def test_the_message_names_the_line_and_the_code_point(repo):
    write(repo, "research/runs/r.md", "clean\nzero​width\n")
    [finding] = check_repository(repo.root).findings
    assert finding.message.startswith("line 2 holds U+200B")


def test_a_file_outside_the_scope_is_not_checked(repo):
    write(repo, "docs/notes.md", f"Out of scope{RLO}.\n")
    assert check_repository(repo.root).findings == []


def test_a_binary_research_file_is_skipped(repo):
    path = repo.root / "research" / "runs" / "figure.bin"
    path.parent.mkdir(parents=True)
    path.write_bytes(b"\xff\xfe\x00binary")
    assert check_repository(repo.root).findings == []
