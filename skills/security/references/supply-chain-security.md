# Supply chain security

Read this for adding a dependency, installing from a lockfile, building a dependency from
source, writing code that downloads and installs an update, or publishing artifacts others
install: checking a package is real and the one meant, pinning to a full commit, verifying
provenance, and refusing an update that can't be verified.

It covers what code and agents do with other people's code. How a repository configures its
update bot, its cooldown, Scorecard and its inbound licenses is the standard's *Dependencies*
dimension, and this module doesn't restate it. Pinning GitHub Actions is `actions-security`; a
secret that reached a commit is `leaked-data`; tags, changelogs and version numbers are
`releases-and-versions`.

<!-- Draft, 2026-10-26. Built from research R05 (2026-09-23), checked again for each fact used
here, and lessons L51 and L53 in ROADMAP.md. Not reviewed under docs/authoring-a-skill.md yet. -->

## Rules

1. **Before adding a package, check it exists and is the one meant.** Read its registry page,
   its repository and its maintainers. A name a model suggested may not exist, or may have been
   registered by someone waiting for that suggestion (fact `package-hallucination`).
2. **Install from the lockfile, frozen,** so an install can't quietly resolve something new:
   `npm ci` (fact `npm-ci`), `uv sync --locked` (fact `uv-locked`), pip with hashes (fact
   `pip-require-hashes`).
3. **Give a new release time before it installs,** at install time as well as in the update
   bot: the bot's wait doesn't stop an install pulling a new transitive version. pnpm waits a
   day by default (fact `pnpm-release-age`); uv takes a cutoff date (fact `uv-exclude-newer`).
4. **Don't run dependencies' install scripts by default.** Allow them by name for the packages
   that need them (fact `pnpm-scripts-off`).
5. **Build from source at a full commit SHA, check the commit you landed on, and refuse a dirty
   tree.** A short SHA names whatever is unique today (fact `git-short-sha`), and a dirty tree
   builds code the pin doesn't name.
6. **Code that installs an update verifies who built it, not only that it arrived intact.** A
   checksum published beside a file can be replaced with the file. Verify a signed provenance
   attestation (facts `artifact-attestations`, `gh-attestation-verify`), fail closed, and
   refuse a version older than the one installed.
7. **Publish what others install with provenance,** in an immutable release (fact `immutable`),
   so they can apply rule 6 to you.

### Adding a dependency

- **Name the need first,** and check whether the standard library or a dependency already in
  the project covers it. Each new package is code you now run, and its own dependencies too.
  TODO(new-skill) The fewest-dependencies rule, from research R21 when it's run.
- **Check the name letter by letter** against the project's own documentation, not a search
  result or a model's memory. Typosquats differ by one character, and an assistant's
  suggestion can name a package that has never existed.
- **Read it before it's load-bearing,** as the standard's *Reading a dependency's source*
  says, and pin the version you read.

### Installing

- **CI and release builds install frozen,** and fail when the lockfile and the manifest
  disagree, rather than updating the lockfile in passing.
- **Hash-checked installs where the tool has them.** pip's hash-checking mode needs a hash for
  every requirement, so an unpinned one fails (fact `pip-require-hashes`).
- TODO(new-skill) The per-ecosystem table of lockfiles and their frozen install commands: Cargo,
  Go, NuGet, Composer, Bundler, pnpm and Yarn. Research R05 left it out.

### Building from source

Pin the full SHA, fetch it, and check both the commit and the tree before building:

```sh
src=build/dependency
pin=<full-commit-sha>
git -C "$src" fetch --depth 1 origin "$pin"
git -C "$src" checkout --detach "$pin"
if [ "$(git -C "$src" rev-parse HEAD)" != "$pin" ]; then
  echo "not the pinned commit" >&2
  exit 1
fi
if [ -n "$(git -C "$src" status --porcelain)" ]; then
  echo "the source tree is dirty" >&2
  exit 1
fi
```

- **Record the commit in what you build,** and mark a build from a dirty tree so nothing
  downstream treats it as the release it was cut from.

### Installing updates from code

- **Provenance over checksums.** Check the attestation's signer: the repository and the workflow
  that built it, not only that a signature exists (fact `gh-attestation-verify`).
- **Fail closed.** No attestation, a signer you didn't expect, or a verifier that errors all
  mean no install. Say which, and keep the installed version.
- **No downgrades.** A genuine older build served as a newer one passes provenance; compare
  versions and refuse.
- TODO(new-skill) npm provenance and PyPI's attestations, checked by the installer: research
  R05 didn't verify how either is checked.

## Mistakes

- **Installing a package because a model named it.** It may not exist, or may be someone's trap
  for that name (fact `package-hallucination`). Check the registry and the repository first.
- **`npm install` in CI,** which can rewrite the lockfile. Use `npm ci` (fact `npm-ci`).
- **`uv sync --frozen` where `--locked` was meant:** `--frozen` skips the check that the
  lockfile is current (fact `uv-locked`).
- **Configuring the bot's cooldown and not the installer's, or the reverse.** Each guards a
  different path.
- **Pinning a source build to a short SHA,** or checking out the pin and building without
  comparing the commit or checking the tree.
- **Verifying a download against a checksum from the same release.** It proves the file
  arrived whole, not who made it.
- **Warning on a dirty tree and building anyway.** The build then names a commit it wasn't
  built from.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| CI installs frozen | The install step: `npm install`, `pip install` without hashes, `uv sync` without `--locked` | `GAP` | The frozen command (rule 2) |
| A source build pinned by a short SHA | Build scripts' checkouts: a pin under 40 characters, or no comparison with `rev-parse HEAD` | `GAP` | The full SHA, compared (rule 5) |
| A dirty tree only warns | Build scripts that check `status --porcelain` and carry on | `GAP` | Stop the build (rule 5) |
| An updater checks a checksum only | Code that downloads and installs a release | `GAP`; `BLOCKER` where the install runs with the user's rights and the checksum comes from the same place as the file | Verify provenance, fail closed (rule 6) |
| An updater installs an older version | The version comparison before install | `GAP` | Refuse a downgrade (rule 6) |
| Releases others install carry no provenance | The release workflow | `GAP` at T2 and above | Attest each artifact (rule 7) |
| Install scripts run by default | The package manager's settings | `DRIFT` | Allow by name (rule 4) |

## Why

### Checking a package is real before adding it

- **The advice:** check the registry, the repository and the maintainers before adding a
  package, whatever suggested it.
- **The reason:** code-generating models name packages that don't exist. One study found at
  least 5.2% of suggested packages were hallucinated for commercial models and 21.7% for
  open-source ones, across 205,474 unique names (fact `package-hallucination`). Anyone can
  register a name a model keeps suggesting, and the next install runs their code.
- **What others do, and why:** TODO(new-skill) Registries' and tools' defenses against
  hallucinated and typosquatted names, from research R01 and R21.
- **What it costs:** a minute per package, and a slower first draft.
- **When to choose differently:** never for a new name. A package already in the lockfile, at a
  version someone read, has had this check.

### Pinning and checking a source build

- **The advice:** pin the full SHA, compare the commit you landed on, and stop on a dirty tree.
- **The reason:** git resolves a short SHA to whatever object is unique by that prefix today
  (fact `git-short-sha`), so the pin's meaning depends on what's been pushed since. A build
  script that warned on a dirty tree and built anyway produced a binary whose tag named a
  commit it wasn't built from (one app's build script, reviewed on 2026-10-26).
- **What others do, and why:** GitHub tells workflows to pin actions by full SHA for the same
  reason a tag is weaker (fact `sha-pin`).
- **What it costs:** a longer string in the script, and a failed build to investigate when the
  tree is dirty.
- **When to choose differently:** a developer's local build of their own work-in-progress may
  build dirty, if the result is marked and never shipped.

### Provenance, not a checksum beside the file

- **The advice:** code that installs an update verifies a signed attestation of who built it,
  checks the signer, fails closed and refuses a downgrade.
- **The reason:** whoever can replace a release's file can replace the checksum next to it. An
  attestation is signed through Sigstore by the workflow that built the file, so a file built
  anywhere else fails (facts `artifact-attestations`, `gh-attestation-verify`). One desktop app
  verifies these attestations before installing its own updates, and records the gaps it
  doesn't close: an unprotected default branch, and an older build served as newer.
- **What others do, and why:** many projects publish checksums only, which catch corruption in
  transit and nothing more.
- **What it costs:** a verifier in the installer, which needs the network and a library such as
  Sigstore's.
- **When to choose differently:** an installer that can't reach the transparency log, such as
  one offline, can pin a public key it ships with instead.

## Facts

Versions, dates and defaults, each named elsewhere in this module by its ID. Checked
2026-10-26.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `package-hallucination` | A study of code-generating models found at least 5.2% of suggested packages hallucinated for commercial models and 21.7% for open-source ones, with 205,474 unique hallucinated names; to appear at USENIX Security 2025 | [Spracklen et al., arXiv:2406.10279](https://arxiv.org/abs/2406.10279) | "the average percentage of hallucinated packages is at least 5.2% for commercial models and 21.7% for open-source models" | 2026-10-26 | 2027-10-26 |
| `npm-ci` | `npm ci` needs a lockfile, fails when it disagrees with `package.json`, and never writes either | [npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci) | "It will never write to package.json or any of the package-locks: installs are essentially frozen." | 2026-10-26 | 2027-04-26 |
| `pip-require-hashes` | pip's hash-checking mode needs a hash for every requirement, and an unlisted dependency is an error | [Secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/) | "If there is a dependency that is not spelled out and hashed in the requirements file, it will result in an error." | 2026-10-26 | 2027-04-26 |
| `pnpm-release-age` | pnpm's `minimumReleaseAge` defaults to 1440 minutes, so a version installs once it's a day old | [Supply chain security](https://pnpm.io/supply-chain-security) | "newly published packages will not be resolved until they are at least 1 day old" | 2026-10-26 | 2027-04-26 |
| `pnpm-scripts-off` | pnpm v10 doesn't run dependencies' `postinstall` scripts unless allowed | [Supply chain security](https://pnpm.io/supply-chain-security) | "pnpm v10 disables the automatic execution of `postinstall` scripts in dependencies" | 2026-10-26 | 2027-04-26 |
| `uv-exclude-newer` | uv's `exclude-newer` installs only what was uploaded before a date | [uv settings](https://docs.astral.sh/uv/reference/settings/) | "Limit candidate packages to those that were uploaded prior to the given date." | 2026-10-26 | 2027-04-26 |
| `git-short-sha` | git takes a full object name or any leading part of it that is unique in the repository | [gitrevisions](https://git-scm.com/docs/gitrevisions) | "or a leading substring that is unique within the repository" | 2026-10-26 | 2027-10-26 |
| `artifact-attestations` | GitHub Artifact Attestations, signed through Sigstore, are generally available | [GitHub changelog, 2024-06-25](https://github.blog/changelog/2024-06-25-artifact-attestations-is-generally-available/) | "We’re thrilled to announce the general availability of GitHub Artifact Attestations!" | 2026-10-26 | 2027-04-26 |
| `gh-attestation-verify` | `gh attestation verify` checks an artifact against its signed attestations, including the source repository and, with a flag, the signing workflow | [gh attestation verify](https://cli.github.com/manual/gh_attestation_verify) | "Verify the integrity and provenance of an artifact using its associated cryptographically signed attestations." | 2026-10-26 | 2027-04-26 |

## Sources

Every source, with its license and how this module uses it: quoted, adapted with a notice, or
stated in our own words with a link.

| Source | Used for | License |
|---|---|---|
| [Spracklen et al., arXiv:2406.10279](https://arxiv.org/abs/2406.10279) | How often models name packages that don't exist | arXiv's non-exclusive license: a fact with a short quote |
| [npm documentation](https://docs.npmjs.com/) | Frozen installs | TODO(new-skill) its license |
| [pip documentation](https://pip.pypa.io/) | Hash-checking mode | MIT: a fact with a short quote |
| [pnpm documentation](https://pnpm.io/) | Release age and install scripts | TODO(new-skill) its license |
| [uv documentation](https://docs.astral.sh/uv/) | Excluding new uploads | TODO(new-skill) its license |
| [Git documentation](https://git-scm.com/docs) | Short object names | GPL-2.0: a fact with a short quote |
| [GitHub changelog](https://github.blog/changelog/) and [GitHub CLI manual](https://cli.github.com/manual/) | Attestations and their verification | © GitHub, and the CLI's MIT: facts with short quotes |
| This repository's research R05, 2026-09-23 | Leads, each checked again at its source | This repository's own |
