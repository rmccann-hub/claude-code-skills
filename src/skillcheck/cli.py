"""Command-line entry point: ``skillcheck [ROOT] [--due [DATE] | --verify]``."""

import argparse
from datetime import date
from pathlib import Path

from skillcheck.core import facts
from skillcheck.core.checks import check_repository


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="skillcheck", description="Check the skills and plugin catalog in a repository."
    )
    parser.add_argument(
        "root", nargs="?", default=".", type=Path, help="repository root (default: .)"
    )
    # These two answer by the date and the network, so the scheduled freshness workflow runs
    # them. A pull request's checks depend only on the commit.
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--due",
        nargs="?",
        const=date.today(),
        type=_day,
        metavar="DATE",
        help="list the facts to check again by today, or by DATE (YYYY-MM-DD)",
    )
    mode.add_argument(
        "--verify",
        action="store_true",
        help="fetch each fact's source and look for its quote (uses the network)",
    )
    args = parser.parse_args(argv)
    if not args.root.is_dir():
        # A missing root would otherwise report zero findings, which reads as a pass.
        parser.error(f"{args.root} is not a directory")
    if args.due is not None:
        return _due(args.root, args.due)
    if args.verify:
        return _verify(args.root)

    report = check_repository(args.root)
    for finding in report.findings:
        print(f"{finding.path}: {finding.rule}: {finding.message}")
    # Always printed, so a run that checked nothing says so rather than looking like a pass.
    print(report.summary())
    return 1 if report.findings else 0


def _day(text: str) -> date:
    try:
        return date.fromisoformat(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{text!r} is not a YYYY-MM-DD date") from None


def _due(root: Path, by: date) -> int:
    found = facts.collect(root)
    due = [fact for fact in found if fact.check_by <= by]
    for fact in due:
        print(
            f"{fact.path}:{fact.line}: due: `{fact.id}` was to be checked again by {fact.check_by}"
        )
    print(f"skillcheck: {len(found)} fact(s), {len(due)} due by {by}")
    return 1 if due else 0


def _verify(root: Path) -> int:
    found = facts.collect(root)
    problems = list(facts.verify(found))
    for fact, problem in problems:
        print(f"{fact.path}:{fact.line}: verify: `{fact.id}`: {problem}")
    quoted = sum(1 for fact in found if fact.quotes)
    print(
        f"skillcheck: {len(found)} fact(s), {quoted} with a quote to look for, "
        f"{len(problems)} not confirmed"
    )
    return 1 if problems else 0
