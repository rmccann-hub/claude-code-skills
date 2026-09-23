"""The standard's own mechanical checks, run on the copy this repository ships.

PROJECT-BOOTSTRAP-AND-AUDIT lists them under "Validating a Change to This Standard" as Test G:
properties of the file checkable by reading it, each added because it once failed. Its version
history shows them run by hand. Here they run in CI on every change.
"""

import re
from collections import Counter
from collections.abc import Callable
from pathlib import Path

from skillcheck.core import frontmatter

FILENAME = re.compile(r"PROJECT-BOOTSTRAP-AND-AUDIT-v(\d+\.\d+\.\d+)\.md")
FENCE = re.compile(r"^\s*```")
HEADING = re.compile(r"^#{1,6} ")
DIMENSION = re.compile(r"^### (\d+)\. ")
WAIT = re.compile(r"^## Phase .*\*\*WAIT\*\*")
PHASE = re.compile(r"^phase: (\d+)$", re.MULTILINE)
VERSION_ENTRY = re.compile(r"^\*\*(\d+\.\d+\.\d+)\*\*")
PHASES = list(range(10))
DIMENSIONS = list(range(1, 11))
WAITS = 2

Add = Callable[[str, str, str], None]


def find(root: Path) -> list[Path]:
    """Every copy of the standard carried as a skill reference, by filename."""
    return sorted(
        path
        for path in (root / "skills").glob("*/references/*.md")
        if FILENAME.fullmatch(path.name)
    )


def check(root: Path, path: Path, add: Add) -> str:
    """Check one copy and return its version: the frontmatter's, or failing that the filename's."""
    where = path.relative_to(root).as_posix()
    file_version = FILENAME.fullmatch(path.name).group(1)
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")

    fences = [number for number, line in enumerate(lines, 1) if FENCE.match(line)]
    if len(fences) % 2:
        # An unclosed fence swallows everything after it, so nothing below would be reliable.
        add(where, "standard", f"code fences are unbalanced: {len(fences)} fence lines")
        return file_version
    inside = _fenced(lines)
    prose = [(number, line) for number, line in enumerate(lines, 1) if not inside[number - 1]]

    _check_constraints(prose, where, add)
    _check_tables(lines, inside, where, add)
    _check_counts(prose, where, add)
    _check_phase_blocks(lines, where, add)
    _check_headings(prose, where, add)
    _check_whitespace(prose, where, add)
    version = _check_versions(text, prose, file_version, where, add)
    _check_skill_version(root, path.parent.parent, file_version, add)
    return version


def _fenced(lines: list[str]) -> list[bool]:
    """For each line, whether it is part of a fenced block, the fence lines included."""
    inside, state = [], False
    for line in lines:
        if FENCE.match(line):
            inside.append(True)
            state = not state
        else:
            inside.append(state)
    return inside


def _check_constraints(prose: list[tuple[int, str]], where: str, add: Add) -> None:
    depth = opened = closed = 0
    for number, line in prose:
        if line.strip() == "<constraints>":
            opened += 1
            depth += 1
            if depth > 1:
                add(where, "standard", f"<constraints> opens inside another at line {number}")
        elif line.strip() == "</constraints>":
            closed += 1
            depth = max(depth - 1, 0)
    if opened != closed:
        add(where, "standard", f"<constraints> opens {opened} times and closes {closed} times")


def _check_tables(lines: list[str], inside: list[bool], where: str, add: Add) -> None:
    # A comment between two rows splits the table, and every row after it renders as raw text.
    for index in range(1, len(lines) - 1):
        if (
            not inside[index]
            and lines[index].lstrip().startswith("<!--")
            and lines[index - 1].lstrip().startswith("|")
            and lines[index + 1].lstrip().startswith("|")
        ):
            add(where, "standard", f"HTML comment inside a table at line {index + 1}")


def _check_counts(prose: list[tuple[int, str]], where: str, add: Add) -> None:
    dimensions = [int(match.group(1)) for _, line in prose if (match := DIMENSION.match(line))]
    if dimensions != DIMENSIONS:
        add(where, "standard", f"dimensions are numbered {dimensions}; expected 1 to 10")
    waits = sum(1 for _, line in prose if WAIT.match(line))
    if waits != WAITS:
        add(where, "standard", f"{waits} waits; the standard has exactly {WAITS}")


def _check_phase_blocks(lines: list[str], where: str, add: Add) -> None:
    phases = []
    index = 0
    while index < len(lines):
        if lines[index].strip() == "```yaml":
            end = index + 1
            while end < len(lines) and not FENCE.match(lines[end]):
                end += 1
            body = "\n".join(lines[index + 1 : end])
            match = PHASE.search(body)
            if match:
                phases.append(int(match.group(1)))
                if not re.search(r"^notes:", body, re.MULTILINE):
                    add(where, "standard", f"the phase {match.group(1)} block has no notes field")
            index = end
        index += 1
    if sorted(phases) != PHASES:
        add(where, "standard", f"phase blocks are {sorted(phases)}; expected one each for 0 to 9")


def _check_headings(prose: list[tuple[int, str]], where: str, add: Add) -> None:
    headings = Counter(line.strip() for _, line in prose if HEADING.match(line))
    for heading, count in sorted(headings.items()):
        if count > 1:
            add(where, "standard", f"duplicate heading {heading!r}, {count} times")


def _check_whitespace(prose: list[tuple[int, str]], where: str, add: Add) -> None:
    trailing = [number for number, line in prose if line != line.rstrip()]
    if trailing:
        add(
            where,
            "standard",
            f"trailing whitespace on {len(trailing)} line(s), first at line {trailing[0]}",
        )
    # Consecutive in the file, not in this list: a fenced block between two blank lines is
    # missing from it, and would otherwise join the blanks on either side into one run.
    blank_runs, run, previous = [], 0, 0
    for number, line in prose:
        run = run + 1 if line == "" and number == previous + 1 else int(line == "")
        previous = number
        if run == 3:
            blank_runs.append(number - 2)
    if blank_runs:
        add(
            where,
            "standard",
            f"{len(blank_runs)} run(s) of three or more blank lines, first at line {blank_runs[0]}",
        )


def _check_versions(
    text: str, prose: list[tuple[int, str]], file_version: str, where: str, add: Add
) -> str:
    try:
        data, _ = frontmatter.parse(text)
    except frontmatter.FrontmatterError as exc:
        add(where, "standard", f"frontmatter: {exc}")
        return file_version
    metadata = data.get("metadata")
    version = str(metadata.get("version")) if isinstance(metadata, dict) else "none"
    if version != file_version:
        add(where, "standard", f"frontmatter says {version}; the filename says {file_version}")

    # The version history: the entries under "## Entries", up to the next heading at that level.
    entries, collecting = [], False
    for _, line in prose:
        if line.strip() == "## Entries":
            collecting = True
        elif collecting and line.startswith(("# ", "## ")):
            break
        elif collecting and (match := VERSION_ENTRY.match(line)):
            entries.append(match.group(1))
    if not entries:
        add(where, "standard", "the version history (## Entries) holds no versions")
        return version
    if entries[0] != version:
        add(
            where,
            "standard",
            f"the version history starts at {entries[0]}; the frontmatter says {version}",
        )
    for newer, older in zip(entries, entries[1:], strict=False):
        if _key(older) >= _key(newer):
            add(
                where,
                "standard",
                f"the version history is not newest-first: {newer} comes before {older}",
            )
            break
    return version


def _check_skill_version(root: Path, skill_dir: Path, file_version: str, add: Add) -> None:
    skill_md = skill_dir / "SKILL.md"
    try:
        data, _ = frontmatter.parse(skill_md.read_text(encoding="utf-8"))
    except OSError, frontmatter.FrontmatterError:
        return  # the skill checks already report an unreadable SKILL.md
    metadata = data.get("metadata")
    shipped = metadata.get("standard-version") if isinstance(metadata, dict) else None
    if shipped is not None and str(shipped) != file_version:
        add(
            skill_md.relative_to(root).as_posix(),
            "standard",
            f"SKILL.md says standard-version {shipped}; the reference file is v{file_version}",
        )


def _key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))
