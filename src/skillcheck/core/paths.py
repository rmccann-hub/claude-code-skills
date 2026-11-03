"""Which files under a scanned directory belong to the repository."""

from pathlib import Path

# Claude Code makes an agent's isolated copy of the repository under `.claude/worktrees/`, and
# `.gitignore` leaves it out. Its files are another checkout's, so scanning them reports that
# checkout's state as this one's.
WORKTREES = Path(".claude") / "worktrees"


def files_under(root: Path, directory: str, suffixes: set[str] | None = None) -> list[Path]:
    """Every file under `root / directory`, sorted, with agents' worktrees left out."""
    base = root / directory
    if not base.is_dir():
        return []
    skip = root / WORKTREES
    return sorted(
        p
        for p in base.rglob("*")
        if p.is_file() and skip not in p.parents and (suffixes is None or p.suffix in suffixes)
    )
