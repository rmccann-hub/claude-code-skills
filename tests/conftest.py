import json
from pathlib import Path

import pytest

DEFAULT_DESCRIPTION = "A fixture skill for tests. Use when testing."
DEFAULT_FRONTMATTER = "name: {name}\ndescription: " + DEFAULT_DESCRIPTION + "\n"
RATIONALE_LINK = "\nWhy: [the reasons](references/why.md).\n"
# Every skill says what to do when something in it is wrong (core/reporting.py).
REPORTING = "\n## When something here is wrong\n\nSay so.\n"

# A module that passes every rule: each section, and a fact named by its ID.
MODULE_TEXT = """\
# {title}

Read this for {name} requests.

## Rules

Follow the rule (fact `{name}-fact`).

## Mistakes

- **A mistake.** Do the other thing.

## Audit

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| One | Something | GAP | Fix it |

## Why

The reason.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `{name}-fact` | A fact | [p](https://example.com/{name}) | "a quote" | 2026-10-01 | 2027-04-01 |

## Sources

| Source | Used for | License |
|---|---|---|
| A page | The fact | CC0 |
"""
TRIGGERS = [
    {"query": "a request it answers", "should_trigger": True},
    {"query": "a near miss", "should_trigger": False},
]


class RepoBuilder:
    """Builds a throwaway repository under tmp_path. Every skill here is synthetic."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def skill(
        self,
        directory: str,
        frontmatter: str | None = None,
        body: str = "Body.\n",
        rationale: bool = True,
    ) -> Path:
        """A skill that passes every rule, unless told to leave out its rationale file."""
        if frontmatter is None:
            frontmatter = DEFAULT_FRONTMATTER.format(name=directory)
        skill_dir = self.skill_file(
            directory,
            f"---\n{frontmatter}---\n\n{body}{RATIONALE_LINK if rationale else ''}{REPORTING}",
        )
        if rationale:
            (skill_dir / "references").mkdir()
            (skill_dir / "references" / "why.md").write_text("# Why\n", encoding="utf-8")
        return skill_dir

    def skill_file(self, directory: str, text: str) -> Path:
        skill_dir = self.root / "skills" / directory
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(text, encoding="utf-8")
        return skill_dir

    def modular_skill(self, directory: str, *module_names: str) -> Path:
        """A skill made of modules, each passing every rule, with its trigger tests."""
        rows = "".join(
            f"| [`{name}`](references/{name}.md) | {name} requests |\n" for name in module_names
        )
        skill_dir = self.skill_file(
            directory,
            f"---\n{DEFAULT_FRONTMATTER.format(name=directory)}---\n\n# Title\n\n"
            f"## Modules\n\n| Module | Read it for |\n|---|---|\n{rows}{REPORTING}",
        )
        (skill_dir / "references").mkdir()
        for name in module_names:
            self.module(skill_dir, name)
        return skill_dir

    def module(self, skill_dir: Path, name: str, text: str | None = None) -> Path:
        path = skill_dir / "references" / f"{name}.md"
        title = name.replace("-", " ").capitalize()
        path.write_text(text or MODULE_TEXT.format(name=name, title=title), encoding="utf-8")
        fixtures = self.root / "tests" / "fixtures" / "modules"
        fixtures.mkdir(parents=True, exist_ok=True)
        (fixtures / f"{name}.json").write_text(json.dumps(TRIGGERS), encoding="utf-8")
        return path

    def roadmap(self, skills: dict[str, str], modules: dict[str, tuple[str, str]]) -> None:
        """ROADMAP.md with a skills table ({name: status}) and a modules table."""
        lines = ["# Roadmap", "", "| Skill | Status |", "|---|---|"]
        lines += [f"| `{name}` | {status} |" for name, status in skills.items()]
        lines += ["", "| Module | Skill | Status |", "|---|---|---|"]
        lines += [
            f"| `{name}` | `{skill}` | {status} |" for name, (skill, status) in modules.items()
        ]
        (self.root / "ROADMAP.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def plugin(self, name: str, *paths: str) -> dict:
        return {"name": name, "source": "./", "strict": False, "skills": list(paths)}

    def catalog(self, *plugins: dict) -> None:
        self.catalog_text(
            json.dumps({"name": "fixture-skills", "owner": {"name": "fixture"}, "plugins": plugins})
        )

    def catalog_text(self, text: str) -> None:
        (self.root / ".claude-plugin").mkdir(exist_ok=True)
        (self.root / ".claude-plugin" / "marketplace.json").write_text(text, encoding="utf-8")


@pytest.fixture
def repo(tmp_path: Path) -> RepoBuilder:
    return RepoBuilder(tmp_path)


STANDARD_SKILL = "standard-skill"

# The smallest document that passes every mechanical check the standard states for itself.
STANDARD_TEXT = """\
---
name: project-bootstrap-and-audit
description: "A synthetic standard for tests."
metadata:
  version: "0.2.0"
---

# Synthetic standard

## Phase 3 — Establish Tier — **WAIT**

## Phase 6 — Approval Gate — **WAIT**

<constraints>

A rule.

</constraints>

| Status | Meaning |
|---|---|
| `OK` | Fine |

{phases}

{dimensions}

# Provenance

## Entries

**0.2.0** — second.

**0.1.0** — first.

## Longer write-ups

**0.1.0** — the first, at length.
"""

PHASE_BLOCK = "```yaml\nphase: {n}\nnotes: none\n```"
DIMENSION = "### {n}. Dimension {n}\n\nText."


def standard_text(version: str = "0.2.0") -> str:
    phases = "\n\n".join(PHASE_BLOCK.format(n=n) for n in range(10))
    dimensions = "\n\n".join(DIMENSION.format(n=n) for n in range(1, 11))
    text = STANDARD_TEXT.format(phases=phases, dimensions=dimensions)
    return text.replace('version: "0.2.0"', f'version: "{version}"')


def add_standard(repo: RepoBuilder, text: str | None = None, version: str = "0.2.0") -> Path:
    """A skill carrying the standard as its reference, listed in the catalog."""
    frontmatter = (
        f"name: {STANDARD_SKILL}\ndescription: Runs the synthetic standard. Use when testing.\n"
        f'metadata:\n  standard-version: "{version}"\n'
    )
    reference = f"references/PROJECT-BOOTSTRAP-AND-AUDIT-v{version}.md"
    # The skill carrying the standard needs no rationale file: the standard gives its reasons.
    skill_dir = repo.skill(
        STANDARD_SKILL, frontmatter, body=f"Read [the standard]({reference}).\n", rationale=False
    )
    (skill_dir / "references").mkdir()
    (skill_dir / reference).write_text(
        standard_text(version) if text is None else text, encoding="utf-8"
    )
    repo.catalog(repo.plugin("standards", f"./skills/{STANDARD_SKILL}"))
    return skill_dir / reference
