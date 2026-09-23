"""Each rule fires on a planted defect, alone, and stays quiet on a clean repository."""

import pytest
from conftest import DEFAULT_DESCRIPTION

from skillcheck.core.checks import (
    MAX_COMPATIBILITY_LENGTH,
    MAX_DESCRIPTION_LENGTH,
    MAX_NAME_LENGTH,
    MAX_SKILL_LINES,
    check_repository,
)


def rules(report) -> set[str]:
    return {finding.rule for finding in report.findings}


def test_empty_repository_says_nothing_was_checked(repo):
    report = check_repository(repo.root)
    assert report.findings == []
    assert report.summary() == (
        "skillcheck: 0 skill(s), 0 description characters, no catalog, no roadmap, no standard, "
        "0 finding(s)"
    )


def test_clean_repository_passes(repo):
    repo.skill("example-skill")
    repo.catalog(repo.plugin("example", "./skills/example-skill"))
    report = check_repository(repo.root)
    assert report.findings == []
    assert report.summary() == (
        f"skillcheck: 1 skill(s), {len(DEFAULT_DESCRIPTION)} description characters, "
        "1 catalog plugin(s), no roadmap, no standard, 0 finding(s)"
    )


def test_limits_are_inclusive(repo):
    name = "a" * MAX_NAME_LENGTH
    repo.skill(name, f"name: {name}\ndescription: {'d' * MAX_DESCRIPTION_LENGTH}\n")
    repo.catalog(repo.plugin("example", f"./skills/{name}"))
    assert check_repository(repo.root).findings == []


def test_whole_folder_entry_lists_every_skill(repo):
    repo.skill("first-skill")
    repo.skill("second-skill")
    repo.catalog(repo.plugin("everything", "./skills/"))
    assert check_repository(repo.root).findings == []


@pytest.mark.parametrize(
    ("directory", "frontmatter", "expected"),
    [
        ("mismatched", "name: other-name\ndescription: d\n", "name"),
        ("Bad_Name", "name: Bad_Name\ndescription: d\n", "name"),
        ("double--hyphen", "name: double--hyphen\ndescription: d\n", "name"),
        (
            "a" * (MAX_NAME_LENGTH + 1),
            f"name: {'a' * (MAX_NAME_LENGTH + 1)}\ndescription: d\n",
            "name",
        ),
        ("no-name", "description: d\n", "name"),
        ("no-description", "name: no-description\n", "description"),
        ("blank-description", "name: blank-description\ndescription: '  '\n", "description"),
        (
            "long-description",
            f"name: long-description\ndescription: {'d' * (MAX_DESCRIPTION_LENGTH + 1)}\n",
            "description",
        ),
        (
            "extra-field",
            "name: extra-field\ndescription: d\nwhen_to_use: never\n",
            "frontmatter-keys",
        ),
        ("empty-license", "name: empty-license\ndescription: d\nlicense: ''\n", "license"),
        ("list-license", "name: list-license\ndescription: d\nlicense: [MIT]\n", "license"),
        (
            "long-compatibility",
            "name: long-compatibility\ndescription: d\n"
            f"compatibility: {'c' * (MAX_COMPATIBILITY_LENGTH + 1)}\n",
            "compatibility",
        ),
        (
            "empty-compatibility",
            "name: empty-compatibility\ndescription: d\ncompatibility: ''\n",
            "compatibility",
        ),
        (
            "unquoted-version",
            "name: unquoted-version\ndescription: d\nmetadata:\n  version: 1.0\n",
            "metadata",
        ),
        (
            "nested-metadata",
            "name: nested-metadata\ndescription: d\nmetadata:\n  owner:\n    team: x\n",
            "metadata",
        ),
        ("list-metadata", "name: list-metadata\ndescription: d\nmetadata: [a, b]\n", "metadata"),
        (
            "listed-tools",
            "name: listed-tools\ndescription: d\nallowed-tools: [Read, Grep]\n",
            "allowed-tools",
        ),
    ],
)
def test_frontmatter_rule_fires_alone(repo, directory, frontmatter, expected):
    repo.skill(directory, frontmatter)
    repo.catalog(repo.plugin("example", f"./skills/{directory}"))
    assert rules(check_repository(repo.root)) == {expected}


@pytest.mark.parametrize(
    "text",
    [
        "name: no-delimiters\ndescription: d\n",
        "---\nname: unclosed\ndescription: d\n",
        "---\n- a\n- list\n---\n",
        "---\nname: [unclosed\n---\n",
    ],
)
def test_unreadable_frontmatter_fires(repo, text):
    repo.skill_file("broken", text)
    repo.catalog(repo.plugin("example", "./skills/broken"))
    assert rules(check_repository(repo.root)) == {"frontmatter"}


def test_skill_directory_without_skill_md_fires(repo):
    (repo.root / "skills" / "empty").mkdir(parents=True)
    assert rules(check_repository(repo.root)) == {"layout"}


def test_stray_file_in_skills_fires(repo):
    repo.skill("example-skill")
    (repo.root / "skills" / "notes.md").write_text("stray\n", encoding="utf-8")
    repo.catalog(repo.plugin("example", "./skills/example-skill"))
    assert rules(check_repository(repo.root)) == {"layout"}


def test_skill_missing_from_catalog_fires(repo):
    repo.skill("listed-skill")
    repo.skill("unlisted-skill")
    repo.catalog(repo.plugin("example", "./skills/listed-skill"))
    report = check_repository(repo.root)
    assert [(f.path, f.rule) for f in report.findings] == [("skills/unlisted-skill", "catalog")]


def test_catalog_path_to_missing_skill_fires(repo):
    repo.skill("example-skill")
    repo.catalog(repo.plugin("example", "./skills/example-skill", "./skills/typo-skill"))
    assert rules(check_repository(repo.root)) == {"catalog"}


def test_catalog_path_outside_skills_fires(repo):
    repo.skill("example-skill")
    repo.catalog(repo.plugin("example", "./skills/example-skill", "./other/example-skill"))
    assert rules(check_repository(repo.root)) == {"catalog"}


def test_skill_in_two_plugins_fires(repo):
    repo.skill("shared-skill")
    repo.catalog(
        repo.plugin("first", "./skills/shared-skill"),
        repo.plugin("second", "./skills/shared-skill"),
    )
    assert rules(check_repository(repo.root)) == {"catalog"}


def test_skills_without_catalog_fire(repo):
    repo.skill("example-skill")
    report = check_repository(repo.root)
    assert [(f.path, f.rule) for f in report.findings] == [
        (".claude-plugin/marketplace.json", "catalog")
    ]


@pytest.mark.parametrize("skills", [{"not": "a list"}, [42]])
def test_malformed_skills_field_fires(repo, skills):
    repo.skill("example-skill")
    repo.catalog(
        repo.plugin("example", "./skills/example-skill"),
        {"name": "malformed", "source": "./", "skills": skills},
    )
    assert rules(check_repository(repo.root)) == {"catalog"}


def test_single_path_string_is_accepted(repo):
    repo.skill("example-skill")
    repo.catalog({"name": "example", "source": "./", "skills": "./skills/example-skill"})
    assert check_repository(repo.root).findings == []


@pytest.mark.parametrize("text", ["{not json", '{"name": "no-plugins"}', "[]"])
def test_unreadable_catalog_fires(repo, text):
    repo.catalog_text(text)
    assert rules(check_repository(repo.root)) == {"catalog"}


def test_entries_from_other_sources_are_not_ours_to_check(repo):
    repo.skill("example-skill")
    repo.catalog(
        repo.plugin("example", "./skills/example-skill"),
        {"name": "elsewhere", "source": {"source": "github", "repo": "someone/else"}},
    )
    assert check_repository(repo.root).findings == []


def test_description_characters_are_summed_across_skills(repo):
    repo.skill("first-skill")
    repo.skill("second-skill", "name: second-skill\ndescription: twelve chars\n")
    repo.catalog(repo.plugin("example", "./skills/first-skill", "./skills/second-skill"))
    report = check_repository(repo.root)
    assert report.description_chars == len(DEFAULT_DESCRIPTION) + len("twelve chars")


def test_link_to_missing_bundled_file_fires(repo):
    repo.skill("example-skill", body="See [the guide](references/guide.md).\n")
    repo.catalog(repo.plugin("example", "./skills/example-skill"))
    report = check_repository(repo.root)
    assert [(f.rule, f.message) for f in report.findings] == [
        ("reference", "links to references/guide.md, which does not exist")
    ]


def test_links_that_resolve_or_point_elsewhere_pass(repo):
    body = (
        "[guide](references/guide.md) [part](references/guide.md#setup) [web](https://example.com/x)\n"
        "[here](#usage) [mail](mailto:someone@example.com) [absolute](/etc/hosts)\n"
    )
    skill_dir = repo.skill("example-skill", body=body)
    (skill_dir / "references").mkdir()
    (skill_dir / "references" / "guide.md").write_text("guide\n", encoding="utf-8")
    repo.catalog(repo.plugin("example", "./skills/example-skill"))
    assert check_repository(repo.root).findings == []


def test_optional_fields_in_spec_form_pass(repo):
    frontmatter = (
        "name: full-skill\ndescription: d\nlicense: Apache-2.0\n"
        f"compatibility: {'c' * MAX_COMPATIBILITY_LENGTH}\n"
        'metadata:\n  author: example-org\n  version: "1.0"\n'
        "allowed-tools: Bash(git:*) Read\n"
    )
    repo.skill("full-skill", frontmatter)
    repo.catalog(repo.plugin("example", "./skills/full-skill"))
    assert check_repository(repo.root).findings == []


def skill_of_lines(repo, total: int) -> None:
    frontmatter = "---\nname: sized-skill\ndescription: d\n---\n"
    body_lines = total - frontmatter.count("\n")
    repo.skill_file("sized-skill", frontmatter + "line\n" * body_lines)
    repo.catalog(repo.plugin("example", "./skills/sized-skill"))


def test_skill_md_under_the_line_limit_passes(repo):
    skill_of_lines(repo, MAX_SKILL_LINES - 1)
    assert check_repository(repo.root).findings == []


def test_skill_md_at_the_line_limit_fires(repo):
    skill_of_lines(repo, MAX_SKILL_LINES)
    report = check_repository(repo.root)
    assert [(f.rule, f.message) for f in report.findings] == [
        ("size", f"SKILL.md is {MAX_SKILL_LINES} lines; keep it under {MAX_SKILL_LINES}")
    ]


def test_reference_that_links_to_another_reference_fires(repo):
    skill_dir = repo.skill("chained-skill", body="See [a](references/a.md).\n")
    (skill_dir / "references").mkdir()
    (skill_dir / "references" / "a.md").write_text("Then [b](b.md).\n", encoding="utf-8")
    (skill_dir / "references" / "b.md").write_text("b\n", encoding="utf-8")
    repo.catalog(repo.plugin("example", "./skills/chained-skill"))
    report = check_repository(repo.root)
    assert [(f.path, f.rule, f.message) for f in report.findings] == [
        (
            "skills/chained-skill/references/a.md",
            "reference-depth",
            "links to references/b.md; keep references one level deep from SKILL.md",
        )
    ]


def test_reference_links_back_out_or_to_scripts_pass(repo):
    skill_dir = repo.skill("flat-skill", body="See [a](references/a.md).\n")
    (skill_dir / "references").mkdir()
    (skill_dir / "scripts").mkdir()
    (skill_dir / "scripts" / "run.py").write_text("print()\n", encoding="utf-8")
    (skill_dir / "references" / "a.md").write_text(
        "[back](../SKILL.md) [script](../scripts/run.py) [web](https://example.com/x.md)"
        " [missing](gone.md) [here](#top)\n",
        encoding="utf-8",
    )
    repo.catalog(repo.plugin("example", "./skills/flat-skill"))
    assert check_repository(repo.root).findings == []


@pytest.mark.parametrize("char", ["\u202e", "\u200b", "\u2066", "\ufeff", "\U000e0041"])
def test_hidden_character_in_skill_md_fires(repo, char):
    repo.skill("hidden-skill", body=f"Innocent{char} text.\n")
    repo.catalog(repo.plugin("example", "./skills/hidden-skill"))
    report = check_repository(repo.root)
    assert [(f.path, f.rule) for f in report.findings] == [
        ("skills/hidden-skill/SKILL.md", "unicode")
    ]
    assert f"U+{ord(char):04X}" in report.findings[0].message
    assert "line 6" in report.findings[0].message


def test_hidden_character_in_a_bundled_file_fires(repo):
    skill_dir = repo.skill("bundled-skill")
    (skill_dir / "scripts").mkdir()
    (skill_dir / "scripts" / "run.sh").write_text("echo ok\u202e\n", encoding="utf-8")
    (skill_dir / "assets.bin").write_bytes(b"\xff\xfe\x00binary")
    repo.catalog(repo.plugin("example", "./skills/bundled-skill"))
    report = check_repository(repo.root)
    assert [(f.path, f.rule) for f in report.findings] == [
        ("skills/bundled-skill/scripts/run.sh", "unicode")
    ]


def test_link_to_another_skill_is_not_a_reference_chain(repo):
    repo.skill("first-skill", body="Pairs with [second](../second-skill/SKILL.md).\n")
    repo.skill("second-skill", body="Back to [first](../first-skill/SKILL.md).\n")
    repo.catalog(repo.plugin("example", "./skills/first-skill", "./skills/second-skill"))
    assert check_repository(repo.root).findings == []


def test_several_hidden_characters_are_counted_once_per_file(repo):
    repo.skill("hidden-skill", body="One​ two​ three‮.\n")
    repo.catalog(repo.plugin("example", "./skills/hidden-skill"))
    report = check_repository(repo.root)
    assert [(f.rule, f.message) for f in report.findings] == [
        (
            "unicode",
            "line 6 holds U+200B, which is invisible or reorders text, and 2 more in this file",
        )
    ]


def test_link_to_a_bundled_script_is_checked_for_existence_only(repo):
    skill_dir = repo.skill("script-skill", body="Run [the build](scripts/build.sh).\n")
    (skill_dir / "scripts").mkdir()
    (skill_dir / "scripts" / "build.sh").write_text("echo [not](a-link.md)\n", encoding="utf-8")
    repo.catalog(repo.plugin("example", "./skills/script-skill"))
    assert check_repository(repo.root).findings == []
