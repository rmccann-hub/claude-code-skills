"""Dated facts: a skill's references/facts.md, one table row per fact.

A fact that can go stale carries its source, a short quote, the date it was checked and a date
to check it again by (docs/authoring-a-skill.md, item 2). Three checks keep the rows honest:

- on every run, each row is well formed, and every fact a skill's files name by ID exists;
- ``skillcheck --due`` lists the facts whose check-by date has come;
- ``skillcheck --verify`` fetches each source again and looks for its quote.

The last two depend on the date and the network, so they run on a schedule and never on a pull
request, where a result should depend only on the commit.
"""

import re
import subprocess
import urllib.request
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

FACTS = "references/facts.md"
COLUMNS = ("ID", "Fact", "Source", "Quote", "Checked", "Check by")
# GitHub splits a table row on every pipe that isn't escaped, inside code spans too.
CELL = re.compile(r"(?<!\\)\|")
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
FACT_ID = re.compile(rf"`({NAME.pattern})`")
# A source is a page, or the command that shows the fact: a tag's commit is read off the remote,
# and running it again is how a moved tag gets caught.
LINK = re.compile(r"\]\((https://[^)\s]+)\)")
LS_REMOTE = "git ls-remote --tags "
COMMAND = re.compile(rf"`({LS_REMOTE}https://[^`\s]+)`")
QUOTED = re.compile(r'"((?:[^"\\]|\\.)+)"')
CODE = re.compile(r"`([^`]+)`")
ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
# How a skill's other files name a fact: "(fact `node20`)", "(facts `pre-commit`, `prek`)".
REFERENCE = re.compile(r"\b[Ff]acts?((?:,?\s+(?:and\s+)?`[^`\n]+`)+)")
# A quote that leaves words out marks the gap with an ellipsis. Each piece is looked for alone.
ELISION = re.compile("\u2026|\\.\\.\\.")
# Pages set the same words with typographic quotes, non-breaking spaces and code spans.
PLAIN = str.maketrans(
    {"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u00a0": " ", "`": None}
)
BLOCKS = frozenset({"br", "dd", "div", "dt", "h1", "h2", "h3", "h4", "li", "p", "pre", "td", "th"})
# Some sites refuse a request that names no browser or tool.
USER_AGENT = "skillcheck (+https://github.com/rmccann-hub/claude-code-skills)"
TIMEOUT_SECONDS = 30

Add = Callable[[str, str, str], None]
Fetch = Callable[[str], str]


@dataclass(frozen=True)
class Fact:
    path: str
    line: int
    id: str
    sources: tuple[str, ...]
    quotes: tuple[str, ...]
    check_by: date


def check(root: Path, skill_dir: Path, add: Add) -> int:
    """Report malformed rows and unknown fact IDs in one skill; return how many facts it has."""
    path = skill_dir / FACTS
    found: list[Fact] = []
    if path.is_file():
        found, problems = _read(root, path)
        for message in problems:
            add(path.relative_to(root).as_posix(), "facts", message)
    _check_references(root, skill_dir, {fact.id for fact in found}, add)
    return len(found)


def collect(root: Path) -> list[Fact]:
    """Every well-formed fact in every skill. The full check reports the malformed rows."""
    found: list[Fact] = []
    for path in sorted((root / "skills").glob(f"*/{FACTS}")):
        found += _read(root, path)[0]
    return found


def verify(facts: list[Fact], fetch: Fetch | None = None) -> Iterator[tuple[Fact, str]]:
    """Yield each fact whose quote isn't found at any of its sources, with the reason.

    The quote is the cell's text in double quotes, or, for a command's output, in backticks. A
    cell holding neither has nothing to look for, and is left to be checked by hand.
    """
    fetch = fetch or fetch_text
    pages: dict[str, str | OSError] = {}
    for fact in facts:
        if not fact.quotes:
            continue
        texts, failures = [], []
        for source in fact.sources:
            if source not in pages:
                try:
                    pages[source] = _plain(fetch(source))
                except OSError as exc:  # urllib's errors, HTTP ones included, are all OSErrors
                    pages[source] = exc
            page = pages[source]
            if isinstance(page, OSError):
                failures.append(f"{source} could not be read ({page})")
            else:
                texts.append(page)
        if not texts:
            yield fact, "; ".join(failures)
            continue
        for quote in fact.quotes:
            if not any(_holds(text, quote) for text in texts):
                yield fact, f'the quote is no longer at its source: "{quote}"'


def fetch_text(source: str) -> str:
    """A page's visible text, a non-HTML response as it came, or a command's output."""
    if source.startswith(LS_REMOTE):
        return _ls_remote(source.removeprefix(LS_REMOTE))
    request = urllib.request.Request(source, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        body = response.read().decode(charset, errors="replace")
        if response.headers.get_content_type() != "text/html":
            return body
    parser = _Text()
    parser.feed(body)
    parser.close()
    return "".join(parser.parts)


def _ls_remote(url: str) -> str:
    try:
        result = subprocess.run(
            ["git", "ls-remote", "--tags", url],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise OSError(f"git ls-remote took over {TIMEOUT_SECONDS} seconds") from exc
    if result.returncode:
        raise OSError(f"git ls-remote exited {result.returncode}: {result.stderr.strip()}")
    return result.stdout


def _read(root: Path, path: Path) -> tuple[list[Fact], list[str]]:
    where = path.relative_to(root).as_posix()
    found: list[Fact] = []
    problems: list[str] = []
    seen: set[str] = set()
    table = None  # None outside a table; else whether the table is a fact table
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|"):
            table = None
            continue
        cells = [cell.strip() for cell in CELL.split(line.strip()[1:].removesuffix("|"))]
        if table is None:
            table = tuple(cells) == COLUMNS
            if not table:
                problems.append(
                    f"line {number}: a table here has the columns {', '.join(cells)}; "
                    f"a fact table has {', '.join(COLUMNS)}"
                )
            continue
        if not table or set(line) <= set("|-: "):
            continue
        fact = _row(where, number, cells, problems)
        if fact is None:
            continue
        if fact.id in seen:
            problems.append(f"line {number}: `{fact.id}` is already defined above")
            continue
        seen.add(fact.id)
        found.append(fact)
    return found, problems


def _row(where: str, number: int, cells: list[str], problems: list[str]) -> Fact | None:
    if len(cells) != len(COLUMNS):
        problems.append(f"line {number}: a fact row has {len(COLUMNS)} cells, not {len(cells)}")
        return None
    ident, _, source, quote, checked, check_by = cells
    wrong = []
    name = FACT_ID.fullmatch(ident)
    if name is None:
        wrong.append("the ID is not one lowercase, hyphenated name in backticks")
    sources = tuple(LINK.findall(source) + COMMAND.findall(source))
    if not sources:
        wrong.append(f"the source is neither an https link nor `{LS_REMOTE}<https URL>`")
    if not quote:
        wrong.append("the quote is empty")
    checked_on, due_on = _day(checked), _day(check_by)
    if checked_on is None or due_on is None:
        wrong.append("the dates are not both YYYY-MM-DD")
    elif due_on <= checked_on:
        wrong.append("the check-by date is not after the checked date")
    if wrong:
        problems.append(f"line {number}: {'; '.join(wrong)}")
        return None
    quotes = tuple(text.replace('\\"', '"') for text in QUOTED.findall(quote))
    return Fact(where, number, name.group(1), sources, quotes or tuple(CODE.findall(quote)), due_on)


def _day(text: str) -> date | None:
    # date.fromisoformat also takes 20261231 and 2026-W53-4, which a reader would not.
    if not ISO_DATE.fullmatch(text):
        return None
    try:
        return date.fromisoformat(text)
    except ValueError:  # the right shape, but no such day, such as 2026-02-30
        return None


def _check_references(root: Path, skill_dir: Path, ids: set[str], add: Add) -> None:
    for path in sorted(skill_dir.rglob("*.md")):
        if path == skill_dir / FACTS:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in REFERENCE.finditer(text):
            for ident in CODE.findall(match.group(1)):
                # Only an ID's shape counts, so "a fact `UNVERIFIABLE-HERE`" in prose doesn't.
                if NAME.fullmatch(ident) and ident not in ids:
                    number = text.count("\n", 0, match.start()) + 1
                    add(
                        path.relative_to(root).as_posix(),
                        "facts",
                        f"line {number} names fact `{ident}`, which {FACTS} doesn't define",
                    )


def _plain(text: str) -> str:
    return " ".join(text.translate(PLAIN).split()).casefold()


def _holds(page: str, quote: str) -> bool:
    return all(piece in page for piece in map(_plain, ELISION.split(quote)) if piece)


class _Text(HTMLParser):
    """Visible text: scripts and styles dropped, and a space where a block starts."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.hidden = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in ("script", "style"):
            self.hidden += 1
        elif tag in BLOCKS:
            self.parts.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self.hidden:
            self.hidden -= 1

    def handle_data(self, data: str) -> None:
        if not self.hidden:
            self.parts.append(data)
