"""Each dependency against its newest release: ``skillcheck --outdated``.

What a repository uses comes from the same readers as the dependency map (``bom.py``): the
lockfiles, the workflows' actions and tool versions, ``.python-version`` and ``pyproject.toml``.
The pins in a ``requirements*.lock`` or ``requirements*.txt`` at the root are read here too, as
pip-tools and ``uv pip compile`` write them: ``name==version``, one to a line.
Each registry then names its newest stable release and the day it came out:

- **behind:** a newer release has been out for at least ``COOLDOWN_DAYS``;
- **waiting:** a newer release is still inside that wait, the default Dependabot also keeps;
- **unread:** the registry couldn't be read, or the pin names no exact version. A lookup that
  fails never passes for current.

A version range in ``pyproject.toml`` that excludes the newest release is behind too, because
nothing can install the newest until someone raises it. Runner images and system packages
aren't checked: neither has a registry that says which version is newest.
"""

import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from urllib.parse import quote

from skillcheck import bom

COOLDOWN_DAYS = 3
TIMEOUT_SECONDS = 30
USER_AGENT = "skillcheck (https://github.com/rmccann-hub/claude-code-skills)"

# A runtime set by a setup action or `.python-version`, and its product on endoflife.date.
RUNTIMES = {"Python": "python", "Go": "go", "Node.js": "nodejs"}
GITHUB_MODULE = re.compile(r"pkg:golang/github\.com/([\w.-]+)/([\w.-]+)")
PINNED = re.compile(r"^([A-Za-z0-9][\w.-]*)(?:\[[^\]]*\])?[ \t]*==[ \t]*([^\s;\\#]+)", re.MULTILINE)
# An action pinned to a tag or a branch, not a commit: it moves with each release it names.
MOVING = "a moving tag, not a commit"
CLAUSE = re.compile(r"\s*(~=|==|!=|<=|>=|<|>)\s*([^\s,;]+)")
REQUIREMENT = re.compile(r"\s*(?P<name>[A-Za-z0-9][\w.-]*)(?:\[[^\]]*\])?\s*(?P<spec>[^;@]*)")

Fetch = Callable[[str], object]


class NoRelease(ValueError):
    """A repository with neither a published release nor a version tag."""


@dataclass(frozen=True)
class Release:
    version: str
    published: date | None


@dataclass(frozen=True)
class Result:
    state: str
    kind: str
    name: str
    used: str
    newest: str = ""
    published: date | None = None
    note: str = ""

    def line(self) -> str:
        if self.state == "unread":
            return f"unread   {self.kind} {self.name} {self.used}: {self.note}"
        out = f"{self.state:<8} {self.kind} {self.name} {self.used} -> {self.newest}"
        if self.published:
            out += f", out since {self.published.isoformat()}"
        return out + (f" ({self.note})" if self.note else "")


def fetch_json(url: str) -> object:
    """Read one registry answer. A GitHub token in the environment lifts the API's rate limit."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def scan(root: Path, fetch: Fetch = fetch_json, today: date | None = None) -> list[Result]:
    """Every dependency the repository declares, each with its state."""
    today = today or datetime.now(UTC).date()
    fetch = _once(fetch)
    wanted: dict[tuple[str, str, str], tuple[Callable[[], Release], str]] = {}

    def want(kind: str, name: str, used: str, newest: Callable[[], Release], note: str = ""):
        wanted.setdefault((kind, name, used), (newest, note))

    _, packages = bom._python(root)
    for package in packages:
        want("pypi", package.name, package.version, lambda n=package.name: _pypi(fetch, n))
    for where, name, version in _pinned(root):
        want("pypi", name, version, lambda n=name: _pypi(fetch, n), where)
    # An optional npm package is a platform build of another, at that package's version.
    for package in bom._node(root)[0]:
        if not package.optional:
            want("npm", package.name, package.version, lambda n=package.name: _npm(fetch, n))
    workflows = bom._workflows(root)
    for action in bom._actions(workflows):
        owner_repo = "/".join(action.name.split("/")[:2])
        pinned = bom.SHA.fullmatch(action.ref)
        want(
            "action",
            action.name,
            action.tag if pinned else action.ref,
            lambda r=owner_repo: _github(fetch, r),
            "" if pinned else MOVING,
        )
    pyproject = bom._toml(root / "pyproject.toml")
    for tool in bom._ci_tools(workflows) + bom._runtimes(root, pyproject):
        _want_tool(want, fetch, tool)
    for requirement in _requirements(pyproject):
        if (match := REQUIREMENT.match(requirement)) and match["spec"].strip():
            name = match["name"]
            want(
                "range",
                name,
                match["spec"].strip(),
                lambda n=name: _pypi(fetch, n),
                "pyproject.toml",
            )

    results = []
    for (kind, name, used), (newest, note) in sorted(wanted.items()):
        try:
            release = newest()
        except (
            OSError,
            ValueError,
            KeyError,
            IndexError,
            TypeError,
            subprocess.SubprocessError,
        ) as error:
            results.append(Result("unread", kind, name, used, note=_reason(error)))
            continue
        results.append(_judge(kind, name, used, release, note, today))
    return results


def _once(fetch: Fetch) -> Fetch:
    """The fetch, asking each address once a run: several pins can share one registry answer."""
    answers: dict[str, object] = {}

    def cached(url: str) -> object:
        if url not in answers:
            try:
                answers[url] = fetch(url)
            except Exception as error:
                answers[url] = error
        answer = answers[url]
        if isinstance(answer, Exception):
            raise answer
        return answer

    return cached


def report(results: list[Result]) -> tuple[list[str], str, int]:
    """The lines worth reading, the summary, and the exit code: 1 when anything needs action."""
    counts = {state: sum(r.state == state for r in results) for state in ("behind", "waiting")}
    unread = sum(r.state == "unread" for r in results)
    lines = [r.line() for r in results if r.state != "current"]
    summary = (
        f"skillcheck: {len(results)} dependencies checked, {counts['behind']} behind, "
        f"{counts['waiting']} waiting out the {COOLDOWN_DAYS}-day wait, {unread} unread"
    )
    return lines, summary, 1 if counts["behind"] or unread else 0


def _want_tool(want, fetch: Fetch, tool: bom.Tool) -> None:
    if tool.name in RUNTIMES:
        product = RUNTIMES[tool.name]
        want("runtime", tool.name, tool.version, lambda: _cycle(fetch, product), tool.where[0])
    elif tool.name == "uv":
        want("tool", "uv", tool.version, lambda: _pypi(fetch, "uv"), tool.where[0])
    elif tool.note == "build backend":
        want("range", tool.name, tool.version, lambda: _pypi(fetch, tool.name), "build backend")
    elif match := GITHUB_MODULE.match(tool.purl):
        repo = f"{match[1]}/{match[2]}"
        want("tool", tool.name, tool.version, lambda: _github(fetch, repo), tool.where[0])


def _judge(kind: str, name: str, used: str, release: Release, note: str, today: date) -> Result:
    if kind == "range":
        fresh = _allows(used, release.version)
    elif kind == "runtime":
        if "${{" in used:
            return Result("unread", kind, name, used, note="set by an expression; read its values")
        if not _key(used):
            return Result("unread", kind, name, used, note="no version is named")
        fresh = _runtime_current(used, release.version)
    else:
        newest, mine = _key(release.version), _key(used)
        if not mine:
            return Result("unread", kind, name, used or "(none)", note="the pin names no version")
        if note == MOVING:
            # `v7` follows every 7.x release, so it's current while the newest is a 7.x.
            fresh = mine >= newest[: len(mine)]
        elif len(mine) < len(newest) and newest[: len(mine)] == mine:
            return Result("unread", kind, name, used, note=f"names {used}, not one release of it")
        else:
            fresh = mine >= newest
    if fresh:
        return Result("current", kind, name, used, release.version, release.published, note)
    age = (today - release.published).days if release.published else COOLDOWN_DAYS
    state = "behind" if age >= COOLDOWN_DAYS else "waiting"
    return Result(state, kind, name, used, release.version, release.published, note)


def _runtime_current(used: str, cycle: str) -> bool:
    """A version like `3.14`, `24` or `>=3.14` against the newest release line."""
    if CLAUSE.match(used):
        return _allows(used, cycle)
    return _key(used)[: len(_key(cycle))] >= _key(cycle)


def _allows(spec: str, version: str) -> bool:
    """Whether a PEP 440-style range admits a version, for the operators ranges use."""
    target = _key(version)
    for op, bound in CLAUSE.findall(spec):
        edge = _key(bound.rstrip(".*"))
        head = target[: len(edge)]
        if op == "~=":
            ok = target >= edge and target[: len(edge) - 1] == edge[:-1]
        else:
            ok = {
                "==": head == edge,
                "!=": head != edge,
                "<": target < edge,
                "<=": target <= edge,
                ">": target > edge,
                ">=": target >= edge,
            }[op]
        if not ok:
            return False
    return True


def _key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in re.findall(r"\d+", version))


def _pinned(root: Path) -> list[tuple[str, str, str]]:
    """Each pin in a requirements file at the root, with the file it's in."""
    return [
        (path.name, name, version)
        for path in sorted(root.glob("requirements*"))
        if path.suffix in {".lock", ".txt"}
        for name, version in PINNED.findall(path.read_text(encoding="utf-8"))
    ]


def _requirements(pyproject: dict) -> list[str]:
    project = pyproject.get("project", {})
    found = list(project.get("dependencies", []))
    for group in project.get("optional-dependencies", {}).values():
        found += group
    for group in pyproject.get("dependency-groups", {}).values():
        found += [entry for entry in group if isinstance(entry, str)]
    return found


def _day(text: str | None) -> date | None:
    return date.fromisoformat(text[:10]) if text else None


def _pypi(fetch: Fetch, name: str) -> Release:
    data = fetch(f"https://pypi.org/pypi/{quote(name)}/json")
    version = data["info"]["version"]
    files = data["releases"].get(version) or [{}]
    return Release(version, _day(files[0].get("upload_time_iso_8601")))


def _npm(fetch: Fetch, name: str) -> Release:
    data = fetch(f"https://registry.npmjs.org/{quote(name, safe='@')}")
    version = data["dist-tags"]["latest"]
    return Release(version, _day(data.get("time", {}).get(version)))


def _github(fetch: Fetch, repo: str) -> Release:
    """The latest release, or the highest version tag where the API can't be read.

    The API names the release's date; the tags don't, so a release found by its tag counts as
    past the wait. Without a token the API allows 60 requests an hour, and some networks
    refuse it while still serving git.
    """
    try:
        data = fetch(f"https://api.github.com/repos/{repo}/releases/latest")
        return Release(data["tag_name"], _day(data.get("published_at")))
    except (OSError, ValueError, KeyError, TypeError) as error:
        if isinstance(error, urllib.error.HTTPError):
            error.close()
        listed = subprocess.run(
            ["git", "ls-remote", "--tags", "--refs", f"https://github.com/{repo}.git"],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            check=True,
        ).stdout
        tags = [line.rpartition("refs/tags/")[2] for line in listed.splitlines()]
        versions = [t for t in tags if re.fullmatch(r"v?\d+(\.\d+)*", t)]
        if not versions:
            raise NoRelease("it publishes no release and no version tag") from None
        return Release(max(versions, key=_key), None)


def _cycle(fetch: Fetch, product: str) -> Release:
    """The newest release line; for Node.js, the newest that has reached long-term support."""
    cycles = fetch(f"https://endoflife.date/api/{product}.json")
    if product == "nodejs":
        today = datetime.now(UTC).date().isoformat()
        cycles = [c for c in cycles if c.get("lts") is True or str(c.get("lts")) <= today]
    newest = cycles[0]
    return Release(str(newest["cycle"]), _day(newest.get("releaseDate")))


def _reason(error: Exception) -> str:
    if isinstance(error, NoRelease):
        return str(error)
    if isinstance(error, urllib.error.HTTPError):
        error.close()  # it holds the response open
        return f"the registry answered {error.code}"
    return f"the registry couldn't be read ({type(error).__name__})"
