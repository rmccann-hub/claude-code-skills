"""Parity runs for project-bootstrap-and-audit: build a sample repository, then grade the report.

A parity run audits a sample repository with the skill, in a fresh session, and its report is
checked against the sample's answer key and against the recorded baseline. Samples are stored
as manifests rather than as trees, because a sample's CLAUDE.md, pyproject.toml or
.gitattributes kept as a real file here would be read by Claude Code, ruff or git as this
repository's own. The procedure is in docs/testing-the-skill.md.

Usage: ``python -m skillcheck.parity {materialize,grade,record,compare} ...``
"""

import argparse
import datetime
import os
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# The standard's dimension statuses, in its order of precedence.
STATUSES = ("BLOCKER", "DRIFT", "GAP", "OVER", "MIRROR", "UNVERIFIABLE-HERE", "OK", "N/A")
DIMENSIONS = tuple(range(1, 11))

YAML_BLOCK = re.compile(r"^```ya?ml[^\n]*\n(.*?)^```", re.MULTILINE | re.DOTALL)
PHASE = re.compile(r"^phase:\s*(\d+)\s*$", re.MULTILINE)
# A key at the start of a line. Report blocks are YAML in shape but often not valid YAML, so
# they are read by their top-level keys rather than parsed.
TOP_KEY = re.compile(r"^([A-Za-z_][\w-]*):", re.MULTILINE)
ENTRY = re.compile(r"\bn:\s*(\d+)")
# Any word, so a run that coins a status is reported with the word it coined.
STATUS_FIELD = re.compile(r"\bstatus:\s*\"?([A-Za-z][\w/-]*)")
SECONDARY_FIELD = re.compile(r"\bsecondary:\s*\[([^\]]*)\]")
STATUS_WORD = re.compile(r"\b(?:" + "|".join(re.escape(s) for s in STATUSES) + r")(?![\w/-])")
COUNT = re.compile(r"([A-Z][A-Z/-]*)\s*:\s*(\d+)")
AUTHOR = re.compile(r"^(?P<name>[^<>]+?) <(?P<email>[^<>]+)>$")
MODES = {"re-check": "recheck"}


class SampleError(ValueError):
    """A sample manifest or answer key that cannot be used."""


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SampleError(f"{path}: expected a mapping")
    return data


def check_sample(sample: dict) -> None:
    for key in ("name", "job", "answers", "commits"):
        if key not in sample:
            raise SampleError(f"the sample has no {key!r}")
    commits = sample["commits"]
    if not commits:
        raise SampleError("the sample has no commits")
    for number, commit in enumerate(commits, 1):
        for key in ("message", "author", "date"):
            if key not in commit:
                raise SampleError(f"commit {number} has no {key!r}")
        if not AUTHOR.match(commit["author"]):
            raise SampleError(f"commit {number}: author must read 'Name <email>'")
    for tag in sample.get("tags") or []:
        if not 1 <= tag["commit"] <= len(commits):
            raise SampleError(f"tag {tag['name']} names commit {tag['commit']}, which is absent")


def materialize(sample: dict, dest: Path) -> Path:
    """Build the sample as a git repository under dest, with a bare remote beside it."""
    check_sample(sample)
    work = dest / sample["name"]
    remote = dest / f"{sample['name']}.git"
    for path in (work, remote):
        if path.exists():
            raise SampleError(f"{path} already exists")
    work.mkdir(parents=True)
    _git(work, "init", "--quiet", "--initial-branch=main")
    shas = []
    for commit in sample["commits"]:
        for relative, text in (commit.get("files") or {}).items():
            path = work / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        for relative in commit.get("delete") or []:
            (work / relative).unlink()
        author = AUTHOR.match(commit["author"])
        date = _date(commit["date"])
        identity = {}
        for role in ("AUTHOR", "COMMITTER"):
            identity[f"GIT_{role}_NAME"] = author["name"]
            identity[f"GIT_{role}_EMAIL"] = author["email"]
            identity[f"GIT_{role}_DATE"] = date
        _git(work, "add", "--all")
        _git(work, "commit", "--quiet", "--message", commit["message"], env=identity)
        shas.append(_git(work, "rev-parse", "HEAD"))
    for tag in sample.get("tags") or []:
        _git(work, "tag", tag["name"], shas[tag["commit"] - 1])
    _git(dest, "init", "--quiet", "--bare", remote.name)
    _git(work, "remote", "add", "origin", str(remote))
    _git(work, "push", "--quiet", "origin", "main", "--tags")
    _git(work, "branch", "--quiet", "--set-upstream-to=origin/main")
    return work


def _date(value: object) -> str:
    # YAML reads an unquoted timestamp as a datetime rather than as text.
    return value.isoformat() if isinstance(value, datetime.datetime) else str(value)


def _git(cwd: Path, *args: str, env: dict[str, str] | None = None) -> str:
    # Isolated from this machine's git configuration, so a sample builds the same everywhere.
    environment = {
        **os.environ,
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        **(env or {}),
    }
    result = subprocess.run(
        ["git", "-c", "commit.gpgSign=false", "-c", "tag.gpgSign=false", *args],
        cwd=cwd,
        env=environment,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


@dataclass
class Results:
    """What a run's report says, read from its YAML blocks."""

    phases: list[int] = field(default_factory=list)
    mode: str | None = None
    tier: str | None = None
    blast_radius: str | None = None
    audience: str | None = None
    statuses: dict[int, str] = field(default_factory=dict)
    secondaries: dict[int, list[str]] = field(default_factory=dict)
    tally: dict[str, int] = field(default_factory=dict)


def extract(report: str) -> Results:
    blocks = [match.group(1) for match in YAML_BLOCK.finditer(report)]
    phases: dict[int, dict[str, str]] = {}
    header: dict[str, str] = {}
    for block in blocks:
        sections = _sections(block)
        match = PHASE.search(block)
        if match:
            phases.setdefault(int(match.group(1)), sections)
        elif not header and "mode" in sections and "tier" in sections:
            header = sections
    results = Results(phases=sorted(phases))
    mode = _first(phases.get(1, {}).get("mode")) or _first(header.get("mode"))
    results.mode = MODES.get(mode, mode)
    tier = phases.get(3, {})
    for name, pattern in (("tier", "T[0-3]"), ("blast_radius", "B[0-3]"), ("audience", "A[0-3]")):
        # The run report's header gives all three on its tier line.
        value = _code(tier.get(name), pattern) or _code(header.get("tier"), pattern)
        setattr(results, name, value)
    dimensions = phases.get(4, {})
    results.statuses, results.secondaries = _dimensions(dimensions)
    results.tally = {word: int(count) for word, count in COUNT.findall(dimensions.get("tally", ""))}
    return results


def _sections(block: str) -> dict[str, str]:
    marks = list(TOP_KEY.finditer(block))
    sections: dict[str, str] = {}
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(block)
        sections.setdefault(mark.group(1), block[mark.end() : end])
    return sections


def _first(value: str | None) -> str | None:
    match = re.search(r"[a-z][a-z-]*", (value or "").lower())
    return match.group(0) if match else None


def _code(value: str | None, pattern: str) -> str | None:
    match = re.search(rf"\b{pattern}\b", value or "")
    return match.group(0) if match else None


def _dimensions(sections: dict[str, str]) -> tuple[dict[int, str], dict[int, list[str]]]:
    statuses: dict[int, str] = {}
    secondaries: dict[int, list[str]] = {}
    for number, chunk in _entries(sections.get("dimensions", "")):
        status = STATUS_FIELD.search(chunk)
        if status and number not in statuses:
            statuses[number] = status.group(1)
        listed = SECONDARY_FIELD.search(chunk)
        words = STATUS_WORD.findall(listed.group(1)) if listed else []
        if words:
            secondaries.setdefault(number, []).extend(words)
    for number, chunk in _entries(sections.get("secondaries", "")):
        status = STATUS_FIELD.search(chunk)
        if status:
            secondaries.setdefault(number, []).append(status.group(1))
    return statuses, secondaries


def _entries(text: str) -> list[tuple[int, str]]:
    """Each `n: <number>` in text, with the text up to the next one."""
    marks = list(ENTRY.finditer(text))
    return [
        (int(mark.group(1)), text[mark.start() : marks[index + 1].start()])
        if index + 1 < len(marks)
        else (int(mark.group(1)), text[mark.start() :])
        for index, mark in enumerate(marks)
    ]


@dataclass
class Check:
    name: str
    # None when the report did not hold what the check needs.
    passed: bool | None
    detail: str


def grade(report: str, key: dict) -> list[Check]:
    results = extract(report)
    lower = report.lower()
    stops_at = key["stops_at"]
    last = max(results.phases, default=None)
    checks = [
        Check(f"stops at Phase {stops_at}", last == stops_at, f"last phase block: {last}"),
        _expect("mode", results.mode, [key["mode"]]),
        _expect("tier", results.tier, key["tier"]),
        _expect("blast radius", results.blast_radius, key["blast_radius"]),
        _expect("audience", results.audience, key["audience"]),
    ]
    if stops_at >= 4:
        checks += [_ten_statuses(results), _tally(results)]
    for item in key.get("planted") or []:
        checks.append(_planted(item, results, lower))
    for word in key.get("words") or []:
        found = word.lower() in lower
        checks.append(Check(f"mentions {word}", found, "found" if found else "not in the report"))
    amendments = _amendments(report)
    for term in key.get("not_proposed") or []:
        if amendments is None:
            checks.append(Check(f"does not propose {term}", None, "no Phase 6 amendments"))
        else:
            proposed = term.lower() in amendments.lower()
            detail = "named in the amendments" if proposed else "absent from the amendments"
            checks.append(Check(f"does not propose {term}", not proposed, detail))
    return checks


def _expect(name: str, actual: str | None, allowed: list[str]) -> Check:
    if actual is None:
        return Check(name, None, "not found in the report")
    return Check(name, actual in allowed, f"{actual}; the key allows {', '.join(allowed)}")


def _ten_statuses(results: Results) -> Check:
    missing = [n for n in DIMENSIONS if n not in results.statuses]
    coined = sorted({s for s in results.statuses.values() if s not in STATUSES})
    problems = []
    if missing:
        problems.append(f"no status for {', '.join(map(str, missing))}")
    if coined:
        problems.append(f"statuses outside the vocabulary: {', '.join(coined)}")
    return Check("ten statuses", not problems, "; ".join(problems) or "1 to 10, all known")


def _tally(results: Results) -> Check:
    if not results.tally:
        return Check("tally", None, "no tally in the Phase 4 block")
    counted = Counter(s for n, s in results.statuses.items() if n in DIMENSIONS)
    stated = {word: count for word, count in results.tally.items() if count}
    total = sum(results.tally.values())
    matches = stated == dict(counted)
    detail = f"sums to {total}; {'matches' if matches else 'does not match'} the statuses"
    return Check("tally", total == 10 and matches, detail)


def _planted(item: dict, results: Results, lower: str) -> Check:
    found = any(word.lower() in lower for word in item["words"])
    seen = {
        n: [results.statuses.get(n, "none"), *results.secondaries.get(n, [])]
        for n in item["dimensions"]
    }
    rated = any(status in item["rated"] for statuses in seen.values() for status in statuses)
    shown = "; ".join(f"{n}: {', '.join(statuses)}" for n, statuses in seen.items())
    detail = f"words {'found' if found else 'missing'}; dimensions {shown}"
    return Check(f"{item['id']} {item['problem']}", found and rated, detail)


def _amendments(report: str) -> str | None:
    for match in YAML_BLOCK.finditer(report):
        phase = PHASE.search(match.group(1))
        if phase and phase.group(1) == "6":
            return _sections(match.group(1)).get("amendments", "")
    return None


def record(report: str, key: dict, label: str) -> dict:
    """One run's results, in the form a baseline file keeps."""
    results = extract(report)
    return {
        "label": label,
        "phases": results.phases,
        "mode": results.mode,
        "tier": results.tier,
        "blast_radius": results.blast_radius,
        "audience": results.audience,
        "statuses": dict(sorted(results.statuses.items())),
        "tally": results.tally,
        "checks": {check.name: check.passed for check in grade(report, key)},
    }


def compare(report: str, key: dict, baseline: dict) -> list[str]:
    """How a run differs from every run in the baseline. A value any baseline run gave matches."""
    current = record(report, key, "this run")
    runs = baseline["runs"]
    differences = []
    for name in ("mode", "tier", "blast_radius", "audience"):
        seen = {run[name] for run in runs}
        if current[name] not in seen:
            differences.append(f"{name}: {current[name]}; the baseline gave {_listed(seen)}")
    for n in DIMENSIONS:
        seen = {run["statuses"].get(n) for run in runs}
        if current["statuses"].get(n) not in seen:
            differences.append(
                f"dimension {n}: {current['statuses'].get(n)}; the baseline gave {_listed(seen)}"
            )
    for name, passed in current["checks"].items():
        if passed is not True and all(run["checks"].get(name) is True for run in runs):
            differences.append(f"{name}: passed in every baseline run, and not in this one")
    return differences


def _listed(values: set) -> str:
    return ", ".join(sorted(str(value) for value in values))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m skillcheck.parity",
        description="Build parity-run samples, and grade a run's report.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("materialize", help="build a sample as a git repository")
    build.add_argument("sample", type=Path)
    build.add_argument("dest", type=Path)
    for name, helptext in (
        ("grade", "check a report against its answer key"),
        ("record", "print a report's results, for the baseline"),
        ("compare", "compare a report with the baseline"),
    ):
        command = commands.add_parser(name, help=helptext)
        command.add_argument("report", type=Path)
        command.add_argument("key", type=Path)
        if name == "record":
            command.add_argument("--label", required=True)
        if name == "compare":
            command.add_argument("baseline", type=Path)
    args = parser.parse_args(argv)

    if args.command == "materialize":
        print(materialize(load_yaml(args.sample), args.dest))
        return 0
    report = args.report.read_text(encoding="utf-8")
    key = load_yaml(args.key)
    if args.command == "grade":
        checks = grade(report, key)
        for check in checks:
            mark = {True: "PASS", False: "FAIL", None: "----"}[check.passed]
            print(f"{mark} {check.name}: {check.detail}")
        return 0 if all(check.passed for check in checks) else 1
    if args.command == "record":
        print(yaml.safe_dump(record(report, key, args.label), sort_keys=False), end="")
        return 0
    differences = compare(report, key, load_yaml(args.baseline))
    for difference in differences:
        print(difference)
    print(f"{len(differences)} difference(s) from the baseline")
    return 1 if differences else 0


if __name__ == "__main__":
    sys.exit(main())
