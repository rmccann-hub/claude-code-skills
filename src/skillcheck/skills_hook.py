"""Copies the skills of REPOSITORY's newest release into ``~/.claude/skills``.

A cloud environment's setup script installs this file as a hook that runs as each session starts
or resumes (``cloud-setup.sh``), so every session there loads the released skills with no upload.
It runs on whatever ``python3`` the machine has, so it uses only the standard library.

It never stops a session: on any failure it keeps the skills already installed and says why on
stderr. It replaces and removes only the skills its ledger says it installed, and leaves alone a
skill of the same name that someone else put there. When the claude.ai account still has its own
copy of one, which loads beside it under another name, it tells the session, on stdout, to have
the user delete that copy.
"""

import io
import json
import re
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

URL = "https://github.com/REPOSITORY/releases/latest/download/skills.zip"
# The release's own list of what it holds: {"version": "1.4.0", "skills": ["name", ...]}.
MANIFEST = "release.json"
LEDGER = ".claude-code-skills.json"
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def main(url: str = URL, home: Path | None = None) -> int:
    skills = (home or Path.home()) / ".claude" / "skills"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            names = install(response.read(), skills)
    except Exception as error:  # an update that fails must never stop the session
        print(f"claude-code-skills: kept the skills already installed: {error}", file=sys.stderr)
        return 0
    # Skills synced from claude.ai sit under skills/synced/<account>/<name>.
    doubled = [name for name in names if any(skills.glob(f"synced/*/{name}/SKILL.md"))]
    if doubled:
        print(
            "claude-code-skills: the claude.ai account still has its own copy of "
            f"{', '.join(doubled)}, which loads beside the released one under a prefix such as "
            "anthropic-skills:. Use the unprefixed one, and ask the user to delete the old copy "
            "on claude.ai, under Customize, then Skills, with any skill that depends on it."
        )
    return 0


def install(data: bytes, skills: Path) -> list[str]:
    """Install the archive's skills, unless the ledger says this release is already there.

    Returns the skills this hook now looks after.
    """
    archive = zipfile.ZipFile(io.BytesIO(data))
    version, names = _manifest(archive)
    ledger = skills / LEDGER
    owned = json.loads(ledger.read_text(encoding="utf-8")) if ledger.is_file() else {}
    mine = {name for name in owned.get("skills", []) if NAME.fullmatch(name)}
    if owned.get("version") == version and all((skills / name).is_dir() for name in mine):
        return sorted(mine)
    skills.mkdir(parents=True, exist_ok=True)
    # Unpacked beside the skills folder, not in it, so a session never lists a half-copied skill.
    staging = Path(tempfile.mkdtemp(prefix=".skills-", dir=skills.parent))
    try:
        for info in archive.infolist():
            archive.extract(info, staging)
            if info.external_attr >> 16 & 0o111:
                (staging / info.filename).chmod(0o755)
        installed = []
        for name in names:
            target = skills / name
            if target.exists() and name not in mine:
                print(
                    f"claude-code-skills: left {target} alone: it isn't one this hook installed",
                    file=sys.stderr,
                )
                continue
            if target.exists():
                shutil.rmtree(target)
            (staging / name).rename(target)
            installed.append(name)
        # A skill the newest release no longer ships is removed, as a release removes it.
        for name in mine - set(names):
            shutil.rmtree(skills / name, ignore_errors=True)
        ledger.write_text(json.dumps({"version": version, "skills": installed}) + "\n", "utf-8")
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    return installed


def _manifest(archive: zipfile.ZipFile) -> tuple[str, list[str]]:
    """The release's version and skills, once every entry is checked to sit inside one of them."""
    manifest = json.loads(archive.read(MANIFEST))
    version, names = manifest.get("version"), manifest.get("skills")
    if not isinstance(version, str) or not isinstance(names, list) or not names:
        raise ValueError(f"{MANIFEST} needs a version and a list of skills")
    for name in names:
        if not isinstance(name, str) or not NAME.fullmatch(name):
            raise ValueError(f"{MANIFEST} names {name!r}, which isn't a skill's name")
    entries = archive.namelist()
    for entry in entries:
        parts = entry.split("/")
        if entry != MANIFEST and (parts[0] not in names or ".." in parts or "\\" in entry):
            raise ValueError(f"the archive holds {entry}, outside its skills")
    for name in names:
        if f"{name}/SKILL.md" not in entries:
            raise ValueError(f"the archive has no {name}/SKILL.md")
    return version, names


if __name__ == "__main__":
    sys.exit(main())
