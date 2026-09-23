# Roadmap

What this repository ships and what comes next, one row per skill. `skillcheck` keeps this file
in step with `skills/`, the README and the catalog, so it can't drift: a skill that ships
without a `shipped` row here, or a `shipped` row with no skill behind it, fails CI.

- **Status** (closed set): `shipped`, `building`, `researching`, `planned`.
- **Coverage:** `core` is the owner's stack, covered deepest and built first. `standard` gets
  full coverage. `on request` is named now and built when a repository needs it.
- **Research:** the run in `research/prompts/` whose results the skill is built from.

The PROJECT-BOOTSTRAP-AND-AUDIT standard covers configuration and process, and says it doesn't
judge code. The skills in sections B to F cover the code itself, beside the standard rather
than inside it.

## A. How the work is done

| Skill | Covers | Status | Coverage | Research |
|---|---|---|---|---|
| `project-bootstrap-and-audit` | Set up a new repository, retrofit or audit an existing one, re-check, release, prune: the standard, v0.35.0 | shipped | core | none |
| `keeping-current` | Sweep a repository for versions behind, end-of-life dates, deprecated APIs and stale facts; propose the updates | planned | core | R05 |
| `skill-builder` | Design, write, test and tune a skill | planned | core | done |
| `agent-context-files` | AGENTS.md, CLAUDE.md, rules, settings, hooks, subagents, MCP, other agents' files | planned | core | R01 |

## B. Engineering practice, for every language

| Skill | Covers | Status | Coverage | Research |
|---|---|---|---|---|
| `repo-structure` | Layouts by project type, where each file goes, naming files and folders | planned | core | R02 |
| `documentation` | READMEs, decision records, docs sites, diagrams, file size and splitting | planned | core | R02 |
| `code-style` | Naming, formatting, structure, comments and docstrings | planned | core | R03 |
| `types` | Static and gradual typing, strictness, type checkers, types at trust boundaries | planned | core | R03 |
| `input-handling` | Validation, sanitization and output encoding by context | planned | core | R04 |
| `secure-coding` | OWASP Top 10, ASVS, CWE Top 25, authentication, cryptography, threat modelling | planned | core | R04 |
| `supply-chain-security` | Dependencies, lockfiles, pinning, SBOMs, provenance, malicious and hallucinated packages | planned | core | R05 |
| `ai-agent-security` | Prompt injection, permission design, secret exposure, MCP, skills as a supply chain, hidden Unicode | planned | core | R01 |
| `error-handling` | Failure classes, retries, timeouts, circuit breakers, user messages, RFC 9457 | planned | core | R07 |
| `testing` | Strategy, test doubles, fixtures, property-based and mutation testing, flaky tests | planned | core | R06 |
| `api-design` | REST, OpenAPI, GraphQL, gRPC, auth flows, pagination, versioning, webhooks | planned | core | R19 |
| `data-and-sql` | Schema design, migrations, SQL style, indexing, transactions | planned | core | R14 |
| `git-and-review` | Branching, commits, pull requests, code review | planned | core | R08 |
| `ci-cd` | Pipelines, Actions hardening, caching, environments, deployment | planned | core | R08 |
| `versioning-and-releases` | SemVer, changelogs, release notes, deprecation policy, support windows | planned | core | R05 |
| `legacy-modernization` | Reading legacy code, characterization tests, the strangler fig pattern, migration playbooks | planned | core | R17 |
| `logging-and-observability` | Structured logs, OpenTelemetry, metrics, tracing, what never to log | planned | standard | R07 |
| `performance-and-concurrency` | Profiling, complexity, caching, async and threads | planned | standard | R07 |
| `configuration` | Layered config, environment variables, validation at startup, secret stores | planned | standard | R04 |
| `architecture-and-design` | Principles, boundaries, decision records, diagrams, planning, refactoring | planned | standard | R19 |
| `accessibility` | WCAG 2.2, ARIA, contrast, testing tools | planned | standard | R18 |
| `internationalization` | Unicode, locales, time zones, formats, right-to-left text | planned | standard | R18 |
| `privacy-and-compliance` | Personal data, retention, licences and notices, obligations on software publishers | planned | standard | R18 |

## C. Languages in current use

| Skill | Covers | Status | Coverage | Research |
|---|---|---|---|---|
| `python` | Python 3, its toolchain and idioms | planned | core | R09 |
| `typescript-javascript` | TypeScript, JavaScript, Node.js | planned | core | R10 |
| `html-css` | HTML, CSS, front-end security | planned | core | R10 |
| `csharp-dotnet` | C# and .NET | planned | core | R11 |
| `powershell` | PowerShell 7 and Windows PowerShell 5.1 | planned | core | R11 |
| `shell` | Bash and POSIX sh | planned | core | R15 |
| `vba` | VBA in Office applications | planned | core | R16 |
| `go` | Go | planned | standard | R12 |
| `rust` | Rust | planned | standard | R12 |
| `c` | C | planned | standard | R12 |
| `cpp` | C++ | planned | standard | R12 |
| `java` | Java | planned | standard | R13 |
| `kotlin` | Kotlin | planned | standard | R13 |
| `php` | PHP | planned | standard | R13 |
| `ruby` | Ruby | planned | standard | R13 |
| `config-formats` | YAML, JSON, TOML, XML | planned | standard | R15 |
| `markdown` | Markdown for people and for agents | planned | standard | R02 |

## D. Languages from the past: read, maintain, modernize

| Skill | Covers | Status | Coverage | Research |
|---|---|---|---|---|
| `legacy-languages` | One reference per language, for example VB6, VBScript, classic ASP, .NET Framework, COBOL and Python 2 | planned | core | R17 |

## E. Platforms and domains

| Skill | Covers | Status | Coverage | Research |
|---|---|---|---|---|
| `windows-server` | AD, Group Policy, DNS/DHCP, certificates, file services, updates, hardening | planned | core | R11 |
| `excel` | Workbooks from code, formulas, Power Query, DAX, Office Scripts, add-ins | planned | core | R16 |
| `word-documents` | Generating and filling Word templates | planned | core | R16 |
| `epicor-kinetic` | BPM, BAQ, REST API v2, Functions, from public knowledge only | planned | core | R16 |
| `solidworks-api` | VBA and C# macros, documents, drawings, sheet metal, exports | planned | core | R16 |
| `linux` | Administration and troubleshooting across distributions | planned | standard | R15 |
| `networking-security` | Firewalls, segmentation, IDS, VPN, Wi-Fi, DNS | planned | standard | R15 |
| `containers` | Dockerfiles, Compose, hardening, registries | planned | standard | R15 |
| `log-analysis` | Event logs, crash dumps, journals, application logs | planned | standard | R07 |
| `optimization-and-scheduling` | Solvers, business rules as constraints, the human factors in plans | planned | standard | R19 |
| `linux-gaming` | Proton, Steam, handhelds | planned | on request | R15 |
| `kubernetes` | Clusters, workloads, the Gateway API | planned | on request | R15 |
| `cloud` | Azure, AWS and Google Cloud baselines | planned | on request | R15 |
| `infrastructure-as-code` | Terraform, OpenTofu, Bicep | planned | on request | R15 |

## F. Output and presentation

| Skill | Covers | Status | Coverage | Research |
|---|---|---|---|---|
| `visual-theme` | Design tokens, palettes, typography, dark mode | planned | standard | R20 |
| `data-visualization` | Choosing charts, accessible charts, charting libraries | planned | standard | R20 |

## Repository

These aren't skills, so `skillcheck` doesn't match them against `skills/`. Each waits on its
trigger.

| Item | What it is | Status | Trigger |
|---|---|---|---|
| Weekly currency check | A scheduled workflow that flags stale facts, versions behind, and end of life within six months | planned | the first category skill ships |
| `copier` template | The standard's starter files, so a new repository is set up without a session | planned | the first repository set up from this one |
| Reusable workflows | This repository's CI gates, callable from other repositories | planned | a second repository wants this CI |
| `upstream-defects.md` | The standard's register of upstream defects shared across repositories | planned | the first upstream defect found |
