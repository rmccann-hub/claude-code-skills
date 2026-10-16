"""`skillcheck --new` and `--new-module` write a skill and its modules, marked until finished."""

import json

import pytest

from skillcheck import scaffold
from skillcheck.cli import main
from skillcheck.core.checks import PLACEHOLDER, check_repository

SKILL = "skills/demo-skill/SKILL.md"
MODULE = "skills/demo-skill/references/demo-module.md"
FIXTURE = "tests/fixtures/modules/demo-module.json"


def rules(report) -> list[tuple[str, str]]:
    return [(finding.path, finding.rule) for finding in report.findings]


def finish(repo, *paths):
    for path in paths:
        target = repo.root / path
        target.write_text(target.read_text(encoding="utf-8").replace(PLACEHOLDER, "Done."), "utf-8")


def roadmap(repo):
    repo.roadmap({"demo-skill": "shipped"}, {"demo-module": ("demo-skill", "shipped")})


def test_a_new_skill_is_one_router_with_no_modules(repo):
    assert [path.as_posix() for path in scaffold.create(repo.root, "demo-skill")] == [SKILL]
    repo.catalog(repo.plugin("demo", "./skills/demo-skill"))
    assert sorted(rules(check_repository(repo.root))) == [
        (SKILL, "modules"),
        (SKILL, "placeholder"),
    ]


def test_a_new_module_adds_its_file_row_and_trigger_tests(repo):
    scaffold.create(repo.root, "demo-skill")
    written = scaffold.create_module(repo.root, "demo-module", "demo-skill")
    assert [path.as_posix() for path in written] == [SKILL, MODULE, FIXTURE]
    triggers = json.loads((repo.root / FIXTURE).read_text(encoding="utf-8"))
    assert {case["should_trigger"] for case in triggers} == {True, False}
    assert "| [`demo-module`](references/demo-module.md) |" in (repo.root / SKILL).read_text(
        encoding="utf-8"
    )


def test_an_unfinished_module_fails_only_on_its_placeholders(repo):
    scaffold.create(repo.root, "demo-skill")
    scaffold.create_module(repo.root, "demo-module", "demo-skill")
    repo.catalog(repo.plugin("demo", "./skills/demo-skill"))
    roadmap(repo)
    found = sorted(rules(check_repository(repo.root)))
    assert found == [(SKILL, "placeholder"), (MODULE, "placeholder"), (FIXTURE, "placeholder")]


def test_a_finished_skeleton_passes_every_rule(repo):
    scaffold.create(repo.root, "demo-skill")
    scaffold.create_module(repo.root, "demo-module", "demo-skill")
    repo.catalog(repo.plugin("demo", "./skills/demo-skill"))
    roadmap(repo)
    finish(repo, SKILL, MODULE, FIXTURE)
    report = check_repository(repo.root)
    assert report.findings == []
    assert (report.skills, report.modules) == (1, 1)


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
    before = (repo.root / SKILL).read_text(encoding="utf-8")
    with pytest.raises(scaffold.ScaffoldError, match="already there: skills/demo-skill"):
        scaffold.create(repo.root, "demo-skill")
    assert (repo.root / SKILL).read_text(encoding="utf-8") == before


@pytest.mark.parametrize(
    ("name", "skill", "message"),
    [
        ("Bad", "demo-skill", "lowercase letters"),
        ("demo-module", "nowhere", "there's no skill `nowhere`; make it with --new nowhere first"),
        ("demo-module", "plain", "`plain` has no Modules section to route it"),
        ("taken", "demo-skill", "`taken` is already a module of `other`"),
        ("plain", "demo-skill", "`plain` is already the name of a skill"),
        ("demo-module", "demo-skill", f"already there: {FIXTURE}"),
    ],
)
def test_a_refused_module_writes_nothing(repo, name, skill, message):
    scaffold.create(repo.root, "demo-skill")
    repo.skill("plain")
    repo.modular_skill("other", "taken")
    (repo.root / FIXTURE).write_text("[]\n", encoding="utf-8")
    before = (repo.root / SKILL).read_text(encoding="utf-8")
    with pytest.raises(scaffold.ScaffoldError, match=message.replace("(", r"\(")):
        scaffold.create_module(repo.root, name, skill)
    assert (repo.root / SKILL).read_text(encoding="utf-8") == before
    assert not (repo.root / MODULE).exists()


def test_a_skill_may_route_a_module_of_its_own_name(repo):
    scaffold.create(repo.root, "demo-skill")
    written = scaffold.create_module(repo.root, "demo-skill", "demo-skill")
    assert written[1].as_posix() == "skills/demo-skill/references/demo-skill.md"


def test_the_commands_write_and_say_what_comes_next(repo, capsys):
    assert main([str(repo.root), "--new", "demo-skill"]) == 0
    assert main([str(repo.root), "--new-module", "demo-module", "demo-skill"]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[0] == f"wrote {SKILL}"
    assert out[1].startswith("skillcheck: new skill demo-skill, 1 file(s).")
    assert out[2:5] == [f"wrote {SKILL}", f"wrote {MODULE}", f"wrote {FIXTURE}"]
    assert out[5].startswith("skillcheck: new module demo-module in demo-skill, 3 file(s).")
    assert "docs/authoring-a-skill.md" in out[5]


def test_the_commands_refuse_and_exit_one(repo, capsys):
    assert main([str(repo.root), "--new", "Bad"]) == 1
    assert main([str(repo.root), "--new-module", "demo-module", "nowhere"]) == 1
    out = capsys.readouterr().out.splitlines()
    assert out[0].startswith("new: 'Bad' must be")
    assert out[1].startswith("new-module: there's no skill `nowhere`")
