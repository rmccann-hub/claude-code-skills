"""The standard's own mechanical checks (its "Test G"), each proven on a planted defect."""

import pytest
from conftest import add_standard, standard_text

from skillcheck.core.checks import check_repository


def standard_findings(report) -> list[str]:
    return [f.message for f in report.findings if f.rule == "standard"]


def test_a_conforming_standard_passes_and_is_reported(repo):
    add_standard(repo)
    report = check_repository(repo.root)
    assert report.findings == []
    assert report.standard_version == "0.2.0"
    assert "standard 0.2.0" in report.summary()


def test_no_standard_is_reported_as_such(repo):
    report = check_repository(repo.root)
    assert report.standard_version is None
    assert "no standard" in report.summary()


def replace_once(text: str, old: str, new: str) -> str:
    assert old in text, f"fixture no longer contains {old!r}"
    return text.replace(old, new, 1)


@pytest.mark.parametrize(
    ("defect", "expected"),
    [
        (lambda t: replace_once(t, "notes: none\n```", "notes: none\n"), "code fences"),
        (lambda t: replace_once(t, "</constraints>\n\n", ""), "<constraints>"),
        (
            lambda t: replace_once(
                t,
                "<constraints>\n\nA rule.",
                "<constraints>\n\n<constraints>\n\nA rule.\n\n</constraints>",
            ),
            "opens inside another",
        ),
        (lambda t: replace_once(t, "## Entries", "## Old entries"), "holds no versions"),
        (
            lambda t: replace_once(t, "|---|---|\n", "|---|---|\n<!-- WHY -->\n| `N/A` | No |\n"),
            "HTML comment",
        ),
        (lambda t: replace_once(t, "### 10. Dimension 10", "### 11. Dimension 11"), "dimensions"),
        (
            lambda t: replace_once(
                t, "# Provenance", "## Phase 9 — Extra — **WAIT**\n\n# Provenance"
            ),
            "waits",
        ),
        (lambda t: replace_once(t, "phase: 4\nnotes: none", "phase: 4\nother: x"), "notes"),
        (lambda t: replace_once(t, "phase: 7\n", "phase: 6\n"), "phase blocks"),
        (
            lambda t: replace_once(t, "# Provenance", "# Synthetic standard\n\n# Provenance"),
            "duplicate heading",
        ),
        (lambda t: replace_once(t, "**0.2.0** — second.", "**0.1.5** — second."), "version"),
        (
            lambda t: replace_once(
                t,
                "**0.2.0** — second.\n\n**0.1.0** — first.",
                "**0.2.0** — second.\n\n**0.3.0** — third.",
            ),
            "newest-first",
        ),
        (lambda t: replace_once(t, "A rule.", "A rule.  "), "trailing whitespace"),
        (lambda t: replace_once(t, "A rule.", "A rule.\n\n\n\nMore."), "blank lines"),
    ],
)
def test_each_mechanical_check_fires_on_its_defect(repo, defect, expected):
    add_standard(repo, text=defect(standard_text()))
    messages = standard_findings(check_repository(repo.root))
    assert len(messages) == 1, messages
    assert expected in messages[0]


def test_filename_and_frontmatter_versions_must_agree(repo):
    add_standard(repo, text=standard_text("0.2.0").replace('version: "0.2.0"', 'version: "0.9.0"'))
    messages = standard_findings(check_repository(repo.root))
    assert any("frontmatter says 0.9.0" in m for m in messages), messages


def test_the_skill_must_name_the_version_it_ships(repo):
    reference = add_standard(repo)
    skill_md = reference.parent.parent / "SKILL.md"
    skill_md.write_text(
        skill_md.read_text(encoding="utf-8").replace('"0.2.0"', '"0.1.0"'), encoding="utf-8"
    )
    messages = standard_findings(check_repository(repo.root))
    assert messages == ["SKILL.md says standard-version 0.1.0; the reference file is v0.2.0"]


def test_unreadable_frontmatter_in_the_standard_is_reported(repo):
    add_standard(repo, text=standard_text().replace("---\nname:", "name:", 1))
    messages = standard_findings(check_repository(repo.root))
    assert any("frontmatter" in m for m in messages), messages


def test_fenced_content_is_not_mistaken_for_structure(repo):
    fenced = "```markdown\n# Synthetic standard\n\n### 3. Not a dimension\n\nA rule.  \n```\n"
    add_standard(
        repo, text=replace_once(standard_text(), "# Provenance", fenced + "\n# Provenance")
    )
    assert standard_findings(check_repository(repo.root)) == []


def test_an_unreadable_skill_md_is_left_to_the_skill_checks(repo):
    reference = add_standard(repo)
    (reference.parent.parent / "SKILL.md").write_text("no frontmatter\n", encoding="utf-8")
    report = check_repository(repo.root)
    assert standard_findings(report) == []
    assert "frontmatter" in {f.rule for f in report.findings}
