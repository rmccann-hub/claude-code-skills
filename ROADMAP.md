# Roadmap

What this repository ships and what comes next, one row per skill. `skillcheck` keeps this file
in step with `skills/`, the README and the catalog, so it can't drift: a skill that ships
without a `shipped` row here, or a `shipped` row with no skill behind it, fails CI.

- **Status** (closed set): `shipped`, `building`, `researching`, `planned`.
- **Coverage:** `core` is the owner's stack, covered deepest and built first. `standard` gets
  full coverage. `on request` is named now and built when a repository needs it.
- **Research:** the runs in `research/prompts/` whose results the skill is built from.

The PROJECT-BOOTSTRAP-AND-AUDIT standard covers configuration and process, and says it doesn't
judge code. The skills in sections B to F cover the code itself, beside the standard rather
than inside it.

## A. How the work is done

| Skill | Covers | Status | Coverage | Research |
|---|---|---|---|---|
| `project-bootstrap-and-audit` | Set up a new repository, retrofit or audit an existing one, re-check, release, prune: the standard, v0.37.0 | shipped | core | none |
| `keeping-current` | Sweep a repository for versions behind, end-of-life dates, deprecated APIs and stale facts; propose the updates | planned | core | R05, R21 |
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
| `supply-chain-security` | Dependencies, lockfiles, pinning, SBOMs, provenance, malicious and hallucinated packages | planned | core | R05, R21 |
| `ai-agent-security` | Prompt injection, permission design, secret exposure, MCP, skills as a supply chain, hidden Unicode | planned | core | R01 |
| `error-handling` | Failure classes, retries, timeouts, circuit breakers, user messages, RFC 9457 | planned | core | R07 |
| `testing` | Strategy, test doubles, fixtures, property-based and mutation testing, flaky tests | planned | core | R06 |
| `api-design` | REST, OpenAPI, GraphQL, gRPC, auth flows, pagination, versioning, webhooks | planned | core | R19 |
| `data-and-sql` | Schema design, migrations, SQL style, indexing, transactions | planned | core | R14 |
| `git-and-review` | Branching, commits, pull requests, code review | planned | core | R08 |
| `ci-cd` | Pipelines, Actions hardening, caching, environments, deployment | planned | core | R08, R21 |
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

## Rebuilding `project-bootstrap-and-audit`

The standard stops being one separate document. Its content becomes the skill's own parts, one
piece at a time. Each piece moves its sections out of the standard file in the same commit, and
is checked against the version before it by parity runs
([docs/testing-the-skill.md](docs/testing-the-skill.md)). The decision is in
[docs/decisions.md](docs/decisions.md).

What it becomes:

- **`SKILL.md`:** the procedure. That's the jobs, the phases, the two stops and the report.
- **`references/`:** one topic each:
  - standing rules, vocabularies, the environment, facts and the self-check;
  - the phases, and one file per dimension;
  - new projects and the starter files;
  - the configuration file map, file governance, the release gate and cross-repository
    contracts;
  - `other-tools.md`, which says how to use the skill with other AIs and lists each Claude
    Code-only feature with what it does.
- **`assets/`:** the starter files as tested templates, and the run report's skeleton and schema.
- **`scripts/`:** the mechanical checks, in Python with the standard library only.

Rules for the rebuild:
- Nothing is lost: each piece's pull request lists every rule it moved and where it went.
- A reference never links to another reference.
- No rule lives in two places.
- Frontmatter uses only the Agent Skills fields.
- A Claude Code-only feature is marked where it's used.

The baseline runs found nine things about the skill itself. The owner had them applied at once,
in standard v0.37.0, together with the set-up run's open amendments S2-S7 and S9-S11, so each
piece moves text that is already fixed. The piece named is where each one's section goes:

- **F1:** the read-only phases rewrite `.git/index`, so git reads should use
  `GIT_OPTIONAL_LOCKS=0` (piece 4).
- **F2:** in greenfield, Phase 2 says the run chooses the language while Phase 3 says the person
  picks. It should say "proposes" (piece 4).
- **F3:** the Phase 3 block has no field for a recommendation not yet picked (piece 1).
- **F4:** no rule says what the report holds when a run stops at Phase 3 (piece 1).
- **F5:** two runs rated dimension 5 differently, GAP and BLOCKER, for a check that can never
  fail. The dimension should say which it is (piece 3).
- **F6:** a session started outside the audited repository can't observe what loads, so the
  context-file check should record its verdict as inferred (piece 3).
- **F7:** a tracked `settings.local.json` should be rated for what it grants, not only for what
  it fails to enforce (piece 5).
- **F8:** a vendored context file that instructs agents needs a stated remedy, left to the
  person: drop the copy, or carry a recorded patch (piece 3).
- **F9:** the starter CI template's collection guard, which this repository's CI copies, fails
  without saying why when nothing is collected. Under GitHub's default `bash -e`, the `grep` in
  its command substitution exits first. It should name itself when it fails (piece 2).

The v0.37.0 parity runs found two more, left for the piece named:

- **F10:** for Active Directory on a Windows host, the defaults say PowerShell 7, while the
  first criterion, what the target already has, points at Windows PowerShell 5.1, which ships
  with Windows Server. The default should say which wins (piece 5).
- **F11:** the shapes table has no row for a PowerShell scheduled job (piece 5).

The owner asked for one more rule, researched before it's written:

- **Fewest dependencies, newest versions:** a repository the standard sets up or audits runs on
  as few dependencies as possible, each at its newest version, so there's less to keep current
  and less for CI and dependency tools to check. R21 tests the aim against the evidence, and
  asks where it needs a limit. Its checked result goes into the standard as a change of its
  own, in dimensions 2, 6 and 8 and in what a new project starts with, so the pieces move text
  that already carries it.

| Piece | What moves | Status |
|---|---|---|
| 0 | Parity checks: sample repositories, answer keys, the grader, and the current skill's results as the baseline | shipped |
| 1 | The procedure into `SKILL.md`, from How to Read This File, the routing table, What this is for, Scope, Assumptions, Limitations and the stop rules. Standing rules, vocabularies, environment and the conformance self-check into references, with `other-tools.md`. The report's skeleton and schema, and `check_report.py`. `skillcheck` checks the new structure. | planned |
| 2 | Starter File Contents into `assets/templates/`, each file tested, with `starter-files.md`. | planned |
| 3 | Phase 4: one file per dimension, and `phase-4-dimensions.md` for greenfield generation. | planned |
| 4 | Phases 0 to 3 and 5 to 9 into four phase files, with `preflight.py` and `inventory.py`. | planned |
| 5 | Choosing a Language and Runtime, Choosing the Shape and Project Shapes into `new-project.md`. The Configuration File Map, Standards Distribution, File Governance, the Release and Deploy Currency Gate, Cross-Repository Contracts, Any Agent, Any Tool and the facts into their references. | planned |
| 6 | Versioning, Proposing a Change, Sending Results Back, Validating a Change and Provenance retired. The standard file deleted. `AGENTS.md`, the authoring review, the README, the catalog and the research prompts updated. The skill's licence becomes Apache-2.0. Release 0.2.0 | planned |

## Repository

These aren't skills, so `skillcheck` doesn't match them against `skills/`. Each waits on its
trigger.

| Item | What it is | Status | Trigger |
|---|---|---|---|
| Weekly currency check | A scheduled workflow that flags stale facts, versions behind, and end of life within six months | planned | the first category skill ships |
| `copier` template | The standard's starter files, so a new repository is set up without a session | planned | the first repository set up from this one |
| Reusable workflows | This repository's CI gates, callable from other repositories | planned | a second repository wants this CI |
| `upstream-defects.md` | The standard's register of upstream defects shared across repositories | planned | the first upstream defect found |
| Fewest dependencies here | This repository's own dependencies and pins, in `pyproject.toml`, `package.json` and CI, held to the R21 rule | planned | the rule is in the standard |
