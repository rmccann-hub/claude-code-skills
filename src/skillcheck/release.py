"""What a release publishes beside its tag, built from the commit being released.

- ``KICKSTART.md``: the standard as one file, with run instructions for any repository, so a
  session can be handed it with no message. The standard's text is unchanged; only the two
  sections no run reads are left out.
- ``<skill>.zip``: each skill, packaged to upload to claude.ai.
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
AFTER_LICENCE = "No warranty of any kind.\n\n---\n\n# How to Read This File"
END = "**End of the kickstart file.** If you can read this line, the whole file arrived."
# A fixed time for every entry, so the same commit always packs the same bytes.
EPOCH = (1980, 1, 1, 0, 0, 0)
# A skill's rulesets, attached on their own because GitHub imports a ruleset from one JSON file.
RULESETS = "skills/*/assets/rulesets/*.json"


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
    files: dict[str, bytes] = {
        KICKSTART: kickstart(root, version).encode("utf-8"),
        NOTES: notes(root, version).encode("utf-8"),
        bom.BOM: (root / bom.BOM).read_bytes(),
        **packages(root),
        **rulesets(root),
    }
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
    for marker in (CUT, AFTER_LICENCE, frontmatter_version):
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
        + '  run_file: "the kickstart file: run instructions follow the licence, and the last'
        ' line is its end marker"\n',
    )
    text = text.replace(
        AFTER_LICENCE,
        "No warranty of any kind.\n\n" + instructions.rstrip("\n") + "\n\n---\n\n"
        "# How to Read This File",
    )
    first = (
        "RUN-FILE-FOR: the repository this session works in · JOB: chosen by what it holds · "
        f"FROM: {repository}, release {version}\n\n"
        "This file is the whole request, and it may arrive with no message. Read the run\n"
        "instructions below the licence, then run the standard that follows them.\n\n"
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
    lines = [
        "Install in Claude Code:",
        "",
        "```",
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
            f"| `{name}` | The {ruleset['name']} {ruleset['target']} ruleset, to import |"
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
            # Each entry reads "<mode> <object> <stage>\t<path>"; a hook keeps its mode 100755.
            listed = subprocess.run(
                ["git", "-C", str(root), "ls-files", "-s", "-z", "--", f"skills/{name}"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout
            entries = sorted(
                (path, mode.split()[0])
                for mode, path in (e.split("\t", 1) for e in listed.split("\0") if e)
            )
            buffer = BytesIO()
            with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
                for tracked, mode in entries:
                    entry = zipfile.ZipInfo(Path(tracked).relative_to("skills").as_posix(), EPOCH)
                    entry.external_attr = (0o755 if mode == "100755" else 0o644) << 16
                    entry.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(entry, (root / tracked).read_bytes())
            out[f"{name}.zip"] = buffer.getvalue()
    return out


def rulesets(root: Path) -> dict[str, bytes]:
    """Each tracked ruleset a skill ships, under the name the release gives it."""
    listed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "--", RULESETS],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    out: dict[str, bytes] = {}
    for tracked in sorted(path for path in listed.split("\0") if path):
        name = f"ruleset-{Path(tracked).stem}.json"
        if name in out:
            raise ReleaseError(f"two skills ship a ruleset called {Path(tracked).name}")
        out[name] = (root / tracked).read_bytes()
    return out


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
