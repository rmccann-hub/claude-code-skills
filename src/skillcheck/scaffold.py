"""A new skill's starting files, in the shape docs/authoring-a-skill.md asks for.

Every part a person still has to write is marked with ``PLACEHOLDER``, and the placeholder rule in
the checks fails a skill that still holds one, so a skeleton can't ship by accident.
"""

import json
from pathlib import Path

from skillcheck.core.checks import MAX_NAME_LENGTH, NAME_PATTERN, PLACEHOLDER, SKILLS_DIR

TRIGGERS_DIR = "tests/fixtures/skills"


class ScaffoldError(Exception):
    """The skill can't be created as asked, and nothing was written."""


def create(root: Path, name: str) -> list[Path]:
    """Write a new skill's files under ``root`` and return their paths, relative to it."""
    if len(name) > MAX_NAME_LENGTH or not NAME_PATTERN.fullmatch(name):
        raise ScaffoldError(
            f"{name!r} must be 1-{MAX_NAME_LENGTH} lowercase letters, digits and single hyphens"
        )
    files = _files(name)
    taken = [path for path in files if (root / path).exists()]
    if (root / SKILLS_DIR / name).exists():
        taken.insert(0, f"{SKILLS_DIR}/{name}")
    if taken:
        raise ScaffoldError(f"already there: {', '.join(taken)}")
    written = []
    for path, text in files.items():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        written.append(Path(path))
    return written


def _files(name: str) -> dict[str, str]:
    title = name.replace("-", " ").capitalize()
    base = f"{SKILLS_DIR}/{name}"
    triggers = [
        {"query": f"{PLACEHOLDER} a request this skill should take", "should_trigger": True},
        {"query": f"{PLACEHOLDER} another one, worded differently", "should_trigger": True},
        {"query": f"{PLACEHOLDER} a near miss a neighboring skill takes", "should_trigger": False},
    ]
    return {
        f"{base}/SKILL.md": _SKILL.format(name=name, title=title, todo=PLACEHOLDER),
        f"{base}/references/why.md": _WHY.format(todo=PLACEHOLDER),
        f"{base}/references/facts.md": _FACTS.format(todo=PLACEHOLDER),
        f"{base}/references/audit.md": _AUDIT.format(todo=PLACEHOLDER),
        f"{base}/references/mistakes.md": _MISTAKES.format(todo=PLACEHOLDER),
        f"{base}/references/sources.md": _SOURCES.format(todo=PLACEHOLDER),
        f"{TRIGGERS_DIR}/{name}.json": json.dumps(triggers, indent=2) + "\n",
    }


_SKILL = """\
---
name: {name}
description: "{todo} What the skill does and when to use it, in the third person, with the \
words a request would use rather than a keyword list, in 1,024 characters or fewer."
license: Apache-2.0
metadata:
  reviewed: "{todo} the date of its review, YYYY-MM-DD"
---

# {title}

{todo} One paragraph: what this skill covers, and which neighboring skill takes what it
doesn't. Where the standard already rules, such as on budgets, layouts, versioning, secrets and
dependencies, name its section rather than restating it.

## The rules that matter most

{todo} The handful of rules a reader must not miss, each in a line or two, with its reason in
the rationale file below.

## How to check

{todo} The commands that check work in this area, each with what its output should show.

## How to audit

Every check, with what to look for, its severity and its fix, is in
[references/audit.md](references/audit.md).

## Where to go next

- Why each rule is what it is, what other projects do, and what each choice costs:
  [references/why.md](references/why.md)
- Versions, support dates and defaults, each with its source and the date it was checked:
  [references/facts.md](references/facts.md)
- What goes wrong, including what AI assistants get wrong:
  [references/mistakes.md](references/mistakes.md)
- Every source, with its license: [references/sources.md](references/sources.md)
"""

_WHY = """\
# Why: the reasons behind each rule

Read this when a rule's reason matters, when a project does it differently, or when you're
deciding whether to follow the advice here.

## {todo} The first rule

- **The advice:** what to do.
- **The reason:** what goes wrong without it, with the case that showed it.
- **What others do, and why:** the projects that choose differently.
- **What it costs:** each choice's price.
- **When to choose differently:** the cases where the other choice is right.
"""

_FACTS = """\
# Facts: versions, dates and defaults

Read this when a version, date or default matters. Every other file here names a fact by its
ID instead of repeating its value, so there's one copy to update. Each fact carries its source,
a short quote, the date it was checked and a date to check it again by.

Checked {todo} YYYY-MM-DD.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
"""

_AUDIT = """\
# Audit: every check

Read this when auditing work in this area. Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| {todo} | | | |
"""

_MISTAKES = """\
# Mistakes: what goes wrong, including what AI assistants get wrong

Read this before risky work in this area, or when you're checking advice an assistant gave.
Facts are named by their ID.

- **{todo} The mistake.** What it breaks, and what to do instead.
"""

_SOURCES = """\
# Sources

Every source this skill rests on, with its license and how the skill may use it: quoted,
adapted with a notice, or stated in our own words with a link.

| Source | Used for | License |
|---|---|---|
| {todo} | | |
"""
