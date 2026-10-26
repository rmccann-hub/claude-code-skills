"""Whether a request reaches the right skill and module: ``skillcheck --triggers``.

Each skill's and module's trigger evaluations (``tests/fixtures/skills/<skill>.json`` and
``tests/fixtures/modules/<module>.json``) list requests that should reach it and near misses
that shouldn't. ``--triggers`` asks Claude Code each one, in a scratch project that holds
this repository's skills as project skills, and reads its stream of tool calls:

- **a skill's request** passes when the skill is invoked, and a near miss when it isn't;
- **a module's request** passes when its skill's ``references/<module>.md`` is read from the
  scratch project, and a near miss when that file isn't read. A read of another copy, such as
  an older one synced to the account, fails and names where it came from.

Claude Code may only invoke skills and read files there: every other tool is refused without
asking. Each request is a model call, so it runs by hand, never in CI. ``--tries`` writes the
list the owner tries by hand on claude.ai instead, where no program can drive a chat: for each
skill and module, one request that should reach it and one near miss.
"""

import json
import shutil
import subprocess
import tempfile
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path

from skillcheck.core.text import printable

CLAUDE = ("npx", "--no-install", "claude")
TIMEOUT_SECONDS = 300
TOOLS = "Skill Read Glob Grep"
FIXTURES = {"skill": "tests/fixtures/skills", "module": "tests/fixtures/modules"}


@dataclass(frozen=True)
class Case:
    kind: str
    name: str
    skill: str
    query: str
    should: bool
    note: str = ""


@dataclass(frozen=True)
class Seen:
    skills: tuple[str, ...]
    reads: tuple[str, ...]
    error: str = ""
    model: str = ""


def cases(root: Path, names: Iterable[str] = ()) -> list[Case]:
    """Every trigger evaluation, or those of the skills and modules named."""
    wanted = set(names)
    homes = {path.stem: path.parents[1].name for path in root.glob("skills/*/references/*.md")}
    found = []
    for kind, folder in FIXTURES.items():
        for path in sorted((root / folder).glob("*.json")):
            name = path.stem
            if wanted and name not in wanted:
                continue
            skill = name if kind == "skill" else homes.get(name, "")
            for entry in json.loads(path.read_text(encoding="utf-8")):
                found.append(
                    Case(
                        kind,
                        name,
                        skill,
                        entry["query"],
                        entry["should_trigger"],
                        entry.get("note", ""),
                    )
                )
    return found


def ask(query: str, project: Path, run: Callable = subprocess.run) -> Seen:
    """One request to Claude Code: the skills it invoked and the files it read."""
    command = [
        *CLAUDE,
        "-p",
        query,
        "--output-format",
        "stream-json",
        "--verbose",
        "--no-session-persistence",
        "--setting-sources",
        "project",
        "--permission-mode",
        "dontAsk",
        "--allowedTools",
        TOOLS,
    ]
    done = run(
        command, cwd=project, capture_output=True, text=True, timeout=TIMEOUT_SECONDS, check=False
    )
    if done.returncode:
        reason = (done.stderr or done.stdout).strip().splitlines() or [f"exit {done.returncode}"]
        return Seen((), (), printable(reason[0]))
    skills, reads, model = [], [], ""
    for line in done.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "system" and event.get("subtype") == "init":
            model = printable(str(event.get("model", "")))
        if event.get("type") != "assistant":
            continue
        for item in event.get("message", {}).get("content", []):
            if item.get("type") != "tool_use":
                continue
            given = item.get("input", {})
            if item.get("name") == "Skill":
                skills.append(printable(str(given.get("skill", ""))))
            elif item.get("name") == "Read":
                reads.append(printable(str(given.get("file_path", ""))))
    return Seen(tuple(skills), tuple(reads), model=model)


def judge(case: Case, seen: Seen, project: Path) -> str:
    """Why the case failed, or an empty string when it passed."""
    if seen.error:
        return f"Claude Code failed: {seen.error}"
    if case.kind == "skill":
        reached = case.skill in seen.skills
    else:
        target = f".claude/skills/{case.skill}/references/{case.name}.md"
        matching = [path for path in seen.reads if path.endswith(target)]
        here = str(project.resolve())
        elsewhere = [path for path in matching if not path.startswith(here)]
        if elsewhere:
            return f"read another copy: {elsewhere[0]}"
        reached = bool(matching)
    if reached == case.should:
        return ""
    invoked = ", ".join(seen.skills) or "no skill"
    return ("didn't reach it; invoked " if case.should else "reached it; invoked ") + invoked


def project(root: Path, into: Path) -> Path:
    """A scratch project holding this repository's skills as its project skills."""
    for skill in sorted((root / "skills").iterdir()):
        if (skill / "SKILL.md").is_file():
            shutil.copytree(skill, into / ".claude" / "skills" / skill.name)
    return into


def run_all(
    root: Path, names: Iterable[str] = (), run: Callable = subprocess.run
) -> tuple[list[str], str, int]:
    """Ask every case; the failures, the summary, and the exit code: 1 when any failed."""
    chosen = cases(root, names)
    failures, models = [], set()
    with tempfile.TemporaryDirectory(prefix="skillcheck-triggers-") as scratch:
        where = project(root, Path(scratch))
        for case in chosen:
            seen = ask(case.query, where, run)
            models.add(seen.model or "an unnamed model")
            problem = judge(case, seen, where)
            if problem:
                expected = "should reach" if case.should else "near miss for"
                failures.append(
                    f"{case.kind} {case.name}: {expected} it: {case.query!r}: {problem}"
                )
    summary = f"skillcheck: {len(chosen)} trigger request(s) asked, {len(failures)} failed"
    if models:
        summary += f", on {', '.join(sorted(models))}"
    return failures, summary, 1 if failures or not chosen else 0


def tries(root: Path, names: Iterable[str] = ()) -> str:
    """The claude.ai list: per skill and module, one request that should reach it, one miss."""
    lines = [
        "# Requests to try on claude.ai",
        "",
        "Try each in a new chat, with this repository's skills uploaded and turned on.",
        "",
        "| Skill or module | Request | A pass |",
        "|---|---|---|",
    ]
    picked: dict[tuple[str, str], dict[bool, Case]] = {}
    for case in cases(root, names):
        picked.setdefault((case.kind, case.name), {}).setdefault(case.should, case)
    for (kind, name), pair in picked.items():
        for should in (True, False):
            case = pair.get(should)
            if case is None:
                continue
            if kind == "skill":
                outcome = f"the `{name}` skill loads" if should else f"`{name}` doesn't load"
            elif should:
                outcome = f"`{case.skill}` loads and reads `references/{name}.md`"
            else:
                outcome = f"`references/{name}.md` isn't read"
            if case.note and not should:
                outcome += f"; it's for `{case.note}`"
            query = case.query.replace("|", "\\|")
            lines.append(f"| {kind} `{name}` | {query} | {outcome} |")
    return "\n".join(lines) + "\n"
