"""ROADMAP.md and the README's skill table must agree with skills/, so neither can drift."""

import pytest

from skillcheck.core.checks import check_repository

ROADMAP_HEAD = (
    "# Roadmap\n\n| Skill | Covers | Status | Coverage | Research |\n|---|---|---|---|---|\n"
)
README_HEAD = "# Fixture\n\n## Skills\n\n| Skill | Plugin | What it does |\n|---|---|---|\n"


def roadmap(repo, *rows: tuple[str, str]) -> None:
    body = "".join(f"| `{name}` | covers | {status} | core | R01 |\n" for name, status in rows)
    (repo.root / "ROADMAP.md").write_text(ROADMAP_HEAD + body, encoding="utf-8")


def readme(repo, *names: str) -> None:
    body = "".join(f"| `{name}` | `example` | does |\n" for name in names)
    (repo.root / "README.md").write_text(README_HEAD + body, encoding="utf-8")


def shipped_skill(repo, name: str = "example-skill") -> None:
    repo.skill(name)
    repo.catalog(repo.plugin("example", f"./skills/{name}"))


def findings(report) -> list[tuple[str, str, str]]:
    return [(f.path, f.rule, f.message) for f in report.findings]


def test_agreeing_roadmap_and_readme_pass_and_are_counted(repo):
    shipped_skill(repo)
    roadmap(repo, ("example-skill", "shipped"), ("later-skill", "planned"))
    readme(repo, "example-skill")
    report = check_repository(repo.root)
    assert report.findings == []
    assert report.roadmap_entries == 2
    assert "2 roadmap entries" in report.summary()


def test_a_repository_without_a_roadmap_says_so(repo):
    report = check_repository(repo.root)
    assert report.roadmap_entries is None
    assert "no roadmap" in report.summary()


def test_a_shipped_skill_missing_from_the_roadmap_fires(repo):
    shipped_skill(repo)
    roadmap(repo, ("later-skill", "planned"))
    assert findings(check_repository(repo.root)) == [
        ("skills/example-skill", "roadmap", "not listed as shipped in ROADMAP.md")
    ]


def test_a_skill_listed_but_not_shipped_fires(repo):
    shipped_skill(repo)
    roadmap(repo, ("example-skill", "planned"))
    assert findings(check_repository(repo.root)) == [
        ("skills/example-skill", "roadmap", "not listed as shipped in ROADMAP.md")
    ]


def test_a_shipped_row_with_no_skill_fires(repo):
    roadmap(repo, ("ghost-skill", "shipped"))
    assert findings(check_repository(repo.root)) == [
        (
            "ROADMAP.md",
            "roadmap",
            "`ghost-skill` is marked shipped, but skills/ghost-skill does not exist",
        )
    ]


@pytest.mark.parametrize("status", ["done", "Shipped", ""])
def test_a_status_outside_the_closed_set_fires(repo, status):
    roadmap(repo, ("later-skill", status))
    [(path, rule, message)] = findings(check_repository(repo.root))
    assert (path, rule) == ("ROADMAP.md", "roadmap")
    assert "status" in message


def test_a_skill_listed_twice_fires(repo):
    roadmap(repo, ("later-skill", "planned"), ("later-skill", "researching"))
    assert findings(check_repository(repo.root)) == [
        ("ROADMAP.md", "roadmap", "`later-skill` is listed 2 times")
    ]


def test_tables_about_other_things_are_ignored(repo):
    text = (
        ROADMAP_HEAD
        + "| `later-skill` | covers | planned | core | R01 |\n\n"
        + "| Item | What it is | Status | Trigger |\n|---|---|---|---|\n"
        + "| Weekly check | a workflow | planned | a skill ships |\n"
    )
    (repo.root / "ROADMAP.md").write_text(text, encoding="utf-8")
    report = check_repository(repo.root)
    assert report.findings == []
    assert report.roadmap_entries == 1


def test_a_readme_missing_a_shipped_skill_fires(repo):
    shipped_skill(repo)
    readme(repo)
    assert findings(check_repository(repo.root)) == [
        ("skills/example-skill", "readme", "not listed in the README's skill table")
    ]


def test_a_readme_listing_a_skill_that_does_not_exist_fires(repo):
    readme(repo, "ghost-skill")
    assert findings(check_repository(repo.root)) == [
        ("README.md", "readme", "lists `ghost-skill`, but skills/ghost-skill does not exist")
    ]


def test_a_readme_without_a_skill_table_is_not_checked(repo):
    (repo.root / "README.md").write_text("# Fixture\n\nNo skills yet.\n", encoding="utf-8")
    assert check_repository(repo.root).findings == []
