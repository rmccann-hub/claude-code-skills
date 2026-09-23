# Verification: C-platform (2026-09-23)

Checked by the receiving session on 2026-09-23 before the scaffold's pins were changed.

| Claim | Status | Checked against |
|---|---|---|
| actions/checkout v7.0.1 = `3d3c42e5aac5ba805825da76410c181273ba90b1`; floating `v7` at the same commit | verified | `git ls-remote https://github.com/actions/checkout` |
| actions/setup-go v7.0.0 = `b7ad1dad31e06c5925ef5d2fc7ad053ef454303e`; `v7` at the same commit | verified | `git ls-remote` |
| actions/setup-node v7.0.0 = `820762786026740c76f36085b0efc47a31fe5020`; `v7` at the same commit | verified | `git ls-remote` |
| astral-sh/setup-uv v10.2.0 = `c18668ad3cf93ea998bef934396af7bb5c839dc7`; no `v10` tag | verified | `git ls-remote` |
| setup-uv v10.2.0 still takes a `version` input, and runs on node24 | verified | its `action.yml` at v10.2.0 |
| @anthropic-ai/claude-code latest is 2.1.280 | verified | `npm view @anthropic-ai/claude-code version` |
| Everything else in the pins table | not yet checked | unchanged in the scaffold, so nothing relies on it yet |

---

RESULT-FOR: rmccann-hub/claude-code-skills · RUN: C-platform · FORM: research-result v1 · DATE: 2026-09-23 · BY: Claude Code subagent with web tools

# Platform facts and versions: research result

## Pins to change

| Pin | In the scaffold | Latest (official) | Source | Change? |
|---|---|---|---|---|
| actions/checkout | `@v5` (floating tag; since 2026-07-20 it resolves to v5.1.0) | v7.0.1, released 2026-07-20, commit `3d3c42e5aac5ba805825da76410c181273ba90b1` | [v7.0.1 release](https://github.com/actions/checkout/releases/tag/v7.0.1) | Yes: `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1` |
| astral-sh/setup-uv | `@v7` | v10.2.0, released 2026-09-21, commit `c18668ad3cf93ea998bef934396af7bb5c839dc7`. No `@v10` tag exists (floating tags stopped at v8.0.0) | [v10.2.0 release](https://github.com/astral-sh/setup-uv/releases/tag/v10.2.0), [v8.0.0 release](https://github.com/astral-sh/setup-uv/releases/tag/v8.0.0) | Yes: `astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0` (or `@v10.2.0`) |
| uv (setup-uv `version:` input) | 0.12.18 | 0.12.18, released 2026-09-22 | [uv 0.12.18 release](https://github.com/astral-sh/uv/releases/tag/0.12.18), [PyPI](https://pypi.org/project/uv/) | No |
| actions/setup-go | `@v6` | v7.0.0, released 2026-07-16, commit `b7ad1dad31e06c5925ef5d2fc7ad053ef454303e` | [v7.0.0 release](https://github.com/actions/setup-go/releases/tag/v7.0.0) | Yes: `actions/setup-go@b7ad1dad31e06c5925ef5d2fc7ad053ef454303e # v7.0.0` |
| setup-go `go-version` | `"1.27"` | go1.27.1, released 2026-09-01, is the current stable Go. `'1.27'` is a valid value | [go.dev/dl](https://go.dev/dl/), [Go release history](https://go.dev/doc/devel/release) | No (optional: pin `'1.27.1'` or set `check-latest: true` so an older cached 1.27.x is not used) |
| actions/setup-node | not chosen | v7.0.0, released 2026-07-14, commit `820762786026740c76f36085b0efc47a31fe5020`. The Node.js LTS line is 24 (v24.21.0) | [v7.0.0 release](https://github.com/actions/setup-node/releases/tag/v7.0.0), [nodejs.org releases](https://nodejs.org/en/about/previous-releases) | Choose: `actions/setup-node@820762786026740c76f36085b0efc47a31fe5020 # v7.0.0` with `node-version: 24` |
| gitleaks | v8.30.1, via `go install github.com/zricethezav/gitleaks/v8@v8.30.1` | v8.30.1, released 2026-03-21. The module path is unchanged | [v8.30.1 release](https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1), [go.mod at v8.30.1](https://github.com/gitleaks/gitleaks/blob/v8.30.1/go.mod) | No |
| actionlint | v1.7.12 | v1.7.12, 2026-03-30 | [actionlint CHANGELOG](https://github.com/rhysd/actionlint/blob/main/CHANGELOG.md) | No |
| Python | 3.14 (CPython 3.14.7) | 3.14.7, Aug. 5, 2026 | [python.org downloads](https://www.python.org/downloads/) | No |
| ruff | 0.16.8 | 0.16.8, uploaded 2026-09-16 | [PyPI ruff](https://pypi.org/project/ruff/) | No (but see C7: ruff 0.16 formats Markdown by default) |
| pytest | 9.1.1 | 9.1.1, uploaded 2026-06-19 | [PyPI pytest](https://pypi.org/project/pytest/) | No |
| pytest-cov | 7.1.0 | 7.1.0, uploaded 2026-03-21 | [PyPI pytest-cov](https://pypi.org/project/pytest-cov/) | No |
| PyYAML | 6.0.3 | 6.0.3, uploaded 2025-09-25 | [PyPI PyYAML](https://pypi.org/project/PyYAML/) | No |
| @anthropic-ai/claude-code | 2.1.280 | 2.1.280, published 2026-09-22T15:44:39Z (dist-tag `latest`; the `stable` dist-tag is 2.1.267) | [npm registry](https://registry.npmjs.org/@anthropic-ai/claude-code) | No |

## Findings

### C1. GitHub Free, public repo owned by a personal account: rulesets, secret scanning and push protection, private vulnerability reporting

- **Answer:**
  - (a) Yes. Rulesets are available in public repositories on GitHub Free. The available rules include "Require status checks to pass before merging" and "Block force pushes", and "Block force pushes" is on by default in a new ruleset. Push rulesets are not included: they are Team plan only, for private and internal repositories. Menu path: repository **Settings**, then in the left sidebar under "Code and automation" click **Rulesets**, then **Rulesets**, then **New ruleset** > **New branch ruleset**.
  - (b) Yes, both are available free for public repositories. Secret scanning "runs automatically for free" on public repositories.
    - Default for a new repository: the GitHub changelog of 2024-03-11 says new public repositories owned by personal accounts get secret scanning and push protection on by default. I found nothing later that reverses this. Existing repositories and organization-owned ones are not covered.
    - Caveat: today's general description of repository-level push protection still says "Is disabled by default". Check the toggle once after you create the repository.
    - Separately, user-level "push protection for users" is on by default. It blocks your own pushes of secrets to any public repository.
    - Repository settings: **Settings** > "Security and quality" section of the sidebar > **Advanced Security**. Next to "Secret Protection", click **Enable**. Then, in the "Secret Protection" section next to "Push protection", click **Enable**.
    - User-level setting: profile picture > **Settings** > "Security" section > **Code security**. Under "User", use "Push protection for yourself".
  - (c) Yes, it is available for public repositories, and owners and admins turn it on. No official page says it is on by default. The docs only say owners and admins "can enable" it, and a repository without it falls back to SECURITY.md or issue-based reporting. Treat it as off until enabled. Path: **Settings** > "Security and quality" > **Advanced Security**, then next to "Private vulnerability reporting" click **Enable**.
- **Sources:**
  - [About rulesets, GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets): "Rulesets are available in public repositories with GitHub Free and GitHub Free for organizations, and in public and private repositories with GitHub Pro, GitHub Team, and GitHub Enterprise Cloud." and "Push rulesets are available for the GitHub Team plan in internal and private repositories, and forks of repositories that have push rulesets enabled." (undated docs page; read 2026-09-23)
  - [Available rules for rulesets, GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets): "Required status checks ensure that all required CI tests are passing before collaborators can make changes to a branch or tag targeted by your ruleset." and "You can prevent users from force pushing to the targeted branches or tags. This rule is enabled by default." (undated; read 2026-09-23)
  - [Creating rulesets for a repository, GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository): "In the left sidebar, under "Code and automation," click Rulesets, then click Rulesets." and "To create a ruleset targeting branches, click New branch ruleset." (undated; read 2026-09-23)
  - [Enable secret scanning, GitHub Docs](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/detect-secret-leaks/enable-secret-scanning): availability box "Public repositories: Secret scanning runs automatically for free."; "Secret scanning alerts for users can be enabled on any free public repository that you own."; "In the "Security and quality" section of the sidebar, click Advanced Security."; "To the right of "Secret Protection", click Enable." (undated; read 2026-09-23)
  - [Enabling push protection for your repository, GitHub Docs](https://docs.github.com/en/code-security/secret-scanning/enabling-secret-scanning-features/enabling-push-protection-for-your-repository): "In the "Secret Protection" section, to the right of "Push protection", click Enable." (undated; read 2026-09-23)
  - [Push protection, GitHub Docs](https://docs.github.com/en/code-security/concepts/secret-security/push-protection): repository-level push protection "Is disabled by default, and can be enabled by a repository administrator, organization owner, security manager, or enterprise owner". User-level push protection "Is enabled by default" and "Stops you from pushing secrets to public repositories on GitHub". (undated; read 2026-09-23)
  - [GitHub Changelog: Secret scanning and push protection are enabled by default on new public repositories](https://github.blog/changelog/2024-03-11-secret-scanning-and-push-protection-are-enabled-by-default-on-new-public-repositories/): "All new public repositories owned by personal accounts will now have secret scanning and push protection enabled by default." and "Existing public repositories are not affected, nor are new public repositories that belong to an organization." (dated 2024-03-11; read 2026-09-23)
  - [Managing push protection for users, GitHub Docs](https://docs.github.com/en/code-security/secret-scanning/working-with-secret-scanning-and-push-protection/push-protection-for-users): "In the "Security" section of the sidebar, click Code security." and "Under "User", to the right of "Push protection for yourself", update your settings." (undated; read 2026-09-23)
  - [Configuring private vulnerability reporting for a repository, GitHub Docs](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository): "Owners and administrators of public repositories can allow security researchers to report vulnerabilities securely in the repository by enabling private vulnerability reporting." and "Under "Advanced Security", to the right of "Private vulnerability reporting", click Enable or Disable, to enable or disable the feature, respectively." (undated; read 2026-09-23)
  - [Coordinated disclosure of security vulnerabilities, GitHub Docs](https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/coordinated-disclosure): "Owners and administrators of public repositories can enable private vulnerability reporting on their repositories." (undated; read 2026-09-23)
- **Confidence:** (a) High. (b) High for availability and menu paths. Medium for "on by default": the 2024 changelog is explicit, but the general docs wording says repository push protection is off by default. (c) High for availability and path. Medium for "off by default", which is inferred because no page states it.

### C2. Latest action releases with full SHAs; Go and Node.js lines

- **Answer:** Each SHA below was read from the commit link on the release page. It matches the short SHA shown on that page, and each full-SHA commit URL resolves on github.com. One tool summary of the setup-node tags page returned a garbled 41-character value; I ignored it.
  - actions/checkout: **v7.0.1**, released 2026-07-20 (tag commit dated 2026-07-17), SHA `3d3c42e5aac5ba805825da76410c181273ba90b1`. uv's own docs use the same SHA for v7.0.1. A floating `v7` tag also exists.
  - actions/setup-go: **v7.0.0**, released 2026-07-16, SHA `b7ad1dad31e06c5925ef5d2fc7ad053ef454303e`. A floating `v7` tag exists. The README says v7 changes nothing in inputs, outputs or behavior.
  - actions/setup-node: **v7.0.0**, released 2026-07-14, SHA `820762786026740c76f36085b0efc47a31fe5020`. A floating `v7` tag exists. Breaking change: the dummy `NODE_AUTH_TOKEN` fallback was removed.
  - astral-sh/setup-uv: **v10.2.0**, released 2026-09-21, SHA `c18668ad3cf93ea998bef934396af7bb5c839dc7`.
    - No floating major or minor tags since v8.0.0, so `@v10` does not exist. Pin the full version or the SHA.
    - Breaking changes since v7: v8.0.0 moved to immutable releases, dropped floating tags and removed the deprecated custom manifest format. v9.0.0 made `prune-cache` default to `false`. v10.0.0 disabled automatic caching for sensitive events.
  - Go: the current stable release is **go1.27.1** (released 2026-09-01; go1.27.0 was 2026-08-19).
    - `go-version: "1.27"` is valid: setup-go accepts "Specific versions: `1.25`, ...", and 1.27.1 and 1.27.0 are the first entries in the actions/go-versions manifest.
    - setup-go checks the runner tool cache first, so an older cached 1.27.x can be used unless you pin `'1.27.1'` or set `check-latest: true`. This is my inference from the documented resolution order.
  - Node.js: the LTS line is **24 "Krypton"** (latest LTS v24.21.0, 2026-09-07). v26 is "Current" (v26.10.0, 2026-09-21), and v22 "Jod" is still listed as LTS. The claude-code npm package declares `"node":">=22.0.0"`.
- **Sources:**
  - [actions/checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1): commit link "/actions/checkout/commit/3d3c42e5aac5ba805825da76410c181273ba90b1"; entry "skip running unsafe pr check if input is default by @aiqiaoy in #2518" (released 20 Jul 2026; read 2026-09-23)
  - [uv GitHub Actions guide](https://docs.astral.sh/uv/guides/integration/github/): "- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1" (undated; read 2026-09-23)
  - [actions/setup-go v7.0.0](https://github.com/actions/setup-go/releases/tag/v7.0.0): commit link "/actions/setup-go/commit/b7ad1dad31e06c5925ef5d2fc7ad053ef454303e"; [README](https://github.com/actions/setup-go/blob/main/README.md): "Migrated action internals to ESM for compatibility with latest `@actions/*` packages. No changes to action inputs, outputs, or behavior." (released 16 Jul 2026; read 2026-09-23)
  - [actions/setup-node v7.0.0](https://github.com/actions/setup-node/releases/tag/v7.0.0): commit link "/actions/setup-node/commit/820762786026740c76f36085b0efc47a31fe5020"; [README](https://github.com/actions/setup-node/blob/main/README.md): "The dummy `NODE_AUTH_TOKEN` fallback has been removed, as it could unintentionally affect the generated `.npmrc` with a non-functional token." (released 14 Jul 2026; read 2026-09-23)
  - [astral-sh/setup-uv v10.2.0](https://github.com/astral-sh/setup-uv/releases/tag/v10.2.0): commit link "/astral-sh/setup-uv/commit/c18668ad3cf93ea998bef934396af7bb5c839dc7"; "This release contains the known-checksum of the most recent uv releases and also disabled the uploading(saving) of the cache when in a merge queue since theses caches would almost never be used." (released 21 Sep 2026; read 2026-09-23)
  - [astral-sh/setup-uv v8.0.0](https://github.com/astral-sh/setup-uv/releases/tag/v8.0.0): "To increase security even more we will stop publishing minor tags. You won't be able to use `@v8` or `@v8.0` any longer." (released 29 Mar 2026; read 2026-09-23)
  - [Go downloads](https://go.dev/dl/): the first entry under the "Stable versions" heading is "go1.27.1", and the [JSON feed](https://go.dev/dl/?mode=json) lists go1.27.1 and go1.26.8 as `"stable": true`. [Go release history](https://go.dev/doc/devel/release): "go1.27.1 (released 2026-09-01) includes fixes to cgo, the compiler, the runtime" and "go1.27.0 (released 2026-08-19)" (read 2026-09-23)
  - [setup-go README](https://github.com/actions/setup-go/blob/main/README.md): "Specific versions: `1.25`, `1.24.11`, `1.24.0-rc.1`, `1.23.0-beta.1`"; "Checks the local tool cache for a matching semver version."; "To change the default behavior, please use the check-latest input." (undated; read 2026-09-23)
  - [actions/go-versions manifest](https://github.com/actions/go-versions/blob/main/versions-manifest.json): first entries are 1.27.1 then 1.27.0 (read 2026-09-23)
  - [Node.js releases](https://nodejs.org/en/about/previous-releases): release links "v24.21.0" labelled "Latest LTS" and "v26.10.0" labelled "Latest Release". Table cells for v24: "Krypton", "May 06, 2025", "Sep 07, 2026", "LTS". For v26: "May 05, 2026", "Sep 21, 2026", "Current". "Production applications should only use Active LTS or Maintenance LTS releases." (read 2026-09-23). Cross-check: [nodejs.org/dist/index.json](https://nodejs.org/dist/index.json) has v24.21.0 dated 2026-09-07 with `lts` "Krypton".
- **Confidence:** High for tags and SHAs (release-page commit links; each full-SHA commit page resolves; checkout's SHA is also confirmed by uv's docs). High for Go and Node. Medium for the tool-cache caveat on `'1.27'`, which is inferred.

### C3. Dependabot: uv and npm support; cooldown

- **Answer:**
  - uv (`package-ecosystem: "uv"`): yes for both version updates and security updates. The docs table lists uv with "Supported" for version updates, security updates, private repositories and private registries.
    - Version updates went GA 2025-03-13; security updates arrived 2025-12-16.
    - The documented "Supported versions" for uv is "v0.11". The scaffold uses 0.12.18. No incompatibility is stated, but this is worth watching.
    - The separate dependency-graph ecosystems table has no uv row.
  - npm with package-lock.json: yes. `npm` is listed for npm v7 to v11 with version and security updates supported, and the dependency graph lists `package-lock.json` as npm's "Recommended files".
  - Default cooldown: **3 days** for version updates, applied even with no `cooldown` configured (default since 2026-07-14). **Security updates are exempt.**
  - The `cooldown` key is documented, with fields `default-days`, `semver-major-days`, `semver-minor-days`, `semver-patch-days`, `include` and `exclude`. `include` and `exclude` take up to 150 items each and allow `*` wildcards.
    - The semver fields apply only to package managers that support them. The support table marks UV, "NPM and Yarn", Pip and Gomod as supporting both default and SemVer-bump days, and GitHub Actions as default days only.
- **Sources:**
  - [Dependabot supported ecosystems and repositories, GitHub Docs](https://docs.github.com/en/code-security/reference/supply-chain-security/supported-ecosystems-and-repositories): header "| Package manager | YAML value | Supported versions | Version updates | Security updates | Private repositories | Private registries | Vendoring |". The uv row reads "uv", "`uv`", "v0.11", then four cells with aria-label "Supported", then "Not applicable". The npm row reads "npm", "`npm`", "v7, v8, v9, v10, v11", then four "Supported" cells and one "Not supported" (vendoring). (undated; read 2026-09-23)
  - [Dependabot options reference, GitHub Docs](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference): "The `cooldown` option is only available for *version* updates, not *security* updates."; "Apply a **default cooldown period of 3 days** to version updates, even when `cooldown` is not configured. A new version is not considered for a version update until 3 days after its release. **This default cooldown does not apply to security updates.**"; `default-days` row: "If not specified, Dependabot applies a default cooldown of 3 days."; `include` row: "List of dependencies to **apply cooldown** (up to **150 items**). Supports wildcards (`*`)."; package-ecosystem row "| uv | `uv` | v0.11 |" (undated; read 2026-09-23)
  - [GitHub Changelog: Dependabot version updates introduce default package cooldown](https://github.blog/changelog/2026-07-14-dependabot-version-updates-introduce-default-package-cooldown/): "Dependabot now waits until a new release has been available on its registry for at least three days before opening a version update pull request. This cooldown is now the default and requires no configuration." and "The default applies only to version updates. Security updates still open immediately, so critical fixes are never delayed." (dated 2026-07-14; read 2026-09-23)
  - [GitHub Changelog: Dependabot security updates now support uv](https://github.blog/changelog/2025-12-16-dependabot-security-updates-now-support-uv/): "Dependabot now supports security alerts and updates for uv." (dated 2025-12-16; read 2026-09-23)
  - [GitHub Changelog: Dependabot version updates now support uv in general availability](https://github.blog/changelog/2025-03-13-dependabot-version-updates-now-support-uv-in-general-availability/): "Developers can now use Dependabot to automatically keep their `uv` dependencies up to date." (dated 2025-03-13; read 2026-09-23)
  - [Dependency graph supported package ecosystems, GitHub Docs](https://docs.github.com/en/code-security/reference/supply-chain-security/dependency-graph-supported-package-ecosystems): npm row, "Recommended files" column: "`package-lock.json`" (undated; read 2026-09-23)
- **Confidence:** High.

### C4. gitleaks: release, module path, generic-api-key logic, custom rules; actionlint

- **Answer:**
  - Latest gitleaks: **v8.30.1**, published 2026-03-21 (the tag commit is dated 2026-03-12). There is no newer release or pre-release. The Go module path is still `github.com/zricethezav/gitleaks/v8`, so the scaffold's `go install` line is correct.
  - How the default `generic-api-key` rule decides:
    1. Keyword pre-filter, case-insensitive: access, api, auth, key, credential, creds, passwd, password, secret, token.
    2. Regex: an identifier containing access, auth, api, credential, creds, key, passw(or)d, secret or token, then an assignment operator such as `=`, `:`, `:=`, `=>`, `?=` or `,`. The captured value must be either 10 to 150 characters of `[\w.=-]` or a base64-like `[a-z0-9][a-z0-9+/]{11,}={0,3}`. It must be followed by a quote, backtick, whitespace, `;`, an escaped newline, or end of line.
    3. `entropy = 3.5`: the captured value's Shannon entropy must be at least 3.5.
    4. Rule allowlists drop a match if any of these hits:
       - the secret matches `^[a-zA-Z_.-]+$`;
       - the whole match (`regexTarget = "match"`) matches a long regex list of known false-positive words;
       - the secret contains a stopword such as "000000", "aaaaaa", "about" or "account", checked by lowercasing the secret and testing substring containment;
       - line-level patterns for `--mount=type=secret,`, imports, and LICENSE lines in BitBake files.
    5. The global allowlist skips images, fonts, lockfiles such as `package-lock.json`, `gitleaks.toml` and others. It does not skip `.md` files.
  - Why a password with no digits is skipped: the first allowlist is a deliberate stand-in for "must contain digits", because Go regex has no lookaheads. Any value made only of letters, `_`, `.` and `-` is never reported. Such a value can also miss the 3.5 entropy threshold, be shorter than 10 characters, or contain a stopword.
  - Custom rule for `KEY=value` lines in Markdown: put a `.gitleaks.toml` in the scanned path, where it is auto-detected (`--config`, `GITLEAKS_CONFIG` or `GITLEAKS_CONFIG_TOML` take precedence).
    - Keep `[extend]` with `useDefault = true`. This is still the documented way to inherit the built-in rules, and it cannot be combined with `[extend] path`.
    - Add a `[[rules]]` table with `id`, `description`, `regex` (Go regex, no lookaheads), `path` (a Go regex on the file path, e.g. `'''\.md$'''`; for path+regex rules the path is checked first), `secretGroup`, and optional `entropy`, `keywords` (lowercase; matched case-insensitively) and `tags`. Add `[[rules.allowlists]]` if needed.
    - Example (my own, not from the docs):
    ```toml
    [extend]
    useDefault = true

    [[rules]]
    id = "markdown-key-value"
    description = "KEY=value secret assignment in a Markdown file"
    path = '''(?i)\.md$'''
    regex = '''(?m)^\s*(?:export\s+)?[A-Z][A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD|PASSWD)[A-Z0-9_]*\s*=\s*['"]?([^\s'"]{8,})'''
    secretGroup = 1
    keywords = ["key", "token", "secret", "password", "passwd"]
    ```
  - actionlint: **v1.7.12** (2026-03-30) is the latest release, which matches the scaffold.
- **Sources:**
  - [gitleaks v8.30.1 release](https://github.com/gitleaks/gitleaks/releases/tag/v8.30.1): released "21 Mar 02:17" (2026-03-21T02:17:03Z on the releases list, marked Latest); entry "build: switch to Go 1.24 (#2002)" (read 2026-09-23)
  - [gitleaks go.mod at v8.30.1](https://github.com/gitleaks/gitleaks/blob/v8.30.1/go.mod): "module github.com/zricethezav/gitleaks/v8" (read 2026-09-23)
  - [generic.go (rule source)](https://github.com/gitleaks/gitleaks/blob/master/cmd/generate/config/rules/generic.go): `RuleID: "generic-api-key",`; secret pattern `` `[\w.=-]{10,150}|[a-z0-9][a-z0-9+/]{11,}={0,3}` ``; `Entropy: 3.5,`; comments "NOTE: this is a goofy hack to get around the fact there golang's regex engine does not support positive lookaheads." and "Ideally we would want to ensure the secret contains both numbers and alphabetical characters, not just alphabetical characters."; `` regexp.MustCompile(`^[a-zA-Z_.-]+$`), ``; `Description: "Allowlist for Generic API Keys",` (read 2026-09-23)
  - [config/gitleaks.toml (default config)](https://github.com/gitleaks/gitleaks/blob/master/config/gitleaks.toml): `id = "generic-api-key"`, `entropy = 3.5`, `description = "Allowlist for Generic API Keys"`, `regexTarget = "match"`, stopwords beginning "000000", "6fe4476ee5a1832882e326b506d14126", "_ec2_", "aaaaaa", "about"; the global allowlist `description = "global allow lists"` includes `'''gitleaks\.toml'''` and `'''(?:^|/)(?:deno\.lock|npm-shrinkwrap\.json|package-lock\.json|pnpm-lock\.yaml|yarn\.lock)$'''` (read 2026-09-23)
  - [config/allowlist.go](https://github.com/gitleaks/gitleaks/blob/master/config/allowlist.go): `s = strings.ToLower(s)` and `if strings.Contains(s, stopWord) {` (read 2026-09-23)
  - [detect/detect.go](https://github.com/gitleaks/gitleaks/blob/master/detect/detect.go): `normalizedRaw := strings.ToLower(currentRaw)` and `if _, ok := keywords[strings.ToLower(k)]; ok {` (read 2026-09-23)
  - [gitleaks README](https://github.com/gitleaks/gitleaks/blob/master/README.md): "A `.gitleaks.toml` file within the target path"; "If none of the four options are used, then gitleaks will use the default config."; "useDefault and path can NOT be used at the same time. Choose one."; "useDefault will extend the default gitleaks config built in to the binary"; "Golang regular expression used to detect secrets. Note Golang's regex engine"; "Golang regular expression used to match paths. This can be used as a standalone rule or it can be used"; "Float representing the minimum shannon entropy a regex group must have to be considered a secret."; "note: stopwords targets the extracted secret, not the entire regex match" (read 2026-09-23)
  - [actionlint CHANGELOG](https://github.com/rhysd/actionlint/blob/main/CHANGELOG.md): "v1.7.12 - 2026-03-30"; [v1.7.12 release](https://github.com/rhysd/actionlint/releases/tag/v1.7.12): "Support the `jobs.<job_name>.environment.deployment` configuration." (dated 2026-03-30; read 2026-09-23)
- **Confidence:** High for versions, module path and the rule's mechanics (read from source). The example rule is mine and has not been run.

### C5. Claude Code: latest version, AGENTS.md, cloud sessions, plugins, synced skills

- **Answer:**
  - Latest: **2.1.280**, published 2026-09-22T15:44:39Z (changelog: September 22, 2026). The npm `latest` and `next` dist-tags are 2.1.280. The `stable` dist-tag is **2.1.267**, which predates AGENTS.md support.
  - AGENTS.md: first read natively in **v2.1.277** (2026-09-18). Conditions:
    - no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` in the working directory or above it (`~/.claude/CLAUDE.md`, managed CLAUDE.md and `.claude/rules/` don't count);
    - the session fetches feature flags from Anthropic (not Bedrock or another third-party provider, not a Claude apps gateway, and telemetry or nonessential traffic not disabled);
    - it is not the first session after an install or upgrade to a version with AGENTS.md support;
    - the built-in `agents-md` plugin is not disabled.

    The default **Project instructions** value is `claude-md-or-agents-md`. `AGENTS.local.md`, `AGENTS.override.md` and `.agents/` are not read.
  - Cloud session in a fresh VM as a "first session after an install or upgrade": **not found**. The docs describe cloud sessions as a fresh VM with a fresh clone, but no page says whether that counts. The docs' remedy for any session that can't read AGENTS.md is a `CLAUDE.md` containing `@AGENTS.md`.
  - Plugins declared in the repo's `.claude/settings.json` (`enabledPlugins`, `extraKnownMarketplaces`): **not installed in cloud sessions**. Enable them on the claude.ai account instead, so they load as synced plugins. The repo's `.claude/skills/`, `.claude/agents/`, `.claude/commands/`, CLAUDE.md, hooks and permission rules are available in a single-repository session.
  - Skills enabled on claude.ai: cloud and Cowork sessions load them automatically at session start. In terminal sessions signed in with the claude.ai account (v2.1.273 or later), they are downloaded in the background into `~/.claude/skills/synced/`, re-checked about every 10 minutes, and invoked as `/anthropic-skills:<name>`, or `/<name>` when no other command uses that name. Syncing only happens in sessions that sign in via `/login` and fetch feature flags. It never uploads local edits.
- **Sources:**
  - [Claude Code changelog](https://code.claude.com/docs/en/changelog): `<Update label="2.1.280" description="September 22, 2026">`; 2.1.277 (September 18, 2026): "Added AGENTS.md support: in a project with no CLAUDE.md, Claude Code reads AGENTS.md instead; change it under "Project instructions" in `/config` (not yet on Bedrock, Vertex or Foundry)" (read 2026-09-23)
  - [npm registry: @anthropic-ai/claude-code](https://registry.npmjs.org/@anthropic-ai/claude-code): dist-tags `{"stable":"2.1.267","latest":"2.1.280","next":"2.1.280"}`; time "2.1.280": "2026-09-22T15:44:39.443Z"; "2.1.277": "2026-09-18T16:22:26.548Z"; engines `{"node":">=22.0.0"}` (read 2026-09-23)
  - [Memory docs, section AGENTS.md](https://code.claude.com/docs/en/memory#agents-md): "Reading `AGENTS.md` directly requires Claude Code v2.1.277 or later. In some sessions, such as those on Amazon Bedrock or with telemetry disabled, Claude can't read `AGENTS.md`, so import it from a `CLAUDE.md` there instead."; "By default, Claude reads `AGENTS.md` only when you have no `CLAUDE.md` in your working directory or above it."; "**Count, so Claude reads them instead of `AGENTS.md`**: a `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` in your working directory or any directory above it"; "In these sessions Claude reads `CLAUDE.md` files only, and **Project instructions** doesn't appear in the `/config` settings panel:"; "It's your first session after you install or upgrade to a version with `AGENTS.md` support. Claude reads `AGENTS.md` from your next session on"; "You disabled the built-in `agents-md` plugin in `/plugin`"; "**Not read**: `AGENTS.local.md`, `AGENTS.override.md`, or anything under a `.agents/` directory" (read 2026-09-23)
  - [Environment variables, section First session after an install or upgrade](https://code.claude.com/docs/en/env-vars#first-session-after-an-install-or-upgrade): "In your first session after you install Claude Code, or upgrade to a version that adds a feature, a flag-gated feature can be missing, and the session can start in Manual mode on a plan that otherwise starts in auto mode. Claude Code fetches the flags during that session, so both are there in your next session." and "Have Claude Code read `AGENTS.md` files as project instructions; it loads `CLAUDE.md` files only" (from the list of what you can't do with fetching off) (read 2026-09-23)
  - [Cloud environments](https://code.claude.com/docs/en/cloud-environments): "Cloud sessions start from a fresh clone of your repository."; "In Anthropic-hosted environments, each session gets a fresh virtual machine (VM) running Ubuntu 24.04 on x86_64"; "A cloud session doesn't install the plugins a repository turns on under `enabledPlugins`, including ones from the marketplaces it lists under `extraKnownMarketplaces`. Enable the plugin for your claude.ai account instead, so Claude Code loads it as a synced plugin"; "Cloud sessions automatically load skills you enable on claude.ai" (read 2026-09-23)
  - [Skills](https://code.claude.com/docs/en/skills): "In a Cowork or cloud session, Claude Code loads the skills enabled for your claude.ai account"; "When the session starts, Claude Code downloads your account's skills into `~/.claude/skills/synced/` in the background, then checks claude.ai for changes about every 10 minutes while the session runs."; "Syncing in terminal sessions requires Claude Code v2.1.273 or later."; "Claude Code syncs only in a session that signs in with your claude.ai account and fetches feature flags from Anthropic."; "Claude Code downloads synced skills and never uploads them." (read 2026-09-23)
  - [Plugins reference, section Synced plugins](https://code.claude.com/docs/en/plugins-reference#synced-plugins): "In Cowork and cloud sessions, Claude Code downloads them into the session's own environment when the session starts." (read 2026-09-23)
- **Confidence:** High for version, AGENTS.md conditions, plugins and skills (read from the raw docs). The cloud "first session" question is unanswered by the docs.

### C6. uv, Python 3.14, and PyPI versions

- **Answer:**
  - uv: latest **0.12.18** (GitHub release and PyPI, 2026-09-22).
  - `uv sync --locked` is still what the uv GitHub Actions guide uses: `uv sync --locked --all-extras --dev`. With `--locked`, uv errors instead of rewriting an out-of-date `uv.lock`.
  - The same guide recommends pinning the uv version through setup-uv's `version:` input, and its example uses `"0.12.18"`. Its examples still show `astral-sh/setup-uv@... # v9.0.0`, which is older than v10.2.0.
  - Python: latest 3.14 patch on python.org is **3.14.7** (Aug. 5, 2026), which is also the version on the site's main download button.
  - PyPI (latest version and upload date of its first file):
    - ruff **0.16.8** (2026-09-16)
    - pytest **9.1.1** (2026-06-19)
    - pytest-cov **7.1.0** (2026-03-21)
    - PyYAML **6.0.3** (2025-09-25)
    - uv **0.12.18** (2026-09-22)
- **Sources:**
  - [uv 0.12.18 release](https://github.com/astral-sh/uv/releases/tag/0.12.18): "Released on 2026-09-22." (read 2026-09-23)
  - [uv GitHub Actions guide](https://docs.astral.sh/uv/guides/integration/github/): "It is considered best practice to pin to a specific uv version, e.g., with:"; `version: "0.12.18"`; "Once uv and Python are installed, the project can be installed with uv sync and commands can be run in the environment with uv run:"; `run: uv sync --locked --all-extras --dev` (undated; read 2026-09-23)
  - [uv docs: Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/): "To disable automatic locking, use the --locked option:" and "If the lockfile is not up-to-date, uv will raise an error instead of updating the lockfile." (undated; read 2026-09-23)
  - [python.org downloads](https://www.python.org/downloads/): "Download Python 3.14.7"; release list entry "Python 3.14.7 Aug. 5, 2026" (read 2026-09-23)
  - PyPI JSON API, `info.version` and the first file's `upload_time_iso_8601`:
    - [ruff](https://pypi.org/pypi/ruff/json): "0.16.8", "2026-09-16T15:53:57.605047Z"
    - [pytest](https://pypi.org/pypi/pytest/json): "9.1.1", "2026-06-19T10:58:31.347074Z"
    - [pytest-cov](https://pypi.org/pypi/pytest-cov/json): "7.1.0", "2026-03-21T20:11:14.438324Z"
    - [PyYAML](https://pypi.org/pypi/PyYAML/json): "6.0.3", "2025-09-25T21:31:46.040932Z"
    - [uv](https://pypi.org/pypi/uv/json): "0.12.18", "2026-09-22T22:58:15.871201Z"

    None of these files is yanked. (read 2026-09-23)
- **Confidence:** High.

### C7. ruff and Markdown

- **Answer:**
  - **Yes, by default.** `ruff format` formats Python code blocks in Markdown files. Fenced blocks tagged `python`, `py`, `python3`, `py3`, `pyi` or `pycon` are formatted, as are Quarto `{python}` blocks. Blocks that don't parse are skipped, and `<!-- fmt:off -->` / `<!-- fmt:on -->` regions are left alone.
  - History:
    - it first appeared as a preview feature in **0.15.0** (2026-02-03);
    - 0.15.5 made preview mode discover Markdown files by default;
    - **0.16.0** (2026-07-23) made it the default, listed under "Breaking changes".
  - `*.md` is now part of the default `include` list, so ruff 0.16.8 will reformat Python blocks in the repo's SKILL.md and README files, and `ruff format --check` will flag them.
  - To exclude Markdown, the formatter docs say to add it to `extend-exclude`:
    ```toml
    [tool.ruff]
    extend-exclude = ["*.md"]
    ```
    This skips both formatting and linting. `[tool.ruff.format] exclude = ["*.md"]` skips formatting only. Setting `include` without `"*.md"` also removes Markdown, but it replaces the whole default list.
- **Sources:**
  - [Ruff formatter docs, section Markdown code formatting](https://docs.astral.sh/ruff/formatter/#markdown-code-formatting): "The Ruff formatter can also format Python code blocks in Markdown files."; "In these files, Ruff will format any CommonMark fenced code blocks with the following info strings: python, py, python3, py3, pyi, or pycon."; "To disable formatting of Markdown files, add them to extend-exclude in your project settings:"; `extend-exclude = ["*.md"]` (undated; read 2026-09-23)
  - [Ruff 0.16.0 release](https://github.com/astral-sh/ruff/releases/tag/0.16.0), under "Breaking changes": "Ruff can now format Python code blocks in Markdown files and will do this by default." (released 2026-07-23; read 2026-09-23)
  - [Ruff 0.15.x changelog](https://github.com/astral-sh/ruff/blob/main/changelogs/0.15.x.md): under 0.15.0 "Preview features", "Apply formatting to Markdown code blocks"; under 0.15.5, "Discover Markdown files by default in preview mode" (dated 2026-02-03 and 2026-03-05; read 2026-09-23)
  - [Ruff settings reference](https://docs.astral.sh/ruff/settings/): `include` "Default value: ["*.py", "*.pyi", "*.pyw", "*.ipynb", "*.md", "**/pyproject.toml", "**/ruff.toml", "**/.ruff.toml"]"; `extend-exclude`: "A list of file patterns to omit from formatting and linting, in addition to those specified by exclude."; `format.exclude`: "A list of file patterns to exclude from formatting in addition to the files excluded globally (see exclude, and extend-exclude)." (undated; read 2026-09-23)
- **Confidence:** High.

### C8. Least-privilege checkout pattern; 2026 actions/checkout credential changes

- **Answer:**
  - **Yes, still consistent with the docs.** GitHub Docs recommend a read-only default `GITHUB_TOKEN` for repository contents, "the least required access", and SHA pinning. The checkout README recommends `permissions: contents: read`.
  - `persist-credentials: false` is not a GitHub Docs recommendation. It is the checkout README's documented opt-out; the input defaults to `true`, and the token is otherwise kept for later steps.
  - **No 2026 change to how checkout persists credentials.** The move to a separate credentials file under `$RUNNER_TEMP` was v6.0.0 (20 Nov 2025; the release page omits the year, inferred from release order), and worktree support for the includeIf mechanism was v6.0.1 (2 Dec 2025).
  - The 2026 security changes:
    - v7.0.0 (2026-06-18) refuses to check out fork pull request code in `pull_request_target` and `workflow_run` workflows unless the new `allow-unsafe-pr-checkout: true` input is set. Its default is false.
    - This was backported as "[BREAKING]" to v6.1.0, v5.1.0, v4.4.0, v3.7.0 and v2.8.0, enforced from Monday 2026-07-20. Floating major tags picked it up automatically, so the scaffold's `@v5` already has it.
    - v7.0.1 (2026-07-20) adds "escape values passed to --unset".
- **Sources:**
  - [Secure use reference, GitHub Docs](https://docs.github.com/en/actions/reference/security/secure-use): "It's good security practice to set the default permission for the `GITHUB_TOKEN` to read access only for repository contents. The permissions can then be increased, as required, for individual jobs within the workflow file." and "Pinning an action to a full-length commit SHA is currently the only way to use an action as an immutable release." (undated; read 2026-09-23)
  - [Use GITHUB_TOKEN in workflows, GitHub Docs](https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/use-github_token-in-workflows): "Use the `permissions` key in your workflow file to modify permissions for the `GITHUB_TOKEN` for an entire workflow or for individual jobs. This allows you to configure the minimum required permissions for a workflow or job. As a good security practice, you should grant the `GITHUB_TOKEN` the least required access." (undated; read 2026-09-23)
  - [actions/checkout README](https://github.com/actions/checkout/blob/main/README.md): "When using the `checkout` action in your GitHub Actions workflow, it is recommended to set the following `GITHUB_TOKEN` permissions to ensure proper functionality, unless alternative auth is provided via the `token` or `ssh-key` inputs:"; "The auth token is persisted in the local git config. This enables your scripts to run authenticated git commands. The token is removed during post-job cleanup. Set `persist-credentials: false` to opt-out."; input text "Whether to configure the token or SSH key with the local git config"; v6: "Improved credential security: `persist-credentials` now stores credentials in a separate file under `$RUNNER_TEMP` instead of directly in `.git/config`"; v7: "Safer fork pull request handling: checkout now refuses to check out fork pull request code by default when the workflow is triggered by `pull_request_target` or `workflow_run`." (read 2026-09-23)
  - [checkout v7.0.0 release](https://github.com/actions/checkout/releases/tag/v7.0.0): "block checking out fork pr for pull_request_target and workflow_run by @aiqiaoy in #2454" (released 18 Jun 2026; read 2026-09-23)
  - [checkout v7.0.1 release](https://github.com/actions/checkout/releases/tag/v7.0.1): "escape values passed to --unset by @aiqiaoy in #2530" (released 20 Jul 2026; read 2026-09-23)
  - [checkout v5.1.0 release](https://github.com/actions/checkout/releases/tag/v5.1.0): "**[BREAKING]** backport `allow-unsafe-pr-checkout` to v5 by @aiqiaoy in #2501" (released 20 Jul 2026; read 2026-09-23)
  - [checkout v6.0.0 release](https://github.com/actions/checkout/releases/tag/v6.0.0): "Persist creds to a separate file"; [v6.0.1 release](https://github.com/actions/checkout/releases/tag/v6.0.1): "Add worktree support for persist-credentials includeIf" (released 20 Nov and 02 Dec, 2025 inferred; read 2026-09-23)
  - [GitHub Changelog: Safer pull_request_target defaults for GitHub Actions checkout](https://github.blog/changelog/2026-06-18-safer-pull_request_target-defaults-for-github-actions-checkout/): "Enforcement for backported versions of actions/checkout has been moved from July 16, 2026 to Monday, July 20, 2026." and "Workflows pinned to a floating major tag (e.g., `actions/checkout@v4`) will automatically pick up the change." (dated 2026-06-18, editor's note 2026-07-15; read 2026-09-23)
- **Confidence:** High.

## Not found

- C1(c): an official statement that private vulnerability reporting is on or off by default for a new public repository owned by a personal account. The docs only say owners and admins "can enable" it, and "off until enabled" is inferred from that.
- C5: an official statement on whether a Claude Code on the web / cloud session, which runs in a fresh VM, counts as the "first session after an install or upgrade". No docs page addresses feature-flag fetching in cloud sessions.
- C8: any GitHub Docs page recommending `persist-credentials: false`. Only the actions/checkout README documents it, as the opt-out.
- C3: an official statement that Dependabot's uv support covers uv 0.12.x. The docs table lists "v0.11".
- C2/C8: the year of actions/checkout v6.0.0 and v6.0.1 as printed on their release pages. I inferred 2025 from release order.
