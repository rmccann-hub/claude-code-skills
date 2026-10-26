"""Copies the skills of REPOSITORY's newest release into ``~/.claude/skills``.

A cloud environment's setup script installs this file as a hook that runs as each session starts
or resumes (``cloud-setup.sh``), so every session there loads the released skills with no upload.
It runs on whatever ``python3`` the machine has, so it uses only the standard library.

It never stops a session: on any failure it keeps the skills already installed and says why on
stderr. It installs a release only once the release's signed build attestation names the
archive's digest and this repository's release workflow, and only when the attestation's
signature checks out with ``gh attestation verify``, where ``gh`` is installed; with no ``gh``, it
checks the digest and the claims, not the signature, and says so. It refuses an older release
than the one installed. It replaces and removes only the skills its ledger says it installed,
and leaves alone a skill of the same name that someone else put there. When the claude.ai account
still has its own copy of one, which loads beside it under another name, it tells the session,
on stdout, to have the user delete that copy.
"""

import base64
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

URL = "https://github.com/REPOSITORY/releases/latest/download/skills.zip"
# The release's Sigstore bundle, beside the archive: an in-toto statement, signed in the
# release workflow, that names each file's SHA-256 and the workflow that built it.
ATTESTATION = "attestation.sigstore.json"
WORKFLOW = "https://github.com/REPOSITORY", ".github/workflows/release.yml"
# The release's own list of what it holds: {"version": "1.4.0", "skills": ["name", ...]}.
MANIFEST = "release.json"
LEDGER = ".claude-code-skills.json"
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
# Characters that render as nothing or reorder text, so what a reviewer saw differs from what an
# agent reads. The same as ``skillcheck.core.text.HIDDEN``, which a test keeps equal: this file
# runs on its own, without that package. A release already passed the check; the hook checks
# again because what arrives is what the session reads.
HIDDEN = re.compile(
    "[\u00ad\u180e\u200b-\u200f\u202a-\u202e\u2060-\u2064\u2066-\u2069\ufeff\U000e0000-\U000e007f]"
)


def main(url: str = URL, home: Path | None = None) -> int:
    skills = (home or Path.home()) / ".claude" / "skills"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()
        beside = f"{url.rsplit('/', 1)[0]}/{ATTESTATION}"
        with urllib.request.urlopen(beside, timeout=30) as response:
            bundle = response.read()
        names = install(data, skills, bundle)
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


def install(data: bytes, skills: Path, bundle: bytes) -> list[str]:
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
    installed_version = owned.get("version")
    if isinstance(installed_version, str) and _order(version) < _order(installed_version):
        raise ValueError(f"{version} is older than {installed_version}, which is installed")
    _attested(data, bundle)
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


def _order(version: str) -> tuple:
    """A version's place in Semantic Versioning's order, as far as numbers and a pre-release go."""
    core, _, pre = version.partition("-")
    numbers = tuple(int(n) if n.isdigit() else -1 for n in core.split("."))
    return numbers, not pre, pre


def _attested(data: bytes, bundle: bytes) -> None:
    """Refuse an archive the release's attestation doesn't name, built by another workflow."""
    digest = hashlib.sha256(data).hexdigest()
    for line in bundle.decode("utf-8").splitlines():
        if not line.strip():
            continue
        envelope = json.loads(line).get("dsseEnvelope", {})
        statement = json.loads(base64.b64decode(envelope.get("payload", "")))
        subjects = {s.get("name"): s.get("digest", {}).get("sha256") for s in statement["subject"]}
        workflow = (
            statement.get("predicate", {})
            .get("buildDefinition", {})
            .get("externalParameters", {})
            .get("workflow", {})
        )
        claimed = workflow.get("repository"), workflow.get("path")
        if subjects.get("skills.zip") == digest and claimed == WORKFLOW:
            break
    else:
        raise ValueError(f"no attestation from {WORKFLOW[1]} names this skills.zip, {digest}")
    gh = shutil.which("gh")
    if gh is None:
        print(
            "claude-code-skills: matched the attestation's digest and workflow; its signature "
            "isn't checked without gh",
            file=sys.stderr,
        )
        return
    with tempfile.TemporaryDirectory() as folder:
        archive, signed = Path(folder, "skills.zip"), Path(folder, ATTESTATION)
        archive.write_bytes(data)
        signed.write_bytes(bundle)
        repository = WORKFLOW[0].removeprefix("https://github.com/")
        command = [gh, "attestation", "verify", str(archive), "--bundle", str(signed)]
        command += ["--repo", repository, "--signer-workflow", f"{repository}/{WORKFLOW[1]}"]
        done = subprocess.run(command, capture_output=True, text=True, timeout=60, check=False)
    if done.returncode != 0:
        # gh's own words, escaped by !r: they can quote what the bundle holds.
        said = (done.stderr or done.stdout).strip().splitlines() or [f"exit {done.returncode}"]
        raise ValueError(f"gh attestation verify refused it: {said[-1]!r}")


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
            raise ValueError(f"the archive holds {entry!r}, outside its skills")
        try:
            text = archive.read(entry).decode("utf-8")
        except UnicodeDecodeError:  # an image or another binary file has no text to hide in
            continue
        hidden = HIDDEN.search(text)
        if hidden:
            raise ValueError(f"{entry!r} holds U+{ord(hidden.group()):04X}, a hidden character")
    for name in names:
        if f"{name}/SKILL.md" not in entries:
            raise ValueError(f"the archive has no {name}/SKILL.md")
    return version, names


if __name__ == "__main__":
    sys.exit(main())
