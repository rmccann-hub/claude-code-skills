"""The dependency map is read from the files that decide it, the same way every time."""

import json
import os
import subprocess
from pathlib import Path

from skillcheck import bom
from skillcheck.cli import main

PIN = "1" * 40
FACTS = (
    "# Facts\n\n| ID | Fact | Source | Quote | Checked | Check by |\n|---|---|---|---|---|---|\n"
    '| `one` | A fact | [Docs](https://docs.example.com/a) | "a" | 2026-01-01 | 2026-06-30 |\n'
    '| `two` | A fact | [Docs](https://docs.example.com/b) | "b" | 2026-01-01 | 2026-06-30 |\n'
    "| `tag` | A fact | `git ls-remote --tags https://github.com/example/tool` | `abc` "
    "| 2026-01-01 | 2026-06-30 |\n"
)
UV_LOCK = """\
version = 1
requires-python = ">=3.14"

[[package]]
name = "colorama"
version = "0.4.6"
source = { registry = "https://pypi.org/simple" }

[[package]]
name = "fixture"
version = "0.0.0"
source = { editable = "." }
dependencies = [{ name = "PyYAML" }]

[package.dev-dependencies]
dev = [{ name = "pytest" }, { name = "pytest-cov" }]

[[package]]
name = "pluggy"
version = "1.6.0"
source = { registry = "https://pypi.org/simple" }

[[package]]
name = "pytest"
version = "9.1.1"
source = { registry = "https://pypi.org/simple" }
dependencies = [{ name = "colorama", marker = "sys_platform == 'win32'" }, { name = "pluggy" }]

[[package]]
name = "pytest-cov"
version = "7.1.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [{ name = "pluggy" }, { name = "pytest" }]

[[package]]
name = "PyYAML"
version = "6.0.3"
source = { registry = "https://pypi.org/simple" }
"""
PACKAGE_LOCK = {
    "lockfileVersion": 3,
    "packages": {
        "": {"dependencies": {"lib": "2.0.0"}, "devDependencies": {"tool": "1.0.0"}},
        "node_modules/lib": {
            "version": "2.0.0",
            "resolved": "https://registry.example.com/lib/-/lib-2.0.0.tgz",
            "dependencies": {"@scope/nested": "3.0.0"},
        },
        "node_modules/lib/node_modules/@scope/nested": {
            "version": "3.0.0",
            "resolved": "https://registry.example.com/@scope/nested/-/nested-3.0.0.tgz",
        },
        "node_modules/tool": {
            "version": "1.0.0",
            "resolved": "https://registry.npmjs.org/tool/-/tool-1.0.0.tgz",
            "dev": True,
            "optionalDependencies": {"tool-linux": "1.0.0"},
        },
        "node_modules/tool-linux": {"version": "1.0.0", "dev": True, "optional": True},
    },
}
CI = f"""\
name: CI
on: push
env:
  TOOL_VERSION: v1.2.3
jobs:
  build:
    runs-on: ubuntu-latest
    env:
      LOCAL: x
    steps:
      - uses: actions/checkout@{PIN} # v4.0.0
      - uses: astral-sh/setup-uv@{PIN} # v1.0.0
        with:
          version: "0.9.0"
      - uses: actions/setup-node@{PIN}
        with:
          node-version: "24"
      - uses: actions/setup-go@v5
      - uses: ./local-action
      - run: |
          go install "github.com/example/tool/v8@${{TOOL_VERSION}}"
          go install example.com/other@$MISSING
  other:
    runs-on: [self-hosted, linux]
    steps:
      - run: echo nothing to install
"""


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


DEPENDABOT = "version: 2\nupdates:\n  - package-ecosystem: uv\n  - package-ecosystem: npm\n"


def fixture(
    root: Path,
    full: bool = True,
    python_version: str | None = "3.14",
    dependabot: str | None = DEPENDABOT,
) -> Path:
    """A throwaway repository. The full one has every kind of file the map reads."""
    files = {
        ".claude-plugin/marketplace.json": json.dumps(
            {
                "name": "fixture-skills",
                "plugins": [
                    {
                        "name": "alpha",
                        "version": "1.2.3",
                        "license": "MIT",
                        "repository": "https://github.com/example/fixture" if full else "",
                        "skills": ["./skills/alpha-skill", "./skills/beta-skill"],
                    },
                    {"name": "gamma", "skills": ["./skills/gamma-skill"]},
                ],
            }
        ),
        "skills/alpha-skill/SKILL.md": "---\nname: alpha-skill\nlicense: MIT\n"
        'metadata:\n  standard-version: "1.0.0"\n---\nBody.\n',
        "skills/alpha-skill/references/facts.md": FACTS,
        "skills/beta-skill/SKILL.md": '---\nname: beta-skill\nmetadata:\n  reviewed: "2026-01-01"\n'
        "---\nBody.\n",
        "skills/gamma-skill/SKILL.md": "---\nname: gamma-skill\n---\nBody.\n",
        "pyproject.toml": '[project]\nlicense = "Apache-2.0"\nrequires-python = ">=3.14"\n'
        + ('[build-system]\nrequires = ["uv_build>=0.12.19,<0.13", "hatchling"]\n' if full else ""),
        "src/fixture.py": "",
        "hooks/pre-push": "#!/bin/sh\nexit 0\n",
        "LICENSE": "License text.\n",
        "notes.txt": "",
    }
    if python_version:
        files[".python-version"] = f"{python_version}\n"
    if dependabot is not None:
        files[".github/dependabot.yml"] = dependabot
    if full:
        files |= {
            "uv.lock": UV_LOCK,
            "package-lock.json": json.dumps(PACKAGE_LOCK),
            ".github/workflows/ci.yml": CI,
            ".github/workflows/empty.yml": "",
        }
    for path, text in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text, encoding="utf-8")
    # Git lists a link as a file even when it points at a directory.
    os.symlink("skills", root / "link")
    git(root, "init", "-q")
    git(root, "add", "-A")
    return root


def test_the_map_reads_each_kind_of_dependency_from_its_file(tmp_path):
    inventory = bom.collect(fixture(tmp_path))
    assert (inventory.name, inventory.version, inventory.license) == (
        "fixture-skills",
        "1.2.3",
        "Apache-2.0",
    )
    assert inventory.languages == {
        "Markdown": 4,
        "JSON": 2,
        "TOML": 2,
        "YAML": 3,
        "Python": 1,
        "Shell": 1,
    }
    pypi = {p.name: p for p in inventory.packages if p.ecosystem == "pypi"}
    assert {name: (p.version, p.dev) for name, p in pypi.items()} == {
        "colorama": ("0.4.6", True),
        "pluggy": ("1.6.0", True),
        "pytest": ("9.1.1", True),
        "pytest-cov": ("7.1.0", True),
        "PyYAML": ("6.0.3", False),
    }
    assert pypi["colorama"].only_when == "sys_platform == 'win32'"
    assert pypi["pluggy"].only_when == ""
    assert pypi["PyYAML"].purl == "pkg:pypi/pyyaml@6.0.3"
    npm = {p.name: p for p in inventory.packages if p.ecosystem == "npm"}
    assert {name: (p.dev, p.optional) for name, p in npm.items()} == {
        "@scope/nested": (False, False),
        "lib": (False, False),
        "tool": (True, False),
        "tool-linux": (True, True),
    }
    assert npm["@scope/nested"].purl == "pkg:npm/%40scope/nested@3.0.0"
    assert inventory.direct == {"pypi": ["PyYAML", "pytest", "pytest-cov"], "npm": ["lib", "tool"]}
    tools = {(t.name, t.version): t for t in inventory.tools}
    assert sorted(tools) == [
        ("GitHub-hosted runner", "linux"),
        ("GitHub-hosted runner", "self-hosted"),
        ("GitHub-hosted runner", "ubuntu-latest"),
        ("Go", "the action's default"),
        ("Node.js", "24"),
        ("Python", "3.14"),
        ("hatchling", "any"),
        ("other", "$MISSING"),
        ("tool", "v1.2.3"),
        ("uv", "0.9.0"),
        ("uv_build", ">=0.12.19,<0.13"),
    ]
    assert tools[("Python", "3.14")].note == "`pyproject.toml` requires >=3.14"
    assert tools[("tool", "v1.2.3")].purl == "pkg:golang/github.com/example/tool/v8@v1.2.3"
    assert [(a.name, a.ref, a.tag) for a in inventory.actions] == [
        ("actions/checkout", PIN, "v4.0.0"),
        ("actions/setup-go", "v5", ""),
        ("actions/setup-node", PIN, ""),
        ("astral-sh/setup-uv", PIN, "v1.0.0"),
    ]
    assert [s.key for s in inventory.services] == [
        "github",
        "github-actions",
        "dependabot",
        "pypi",
        "npm",
        "go-modules",
        "claude-code-plugins",
        "claude-ai",
    ]
    services = {s.key: s for s in inventory.services}
    assert services["npm"].endpoints == (
        "https://registry.example.com",
        "https://registry.npmjs.org",
    )
    assert services["dependabot"].description.endswith("dependencies: npm, uv.")
    skills = {s.name: s for p in inventory.plugins for s in p.skills}
    assert skills["alpha-skill"].detail == "standard v1.0.0"
    assert skills["alpha-skill"].sources == (("docs.example.com", 2), ("github.com", 1))
    assert skills["beta-skill"].detail == "reviewed 2026-01-01"
    assert (skills["gamma-skill"].detail, skills["gamma-skill"].license) == ("", "")


def test_the_cyclonedx_file_is_the_same_every_time_and_records_what_it_read(tmp_path):
    root = fixture(tmp_path)
    text = bom.render(root)[bom.BOM]
    assert text == bom.render(root)[bom.BOM]
    data = json.loads(text)
    assert list(data)[:5] == ["$schema", "bomFormat", "specVersion", "serialNumber", "version"]
    assert (data["bomFormat"], data["specVersion"]) == ("CycloneDX", "1.7")
    assert data["serialNumber"].startswith("urn:uuid:")
    components = {c["bom-ref"]: c for c in data["components"]}
    assert components["pkg:npm/tool@1.0.0"]["properties"] == [
        {"name": "cdx:npm:package:development", "value": "true"}
    ]
    assert {"name": "claude-code-skills:optional", "value": "true"} in components[
        "pkg:npm/tool-linux@1.0.0"
    ]["properties"]
    assert components["pkg:pypi/colorama@0.4.6"]["scope"] == "excluded"
    assert components["pkg:pypi/pyyaml@6.0.3"]["scope"] == "required"
    assert "properties" not in components["pkg:pypi/pyyaml@6.0.3"]
    pinned = components[f"pkg:github/actions/checkout@{PIN}"]
    assert pinned["version"] == "v4.0.0"
    assert {"name": "claude-code-skills:pinned-commit", "value": PIN} in pinned["properties"]
    unpinned = components["pkg:github/actions/setup-go@v5"]
    assert unpinned["version"] == "v5"
    assert [p["name"] for p in unpinned["properties"]] == ["claude-code-skills:used-in"]
    assert "purl" not in components["tool:Python@3.14"]
    gamma = components["plugin:gamma"]
    assert "licenses" not in gamma
    assert "description" not in gamma["components"][0]
    graph = {d["ref"]: d["dependsOn"] for d in data["dependencies"]}
    assert graph["project:fixture@0.0.0"] == [
        "pkg:pypi/pytest-cov@7.1.0",
        "pkg:pypi/pytest@9.1.1",
        "pkg:pypi/pyyaml@6.0.3",
    ]
    assert "pkg:npm/lib@2.0.0" in graph["fixture-skills"]
    services = {s["bom-ref"]: s for s in data["services"]}
    assert "endpoints" not in services["service:dependabot"]
    assert services["service:dependabot"]["externalReferences"][0]["type"] == "documentation"
    assert "externalReferences" not in services["service:github"]


def test_the_page_draws_the_tree_and_says_what_it_could_not_find(tmp_path):
    page = bom.render(fixture(tmp_path))[bom.MAP]
    assert "fixture 0.0.0 (this repository's checks)\n├── PyYAML 6.0.3\n" in page
    assert "│   ├── colorama 0.4.6 (dev; only when sys_platform == 'win32')\n" in page
    # A package shown once with its dependencies isn't drawn again, but a leaf is.
    assert "    └── pytest 9.1.1 (dev) (listed above)\n" in page
    assert page.count("pluggy 1.6.0 (dev)") == 2
    assert "└── tool 1.0.0 (dev)\n    └── tool-linux 1.0.0 (dev; optional)\n" in page
    assert "| `actions/setup-go` | v5 | not pinned to a commit |" in page
    assert "documented at https://docs.github.com/en/code-security/dependabot" in page
    assert "| `beta-skill` | no `references/facts.md` | — |" in page


def test_a_repository_with_no_lockfiles_or_workflows_still_gets_a_map(tmp_path):
    root = fixture(tmp_path, full=False, python_version=None, dependabot="")
    inventory = bom.collect(root)
    assert inventory.project is None
    assert (inventory.packages, inventory.actions, inventory.direct) == (
        [],
        [],
        {"pypi": [], "npm": []},
    )
    assert [(t.name, t.version, t.where) for t in inventory.tools] == [
        ("Python", ">=3.14", ("pyproject.toml",))
    ]
    assert [s.key for s in inventory.services] == ["dependabot", "claude-code-plugins", "claude-ai"]
    assert inventory.services[0].description == "Opens pull requests that update dependencies."
    page = bom.render(root)[bom.MAP]
    assert "## Python packages" not in page
    assert "## Node packages" not in page


def test_a_python_version_file_needs_no_requirement_beside_it(tmp_path):
    root = fixture(tmp_path, full=False, dependabot=None)
    assert [s.key for s in bom.collect(root).services] == ["claude-code-plugins", "claude-ai"]
    (root / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
    inventory = bom.collect(root)
    assert [(t.name, t.version, t.note) for t in inventory.tools] == [("Python", "3.14", "")]
    assert inventory.license == ""
    (root / "pyproject.toml").unlink()
    (root / ".python-version").unlink()
    assert bom.collect(root).tools == []


def test_the_check_names_each_file_that_no_longer_matches(tmp_path):
    root = fixture(tmp_path)
    assert bom.stale(root) == [bom.BOM, bom.MAP]
    assert bom.write(root) == [bom.BOM, bom.MAP]
    assert bom.stale(root) == []
    (root / bom.MAP).write_text("edited by hand\n", encoding="utf-8")
    assert bom.stale(root) == [bom.MAP]


def test_the_command_line_writes_and_checks_the_map(tmp_path, capsys):
    root = fixture(tmp_path)
    assert main([str(root), "--bom-check"]) == 1
    assert "bom.json: bom: out of date; run `uv run skillcheck --bom`" in capsys.readouterr().out
    assert main([str(root), "--bom"]) == 0
    out = capsys.readouterr().out
    assert "wrote bom.json\nwrote docs/dependencies.md\n" in out
    assert out.endswith("skillcheck: dependency map written, 24 dependencies, 8 services\n")
    assert main([str(root), "--bom-check"]) == 0
    assert capsys.readouterr().out.endswith("8 services, 0 file(s) out of date\n")
