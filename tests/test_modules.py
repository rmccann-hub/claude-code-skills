"""Skills made of modules: the router, each module's file and tests, and the roadmap's rows."""

import json

import pytest

from skillcheck.cli import main
from skillcheck.core import modules
from skillcheck.core.checks import check_repository


def built(repo, *names, skill="demo"):
    """A repository whose one skill routes ``names``, each listed as shipped."""
    skill_dir = repo.modular_skill(skill, *names)
    repo.catalog(repo.plugin("demo", f"./skills/{skill}"))
    repo.roadmap({skill: "shipped"}, {name: (skill, "shipped") for name in names})
    return skill_dir


def findings(repo):
    return [(f.path, f.rule, f.message) for f in check_repository(repo.root).findings]


def test_a_skill_made_of_modules_passes_without_a_rationale_file(repo):
    built(repo, "first", "second")
    report = check_repository(repo.root)
    assert report.findings == []
    assert (report.skills, report.modules, report.facts) == (1, 2, 2)
    assert "1 skill(s), 2 module(s)" in report.summary()


def test_a_module_may_share_its_own_skills_name(repo):
    built(repo, "demo")
    assert findings(repo) == []


def test_a_router_without_its_table_fires(repo):
    skill_dir = built(repo, "first")
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    (skill_dir / "SKILL.md").write_text(text.replace("| Module |", "| Name |"), encoding="utf-8")
    assert findings(repo)[0] == (
        "skills/demo/SKILL.md",
        "modules",
        "the Modules section has no table headed Module | Read it for",
    )


@pytest.mark.parametrize(
    ("row", "message"),
    [
        (
            "| first | x |",
            "line 12: a router row starts with [`name`](references/name.md)",
        ),
        (
            "| [`first`](references/other.md) | x |",
            "line 12: `first` links references/other.md, not references/first.md",
        ),
    ],
)
def test_a_malformed_router_row_fires(repo, row, message):
    skill_dir = built(repo, "first")
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    old = "| [`first`](references/first.md) | first requests |"
    (skill_dir / "SKILL.md").write_text(text.replace(old, row), encoding="utf-8")
    assert ("skills/demo/SKILL.md", "modules", message) in findings(repo)


def test_a_module_routed_twice_fires(repo):
    skill_dir = built(repo, "first")
    modules.add_row(skill_dir / "SKILL.md", "| [`first`](references/first.md) | again |")
    assert findings(repo) == [
        ("skills/demo/SKILL.md", "modules", "line 13: `first` is routed twice")
    ]


def test_an_empty_router_fires(repo):
    skill_dir = repo.modular_skill("demo")
    repo.catalog(repo.plugin("demo", "./skills/demo"))
    assert findings(repo) == [("skills/demo/SKILL.md", "modules", "the router lists no modules")]
    assert skill_dir.is_dir()


def test_a_routed_module_without_its_file_fires(repo):
    skill_dir = built(repo, "first")
    (skill_dir / "references" / "first.md").unlink()
    assert (
        "skills/demo/SKILL.md",
        "modules",
        "`first` has no file at skills/demo/references/first.md",
    ) in findings(repo)


def test_a_module_missing_sections_fires(repo):
    skill_dir = built(repo, "first")
    path = skill_dir / "references" / "first.md"
    text = path.read_text(encoding="utf-8").replace("## Why", "## Reasons")
    path.write_text(text.replace("## Sources", "## Cited"), encoding="utf-8")
    assert findings(repo) == [
        ("skills/demo/references/first.md", "modules", "missing the section(s) Why, Sources")
    ]


@pytest.mark.parametrize(
    ("content", "message"),
    [
        (None, "`first` has no trigger tests"),
        ("[", "not JSON: Expecting value: line 1 column 2 (char 1)"),
        ('[{"query": 1}]', 'a list of {"query": text, "should_trigger": true or false}'),
        (
            '[{"query": "q", "should_trigger": true}]',
            "needs requests that should reach the module and near misses that shouldn't",
        ),
        (
            '[{"query": "TODO(new-skill) q", "should_trigger": true}]',
            "a request still marked TODO(new-skill)",
        ),
    ],
)
def test_a_module_needs_sound_trigger_tests(repo, content, message):
    built(repo, "first")
    fixture = repo.root / modules.FIXTURES / "first.json"
    if content is None:
        fixture.unlink()
    else:
        fixture.write_text(content, encoding="utf-8")
    found = [(path, text) for path, _, text in findings(repo)]
    assert found == [("tests/fixtures/modules/first.json", message)]


def test_an_unrouted_reference_fires(repo):
    skill_dir = built(repo, "first")
    (skill_dir / "references" / "notes.md").write_text("# Notes\n", encoding="utf-8")
    assert findings(repo) == [
        (
            "skills/demo/references/notes.md",
            "modules",
            "no router row reads this file; a skill made of modules holds only modules",
        )
    ]


def test_a_module_in_two_skills_fires(repo):
    repo.modular_skill("one", "shared")
    two = repo.skill_file(
        "two",
        "---\nname: two\ndescription: Two. Use when testing.\n---\n\n## Modules\n\n"
        "| Module | Read it for |\n|---|---|\n| [`shared`](references/shared.md) | x |\n",
    )
    (two / "references").mkdir()
    (two / "references" / "shared.md").write_text(
        (repo.root / "skills/one/references/shared.md")
        .read_text(encoding="utf-8")
        .replace("shared-fact", "other-fact"),
        encoding="utf-8",
    )
    repo.catalog(repo.plugin("p", "./skills/one", "./skills/two"))
    assert findings(repo) == [
        ("skills/two/SKILL.md", "modules", "`shared` is also a module of `one`")
    ]


def test_a_module_named_like_another_skill_fires(repo):
    repo.modular_skill("one", "two")
    repo.modular_skill("two", "other")
    repo.catalog(repo.plugin("p", "./skills/one", "./skills/two"))
    assert findings(repo) == [
        ("skills/one/SKILL.md", "modules", "`two` is also the name of a skill")
    ]


def test_a_module_names_only_its_own_facts(repo):
    skill_dir = built(repo, "first", "second")
    path = skill_dir / "references" / "first.md"
    text = path.read_text(encoding="utf-8").replace("(fact `first-fact`)", "(fact `second-fact`)")
    path.write_text(text, encoding="utf-8")
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(
        skill_md.read_text(encoding="utf-8") + "\nSee fact `nowhere`.\n", encoding="utf-8"
    )
    assert findings(repo) == [
        (
            "skills/demo/references/first.md",
            "facts",
            "line 7 names fact `second-fact`, not defined in its Facts section",
        ),
        (
            "skills/demo/SKILL.md",
            "facts",
            "line 15 names fact `nowhere`, not defined in any of its modules' Facts sections",
        ),
    ]


def test_a_malformed_fact_in_a_module_fires(repo):
    skill_dir = built(repo, "first")
    path = skill_dir / "references" / "first.md"
    text = path.read_text(encoding="utf-8").replace("2027-04-01", "2026-01-01")
    path.write_text(text, encoding="utf-8")
    assert findings(repo)[0] == (
        "skills/demo/references/first.md",
        "facts",
        "line 27: the check-by date is not after the checked date",
    )


def test_a_fact_id_is_defined_once_across_the_repository(repo):
    built(repo, "first")
    other = repo.skill("other")
    (other / "references" / "facts.md").write_text(
        "| ID | Fact | Source | Quote | Checked | Check by |\n|---|---|---|---|---|---|\n"
        '| `first-fact` | Again | [p](https://example.com) | "q" | 2026-10-01 | 2027-01-01 |\n',
        encoding="utf-8",
    )
    repo.catalog(repo.plugin("demo", "./skills/demo", "./skills/other"))
    repo.roadmap({"demo": "shipped", "other": "shipped"}, {"first": ("demo", "shipped")})
    assert findings(repo) == [
        (
            "skills/other/references/facts.md",
            "facts",
            "line 3: `first-fact` is already defined in skills/demo/references/first.md",
        )
    ]


def test_due_reads_facts_inside_modules(repo, capsys):
    built(repo, "first")
    (repo.root / "skills" / "loose").mkdir()
    assert main([str(repo.root), "--due", "2027-04-01"]) == 1
    out = capsys.readouterr().out
    assert "skills/demo/references/first.md:27: due: `first-fact`" in out


def test_due_skips_a_routed_module_with_no_file(repo, capsys):
    skill_dir = built(repo, "first", "second")
    (skill_dir / "references" / "second.md").unlink()
    assert main([str(repo.root), "--due", "2026-01-01"]) == 0
    assert "skillcheck: 1 fact(s), 0 due by 2026-01-01" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("rows", "message"),
    [
        ({}, ("skills/demo/SKILL.md", "module `first` is not listed as shipped in ROADMAP.md")),
        (
            {"first": ("demo", "planned")},
            ("skills/demo/SKILL.md", "module `first` is not listed as shipped in ROADMAP.md"),
        ),
        (
            {"first": ("other", "shipped")},
            ("ROADMAP.md", "module `first` is marked shipped in `other`, which doesn't route it"),
        ),
        (
            {"first": ("demo", "shipped"), "ghost": ("demo", "shipped")},
            ("ROADMAP.md", "module `ghost` is marked shipped in `demo`, which doesn't route it"),
        ),
        (
            {"first": ("demo", "shipped"), "later": ("demo", "someday")},
            (
                "ROADMAP.md",
                "module `later` has status 'someday'; use one of "
                "shipped, building, researching, planned",
            ),
        ),
    ],
)
def test_the_roadmap_keeps_step_with_the_routers(repo, rows, message):
    built(repo, "first")
    repo.roadmap({"demo": "shipped"}, rows)
    found = [(path, text) for path, _, text in findings(repo)]
    assert message in found


def test_a_roadmap_row_naming_another_skill_fires(repo):
    built(repo, "first")
    path = repo.root / "ROADMAP.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace("| `first` | `demo` |", "| `first` | demo |"),
        encoding="utf-8",
    )
    assert ("skills/demo/SKILL.md", "roadmap", "ROADMAP.md gives module `first` another skill") in (
        findings(repo)
    )


def test_a_module_listed_twice_in_the_roadmap_fires(repo):
    built(repo, "first")
    path = repo.root / "ROADMAP.md"
    path.write_text(
        path.read_text(encoding="utf-8") + "| `first` | `demo` | shipped |\n", encoding="utf-8"
    )
    assert findings(repo) == [("ROADMAP.md", "roadmap", "module `first` is listed 2 times")]


def test_modules_are_checked_without_a_roadmap(repo):
    repo.modular_skill("demo", "first")
    repo.catalog(repo.plugin("demo", "./skills/demo"))
    assert findings(repo) == []


def test_sections_skip_headings_in_code_and_number_lines():
    text = "# T\n\n## One\n\na\n```\n## Not\n```\n## Two\nb\n"
    found = modules.sections(text)
    assert list(found) == ["One", "Two"]
    assert found["Two"] == [(10, "b")]


def test_add_row_mends_a_table_with_no_final_newline(repo):
    skill_dir = repo.modular_skill("demo", "first")
    path = skill_dir / "SKILL.md"
    path.write_text(path.read_text(encoding="utf-8").rstrip("\n"), encoding="utf-8")
    modules.add_row(path, "| [`second`](references/second.md) | x |")
    assert path.read_text(encoding="utf-8").endswith(
        "first requests |\n| [`second`](references/second.md) | x |\n"
    )


def test_the_fixture_helper_writes_both_kinds_of_case(repo):
    repo.modular_skill("demo", "first")
    cases = json.loads((repo.root / modules.FIXTURES / "first.json").read_text(encoding="utf-8"))
    assert {case["should_trigger"] for case in cases} == {True, False}
