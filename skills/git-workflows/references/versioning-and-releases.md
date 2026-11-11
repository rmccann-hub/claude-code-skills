# Versioning and releases

Read this for writing a release's notes for the people upgrading, publishing which versions get
fixes and until when, deciding whether to keep a long-term support line, shipping a security fix
with an advisory and a CVE, announcing a deprecation's timeline, or marking which release is the
latest when version numbers don't sort.

Tags, the release workflow, changelog entries, version numbers, and keeping and backporting to a
release line are `releases-and-versions`. The version scheme and deprecating before removing
are project-bootstrap-and-audit's rules (dimension 10). A leaked secret is `leaked-data`.

## Rules

1. **Write release notes from the changelog, for someone upgrading:** what they must do first,
   then security fixes, then the rest (fact `vr-kac-notes`).
2. **Publish the support window in one place:** for each line, bug fixes, security fixes or
   nothing, and until when. GitHub asks for it in `SECURITY.md` (fact `vr-security-md`).
3. **Give a line its end date when it ships,** or tie the end to a later release and date it
   then. Announce an end in the notes of each release before it.
4. **Keep a long-term support line only with the hands to backport to it for its whole life,**
   and CI that still builds it (fact `vr-node-lines`).
5. **Fix a reported vulnerability in a draft advisory, release, then publish the advisory with
   the fixed versions** (facts `vr-ghsa-flow`, `vr-ghsa-fix-version`).
6. **A deprecation names its replacement and the release that removes it,** in the warning, the
   changelog and each release's notes until it's gone (facts `vr-kac-removal`,
   `vr-pep387-message`).
7. **Say which release is latest** when you release an older line, and order releases whose
   versions don't sort by a sequence of their own (L24).

### Release notes

1. **Who must act:** each breaking change with its upgrade step or a link to the migration
   guide, each removal, a raised minimum runtime.
2. **Security:** each fix with its CVE or GHSA ID and a link to the advisory.
3. **New, then fixed,** in the user's words.
4. **Support:** a line whose end is now announced, or that ends with this release.
5. **The full record:** the version's changelog section and the compare view.

GitHub's generated notes list merged pull requests, contributors and a link (fact
`vr-generated-notes`): keep those, and write the part above them. Notes live in the host's
database (fact `vr-kac-notes`), so what must survive a move goes in `CHANGELOG.md`.

### Support periods

One table in `SECURITY.md`, changed in the release that changes support:

| Version | Gets | Until |
|---|---|---|
| 3.x | bug and security fixes | six months after 4.0.0 ships |
| 2.x | security fixes only | 2027-06-30 |
| 1.x | nothing | ended 2026-06-30 |

- **Two phases are common:** bug fixes, then security fixes only. Python ends support five years
  after a release (fact `vr-python-phases`), .NET gives an LTS three years and an STS two (fact
  `cs-support-policy`), and from 27 every Node release gets 36 months (fact
  `vr-node-schedule`).
- **"The latest release only" is a window.** Say it.
- **Extend a window freely; shorten one only as a breaking change,** announced like one.

### Long-term support lines

A line costs, for its whole life, every security fix backported to drifted code, CI that still
builds it as toolchains move on, and a release per fix. Node cut its lines for this (fact
`vr-node-lines`). LTS names a length, not a later end: .NET 8, an LTS, ended the same day as
.NET 9, an STS (fact `cs-dotnet8-9-end`).

### Security releases

project-bootstrap-and-audit asks for a security contact (dimension 7) and turns on private
vulnerability reporting (its settings table). Once a report arrives, in a public repository:

1. **Open a draft repository security advisory** with the affected versions. It stays private.
2. **Request a CVE from the draft** if there's none. GitHub is a CNA, usually answers within 72
   hours, and requesting doesn't publish (fact `vr-ghsa-cve`). Where another CNA covers the
   project, ask that one.
3. **Fix it in the advisory's temporary private fork,** one pull request per supported line.
   No status check runs there and branch protection isn't enforced (fact `vr-private-fork`), so
   run each line's suite yourself before merging.
4. **Merge, then release every line at once:** the merge puts the fix in public history. Each
   release still goes the normal route (`releases-and-versions`).
5. **Add the fixed versions to the advisory, then publish it.** Without them, Dependabot alerts
   users with no version to move to (fact `vr-ghsa-fix-version`).
6. **Lead the Security entry with the CVE** (`releases-and-versions`), and link the advisory.

### Deprecation timelines

- **The warning, the `Deprecated` entry and the notes** each name the replacement and the
  removing version (facts `vr-kac-removal`, `vr-pep387-message`).
- **Repeat it in each release's notes** until the removal, which goes under "Who must act".
- **Remove the old way only once every supported line has the new one,** so users on any
  supported line can move without a jump (fact `vr-pep387-support`).

### Which release is latest

- **A release on an older line:** `gh release create v2.8.4 --verify-tag --latest=false` (fact
  `vr-gh-latest`). Through the API, set `make_latest` to `"false"`: it defaults to marking each
  newly published release latest (fact `vr-make-latest`).
- **A fork whose only advancing part is build metadata** can't order its releases: SemVer
  ignores build metadata for precedence (fact `vr-semver-build`), so `1.4.0+fork.2` and
  `1.4.0+fork.3` tie. Give the fork a sequence of its own in the version, a counter or a date,
  and name upstream's version in the notes.

## Mistakes

- **Notes pasted from the generated pull request list,** with the breaking change halfway down
  under its pull request's title. Put it first, with its upgrade step.
- **An end of life announced in the release that ends the line.** Users learn it when fixes
  stop. Announce it in the releases before.
- **A reported vulnerability fixed in a public pull request,** disclosing it before any release
  exists. Use the advisory's private fork.
- **Merging the private fix, then releasing days later,** with the fix readable in history.
- **A backport release marked latest,** sending new users to an old line.
- **What AI assistants get wrong:** notes rewritten from commits, a support period nobody
  promised, and "removed in a future release".

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| A support window is published | `SECURITY.md` or the docs give each line's status and end | `GAP` where others depend on it; `N/A` before a first release | Add the table |
| The window matches the releases | The table against `gh release list` and the release branches | `DRIFT` | Update it in the next release |
| Breaking changes lead the notes | `gh release view vX.0.0`, the last major release | `GAP` | Rewrite them from the changelog |
| A shipped security fix has an advisory | Security changelog entries against `gh api repos/OWNER/REPO/security-advisories --jq '.[].ghsa_id'` | `GAP` in a public repository; `UNVERIFIABLE-HERE` for a private one without access | Publish one with the fixed versions |
| The latest release is on the newest line | `gh release view --json tagName` against the highest version | `DRIFT` | `gh release edit <tag> --latest` |
| Deprecations name their removal | `Deprecated` entries in `CHANGELOG.md` | `GAP` | Add the replacement and the version |

## Why

### Release notes from the changelog

Keep a Changelog 2.0.0 draws release notes from the changelog (fact `vr-kac-notes`); two
documents kept by hand drift. Many projects publish GitHub's generated notes as they come (fact
`vr-generated-notes`): free, but sorted by pull request, not by what a reader must do. An app
whose users never see a changelog may need notes only.

### Support periods and long-term lines

Without a published window, each user guesses, and a security fix reaches some lines and not
others with no warning. Python's end falls five years after each release (fact
`vr-python-phases`), so users plan from the day it ships. A window is a promise kept in public,
so a small project's is often the latest release only. Each extra line multiplies every security
fix (fact `vr-node-lines`). Keep one for users who can't upgrade on your schedule, such as
embedded, regulated or pinned installs; where upgrading is cheap, make upgrades safe instead.

### The security release order

A published advisory may alert dependents through Dependabot (fact `vr-ghsa-flow`), so one with
no fixed version alerts users with nowhere to go (fact `vr-ghsa-fix-version`). The private fork
keeps the fix out of public history, at the price of no checks until it merges (fact
`vr-private-fork`). Where no fix is planned, GitHub advises saying so in the advisory, with
steps users can take (fact `vr-ghsa-flow`).

### Deprecation timelines

A warning without a version gives no deadline, and a removal before the last line without the
replacement ends forces a jump. Python's policy rules out both (facts `vr-pep387-message`,
`vr-pep387-support`), at the cost of two code paths for the period. Before 1.0.0, or for a
security fix, removal may come sooner; say so in the notes.

### Which release is latest

The API marks each new release latest (fact `vr-make-latest`). An audited fork's releases
advanced only in build metadata, which SemVer can't order (fact `vr-semver-build`). Its own
sequence costs a version that no longer mirrors upstream's alone.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `vr-kac-notes` | Notes come from the changelog; a host keeps releases in its own database | [Keep a Changelog 2.0.0](https://keepachangelog.com/en/2.0.0/) | "The changelog is the source; release notes are drawn from it" and "everything is stored in the host's database, not your repository" | 2026-11-11 | 2027-05-11 |
| `vr-kac-removal` | A deprecation names the removing version | [Keep a Changelog 2.0.0](https://keepachangelog.com/en/2.0.0/) | "Say which version will remove it, so they can plan." | 2026-11-11 | 2027-05-11 |
| `vr-generated-notes` | Generated notes: pull requests, contributors, a link | [Generated release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes) | "include a list of merged pull requests, a list of contributors to the release, and a link to a full changelog" | 2026-11-11 | 2027-02-11 |
| `vr-security-md` | GitHub asks `SECURITY.md` for supported versions | [Security policy](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/add-security-policy) | "add information about supported versions of your project" | 2026-11-11 | 2027-02-11 |
| `vr-python-phases` | Python: bug fixes, then security only, to five years | [Python versions](https://devguide.python.org/versions/) | "only security fixes are accepted" and "Five years after a release, support ends." | 2026-11-11 | 2027-02-11 |
| `vr-node-schedule` | Node 27 on: every release LTS, 36 months | [Node's schedule](https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule) | "Every release becomes LTS" and "36 months from first Current release to End of Life" | 2026-11-11 | 2027-02-11 |
| `vr-node-lines` | Node: each release line adds backporting | [Node's schedule](https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule) | "Each additional line increases backporting complexity." | 2026-11-11 | 2027-05-11 |
| `vr-pep387-message` | The warning names the release that changes | [PEP 387](https://peps.python.org/pep-0387/) | "The warning message should include the release the incompatibility is expected to become the default" | 2026-11-11 | 2027-05-11 |
| `vr-pep387-support` | Remove only once every version has the replacement | [PEP 387](https://peps.python.org/pep-0387/) | "removed only after the last Python version without the new feature reaches end of support" | 2026-11-11 | 2027-05-11 |
| `vr-ghsa-flow` | Publish once patched; may alert via Dependabot; say if no fix is planned | [Security advisories](https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories) | "once a patch is released" and "may use the security advisory to send Dependabot alerts" and "be clear about it in the advisory" | 2026-11-11 | 2027-02-11 |
| `vr-ghsa-cve` | CVE requests: about 72 hours, not published | [Security advisories](https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories) | "GitHub usually reviews the request within 72 hours" and "doesn't make your security advisory public" | 2026-11-11 | 2027-02-11 |
| `vr-ghsa-fix-version` | Add the fix version before publishing | [Publish an advisory](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/fix-reported-vulnerabilities/publish-repository-advisory) | "add a fix version to a security advisory prior to publishing the advisory" | 2026-11-11 | 2027-02-11 |
| `vr-private-fork` | No status checks in an advisory's private fork | [Private fork](https://docs.github.com/en/code-security/tutorials/fix-reported-vulnerabilities/collaborate-in-a-fork) | "status checks do not run on pull requests in temporary private forks" | 2026-11-11 | 2027-02-11 |
| `vr-make-latest` | The API marks new releases latest | [Releases API](https://docs.github.com/en/rest/releases/releases) | "Defaults to true for newly published releases." | 2026-11-11 | 2027-02-11 |
| `vr-gh-latest` | `--latest=false` leaves the latest release alone | [gh release create](https://cli.github.com/manual/gh_release_create) | "--latest=false to explicitly NOT set as latest" | 2026-11-11 | 2027-02-11 |
| `vr-semver-build` | SemVer ignores build metadata for precedence | [semver.org](https://semver.org/) | "Build metadata MUST be ignored when determining version precedence." | 2026-11-11 | 2027-05-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Keep a Changelog 2.0.0](https://keepachangelog.com/en/2.0.0/) | Notes against the changelog; naming the removal | MIT: short quotes, summarized |
| [GitHub Docs](https://docs.github.com/) | Generated notes, `SECURITY.md`, advisories, CVEs, `make_latest` | CC BY 4.0: our own words, short quotes |
| [gh manual](https://cli.github.com/manual/) | `--latest=false` | MIT: short quotes |
| [Python Developer's Guide](https://devguide.python.org/versions/) | Python's support phases | CC0 1.0: short quotes, attributed |
| [PEP 387](https://peps.python.org/pep-0387/) | Deprecation timelines | Public domain: short quotes |
| [Node.js blog](https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule) | Node's lines and their cost | Not stated: our own words, short quotes |
| [Semantic Versioning 2.0.0](https://semver.org/) | Build metadata | CC BY 3.0: summarized, attributed |
