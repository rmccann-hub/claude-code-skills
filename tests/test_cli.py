import runpy
import sys

import pytest
from conftest import DEFAULT_DESCRIPTION

from skillcheck.cli import main


def test_clean_repository_exits_zero_and_prints_summary(repo, capsys):
    repo.skill("example-skill")
    repo.catalog(repo.plugin("example", "./skills/example-skill"))
    assert main([str(repo.root)]) == 0
    assert capsys.readouterr().out == (
        f"skillcheck: 1 skill(s), {len(DEFAULT_DESCRIPTION)} description characters, "
        "1 catalog plugin(s), no roadmap, no standard, 0 finding(s)\n"
    )


def test_findings_exit_one_with_one_line_each(repo, capsys):
    repo.skill("example-skill", "name: other-name\ndescription: d\n")
    repo.catalog(repo.plugin("example", "./skills/example-skill"))
    assert main([str(repo.root)]) == 1
    lines = capsys.readouterr().out.splitlines()
    assert lines == [
        "skills/example-skill/SKILL.md: name: name 'other-name' does not match directory "
        "'example-skill'",
        "skillcheck: 1 skill(s), 1 description characters, 1 catalog plugin(s), no roadmap, "
        "no standard, 1 finding(s)",
    ]


def test_missing_root_fails_rather_than_passing(tmp_path, capsys):
    with pytest.raises(SystemExit) as exited:
        main([str(tmp_path / "does-not-exist")])
    assert exited.value.code == 2
    assert "is not a directory" in capsys.readouterr().err


def test_module_entry_point(repo, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["skillcheck", str(repo.root)])
    with pytest.raises(SystemExit) as exited:
        runpy.run_module("skillcheck", run_name="__main__")
    assert exited.value.code == 0
    assert capsys.readouterr().out == (
        "skillcheck: 0 skill(s), 0 description characters, no catalog, no roadmap, "
        "no standard, 0 finding(s)\n"
    )
