"""The house-style skill's Vale style, prose workflow and wrap check work as its references say."""

import configparser
import re
import subprocess
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
WRAP_CHECK = SKILL / "scripts" / "wrap-check.sh"
LONG = "x" * 101


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


def test_the_check_module_names_each_rule_the_style_has():
    text = (SKILL / "references" / "prose-check.md").read_text(encoding="utf-8")
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


def quoted(text: str) -> list[str]:
    """What the package's TokenIgnores skips in a text, as Vale's Go regexp would find it."""
    pattern = ini(PACKAGE / ".vale.ini")["*.md"]["TokenIgnores"]
    # Vale splits TokenIgnores at each comma not written as "\,".
    assert "," not in pattern.replace("\\,", "")
    return re.findall(pattern, text)


def test_the_style_skips_a_quote_wrapped_within_its_paragraph():
    assert quoted('The "colour of\n  the sky" is blue.') == ['"colour of\n  the sky"']
    assert quoted('"Colour,\n2026 and 3.5 more" (and "this")') == [
        '"Colour,\n2026 and 3.5 more"',
        '"this"',
    ]
    assert quoted('A "say \\"hi\\" colour" here.') == ['"say \\"hi\\" colour"']


def test_an_inch_mark_or_a_quote_in_code_opens_no_quote():
    # A mark after a letter, a digit or a backtick opens nothing, so it can't pair with the
    # next quote and hide the words between.
    assert quoted('A 3" board with colour and "a quote".') == ['"a quote"']
    assert quoted('A 3.5" board, 4"x2" and colour.') == []
    assert quoted('Use `"` in code, then colour and "x".') == ['"x"']


@pytest.mark.parametrize("blank", ["", "   "])
def test_an_unclosed_quote_never_hides_the_next_paragraph(blank):
    assert not any("colour" in match for match in quoted(f'Say "hi.\n{blank}\nThe colour".'))


@pytest.mark.parametrize(
    "opener", ["- ", "* ", "+ ", "1. ", "2) ", "10. ", "| ", "```", "~~~", "# ", "> "]
)
def test_an_unclosed_quote_never_hides_a_list_table_fence_heading_or_block_quote(opener):
    assert not any("colour" in match for match in quoted(f'Say "hi:\n{opener}colour".'))


def test_this_repository_checks_itself_with_the_style_from_its_source():
    # A changed rule meets this repository's own text in the same pull request, not after a
    # release.
    assert ini(ROOT / ".vale.ini")["core"]["Packages"] == PACKAGE.relative_to(ROOT).as_posix()


def test_the_setup_reference_names_the_style_the_release_publishes():
    text = (SKILL / "references" / "prose-check.md").read_text(encoding="utf-8")
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
    assert f"`refs/tags/{version}`" in (SKILL / "references" / "prose-check.md").read_text("utf-8")
    assert f"/cmd/vale@{version}\n" in (SKILL / "references" / "prose-check.md").read_text("utf-8")


def test_this_repository_runs_the_shipped_prose_check():
    # The repository checks its own prose with the example, unchanged.
    own = ROOT / ".github" / "workflows" / "prose.yml"
    assert own.read_bytes() == WORKFLOW.read_bytes()


def wrap_check(tmp_path: Path, text: str) -> tuple[int, list[int]]:
    """The wrap check's exit status, and the line numbers it names, on one file."""
    page = tmp_path / "page.md"
    page.write_text(text, encoding="utf-8")
    run = subprocess.run(
        ["sh", str(WRAP_CHECK), str(page)], capture_output=True, text=True, check=False
    )
    return run.returncode, [int(line.rsplit(":", 1)[1]) for line in run.stdout.splitlines()]


def test_the_wrap_check_passes_lines_of_100_characters_counted_as_characters(tmp_path):
    # An em dash is three bytes in UTF-8 and one character.
    assert wrap_check(tmp_path, "x" * 100 + "\n" + "\u2014" * 100 + "\n") == (0, [])
    assert wrap_check(tmp_path, f"# Title\n\n{LONG}\n") == (1, [3])


def test_the_wrap_check_skips_frontmatter_tables_and_the_length_of_a_url(tmp_path):
    text = (
        f"---\ndescription: {LONG}\n---\n"
        f"| {LONG} |\n"
        f"see https://example.com/{LONG}\n"
        f"a [link](https://example.com/) then {LONG}\n"
    )
    assert wrap_check(tmp_path, text) == (1, [6])


def test_the_wrap_check_skips_fenced_code_and_closes_a_fence_only_on_its_own_mark(tmp_path):
    text = (
        f"````markdown\n```\n{LONG}\n```\n{LONG}\n````\n"
        f"~~~\n```\n{LONG}\n~~~\n"
        f"  ```sh\n  {LONG}\n  ```\n"
        f"{LONG}\n"
    )
    assert wrap_check(tmp_path, text) == (1, [14])


def test_a_rule_after_the_first_line_is_not_frontmatter(tmp_path):
    assert wrap_check(tmp_path, f"{LONG}\n---\n{LONG}\n---\n") == (1, [1, 3])
