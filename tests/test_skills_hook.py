"""The cloud hook installs a release's skills, replaces only its own, and never stops a session."""

import io
import json
import runpy
import urllib.request
import zipfile
from pathlib import Path

import pytest

from skillcheck import skills_hook
from skillcheck.skills_hook import LEDGER, MANIFEST, install, main


def archive(version: str, skills: dict[str, dict[str, str]], manifest: dict | None = None) -> bytes:
    """A release's skills.zip: each skill's files, and the manifest naming them."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as out:
        listed = {"version": version, "skills": list(skills)} if manifest is None else manifest
        out.writestr(MANIFEST, json.dumps(listed))
        for name, files in skills.items():
            for path, text in files.items():
                entry = zipfile.ZipInfo(f"{name}/{path}")
                entry.external_attr = (0o755 if path.startswith("scripts/") else 0o644) << 16
                out.writestr(entry, text)
    return buffer.getvalue()


def skill(body: str = "Body.") -> dict[str, str]:
    return {"SKILL.md": body, "scripts/run.sh": "#!/bin/sh\n"}


def ledger(skills: Path) -> dict:
    return json.loads((skills / LEDGER).read_text(encoding="utf-8"))


def test_a_release_installs_with_its_ledger_and_scripts_stay_runnable(tmp_path):
    skills = tmp_path / ".claude/skills"
    install(archive("1.0.0", {"alpha": skill(), "beta": skill()}), skills)
    assert sorted(p.name for p in skills.iterdir()) == [LEDGER, "alpha", "beta"]
    assert ledger(skills) == {"version": "1.0.0", "skills": ["alpha", "beta"]}
    assert (skills / "alpha/scripts/run.sh").stat().st_mode & 0o111
    assert not (skills / "alpha/SKILL.md").stat().st_mode & 0o111
    # Nothing is left beside the skills folder from unpacking.
    assert sorted(p.name for p in skills.parent.iterdir()) == ["skills"]


def test_the_same_release_again_changes_nothing(tmp_path):
    skills = tmp_path / "skills"
    install(archive("1.0.0", {"alpha": skill()}), skills)
    (skills / "alpha/SKILL.md").write_text("Edited.", encoding="utf-8")
    install(archive("1.0.0", {"alpha": skill()}), skills)
    assert (skills / "alpha/SKILL.md").read_text(encoding="utf-8") == "Edited."
    # A skill of its own that went missing brings the release back.
    (skills / "alpha/SKILL.md").unlink()
    (skills / "alpha/scripts/run.sh").unlink()
    (skills / "alpha/scripts").rmdir()
    (skills / "alpha").rmdir()
    install(archive("1.0.0", {"alpha": skill()}), skills)
    assert (skills / "alpha/SKILL.md").read_text(encoding="utf-8") == "Body."


def test_a_newer_release_replaces_its_own_removes_the_retired_and_spares_others(tmp_path, capsys):
    skills = tmp_path / "skills"
    install(archive("1.0.0", {"alpha": skill(), "retired": skill()}), skills)
    (skills / "mine").mkdir()
    (skills / "mine/SKILL.md").write_text("Someone else's.", encoding="utf-8")
    install(archive("1.1.0", {"alpha": skill("New."), "mine": skill()}), skills)
    assert (skills / "alpha/SKILL.md").read_text(encoding="utf-8") == "New."
    assert not (skills / "retired").exists()
    assert (skills / "mine/SKILL.md").read_text(encoding="utf-8") == "Someone else's."
    assert ledger(skills) == {"version": "1.1.0", "skills": ["alpha"]}
    assert "left " in capsys.readouterr().err


@pytest.mark.parametrize(
    ("manifest", "files", "message"),
    [
        ({"skills": ["alpha"]}, {}, "needs a version and a list of skills"),
        ({"version": "1.0.0", "skills": []}, {}, "needs a version and a list of skills"),
        ({"version": "1.0.0", "skills": "alpha"}, {}, "needs a version and a list of skills"),
        ({"version": "1.0.0", "skills": ["Alpha"]}, {}, "names 'Alpha', which isn't a skill"),
        ({"version": "1.0.0", "skills": [1]}, {}, "names 1, which isn't a skill"),
        ({"version": "1.0.0", "skills": ["alpha"]}, {"other": skill()}, "holds 'other/SKILL.md'"),
        ({"version": "1.0.0", "skills": ["alpha"]}, {"alpha": {"../x": "y"}}, "holds 'alpha/../x'"),
        ({"version": "1.0.0", "skills": ["alpha"]}, {"alpha": {"a\\b": "y"}}, "holds 'alpha/a"),
        ({"version": "1.0.0", "skills": ["alpha"]}, {"alpha": {"x.md": "y"}}, "no alpha/SKILL.md"),
    ],
)
def test_an_archive_that_isnt_a_release_installs_nothing(tmp_path, manifest, files, message):
    with pytest.raises(ValueError, match=message):
        install(archive("", files, manifest), tmp_path / "skills")
    assert not (tmp_path / "skills").exists()


@pytest.mark.parametrize("char", ["\u202e", "\u200b", "\U000e0041"])
def test_a_skill_carrying_a_hidden_character_installs_nothing(tmp_path, char):
    files = {"SKILL.md": f"Looks{char} harmless.", "assets/logo.png": "\x89PNG"}
    with pytest.raises(ValueError, match=r"'alpha/SKILL.md' holds U\+"):
        install(archive("1.0.0", {"alpha": files}), tmp_path / "skills")
    assert not (tmp_path / "skills").exists()


def test_a_binary_file_is_not_read_as_text(tmp_path):
    buffer = io.BytesIO(archive("1.0.0", {"alpha": skill()}))
    with zipfile.ZipFile(buffer, "a") as out:
        out.writestr("alpha/assets/image.png", b"\xff\xfe\x00\xe2\x80\x8b")
    install(buffer.getvalue(), tmp_path / "skills")
    assert (tmp_path / "skills/alpha/assets/image.png").is_file()


def test_a_failed_download_keeps_the_installed_skills(tmp_path, capsys):
    bundle = tmp_path / "skills.zip"
    bundle.write_bytes(archive("1.0.0", {"alpha": skill()}))
    assert main(bundle.as_uri(), tmp_path) == 0
    assert (tmp_path / ".claude/skills/alpha/SKILL.md").is_file()
    assert capsys.readouterr().out == ""
    assert main((tmp_path / "missing.zip").as_uri(), tmp_path) == 0
    assert "kept the skills already installed" in capsys.readouterr().err
    assert (tmp_path / ".claude/skills/alpha/SKILL.md").is_file()


def test_a_copy_still_on_the_account_is_named_for_the_user_to_delete(tmp_path, capsys):
    bundle = tmp_path / "skills.zip"
    bundle.write_bytes(archive("1.0.0", {"alpha": skill(), "beta": skill()}))
    synced = tmp_path / ".claude/skills/synced/account/beta"
    synced.mkdir(parents=True)
    (synced / "SKILL.md").write_text("Old.", encoding="utf-8")
    for _ in range(2):  # whether it installs or finds the release already there
        assert main(bundle.as_uri(), tmp_path) == 0
        said = capsys.readouterr().out
        assert said.startswith("claude-code-skills: the claude.ai account still has its own copy")
        assert " of beta, which " in said


def test_run_as_a_script_it_installs_into_the_home_folder(tmp_path, monkeypatch):
    bundle = tmp_path / "skills.zip"
    bundle.write_bytes(archive("1.0.0", {"alpha": skill()}))
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setattr(urllib.request, "urlopen", lambda url, timeout: bundle.open("rb"))
    with pytest.raises(SystemExit) as stopped:
        runpy.run_path(skills_hook.__file__, run_name="__main__")
    assert stopped.value.code == 0
    assert (tmp_path / ".claude/skills/alpha/SKILL.md").is_file()
