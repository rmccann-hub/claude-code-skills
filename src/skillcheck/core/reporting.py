"""Every skill's "When something here is wrong" section: one text, the same in every skill.

A person using a skill is the first to see it fail: a fact gone stale, an example that doesn't
run, advice that doesn't fit. The section tells the model reading the skill to say so in a
sentence when a person raises a problem, and to draft a full report when the fault is the
skill's own. The text is kept here, once, and ``skillcheck`` holds every ``SKILL.md`` to it, so
a change to how problems are reported reaches every skill in one edit.
"""

import json
from collections.abc import Callable
from pathlib import Path

from skillcheck.core import modules

HEADING = "When something here is wrong"
CATALOG = ".claude-plugin/marketplace.json"
# Where a skill whose catalog names no single repository says to report, until it names one.
UNKNOWN = "https://github.com/OWNER/REPO/issues"

TEXT = """\
If the person says advice here is wrong, out of date, failed or doesn't fit, answer their
problem first. Then say in one sentence whether the fault looks like this skill's, and why: a
fact past its check-by date, an example that fails, two rules that disagree, or a case the skill
doesn't cover. If the fault is elsewhere, such as their setup, say that instead.

When the fault is the skill's own, draft a full report they can paste as a new issue at
{issues}.
Give the skill and module, the plugin's version or the skill's date in its frontmatter, their
request word for word, the line of the skill that misled, what happened, what's right with its
source, and the fix you'd suggest. Leave out their private data, company detail and repository
names. File it only if they ask you to.
"""

Add = Callable[[str, str, str], None]


def issues_url(root: Path) -> str | None:
    """The issues page of the one repository the catalog names, or None when it names none."""
    path = root / CATALOG
    if not path.is_file():
        return None
    try:
        plugins = json.loads(path.read_text(encoding="utf-8")).get("plugins", [])
    except json.JSONDecodeError, AttributeError:
        return None  # the catalog check reports a broken catalog
    urls = {
        p["repository"].rstrip("/") for p in plugins if isinstance(p, dict) and p.get("repository")
    }
    return f"{urls.pop()}/issues" if len(urls) == 1 else None


def section(issues: str | None) -> str:
    """The section as a skill holds it, heading included."""
    return f"## {HEADING}\n\n{TEXT.format(issues=issues or UNKNOWN)}"


def check(root: Path, skill_dir: Path, issues: str | None, add: Add) -> None:
    where = skill_dir.relative_to(root).as_posix() + "/SKILL.md"
    lines = modules.sections((skill_dir / "SKILL.md").read_text(encoding="utf-8")).get(HEADING)
    if lines is None:
        add(
            where,
            "reporting",
            f"no '{HEADING}' section, so a problem with the skill goes unreported",
        )
        return
    if issues is None:
        return
    found = "\n".join(line for _, line in lines).strip()
    if found != TEXT.format(issues=issues).strip():
        add(
            where,
            "reporting",
            f"the '{HEADING}' section differs from the text every skill shares, in "
            "src/skillcheck/core/reporting.py; copy it from there",
        )
