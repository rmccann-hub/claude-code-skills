"""A release publishes what it says, from the commit being released, or nothing at all."""

import base64
import hashlib
import io
import json
import os
import shutil
import subprocess
import zipfile
from pathlib import Path

import pytest

from skillcheck import bom, release
from skillcheck.cli import main

STANDARD = """\
---
name: project-bootstrap-and-audit
description: "A synthetic standard for tests."
metadata:
  version: "1.0.0"
---

**License.** Free to use. No warranty of any kind.

---

# How to read this file

Read it in ranges.

---

# Validating a change to this standard

Not for runs.

# Provenance

Where it came from.
"""
STANDARD_PATH = (
    "skills/project-bootstrap-and-audit/references/PROJECT-BOOTSTRAP-AND-AUDIT-v1.0.0.md"
)
RULESET_PATH = "skills/tool/assets/rulesets/tags.json"
RULESET = '{"name": "Tags", "target": "tag", "rules": [{"type": "deletion"}]}\n'
VALE_PATH = "skills/tool/assets/vale/Plain"
VALE_CONFIG = "[*.md]\nBasedOnStyles = Plain\n"
VALE_RULE = "extends: existence\nmessage: \"Cut '%s'.\"\ntokens: [very]\n"
CHANGELOG = """\
# Changelog

## [Unreleased]

## [1.0.0] - 2026-10-05

### Added

- A thing.

## [0.9.0] - 2026-09-01

- Old.
"""


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


def plugin(name: str, skill: str, repository: str = "https://github.com/example/fixture") -> dict:
    return {
        "name": name,
        "version": "1.0.0",
        "repository": repository,
        "skills": [f"./skills/{skill}"],
    }


def fixture(root: Path) -> Path:
    """A repository whose catalog, changelog and map all agree on version 1.0.0."""
    files = {
        ".claude-plugin/marketplace.json": json.dumps(
            {
                "name": "fixture-skills",
                "plugins": [
                    plugin("alpha", "project-bootstrap-and-audit"),
                    plugin("beta", "tool"),
                ],
            }
        ),
        "skills/project-bootstrap-and-audit/SKILL.md": "---\nname: project-bootstrap-and-audit\n"
        'metadata:\n  standard-version: "1.0.0"\n---\nBody.\n',
        STANDARD_PATH: STANDARD,
        "skills/tool/SKILL.md": "---\nname: tool\n---\nBody.\n",
        "skills/tool/hooks/run": "#!/bin/sh\nexit 0\n",
        RULESET_PATH: RULESET,
        f"{VALE_PATH}/.vale.ini": VALE_CONFIG,
        f"{VALE_PATH}/styles/Plain/Words.yml": VALE_RULE,
        "CHANGELOG.md": CHANGELOG,
        "pyproject.toml": "[project]\n",
    }
    for path, text in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text, encoding="utf-8")
    (root / "skills/tool/hooks/run").chmod(0o755)
    git(root, "init", "-q")
    git(root, "add", "-A")
    # The map counts tracked files, its own among them, so it settles on the second writing.
    bom.write(root)
    git(root, "add", "-A")
    bom.write(root)
    return root


def test_a_release_is_built_from_the_commit(tmp_path):
    root = fixture(tmp_path / "repo")
    assert release.problems(root, "1.0.0") == []
    out = tmp_path / "out"
    assert release.build(root, "1.0.0", out) == [
        "KICKSTART.md",
        "Plain.zip",
        "bom.json",
        "cloud-setup.sh",
        "notes.md",
        "project-bootstrap-and-audit.zip",
        "ruleset-tags.json",
        "skills.zip",
        "tool.zip",
    ]
    kick = (out / "KICKSTART.md").read_text(encoding="utf-8")
    assert kick.startswith(
        "RUN-FILE-FOR: the repository this session works in · JOB: chosen by what it holds · "
        "FROM: example/fixture, release 1.0.0\n\n"
    )
    assert hashlib.sha256(STANDARD.encode()).hexdigest() in kick
    assert "release 1.0.0 of\n> example/fixture." in kick
    assert "RELEASE_VERSION" not in kick and "STANDARD_SHA256" not in kick
    assert (
        'extract: "Validating a change to this standard and Provenance left out; the full' in kick
    )
    assert "No warranty of any kind.\n\n> **About this file.**" in kick
    assert "\n---\n\n# How to read this file\n" in kick
    assert "# Validating a change" not in kick and "# Provenance" not in kick
    assert kick.endswith(f"\n\n{release.END}\n")
    notes = (out / "notes.md").read_text(encoding="utf-8")
    assert (
        "/plugin marketplace add example/fixture\n/plugin install alpha@fixture-skills\n" in notes
    )
    assert "/plugin install beta@fixture-skills\n```" in notes
    assert "| `tool.zip` | The `tool` skill, packaged to upload to claude.ai |" in notes
    assert "choose Import a ruleset.\n\n| File |" in notes
    assert "add the lines in `cloud-setup.sh` to the end of the\nenvironment's setup" in notes
    assert "| `skills.zip` | Every skill in one file" in notes
    assert '| `ruleset-tags.json` | A tag ruleset, "Tags", to import |' in notes
    assert (
        "| `Plain.zip` | The Plain Vale style, which a repository's `.vale.ini` names by URL |"
        in notes
    )
    assert notes.endswith("### Added\n\n- A thing.\n")
    assert (out / "bom.json").read_bytes() == (root / "bom.json").read_bytes()
    assert (out / "ruleset-tags.json").read_text(encoding="utf-8") == RULESET
    archive = zipfile.ZipFile(io.BytesIO((out / "tool.zip").read_bytes()))
    modes = {info.filename: info.external_attr >> 16 for info in archive.infolist()}
    assert modes == {
        "tool/SKILL.md": 0o644,
        "tool/assets/rulesets/tags.json": 0o644,
        "tool/assets/vale/Plain/.vale.ini": 0o644,
        "tool/assets/vale/Plain/styles/Plain/Words.yml": 0o644,
        "tool/hooks/run": 0o755,
    }
    # Vale wants one folder, named for the package, at the top of its ZIP.
    style = zipfile.ZipFile(io.BytesIO((out / "Plain.zip").read_bytes()))
    assert style.namelist() == ["Plain/.vale.ini", "Plain/styles/Plain/Words.yml"]
    assert style.read("Plain/.vale.ini").decode("utf-8") == VALE_CONFIG
    # One file holds every skill, with the manifest the cloud hook checks.
    bundle = zipfile.ZipFile(io.BytesIO((out / "skills.zip").read_bytes()))
    assert json.loads(bundle.read("release.json")) == {
        "version": "1.0.0",
        "skills": ["project-bootstrap-and-audit", "tool"],
    }
    assert "tool/hooks/run" in bundle.namelist()
    assert bundle.read(STANDARD_PATH.removeprefix("skills/")).decode("utf-8") == STANDARD
    # The same commit packs the same bytes.
    assert release.bundle(root, "1.0.0") == release.bundle(root, "1.0.0")
    assert release.packages(root) == release.packages(root)
    assert release.vale_packages(root) == release.vale_packages(root)


def test_nothing_is_built_until_the_catalog_the_changelog_and_the_map_agree(tmp_path):
    root = fixture(tmp_path)
    assert release.problems(root, "2.0.0") == [
        "the catalog's `alpha` plugin says 1.0.0, not 2.0.0",
        "the catalog's `beta` plugin says 1.0.0, not 2.0.0",
        "CHANGELOG.md has no section for 2.0.0",
    ]
    (root / bom.MAP).write_text("edited by hand\n", encoding="utf-8")
    assert release.problems(root, "1.0.0") == [
        "docs/dependencies.md is out of date: run `uv run skillcheck --bom`"
    ]


def test_a_ruleset_needs_a_name_no_other_skill_uses(tmp_path):
    root = fixture(tmp_path)
    other = root / "skills/project-bootstrap-and-audit/assets/rulesets/tags.json"
    other.parent.mkdir(parents=True)
    other.write_text(RULESET, encoding="utf-8")
    git(root, "add", "-A")
    with pytest.raises(release.ReleaseError, match="two skills ship a ruleset called tags.json"):
        release.rulesets(root)


def test_the_page_says_how_to_import_a_ruleset_only_when_it_carries_one(tmp_path):
    root = fixture(tmp_path)
    # The fixture stages its files without committing them, so git rm needs -f.
    git(root, "rm", "-q", "-f", RULESET_PATH)
    page = release.notes(root, "1.0.0")
    assert "ruleset" not in page


def test_a_vale_package_needs_a_name_no_other_skill_uses(tmp_path):
    root = fixture(tmp_path)
    other = root / "skills/project-bootstrap-and-audit/assets/vale/Plain/.vale.ini"
    other.parent.mkdir(parents=True)
    other.write_text(VALE_CONFIG, encoding="utf-8")
    git(root, "add", "-A")
    with pytest.raises(release.ReleaseError, match="two skills ship a Vale package called Plain"):
        release.vale_packages(root)


def test_a_vale_file_outside_a_package_folder_stops_the_release(tmp_path):
    root = fixture(tmp_path)
    loose = root / "skills/tool/assets/vale/.vale.ini"
    loose.write_text(VALE_CONFIG, encoding="utf-8")
    git(root, "add", "-A")
    with pytest.raises(release.ReleaseError, match="isn't inside a Vale package's folder"):
        release.vale_packages(root)


def test_a_vale_package_named_like_a_skill_stops_the_release(tmp_path):
    root = fixture(tmp_path)
    clash = root / "skills/tool/assets/vale/tool/.vale.ini"
    clash.parent.mkdir(parents=True)
    clash.write_text(VALE_CONFIG, encoding="utf-8")
    git(root, "add", "-A")
    with pytest.raises(release.ReleaseError, match="two of the release's files would be called"):
        release.build(root, "1.0.0", tmp_path / "out")
    assert not (tmp_path / "out").exists()


def test_the_page_lists_a_vale_style_only_when_it_carries_one(tmp_path):
    root = fixture(tmp_path)
    git(root, "rm", "-q", "-r", "-f", VALE_PATH)
    assert "Vale" not in release.notes(root, "1.0.0")
    assert release.vale_packages(root) == {}


def test_the_changelog_section_ends_at_the_next_version_or_the_file(tmp_path):
    root = fixture(tmp_path)
    assert release._section(root, "1.0.0") == "### Added\n\n- A thing."
    assert release._section(root, "0.9.0") == "- Old."
    with pytest.raises(release.ReleaseError, match="no section for 3.0.0"):
        release.notes(root, "3.0.0")


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (lambda root: (root / STANDARD_PATH).unlink(), "one copy of the standard, found 0"),
        (
            lambda root: (root / STANDARD_PATH).write_text(
                STANDARD.replace("No warranty of any kind.\n\n", ""), encoding="utf-8"
            ),
            "doesn't hold 'No warranty of any kind.",
        ),
        (
            lambda root: (root / STANDARD_PATH).write_text(
                STANDARD.replace("Read it", "Read\u200bit"), encoding="utf-8"
            ),
            "would hold U\\+200B",
        ),
    ],
)
def test_the_kickstart_file_needs_one_whole_standard(tmp_path, change, message):
    root = fixture(tmp_path)
    change(root)
    with pytest.raises(release.ReleaseError, match=message):
        release.kickstart(root, "1.0.0")


@pytest.mark.parametrize("repositories", [["", ""], ["https://a.example/x", "https://b.example/y"]])
def test_the_catalog_must_name_one_repository(tmp_path, repositories):
    root = fixture(tmp_path)
    catalog = {
        "name": "fixture-skills",
        "plugins": [
            plugin("alpha", "project-bootstrap-and-audit", repositories[0]),
            plugin("beta", "tool", repositories[1]),
        ],
    }
    (root / ".claude-plugin/marketplace.json").write_text(json.dumps(catalog), encoding="utf-8")
    with pytest.raises(release.ReleaseError, match="one repository"):
        release.kickstart(root, "1.0.0")


def test_the_command_line_builds_a_release_or_says_why_not(tmp_path, capsys):
    root = fixture(tmp_path / "repo")
    out = tmp_path / "out"
    assert main([str(root), "--release-assets", "1.0.0", str(out)]) == 0
    printed = capsys.readouterr().out
    assert f"wrote {out / 'KICKSTART.md'}\n" in printed
    assert printed.endswith("skillcheck: release 1.0.0, 0 problem(s)\n")
    assert main([str(root), "--release-assets", "2.0.0", str(out)]) == 1
    printed = capsys.readouterr().out
    assert "release: CHANGELOG.md has no section for 2.0.0\n" in printed
    assert printed.endswith("skillcheck: release 2.0.0, 3 problem(s)\n")
    # A standard that can't be packed stops the build, though the map still matches.
    (root / STANDARD_PATH).write_text(STANDARD.replace("Read it", "Read\u200bit"), encoding="utf-8")
    assert main([str(root), "--release-assets", "1.0.0", str(tmp_path / "again")]) == 1
    assert "release: the kickstart file would hold U+200B\n" in capsys.readouterr().out


def test_the_cloud_setup_lines_install_the_hook_once_and_keep_other_settings(tmp_path):
    root = fixture(tmp_path / "repo")
    out = tmp_path / "out"
    release.build(root, "1.0.0", out)
    script = (out / "cloud-setup.sh").read_text(encoding="utf-8")
    assert script.startswith("# From example/fixture, release 1.0.0.")
    assert "REPOSITORY" not in script and "HOOK_SOURCE" not in script
    url = "https://github.com/example/fixture/releases/latest/download/skills.zip"
    assert script.count(url) == 1
    # Run against the built file, as the hook would fetch it from the release, with the
    # attestation the release workflow adds beside it, unsigned: the PATH below has no gh.
    script = script.replace(url, (out / "skills.zip").as_uri())
    workflow = {"repository": "https://github.com/example/fixture"}
    workflow["path"] = ".github/workflows/release.yml"
    digest = hashlib.sha256((out / "skills.zip").read_bytes()).hexdigest()
    statement = {
        "subject": [{"name": "skills.zip", "digest": {"sha256": digest}}],
        "predicate": {"buildDefinition": {"externalParameters": {"workflow": workflow}}},
    }
    payload = base64.b64encode(json.dumps(statement).encode()).decode()
    envelope = json.dumps({"dsseEnvelope": {"payload": payload}})
    (out / "attestation.sigstore.json").write_text(envelope, encoding="utf-8")
    tools = tmp_path / "bin"
    tools.mkdir()
    for tool in ("cat", "mkdir", "python3"):
        (tools / tool).symlink_to(shutil.which(tool))
    home = tmp_path / "home"
    settings = home / ".claude/settings.json"
    settings.parent.mkdir(parents=True)
    other = {"matcher": "startup", "hooks": [{"type": "command", "command": "true"}]}
    settings.write_text(
        json.dumps({"model": "kept", "hooks": {"SessionStart": [other]}}), encoding="utf-8"
    )
    env = {"HOME": str(home), "PATH": str(tools)}
    said = [
        subprocess.run(
            [shutil.which("bash"), "-c", script], env=env, check=True, capture_output=True
        ).stderr
        for _ in range(2)
    ]
    # The first run installs, saying what it checked; the second finds the release there.
    assert said[0].decode().endswith("isn't checked without gh\n")
    assert said[1] == b""
    written = json.loads(settings.read_text(encoding="utf-8"))
    command = 'python3 "$HOME/.claude/hooks/claude-code-skills.py"'
    assert written == {
        "model": "kept",
        "hooks": {
            "SessionStart": [
                other,
                {
                    "matcher": "startup|resume",
                    "hooks": [{"type": "command", "command": command, "timeout": 60}],
                },
            ]
        },
        "syncClaudeAiPlugins": False,
    }
    skills = home / ".claude/skills"
    assert sorted(p.name for p in skills.iterdir()) == [
        ".claude-code-skills.json",
        "project-bootstrap-and-audit",
        "tool",
    ]
    assert os.access(skills / "tool/hooks/run", os.X_OK)
