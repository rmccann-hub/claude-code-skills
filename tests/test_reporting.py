"""Every skill's "When something here is wrong" section (core/reporting.py)."""

from conftest import REPORTING

from skillcheck import scaffold
from skillcheck.core import reporting
from skillcheck.core.checks import check_repository

URL = "https://github.com/example/skills"
ISSUES = f"{URL}/issues"


def findings(repo):
    return [(f.path, f.rule, f.message) for f in check_repository(repo.root).findings]


def published(repo, body: str) -> None:
    """One skill, from a catalog naming one repository, holding ``body`` as its section."""
    skill_dir = repo.skill("example-skill")
    path = skill_dir / "SKILL.md"
    path.write_text(path.read_text(encoding="utf-8").replace(REPORTING, body), encoding="utf-8")
    plugin = repo.plugin("example", "./skills/example-skill") | {"repository": URL}
    repo.catalog(plugin)


def test_the_shared_text_passes(repo):
    published(repo, "\n" + reporting.section(ISSUES))
    assert findings(repo) == []


def test_a_skill_without_the_section_fires_alone(repo):
    published(repo, "\n")
    assert findings(repo) == [
        (
            "skills/example-skill/SKILL.md",
            "reporting",
            "no 'When something here is wrong' section, so a problem with the skill goes "
            "unreported",
        )
    ]


def test_a_section_that_differs_from_the_shared_text_fires(repo):
    published(repo, "\n" + reporting.section(ISSUES).replace("one sentence", "a paragraph"))
    assert findings(repo) == [
        (
            "skills/example-skill/SKILL.md",
            "reporting",
            "the 'When something here is wrong' section differs from the text every skill "
            "shares, in src/skillcheck/core/reporting.py; copy it from there",
        )
    ]


def test_a_section_naming_another_repository_fires(repo):
    published(repo, "\n" + reporting.section("https://github.com/someone/else/issues"))
    assert [rule for _, rule, _ in findings(repo)] == ["reporting"]


def test_the_issues_page_comes_from_the_catalog(repo):
    assert reporting.issues_url(repo.root) is None
    repo.catalog_text("not json")
    assert reporting.issues_url(repo.root) is None
    repo.catalog(repo.plugin("a") | {"repository": URL + "/"}, repo.plugin("b"))
    assert reporting.issues_url(repo.root) == ISSUES
    repo.catalog(repo.plugin("a") | {"repository": URL}, repo.plugin("b") | {"repository": "x"})
    assert reporting.issues_url(repo.root) is None


def test_without_one_repository_the_section_still_has_to_be_there(repo):
    repo.skill("example-skill")
    repo.catalog(repo.plugin("example", "./skills/example-skill"))
    assert findings(repo) == []
    assert reporting.section(None).count(reporting.UNKNOWN) == 1


def test_a_new_skill_carries_the_shared_section(repo):
    repo.catalog(repo.plugin("example") | {"repository": URL})
    scaffold.create(repo.root, "fresh-skill")
    text = (repo.root / "skills/fresh-skill/SKILL.md").read_text(encoding="utf-8")
    assert text.endswith(reporting.section(ISSUES))
