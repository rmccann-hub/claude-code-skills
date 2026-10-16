"""``skillcheck --move MODULE SKILL``: give a module a new home skill (ROADMAP.md, rule 5).

A module holds its own rules, reasons, facts and sources, and its trigger tests are keyed by its
name, so a move touches four places: the module's file, the router row in each skill, the
module's row in ROADMAP.md, and the record of moves. Everything is checked before anything is
written, so a refused move changes nothing.
"""

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from skillcheck.core import modules
from skillcheck.core.checks import ROADMAP, SKILLS_DIR, TICKED

RECORD = "docs/module-moves.md"
RECORD_HEADER = """\
# Module moves

Every module moved between skills, and every skill renamed or removed, newest last. Old copies
of a skill on claude.ai, and what depends on them, are found from here. `skillcheck --move`
adds a module's row. A skill's rename or removal is added by hand, with `none` as its module,
and `none` in To for a removal. The rules are in the roadmap's
[*How skills are structured*](../ROADMAP.md#how-skills-are-structured).

| Date | Module | From | To |
|---|---|---|---|
"""


class MoveError(Exception):
    """The move can't be made as asked, and nothing was written."""


@dataclass(frozen=True)
class _Plan:
    module: modules.Module
    target_dir: Path
    target_file: Path
    roadmap_line: int | None


def move(root: Path, name: str, target: str, today: date | None = None) -> list[str]:
    """Move module ``name`` into skill ``target``; return what changed, one line each."""
    plan = _plan(root, name, target)
    module = plan.module
    source_skill = plan.module.path.parent.parent / "SKILL.md"
    plan.target_file.parent.mkdir(exist_ok=True)
    _remove_line(source_skill, module.row)
    modules.add_row(plan.target_dir / "SKILL.md", module.row)
    plan.target_file.write_bytes(module.path.read_bytes())
    module.path.unlink()
    changed = [
        f"moved {_rel(root, module.path)} to {_rel(root, plan.target_file)}",
        f"moved the router row from {module.skill} to {target}",
    ]
    if plan.roadmap_line is not None:
        _set_roadmap_skill(root / ROADMAP, plan.roadmap_line, name, target)
        changed.append(f"set module `{name}`'s skill to `{target}` in {ROADMAP}")
    _record(root, name, module.skill, target, today or date.today())
    changed.append(f"recorded the move in {RECORD}")
    routed = modules.router(source_skill.parent)
    if routed is not None and not routed[0]:
        changed.append(f"{module.skill} has no modules left: remove it, or route another module")
    return changed


def _plan(root: Path, name: str, target: str) -> _Plan:
    skills_root = root / SKILLS_DIR
    homes = []
    for skill_dir in sorted(path for path in skills_root.glob("*") if path.is_dir()):
        if not (skill_dir / "SKILL.md").is_file():
            continue
        routed = modules.router(skill_dir)
        if routed is not None:
            homes += [module for module in routed[0] if module.name == name]
    if not homes:
        raise MoveError(f"no skill routes a module `{name}`")
    if len(homes) > 1:
        raise MoveError(
            f"`{name}` is routed by {', '.join(m.skill for m in homes)}; fix that first"
        )
    (module,) = homes
    if not module.path.is_file():
        raise MoveError(f"`{name}` has no file at {_rel(root, module.path)}")
    if module.skill == target:
        raise MoveError(f"`{name}` is already in `{target}`")
    target_dir = skills_root / target
    if not (target_dir / "SKILL.md").is_file():
        raise MoveError(
            f"there's no skill `{target}`; make it with `skillcheck --new {target}` first"
        )
    if modules.router(target_dir) is None:
        raise MoveError(f"`{target}` has no Modules section to route `{name}`")
    target_file = target_dir / "references" / f"{name}.md"
    if target_file.exists():
        raise MoveError(f"{_rel(root, target_file)} already exists")
    return _Plan(module, target_dir, target_file, _roadmap_line(root / ROADMAP, name))


def _remove_line(path: Path, line: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    lines = [text for text in lines if text.rstrip("\n") != line]
    path.write_text("".join(lines), encoding="utf-8")


def _roadmap_line(path: Path, name: str) -> int | None:
    if not path.is_file():
        return None
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        row = modules.cells(line) if line.startswith(f"| `{name}` |") else []
        if len(row) > 1 and TICKED.fullmatch(row[1]):
            return index
    return None


def _set_roadmap_skill(path: Path, index: int, name: str, new: str) -> None:
    # The row starts | `module` | `skill` |, which _roadmap_line has checked.
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    prefix = f"| `{name}` |"
    rest = lines[index][len(prefix) :]
    lines[index] = f"{prefix} `{new}` |{rest[rest.index('|') + 1 :]}"
    path.write_text("".join(lines), encoding="utf-8")


def _record(root: Path, name: str, old: str, new: str, today: date) -> None:
    path = root / RECORD
    if not path.is_file():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(RECORD_HEADER, encoding="utf-8")
    text = path.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(f"{text}| {today.isoformat()} | `{name}` | `{old}` | `{new}` |\n", "utf-8")


def _rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()
