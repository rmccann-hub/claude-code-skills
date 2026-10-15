"""`skillcheck --new` writes a skill in the authoring guide's shape, marked until it's finished."""

import json

import pytest

from skillcheck import scaffold
from skillcheck.cli import main
from skillcheck.core.checks import PLACEHOLDER, check_repository

FILES = [
    "skills/demo-skill/SKILL.md",
    "skills/demo-skill/references/why.md",
    "skills/demo-skill/references/facts.md",
    "skills/demo-skill/references/audit.md",
    "skills/demo-skill/references/mistakes.md",
    "skills/demo-skill/references/sources.md",
    "tests/fixtures/skills/demo-skill.json",
]


def rules(report) -> list[tuple[str, str]]:
    return [(finding.path, finding.rule) for finding in report.findings]


def test_it_writes_every_file_the_guide_asks_for(repo):
    written = scaffold.create(repo.root, "demo-skill")
    assert [path.as_posix() for path in written] == FILES
    assert all((repo.root / path).is_file() for path in FILES)
    triggers = json.loads((repo.root / FILES[-1]).read_text(encoding="utf-8"))
    assert {case["should_trigger"] for case in triggers} == {True, False}


def test_an_unfinished_skill_fails_only_on_its_placeholders(repo):
    scaffold.create(repo.root, "demo-skill")
    repo.catalog(repo.plugin("demo", "./skills/demo-skill"))
    found = rules(check_repository(repo.root))
    assert found == [(path, "placeholder") for path in sorted(FILES[:-1])]


def test_a_finished_skeleton_passes_every_rule(repo):
    scaffold.create(repo.root, "demo-skill")
    repo.catalog(repo.plugin("demo", "./skills/demo-skill"))
    for path in FILES[:-1]:
        target = repo.root / path
        text = target.read_text(encoding="utf-8").replace(PLACEHOLDER, "Done.")
        target.write_text(text, encoding="utf-8")
    report = check_repository(repo.root)
    assert report.findings == []
    assert report.skills == 1


def test_the_placeholder_rule_counts_and_locates(repo):
    skill = repo.skill("example-skill")
    (skill / "references" / "why.md").write_text(
        f"# Why\n\n{PLACEHOLDER} one\n{PLACEHOLDER} two\n", encoding="utf-8"
    )
    repo.catalog(repo.plugin("example", "./skills/example-skill"))
    (finding,) = check_repository(repo.root).findings
    assert finding.rule == "placeholder"
    assert finding.message == f"2 unfinished part(s) marked {PLACEHOLDER}, the first on line 3"


@pytest.mark.parametrize("name", ["Demo", "demo_skill", "-demo", "demo--skill", "d" * 65, ""])
def test_a_bad_name_is_refused_with_nothing_written(repo, name):
    with pytest.raises(scaffold.ScaffoldError, match="lowercase letters"):
        scaffold.create(repo.root, name)
    assert not (repo.root / "skills").exists()


def test_an_existing_skill_is_not_overwritten(repo):
    repo.skill("demo-skill")
    before = (repo.root / "skills/demo-skill/SKILL.md").read_text(encoding="utf-8")
    with pytest.raises(scaffold.ScaffoldError, match="already there: skills/demo-skill"):
        scaffold.create(repo.root, "demo-skill")
    assert (repo.root / "skills/demo-skill/SKILL.md").read_text(encoding="utf-8") == before


def test_an_existing_trigger_file_is_not_overwritten(repo):
    (repo.root / "tests/fixtures/skills").mkdir(parents=True)
    (repo.root / FILES[-1]).write_text("[]\n", encoding="utf-8")
    with pytest.raises(scaffold.ScaffoldError, match="tests/fixtures/skills/demo-skill.json"):
        scaffold.create(repo.root, "demo-skill")
    assert not (repo.root / "skills").exists()


def test_the_command_writes_and_says_what_comes_next(repo, capsys):
    assert main([str(repo.root), "--new", "demo-skill"]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[:-1] == [f"wrote {path}" for path in FILES]
    assert out[-1].startswith("skillcheck: new skill demo-skill, 7 file(s).")
    assert "docs/authoring-a-skill.md" in out[-1]


def test_the_command_refuses_and_exits_one(repo, capsys):
    assert main([str(repo.root), "--new", "Bad"]) == 1
    assert capsys.readouterr().out.startswith("new: 'Bad' must be")
