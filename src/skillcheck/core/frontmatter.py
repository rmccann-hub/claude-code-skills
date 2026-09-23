"""Read the YAML frontmatter block at the top of a SKILL.md file."""

from typing import Any

import yaml

DELIMITER = "---"


class FrontmatterError(ValueError):
    """The file has no readable frontmatter mapping."""


def parse(text: str) -> tuple[dict[str, Any], str]:
    """Return the frontmatter mapping and the body after it, or raise FrontmatterError."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != DELIMITER:
        raise FrontmatterError("file does not start with a '---' line")
    end = next((i for i, line in enumerate(lines[1:], start=1) if line.strip() == DELIMITER), None)
    if end is None:
        raise FrontmatterError("frontmatter has no closing '---' line")
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as exc:
        raise FrontmatterError(
            f"frontmatter is not valid YAML: {' '.join(str(exc).split())}"
        ) from None
    if not isinstance(data, dict):
        raise FrontmatterError("frontmatter is not a YAML mapping")
    return data, "\n".join(lines[end + 1 :])
