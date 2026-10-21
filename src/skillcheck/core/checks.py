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

from skillcheck.core import content, facts, frontmatter, modules, reporting, standard, times

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
# Claude Code lists every skill to the model as "- name: description", within 1% of the context
# window at 4 characters a token: 8,000 characters for a 200,000-token model, 40,000 for a
# million (its code, read on 2.1.301). Over that, the skills used least keep only their names.
# So coverage grows by modules, which cost nothing until read, and the skills stay few: each
# description is capped well under the spec's limit, and the listing is held to 20 skills at 240,
# which leaves room on a 200,000-token model for Anthropic's skills beside them (ROADMAP.md).
DESCRIPTION_CAP = 250
MAX_SKILLS = 20
LISTING_BUDGET = MAX_SKILLS * (240 + 20)
MAX_COMPATIBILITY_LENGTH = 500
# Both the spec and Claude Code's docs: "Keep SKILL.md under 500 lines." The whole file loads
# every time the skill activates; detail belongs in files it links to.
MAX_SKILL_LINES = 500
# Anthropic sizes the part of a skill read when it's triggered at "Under 5k tokens" (Agent
# Skills overview, read 2026-10-16); at about 4 characters a token that's 20,000 characters.
# The same file loads on claude.ai and in Claude Code, so a router stays small on both.
MAX_SKILL_CHARS = 20_000
# The standard's budget for an always-loaded context file, enforced since v0.43.0: 300 lines at
# most, and Codex stops reading instruction files past 32 KiB by default.
MAX_CONTEXT_LINES = 300
MAX_CONTEXT_BYTES = 32 * 1024

# A catalog entry serving skills from this repository names each one as ./skills/<name>, or the
# whole folder as ./skills/. Claude Code loads every skill when none of an entry's listed paths
# exist, so a typo does not fail at install time: it quietly ships the whole folder.
SKILL_PATH = re.compile(r"\./skills/([^/]+)/?")
WHOLE_FOLDER = {"./skills", "./skills/"}

# Only explicit Markdown links are checked. A bare path such as scripts/build.sh in a skill's
# advice usually means the reader's repository, not a file bundled with the skill.
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")

# A reference that names another by its file, as `setup.md` rather than as a link, still sends
# the reader on, and the link check can't see it. Naming facts.md is the one exception: a fact is
# looked up by its ID, not read on to.
MENTION = re.compile(r"(?<![\w./-])([\w-]+\.md)\b")
LINK_TARGET = re.compile(r"\]\([^)\s]+\)")
LOOKUP = "facts.md"

# GitHub splits a table row on every pipe that isn't escaped, inside code spans too, so a command
# with a pipe in a table cell breaks the row. Escaping it doesn't help an agent, which reads the
# raw file and would copy the backslash. Rows are compared with their table's header.
TABLE_CELL = re.compile(r"(?<!\\)\|")
FENCE = re.compile(r"^\s*(```|~~~)")

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

# A merge's conflict markers. Nothing parses Markdown, so markers in it pass every test: a live
# repository shipped them through nine green jobs. Git writes the opening, closing and diff3 base
# markers with a label after a space. A line of seven equals signs is also a Markdown heading
# underline, so it isn't matched, and a conflict always leaves the other two.
CONFLICT_MARKER = re.compile(r"^(?:<{7}|>{7}|\|{7})(?: |$)", re.MULTILINE)
# Everything a commit here carries: the files at the root, and these directories. `.vale` holds
# the tracked vocabulary beside the styles `vale sync` installs. The other dot-directories hold
# tools' caches.
SCANNED_DIRS = (
    "skills",
    "docs",
    "research",
    "src",
    "tests",
    ".claude",
    ".claude-plugin",
    ".github",
    ".vale",
)

# `skillcheck --new` marks each part of a new skill a person still has to write. A skill that
# still holds one isn't finished, so it fails here rather than shipping half-written.
PLACEHOLDER = modules.PLACEHOLDER

# The owner's exclusion list: the claude.ai skills repository sessions don't load, as Claude Code's
# skillOverrides, each with its reason. A listed skill this repository ships would hide it in
# every repository the list is applied to, and this repository applies the list to itself.
EXCLUSIONS = "assets/skill-overrides.json"
SETTINGS = ".claude/settings.json"
OVERRIDE_VALUES = ("on", "name-only", "user-invocable-only", "off")

# Every skill says why it advises what it does, what others do instead, and what each choice
# costs (docs/authoring-a-skill.md). The skill carrying the standard is exempt: the standard
# gives its reasons inline, and it changes only on its own.
RATIONALE = "references/why.md"

# The version the README and the roadmap state for the standard, in the rows of the skill that
# ships it. A copy kept by hand drifts, so each is compared with the standard file's own.
STANDARD_VERSION = re.compile(r"standard\W{0,3}v(\d+\.\d+\.\d+)", re.IGNORECASE)


@dataclass(frozen=True)
class Finding:
    path: str
    rule: str
    message: str


@dataclass
class Report:
    skills: int = 0
    modules: int = 0
    # Every installed skill's description is listed to the model, and the listing has a budget:
    # in one session 50 skills' 26,620 characters left the last 9 with no description at all.
    description_chars: int = 0
    # The same skills as Claude Code lists them: "- name: description" and a newline each.
    listing_chars: int = 0
    # Rows in the skills' references/facts.md, each checked for its source, quote and dates.
    facts: int = 0
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
            f"skillcheck: {self.skills} skill(s), {self.modules} module(s), "
            f"{self.description_chars} description "
            f"characters, {self.facts} fact(s), {catalog}, {roadmap}, {stamp}, "
            f"{len(self.findings)} finding(s)"
        )


def check_repository(root: Path) -> Report:
    report = Report()
    skills = _discover_skills(root, report)
    standards = standard.find(root)
    carriers = {path.parent.parent for path in standards}
    found_facts: list[facts.Fact] = []
    issues = reporting.issues_url(root)
    for skill_dir in skills:
        # A skill made of modules gives its reasons in each module's Why section.
        modular = modules.router(skill_dir) is not None
        _check_skill(skill_dir, report, needs_rationale=not modular and skill_dir not in carriers)
        found_facts += facts.check(root, skill_dir, report.add)
        reporting.check(root, skill_dir, issues, report.add)
    report.facts = len(found_facts)
    _check_fact_ids(found_facts, report)
    facts.check_references(root, skills, {fact.id for fact in found_facts}, report.add)
    _check_catalog(root, skills, report)
    names = {skill.name for skill in skills}
    found_modules = modules.check(root, skills, names, report.add)
    report.modules = len(found_modules)
    _check_roadmap(root, names, report)
    _check_roadmap_modules(root, found_modules, report)
    _check_readme(root, names, report)
    _check_agent_files(root, report)
    _check_conflict_markers(root, report)
    times.check(root, report.add)
    content.check(root, report.add)
    for skill_dir in skills:
        if (skill_dir / EXCLUSIONS).is_file():
            _check_exclusions(root, skill_dir, names, report)
    _check_own_copies(root, names, report)
    if report.listing_chars > LISTING_BUDGET:
        report.add(
            SKILLS_DIR,
            "listing",
            f"the skills' listing is {report.listing_chars} characters; the budget is "
            f"{LISTING_BUDGET}, room for {MAX_SKILLS} skills at 240; grow by modules instead",
        )
    for path in standards:
        report.standard_version = standard.check(root, path, report.add)
        _check_version_copies(root, path.parent.parent.name, report.standard_version, report)
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


def _check_skill(skill_dir: Path, report: Report, needs_rationale: bool) -> None:
    where = f"{SKILLS_DIR}/{skill_dir.name}/SKILL.md"
    _check_hidden_characters(skill_dir.parent.parent, _files_under(skill_dir), report)
    _check_placeholders(skill_dir, report)
    try:
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        data, body = frontmatter.parse(text)
    except (frontmatter.FrontmatterError, UnicodeDecodeError) as exc:
        report.add(where, "frontmatter", str(exc))
        return
    lines = len(text.splitlines())
    if lines >= MAX_SKILL_LINES:
        report.add(where, "size", f"SKILL.md is {lines} lines; keep it under {MAX_SKILL_LINES}")
    if len(text) > MAX_SKILL_CHARS:
        report.add(
            where,
            "size",
            f"SKILL.md is {len(text)} characters, over about 5,000 tokens; keep it within "
            f"{MAX_SKILL_CHARS} and move detail into modules",
        )
    _check_links(skill_dir, body, where, report)
    _check_reference_mentions(skill_dir, report)
    _check_tables(skill_dir, report)
    if needs_rationale and RATIONALE not in _local_links(body):
        report.add(
            where,
            "rationale",
            f"SKILL.md doesn't link {RATIONALE}, which says why the skill advises what it does, "
            "what others do instead, and the trade-offs",
        )
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
    report.listing_chars += len(skill_dir.name) + len(description) + 5
    if len(description) > MAX_DESCRIPTION_LENGTH:
        report.add(
            where,
            "description",
            f"description is {len(description)} characters; the limit is {MAX_DESCRIPTION_LENGTH}",
        )
    elif len(description) > DESCRIPTION_CAP:
        report.add(
            where,
            "listing",
            f"description is {len(description)} characters; this repository's cap is "
            f"{DESCRIPTION_CAP}, so {MAX_SKILLS} skills fit Claude Code's listing",
        )


def _check_placeholders(skill_dir: Path, report: Report) -> None:
    for path in _files_under(skill_dir):
        text = path.read_text(encoding="utf-8", errors="replace")
        count = text.count(PLACEHOLDER)
        if count:
            line = text.count("\n", 0, text.index(PLACEHOLDER)) + 1
            report.add(
                f"{SKILLS_DIR}/{skill_dir.name}/{path.relative_to(skill_dir).as_posix()}",
                "placeholder",
                f"{count} unfinished part(s) marked {PLACEHOLDER}, the first on line {line}",
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


def _check_reference_mentions(skill_dir: Path, report: Report) -> None:
    references = sorted((skill_dir / "references").glob("*.md"))
    names = {path.name for path in references}
    for path in references:
        # Links are the depth check's to report, so their targets are taken out first.
        text = LINK_TARGET.sub("]", path.read_text(encoding="utf-8", errors="replace"))
        named = set()
        for match in MENTION.finditer(text):
            name = match.group(1)
            if name in names and name not in (path.name, LOOKUP) and name not in named:
                named.add(name)
                number = text.count("\n", 0, match.start()) + 1
                report.add(
                    f"{SKILLS_DIR}/{skill_dir.name}/references/{path.name}",
                    "reference-depth",
                    f"line {number} names {name}; keep references one level deep from SKILL.md",
                )


def _check_tables(skill_dir: Path, report: Report) -> None:
    for path in sorted(skill_dir.rglob("*.md")):
        if path == skill_dir / facts.FACTS:
            continue  # its rows' cell counts are the facts check's to report
        header = None
        fenced = False
        for number, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").split("\n"), 1
        ):
            if FENCE.match(line):
                fenced = not fenced
            row = line.strip()
            if fenced or not row.startswith("|"):
                header = None
                continue
            cells = len(TABLE_CELL.split(row[1:].removesuffix("|")))
            if header is None:
                header = cells
            elif cells != header:
                report.add(
                    f"{SKILLS_DIR}/{skill_dir.name}/{path.relative_to(skill_dir).as_posix()}",
                    "table",
                    f"line {number} has {cells} cells and its table {header}; GitHub splits a "
                    "row on every pipe, even inside code",
                )


def _check_optional_fields(data: dict, where: str, report: Report) -> None:
    """The spec's optional fields, in the form claude.ai accepts at upload."""
    if "license" in data and not _is_text(data["license"]):
        report.add(where, "license", "license must name a license or a bundled license file")
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


def _check_exclusions(root: Path, skill_dir: Path, names: set[str], report: Report) -> None:
    where = f"{SKILLS_DIR}/{skill_dir.name}/{EXCLUSIONS}"
    try:
        data = json.loads((skill_dir / EXCLUSIONS).read_text(encoding="utf-8"))
        overrides, reasons = data["skillOverrides"], data["reasons"]
        if not isinstance(overrides, dict) or not isinstance(reasons, dict):
            raise TypeError
    except ValueError, KeyError, TypeError:
        report.add(where, "exclusions", 'needs "skillOverrides" and "reasons", each an object')
        return
    for name, value in overrides.items():
        if not NAME_PATTERN.fullmatch(name) or len(name) > MAX_NAME_LENGTH:
            report.add(where, "exclusions", f"{name!r} isn't a skill name")
        if value not in OVERRIDE_VALUES:
            report.add(where, "exclusions", f"{name}: {value!r} isn't one of {OVERRIDE_VALUES}")
        if name in names:
            report.add(where, "exclusions", f"{name} ships here, and the list would hide it")
        if not _is_text(reasons.get(name)):
            report.add(where, "exclusions", f"{name} has no reason")
    for name in sorted(set(reasons) - set(overrides)):
        report.add(where, "exclusions", f"{name} has a reason but no setting")
    try:
        settings = json.loads((root / SETTINGS).read_text(encoding="utf-8"))
        applied = settings.get("skillOverrides") or {}
    except OSError, ValueError, AttributeError:
        applied = {}
    missing = sorted(set(overrides) - set(applied))
    if missing:
        report.add(
            SETTINGS,
            "exclusions",
            f"skillOverrides lacks {len(missing)} of {where}'s entries: {', '.join(missing)}",
        )


def _check_own_copies(root: Path, names: set[str], report: Report) -> None:
    """Where settings here set skillOverrides, they hide every installed copy of a skill here.

    A session here works on the files under skills/. A copy installed from a release, by an
    upload, a plugin or the cloud hook, would load beside them under the same name.
    """
    try:
        applied = json.loads((root / SETTINGS).read_text(encoding="utf-8"))["skillOverrides"]
        if not isinstance(applied, dict):
            return
    except OSError, ValueError, KeyError, TypeError:
        return
    shown = sorted(name for name in names if applied.get(name) != "off")
    if shown:
        report.add(
            SETTINGS,
            "own-copies",
            f"skillOverrides doesn't turn off {', '.join(shown)}, so a session here would load "
            "an installed copy beside the files being edited",
        )


def _check_agent_files(root: Path, report: Report) -> None:
    files = [root / name for name in AGENT_FILES if (root / name).is_file()]
    for path in files:
        _check_context_size(path, report)
    for directory in AGENT_DIRS:
        if (root / directory).is_dir():
            files += _files_under(root / directory)
    _check_hidden_characters(root, files, report)


def _check_context_size(path: Path, report: Report) -> None:
    data = path.read_bytes()
    lines = len(data.splitlines())
    if lines > MAX_CONTEXT_LINES or len(data) > MAX_CONTEXT_BYTES:
        report.add(
            path.name,
            "size",
            f"{path.name} is {lines} lines and {len(data)} bytes; keep it within "
            f"{MAX_CONTEXT_LINES} lines and {MAX_CONTEXT_BYTES} bytes",
        )


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


def _check_conflict_markers(root: Path, report: Report) -> None:
    files = sorted(p for p in root.iterdir() if p.is_file())
    for directory in SCANNED_DIRS:
        if (root / directory).is_dir():
            files += _files_under(root / directory)
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue  # a binary file is merged whole, never marked
        match = CONFLICT_MARKER.search(text)
        if match:
            number = text.count("\n", 0, match.start()) + 1
            report.add(
                path.relative_to(root).as_posix(),
                "conflict",
                f"line {number} is a merge's conflict marker",
            )


def _check_version_copies(root: Path, skill: str, version: str, report: Report) -> None:
    for name in (README, ROADMAP):
        path = root / name
        if not path.is_file():
            continue
        for table in _skill_tables(path.read_text(encoding="utf-8")):
            for row_name, cells in table:
                if row_name != skill:
                    continue
                for stated in STANDARD_VERSION.findall(" | ".join(cells.values())):
                    if stated != version:
                        report.add(
                            name,
                            "standard",
                            f"the `{skill}` row says standard v{stated}; the file is v{version}",
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


def _check_fact_ids(found: list[facts.Fact], report: Report) -> None:
    # One ID, one fact, across the repository, so a module can move between skills safely.
    first: dict[str, facts.Fact] = {}
    for fact in found:
        if fact.id in first:
            report.add(
                fact.path,
                "facts",
                f"line {fact.line}: `{fact.id}` is already defined in {first[fact.id].path}",
            )
        else:
            first[fact.id] = fact


def _skill_tables(text: str, first: str = "Skill") -> list[list[tuple[str, dict[str, str]]]]:
    """Every Markdown table whose first header cell is ``first``, as rows of (name, cells)."""
    lines = text.splitlines()
    tables = []
    index = 0
    while index < len(lines) - 1:
        header = _cells(lines[index])
        separator = lines[index + 1].strip()
        if header and header[0] == first and "-" in separator and set(separator) <= set("|-: "):
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


def _check_roadmap_modules(root: Path, found: list[modules.Module], report: Report) -> None:
    # Each built module has a shipped row naming its home skill, and each shipped row has its
    # module, so the roadmap can't drift from the routers. `skillcheck --move` keeps the row.
    path = root / ROADMAP
    if not path.is_file():
        return
    rows = [
        row for table in _skill_tables(path.read_text(encoding="utf-8"), "Module") for row in table
    ]
    for name, count in sorted(Counter(name for name, _ in rows).items()):
        if count > 1:
            report.add(ROADMAP, "roadmap", f"module `{name}` is listed {count} times")
    homes = {name: _ticked(cells.get("Skill", "")) for name, cells in rows}
    listed = dict(rows)
    built = {module.name: module for module in found}
    for name, cells in rows:
        status = cells.get("Status", "")
        home = homes[name]
        if status not in ROADMAP_STATUSES:
            report.add(
                ROADMAP,
                "roadmap",
                f"module `{name}` has status {status!r}; use one of {', '.join(ROADMAP_STATUSES)}",
            )
        elif status == "shipped" and (name not in built or built[name].skill != home):
            report.add(
                ROADMAP,
                "roadmap",
                f"module `{name}` is marked shipped in `{home}`, which doesn't route it",
            )
    for name, module in sorted(built.items()):
        where = f"{SKILLS_DIR}/{module.skill}/SKILL.md"
        cells = listed.get(name)
        if cells is None or cells.get("Status") != "shipped":
            report.add(where, "roadmap", f"module `{name}` is not listed as shipped in {ROADMAP}")
        elif homes[name] != module.skill:
            report.add(where, "roadmap", f"{ROADMAP} gives module `{name}` another skill")


def _ticked(cell: str) -> str:
    match = TICKED.search(cell)
    return match.group(1) if match else ""


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
