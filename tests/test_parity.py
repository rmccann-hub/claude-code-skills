import datetime
import runpy
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from skillcheck import parity

FIXTURES = Path(__file__).parent / "fixtures" / "standard"
SAMPLES = sorted((FIXTURES / "samples").glob("*.yaml"))
KEYS = sorted((FIXTURES / "keys").glob("*.yaml"))
BASELINES = sorted((FIXTURES / "baseline").glob("*.yaml"))


def git(cwd: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def small_sample(**changes) -> dict:
    sample = {
        "name": "small",
        "job": "Survey it.",
        "answers": "Nothing has changed.",
        "commits": [
            {
                "message": "First",
                "author": "A Person <a@example.com>",
                "date": "2026-01-01T00:00:00+00:00",
                "files": {"README.md": "# small\n", "old.txt": "gone soon\n"},
            },
            {
                "message": "Second",
                "author": "B Person <b@example.com>",
                "date": datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC),
                "files": {"src/app.py": "print('hi')\n"},
                "delete": ["old.txt"],
            },
            {
                "message": "Third",
                "author": "A Person <a@example.com>",
                "date": "2026-01-03T00:00:00+00:00",
                "delete": ["README.md"],
            },
        ],
        "tags": [{"name": "v1.0.0", "commit": 1}],
    }
    sample.update(changes)
    return sample


def block(body: str) -> str:
    return f"```yaml\n{body}```\n"


def phase(number: int, body: str = "") -> str:
    return block(f"phase: {number}\n{body}notes: none\n")


STATUSES = {
    1: "GAP",
    2: "DRIFT",
    3: "OK",
    4: "GAP",
    5: "GAP",
    6: "N/A",
    7: "BLOCKER",
    8: "OVER",
    9: "GAP",
    10: "DRIFT",
}
TALLY = (
    "tally: {BLOCKER: 1, DRIFT: 2, GAP: 4, OVER: 1, MIRROR: 0, UNVERIFIABLE-HERE: 0, OK: 1, "
    "N/A: 1}\n"
)


def dimensions(statuses: dict[int, str] = STATUSES) -> str:
    entries = "".join(
        f'  - {{n: {n}, name: d{n}, status: {status}, finding: "f", evidence: "e",\n'
        f"     secondary: [{'DRIFT' if n == 4 else ''}], strength: none}}\n"
        for n, status in statuses.items()
    )
    return f"dimensions:\n{entries}"


def report(
    statuses: dict[int, str] = STATUSES,
    tier: str = "T1",
    tally: str = TALLY,
    amendments: str = 'amendments: [{id: A1, change: "add a LICENSE file"}]\n',
) -> str:
    return "\n".join(
        [
            "# Run report\n",
            block(
                "standard: PROJECT-BOOTSTRAP-AND-AUDIT v0.36.0\nmode: audit\n"
                f"tier: {tier} (blast radius B1, audience A1, basis current)\n"
            ),
            "The shim links @AGENTS.md instead of importing it; the cooldown is the default.\n",
            phase(0),
            phase(1, "mode: audit\n"),
            phase(2),
            phase(3, f"tier: {tier}\nblast_radius: B1\naudience: A1\n"),
            phase(4, dimensions(statuses) + tally + SECONDARIES),
            phase(5),
            phase(6, amendments),
        ]
    )


SECONDARIES = 'secondaries: [{n: 6, status: GAP, note: "x"}]\n'

KEY = {
    "stops_at": 6,
    "mode": "audit",
    "tier": ["T1"],
    "blast_radius": ["B1"],
    "audience": ["A1"],
    "planted": [
        {
            "id": "P1",
            "problem": "p",
            "dimensions": [4],
            "rated": ["DRIFT"],
            "words": ["@AGENTS.md"],
        },
        {"id": "P2", "problem": "q", "dimensions": [8], "rated": ["GAP"], "words": ["nowhere"]},
    ],
    "words": ["cooldown", "missing-word"],
    "not_proposed": ["LICENSE", "Dependabot"],
}


def by_name(checks: list[parity.Check]) -> dict[str, bool | None]:
    return {check.name: check.passed for check in checks}


# The fixtures themselves


@pytest.mark.parametrize("path", SAMPLES, ids=lambda path: path.stem)
def test_every_sample_materializes_as_a_clean_repository(path, tmp_path):
    sample = parity.load_yaml(path)
    work = parity.materialize(sample, tmp_path)
    assert work == tmp_path / sample["name"]
    assert git(work, "rev-list", "--count", "HEAD") == str(len(sample["commits"]))
    assert git(work, "status", "--porcelain") == ""
    assert git(work, "tag").split() == [tag["name"] for tag in sample.get("tags") or []]


@pytest.mark.parametrize("path", KEYS, ids=lambda path: path.stem)
def test_every_key_names_its_sample_and_known_words(path):
    key = parity.load_yaml(path)
    assert path.stem == key["sample"]
    assert (FIXTURES / "samples" / f"{key['sample']}.yaml").is_file()
    assert key["stops_at"] in (3, 6)
    ids = [item["id"] for item in key["planted"]]
    assert len(ids) == len(set(ids))
    # A run that stops before Phase 4 rates no dimension, so nothing can be planted for it.
    assert key["stops_at"] >= 4 or not ids
    for item in key["planted"]:
        assert set(item["rated"]) <= set(parity.STATUSES)
        assert set(item["dimensions"]) <= set(parity.DIMENSIONS)
        assert item["words"]


def test_every_sample_has_a_key():
    assert [path.stem for path in SAMPLES] == [path.stem for path in KEYS]


@pytest.mark.parametrize("path", BASELINES, ids=lambda path: path.stem)
def test_every_baseline_names_its_key_and_the_skill_it_measured(path):
    baseline = parity.load_yaml(path)
    assert (FIXTURES / "keys" / path.name).is_file()
    assert baseline["skill"]
    assert baseline["runs"]
    key = parity.load_yaml(FIXTURES / "keys" / path.name)
    for run in baseline["runs"]:
        assert set(run) >= {"label", "mode", "tier", "statuses", "checks"}
        assert set(run["statuses"].values()) <= set(parity.STATUSES)
        assert run["mode"] == key["mode"]


# Building a sample


def test_materialize_builds_history_tags_and_a_remote(tmp_path):
    work = parity.materialize(small_sample(), tmp_path)
    # Dates as Unix time: git 2.55 prints a UTC date as ...Z where 2.43 prints ...+00:00.
    log = git(work, "log", "--format=%an|%ae|%at|%ct|%s").splitlines()
    day = {
        n: int(datetime.datetime(2026, 1, n, tzinfo=datetime.UTC).timestamp()) for n in (1, 2, 3)
    }
    assert log == [
        f"A Person|a@example.com|{day[3]}|{day[3]}|Third",
        f"B Person|b@example.com|{day[2]}|{day[2]}|Second",
        f"A Person|a@example.com|{day[1]}|{day[1]}|First",
    ]
    assert sorted(p.name for p in work.iterdir()) == [".git", "src"]
    first = git(work, "rev-list", "--max-parents=0", "HEAD")
    assert git(work, "rev-list", "-n", "1", "v1.0.0") == first
    assert git(work, "status", "--branch", "--porcelain") == "## main...origin/main"
    assert git(tmp_path / "small.git", "rev-parse", "main") == git(work, "rev-parse", "HEAD")


@pytest.mark.parametrize("existing", ["small", "small.git"])
def test_materialize_refuses_to_build_over_anything(tmp_path, existing):
    (tmp_path / existing).mkdir()
    with pytest.raises(parity.SampleError, match="already exists"):
        parity.materialize(small_sample(), tmp_path)


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (lambda sample: sample.pop("job"), "has no 'job'"),
        (lambda sample: sample.update(commits=[]), "has no commits"),
        (lambda sample: sample["commits"][0].pop("date"), "commit 1 has no 'date'"),
        (lambda sample: sample["commits"][1].update(author="nobody"), "commit 2: author must"),
        (lambda sample: sample.update(tags=[{"name": "v9", "commit": 4}]), "commit 4, which is"),
    ],
)
def test_a_malformed_sample_is_refused(change, message):
    sample = small_sample()
    change(sample)
    with pytest.raises(parity.SampleError, match=message):
        parity.check_sample(sample)


def test_load_yaml_refuses_anything_but_a_mapping(tmp_path):
    path = tmp_path / "list.yaml"
    path.write_text("- one\n- two\n", encoding="utf-8")
    with pytest.raises(parity.SampleError, match="expected a mapping"):
        parity.load_yaml(path)


# Reading a report


def test_extract_reads_every_block():
    results = parity.extract(report())
    assert results.phases == list(range(7))
    assert (results.mode, results.tier, results.blast_radius, results.audience) == (
        "audit",
        "T1",
        "B1",
        "A1",
    )
    assert results.statuses == STATUSES
    assert results.secondaries == {4: ["DRIFT"], 6: ["GAP"]}
    assert results.tally == {
        "BLOCKER": 1,
        "DRIFT": 2,
        "GAP": 4,
        "OVER": 1,
        "MIRROR": 0,
        "UNVERIFIABLE-HERE": 0,
        "OK": 1,
        "N/A": 1,
    }


def test_extract_reads_block_style_entries_and_skips_what_is_not_an_entry():
    body = (
        "dimensions:\n"
        "  - n: 1\n    name: stakes\n    status: GAP\n"
        "  # ... through n: 10\n"
        "  - n: 2\n    status: OK\n"
        "  - n: 2\n    status: DRIFT\n"
        "secondaries:\n  - n: 2\n    note: no status here\n"
    )
    results = parity.extract(phase(4, body))
    assert results.statuses == {1: "GAP", 2: "OK"}
    assert results.secondaries == {}


def test_extract_falls_back_to_the_header_and_normalises_re_check():
    text = block("something: else\n") + block(
        "standard: PROJECT-BOOTSTRAP-AND-AUDIT v0.36.0\nmode: re-check\n"
        "tier: T2 (blast radius B2, audience A1, basis imminent)\n"
    )
    text += block("mode: audit\ntier: T0\n")  # a second header-shaped block is not the header
    results = parity.extract(text)
    assert (results.mode, results.tier, results.blast_radius, results.audience) == (
        "recheck",
        "T2",
        "B2",
        "A1",
    )
    assert results.phases == []


def test_extract_leaves_unknowns_empty():
    results = parity.extract("No blocks at all.")
    assert results == parity.Results()
    assert parity.extract(block("\n")).mode is None


# Grading a report


def test_grade_checks_each_line_of_the_key():
    assert by_name(parity.grade(report(), KEY)) == {
        "stops at Phase 6": True,
        "mode": True,
        "tier": True,
        "blast radius": True,
        "audience": True,
        "ten statuses": True,
        "tally": True,
        "P1 p": True,
        "P2 q": False,
        "mentions cooldown": True,
        "mentions missing-word": False,
        "does not propose LICENSE": False,
        "does not propose Dependabot": True,
    }


def test_grade_a_run_that_stops_at_phase_3():
    text = phase(0) + phase(1, "mode: greenfield\n") + phase(3, "tier: T1\n")
    key = {
        "stops_at": 3,
        "mode": "greenfield",
        "tier": ["T1"],
        "blast_radius": ["B1"],
        "audience": ["A1"],
        "planted": [],
        "not_proposed": ["anything"],
    }
    checks = parity.grade(text, key)
    assert by_name(checks) == {
        "stops at Phase 3": True,
        "mode": True,
        "tier": True,
        "blast radius": None,
        "audience": None,
        "does not propose anything": None,
    }
    assert checks[3].detail == "not found in the report"


def test_grade_names_missing_and_invented_statuses():
    statuses = {**STATUSES, 3: "OK-with-gap"}
    del statuses[10]
    checks = {check.name: check for check in parity.grade(report(statuses=statuses), KEY)}
    assert checks["ten statuses"].passed is False
    assert checks["ten statuses"].detail == (
        "no status for 10; statuses outside the vocabulary: OK-with-gap"
    )
    assert checks["tally"].passed is False
    assert checks["tally"].detail == "sums to 10; does not match the statuses"


def test_grade_reports_a_missing_tally_as_unchecked():
    checks = {check.name: check for check in parity.grade(report(tally=""), KEY)}
    assert checks["tally"].passed is None
    assert checks["tally"].detail == "no tally in the Phase 4 block"


# The baseline


def test_a_run_matching_its_baseline_has_no_differences():
    baseline = {"runs": [parity.record(report(), KEY, "run 1")]}
    assert baseline["runs"][0]["label"] == "run 1"
    assert baseline["runs"][0]["statuses"] == STATUSES
    assert parity.compare(report(), KEY, baseline) == []


def test_compare_names_each_difference_from_the_baseline():
    baseline = {"runs": [parity.record(report(), KEY, "run 1")]}
    changed = report(statuses={**STATUSES, 3: "GAP", 4: "OK"}, tier="T2", tally="")
    assert parity.compare(changed, KEY, baseline) == [
        "tier: T2; the baseline gave T1",
        "dimension 3: GAP; the baseline gave OK",
        "dimension 4: OK; the baseline gave GAP",
        "tier: passed in every baseline run, and not in this one",
        "tally: passed in every baseline run, and not in this one",
    ]


def test_a_value_any_baseline_run_gave_is_not_a_difference():
    runs = [parity.record(report(), KEY, "run 1")]
    runs.append(parity.record(report(statuses={**STATUSES, 3: "GAP"}), KEY, "run 2"))
    assert parity.compare(report(statuses={**STATUSES, 3: "GAP"}), KEY, {"runs": runs}) == []


# The command line


def test_cli_materializes_a_sample(tmp_path, capsys):
    path = tmp_path / "small.yaml"
    path.write_text(yaml.safe_dump(small_sample()), encoding="utf-8")
    assert parity.main(["materialize", str(path), str(tmp_path / "out")]) == 0
    assert capsys.readouterr().out == f"{tmp_path / 'out' / 'small'}\n"


@pytest.fixture
def files(tmp_path):
    paths = {"report": tmp_path / "report.md", "key": tmp_path / "key.yaml"}
    paths["report"].write_text(report(), encoding="utf-8")
    paths["key"].write_text(yaml.safe_dump(KEY), encoding="utf-8")
    return paths


def test_cli_grade_prints_each_check_and_fails_on_any_miss(files, capsys):
    assert parity.main(["grade", str(files["report"]), str(files["key"])]) == 1
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "PASS stops at Phase 6: last phase block: 6"
    assert "FAIL P2 q: words missing; dimensions 8: OVER" in lines


def test_cli_grade_passes_when_every_check_does(files, tmp_path):
    key = {**KEY, "planted": KEY["planted"][:1], "words": ["cooldown"], "not_proposed": []}
    files["key"].write_text(yaml.safe_dump(key), encoding="utf-8")
    assert parity.main(["grade", str(files["report"]), str(files["key"])]) == 0


def test_cli_records_and_compares(files, tmp_path, capsys):
    args = ["record", str(files["report"]), str(files["key"]), "--label", "run 1"]
    assert parity.main(args) == 0
    run = yaml.safe_load(capsys.readouterr().out)
    assert run["label"] == "run 1"
    baseline = tmp_path / "baseline.yaml"
    baseline.write_text(yaml.safe_dump({"skill": "abc123", "runs": [run]}), encoding="utf-8")
    assert parity.main(["compare", str(files["report"]), str(files["key"]), str(baseline)]) == 0
    assert capsys.readouterr().out == "0 difference(s) from the baseline\n"
    files["report"].write_text(report(tier="T2"), encoding="utf-8")
    assert parity.main(["compare", str(files["report"]), str(files["key"]), str(baseline)]) == 1
    assert capsys.readouterr().out.splitlines() == [
        "tier: T2; the baseline gave T1",
        "tier: passed in every baseline run, and not in this one",
        "2 difference(s) from the baseline",
    ]


def test_module_entry_point(files, monkeypatch, capsys):
    # A fresh import, so runpy does not warn that the module was already imported.
    monkeypatch.delitem(sys.modules, "skillcheck.parity")
    monkeypatch.setattr(sys, "argv", ["parity", "grade", str(files["report"]), str(files["key"])])
    with pytest.raises(SystemExit) as exited:
        runpy.run_module("skillcheck.parity", run_name="__main__")
    assert exited.value.code == 1
    assert capsys.readouterr().out.startswith("PASS stops at Phase 6")
