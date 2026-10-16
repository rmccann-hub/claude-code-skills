"""The exclusion list is well formed, never hides a skill shipped here, and this repo applies it."""

import json

import pytest

from skillcheck.core.checks import EXCLUSIONS, SETTINGS, check_repository

LIST = f"skills/demo-skill/{EXCLUSIONS}"


def plant(repo, overrides, reasons=None, applied=None):
    repo.skill("demo-skill")
    repo.catalog(repo.plugin("demo", "./skills/demo-skill"))
    path = repo.root / LIST
    path.parent.mkdir(parents=True)
    if reasons is None:
        reasons = {name: "a reason" for name in overrides}
    path.write_text(json.dumps({"skillOverrides": overrides, "reasons": reasons}), "utf-8")
    if applied is not None:
        (repo.root / ".claude").mkdir()
        applied = {"demo-skill": "off", **applied}
        (repo.root / SETTINGS).write_text(json.dumps({"skillOverrides": applied}), "utf-8")


def found(repo) -> list[tuple[str, str, str]]:
    return [(f.path, f.rule, f.message) for f in check_repository(repo.root).findings]


def test_a_list_applied_here_passes(repo):
    plant(
        repo,
        {"chat-only": "off", "named": "name-only"},
        applied={"chat-only": "off", "named": "on"},
    )
    assert found(repo) == []


@pytest.mark.parametrize(
    ("overrides", "reasons", "message"),
    [
        ({"Bad_Name": "off"}, None, "'Bad_Name' isn't a skill name"),
        ({"chat-only": "hidden"}, None, "chat-only: 'hidden' isn't one of"),
        ({"demo-skill": "off"}, None, "demo-skill ships here, and the list would hide it"),
        ({"chat-only": "off"}, {"chat-only": " "}, "chat-only has no reason"),
        ({"chat-only": "off"}, {"chat-only": "x", "other": "y"}, "other has a reason but no"),
    ],
)
def test_each_defect_in_the_list_fires_alone(repo, overrides, reasons, message):
    plant(repo, overrides, reasons, applied=dict.fromkeys(overrides, "off"))
    ((path, rule, text),) = found(repo)
    assert (path, rule) == (LIST, "exclusions")
    assert text.startswith(message)


@pytest.mark.parametrize(
    "text", ["not json", "[]", '{"skillOverrides": {}}', '{"skillOverrides": [], "reasons": {}}']
)
def test_a_list_of_the_wrong_shape_is_one_finding(repo, text):
    plant(repo, {})
    (repo.root / LIST).write_text(text, "utf-8")
    assert found(repo) == [
        (LIST, "exclusions", 'needs "skillOverrides" and "reasons", each an object')
    ]


@pytest.mark.parametrize(
    "settings", [None, "not json", '{"skillOverrides": {"chat-only": "off", "demo-skill": "off"}}']
)
def test_this_repository_applies_every_entry(repo, settings):
    plant(repo, {"chat-only": "off", "tool-only": "off"})
    if settings is not None:
        (repo.root / ".claude").mkdir()
        (repo.root / SETTINGS).write_text(settings, "utf-8")
    missing = "tool-only" if settings and "chat-only" in settings else "chat-only, tool-only"
    count = len(missing.split(", "))
    assert found(repo) == [
        (SETTINGS, "exclusions", f"skillOverrides lacks {count} of {LIST}'s entries: {missing}")
    ]


@pytest.mark.parametrize(
    "settings",
    [
        {"skillOverrides": {"demo-skill": "on"}},
        {"skillOverrides": {"other": "off"}},
    ],
)
def test_settings_here_hide_every_installed_copy_of_a_skill_here(repo, settings):
    repo.skill("demo-skill")
    repo.catalog(repo.plugin("demo", "./skills/demo-skill"))
    (repo.root / ".claude").mkdir()
    (repo.root / SETTINGS).write_text(json.dumps(settings), "utf-8")
    ((path, rule, text),) = found(repo)
    assert (path, rule) == (SETTINGS, "own-copies")
    assert text.startswith("skillOverrides doesn't turn off demo-skill, so")


@pytest.mark.parametrize(
    "settings",
    ["not json", "{}", '{"skillOverrides": []}', '{"skillOverrides": {"demo-skill": "off"}}'],
)
def test_settings_without_overrides_or_hiding_every_skill_pass(repo, settings):
    repo.skill("demo-skill")
    repo.catalog(repo.plugin("demo", "./skills/demo-skill"))
    (repo.root / ".claude").mkdir()
    (repo.root / SETTINGS).write_text(settings, "utf-8")
    assert found(repo) == []
