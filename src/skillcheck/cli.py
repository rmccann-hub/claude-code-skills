"""Command-line entry point: ``skillcheck [ROOT] [MODE]``.

The modes are ``--due [DATE]``, ``--verify``, ``--bom``, ``--bom-check`` and
``--release-assets VERSION DIR``, one at a time. With none, it runs every rule on the repository.
"""

import argparse
from datetime import date
from pathlib import Path

from skillcheck import bom, release
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
    # The dependency map changes whenever a lockfile does, and a Dependabot pull request can't
    # rebuild it, so these two run by hand, weekly and at release rather than on pull requests.
    mode.add_argument(
        "--bom",
        action="store_true",
        help=f"write the dependency map: {bom.BOM} and {bom.MAP}",
    )
    mode.add_argument(
        "--bom-check",
        action="store_true",
        help="name each dependency-map file that no longer matches the repository",
    )
    mode.add_argument(
        "--release-assets",
        nargs=2,
        metavar=("VERSION", "DIR"),
        help="build what a release of VERSION publishes beside its tag, into DIR",
    )
    args = parser.parse_args(argv)
    if not args.root.is_dir():
        # A missing root would otherwise report zero findings, which reads as a pass.
        parser.error(f"{args.root} is not a directory")
    if args.due is not None:
        return _due(args.root, args.due)
    if args.verify:
        return _verify(args.root)
    if args.bom:
        for path in bom.write(args.root):
            print(f"wrote {path}")
        print(f"skillcheck: dependency map written, {_summary(args.root)}")
        return 0
    if args.release_assets:
        return _release(args.root, *args.release_assets)
    if args.bom_check:
        old = bom.stale(args.root)
        for path in old:
            print(f"{path}: bom: out of date; run `uv run skillcheck --bom`")
        print(f"skillcheck: dependency map, {_summary(args.root)}, {len(old)} file(s) out of date")
        return 1 if old else 0

    report = check_repository(args.root)
    for finding in report.findings:
        print(f"{finding.path}: {finding.rule}: {finding.message}")
    # Always printed, so a run that checked nothing says so rather than looking like a pass.
    print(report.summary())
    return 1 if report.findings else 0


def _release(root: Path, version: str, out: str) -> int:
    found = release.problems(root, version)
    for problem in found:
        print(f"release: {problem}")
    if not found:
        try:
            for name in release.build(root, version, Path(out)):
                print(f"wrote {Path(out) / name}")
        except release.ReleaseError as error:
            print(f"release: {error}")
            found = [str(error)]
    print(f"skillcheck: release {version}, {len(found)} problem(s)")
    return 1 if found else 0


def _summary(root: Path) -> str:
    inventory = bom.collect(root)
    parts = len(inventory.packages) + len(inventory.tools) + len(inventory.actions)
    return f"{parts} dependencies, {len(inventory.services)} services"


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
