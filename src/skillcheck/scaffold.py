"""A new skill's or module's starting files, in the shape docs/authoring-a-skill.md asks for.

``skillcheck --new SKILL`` writes a skill made of modules with an empty router, and
``skillcheck --new-module MODULE SKILL`` adds a module to it: its file, its router row and its
trigger tests. Every part a person still has to write is marked with ``PLACEHOLDER``, and the
placeholder rule fails a skill that still holds one, so a skeleton can't ship by accident.
"""

import json
from pathlib import Path

from skillcheck.core import modules
from skillcheck.core.checks import MAX_NAME_LENGTH, NAME_PATTERN, PLACEHOLDER, SKILLS_DIR


class ScaffoldError(Exception):
    """The skill or module can't be created as asked, and nothing was written."""


def create(root: Path, name: str) -> list[Path]:
    """Write a new skill, made of modules, under ``root``; return its paths, relative to it."""
    _check_name(name)
    if (root / SKILLS_DIR / name).exists():
        raise ScaffoldError(f"already there: {SKILLS_DIR}/{name}")
    path = f"{SKILLS_DIR}/{name}/SKILL.md"
    title = name.replace("-", " ").capitalize()
    return _write(root, {path: _SKILL.format(name=name, title=title, todo=PLACEHOLDER)})


def create_module(root: Path, name: str, skill: str) -> list[Path]:
    """Add module ``name`` to ``skill``: its file, router row and trigger tests."""
    _check_name(name)
    skill_dir = root / SKILLS_DIR / skill
    if not (skill_dir / "SKILL.md").is_file():
        raise ScaffoldError(f"there's no skill `{skill}`; make it with --new {skill} first")
    if modules.router(skill_dir) is None:
        raise ScaffoldError(f"`{skill}` has no {modules.ROUTER_HEADING} section to route it")
    for other in sorted((root / SKILLS_DIR).glob("*/SKILL.md")):
        routed = modules.router(other.parent)
        if routed is not None and any(module.name == name for module in routed[0]):
            raise ScaffoldError(f"`{name}` is already a module of `{other.parent.name}`")
        if other.parent.name == name and name != skill:
            raise ScaffoldError(f"`{name}` is already the name of a skill")
    module_path = f"{SKILLS_DIR}/{skill}/references/{name}.md"
    fixture = f"{modules.FIXTURES}/{name}.json"
    taken = [path for path in (module_path, fixture) if (root / path).exists()]
    if taken:
        raise ScaffoldError(f"already there: {', '.join(taken)}")
    triggers = [
        {"query": f"{PLACEHOLDER} a request this module should answer", "should_trigger": True},
        {"query": f"{PLACEHOLDER} another one, worded differently", "should_trigger": True},
        {"query": f"{PLACEHOLDER} a near miss another module takes", "should_trigger": False},
    ]
    title = name.replace("-", " ").capitalize()
    written = _write(
        root,
        {
            module_path: _MODULE.format(title=title, todo=PLACEHOLDER),
            fixture: json.dumps(triggers, indent=2) + "\n",
        },
    )
    row = f"| [`{name}`](references/{name}.md) | {PLACEHOLDER} the requests it answers |"
    modules.add_row(skill_dir / "SKILL.md", row)
    return [Path(f"{SKILLS_DIR}/{skill}/SKILL.md"), *written]


def _check_name(name: str) -> None:
    if len(name) > MAX_NAME_LENGTH or not NAME_PATTERN.fullmatch(name):
        raise ScaffoldError(
            f"{name!r} must be 1-{MAX_NAME_LENGTH} lowercase letters, digits and single hyphens"
        )


def _write(root: Path, files: dict[str, str]) -> list[Path]:
    written = []
    for path, text in files.items():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        written.append(Path(path))
    return written


_SKILL = """\
---
name: {name}
description: "{todo} When to load this skill and what it does, in the third person, its main \
use first, with the words a request would use, in 250 characters or fewer."
license: Apache-2.0
metadata:
  reviewed: "{todo} the date of its review, YYYY-MM-DD"
---

# {title}

{todo} One paragraph: the situations that load this skill, and which neighboring skill takes
what it doesn't. Where the standard already rules, such as on budgets, layouts, versioning,
secrets and dependencies, name its section rather than restating it.

## What applies to every module

{todo} The rules every request here meets, whichever module it reads, each in a line or two.

## Modules

Read the module that fits the request, and each one a request spans. Each holds its rules,
mistakes, audit checks, reasons, dated facts and sources.

| Module | Read it for |
|---|---|
"""

_MODULE = """\
# {title}

Read this for {todo} the requests this module answers.

{todo} One paragraph on its scope, naming the modules that take what it doesn't.

## Rules

{todo} The rules that matter most, each in a line or two, its reason under Why.

## Mistakes

- **{todo} The mistake.** What it breaks, and what to do instead, including what AI assistants
  get wrong.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| {todo} | | | |

## Why

### {todo} The first rule

- **The advice:** what to do.
- **The reason:** what goes wrong without it, with the case that showed it.
- **What others do, and why:** the projects that choose differently.
- **What it costs:** each choice's price.
- **When to choose differently:** the cases where the other choice is right.

## Facts

Versions, dates and defaults, each named elsewhere in this module by its ID. Checked {todo}
YYYY-MM-DD.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|

## Sources

Every source, with its license and how this module uses it: quoted, adapted with a notice, or
stated in our own words with a link.

| Source | Used for | License |
|---|---|---|
| {todo} | | |
"""
