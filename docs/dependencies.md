# Dependency map

What `claude-code-skills` 0.1.6 is built from, runs on and relies on: the
plugins it ships, the languages it's written in, its runtimes and tools, every package
at its exact version, the GitHub Actions it pins, the services it uses, and the sources
its skills' facts cite.

`uv run skillcheck --bom` writes this page, and the same map for other tools to read as
[`bom.json`](../bom.json), in [CycloneDX 1.7](https://cyclonedx.org/specification/overview/).
It reads them from the lockfiles, the workflows, `.python-version`, `pyproject.toml`,
the plugin catalog and the skills, so don't edit either file by hand.
`uv run skillcheck --bom-check` names a file that no longer matches. The weekly
freshness run and the release workflow both run it.

## What it ships

| Plugin | Version | License | Skill | What it carries |
|---|---|---|---|---|
| `standards` | 0.1.6 | CC0-1.0 | `project-bootstrap-and-audit` | standard v0.41.0 |
| `engineering` | 0.1.6 | Apache-2.0 | `git-workflows` | reviewed 2026-10-05 |
| `engineering` | 0.1.6 | Apache-2.0 | `house-style` | reviewed 2026-10-05 |

## Languages

| Language | Tracked files |
|---|---|
| Markdown | 69 |
| Python | 26 |
| YAML | 22 |
| JSON | 9 |
| Shell | 2 |
| TOML | 2 |

## Runtimes and tools

| Name | Version | Set in | Note |
|---|---|---|---|
| Python | 3.14 | `.python-version` | `pyproject.toml` requires >=3.14 |
| uv_build | >=0.12.19,<0.13 | `pyproject.toml` | build backend |
| GitHub-hosted runner | ubuntu-latest | `.github/workflows/ci.yml`, `.github/workflows/commit-subjects.yml`, `.github/workflows/freshness.yml`, `.github/workflows/prose.yml`, `.github/workflows/release.yml` | — |
| Go | 1.27 | `.github/workflows/ci.yml`, `.github/workflows/prose.yml` | — |
| Node.js | 24 | `.github/workflows/ci.yml` | — |
| gitleaks | v8.30.1 | `.github/workflows/ci.yml` | — |
| uv | 0.12.18 | `.github/workflows/ci.yml`, `.github/workflows/freshness.yml`, `.github/workflows/release.yml` | — |
| vale | v3.24.0 | `.github/workflows/prose.yml` | — |

## Python packages

Exact versions from `uv.lock`. A development-only package isn't part of what the
plugins ship.

```text
skillcheck 0.0.0 (this repository's checks)
├── pytest 9.1.1 (dev)
│   ├── colorama 0.4.6 (dev; only when sys_platform == 'win32')
│   ├── iniconfig 2.3.0 (dev)
│   ├── packaging 26.3 (dev)
│   ├── pluggy 1.6.0 (dev)
│   └── pygments 2.21.0 (dev)
├── pytest-cov 7.1.0 (dev)
│   ├── coverage 7.16.1 (dev)
│   ├── pluggy 1.6.0 (dev)
│   └── pytest 9.1.1 (dev) (listed above)
├── pyyaml 6.0.3
├── ruff 0.16.10 (dev)
└── zizmor 1.30.1 (dev)
```

## Node packages

Exact versions from `package-lock.json`. A development-only package isn't part of what the
plugins ship.

```text
package.json
└── @anthropic-ai/claude-code 2.1.283 (dev)
    ├── @anthropic-ai/claude-code-darwin-arm64 2.1.283 (dev; optional)
    ├── @anthropic-ai/claude-code-darwin-x64 2.1.283 (dev; optional)
    ├── @anthropic-ai/claude-code-linux-arm64 2.1.283 (dev; optional)
    ├── @anthropic-ai/claude-code-linux-arm64-musl 2.1.283 (dev; optional)
    ├── @anthropic-ai/claude-code-linux-x64 2.1.283 (dev; optional)
    ├── @anthropic-ai/claude-code-linux-x64-musl 2.1.283 (dev; optional)
    ├── @anthropic-ai/claude-code-win32-arm64 2.1.283 (dev; optional)
    └── @anthropic-ai/claude-code-win32-x64 2.1.283 (dev; optional)
```

## GitHub Actions

| Action | Version | Pinned commit | Used in |
|---|---|---|---|
| `actions/checkout` | v7.0.1 | `3d3c42e5aac5ba805825da76410c181273ba90b1` | `.github/workflows/ci.yml`, `.github/workflows/commit-subjects.yml`, `.github/workflows/freshness.yml`, `.github/workflows/prose.yml`, `.github/workflows/release.yml` |
| `actions/download-artifact` | v8.0.1 | `3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c` | `.github/workflows/release.yml` |
| `actions/setup-go` | v7.0.0 | `b7ad1dad31e06c5925ef5d2fc7ad053ef454303e` | `.github/workflows/ci.yml`, `.github/workflows/prose.yml` |
| `actions/setup-node` | v7.0.0 | `820762786026740c76f36085b0efc47a31fe5020` | `.github/workflows/ci.yml` |
| `actions/upload-artifact` | v7.0.1 | `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` | `.github/workflows/release.yml` |
| `astral-sh/setup-uv` | v10.2.0 | `c18668ad3cf93ea998bef934396af7bb5c839dc7` | `.github/workflows/ci.yml`, `.github/workflows/freshness.yml`, `.github/workflows/release.yml` |

## Services

| Service | Provider | What for | Address |
|---|---|---|---|
| GitHub | GitHub | Hosts the repository, its pull requests, its rulesets and its releases. | https://github.com/rmccann-hub/claude-code-skills |
| GitHub Actions | GitHub | Runs the workflows: ci, commit-subjects, freshness, prose, release. | https://github.com/rmccann-hub/claude-code-skills/actions |
| Dependabot | GitHub | Opens pull requests that update dependencies: github-actions, npm, uv. | documented at https://docs.github.com/en/code-security/dependabot |
| PyPI | Python Software Foundation | Serves the Python packages in `uv.lock`. | https://pypi.org/simple |
| npm registry | GitHub | Serves the packages in `package-lock.json`. | https://registry.npmjs.org |
| Go module proxy and checksum database | Google | Serves the Go modules CI installs, and the checksums `go install` verifies. | https://proxy.golang.org, https://sum.golang.org |
| Claude Code plugin marketplace | Anthropic | Claude Code installs the plugins from `.claude-plugin/marketplace.json`. | documented at https://code.claude.com/docs/en/plugin-marketplaces |
| claude.ai | Anthropic | The owner uploads the skills to their account, which is how they reach cloud sessions. | https://claude.ai |

## Sources the skills' facts rely on

Each skill's dated facts, in its `references/facts.md`, name where each was read. The
weekly freshness run looks for every quote at its source again.

| Skill | Source | Facts |
|---|---|---|
| `project-bootstrap-and-audit` | no `references/facts.md` | — |
| `git-workflows` | docs.github.com | 36 |
| `git-workflows` | git-scm.com | 17 |
| `git-workflows` | raw.githubusercontent.com | 7 |
| `git-workflows` | github.blog | 5 |
| `git-workflows` | docs.kernel.org | 3 |
| `git-workflows` | pypi.org | 3 |
| `git-workflows` | github.com | 2 |
| `git-workflows` | keepachangelog.com | 2 |
| `git-workflows` | rustc-dev-guide.rust-lang.org | 2 |
| `git-workflows` | abseil.io | 1 |
| `git-workflows` | blog.rust-lang.org | 1 |
| `git-workflows` | chromium.googlesource.com | 1 |
| `git-workflows` | cli.github.com | 1 |
| `git-workflows` | cveawg.mitre.org | 1 |
| `git-workflows` | devguide.python.org | 1 |
| `git-workflows` | docs.astral.sh | 1 |
| `git-workflows` | docs.prow.k8s.io | 1 |
| `git-workflows` | dora.dev | 1 |
| `git-workflows` | go.dev | 1 |
| `git-workflows` | llvm.org | 1 |
| `git-workflows` | martinfowler.com | 1 |
| `git-workflows` | nvie.com | 1 |
| `git-workflows` | pip.pypa.io | 1 |
| `git-workflows` | semgrep.dev | 1 |
| `git-workflows` | semver.org | 1 |
| `git-workflows` | towncrier.readthedocs.io | 1 |
| `git-workflows` | www.conventionalcommits.org | 1 |
| `house-style` | developers.google.com | 4 |
| `house-style` | vale.sh | 4 |
| `house-style` | raw.githubusercontent.com | 2 |
| `house-style` | github.com | 1 |
| `house-style` | learn.microsoft.com | 1 |
| `house-style` | www.gov.uk | 1 |
