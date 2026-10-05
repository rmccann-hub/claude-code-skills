"""The dependency map: what this repository runs on, as CycloneDX JSON and as Markdown.

Both are built from the files that decide them: the lockfiles, the workflows, `.python-version`,
`pyproject.toml`, the plugin catalog, the skills' frontmatter and their dated facts. Neither is
written by hand, and `skillcheck --bom-check` names whichever no longer matches what those files
say. Pull requests don't run that check: a Dependabot update changes a lockfile but can't rebuild
the map, so the weekly freshness run and the release workflow run it instead.
"""

import json
import re
import subprocess
import tomllib
import uuid
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, urlsplit

import yaml

from skillcheck.core import facts, frontmatter

BOM = "bom.json"
MAP = "docs/dependencies.md"
SPEC_VERSION = "1.7"
SCHEMA = f"http://cyclonedx.org/schema/bom-{SPEC_VERSION}.schema.json"
# CycloneDX asks that a property name not in its own taxonomy carry a namespace of its own.
PROPERTY = "claude-code-skills:"

# What sets each tool's version: a setup action's input, keyed by the action.
SETUP = {
    "actions/setup-go": ("Go", "go-version", "platform"),
    "actions/setup-node": ("Node.js", "node-version", "platform"),
    "actions/setup-python": ("Python", "python-version", "platform"),
    "astral-sh/setup-uv": ("uv", "version", "application"),
}
USES = re.compile(r"^\s*(?:-\s+)?uses:\s*([^\s#]+)(?:\s*#\s*(\S+))?", re.MULTILINE)
GO_INSTALL = re.compile(r"go install\s+\"?([\w.\-/]+)@([^\s\"]+)\"?")
VARIABLE = re.compile(r"\$\{?(\w+)\}?")
SHA = re.compile(r"[0-9a-f]{40}")

LANGUAGES = {
    ".json": "JSON",
    ".md": "Markdown",
    ".py": "Python",
    ".sh": "Shell",
    ".toml": "TOML",
    ".yaml": "YAML",
    ".yml": "YAML",
}
NAMED = {"uv.lock": "TOML"}


@dataclass(frozen=True)
class Package:
    ecosystem: str
    name: str
    version: str
    dev: bool
    optional: bool
    requires: tuple[str, ...]
    only_when: str = ""

    @property
    def purl(self) -> str:
        if self.ecosystem == "npm":
            return f"pkg:npm/{quote(self.name, safe='/')}@{self.version}"
        return f"pkg:pypi/{_normalise(self.name)}@{self.version}"


@dataclass(frozen=True)
class Tool:
    name: str
    version: str
    kind: str
    where: tuple[str, ...]
    purl: str = ""
    note: str = ""

    @property
    def ref(self) -> str:
        return self.purl or f"tool:{self.name}@{self.version}"


@dataclass(frozen=True)
class Action:
    name: str
    ref: str
    tag: str
    workflows: tuple[str, ...]

    @property
    def purl(self) -> str:
        return f"pkg:github/{self.name}@{self.ref}"


@dataclass(frozen=True)
class Service:
    key: str
    name: str
    provider: str
    endpoints: tuple[str, ...]
    description: str
    docs: str = ""


@dataclass(frozen=True)
class Skill:
    name: str
    license: str
    detail: str
    sources: tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class Plugin:
    name: str
    version: str
    license: str
    skills: tuple[Skill, ...]


@dataclass
class Inventory:
    name: str
    version: str
    repository: str
    license: str
    languages: dict[str, int]
    plugins: list[Plugin]
    project: Package | None
    packages: list[Package]
    direct: dict[str, list[str]]
    tools: list[Tool]
    actions: list[Action]
    services: list[Service]


def collect(root: Path) -> Inventory:
    """Read everything the map records from the files that decide it."""
    catalog = json.loads((root / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    pyproject = _toml(root / "pyproject.toml")
    project, python = _python(root)
    node, node_direct = _node(root)
    workflows = _workflows(root)
    plugins = _plugins(root, catalog)
    repositories = tuple(
        sorted({p["repository"] for p in catalog["plugins"] if p.get("repository")})
    )
    return Inventory(
        name=catalog["name"],
        version=", ".join(sorted({p.version for p in plugins if p.version})),
        repository=", ".join(repositories),
        license=pyproject.get("project", {}).get("license", ""),
        languages=_languages(root),
        plugins=plugins,
        project=project,
        packages=python + node,
        direct={
            "pypi": list(project.requires) if project else [],
            "npm": node_direct,
        },
        tools=_runtimes(root, pyproject) + _ci_tools(workflows),
        actions=_actions(workflows),
        services=_services(root, repositories, python, node, workflows),
    )


def render(root: Path) -> dict[str, str]:
    """The map's two files, by path, as they should read."""
    inventory = collect(root)
    return {BOM: to_cyclonedx(inventory), MAP: to_markdown(inventory)}


def write(root: Path) -> list[str]:
    """Write both files, and return their paths."""
    files = render(root)
    for path, text in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text, encoding="utf-8")
    return sorted(files)


def stale(root: Path) -> list[str]:
    """The paths whose file is missing or no longer matches what the repository says."""
    out = []
    for path, text in sorted(render(root).items()):
        target = root / path
        if not target.is_file() or target.read_text(encoding="utf-8") != text:
            out.append(path)
    return out


def _toml(path: Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def _normalise(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _python(root: Path) -> tuple[Package | None, list[Package]]:
    entries = _toml(root / "uv.lock").get("package", [])
    if not entries:
        return None, []
    [own] = [e for e in entries if "editable" in e["source"] or "virtual" in e["source"]]
    runtime = [d["name"] for d in own.get("dependencies", [])]
    dev = [d["name"] for group in own.get("dev-dependencies", {}).values() for d in group]
    by_name = {e["name"]: e for e in entries if e is not own}
    edges = {name: e.get("dependencies", []) for name, e in by_name.items()}
    in_runtime = _reach(runtime, edges)
    reached = _reach(runtime + dev, edges)
    markers: dict[str, set[str]] = defaultdict(set)
    unmarked: set[str] = set(runtime + dev)
    for name in reached:
        for dep in edges[name]:
            if "marker" in dep:
                markers[dep["name"]].add(dep["marker"])
            else:
                unmarked.add(dep["name"])
    packages = [
        Package(
            "pypi",
            name,
            by_name[name]["version"],
            dev=name not in in_runtime,
            optional=False,
            requires=tuple(sorted(d["name"] for d in edges[name])),
            only_when="" if name in unmarked else " or ".join(sorted(markers[name])),
        )
        for name in sorted(reached)
    ]
    project = Package(
        "pypi",
        own["name"],
        own["version"],
        dev=False,
        optional=False,
        requires=tuple(sorted(set(runtime + dev))),
    )
    return project, packages


def _reach(start: list[str], edges: dict[str, list[dict]]) -> set[str]:
    seen: set[str] = set()
    todo = list(start)
    while todo:
        name = todo.pop()
        if name not in seen:
            seen.add(name)
            todo += [dep["name"] for dep in edges[name]]
    return seen


def _node(root: Path) -> tuple[list[Package], list[str]]:
    path = root / "package-lock.json"
    if not path.is_file():
        return [], []
    entries = json.loads(path.read_text(encoding="utf-8"))["packages"]
    top = entries.get("", {})
    direct = sorted(
        {
            *top.get("dependencies", {}),
            *top.get("devDependencies", {}),
            *top.get("optionalDependencies", {}),
        }
    )
    packages = {
        (key.rsplit("node_modules/", 1)[-1], entry["version"]): Package(
            "npm",
            key.rsplit("node_modules/", 1)[-1],
            entry["version"],
            dev=bool(entry.get("dev")),
            optional=bool(entry.get("optional")),
            requires=tuple(
                sorted({*entry.get("dependencies", {}), *entry.get("optionalDependencies", {})})
            ),
        )
        for key, entry in entries.items()
        if key
    }
    return [packages[key] for key in sorted(packages)], direct


def _workflows(root: Path) -> list[tuple[str, str, dict]]:
    return [
        (path.relative_to(root).as_posix(), text, yaml.safe_load(text) or {})
        for path in sorted((root / ".github/workflows").glob("*.y*ml"))
        for text in [path.read_text(encoding="utf-8")]
    ]


def _actions(workflows: list[tuple[str, str, dict]]) -> list[Action]:
    used: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    for where, text, _ in workflows:
        for target, tag in USES.findall(text):
            # A local action is part of this repository, not something it depends on.
            if not target.startswith("./"):
                name, _, ref = target.partition("@")
                used[(name, ref, tag)].add(where)
    return [Action(n, r, t, tuple(sorted(w))) for (n, r, t), w in sorted(used.items())]


def _ci_tools(workflows: list[tuple[str, str, dict]]) -> list[Tool]:
    found: dict[tuple[str, str, str, str], set[str]] = defaultdict(set)
    for where, _, data in workflows:
        env = data.get("env") or {}
        for job in (data.get("jobs") or {}).values():
            scope = {**env, **(job.get("env") or {})}
            labels = job.get("runs-on", [])
            for label in [labels] if isinstance(labels, str) else labels:
                found[("GitHub-hosted runner", label, "operating-system", "")].add(where)
            for step in job.get("steps", []):
                action = step.get("uses", "").partition("@")[0]
                if action in SETUP:
                    name, key, kind = SETUP[action]
                    version = str((step.get("with") or {}).get(key, "the action's default"))
                    found[(name, version, kind, "")].add(where)
                for module, version in GO_INSTALL.findall(step.get("run", "")):
                    version = _expand(version, scope)
                    tool = next(
                        p for p in reversed(module.split("/")) if not re.fullmatch(r"v\d+", p)
                    )
                    purl = f"pkg:golang/{module}@{version}"
                    found[(tool, version, "application", purl)].add(where)
    return [
        Tool(name, version, kind, tuple(sorted(where)), purl)
        for (name, version, kind, purl), where in sorted(found.items())
    ]


def _expand(text: str, scope: dict) -> str:
    """Put each variable's value in place, and leave one with no value as written."""
    return VARIABLE.sub(lambda m: str(scope.get(m[1], m[0])), text)


def _runtimes(root: Path, pyproject: dict) -> list[Tool]:
    tools = []
    requires = pyproject.get("project", {}).get("requires-python", "")
    pinned = root / ".python-version"
    if pinned.is_file():
        note = f"`pyproject.toml` requires {requires}" if requires else ""
        version = pinned.read_text(encoding="utf-8").strip()
        tools.append(Tool("Python", version, "platform", (".python-version",), note=note))
    elif requires:
        tools.append(Tool("Python", requires, "platform", ("pyproject.toml",)))
    for requirement in pyproject.get("build-system", {}).get("requires", []):
        name, version = re.match(r"([\w.-]+)\s*(.*)", requirement).groups()
        tools.append(
            Tool(name, version or "any", "library", ("pyproject.toml",), note="build backend")
        )
    return tools


def _languages(root: Path) -> dict[str, int]:
    listed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"], capture_output=True, text=True, check=True
    ).stdout
    count: Counter[str] = Counter()
    for name in filter(None, listed.split("\0")):
        path = root / name
        language = NAMED.get(path.name) or LANGUAGES.get(path.suffix)
        if language is None and not path.suffix and path.is_file():
            first = path.read_text(encoding="utf-8", errors="replace").partition("\n")[0]
            language = "Shell" if re.match(r"#!.*\b(ba|da|z)?sh\b", first) else None
        if language:
            count[language] += 1
    return dict(sorted(count.items(), key=lambda item: (-item[1], item[0])))


def _plugins(root: Path, catalog: dict) -> list[Plugin]:
    sources: dict[str, Counter[str]] = defaultdict(Counter)
    for fact in facts.collect(root):
        skill = Path(fact.path).parts[1]
        for host in sorted({_host(source) for source in fact.sources}):
            sources[skill][host] += 1
    plugins = []
    for entry in catalog["plugins"]:
        skills = []
        for path in entry.get("skills", []):
            name = Path(path).name
            data, _ = frontmatter.parse(
                (root / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            )
            meta = data.get("metadata") or {}
            detail = (
                f"standard v{meta['standard-version']}"
                if "standard-version" in meta
                else f"reviewed {meta['reviewed']}"
                if "reviewed" in meta
                else ""
            )
            counted = sorted(sources[name].items(), key=lambda item: (-item[1], item[0]))
            skills.append(Skill(name, data.get("license", ""), detail, tuple(counted)))
        plugins.append(
            Plugin(entry["name"], entry.get("version", ""), entry.get("license", ""), tuple(skills))
        )
    return plugins


def _host(source: str) -> str:
    # Every source names an https address, as a link or inside the command that reads it.
    return urlsplit(re.search(r"https://\S+", source)[0]).netloc


def _services(
    root: Path,
    repositories: tuple[str, ...],
    python: list[Package],
    node: list[Package],
    workflows: list[tuple[str, str, dict]],
) -> list[Service]:
    services = []
    if repositories:
        services.append(
            Service(
                "github",
                "GitHub",
                "GitHub",
                repositories,
                "Hosts the repository, its pull requests, its rulesets and its releases.",
            )
        )
    if workflows and repositories:
        names = ", ".join(Path(where).stem for where, _, _ in workflows)
        services.append(
            Service(
                "github-actions",
                "GitHub Actions",
                "GitHub",
                tuple(f"{repository}/actions" for repository in repositories),
                f"Runs the workflows: {names}.",
            )
        )
    dependabot = root / ".github/dependabot.yml"
    if dependabot.is_file():
        updates = (yaml.safe_load(dependabot.read_text(encoding="utf-8")) or {}).get("updates", [])
        ecosystems = ", ".join(sorted({u["package-ecosystem"] for u in updates}))
        services.append(
            Service(
                "dependabot",
                "Dependabot",
                "GitHub",
                (),
                "Opens pull requests that update dependencies"
                + (f": {ecosystems}." if ecosystems else "."),
                docs="https://docs.github.com/en/code-security/dependabot",
            )
        )
    if python:
        services.append(
            Service(
                "pypi",
                "PyPI",
                "Python Software Foundation",
                tuple(sorted({e["source"]["registry"] for e in _registry_entries(root)})),
                "Serves the Python packages in `uv.lock`.",
            )
        )
    if node:
        hosts = _node_registries(root)
        services.append(
            Service(
                "npm",
                "npm registry",
                "GitHub",
                hosts,
                "Serves the packages in `package-lock.json`.",
            )
        )
    if any(GO_INSTALL.search(step.get("run", "")) for step in _steps(workflows)):
        services.append(
            Service(
                "go-modules",
                "Go module proxy and checksum database",
                "Google",
                ("https://proxy.golang.org", "https://sum.golang.org"),
                "Serves the Go modules CI installs, and the checksums `go install` verifies.",
            )
        )
    services.append(
        Service(
            "claude-code-plugins",
            "Claude Code plugin marketplace",
            "Anthropic",
            (),
            "Claude Code installs the plugins from `.claude-plugin/marketplace.json`.",
            docs="https://code.claude.com/docs/en/plugin-marketplaces",
        )
    )
    services.append(
        Service(
            "claude-ai",
            "claude.ai",
            "Anthropic",
            ("https://claude.ai",),
            "The owner uploads the skills to their account, which is how they reach cloud "
            "sessions.",
        )
    )
    return services


def _registry_entries(root: Path) -> list[dict]:
    return [e for e in _toml(root / "uv.lock").get("package", []) if "registry" in e["source"]]


def _node_registries(root: Path) -> tuple[str, ...]:
    entries = json.loads((root / "package-lock.json").read_text(encoding="utf-8"))["packages"]
    urls = [urlsplit(e["resolved"]) for e in entries.values() if e.get("resolved")]
    return tuple(sorted({f"{url.scheme}://{url.netloc}" for url in urls}))


def _steps(workflows: list[tuple[str, str, dict]]) -> list[dict]:
    return [
        step
        for _, _, data in workflows
        for job in (data.get("jobs") or {}).values()
        for step in job.get("steps", [])
    ]


def to_cyclonedx(inventory: Inventory) -> str:
    """The map as a CycloneDX BOM, in JSON, with nothing in it that changes between runs."""
    root_ref = inventory.name
    components = []
    dependencies: dict[str, set[str]] = {root_ref: set()}
    for plugin in inventory.plugins:
        ref = f"plugin:{plugin.name}" + (f"@{plugin.version}" if plugin.version else "")
        dependencies[root_ref].add(ref)
        components.append(
            {
                "type": "application",
                "bom-ref": ref,
                "name": plugin.name,
                "version": plugin.version,
                "description": "A Claude Code plugin from this repository's catalog.",
                **_licence(plugin.license),
                "components": [_skill(skill) for skill in plugin.skills],
            }
        )
    if inventory.project:
        project = inventory.project
        ref = f"project:{project.name}@{project.version}"
        dependencies[root_ref].add(ref)
        dependencies[ref] = {_ref(inventory, "pypi", name) for name in project.requires}
        components.append(
            {
                "type": "application",
                "bom-ref": ref,
                "name": project.name,
                "version": project.version,
                "description": "This repository's checks, run from source and never published.",
            }
        )
    for package in inventory.packages:
        dependencies[package.purl] = {
            _ref(inventory, package.ecosystem, name) for name in package.requires
        }
        properties = []
        if package.ecosystem == "npm" and package.dev:
            properties.append({"name": "cdx:npm:package:development", "value": "true"})
        if package.optional:
            properties.append({"name": f"{PROPERTY}optional", "value": "true"})
        if package.only_when:
            properties.append({"name": f"{PROPERTY}only-when", "value": package.only_when})
        components.append(
            {
                "type": "library",
                "bom-ref": package.purl,
                "name": package.name,
                "version": package.version,
                "scope": "excluded" if package.dev else "required",
                "purl": package.purl,
                **({"properties": properties} if properties else {}),
            }
        )
    for name in inventory.direct["npm"]:
        dependencies[root_ref].add(_ref(inventory, "npm", name))
    for tool in inventory.tools:
        dependencies[root_ref].add(tool.ref)
        properties = [{"name": f"{PROPERTY}set-in", "value": ", ".join(tool.where)}]
        if tool.note:
            properties.append({"name": f"{PROPERTY}note", "value": tool.note})
        components.append(
            {
                "type": tool.kind,
                "bom-ref": tool.ref,
                "name": tool.name,
                "version": tool.version,
                **({"purl": tool.purl} if tool.purl else {}),
                "properties": properties,
            }
        )
    for action in inventory.actions:
        dependencies[root_ref].add(action.purl)
        properties = [{"name": f"{PROPERTY}used-in", "value": ", ".join(action.workflows)}]
        if SHA.fullmatch(action.ref):
            properties.append({"name": f"{PROPERTY}pinned-commit", "value": action.ref})
        components.append(
            {
                "type": "application",
                "bom-ref": action.purl,
                "name": action.name,
                "version": action.tag or action.ref,
                "purl": action.purl,
                "properties": properties,
            }
        )
    bom = {
        "$schema": SCHEMA,
        "bomFormat": "CycloneDX",
        "specVersion": SPEC_VERSION,
        "version": 1,
        "metadata": {
            "tools": {
                "components": [
                    {
                        "type": "application",
                        "name": "skillcheck",
                        "description": "Builds this file with `uv run skillcheck --bom`.",
                    }
                ]
            },
            "component": {
                "type": "application",
                "bom-ref": root_ref,
                "name": inventory.name,
                "version": inventory.version,
                **_licence(inventory.license),
                "externalReferences": [{"type": "vcs", "url": inventory.repository}],
                "properties": [
                    {"name": f"{PROPERTY}language", "value": f"{language}: {count} file(s)"}
                    for language, count in inventory.languages.items()
                ],
            },
        },
        "components": sorted(components, key=lambda c: c["bom-ref"]),
        "services": [
            {
                "bom-ref": f"service:{service.key}",
                "provider": {"name": service.provider},
                "name": service.name,
                "description": service.description,
                **({"endpoints": list(service.endpoints)} if service.endpoints else {}),
                **(
                    {"externalReferences": [{"type": "documentation", "url": service.docs}]}
                    if service.docs
                    else {}
                ),
            }
            for service in inventory.services
        ],
        "dependencies": [
            {"ref": ref, "dependsOn": sorted(on)} for ref, on in sorted(dependencies.items())
        ],
    }
    # The serial number names this content, so the same repository always gives the same file.
    content = json.dumps(bom, sort_keys=True)
    serial = uuid.uuid5(uuid.NAMESPACE_URL, f"{inventory.repository}#{content}")
    bom = {**bom, "serialNumber": f"urn:uuid:{serial}"}
    order = ["$schema", "bomFormat", "specVersion", "serialNumber", "version"]
    ordered = {key: bom[key] for key in order} | {k: v for k, v in bom.items() if k not in order}
    return json.dumps(ordered, indent=2, ensure_ascii=False) + "\n"


def _ref(inventory: Inventory, ecosystem: str, name: str) -> str:
    [package] = [p for p in inventory.packages if p.ecosystem == ecosystem and p.name == name]
    return package.purl


def _licence(expression: str) -> dict:
    return {"licenses": [{"expression": expression}]} if expression else {}


def _skill(skill: Skill) -> dict:
    return {
        "type": "data",
        "bom-ref": f"skill:{skill.name}",
        "name": skill.name,
        **({"description": skill.detail} if skill.detail else {}),
        **_licence(skill.license),
        "properties": [
            {"name": f"{PROPERTY}fact-source", "value": f"{host}: {count} fact(s)"}
            for host, count in skill.sources
        ],
    }


def to_markdown(inventory: Inventory) -> str:
    """The map for people: the same facts as the BOM, in tables and trees."""
    out = [
        "# Dependency map",
        "",
        f"What `{inventory.name}` {inventory.version} is built from, runs on and relies on: the",
        "plugins it ships, the languages it's written in, its runtimes and tools, every package",
        "at its exact version, the GitHub Actions it pins, the services it uses, and the sources",
        "its skills' facts cite.",
        "",
        "`uv run skillcheck --bom` writes this page, and the same map for other tools to read as",
        f"[`bom.json`](../bom.json), in [CycloneDX {SPEC_VERSION}]"
        "(https://cyclonedx.org/specification/overview/).",
        "It reads them from the lockfiles, the workflows, `.python-version`, `pyproject.toml`,",
        "the plugin catalog and the skills, so don't edit either file by hand.",
        "`uv run skillcheck --bom-check` names a file that no longer matches. The weekly",
        "freshness run and the release workflow both run it.",
        "",
        "## What it ships",
        "",
        "| Plugin | Version | Licence | Skill | What it carries |",
        "|---|---|---|---|---|",
    ]
    for plugin in inventory.plugins:
        for skill in plugin.skills:
            out.append(
                f"| `{plugin.name}` | {plugin.version} | {plugin.license} | `{skill.name}` "
                f"| {skill.detail or '—'} |"
            )
    out += ["", "## Languages", "", "| Language | Tracked files |", "|---|---|"]
    out += [f"| {language} | {count} |" for language, count in inventory.languages.items()]
    out += [
        "",
        "## Runtimes and tools",
        "",
        "| Name | Version | Set in | Note |",
        "|---|---|---|---|",
    ]
    for tool in inventory.tools:
        where = ", ".join(f"`{w}`" for w in tool.where)
        out.append(f"| {tool.name} | {tool.version} | {where} | {tool.note or '—'} |")
    for ecosystem, title, lockfile in (
        ("pypi", "Python packages", "uv.lock"),
        ("npm", "Node packages", "package-lock.json"),
    ):
        packages = [p for p in inventory.packages if p.ecosystem == ecosystem]
        if not packages:
            continue
        out += [
            "",
            f"## {title}",
            "",
            f"Exact versions from `{lockfile}`. A development-only package isn't part of what the",
            "plugins ship.",
            "",
            "```",
            *_tree(inventory, ecosystem),
            "```",
        ]
    out += [
        "",
        "## GitHub Actions",
        "",
        "| Action | Version | Pinned commit | Used in |",
        "|---|---|---|---|",
    ]
    for action in inventory.actions:
        pinned = f"`{action.ref}`" if SHA.fullmatch(action.ref) else "not pinned to a commit"
        used = ", ".join(f"`{w}`" for w in action.workflows)
        out.append(f"| `{action.name}` | {action.tag or action.ref} | {pinned} | {used} |")
    out += [
        "",
        "## Services",
        "",
        "| Service | Provider | What for | Address |",
        "|---|---|---|---|",
    ]
    for service in inventory.services:
        endpoints = ", ".join(service.endpoints) or f"documented at {service.docs}"
        out.append(f"| {service.name} | {service.provider} | {service.description} | {endpoints} |")
    out += [
        "",
        "## Sources the skills' facts rely on",
        "",
        "Each skill's dated facts, in its `references/facts.md`, name where each was read. The",
        "weekly freshness run looks for every quote at its source again.",
        "",
        "| Skill | Source | Facts |",
        "|---|---|---|",
    ]
    for plugin in inventory.plugins:
        for skill in plugin.skills:
            out += [f"| `{skill.name}` | {host} | {count} |" for host, count in skill.sources]
            if not skill.sources:
                out.append(f"| `{skill.name}` | no `references/facts.md` | — |")
    return "\n".join(out) + "\n"


def _tree(inventory: Inventory, ecosystem: str) -> list[str]:
    packages = {p.name: p for p in inventory.packages if p.ecosystem == ecosystem}
    if ecosystem == "pypi" and inventory.project:
        top = inventory.project
        lines = [f"{top.name} {top.version} (this repository's checks)"]
        children = list(top.requires)
    else:
        lines = ["package.json"]
        children = inventory.direct["npm"]
    expanded: set[str] = set()

    def walk(names: list[str], indent: str) -> None:
        for index, name in enumerate(names):
            last = index == len(names) - 1
            package = packages[name]
            labels = [
                label for label, on in (("dev", package.dev), ("optional", package.optional)) if on
            ]
            if package.only_when:
                labels.append(f"only when {package.only_when}")
            label = f" ({'; '.join(labels)})" if labels else ""
            seen = name in expanded and package.requires
            lines.append(
                f"{indent}{'└── ' if last else '├── '}{name} {package.version}{label}"
                + (" (listed above)" if seen else "")
            )
            if not seen:
                expanded.add(name)
                walk(list(package.requires), indent + ("    " if last else "│   "))

    walk(children, "")
    return lines
