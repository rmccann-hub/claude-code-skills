# Dependency map

What `claude-code-skills` 0.1.29 is built from, runs on and relies on: the
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
| `standards` | 0.1.29 | CC0-1.0 | `project-bootstrap-and-audit` | standard v0.49.1 |
| `engineering` | 0.1.29 | Apache-2.0 | `agent-engineering` | reviewed 2026-11-11 |
| `engineering` | 0.1.29 | Apache-2.0 | `architecture` | reviewed 2026-11-11 |
| `engineering` | 0.1.29 | Apache-2.0 | `coding` | reviewed 2026-10-27 |
| `engineering` | 0.1.29 | Apache-2.0 | `git-workflows` | reviewed 2026-11-03 |
| `engineering` | 0.1.29 | Apache-2.0 | `house-style` | reviewed 2026-10-27 |
| `engineering` | 0.1.29 | Apache-2.0 | `human-factors` | reviewed 2026-11-11 |
| `engineering` | 0.1.29 | Apache-2.0 | `operations` | reviewed 2026-11-11 |
| `engineering` | 0.1.29 | Apache-2.0 | `optimization-and-scheduling` | reviewed 2026-11-11 |
| `engineering` | 0.1.29 | Apache-2.0 | `security` | reviewed 2026-11-11 |
| `engineering` | 0.1.29 | Apache-2.0 | `testing` | reviewed 2026-11-11 |
| `engineering` | 0.1.29 | Apache-2.0 | `user-experience` | reviewed 2026-11-11 |

## Languages

| Language | Tracked files |
|---|---|
| Markdown | 167 |
| JSON | 75 |
| Python | 53 |
| YAML | 23 |
| Shell | 4 |
| TOML | 2 |

## Runtimes and tools

| Name | Version | Set in | Note |
|---|---|---|---|
| Python | 3.15 | `.python-version` | `pyproject.toml` requires >=3.14 |
| uv_build | >=0.13.6,<0.14 | `pyproject.toml` | build backend |
| GitHub-hosted runner | ubuntu-latest | `.github/workflows/ci.yml`, `.github/workflows/commit-subjects.yml`, `.github/workflows/freshness.yml`, `.github/workflows/hold.yml`, `.github/workflows/prose.yml`, `.github/workflows/release.yml` | — |
| Go | 1.27 | `.github/workflows/ci.yml`, `.github/workflows/prose.yml` | — |
| Node.js | 26 | `.github/workflows/ci.yml` | — |
| gitleaks | v8.30.1 | `.github/workflows/ci.yml` | — |
| uv | 0.13.5 | `.github/workflows/ci.yml`, `.github/workflows/freshness.yml`, `.github/workflows/release.yml` | — |
| vale | v3.26.0 | `.github/workflows/prose.yml` | — |

## Python packages

Exact versions from `uv.lock`. A development-only package isn't part of what the
plugins ship.

```text
skillcheck 0.0.0 (this repository's checks)
├── pytest 9.2.0 (dev)
│   ├── colorama 0.4.6 (dev; only when sys_platform == 'win32')
│   ├── iniconfig 2.3.1 (dev)
│   ├── packaging 26.3 (dev)
│   ├── pluggy 1.7.0 (dev)
│   └── pygments 2.21.0 (dev)
├── pytest-cov 7.1.0 (dev)
│   ├── coverage 7.17.2 (dev)
│   ├── pluggy 1.7.0 (dev)
│   └── pytest 9.2.0 (dev) (listed above)
├── pyyaml 6.0.3
├── ruff 0.17.4 (dev)
├── shellcheck-py 0.11.0.1 (dev)
└── zizmor 1.32.0 (dev)
```

## Node packages

Exact versions from `package-lock.json`. A development-only package isn't part of what the
plugins ship.

```text
package.json
└── @anthropic-ai/claude-code 2.1.319 (dev)
    ├── @anthropic-ai/claude-code-darwin-arm64 2.1.319 (dev; optional)
    ├── @anthropic-ai/claude-code-darwin-x64 2.1.319 (dev; optional)
    ├── @anthropic-ai/claude-code-linux-arm64 2.1.319 (dev; optional)
    ├── @anthropic-ai/claude-code-linux-arm64-musl 2.1.319 (dev; optional)
    ├── @anthropic-ai/claude-code-linux-x64 2.1.319 (dev; optional)
    ├── @anthropic-ai/claude-code-linux-x64-musl 2.1.319 (dev; optional)
    ├── @anthropic-ai/claude-code-win32-arm64 2.1.319 (dev; optional)
    └── @anthropic-ai/claude-code-win32-x64 2.1.319 (dev; optional)
```

## GitHub Actions

| Action | Version | Pinned commit | Used in |
|---|---|---|---|
| `actions/attest` | v4.2.2 | `1e69f48acb82d1966a394da916b4c1698aa569d6` | `.github/workflows/release.yml` |
| `actions/checkout` | v7.0.1 | `3d3c42e5aac5ba805825da76410c181273ba90b1` | `.github/workflows/ci.yml`, `.github/workflows/commit-subjects.yml`, `.github/workflows/freshness.yml`, `.github/workflows/prose.yml`, `.github/workflows/release.yml` |
| `actions/download-artifact` | v8.0.2 | `9000827ccba6bdab643e8b6fd33ac0654aef8333` | `.github/workflows/release.yml` |
| `actions/setup-go` | v7.0.0 | `b7ad1dad31e06c5925ef5d2fc7ad053ef454303e` | `.github/workflows/ci.yml`, `.github/workflows/prose.yml` |
| `actions/setup-node` | v7.1.0 | `949feb2413d6458794dcd2491c4babbbce0c15c1` | `.github/workflows/ci.yml` |
| `actions/upload-artifact` | v7.0.2 | `cf430e030ddbb5b0abf93d22962f4752f3646cd9` | `.github/workflows/release.yml` |
| `astral-sh/setup-uv` | v10.3.3 | `68559e99cc807c1eb7e9238fd43a15bba460eec2` | `.github/workflows/ci.yml`, `.github/workflows/freshness.yml`, `.github/workflows/release.yml` |

## Services

| Service | Provider | What for | Address |
|---|---|---|---|
| GitHub | GitHub | Hosts the repository, its pull requests, its rulesets and its releases. | https://github.com/rmccann-hub/claude-code-skills |
| GitHub Actions | GitHub | Runs the workflows: ci, commit-subjects, freshness, hold, prose, release. | https://github.com/rmccann-hub/claude-code-skills/actions |
| Dependabot | GitHub | Opens pull requests that update dependencies: github-actions, npm, uv. | documented at https://docs.github.com/en/code-security/dependabot |
| PyPI | Python Software Foundation | Serves the Python packages in `uv.lock`. | https://pypi.org/simple |
| npm registry | GitHub | Serves the packages in `package-lock.json`. | https://registry.npmjs.org |
| Go module proxy and checksum database | Google | Serves the Go modules CI installs, and the checksums `go install` verifies. | https://proxy.golang.org, https://sum.golang.org |
| Claude Code plugin marketplace | Anthropic | Claude Code installs the plugins from `.claude-plugin/marketplace.json`. | documented at https://code.claude.com/docs/en/plugin-marketplaces |
| claude.ai | Anthropic | The owner's account installs the plugins from this repository's marketplace, which is how they reach chat; cloud sessions get them from the release instead. | https://claude.ai |

## Sources the skills' facts rely on

Each skill's dated facts, in its modules' Facts sections or its `references/facts.md`,
name where each was read. The weekly freshness run looks for every quote at its source
again.

| Skill | Source | Facts |
|---|---|---|
| `project-bootstrap-and-audit` | no dated facts | — |
| `agent-engineering` | code.claude.com | 27 |
| `agent-engineering` | arxiv.org | 8 |
| `agent-engineering` | agentskills.io | 5 |
| `agent-engineering` | raw.githubusercontent.com | 3 |
| `agent-engineering` | docs.github.com | 2 |
| `agent-engineering` | platform.claude.com | 2 |
| `agent-engineering` | agents.md | 1 |
| `agent-engineering` | ai.meta.com | 1 |
| `agent-engineering` | cursor.com | 1 |
| `agent-engineering` | cveawg.mitre.org | 1 |
| `agent-engineering` | developers.openai.com | 1 |
| `agent-engineering` | docs.pact.io | 1 |
| `agent-engineering` | geminicli.com | 1 |
| `agent-engineering` | git-scm.com | 1 |
| `agent-engineering` | github.blog | 1 |
| `agent-engineering` | google.github.io | 1 |
| `agent-engineering` | invariantlabs.ai | 1 |
| `agent-engineering` | martin.kleppmann.com | 1 |
| `agent-engineering` | oasdiff.com | 1 |
| `agent-engineering` | simonwillison.net | 1 |
| `agent-engineering` | support.claude.com | 1 |
| `agent-engineering` | www.anthropic.com | 1 |
| `architecture` | learn.microsoft.com | 3 |
| `architecture` | git-scm.com | 2 |
| `architecture` | go.dev | 2 |
| `architecture` | abseil.io | 1 |
| `architecture` | angular.dev | 1 |
| `architecture` | doc.rust-lang.org | 1 |
| `architecture` | docs.npmjs.com | 1 |
| `architecture` | github.com | 1 |
| `architecture` | nodejs.org | 1 |
| `architecture` | packaging.python.org | 1 |
| `architecture` | peps.python.org | 1 |
| `architecture` | pkg.go.dev | 1 |
| `architecture` | pnpm.io | 1 |
| `coding` | learn.microsoft.com | 68 |
| `coding` | docs.python.org | 31 |
| `coding` | raw.githubusercontent.com | 20 |
| `coding` | nodejs.org | 19 |
| `coding` | cheatsheetseries.owasp.org | 17 |
| `coding` | www.w3.org | 17 |
| `coding` | tiswww.case.edu | 16 |
| `coding` | man7.org | 15 |
| `coding` | developer.mozilla.org | 13 |
| `coding` | mesonbuild.com | 12 |
| `coding` | pubs.opengroup.org | 11 |
| `coding` | docs.astral.sh | 9 |
| `coding` | gcc.gnu.org | 9 |
| `coding` | pypi.org | 9 |
| `coding` | www.rfc-editor.org | 7 |
| `coding` | go.dev | 6 |
| `coding` | clang.llvm.org | 5 |
| `coding` | cwe.mitre.org | 5 |
| `coding` | devblogs.microsoft.com | 5 |
| `coding` | html.spec.whatwg.org | 5 |
| `coding` | www.typescriptlang.org | 5 |
| `coding` | curl.se | 4 |
| `coding` | dotnet.microsoft.com | 4 |
| `coding` | google.github.io | 4 |
| `coding` | mypy.readthedocs.io | 4 |
| `coding` | packaging.python.org | 4 |
| `coding` | typescript-eslint.io | 4 |
| `coding` | git-scm.com | 3 |
| `coding` | web.dev | 3 |
| `coding` | best.openssf.org | 2 |
| `coding` | builder.aws.com | 2 |
| `coding` | crates.io | 2 |
| `coding` | devguide.python.org | 2 |
| `coding` | docs.pydantic.dev | 2 |
| `coding` | docs.rs | 2 |
| `coding` | eslint.org | 2 |
| `coding` | man.freebsd.org | 2 |
| `coding` | openjdk.org | 2 |
| `coding` | opentelemetry.io | 2 |
| `coding` | prometheus.io | 2 |
| `coding` | pyyaml.org | 2 |
| `coding` | registry.npmjs.org | 2 |
| `coding` | repo1.maven.org | 2 |
| `coding` | rust-lang.github.io | 2 |
| `coding` | sre.google | 2 |
| `coding` | www.brendangregg.com | 2 |
| `coding` | www.nuget.org | 2 |
| `coding` | www.shellcheck.net | 2 |
| `coding` | yaml.org | 2 |
| `coding` | 12factor.net | 1 |
| `coding` | api.nuget.org | 1 |
| `coding` | arxiv.org | 1 |
| `coding` | biomejs.dev | 1 |
| `coding` | check-jsonschema.readthedocs.io | 1 |
| `coding` | community.owasp.org | 1 |
| `coding` | design-system.service.gov.uk | 1 |
| `coding` | doc.qt.io | 1 |
| `coding` | doc.rust-lang.org | 1 |
| `coding` | docs.github.com | 1 |
| `coding` | documentation.ubuntu.com | 1 |
| `coding` | git.kernel.org | 1 |
| `coding` | gmplib.org | 1 |
| `coding` | grafana.com | 1 |
| `coding` | jinja.palletsprojects.com | 1 |
| `coding` | json-schema.org | 1 |
| `coding` | lists.gnu.org | 1 |
| `coding` | llvm.org | 1 |
| `coding` | logback.qos.ch | 1 |
| `coding` | logging.apache.org | 1 |
| `coding` | manpages.debian.org | 1 |
| `coding` | martinfowler.com | 1 |
| `coding` | neverworkintheory.org | 1 |
| `coding` | oxc.rs | 1 |
| `coding` | packages.debian.org | 1 |
| `coding` | peps.python.org | 1 |
| `coding` | pester.dev | 1 |
| `coding` | pkg.go.dev | 1 |
| `coding` | rubygems.org | 1 |
| `coding` | savannah.gnu.org | 1 |
| `coding` | services.nvd.nist.gov | 1 |
| `coding` | sourceware.org | 1 |
| `coding` | specifications.freedesktop.org | 1 |
| `coding` | src.fedoraproject.org | 1 |
| `coding` | support.apple.com | 1 |
| `coding` | tc39.es | 1 |
| `coding` | toml.io | 1 |
| `coding` | valgrind.org | 1 |
| `coding` | www.cisa.gov | 1 |
| `coding` | www.freedesktop.org | 1 |
| `coding` | www.kernel.org | 1 |
| `coding` | www.open-std.org | 1 |
| `coding` | www.powershellgallery.com | 1 |
| `coding` | www.unicode.org | 1 |
| `coding` | yamllint.readthedocs.io | 1 |
| `coding` | zod.dev | 1 |
| `git-workflows` | docs.github.com | 64 |
| `git-workflows` | git-scm.com | 18 |
| `git-workflows` | raw.githubusercontent.com | 10 |
| `git-workflows` | github.blog | 7 |
| `git-workflows` | code.claude.com | 4 |
| `git-workflows` | keepachangelog.com | 4 |
| `git-workflows` | docs.kernel.org | 3 |
| `git-workflows` | pypi.org | 3 |
| `git-workflows` | cli.github.com | 2 |
| `git-workflows` | devguide.python.org | 2 |
| `git-workflows` | docs.zizmor.sh | 2 |
| `git-workflows` | github.com | 2 |
| `git-workflows` | martinfowler.com | 2 |
| `git-workflows` | nodejs.org | 2 |
| `git-workflows` | peps.python.org | 2 |
| `git-workflows` | rustc-dev-guide.rust-lang.org | 2 |
| `git-workflows` | semver.org | 2 |
| `git-workflows` | 12factor.net | 1 |
| `git-workflows` | abseil.io | 1 |
| `git-workflows` | blog.rust-lang.org | 1 |
| `git-workflows` | chromium.googlesource.com | 1 |
| `git-workflows` | cveawg.mitre.org | 1 |
| `git-workflows` | docs.astral.sh | 1 |
| `git-workflows` | docs.prow.k8s.io | 1 |
| `git-workflows` | dora.dev | 1 |
| `git-workflows` | go.dev | 1 |
| `git-workflows` | llvm.org | 1 |
| `git-workflows` | nvie.com | 1 |
| `git-workflows` | pip.pypa.io | 1 |
| `git-workflows` | semgrep.dev | 1 |
| `git-workflows` | sre.google | 1 |
| `git-workflows` | towncrier.readthedocs.io | 1 |
| `git-workflows` | www.conventionalcommits.org | 1 |
| `house-style` | developers.google.com | 5 |
| `house-style` | raw.githubusercontent.com | 4 |
| `house-style` | vale.sh | 4 |
| `house-style` | www.sphinx-doc.org | 3 |
| `house-style` | docs.vale.sh | 2 |
| `house-style` | github.com | 2 |
| `house-style` | learn.microsoft.com | 2 |
| `house-style` | diataxis.fr | 1 |
| `house-style` | doc.rust-lang.org | 1 |
| `house-style` | docs.djangoproject.com | 1 |
| `house-style` | docs.github.com | 1 |
| `house-style` | docs.python.org | 1 |
| `house-style` | platform.claude.com | 1 |
| `house-style` | pubs.opengroup.org | 1 |
| `house-style` | squidfunk.github.io | 1 |
| `house-style` | www.gov.uk | 1 |
| `house-style` | www.mkdocs.org | 1 |
| `house-style` | zensical.org | 1 |
| `human-factors` | books.hse.gov.uk | 4 |
| `human-factors` | pmc.ncbi.nlm.nih.gov | 4 |
| `human-factors` | ixdf.org | 3 |
| `human-factors` | arxiv.org | 2 |
| `human-factors` | journals.sagepub.com | 2 |
| `human-factors` | aisel.aisnet.org | 1 |
| `human-factors` | ckrybus.com | 1 |
| `human-factors` | eric.ed.gov | 1 |
| `human-factors` | hciengineering.net | 1 |
| `human-factors` | link.springer.com | 1 |
| `human-factors` | openai.com | 1 |
| `human-factors` | pages.ucsd.edu | 1 |
| `human-factors` | papers.ssrn.com | 1 |
| `human-factors` | plato.stanford.edu | 1 |
| `human-factors` | press.uchicago.edu | 1 |
| `human-factors` | pressblog.uchicago.edu | 1 |
| `human-factors` | pubmed.ncbi.nlm.nih.gov | 1 |
| `human-factors` | repositorio.ispa.pt | 1 |
| `human-factors` | www.chesterton.org | 1 |
| `human-factors` | www.england.nhs.uk | 1 |
| `human-factors` | www.konsortswd.de | 1 |
| `human-factors` | www.scielo.br | 1 |
| `human-factors` | www.sciencedirect.com | 1 |
| `operations` | learn.microsoft.com | 22 |
| `operations` | docs.docker.com | 12 |
| `operations` | raw.githubusercontent.com | 4 |
| `operations` | github.com | 3 |
| `operations` | ubuntu.com | 3 |
| `operations` | www.freedesktop.org | 3 |
| `operations` | www.rfc-editor.org | 3 |
| `operations` | csrc.nist.gov | 2 |
| `operations` | docs.fedoraproject.org | 2 |
| `operations` | man.openbsd.org | 2 |
| `operations` | man7.org | 2 |
| `operations` | suricata.io | 2 |
| `operations` | wiki.nftables.org | 2 |
| `operations` | www.cisa.gov | 2 |
| `operations` | www.debian.org | 2 |
| `operations` | access.redhat.com | 1 |
| `operations` | blog.snort.org | 1 |
| `operations` | dnf.readthedocs.io | 1 |
| `operations` | docs.sigstore.dev | 1 |
| `operations` | fedoraproject.org | 1 |
| `operations` | firewalld.org | 1 |
| `operations` | grafana.com | 1 |
| `operations` | jsonlines.org | 1 |
| `operations` | netfilter.org | 1 |
| `operations` | pypi.org | 1 |
| `operations` | techcommunity.microsoft.com | 1 |
| `operations` | wiki.almalinux.org | 1 |
| `operations` | www.netfilter.org | 1 |
| `operations` | www.wi-fi.org | 1 |
| `operations` | www.wireguard.com | 1 |
| `operations` | yamato-security.github.io | 1 |
| `operations` | zeek.org | 1 |
| `optimization-and-scheduling` | github.com | 14 |
| `optimization-and-scheduling` | arxiv.org | 2 |
| `optimization-and-scheduling` | assets.publishing.service.gov.uk | 1 |
| `optimization-and-scheduling` | d-krupke.github.io | 1 |
| `optimization-and-scheduling` | docs.gurobi.com | 1 |
| `optimization-and-scheduling` | docs.timefold.ai | 1 |
| `optimization-and-scheduling` | groups.google.com | 1 |
| `optimization-and-scheduling` | hub.docker.com | 1 |
| `optimization-and-scheduling` | mistic.iict-heig-vd.ch | 1 |
| `optimization-and-scheduling` | plato.asu.edu | 1 |
| `optimization-and-scheduling` | pubsonline.informs.org | 1 |
| `optimization-and-scheduling` | pypi.org | 1 |
| `optimization-and-scheduling` | scipopt.org | 1 |
| `optimization-and-scheduling` | support.gurobi.com | 1 |
| `optimization-and-scheduling` | www.coin-or.org | 1 |
| `optimization-and-scheduling` | www.ibm.com | 1 |
| `optimization-and-scheduling` | www.schedulingbenchmarks.org | 1 |
| `security` | cheatsheetseries.owasp.org | 7 |
| `security` | owasp.org | 6 |
| `security` | cwe.mitre.org | 1 |
| `security` | go.dev | 1 |
| `security` | pages.nist.gov | 1 |
| `security` | www.threatmodelingmanifesto.org | 1 |
| `testing` | arxiv.org | 9 |
| `testing` | code.claude.com | 8 |
| `testing` | gitlab.com | 4 |
| `testing` | testing.googleblog.com | 4 |
| `testing` | github.blog | 3 |
| `testing` | raw.githubusercontent.com | 3 |
| `testing` | docs.kernelci.org | 2 |
| `testing` | docs.pytest.org | 2 |
| `testing` | pypi.org | 2 |
| `testing` | registry.npmjs.org | 2 |
| `testing` | research.google.com | 2 |
| `testing` | www.anthropic.com | 2 |
| `testing` | www.microsoft.com | 2 |
| `testing` | api.nuget.org | 1 |
| `testing` | blitiri.com.ar | 1 |
| `testing` | coverage.readthedocs.io | 1 |
| `testing` | crates.io | 1 |
| `testing` | developer.apple.com | 1 |
| `testing` | docs.cypress.io | 1 |
| `testing` | docs.pact.io | 1 |
| `testing` | go.dev | 1 |
| `testing` | growing-object-oriented-software.com | 1 |
| `testing` | jestjs.io | 1 |
| `testing` | lava.readthedocs.io | 1 |
| `testing` | learn.microsoft.com | 1 |
| `testing` | man7.org | 1 |
| `testing` | open.qa | 1 |
| `testing` | pester.dev | 1 |
| `testing` | repo.packagist.org | 1 |
| `testing` | repo1.maven.org | 1 |
| `testing` | rubygems.org | 1 |
| `testing` | testcontainers.com | 1 |
| `testing` | www.pantsbuild.org | 1 |
| `user-experience` | www.nngroup.com | 16 |
| `user-experience` | developer.gnome.org | 6 |
| `user-experience` | develop.kde.org | 5 |
| `user-experience` | pypi.org | 5 |
| `user-experience` | developer.apple.com | 3 |
| `user-experience` | docs.gtk.org | 3 |
| `user-experience` | chernev.com | 2 |
| `user-experience` | doc.qt.io | 2 |
| `user-experience` | learn.microsoft.com | 2 |
| `user-experience` | playwright.dev | 2 |
| `user-experience` | api.nuget.org | 1 |
| `user-experience` | measuringu.com | 1 |
| `user-experience` | scheibehenne.com | 1 |
| `user-experience` | www.cs.umd.edu | 1 |
