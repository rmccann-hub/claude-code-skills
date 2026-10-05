"""The house-style skill's Vale style and prose workflow work as its references say."""

import configparser
import re
import zipfile
from io import BytesIO
from pathlib import Path

import pytest
import yaml

from skillcheck import release

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "house-style"
PACKAGE = SKILL / "assets" / "vale" / "HouseStyle"
STYLE = PACKAGE / "styles" / "HouseStyle"
WORKFLOW = SKILL / "assets" / "workflows" / "prose.yml"
RULES = sorted(path.stem for path in STYLE.glob("*.yml"))
CANARY = "Prove the style catches each kind of mistake"


class UniqueKeys(yaml.SafeLoader):
    """Refuses a key given twice, where YAML would keep the last one without a word."""


def _mapping(loader: UniqueKeys, node: yaml.MappingNode) -> dict:
    keys = [loader.construct_object(key) for key, _ in node.value]
    repeated = sorted({key for key in keys if keys.count(key) > 1})
    if repeated:
        raise yaml.constructor.ConstructorError(
            None, None, f"keys given twice: {repeated}", node.start_mark
        )
    return loader.construct_mapping(node)


UniqueKeys.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def rule(name: str) -> dict:
    return yaml.load((STYLE / f"{name}.yml").read_text(encoding="utf-8"), Loader=UniqueKeys)


def ini(path: Path) -> configparser.ConfigParser:
    # Vale's keys before the first section have no heading of their own.
    config = configparser.ConfigParser(interpolation=None)
    config.optionxform = str
    config.read_string("[core]\n" + path.read_text(encoding="utf-8"))
    return config


def canary() -> tuple[list[str], str]:
    """The rules the canary step expects to fire, and the text it writes."""
    steps = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))["jobs"]["prose"]["steps"]
    [script] = [step["run"] for step in steps if step.get("name") == CANARY]
    expected = re.search(r"for rule in ([\w ]+); do", script)[1].split()
    text = re.search(r"printf '([^']*)'", script)[1].replace("\\n", "\n")
    return expected, text


def test_the_repeated_key_check_works():
    with pytest.raises(yaml.constructor.ConstructorError, match=r"given twice: \['colour'\]"):
        yaml.load("colour: color\ncolour: colour\n", Loader=UniqueKeys)


def test_each_rule_is_an_error_with_a_message():
    assert RULES == ["Filler", "Headings", "Spelling"]
    for name in RULES:
        spec = rule(name)
        assert spec["level"] == "error"
        assert "%s" in spec["message"]


def test_the_skill_names_each_rule_the_style_has():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert sorted(set(re.findall(r"`HouseStyle\.([A-Z]\w*)`", text))) == RULES


def test_the_release_packs_the_style_as_vale_installs_it():
    packs = release.vale_packages(ROOT)
    assert set(packs) == {"HouseStyle.zip"}
    names = zipfile.ZipFile(BytesIO(packs["HouseStyle.zip"])).namelist()
    assert names == [
        "HouseStyle/.vale.ini",
        *(f"HouseStyle/styles/HouseStyle/{name}.yml" for name in RULES),
    ]


def test_the_style_runs_on_every_markdown_file():
    assert ini(PACKAGE / ".vale.ini")["*.md"]["BasedOnStyles"] == "HouseStyle"


def test_this_repository_checks_itself_with_the_style_from_its_source():
    # A changed rule meets this repository's own text in the same pull request, not after a
    # release.
    assert ini(ROOT / ".vale.ini")["core"]["Packages"] == PACKAGE.relative_to(ROOT).as_posix()


def test_the_setup_reference_names_the_style_the_release_publishes():
    text = (SKILL / "references" / "setup.md").read_text(encoding="utf-8")
    [url] = re.findall(r"^Packages = (\S+)$", text, re.MULTILINE)
    repository = release._repository(ROOT)
    assert url == f"https://github.com/{repository}/releases/latest/download/HouseStyle.zip"


def test_the_kickstart_file_names_the_style_each_release_carries():
    named = set(re.findall(r"\b[A-Z]\w*\.zip\b", release.INSTRUCTIONS.read_text("utf-8")))
    assert named == set(release.vale_packages(ROOT))


def test_the_filler_rule_catches_the_words_rule_3_names():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    [rule_3] = re.findall(r"^3\. (.+?)^4\. ", text, re.MULTILINE | re.DOTALL)
    words = re.findall(r"`(\w+)`", rule_3)
    tokens = rule("Filler")["tokens"]
    assert len(words) == len(tokens) == 6
    for word, token in zip(words, tokens, strict=True):
        assert re.fullmatch(token, word, re.IGNORECASE), (word, token)


def test_the_spelling_rule_never_flags_its_own_answer():
    spelling = rule("Spelling")
    swap = spelling["swap"]
    assert len(swap) > 100
    assert all(word == word.lower() and word != answer for word, answer in swap.items())
    assert not set(swap) & set(swap.values())
    # An exception is a name that keeps a spelling the rule would otherwise swap.
    for name in spelling["exceptions"]:
        assert any(word.lower() in swap for word in name.split()), name


def test_the_canary_breaks_each_rule():
    expected, text = canary()
    assert sorted(expected) == RULES
    [heading] = re.findall(r"^# (.+)$", text, re.MULTILINE)
    names = rule("Headings")["exceptions"]
    assert any(word[0].isupper() and word not in names for word in heading.split()[1:])
    body = text.split("\n", 1)[1]
    assert any(
        re.search(rf"\b{token}\b", body, re.IGNORECASE) for token in rule("Filler")["tokens"]
    )
    assert any(re.search(rf"\b{word}\b", body, re.IGNORECASE) for word in rule("Spelling")["swap"])


def test_the_workflow_installs_the_vale_version_the_facts_name():
    env = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))["jobs"]["prose"]["env"]
    version = env["VALE_VERSION"]
    assert f"`refs/tags/{version}`" in (SKILL / "references" / "facts.md").read_text("utf-8")
    assert f"/cmd/vale@{version}\n" in (SKILL / "references" / "setup.md").read_text("utf-8")


def test_this_repository_runs_the_shipped_prose_check():
    # The repository checks its own prose with the example, unchanged.
    own = ROOT / ".github" / "workflows" / "prose.yml"
    assert own.read_bytes() == WORKFLOW.read_bytes()
