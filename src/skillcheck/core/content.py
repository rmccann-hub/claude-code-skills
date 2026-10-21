"""What the text says: test data, agent-steering text, and names a public repository withholds.

Three rules, asked for by the owner on 2026-10-21 ("are we checking for good info security? for
plausible deniability when needed (for testing)? ... of what they say?"):

- **``test-data``:** examples and fixtures use data no one could mistake for real. An email's
  domain, an IPv4 address and a secret's value come from the reserved sets: ``example.com`` and
  the RFC 2606 and 6761 names, the RFC 5737 documentation ranges, and ``CHANGEME`` or a
  placeholder. A value with a real credential's prefix fails wherever it sits. A realistic fake
  can't be told from a real one, by a reader or by a secret scanner.
- **``content-safety``:** a file an agent reads as instructions or context holds no text that
  steers the agent against its user, such as "ignore previous instructions" or "don't tell the
  user", and no command that fetches a script and runs it. Text in backticks or double quotes is
  a quotation, as when a skill teaches what injected text looks like, and isn't matched.
- **``private-name``:** no file holds a name the repository withholds, such as a private
  repository or an employer. The list holds only each name's SHA-256, so it names no one;
  ``skillcheck --hash-name NAME`` gives the line to add. Each word and each hyphenated or dotted
  compound in a file is hashed and compared.

A line or fenced block that must hold test data or steering text, such as a mistake a module
shows, takes ``<!-- content: allowed, <reason> -->`` on the line before it. Nothing excuses a
withheld name.
"""

import hashlib
import ipaddress
import re
from collections.abc import Callable, Iterator
from pathlib import Path

Add = Callable[[str, str, str], None]

NAMES = ".github/private-names.sha256"
TEST_DATA_ROOTS = ("skills", "tests")
AGENT_ROOTS = ("skills", "research", ".claude")
AGENT_FILES = ("AGENTS.md", "CLAUDE.md")
NAME_ROOTS = ("skills", "docs", "research", "src", "tests", ".claude", ".claude-plugin", ".github")
TEXT_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".toml", ".txt", ".sh", ".ini", ".cfg"}

# An allowance gives its reason; one without isn't an allowance.
ALLOWED = re.compile(r"^\s*<!--\s*content:\s*allowed\b[,:;—-]?\s*\S.*?-->\s*$")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
QUOTED = re.compile(r"`[^`\n]*`|\"[^\"\n]*\"|“[^”\n]*”")

EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@((?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})\b")
RESERVED_DOMAINS = re.compile(
    r"(?:^|\.)(?:example\.(?:com|net|org)|example|test|invalid|localhost"
    r"|users\.noreply\.github\.com)$",
    re.IGNORECASE,
)
# An address may end a sentence, so a full stop after it is allowed; another digit group is not.
IPV4 = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?!\w|\.\d)")
DOCUMENTATION_NETWORKS = tuple(
    ipaddress.ip_network(n)
    for n in ("192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24", "127.0.0.0/8", "0.0.0.0/32")
)
# A key that ends in a secret's word, such as `DB_PASSWORD` or `x-access-token`, then one `:` or
# `=` (not `==`), then its value: an expression or placeholder whole, else up to a space.
SECRET = re.compile(
    r"(?i)\b(?P<key>[\w.-]*(?:password|passwd|secret|token|api[_-]?key|private[_-]?key))\b"
    r"[\"']?\s*[:=](?!=)\s*"
    r"(?P<value>\$\{\{[^}\n]*\}\}|<[^>\n]*>|\"[^\"\n]*\"|'[^'\n]*'|[^\s,;#)]+)"
)
PLACEHOLDER_VALUE = re.compile(
    r"(?i)^(?:|changeme|<[^>]*>|\$\{?\w+\}?|\$\{\{.*\}\}|\{\{.*\}\}|\{\w*\}|%[sd]|%\(\w+\)s"
    r"|\*+|x+|\.\.\.|none|null|true|false|redacted|example[\w-]*|dummy[\w-]*|fake[\w-]*"
    r"|placeholder[\w-]*|os\.environ.*|env\..*|secrets\..*|getenv.*|\w+\(.*)$"
)
REAL_PREFIX = re.compile(
    r"\b(?:ghp_|gho_|ghs_|ghu_|github_pat_|xox[abprs]-|sk-ant-|sk-proj-|AKIA)[A-Za-z0-9_-]{12,}"
)

FETCH_AND_RUN = re.compile(
    r"(?i)\b(?:curl|wget)\b[^|\n]*\|\s*(?:sudo\s+)?(?:ba|z|da)?sh\b"
    r"|\b(?:iex|invoke-expression)\b[^\n]*\b(?:iwr|irm|invoke-webrequest|invoke-restmethod)\b"
    r"|\b(?:iwr|irm|invoke-webrequest|invoke-restmethod)\b[^\n]*\|\s*(?:iex|invoke-expression)\b"
)
STEERING = re.compile(
    r"(?i)\b(?:ignore|disregard|forget)\s+(?:all\s+|any\s+|the\s+|your\s+)*"
    r"(?:previous|prior|above|earlier|system)\s+(?:instructions|rules|prompts?)"
    r"|\b(?:do\s+not|don['’]t|never)\s+(?:tell|inform|show|mention\s+(?:this\s+|it\s+)?to)\s+"
    r"the\s+(?:user|owner|human|operator)"
    r"|\bwithout\s+(?:telling|informing|asking)\s+the\s+(?:user|owner|human|operator)"
    r"|\byou\s+are\s+now\s+(?:a|an|in)\b|\bnew\s+system\s+prompt\b"
)
WORD = re.compile(r"[a-z0-9]+(?:[-_.][a-z0-9]+)*")


def check(root: Path, add: Add) -> None:
    for path in _files(root, TEST_DATA_ROOTS, ()):
        for number, line in _lines(path):
            problem = _test_data(line)
            if problem:
                add(_where(root, path), "test-data", f"line {number}: {problem}")
    for path in _files(root, AGENT_ROOTS, AGENT_FILES, suffixes={".md"}):
        for number, line in _lines(path):
            problem = _safety(line)
            if problem:
                add(_where(root, path), "content-safety", f"line {number}: {problem}")
    hashes = withheld(root)
    if hashes:
        for path in _files(root, NAME_ROOTS, (), every_root_file=True):
            # No allowance excuses a name: a public repository never needs one.
            for number, line in _lines(path, allowances=False):
                if any(_digest(word) in hashes for word in words(line)):
                    add(
                        _where(root, path),
                        "private-name",
                        f"line {number} names something this repository withholds "
                        f"(listed by hash in {NAMES})",
                    )


def withheld(root: Path) -> set[str]:
    """The hashes of the names this repository withholds."""
    path = root / NAMES
    if not path.is_file():
        return set()
    lines = path.read_text(encoding="utf-8").splitlines()
    return {line.split()[0] for line in lines if line.strip() and not line.startswith("#")}


def hash_line(name: str) -> str:
    """The line ``--hash-name`` prints for a name, ready to add to the list."""
    return _digest(name.strip().lower())


def words(line: str) -> Iterator[str]:
    """Each word and compound in a line, lowercased: `a-b.v2` gives itself, `a-b`, `v2`, then `a`,
    `b` and `v2`."""
    for compound in WORD.findall(line.lower()):
        yield compound
        dotted = compound.split(".")
        if len(dotted) > 1:
            yield from dotted
        yield from re.split(r"[-_.]", compound)


def _test_data(line: str) -> str:
    if match := REAL_PREFIX.search(line):
        return f"`{match.group()[:8]}…` has a real credential's prefix; use CHANGEME"
    for match in EMAIL.finditer(line):
        if not RESERVED_DOMAINS.search(match.group(1)):
            return f"the email domain {match.group(1)} is real; use example.com"
    for match in IPV4.finditer(line):
        try:
            address = ipaddress.ip_address(match.group())
        except ValueError:
            continue  # not an address, such as a four-part version number past 255
        if not any(address in network for network in DOCUMENTATION_NETWORKS):
            return f"{address} isn't a documentation address; use 192.0.2.0/24 (RFC 5737)"
    for match in SECRET.finditer(line):
        value = match["value"].strip("\"'")
        if not PLACEHOLDER_VALUE.match(value):
            return f"{match['key']} has a literal value; use CHANGEME or a placeholder"
    return ""


def _safety(line: str) -> str:
    text = QUOTED.sub("", line)
    if match := FETCH_AND_RUN.search(text):
        return f"`{match.group().strip()}` fetches a script and runs it; download, read, then run"
    if match := STEERING.search(text):
        return f'"{match.group()}" steers an agent against its user'
    return ""


def _lines(path: Path, allowances: bool = True) -> Iterator[tuple[int, str]]:
    """Each line to check, leaving out the line or fenced block an allowance covers."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return
    index = 0
    while index < len(lines):
        if not allowances or not ALLOWED.match(lines[index]):
            yield index + 1, lines[index]
            index += 1
            continue
        index += 1
        opened = FENCE.match(lines[index]) if index < len(lines) else None
        if opened:
            fence = opened.group(1)
            index += 1
            while index < len(lines) and lines[index].strip() != fence:
                index += 1
        index += 1


def _files(
    root: Path,
    roots: tuple[str, ...],
    named: tuple[str, ...],
    suffixes: set[str] = TEXT_SUFFIXES,
    every_root_file: bool = False,
) -> list[Path]:
    found = [root / name for name in named if (root / name).is_file()]
    if every_root_file:
        found += sorted(p for p in root.iterdir() if p.is_file() and p.suffix in suffixes)
    for directory in roots:
        if (root / directory).is_dir():
            found += sorted(
                p for p in (root / directory).rglob("*") if p.is_file() and p.suffix in suffixes
            )
    return [p for p in found if p.relative_to(root).as_posix() != NAMES]


def _digest(word: str) -> str:
    return hashlib.sha256(word.encode("utf-8")).hexdigest()


def _where(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()
