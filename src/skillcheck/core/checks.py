"""The repository's rules for skills and the plugin catalog.

These cover what `claude plugin validate --strict` does not. Measured on Claude Code 2.1.280 it
validates the catalog manifest, and it reported none of these planted in a skill: a name that
does not match its directory, a name in the wrong case, a description over the limit, a field
outside the spec, and a catalog path to a skill that does not exist.
"""

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from skillcheck.core import frontmatter, standard

SKILLS_DIR = "skills"
CATALOG = ".claude-plugin/marketplace.json"

# The roadmap and the README both list skills. Two surfaces answering one question are a defect
# waiting for the day they disagree, so both are compared with skills/ on every run.
ROADMAP = "ROADMAP.md"
README = "README.md"
ROADMAP_STATUSES = ("shipped", "building", "researching", "planned")
TICKED = re.compile(r"`([^`]+)`")

# The Agent Skills spec's fields (agentskills.io/specification). claude.ai rejects an upload that
# carries any other field, and claude.ai is how skills reach cloud sessions.
ALLOWED_KEYS = frozenset(
    {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
)
NAME_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500
# Both the spec and Claude Code's docs: "Keep SKILL.md under 500 lines." The whole file loads
# every time the skill activates; detail belongs in files it links to.
MAX_SKILL_LINES = 500

# A catalog entry serving skills from this repository names each one as ./skills/<name>, or the
# whole folder as ./skills/. Claude Code loads every skill when none of an entry's listed paths
# exist, so a typo does not fail at install time: it quietly ships the whole folder.
SKILL_PATH = re.compile(r"\./skills/([^/]+)/?")
WHOLE_FOLDER = {"./skills", "./skills/"}

# Only explicit Markdown links are checked. A bare path such as scripts/build.sh in a skill's
# advice usually means the reader's repository, not a file bundled with the skill.
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

# Characters that render as nothing or reorder the text around them, so what a reviewer sees
# differs from what an agent reads: zero-width characters and joiners, bidirectional controls
# (the Trojan Source attack, CVE-2021-42574), the byte-order mark, the soft hyphen, and Unicode
# tag characters, which can carry a whole hidden instruction.
HIDDEN = re.compile(
    "[\u00ad\u180e\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff\U000e0000-\U000e007f]"
)
# Outside skills/, the files agents read as instructions or context. Research results are pasted
# in from outside the repository, so they get the same scan as a skill.
AGENT_FILES = ("AGENTS.md", "CLAUDE.md")
AGENT_DIRS = (".claude", "research")


@dataclass(frozen=True)
class Finding:
    path: str
    rule: str
    message: str


@dataclass
class Report:
    skills: int = 0
    # Every installed skill's description is listed to the model, and the listing has a budget:
    # in one session 50 skills' 26,620 characters left the last 9 with no description at all.
    description_chars: int = 0
    catalog_plugins: int | None = None
    roadmap_entries: int | None = None
    readme_entries: int | None = None
    standard_version: str | None = None
    findings: list[Finding] = field(default_factory=list)

    def add(self, path: str, rule: str, message: str) -> None:
        self.findings.append(Finding(path, rule, message))

    def summary(self) -> str:
        if self.catalog_plugins is None:
            catalog = "no catalog"
        else:
            catalog = f"{self.catalog_plugins} catalog plugin(s)"
        if self.roadmap_entries is None:
            roadmap = "no roadmap"
        else:
            roadmap = f"{self.roadmap_entries} roadmap entries"
        stamp = (
            "no standard" if self.standard_version is None else f"standard {self.standard_version}"
        )
        return (
            f"skillcheck: {self.skills} skill(s), {self.description_chars} description "
            f"characters, {catalog}, {roadmap}, {stamp}, {len(self.findings)} finding(s)"
        )


def check_repository(root: Path) -> Report:
    report = Report()
    skills = _discover_skills(root, report)
    for skill_dir in skills:
        _check_skill(skill_dir, report)
    _check_catalog(root, skills, report)
    names = {skill.name for skill in skills}
    _check_roadmap(root, names, report)
    _check_readme(root, names, report)
    _check_agent_files(root, report)
    for path in standard.find(root):
        report.standard_version = standard.check(root, path, report.add)
    return report


def _discover_skills(root: Path, report: Report) -> list[Path]:
    skills_root = root / SKILLS_DIR
    if not skills_root.is_dir():
        return []
    found = []
    for entry in sorted(skills_root.iterdir()):
        where = f"{SKILLS_DIR}/{entry.name}"
        if not entry.is_dir():
            report.add(where, "layout", f"{SKILLS_DIR}/ holds only skill directories")
        elif (entry / "SKILL.md").is_file():
            found.append(entry)
        else:
            report.add(where, "layout", "skill directory has no SKILL.md")
    report.skills = len(found)
    return found


def _check_skill(skill_dir: Path, report: Report) -> None:
    where = f"{SKILLS_DIR}/{skill_dir.name}/SKILL.md"
    _check_hidden_characters(skill_dir.parent.parent, _files_under(skill_dir), report)
    try:
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        data, body = frontmatter.parse(text)
    except (frontmatter.FrontmatterError, UnicodeDecodeError) as exc:
        report.add(where, "frontmatter", str(exc))
        return
    lines = len(text.splitlines())
    if lines >= MAX_SKILL_LINES:
        report.add(where, "size", f"SKILL.md is {lines} lines; keep it under {MAX_SKILL_LINES}")
    _check_links(skill_dir, body, where, report)
    _check_optional_fields(data, where, report)

    extra = sorted(str(key) for key in data if key not in ALLOWED_KEYS)
    if extra:
        report.add(where, "frontmatter-keys", f"fields outside the spec: {', '.join(extra)}")

    name = data.get("name")
    if not isinstance(name, str) or not name:
        report.add(where, "name", "name is missing or not a string")
    else:
        if name != skill_dir.name:
            report.add(where, "name", f"name {name!r} does not match directory {skill_dir.name!r}")
        if len(name) > MAX_NAME_LENGTH or not NAME_PATTERN.fullmatch(name):
            report.add(
                where,
                "name",
                f"name {name!r} must be 1-{MAX_NAME_LENGTH} lowercase letters, digits and "
                "single hyphens",
            )

    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        report.add(where, "description", "description is missing or empty")
        return
    report.description_chars += len(description)
    if len(description) > MAX_DESCRIPTION_LENGTH:
        report.add(
            where,
            "description",
            f"description is {len(description)} characters; the limit is {MAX_DESCRIPTION_LENGTH}",
        )


def _local_links(text: str) -> list[str]:
    """Relative link targets in Markdown text, without anchors, URLs, mail or absolute paths."""
    paths = set()
    for match in LINK.finditer(text):
        path = match.group(1).split("#", 1)[0]
        if path and "://" not in path and not path.startswith(("/", "mailto:")):
            paths.add(path)
    return sorted(paths)


def _check_links(skill_dir: Path, body: str, where: str, report: Report) -> None:
    for path in _local_links(body):
        target = skill_dir / path
        if not target.exists():
            report.add(where, "reference", f"links to {path}, which does not exist")
        elif target.suffix == ".md":
            _check_reference_depth(skill_dir, target, report)


def _check_reference_depth(skill_dir: Path, reference: Path, report: Report) -> None:
    # The spec: "Keep file references one level deep from SKILL.md. Avoid deeply nested
    # reference chains." An agent may read part of a file and stop, so a chain hides its end.
    root = skill_dir.resolve()
    reference = reference.resolve()
    if not reference.is_relative_to(root):
        return
    where = f"{SKILLS_DIR}/{skill_dir.name}/{reference.relative_to(root).as_posix()}"
    for path in _local_links(reference.read_text(encoding="utf-8", errors="replace")):
        target = (reference.parent / path).resolve()
        if target.suffix == ".md" and target.is_file() and target != root / "SKILL.md":
            shown = target.relative_to(root).as_posix() if target.is_relative_to(root) else path
            report.add(
                where,
                "reference-depth",
                f"links to {shown}; keep references one level deep from SKILL.md",
            )


def _check_optional_fields(data: dict, where: str, report: Report) -> None:
    """The spec's optional fields, in the form claude.ai accepts at upload."""
    if "license" in data and not _is_text(data["license"]):
        report.add(where, "license", "license must name a licence or a bundled licence file")
    if "compatibility" in data:
        value = data["compatibility"]
        if not _is_text(value):
            report.add(where, "compatibility", "compatibility must be non-empty text")
        elif len(value) > MAX_COMPATIBILITY_LENGTH:
            report.add(
                where,
                "compatibility",
                f"compatibility is {len(value)} characters; "
                f"the limit is {MAX_COMPATIBILITY_LENGTH}",
            )
    if "metadata" in data:
        value = data["metadata"]
        if not isinstance(value, dict):
            report.add(where, "metadata", "metadata must map strings to strings")
        else:
            wrong = sorted(str(k) for k, v in value.items() if not isinstance(v, str))
            if wrong:
                report.add(
                    where, "metadata", f"metadata values must be quoted strings: {', '.join(wrong)}"
                )
    if "allowed-tools" in data and not _is_text(data["allowed-tools"]):
        report.add(where, "allowed-tools", "allowed-tools must be one space-separated string")


def _is_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _check_agent_files(root: Path, report: Report) -> None:
    files = [root / name for name in AGENT_FILES if (root / name).is_file()]
    for directory in AGENT_DIRS:
        if (root / directory).is_dir():
            files += _files_under(root / directory)
    _check_hidden_characters(root, files, report)


def _files_under(directory: Path) -> list[Path]:
    return sorted(p for p in directory.rglob("*") if p.is_file())


def _check_hidden_characters(root: Path, files: list[Path], report: Report) -> None:
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue  # binary assets carry no hidden text instructions
        hits = [
            (number, match.group())
            for number, line in enumerate(text.split("\n"), 1)
            for match in HIDDEN.finditer(line)
        ]
        if not hits:
            continue
        number, char = hits[0]
        more = f", and {len(hits) - 1} more in this file" if len(hits) > 1 else ""
        report.add(
            path.relative_to(root).as_posix(),
            "unicode",
            f"line {number} holds U+{ord(char):04X}, which is invisible or reorders text{more}",
        )


def _check_catalog(root: Path, skills: list[Path], report: Report) -> None:
    catalog_file = root / CATALOG
    if not catalog_file.is_file():
        if skills:
            report.add(CATALOG, "catalog", f"missing, so {len(skills)} skill(s) ship in no plugin")
        return
    try:
        catalog = json.loads(catalog_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        report.add(CATALOG, "catalog", f"not valid JSON: {exc}")
        return
    plugins = catalog.get("plugins") if isinstance(catalog, dict) else None
    if not isinstance(plugins, list):
        report.add(CATALOG, "catalog", "has no 'plugins' list")
        return
    report.catalog_plugins = len(plugins)

    listed_by: dict[str, list[str]] = {skill.name: [] for skill in skills}
    for plugin in plugins:
        # Only entries whose source is this repository's root serve skills from skills/.
        if not isinstance(plugin, dict) or plugin.get("source") != "./":
            continue
        plugin_name = str(plugin.get("name", "<unnamed>"))
        paths = plugin.get("skills", [])
        if isinstance(paths, str):
            paths = [paths]
        if not isinstance(paths, list):
            report.add(CATALOG, "catalog", f"{plugin_name}: 'skills' is not a list of paths")
            continue
        for raw in paths:
            if isinstance(raw, str) and raw in WHOLE_FOLDER:
                for owners in listed_by.values():
                    owners.append(plugin_name)
                continue
            match = SKILL_PATH.fullmatch(raw) if isinstance(raw, str) else None
            if match is None:
                report.add(CATALOG, "catalog", f"{plugin_name}: {raw!r} is not ./skills/<name>")
            elif match.group(1) not in listed_by:
                report.add(CATALOG, "catalog", f"{plugin_name}: {raw!r} has no SKILL.md")
            else:
                listed_by[match.group(1)].append(plugin_name)

    for skill_name, owners in listed_by.items():
        where = f"{SKILLS_DIR}/{skill_name}"
        if not owners:
            report.add(where, "catalog", "no catalog plugin lists this skill")
        elif len(owners) > 1:
            report.add(where, "catalog", f"listed by {len(owners)} plugins: {', '.join(owners)}")


def _skill_tables(text: str) -> list[list[tuple[str, dict[str, str]]]]:
    """Every Markdown table whose first header cell is "Skill", as rows of (name, cells)."""
    lines = text.splitlines()
    tables = []
    index = 0
    while index < len(lines) - 1:
        header = _cells(lines[index])
        separator = lines[index + 1].strip()
        if header and header[0] == "Skill" and "-" in separator and set(separator) <= set("|-: "):
            rows = []
            index += 2
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                cells = _cells(lines[index])
                ticked = TICKED.search(cells[0])
                rows.append(
                    (
                        ticked.group(1) if ticked else cells[0],
                        dict(zip(header, cells, strict=False)),
                    )
                )
                index += 1
            tables.append(rows)
        else:
            index += 1
    return tables


def _cells(line: str) -> list[str]:
    line = line.strip()
    if not line.startswith("|"):
        return []
    return [cell.strip() for cell in line.strip("|").split("|")]


def _check_roadmap(root: Path, names: set[str], report: Report) -> None:
    path = root / ROADMAP
    if not path.is_file():
        return
    rows = [row for table in _skill_tables(path.read_text(encoding="utf-8")) for row in table]
    report.roadmap_entries = len(rows)
    for name, count in sorted(Counter(name for name, _ in rows).items()):
        if count > 1:
            report.add(ROADMAP, "roadmap", f"`{name}` is listed {count} times")
    shipped = set()
    for name, cells in rows:
        status = cells.get("Status", "")
        if status not in ROADMAP_STATUSES:
            report.add(
                ROADMAP,
                "roadmap",
                f"`{name}` has status {status!r}; use one of {', '.join(ROADMAP_STATUSES)}",
            )
        elif status == "shipped":
            shipped.add(name)
            if name not in names:
                report.add(
                    ROADMAP,
                    "roadmap",
                    f"`{name}` is marked shipped, but {SKILLS_DIR}/{name} does not exist",
                )
    for name in sorted(names - shipped):
        report.add(f"{SKILLS_DIR}/{name}", "roadmap", f"not listed as shipped in {ROADMAP}")


def _check_readme(root: Path, names: set[str], report: Report) -> None:
    path = root / README
    if not path.is_file():
        return
    tables = _skill_tables(path.read_text(encoding="utf-8"))
    if not tables:
        return
    listed = {name for table in tables for name, _ in table}
    report.readme_entries = len(listed)
    for name in sorted(names - listed):
        report.add(f"{SKILLS_DIR}/{name}", "readme", "not listed in the README's skill table")
    for name in sorted(listed - names):
        report.add(README, "readme", f"lists `{name}`, but {SKILLS_DIR}/{name} does not exist")
