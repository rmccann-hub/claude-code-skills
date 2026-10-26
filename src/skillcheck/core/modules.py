"""Skills made of modules (ROADMAP.md, How skills are structured).

A skill whose SKILL.md has a "Modules" section is made of modules. That section's table is the
router: each row names a module and says what to read it for, and each module is one file,
``references/<module>.md``, holding everything it needs under fixed headings. Because a module
carries its own rules, reasons, facts and sources, moving it to another skill is moving one
file and one row, which ``skillcheck --move`` does.
"""

import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

ROUTER_HEADING = "Modules"
ROUTER_COLUMNS = ("Module", "Read it for")
# Every module has these, so a module moved elsewhere takes its whole story with it.
SECTIONS = ("Rules", "Mistakes", "Audit", "Why", "Facts", "Sources")
FIXTURES = "tests/fixtures/modules"
# claude.ai's file viewer keeps about 8,000 characters from each end of a longer file and drops
# the middle, which the owner measured on 2026-10-26 (docs/decisions.md). Claude Code reads files
# whole, but a module must work on both.
MAX_CHARACTERS = 16_000
# The mark `skillcheck --new-module` leaves on each part still to be written.
PLACEHOLDER = "TODO(new-skill)"
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
ROW_NAME = re.compile(r"\[`([^`]+)`\]\(([^)\s]+)\)")
HEADING = re.compile(r"^## (.+?)\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
CELL = re.compile(r"(?<!\\)\|")

Add = Callable[[str, str, str], None]


@dataclass(frozen=True)
class Module:
    name: str
    skill: str
    path: Path
    # The router's line for this module, kept whole so a move carries it unchanged.
    row: str


def sections(text: str) -> dict[str, list[tuple[int, str]]]:
    """Each level-two heading's lines, numbered from 1, with fenced code left out of the search."""
    found: dict[str, list[tuple[int, str]]] = {}
    current: list[tuple[int, str]] | None = None
    fenced = False
    for number, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            fenced = not fenced
        heading = None if fenced else HEADING.match(line)
        if heading:
            current = found.setdefault(heading.group(1), [])
        elif current is not None:
            current.append((number, line))
    return found


def cells(line: str) -> list[str]:
    return [cell.strip() for cell in CELL.split(line.strip()[1:].removesuffix("|"))]


def router(skill_dir: Path) -> tuple[list[Module], list[str]] | None:
    """The skill's modules and the router's problems, or None for a skill without a router."""
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    lines = sections(text).get(ROUTER_HEADING)
    if lines is None:
        return None
    modules: list[Module] = []
    problems: list[str] = []
    table = [(number, line) for number, line in lines if line.startswith("|")]
    if not table or tuple(cells(table[0][1])) != ROUTER_COLUMNS:
        problems.append(
            f"the {ROUTER_HEADING} section has no table headed {' | '.join(ROUTER_COLUMNS)}"
        )
        return modules, problems
    for number, line in table[2:]:
        first = cells(line)[0]
        match = ROW_NAME.fullmatch(first)
        if match is None or not NAME.fullmatch(match.group(1)):
            problems.append(f"line {number}: a router row starts with [`name`](references/name.md)")
            continue
        name, target = match.groups()
        if target != f"references/{name}.md":
            problems.append(f"line {number}: `{name}` links {target}, not references/{name}.md")
            continue
        if any(module.name == name for module in modules):
            problems.append(f"line {number}: `{name}` is routed twice")
            continue
        modules.append(Module(name, skill_dir.name, skill_dir / target, line))
    if not modules:
        problems.append("the router lists no modules")
    return modules, problems


def check(root: Path, skills: list[Path], skill_names: set[str], add: Add) -> list[Module]:
    """Check every router, module file and module fixture; return every module found."""
    found: list[Module] = []
    for skill_dir in skills:
        routed = router(skill_dir)
        if routed is None:
            continue
        modules, problems = routed
        where = f"skills/{skill_dir.name}/SKILL.md"
        for message in problems:
            add(where, "modules", message)
        for module in modules:
            _check_module(root, module, add)
        _check_unrouted(root, skill_dir, {module.path for module in modules}, add)
        found += modules
    _check_names(found, skill_names, add)
    return found


def _check_module(root: Path, module: Module, add: Add) -> None:
    where = module.path.relative_to(root).as_posix()
    if not module.path.is_file():
        add(f"skills/{module.skill}/SKILL.md", "modules", f"`{module.name}` has no file at {where}")
        return
    text = module.path.read_text(encoding="utf-8")
    headings = sections(text)
    missing = [name for name in SECTIONS if name not in headings]
    if missing:
        add(where, "modules", f"missing the section(s) {', '.join(missing)}")
    if len(text) > MAX_CHARACTERS:
        add(
            where,
            "modules",
            f"{len(text):,} characters: claude.ai drops the middle of a file over "
            f"{MAX_CHARACTERS:,}, so trim it or split it",
        )
    _check_fixture(root, module, add)


def _check_fixture(root: Path, module: Module, add: Add) -> None:
    path = root / FIXTURES / f"{module.name}.json"
    where = path.relative_to(root).as_posix()
    if not path.is_file():
        add(where, "modules", f"`{module.name}` has no trigger tests")
        return
    try:
        cases = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add(where, "modules", f"not JSON: {exc}")
        return
    shaped = isinstance(cases, list) and all(
        isinstance(case, dict)
        and isinstance(case.get("query"), str)
        and isinstance(case.get("should_trigger"), bool)
        for case in cases
    )
    if not shaped:
        add(where, "modules", 'a list of {"query": text, "should_trigger": true or false}')
    elif any(PLACEHOLDER in case["query"] for case in cases):
        add(where, "placeholder", f"a request still marked {PLACEHOLDER}")
    elif {case["should_trigger"] for case in cases} != {True, False}:
        add(
            where,
            "modules",
            "needs requests that should reach the module and near misses that shouldn't",
        )


def _check_unrouted(root: Path, skill_dir: Path, routed: set[Path], add: Add) -> None:
    references = skill_dir / "references"
    if not references.is_dir():
        return
    for path in sorted(references.glob("*.md")):
        if path not in routed:
            add(
                path.relative_to(root).as_posix(),
                "modules",
                "no router row reads this file; a skill made of modules holds only modules",
            )


def _check_names(found: list[Module], skill_names: set[str], add: Add) -> None:
    homes: dict[str, str] = {}
    for module in found:
        where = f"skills/{module.skill}/SKILL.md"
        if module.name in homes:
            add(where, "modules", f"`{module.name}` is also a module of `{homes[module.name]}`")
        else:
            homes[module.name] = module.skill
        if module.name in skill_names and module.name != module.skill:
            add(where, "modules", f"`{module.name}` is also the name of a skill")


def add_row(skill_md: Path, row: str) -> None:
    """Put ``row`` after the router table's last line, so the table stays one table."""
    text = skill_md.read_text(encoding="utf-8")
    table = [n for n, line in sections(text)[ROUTER_HEADING] if line.startswith("|")]
    lines = text.splitlines(keepends=True)
    if not lines[table[-1] - 1].endswith("\n"):
        lines[table[-1] - 1] += "\n"
    lines.insert(table[-1], row + "\n")
    skill_md.write_text("".join(lines), encoding="utf-8")
