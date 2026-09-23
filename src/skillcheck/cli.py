"""Command-line entry point: ``skillcheck [ROOT]``."""

import argparse
from pathlib import Path

from skillcheck.core.checks import check_repository


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="skillcheck", description="Check the skills and plugin catalog in a repository."
    )
    parser.add_argument(
        "root", nargs="?", default=".", type=Path, help="repository root (default: .)"
    )
    args = parser.parse_args(argv)
    if not args.root.is_dir():
        # A missing root would otherwise report zero findings, which reads as a pass.
        parser.error(f"{args.root} is not a directory")

    report = check_repository(args.root)
    for finding in report.findings:
        print(f"{finding.path}: {finding.rule}: {finding.message}")
    # Always printed, so a run that checked nothing says so rather than looking like a pass.
    print(report.summary())
    return 1 if report.findings else 0
