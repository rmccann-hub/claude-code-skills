"""Every code example in a skill, run under its language's own tool: ``skillcheck --examples``.

Each fenced block in a skill's Markdown is checked by the language its info string names:

- **Python:** compiled, so a syntax error fails. Names it uses needn't be defined, because an
  example is often a fragment.
- **JSON, YAML, TOML, INI:** parsed. INI may start with keys before its first section, as
  EditorConfig and Vale's files do.
- **Shell** (``sh``, ``bash``, ``shell``): parsed by ``bash -n`` or ``sh -n``, then linted by
  ShellCheck at its warning level.
- **PowerShell:** parsed by ``pwsh``'s own parser.

A placeholder such as ``<branch>`` or ``<path | none>`` stands for a value the reader supplies,
so in shell and YAML it's read as a plain word first. In YAML one may run onto a second line.

A block in any other language, or with no language, isn't checked and is counted as such. A block
that is wrong on purpose, such as a mistake being shown, is skipped with a comment on the line
before it that gives the reason: ``<!-- example: unchecked, shows the error the reader will see
-->``. A tool that isn't installed fails the run, so CI never passes a block it couldn't check.
"""

import configparser
import json
import re
import shutil
import subprocess
import tomllib
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

import yaml

TIMEOUT_SECONDS = 60
OPEN = re.compile(r"^(?P<indent>[ \t]*)(?P<fence>`{3,}|~{3,})[ \t]*(?P<info>[^`\n]*)$")
UNCHECKED = re.compile(r"^\s*<!--\s*example:\s*unchecked\b[,:;—-]?\s*(?P<reason>.*?)\s*-->\s*$")
# Shell's is held to one line, so a here-document's `<<EOF` can't swallow the script.
SHELL_PLACEHOLDER = re.compile(r"<[A-Za-z0-9][^<>\n]*>")
YAML_PLACEHOLDER = re.compile(r"<[A-Za-z0-9][^<>]*>")
SHELLS = {"sh": "sh", "bash": "bash", "shell": "bash"}


class ToolMissing(RuntimeError):
    """The tool a language needs isn't installed."""


@dataclass(frozen=True)
class Block:
    path: Path
    line: int
    language: str
    text: str
    skip_reason: str | None = None


@dataclass
class Result:
    checked: int = 0
    failures: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    unchecked: Counter = field(default_factory=Counter)

    def report(self) -> tuple[list[str], str, int]:
        """The lines worth reading, the summary, and the exit code: 1 when any block failed."""
        kinds = ", ".join(f"{lang} {n}" for lang, n in sorted(self.unchecked.items()))
        summary = (
            f"skillcheck: {self.checked} example(s) checked, {len(self.failures)} failed, "
            f"{len(self.skipped)} skipped with a reason, "
            f"{sum(self.unchecked.values())} in a language with no checker"
            + (f" ({kinds})" if kinds else "")
        )
        return self.failures + self.skipped, summary, 1 if self.failures else 0


def blocks(path: Path) -> list[Block]:
    """The fenced blocks in one Markdown file, each with the line its fence opens on."""
    found = []
    lines = path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        opened = OPEN.match(lines[index])
        if not opened:
            index += 1
            continue
        fence, indent = opened["fence"], len(opened["indent"])
        info = opened["info"].split()
        language = info[0].lower() if info else ""
        previous = next((line for line in reversed(lines[:index]) if line.strip()), "")
        marker = UNCHECKED.match(previous)
        body, index = [], index + 1
        start = index
        while index < len(lines):
            line = lines[index]
            stripped = line.strip()
            if stripped.startswith(fence[0] * len(fence)) and not stripped.strip(fence[0]):
                break
            body.append(line[indent:] if line[:indent].strip() == "" else line.lstrip())
            index += 1
        found.append(
            Block(path, start, language, "\n".join(body) + "\n", marker and marker["reason"])
        )
        index += 1
    return found


def check(root: Path, run: Callable = subprocess.run) -> Result:
    """Check every example in every skill under ``root``."""
    result = Result()
    for path in sorted((root / "skills").glob("**/*.md")):
        for block in blocks(path):
            where = f"{path.relative_to(root).as_posix()}:{block.line}"
            if block.skip_reason is not None:
                if not block.skip_reason:
                    result.failures.append(f"{where}: skipped with no reason; give one")
                else:
                    result.skipped.append(f"{where}: skipped: {block.skip_reason}")
                continue
            checker = _checker(block.language)
            if checker is None:
                result.unchecked[block.language or "no language"] += 1
                continue
            result.checked += 1
            try:
                problem = checker(block.text, run)
            except ToolMissing as missing:
                problem = str(missing)
            if problem:
                result.failures.append(f"{where}: {block.language}: {problem}")
    return result


def _checker(language: str) -> Callable[[str, Callable], str] | None:
    if language in SHELLS:
        return lambda text, run: _shell(SHELLS[language], text, run)
    return {
        "python": _python,
        "py": _python,
        "json": _json,
        "yaml": _yaml,
        "yml": _yaml,
        "toml": _toml,
        "ini": _ini,
        "powershell": _powershell,
        "pwsh": _powershell,
        "ps1": _powershell,
    }.get(language)


def _python(text: str, run: Callable) -> str:
    try:
        compile(text, "<example>", "exec")
    except SyntaxError as error:
        return f"line {error.lineno}: {error.msg}"
    return ""


def _json(text: str, run: Callable) -> str:
    try:
        json.loads(text)
    except json.JSONDecodeError as error:
        return f"line {error.lineno}: {error.msg}"
    return ""


def _yaml(text: str, run: Callable) -> str:
    try:
        list(yaml.safe_load_all(YAML_PLACEHOLDER.sub("PLACEHOLDER", text)))
    except yaml.YAMLError as error:
        return " ".join(str(error).split())
    return ""


def _toml(text: str, run: Callable) -> str:
    try:
        tomllib.loads(text)
    except tomllib.TOMLDecodeError as error:
        return str(error)
    return ""


def _ini(text: str, run: Callable) -> str:
    parser = configparser.ConfigParser(interpolation=None, strict=False)
    first = next((line.strip() for line in text.splitlines() if line.strip()), "")
    # EditorConfig and Vale put keys before the first section.
    if not first.startswith(("[", "#", ";")):
        text = "[top]\n" + text
    try:
        parser.read_string(text)
    except configparser.Error as error:
        return " ".join(str(error).split())
    return ""


def _shell(shell: str, text: str, run: Callable) -> str:
    script = SHELL_PLACEHOLDER.sub("PLACEHOLDER", text)
    parsed = _tool(run, [shell, "-n"], script)
    if parsed.returncode:
        return " ".join(parsed.stderr.split())
    linted = _tool(run, ["shellcheck", f"--shell={shell}", "--severity=warning", "-"], script)
    if linted.returncode:
        codes = sorted(set(re.findall(r"SC\d{4}", linted.stdout)))
        return "ShellCheck: " + (", ".join(codes) or " ".join(linted.stdout.split()))
    return ""


def _powershell(text: str, run: Callable) -> str:
    # The script arrives on standard input, so nothing in it is ever run.
    command = (
        "$errors = $null; "
        "[void][System.Management.Automation.Language.Parser]::ParseInput("
        "[Console]::In.ReadToEnd(), [ref]$null, [ref]$errors); "
        "$errors | ForEach-Object { $_.Message }"
    )
    parsed = _tool(run, ["pwsh", "-NoProfile", "-NonInteractive", "-Command", command], text)
    return " ".join(parsed.stdout.split())


def _tool(run: Callable, command: list[str], text: str) -> subprocess.CompletedProcess:
    if shutil.which(command[0]) is None:
        raise ToolMissing(f"needs {command[0]}, which isn't installed")
    return run(
        command, input=text, capture_output=True, text=True, timeout=TIMEOUT_SECONDS, check=False
    )
