#!/usr/bin/env python3
"""Check a repository's evidence branch and manifest, as the standard's *Generated evidence* sets.

Run it in a local repository that holds both the default branch and the evidence branch, such
as a temporary bare repository:

    git clone --bare --single-branch --branch main <url> /tmp/check
    git -C /tmp/check fetch origin evidence:refs/heads/evidence
    python3 verify_evidence.py --repo /tmp/check

It reads Git only, writes nothing, and needs Python 3.11 or later and nothing else. It exits 0
when every check passes, 1 when any fails, and 2 when it couldn't check, so "couldn't check"
never reads as a pass. Rulesets and CI are GitHub's to report, and aren't checked here.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

HEADER = ["path", "bytes", "sha256", "evidence_commit", "last_default_commit"]


class CannotCheck(Exception):
    """An input the checks need is missing, so nothing can be said either way."""


@dataclass
class Result:
    failures: list[str] = field(default_factory=list)
    lines: list[str] = field(default_factory=list)

    def check(self, ok: bool, label: str, detail: str = "") -> None:
        self.lines.append(f"{'ok  ' if ok else 'FAIL'} {label}{': ' + detail if detail else ''}")
        if not ok:
            self.failures.append(label)

    def note(self, text: str) -> None:
        self.lines.append(f"info {text}")


class Git:
    def __init__(self, repo: Path) -> None:
        self.repo = repo

    def run(self, *args: str, ok_codes: tuple[int, ...] = (0,), data: bytes | None = None) -> bytes:
        res = subprocess.run(
            ["git", "-C", str(self.repo), *args], input=data, capture_output=True, check=False
        )
        if res.returncode not in ok_codes:
            raise CannotCheck(
                f"git {' '.join(args)}: {res.stderr.decode(errors='replace').strip()}"
            )
        return res.stdout

    def text(self, *args: str) -> str:
        return self.run(*args).decode().strip()

    def status(self, *args: str) -> int:
        return subprocess.run(
            ["git", "-C", str(self.repo), *args], capture_output=True, check=False
        ).returncode

    def blobs(self, specs: list[str]) -> dict[str, tuple[str, bytes] | None]:
        """Each `<commit>:<path>` mapped to its blob ID and content, or None where it's missing."""
        out = self.run("cat-file", "--batch", data="".join(s + "\n" for s in specs).encode())
        found: dict[str, tuple[str, bytes] | None] = {}
        pos = 0
        for spec in specs:
            end = out.index(b"\n", pos)
            head = out[pos:end].decode(errors="replace")
            pos = end + 1
            if head.endswith(" missing"):
                found[spec] = None
                continue
            oid, kind, size = head.split(" ")
            body = out[pos : pos + int(size)]
            pos += int(size) + 1
            found[spec] = (oid, body) if kind == "blob" else None
        return found


def verify(
    git: Git,
    default: str,
    evidence: str,
    manifest: str,
    identity: str | None = None,
    instant: str | None = None,
) -> Result:
    r = Result()
    for ref in (default, evidence):
        if git.status("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}") != 0:
            raise CannotCheck(f"no commit at {ref}; fetch it first")

    # The branch: an orphan root, one parent per commit after it, and no tag reaching it.
    # Only the branch's own commits: a parent on the default branch would otherwise lead the
    # walk into that branch's history, whose root has no parent either.
    shas = git.text("rev-list", "--reverse", "--parents", evidence, "--not", default).splitlines()
    if not shas:
        raise CannotCheck(f"{evidence} has no commits of its own; it's inside {default}'s history")
    first = shas[0].split()
    r.check(len(first) == 1, "the first evidence commit has no parent", first[0][:12])
    chained = all(
        len(line.split()) == 2 and line.split()[1] == shas[i].split()[0]
        for i, line in enumerate(shas[1:])
    )
    r.check(
        chained,
        "each later evidence commit has the one before as its only parent",
        f"{len(shas)} commit(s)",
    )
    ids = {line.split()[0] for line in shas}
    tags = git.text("tag", "--merged", evidence)
    r.check(not tags, "no tag reaches the evidence branch", tags.replace("\n", ", "))
    r.check(
        git.status("merge-base", default, evidence) == 1,
        "the evidence branch shares no history with the default branch",
    )
    if identity or instant:
        fmt = "%an <%ae>|%cn <%ce>|%aI|%cI"
        an, cn, ad, cd = git.text("show", "-s", f"--format={fmt}", first[0]).split("|")
        if identity:
            r.check(
                an == identity and cn == identity,
                "the move commit's author and committer are the pinned identity",
                an,
            )
        if instant:
            want = _instant(instant)
            r.check(
                _instant(ad) == want and _instant(cd) == want,
                "the move commit's dates are the pinned instant",
                ad,
            )

    # The manifest on the default branch.
    spec = f"{default}:{manifest}"
    found = git.blobs([spec])[spec]
    if found is None:
        raise CannotCheck(f"no {manifest} on {default}")
    rows = list(csv.reader(io.StringIO(found[1].decode("utf-8")), delimiter="\t"))
    if not rows:
        raise CannotCheck(f"{manifest} is empty")
    header, rows = rows[0], rows[1:]
    r.check(header == HEADER, "the manifest's header", "\t".join(header))
    if header != HEADER:
        return r
    short = [i + 2 for i, row in enumerate(rows) if len(row) != len(HEADER)]
    r.check(not short, "every manifest row has five fields", f"lines {short[:5]}" if short else "")
    rows = [row for row in rows if len(row) == len(HEADER)]
    paths = [row[0] for row in rows]
    r.check(paths == sorted(paths), "the manifest is sorted by path")
    r.check(len(paths) == len(set(paths)), "one manifest row per path", f"{len(rows)} row(s)")
    r.check(all(row[3] in ids for row in rows), "every row's evidence commit is on the branch")

    # Each row against its evidence commit, by size and SHA-256, and against its source.
    lookups = [f"{row[3]}:{row[0]}" for row in rows]
    lookups += [f"{row[4]}:{row[0]}" for row in rows if row[4]]
    lookups += [f"{default}:{row[0]}" for row in rows]
    blobs = git.blobs(lookups)
    absent, size, digest, source, changed, kept = [], [], [], [], [], []
    for path, nbytes, sha256, ev, src in rows:
        entry = blobs[f"{ev}:{path}"]
        if entry is None:
            absent.append(path)
            continue
        oid, body = entry
        if str(len(body)) != nbytes:
            size.append(path)
        if hashlib.sha256(body).hexdigest() != sha256:
            digest.append(path)
        if src and (blobs[f"{src}:{path}"] or ("", b""))[0] != oid:
            source.append(path)
        tip = blobs[f"{default}:{path}"]
        if tip is not None:
            (kept if tip[0] == oid else changed).append(path)
    r.check(not absent, "every row's file is in its evidence commit", ", ".join(absent[:3]))
    r.check(not size, "every row's size matches its file", ", ".join(size[:3]))
    r.check(not digest, "every row's SHA-256 matches its file", ", ".join(digest[:3]))
    r.check(
        not source,
        "every moved file is the same blob as in its source commit",
        ", ".join(source[:3]),
    )
    r.check(
        not changed,
        "no row's path holds a different file on the default branch",
        ", ".join(changed[:3]),
    )
    r.note(f"{len(kept)} file(s) on both branches, such as each folder's README")
    return r


def _instant(text: str) -> str:
    from datetime import datetime

    return datetime.fromisoformat(text.replace("Z", "+00:00")).isoformat()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--repo", type=Path, default=Path("."), help="a local repository")
    p.add_argument("--default", default="main", help="the default branch's ref")
    p.add_argument("--evidence", default="evidence", help="the evidence branch's ref")
    p.add_argument("--manifest", default="docs/evidence-manifest.tsv")
    p.add_argument("--identity", help='the move commit\'s pinned identity, "name <email>"')
    p.add_argument("--instant", help="the move commit's pinned instant, ISO 8601")
    a = p.parse_args(argv)
    try:
        r = verify(Git(a.repo), a.default, a.evidence, a.manifest, a.identity, a.instant)
    except CannotCheck as exc:
        print(f"couldn't check: {exc}", file=sys.stderr)
        return 2
    print("\n".join(r.lines))
    print(f"{len(r.failures)} check(s) failed" if r.failures else "every check passed")
    return 1 if r.failures else 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover - the command test runs this line in a subprocess
