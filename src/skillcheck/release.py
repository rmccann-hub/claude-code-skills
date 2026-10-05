"""What a release publishes beside its tag, built from the commit being released.

- ``KICKSTART.md``: the standard as one file, with run instructions for any repository, so a
  session can be handed it with no message. The standard's text is unchanged; only the two
  sections no run reads are left out.
- ``<skill>.zip``: each skill, packaged to upload to claude.ai.
- ``<Package>.zip``: each Vale package a skill ships, for a repository's ``.vale.ini`` to name.
- ``ruleset-<name>.json``: each ruleset a skill ships, to import into a repository's settings.
- ``bom.json``: the dependency map, which must already match the commit.
- ``notes.md``: the release page's text: how to install, what each file is, and the changelog's
  section for the version.

The release workflow runs ``skillcheck --release-assets VERSION DIR`` on the tagged commit, and
nothing is built until the catalog, the changelog and the map all agree with that version.
"""

import hashlib
import json
import subprocess
import zipfile
from io import BytesIO
from pathlib import Path
from urllib.parse import urlsplit

from skillcheck import bom
from skillcheck.core import standard
from skillcheck.core.checks import HIDDEN

KICKSTART = "KICKSTART.md"
NOTES = "notes.md"
INSTRUCTIONS = Path(__file__).with_name("kickstart.md")
# The two sections no run reads come last, from the first of them to the end of the file.
CUT = "\n---\n\n# Validating a Change to This Standard"
AFTER_LICENSE = "No warranty of any kind.\n\n---\n\n# How to Read This File"
END = "**End of the kickstart file.** If you can read this line, the whole file arrived."
# A fixed time for every entry, so the same commit always packs the same bytes.
EPOCH = (1980, 1, 1, 0, 0, 0)
# A skill's rulesets, attached on their own because GitHub imports a ruleset from one JSON file.
RULESETS = "skills/*/assets/rulesets/*.json"
# A skill's Vale packages, one folder each, attached on their own because Vale fetches by URL.
VALE = ":(glob)skills/*/assets/vale/**"


class ReleaseError(Exception):
    """The commit can't be released as it stands."""


def problems(root: Path, version: str) -> list[str]:
    """Everything that stops this commit being released as ``version``."""
    found = []
    for plugin in _catalog(root)["plugins"]:
        if plugin.get("version") != version:
            found.append(
                f"the catalog's `{plugin['name']}` plugin says {plugin.get('version')}, "
                f"not {version}"
            )
    if _section(root, version) is None:
        found.append(f"CHANGELOG.md has no section for {version}")
    found += [f"{path} is out of date: run `uv run skillcheck --bom`" for path in bom.stale(root)]
    return found


def build(root: Path, version: str, out: Path) -> list[str]:
    """Write the release's files to ``out`` and return their names."""
    files: dict[str, bytes] = {}
    for part in (
        {
            KICKSTART: kickstart(root, version).encode("utf-8"),
            NOTES: notes(root, version).encode("utf-8"),
            bom.BOM: (root / bom.BOM).read_bytes(),
        },
        packages(root),
        vale_packages(root),
        rulesets(root),
    ):
        for name, data in part.items():
            if name in files:
                raise ReleaseError(f"two of the release's files would be called {name}")
            files[name] = data
    out.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        (out / name).write_bytes(data)
    return sorted(files)


def kickstart(root: Path, version: str) -> str:
    """The standard, with run instructions for whichever repository it's handed in."""
    copies = standard.find(root)
    if len(copies) != 1:
        raise ReleaseError(f"expected one copy of the standard, found {len(copies)}")
    [path] = copies
    text = path.read_text(encoding="utf-8")
    number = standard.FILENAME.fullmatch(path.name)[1]
    frontmatter_version = f'  version: "{number}"\n'
    for marker in (CUT, AFTER_LICENSE, frontmatter_version):
        if text.count(marker) != 1:
            raise ReleaseError(f"the standard doesn't hold {marker.strip()!r} exactly once")
    repository = _repository(root)
    instructions = (
        INSTRUCTIONS.read_text(encoding="utf-8")
        .replace("RELEASE_VERSION", version)
        .replace("STANDARD_VERSION", number)
        .replace("STANDARD_SHA256", hashlib.sha256(text.encode("utf-8")).hexdigest())
        .replace("REPOSITORY", repository)
    )
    text = text[: text.index(CUT)] + "\n"
    text = text.replace(
        frontmatter_version,
        frontmatter_version
        + '  extract: "Validating a Change to This Standard and Provenance left out; the full'
        f' file is in release {version} of {repository}"\n'
        + '  run_file: "the kickstart file: run instructions follow the license, and the last'
        ' line is its end marker"\n',
    )
    text = text.replace(
        AFTER_LICENSE,
        "No warranty of any kind.\n\n" + instructions.rstrip("\n") + "\n\n---\n\n"
        "# How to Read This File",
    )
    first = (
        "RUN-FILE-FOR: the repository this session works in · JOB: chosen by what it holds · "
        f"FROM: {repository}, release {version}\n\n"
        "This file is the whole request, and it may arrive with no message. Read the run\n"
        "instructions below the license, then run the standard that follows them.\n\n"
    )
    whole = first + text.rstrip("\n") + "\n\n" + END + "\n"
    hidden = HIDDEN.search(whole)
    if hidden:
        raise ReleaseError(f"the kickstart file would hold U+{ord(hidden.group()):04X}")
    return whole


def notes(root: Path, version: str) -> str:
    """The release page: how to install, what each file is, and what changed."""
    catalog = _catalog(root)
    repository = _repository(root)
    number = standard.FILENAME.fullmatch(standard.find(root)[0].name)[1]
    skills = [Path(path).name for plugin in catalog["plugins"] for path in plugin["skills"]]
    section = _section(root, version)
    if section is None:
        raise ReleaseError(f"CHANGELOG.md has no section for {version}")
    sets = {name: json.loads(data) for name, data in rulesets(root).items()}
    styles = sorted(vale_packages(root))
    lines = [
        "Install in Claude Code:",
        "",
        "```text",
        f"/plugin marketplace add {repository}",
        *[f"/plugin install {p['name']}@{catalog['name']}" for p in catalog["plugins"]],
        "```",
        "",
        "To start any repository with the standard, attach `KICKSTART.md` to a session there. It",
        "needs no message: it reads the repository first, asks only what it can't find out, and",
        "stops twice for answers before it changes anything. A session can also be told to read",
        f"the newest one at https://github.com/{repository}/releases/latest/download/{KICKSTART}.",
        "",
        *(
            [
                "A ruleset file imports into any repository: in its Settings, Rules,",
                "Rulesets, open the New ruleset menu and choose Import a ruleset.",
                "",
            ]
            if sets
            else []
        ),
        "| File | What it is |",
        "|---|---|",
        f"| `{KICKSTART}` | Standard v{number} as one file, for a session in any repository |",
        *[
            f"| `{name}.zip` | The `{name}` skill, packaged to upload to claude.ai |"
            for name in skills
        ],
        *[
            f"| `{name}` | The {Path(name).stem} Vale style, which a repository's `.vale.ini` "
            "names by URL |"
            for name in styles
        ],
        *[
            f'| `{name}` | A {ruleset["target"]} ruleset, "{ruleset["name"]}", to import |'
            for name, ruleset in sets.items()
        ],
        f"| `{bom.BOM}` | The dependency map in CycloneDX {bom.SPEC_VERSION}; "
        f"`{bom.MAP}` is the same for people |",
        "",
        section,
    ]
    return "\n".join(lines).rstrip("\n") + "\n"


def packages(root: Path) -> dict[str, bytes]:
    """Each skill in the catalog as a ZIP of its tracked files, under its own folder."""
    out = {}
    for plugin in _catalog(root)["plugins"]:
        for path in plugin["skills"]:
            name = Path(path).name
            out[f"{name}.zip"] = _archive(root, _tracked(root, f"skills/{name}"), "skills")
    return out


def vale_packages(root: Path) -> dict[str, bytes]:
    """Each Vale package a skill ships, as a ZIP holding one folder named for the package."""
    found: dict[str, tuple[str, list[tuple[str, str]]]] = {}
    for tracked, mode in _tracked(root, VALE):
        parts = Path(tracked).parts
        if len(parts) < 6:
            raise ReleaseError(f"{tracked} isn't inside a Vale package's folder")
        base, name = Path(*parts[:4]).as_posix(), parts[4]
        if found.setdefault(name, (base, []))[0] != base:
            raise ReleaseError(f"two skills ship a Vale package called {name}")
        found[name][1].append((tracked, mode))
    return {f"{name}.zip": _archive(root, files, base) for name, (base, files) in found.items()}


def rulesets(root: Path) -> dict[str, bytes]:
    """Each tracked ruleset a skill ships, under the name the release gives it."""
    out: dict[str, bytes] = {}
    for tracked, _mode in _tracked(root, RULESETS):
        name = f"ruleset-{Path(tracked).stem}.json"
        if name in out:
            raise ReleaseError(f"two skills ship a ruleset called {Path(tracked).name}")
        out[name] = (root / tracked).read_bytes()
    return out


def _tracked(root: Path, pathspec: str) -> list[tuple[str, str]]:
    """Each tracked file the pathspec matches, with its mode, so a hook keeps its 100755."""
    # Each entry reads "<mode> <object> <stage>\t<path>".
    listed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-s", "-z", "--", pathspec],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return sorted(
        (path, mode.split()[0])
        for mode, path in (entry.split("\t", 1) for entry in listed.split("\0") if entry)
    )


def _archive(root: Path, files: list[tuple[str, str]], base: str) -> bytes:
    """A ZIP of tracked files, each named from ``base``, the same bytes for the same commit."""
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for tracked, mode in files:
            entry = zipfile.ZipInfo(Path(tracked).relative_to(base).as_posix(), EPOCH)
            entry.external_attr = (0o755 if mode == "100755" else 0o644) << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, (root / tracked).read_bytes())
    return buffer.getvalue()


def _catalog(root: Path) -> dict:
    return json.loads((root / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))


def _repository(root: Path) -> str:
    urls = {p["repository"] for p in _catalog(root)["plugins"] if p.get("repository")}
    if len(urls) != 1:
        raise ReleaseError(f"expected the catalog to name one repository, found {len(urls)}")
    return urlsplit(urls.pop()).path.strip("/")


def _section(root: Path, version: str) -> str | None:
    """The changelog's text for one version, without its heading, or None if it has none."""
    lines = (root / "CHANGELOG.md").read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith(f"## [{version}]")]
    if not starts:
        return None
    body = []
    for line in lines[starts[0] + 1 :]:
        if line.startswith("## ["):
            break
        body.append(line)
    return "\n".join(body).strip("\n")
