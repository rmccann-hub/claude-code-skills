"""Times: UTC is the stamp, and any other zone is derived from it.

The owner asked, on 2026-10-19, for UTC as the stamp every time is recorded in, with a local
time worked out from it, never written on its own. ``stamp`` does the working out, so no
session converts a time zone in its head, and ``check`` holds the repository's Markdown to it:
a time of day carries UTC, and a 12-hour local time follows a UTC time on its line. An ISO 8601
time, such as ``2026-10-17T00:55Z``, is left to whatever parses it, since its offset is part of
it.
"""

import re
from collections.abc import Callable, Iterator
from datetime import UTC, date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# The rule holds what's written from the day the owner set it. Past entries in an append-only
# record stay as they were written.
SINCE = date(2026, 10, 19)
DECISIONS = "docs/decisions.md"
# Markdown the repository writes, by the same roots the conflict-marker scan reads, leaving out
# dated research results, which quote their sources, and test fixtures, which stand in for
# other repositories' text.
ROOTS = ("skills", "docs", "research", ".claude", ".github")
EXCLUDED = ("research/runs/",)

TIME = re.compile(
    r"(?<![\w:.])(?P<t>(?:[01]?\d|2[0-3]):[0-5]\d(?::[0-5]\d)?)(?![\w:])"
    # A look-ahead, so the text after one time never hides the next time on the line.
    r"(?=(?P<after>[^\n]{0,12}))"
)
STAMPED = re.compile(r"\s*(?:UTC|GMT)\b")
TWELVE_HOUR = re.compile(r"\s*[AP]M\s+[A-Z]{2,5}\b")
CODE_SPAN = re.compile(r"`[^`\n]*`")
FENCE = re.compile(r"^\s*(```|~~~)")
ENTRY = re.compile(r"^## (\d{4}-\d{2}-\d{2})\b")

Add = Callable[[str, str, str], None]


class TimeError(ValueError):
    """The stamp or the zone can't be read, and nothing was derived."""


def stamp(text: str, zone: str | None = None) -> str:
    """``text``, an ISO 8601 time with its offset, as UTC, and in ``zone`` derived from it."""
    try:
        moment = datetime.fromisoformat(text.strip())
    except ValueError as exc:
        raise TimeError(f"not an ISO 8601 time: {text!r}") from exc
    if moment.tzinfo is None:
        raise TimeError(f"{text!r} names no zone; a stamp ends in Z or an offset such as +00:00")
    utc = moment.astimezone(UTC)
    written = f"{utc:%Y-%m-%d %H:%M} UTC"
    if not zone:
        return written
    try:
        local = utc.astimezone(ZoneInfo(zone))
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise TimeError(f"no time zone named {zone!r}") from exc
    hour = local.strftime("%I").lstrip("0")
    return f"{written} ({hour}:{local:%M %p %Z, %a %b} {local.day})"


def check(root: Path, add: Add) -> None:
    """Report each time of day in the repository's Markdown written without its zone."""
    for path in _markdown(root):
        where = path.relative_to(root).as_posix()
        lines = path.read_text(encoding="utf-8").splitlines()
        for number, line in _checked_lines(where, lines):
            for problem in _problems(CODE_SPAN.sub("", line)):
                add(where, "times", f"line {number}: {problem}")


def _markdown(root: Path) -> list[Path]:
    files = sorted(p for p in root.glob("*.md") if p.is_file())
    for directory in ROOTS:
        files += sorted((root / directory).rglob("*.md"))
    return [p for p in files if not p.relative_to(root).as_posix().startswith(EXCLUDED)]


def _checked_lines(where: str, lines: list[str]) -> Iterator[tuple[int, str]]:
    fenced = False
    # In the decision record, only entries dated on or after SINCE are held to the rule.
    held = where != DECISIONS
    for number, line in enumerate(lines, 1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if where == DECISIONS and (entry := ENTRY.match(line)):
            held = date.fromisoformat(entry.group(1)) >= SINCE
        if held and not fenced:
            yield number, line


def _problems(line: str) -> Iterator[str]:
    seen_utc = False
    for match in TIME.finditer(line):
        written, after = match.group("t"), match.group("after")
        if STAMPED.match(after):
            seen_utc = True
        elif TWELVE_HOUR.match(after):
            if not seen_utc:
                yield f"{written} is a local time with no UTC stamp before it on its line"
        else:
            yield f"{written} names no zone; write the stamp in UTC, such as {written} UTC"
