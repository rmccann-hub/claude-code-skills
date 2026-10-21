"""Each dependency is measured against its newest release, past a wait (outdated.py)."""

import io
import json
import subprocess
import urllib.error
from datetime import date
from pathlib import Path

from skillcheck import outdated
from skillcheck.cli import main

TODAY = date(2026, 10, 19)
PIN = "1" * 40
UV_LOCK = """\
version = 1

[[package]]
name = "fixture"
version = "0.0.0"
source = { editable = "." }
dependencies = [{ name = "pyyaml" }]

[package.dev-dependencies]
dev = [{ name = "ruff" }]

[[package]]
name = "pyyaml"
version = "6.0.3"
source = { registry = "https://pypi.org/simple" }

[[package]]
name = "ruff"
version = "0.17.0"
source = { registry = "https://pypi.org/simple" }
"""
PACKAGE_LOCK = {
    "lockfileVersion": 3,
    "packages": {
        "": {"devDependencies": {"tool": "1.0.0"}},
        "node_modules/tool": {"version": "1.0.0", "dev": True},
        "node_modules/tool-linux-x64": {"version": "1.0.0", "dev": True, "optional": True},
    },
}
CI = f"""\
name: CI
env:
  LINTER_VERSION: v1.2.0
jobs:
  test:
    runs-on: ubuntu-24.04
    strategy:
      matrix:
        python-version: ["3.14", "3.15"]
    steps:
      - uses: actions/checkout@{PIN} # v7.0.1
      - uses: actions/upload-artifact@{PIN} # v7.0.1
      - uses: actions/attest-build-provenance@{PIN} # v4
      - uses: example/unpinned@main
      - uses: example/no-release/sub@{PIN} # v1.0.0
      - uses: example/broken@{PIN} # v2.0.0
      - uses: ./local-action
      - uses: actions/setup-python@{PIN} # v7.0.0
        with:
          python-version: ${{{{ matrix.python-version }}}}
      - uses: actions/setup-python@{PIN} # v7.0.0
      - uses: actions/setup-node@{PIN} # v7.1.0
        with:
          node-version: "22"
      - uses: actions/setup-go@{PIN} # v7.0.0
        with:
          go-version: "1.27"
      - uses: astral-sh/setup-uv@{PIN} # v10.3.0
        with:
          version: "0.13.1"
      - run: go install "github.com/example/linter/v1/cmd/linter@${{LINTER_VERSION}}"
      - run: go install golang.org/x/tools/cmd/stringer@v0.30.0
"""
PYPROJECT = """\
[project]
requires-python = ">=3.14"
dependencies = ["pyyaml>=6.0.3", "PySide6[addons]>=6.11.1,<6.12 ; python_version >= '3.11'"]

[project.optional-dependencies]
docs = ["sphinx"]

[dependency-groups]
dev = ["ruff>=0.17.0", { include-group = "docs" }, ""]

[build-system]
requires = ["uv_build>=0.13.0,<0.14"]
"""


def release(version: str, published: str) -> dict:
    return {
        "info": {"version": version},
        "releases": {version: [{"upload_time_iso_8601": published}]},
    }


def github(tag: str, published: str = "2026-10-01T00:00:00Z") -> dict:
    return {"tag_name": tag, "published_at": published}


REGISTRY: dict[str, object] = {
    "https://pypi.org/pypi/pyyaml/json": release("6.0.3", "2025-09-25T00:00:00Z"),
    "https://pypi.org/pypi/ruff/json": release("0.17.1", "2026-10-15T00:00:00Z"),
    "https://pypi.org/pypi/PySide6/json": release("6.12.0", "2026-10-08T00:00:00Z"),
    "https://pypi.org/pypi/uv_build/json": release("0.13.2", "2026-10-19T00:00:00Z"),
    "https://pypi.org/pypi/uv/json": {"info": {"version": "0.13.2"}, "releases": {}},
    "https://registry.npmjs.org/tool": {
        "dist-tags": {"latest": "1.0.2"},
        "time": {"1.0.2": "2026-10-18T10:00:00Z"},
    },
    "https://api.github.com/repos/actions/checkout/releases/latest": github("v7.0.1"),
    "https://api.github.com/repos/actions/upload-artifact/releases/latest": github("v7.0.2"),
    "https://api.github.com/repos/actions/attest-build-provenance/releases/latest": github(
        "v4.2.2"
    ),
    "https://api.github.com/repos/actions/setup-python/releases/latest": github("v7.0.0"),
    "https://api.github.com/repos/actions/setup-node/releases/latest": github("v7.1.0"),
    "https://api.github.com/repos/actions/setup-go/releases/latest": github("v7.0.0"),
    "https://api.github.com/repos/astral-sh/setup-uv/releases/latest": github("v10.3.0"),
    "https://api.github.com/repos/example/unpinned/releases/latest": github("v3.0.0"),
    "https://api.github.com/repos/example/no-release/releases/latest": urllib.error.HTTPError(
        "url", 404, "Not Found", {}, None
    ),
    "https://api.github.com/repos/example/broken/releases/latest": urllib.error.HTTPError(
        "url", 404, "Not Found", {}, None
    ),
    "https://api.github.com/repos/example/linter/releases/latest": github("v1.3.0"),
    "https://endoflife.date/api/python.json": [
        {"cycle": "3.15", "releaseDate": "2026-10-09"},
        {"cycle": "3.14", "releaseDate": "2025-10-07"},
    ],
    "https://endoflife.date/api/go.json": [{"cycle": "1.27", "releaseDate": "2026-08-12"}],
    "https://endoflife.date/api/nodejs.json": [
        {"cycle": "26", "releaseDate": "2026-04-21", "lts": "2099-10-20"},
        {"cycle": "25", "releaseDate": "2025-10-15", "lts": False},
        {"cycle": "24", "releaseDate": "2025-05-06", "lts": "2025-10-28"},
    ],
}


def fake_fetch(registry: dict[str, object]):
    def fetch(url: str) -> object:
        answer = registry.get(url, OSError("no such page"))
        if isinstance(answer, Exception):
            raise answer
        return answer

    return fetch


def tags(monkeypatch, listing: dict[str, str]) -> None:
    """Serve `git ls-remote --tags` from a table, keyed by repository."""

    def run(command, **_):
        repo = command[-1].removeprefix("https://github.com/").removesuffix(".git")
        if repo not in listing:
            raise subprocess.CalledProcessError(128, command)
        return subprocess.CompletedProcess(command, 0, stdout=listing[repo])

    monkeypatch.setattr(outdated.subprocess, "run", run)


def repository(root: Path, *, python_version: str | None = "3.14") -> Path:
    files = {
        "uv.lock": UV_LOCK,
        "package-lock.json": json.dumps(PACKAGE_LOCK),
        ".github/workflows/ci.yml": CI,
        "pyproject.toml": PYPROJECT,
    }
    if python_version:
        files[".python-version"] = f"{python_version}\n"
    for path, text in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text, encoding="utf-8")
    return root


def states(results) -> dict[tuple[str, str, str], tuple[str, str]]:
    return {(r.kind, r.name, r.used): (r.state, r.note) for r in results}


def test_each_dependency_gets_its_state(tmp_path, monkeypatch):
    tags(monkeypatch, {"example/no-release": "abc\trefs/tags/nightly\n"})
    found = states(outdated.scan(repository(tmp_path), fake_fetch(REGISTRY), TODAY))
    assert found == {
        ("pypi", "pyyaml", "6.0.3"): ("current", ""),
        ("pypi", "ruff", "0.17.0"): ("behind", ""),
        ("npm", "tool", "1.0.0"): ("waiting", ""),
        ("action", "actions/checkout", "v7.0.1"): ("current", ""),
        ("action", "actions/upload-artifact", "v7.0.1"): ("behind", ""),
        ("action", "actions/attest-build-provenance", "v4"): (
            "unread",
            "names v4, not one release of it",
        ),
        ("action", "actions/setup-python", "v7.0.0"): ("current", ""),
        ("action", "actions/setup-node", "v7.1.0"): ("current", ""),
        ("action", "actions/setup-go", "v7.0.0"): ("current", ""),
        ("action", "astral-sh/setup-uv", "v10.3.0"): ("current", ""),
        ("action", "example/unpinned", "main"): ("unread", "the pin names no version"),
        ("action", "example/no-release/sub", "v1.0.0"): (
            "unread",
            "it publishes no release and no version tag",
        ),
        ("action", "example/broken", "v2.0.0"): (
            "unread",
            "the registry couldn't be read (CalledProcessError)",
        ),
        ("runtime", "Python", "${{ matrix.python-version }}"): (
            "unread",
            "set by an expression; read its values",
        ),
        ("runtime", "Python", "the action's default"): ("unread", "no version is named"),
        ("runtime", "Python", "3.14"): ("behind", ".python-version"),
        ("runtime", "Node.js", "22"): ("behind", ".github/workflows/ci.yml"),
        ("runtime", "Go", "1.27"): ("current", ".github/workflows/ci.yml"),
        ("tool", "uv", "0.13.1"): ("behind", ".github/workflows/ci.yml"),
        ("tool", "linter", "v1.2.0"): ("behind", ".github/workflows/ci.yml"),
        ("range", "uv_build", ">=0.13.0,<0.14"): ("current", "build backend"),
        ("range", "pyyaml", ">=6.0.3"): ("current", "pyproject.toml"),
        ("range", "PySide6", ">=6.11.1,<6.12"): ("behind", "pyproject.toml"),
        ("range", "ruff", ">=0.17.0"): ("current", "pyproject.toml"),
    }


def test_the_report_names_what_needs_action_and_fails_on_it(tmp_path, monkeypatch):
    tags(monkeypatch, {})
    results = outdated.scan(repository(tmp_path), fake_fetch(REGISTRY), TODAY)
    lines, summary, code = outdated.report(results)
    assert "behind   pypi ruff 0.17.0 -> 0.17.1, out since 2026-10-15" in lines
    assert "waiting  npm tool 1.0.0 -> 1.0.2, out since 2026-10-18" in lines
    assert "behind   tool uv 0.13.1 -> 0.13.2 (.github/workflows/ci.yml)" in lines
    assert "unread   action example/unpinned main: the pin names no version" in lines
    assert not any("pyyaml 6.0.3" in line for line in lines)
    assert summary == (
        "skillcheck: 24 dependencies checked, 7 behind, 1 waiting out the 3-day wait, 6 unread"
    )
    assert code == 1


def test_pinned_requirements_and_moving_tags_are_read(tmp_path, monkeypatch):
    tags(monkeypatch, {})
    files = {
        "requirements.lock": (
            "# autogenerated by uv pip compile\n"
            "fastapi==0.141.1 \\\n    --hash=sha256:ab\n"
            "uvicorn[standard]==0.40.0 ; sys_platform != 'win32'\n"
            "-e .\n"
        ),
        "requirements-dev.txt": "ruff==0.17.1\n",
        "requirements.in": "ignored==1.0\n",
        ".github/workflows/ci.yml": (
            "jobs:\n  test:\n    steps:\n"
            "      - uses: actions/checkout@v7\n\n"
            "      # **The comment after a step is not its version\n"
            f"      - uses: actions/setup-go@{PIN}\n"
            "      # v9 is not its version either\n"
            "      - uses: actions/setup-python@v6\n"
        ),
    }
    for path, text in files.items():
        (tmp_path / path).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / path).write_text(text, encoding="utf-8")
    registry = {
        **REGISTRY,
        "https://pypi.org/pypi/fastapi/json": release("0.156.4", "2026-10-01T00:00:00Z"),
        "https://pypi.org/pypi/uvicorn/json": release("0.40.0", "2026-09-01T00:00:00Z"),
    }
    found = states(outdated.scan(tmp_path, fake_fetch(registry), TODAY))
    assert found == {
        ("pypi", "fastapi", "0.141.1"): ("behind", "requirements.lock"),
        ("pypi", "uvicorn", "0.40.0"): ("current", "requirements.lock"),
        ("pypi", "ruff", "0.17.1"): ("current", "requirements-dev.txt"),
        ("action", "actions/checkout", "v7"): ("current", outdated.MOVING),
        ("action", "actions/setup-go", "(none)"): ("unread", "the pin names no version"),
        ("action", "actions/setup-python", "v6"): ("behind", outdated.MOVING),
        ("runtime", "Go", "the action's default"): ("unread", "no version is named"),
        ("runtime", "Python", "the action's default"): ("unread", "no version is named"),
    }


def test_a_release_inside_the_wait_does_not_fail_the_run():
    waiting = outdated.Result("waiting", "npm", "tool", "1.0.0", "1.0.2", TODAY)
    current = outdated.Result("current", "npm", "other", "2.0.0", "2.0.0")
    assert outdated.report([waiting, current])[2] == 0
    assert outdated.report([])[1].startswith("skillcheck: 0 dependencies checked")


def test_a_range_is_read_as_its_operators_say():
    allows = outdated._allows
    assert allows(">=1.2,<2", "1.9.9") and not allows(">=1.2,<2", "2.0")
    assert allows("~=1.4.2", "1.4.9") and not allows("~=1.4.2", "1.5.0")
    assert allows("==6.*", "6.12.0") and not allows("==6.*", "7.0")
    assert allows("!=1.5", "1.6") and not allows("!=1.5", "1.5.0")
    assert allows("<=2.0", "2.0") and allows(">1", "1.1") and not allows(">1", "1")
    assert allows("", "9.9")


def test_a_runtime_line_is_compared_with_the_newest_line():
    assert outdated._runtime_current("3.15", "3.15")
    assert outdated._runtime_current("3.15.2", "3.15")
    assert not outdated._runtime_current("3.14", "3.15")
    assert outdated._runtime_current(">=3.11", "3.15")


def test_requires_python_stands_in_when_no_version_is_pinned(tmp_path, monkeypatch):
    tags(monkeypatch, {})
    found = states(
        outdated.scan(repository(tmp_path, python_version=None), fake_fetch(REGISTRY), TODAY)
    )
    assert found[("runtime", "Python", ">=3.14")] == ("current", "pyproject.toml")


def test_a_release_found_only_by_its_tag_counts_as_past_the_wait(monkeypatch):
    tags(
        monkeypatch, {"example/tool": "a\trefs/tags/v1.2.0\nb\trefs/tags/v1.10.0\nc\trefs/tags/x\n"}
    )
    newest = outdated._github(fake_fetch({}), "example/tool")
    assert newest == outdated.Release("v1.10.0", None)
    judged = outdated._judge("action", "example/tool", "v1.2.0", newest, "", TODAY)
    assert judged.state == "behind"
    assert judged.line() == "behind   action example/tool v1.2.0 -> v1.10.0"


def test_a_registry_that_can_not_be_read_is_never_current(tmp_path):
    assert outdated._reason(urllib.error.HTTPError("u", 503, "x", {}, None)) == (
        "the registry answered 503"
    )
    assert outdated._reason(KeyError("info")) == "the registry couldn't be read (KeyError)"
    (tmp_path / "uv.lock").write_text(UV_LOCK, encoding="utf-8")
    results = outdated.scan(tmp_path, fake_fetch({}), TODAY)
    assert {r.state for r in results} == {"unread"}


def test_nodejs_counts_only_a_line_that_has_reached_long_term_support():
    cycles = [
        {"cycle": "27", "lts": False},
        {"cycle": "26", "lts": True, "releaseDate": "2026-04-21"},
    ]
    fetch = fake_fetch({"https://endoflife.date/api/nodejs.json": cycles})
    assert outdated._cycle(fetch, "nodejs") == outdated.Release("26", date(2026, 4, 21))


def test_fetch_sends_a_token_only_to_github(monkeypatch):
    sent = []

    def urlopen(request, timeout):
        sent.append((request.full_url, request.get_header("Authorization")))
        return io.BytesIO(b'{"ok": true}')

    monkeypatch.setattr(outdated.urllib.request, "urlopen", urlopen)
    monkeypatch.setenv("GITHUB_TOKEN", "t0ken")
    assert outdated.fetch_json("https://api.github.com/repos/a/b/releases/latest") == {"ok": True}
    outdated.fetch_json("https://pypi.org/pypi/a/json")
    monkeypatch.delenv("GITHUB_TOKEN")
    outdated.fetch_json("https://api.github.com/repos/a/b/releases/latest")
    assert sent == [
        ("https://api.github.com/repos/a/b/releases/latest", "Bearer t0ken"),
        ("https://pypi.org/pypi/a/json", None),
        ("https://api.github.com/repos/a/b/releases/latest", None),
    ]


def test_the_command_reports_and_exits_by_what_it_found(tmp_path, capsys, monkeypatch):
    assert main([str(tmp_path), "--outdated"]) == 0
    assert capsys.readouterr().out == (
        "skillcheck: 0 dependencies checked, 0 behind, 0 waiting out the 3-day wait, 0 unread\n"
    )
    (tmp_path / "uv.lock").write_text(UV_LOCK, encoding="utf-8")
    monkeypatch.setattr(outdated.urllib.request, "urlopen", _refuse)
    assert main([str(tmp_path), "--outdated"]) == 1
    out = capsys.readouterr().out
    assert "unread   pypi ruff 0.17.0: the registry couldn't be read (OSError)" in out


def _refuse(request, timeout):
    raise OSError("no network in tests")
