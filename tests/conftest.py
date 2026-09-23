import json
from pathlib import Path

import pytest

DEFAULT_DESCRIPTION = "A fixture skill for tests. Use when testing."
DEFAULT_FRONTMATTER = "name: {name}\ndescription: " + DEFAULT_DESCRIPTION + "\n"


class RepoBuilder:
    """Builds a throwaway repository under tmp_path. Every skill here is synthetic."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def skill(self, directory: str, frontmatter: str | None = None, body: str = "Body.\n") -> Path:
        if frontmatter is None:
            frontmatter = DEFAULT_FRONTMATTER.format(name=directory)
        return self.skill_file(directory, f"---\n{frontmatter}---\n\n{body}")

    def skill_file(self, directory: str, text: str) -> Path:
        skill_dir = self.root / "skills" / directory
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(text, encoding="utf-8")
        return skill_dir

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
    skill_dir = repo.skill(STANDARD_SKILL, frontmatter, body=f"Read [the standard]({reference}).\n")
    (skill_dir / "references").mkdir()
    (skill_dir / reference).write_text(
        standard_text(version) if text is None else text, encoding="utf-8"
    )
    repo.catalog(repo.plugin("standards", f"./skills/{STANDARD_SKILL}"))
    return skill_dir / reference
