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

Each skill says why, not only what: its `references/why.md` gives each rule's reasons, what
other projects do and why, what each choice costs, and when to choose differently. Its dated
facts, including what other projects do, are checked again by `skillcheck --due` and
`skillcheck --verify`, which the weekly freshness workflow runs. `keeping-current` is the skill
that will do the same for other repositories.

## A. How the work is done

| Skill | Covers | Status | Coverage | Research |
|---|---|---|---|---|
| `project-bootstrap-and-audit` | Set up a new repository, retrofit or audit an existing one, re-check, release, prune: the standard, v0.40.0 | shipped | core | R21, R22 |
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
| `git-workflows` | Commits and trailers, branches, pull requests and review, the merge strategy, safe branch deletion, GitHub Actions CI and its hardening, hooks, `.gitignore`, annotated tags, changelogs, versions, release lines and backports | shipped | core | R08, R05 |
| `ci-cd` | Caching, environments and deployment, beyond the CI that `git-workflows` covers | planned | core | R08, R21 |
| `versioning-and-releases` | Release notes and support windows, beyond the tags, changelogs, versions and deprecation that `git-workflows` covers | planned | core | R05 |
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

The v0.37.0 parity runs found two more. The owner had them applied in standard v0.38.0, and
the piece named is where each one's section goes:

- **F10:** for Active Directory on a Windows host, the defaults say PowerShell 7, while the
  first criterion, what the target already has, points at Windows PowerShell 5.1, which ships
  with Windows Server. The default should say which wins (piece 5).
- **F11:** the shapes table has no row for a PowerShell scheduled job (piece 5).

Reading a live repository before its first run found two more, also applied in v0.38.0:

- **F12:** Phase 1 says a decision record is found by content, but its command matched
  filenames only, and its tier grep counted the words "blast radius" in prose as a recorded
  tier (piece 4).
- **F13:** a context file that tells agents to act without asking, commit as they go or write
  a session log before ending could read as lifting the run's waits (piece 1).

The v0.38.0 parity runs found five more, applied before it merged:

- **F14:** Phase 0 says nothing about a fetch that can't run, and its "read without writing"
  sits beside a command that writes refs (piece 4).
- **F15:** the routing table has no row for a repository that holds no source yet (piece 1).
- **F16:** the setup carve-out keeps a failing install out of `command_tally` even when the
  install is CI's first step, so the tally can read all `PASS` (piece 4).
- **F17:** the Phase 6 block has no field for a `class: standard` amendment (piece 1).
- **F21:** the rule that every workflow sets `permissions:` lived only in the starter
  template, which an audit doesn't read, and one final audit run missed the planted workflow
  that lacked it. Dimension 6 now states it (piece 3).

The final v0.38.0 greenfield run raised three more, each one run's evidence. They waited for the
next revision because an audit never reads them, and v0.39.0 applies them:

- **F18:** the "Choose a language" routing row assumes no repository exists, so choosing first
  in a repository that holds only a README fits neither that row nor the set-up one (piece 1).
- **F19:** the wiring rule reads configuration from environment variables, and a PowerShell
  scheduled job may take its settings better as the entry script's parameters in the task's
  definition (piece 5).
- **F20:** the scheduled-job layout keeps the task's definition as a reviewable diff, which an
  XML export in UTF-16 doesn't give without a `working-tree-encoding` rule or a registration
  script instead (piece 5).

The final audit and re-check runs raised four more, also applied in v0.39.0:

- **F22:** the command results don't name a command the session's permission layer refuses.
  Both runs that met one chose `UNVERIFIABLE-HERE`, which fits, but saying so settles it
  (piece 1).
- **F23:** the standard names no default path for a decision record when none exists, so two
  runs on a repository without one can propose different paths (piece 4).
- **F24:** dimension 3's `CODEOWNERS` rule doesn't say which status a missing file gets once
  its condition fires. Two re-check runs split between `GAP` and `UNVERIFIABLE-HERE` (piece 3).
- **F25:** the dated fact on SHA pins names dimension 8, but dimension 8 doesn't say whether an
  action pinned by tag is a finding, or at which tier. The final re-check rated one `GAP` and
  offered the pin as optional (piece 3).

Preparing the first live run found four more, also applied in v0.39.0:

- **F26:** Phase 3 asks its questions in the abstract, and the first live repository's owner
  couldn't answer them as asked. The repository's own records held nearly every answer except
  where it runs: its registry page for exposure, its updater and release workflow for
  production, its licence and manifest for the irreversible decisions. The wait could offer
  those as drafts with their evidence for the owner to confirm, and still ask where it runs
  (piece 1).
- **F27:** a cloud container lacked `libEGL.so.1`, so no test in a Qt suite could import, and
  the repository's CI installs that library with apt. The setup carve-out covers the project's
  declared dependencies but doesn't say whether what its CI workflow installs is declared: the
  system packages, and tools such as `pip-audit` that its jobs install. A run could rate the
  suite `UNVERIFIABLE-HERE` for the container's sake, and the dry run below counted those tools
  one way where a stricter run would count them the other (piece 4).
- **F28:** the time-box of about five minutes rates a longer suite `NOT-RUN-HERE`. That
  repository's suite ran about eight minutes in a cloud container, so the gate CI relies on
  most would never run. The run could start it in the background and rate it when it finishes
  (piece 4).
- **F29:** nothing compares the addresses in commit history with the owner's answer. A public
  personal repository whose commits carry an employer's address raises the question the
  provenance rule exists for, and the owner should see it at the gate (piece 3).

A dry run of that audit, stopped at the Phase 3 wait, found six more, also applied in
v0.39.0:

- **F30:** a run that stops at Phase 3 has nowhere to find its report's shape or its
  self-check. The header, `lifecycle`, `expires` and the three lists are defined only in
  Phase 6. `ten_statuses_emitted`, `tally_sums_to_ten` and `waits_observed` have no value for a
  stop at Phase 3, and the header's `tally` has no "not yet rated" (piece 1).
- **F31:** when a context file documents one command that runs every gate, and CI runs them
  as separate steps, nothing says which the run executes. Either choice fits the rules, so two
  runs can record different command lists (piece 4).
- **F32:** the hook check, `ls .git/hooks/pre-commit`, misses a hook activated through
  `core.hooksPath`, and fails in a worktree. `git rev-parse --git-path hooks` and
  `git config core.hooksPath` cover both (piece 4).
- **F33:** the dated fact on cloud sessions says release-asset requests reach only attached
  repositories. On 2026-09-26, in this repository's session, an unattached public
  repository's release asset downloaded with a 200, while its API returned 403. The fact needs
  checking again, and narrowing to what holds (piece 5).
- **F34:** a finding on the boundary between two repositories has no field for the side that
  owns it, so which side carries the fix can go only in the finding's text (piece 3).
- **F35:** smaller points in the schema and wording (pieces 1 and 4):
  - answers given in the prompt have no `answers_source` value;
  - copyright is worded three ways: the legal entity in Phase 0, the legal name if work-owned
    in Phase 3, and a handle allowed in its schema;
  - `settled` and `locked` aren't defined;
  - `clock_delta_days` taken from `--date=short` reads the commit's own time zone;
  - `reference_markdown_lines` isn't defined;
  - `decision_entries` counts dated entries, where a record can number them instead;
  - two counts in the prose are wrong: "Four of those matches…" and "The two optional
    blocks".

Checking R22 before it was filed found two more dated facts to check again. v0.39.0 checks
and rewrites both (piece 5, where the facts move):

- **F36:** the dated fact on synced plugins says Claude Code's docs have them load in cloud
  sessions. Read on 2026-09-28, the plugin docs say "Synced plugins load in Cowork sessions and
  in terminal sessions where you sign in with your claude.ai account", and name no cloud
  session, while the skills docs name cloud sessions for synced skills. R22 found the same on
  2026-09-27, and this session's folder for synced plugins held none on 2026-09-28. R22's
  deeper pass cites a French page that still named cloud sessions, but the French pages read
  on 2026-09-28 say what the English one does. What was seen on 2026-09-23 is now the
  documented behaviour, and the fact changes to say so.
- **F37:** the dated fact on `syncClaudeAiSkills` concludes that a repository can't keep synced
  skills out of its own sessions, and this repository's `CLAUDE.md` says the same. The settings
  docs, read on 2026-09-28, let any settings file, the committed one included, hide a skill
  with `skillOverrides` or block it with a `Skill(...)` deny rule. R22 found nothing on whether
  a `skillOverrides` key matches a synced skill, and its test 3 tries one. The changelog does
  document `Skill(anthropic-skills:…)` rules for synced skills: allow rules in 2.1.282, deny
  rules in 2.1.283. Neither has been tried on a synced skill. Plugins now have a key of their
  own, `syncClaudeAiPlugins`, which the fact should name too. The first live audit found 49
  account skills loading into the audited repository's sessions, two of them asking to be read
  first, and rated that a dimension 4 secondary.

Taking in R22's result found one more, applied in v0.39.0:

- **F38:** a re-check shows the recorded answers with "nothing has changed" as the stated
  default. R22's checked sources find that a large share of people confirm a wrong preloaded
  answer (its row 61), that a default pulls hardest when it reads as a recommendation
  (row 60), and that asking "Is that still the case?" of each answer gave the most accurate
  reports of change (row 62). The standard already asks where it runs afresh every time.
  Production and dependents may need the same (piece 1).

v0.38.0 also carries four changes the owner asked for before the first live run. Context
files are measured in bytes as well as lines. Evidence files are read in parts. The starter CI
pins its action to a commit SHA. An upload that renames the file isn't a version mismatch.
Its history entry lists them.

Live runs on the owner's repositories come between pieces. Each report is triaged as
[docs/testing-the-skill.md](docs/testing-the-skill.md) describes, and what it finds is fixed
before the next repository's run.

The first live audit ran on 2026-09-28, on v0.38.0 from the owner's run file, in a cloud
session. It stopped at both waits and wrote nothing before approval. It confirmed F27, F30,
F32, F34 and F35 on a real repository: the side that owns a boundary finding went into `notes`.
F26's drafted answers worked: the owner confirmed the tier in one word. Its report up to the
Phase 6 gate found five more. The apply half came back the same day: eleven approved changes
on one pull request, eight held as asked, and nothing held was touched. It found seven more,
after F43, and adds to F40 and F42. v0.39.0 applies all twelve.

- **F39:** a fetch moves `origin/<default>` but not the clone's local branch of the same name,
  so a history scan that names `main` reads the history as old as the clone. The run caught it
  only because a version reconciliation disagreed with the tag. After the fetch, read the
  default branch through its remote-tracking ref (piece 4).
- **F40:** no dated fact covers a secret-scan job's range. For a push, gitleaks-action scans
  `--no-merges --first-parent <first>^..<head>`, so on a merge-commit workflow a push run scans
  no commits and passes. A pull-request run skips merge commits and second-parent history. The
  run rated it `BLOCKER`, as a check reporting success while measuring nothing. A secret-scan
  job is read by its range and its scanned count, never by its conclusion (piece 5). The run's
  own full-history scan missed merge commits' changes too: gitleaks' default log options skip
  them, and only `--log-opts="-m <ref>"` or `"--all -m"` reads them. The fact says so.
- **F41:** a status command whose non-zero exit is its report can only be rated `FAIL` under
  the closed vocabulary. One example is a command that exits 1 while a handshake round is open.
  The tally then counts a failure that isn't one (piece 1).
- **F42:** "write nothing to the repository" doesn't say whether the ignored artifacts that the
  gates leave in the working tree count: caches, an egg-info directory, coverage data. The run
  counted them as no write and listed them, and one of them changed a test's collected count.
  In the apply half, a wheel built while replaying CI in the working tree left `build/lib/`
  behind, and a test that CI failed passed locally because of it. A job that builds or installs
  is replayed in a scratch clone (piece 4).
- **F43:** the Phase 6 schema has no field for an amendment the owner approves but holds. The
  run added a `held` key and declared it under `fields_added_beyond_schema` (piece 1).

The apply half found these:

- **F44:** Phase 7 doesn't say to fetch the default branch before pushing. It had moved five
  commits during the run, so the pull request conflicted with its base, and a conflicting pull
  request gets no workflow run at all: zero check runs, not pending ones. If the base moved,
  bring it in by the repository's convention and run the gate again. After pushing, read the
  pull request's mergeability before reading its checks (piece 4).
- **F45:** "commit by concern" doesn't say to run the full gate before each push. Targeted runs
  of the tests naming the edited files missed the repository's own sweeps over the tree, so two
  of eleven commits were red on their own until they were rebuilt (piece 4).
- **F46:** the fresh-clone check doesn't say to clone from the remote. A clone of the working
  copy took its stale branches as its remote-tracking refs, which is F39's trap by another
  route, and part of the gate run there isn't the gate (piece 4).
- **F47:** a human action has no state for "reported done, not observed". The owner reported a
  setting done while the API still read it as off. Each action records what was seen beside
  what was said: done and observed, reported but not observed, or not observable here
  (piece 4).
- **F48:** when the base moves between Phase 2 and the push, Phase 8's re-checks run again on
  the merged tree, and the record names both base commits (piece 4).
- **F49:** an approved check that runs an optional tool whenever the tool is present can refuse
  good input when the tool is too old. The installer change ran `gh attestation verify`
  whenever `gh` was on the path. The command arrived in gh 2.47.0, and its `--signer-workflow`
  flag, which the check passes, in 2.51.0. Debian 13 packages 2.46.0 (sources.debian.org, read
  2026-09-28; gh's source, read 2026-09-29). A check that uses an optional tool probes for the
  capability, every flag it passes included, not the tool (piece 3).
- **F50:** a report committed to a public repository at the owner's request got no privacy
  pass. Its survey of the owner's other repositories named three private ones. A report
  written for the owner can hold what a public tree mustn't, so committing it needs the check
  any public write gets (piece 4).

Reading the owner's public repositories on 2026-09-29, before the next audit, found two more,
also applied in v0.39.0:

- **F51:** a fork can keep its default branch as a clean mirror of upstream and land its work
  on a branch named for its purpose. The one read here had a default untouched for five weeks
  and a working branch more than a thousand commits ahead, holding the only context file. Every
  rule that reads "the default branch" would audit the mirror, and a session started there
  reads no instructions. The run records `working_branch` and reads it instead (piece 4).
- **F52:** a long-lived session can run a Claude Code release far behind the current one: two
  started in July still ran 2.1.233, while new ones ran 2.1.284. Several dated facts hold only
  from a given version, so the run records its agent's version (piece 4).

The v0.39.0 parity runs found seven more, applied before it merged:

- **F53:** the routing row for choosing a language and a shape sent the run to neither *Project
  Shapes and Layout*, where Phase 2 finds the shapes, nor Phase 6, which gives a Phase 3 stop's
  report its shape (piece 1).
- **F54:** the `job` vocabulary had no value for choosing, so the greenfield run recorded
  "set up" (piece 1).
- **F55:** Phase 1's tier grep named the record found, and had no target when none was
  (piece 4).
- **F56:** GitHub honours `CODEOWNERS` on a private repository only on a paid plan, so a missing
  file there is `N/A` on a free one, as the re-check run proposed (piece 3).
- **F57:** Claude Code's native `AGENTS.md` reading reaches third-party providers and
  telemetry-off sessions from v2.1.281. The fact still said it didn't (piece 5).
- **F58:** a `Read` deny rule now covers the file commands Claude Code recognises in Bash, such
  as `cat`, so the example that it leaves `cat .env` open was out of date (piece 3).
- **F59:** an unattended run can't stop at Phase 3. Both runs that went on to Phase 6 recorded
  that as a deviation, so the standard now says how the answers given in advance meet the wait
  (piece 1).

The first live repository's re-check ran on 2026-09-29, on v0.39.0 from the owner's run file,
in a fresh cloud session. It stopped at both waits, found the last audit's eleven fixes in place
and its eight held amendments still held, and re-raised none of them. Its drafted re-check
questions, the version it recorded and its per-commit secret-scan reading all worked as written.
It found five more, applied in v0.40.0:

- **F60:** the rule to replay a gate in a scratch clone doesn't say to clone from the remote.
  The run cloned its working copy, whose local `main` the fetch had left four days behind, so
  the scratch clone read that as `origin/main` and failed ten tests that pass. Phase 7's
  fresh-clone check already says to clone from the remote; Phase 2's needs the same, and a check
  that the clone's `origin/<default>` matches the fetch (piece 4).
- **F61:** a cloud session's clone can be shallow, 511 commits here, while CI checks out full
  history. Nothing says to deepen it before gates and history counts run, so the run did it as
  an override. A count read from a shallow history should say so beside it (piece 4).
- **F62:** a result caused by the run's own mistake stayed in `command_tally` as a `FAIL`, with
  the correction beside it. It belongs in `corrections`, and the tally counts the re-run
  (piece 1).
- **F63:** the address-domain command prints an author line and a committer line per commit, so
  it counts addresses, not the commits dimension 10 asks for. A per-commit count needs each
  commit's domains deduplicated (piece 3).
- **F64:** nine overrides were recorded, and most were steps the standard directs: installing
  what CI installs, running gates in a scratch clone, deepening a shallow clone. Counted as
  deviations, they hide the few that are departures (piece 1).

Its apply half ran the same day. It applied the four amendments approved without a hold, in one
pull request whose CI passed when read at log level, and found two more, also applied in
v0.40.0:

- **F65:** settings the session can't read were rated `UNVERIFIABLE-HERE`, and the last record
  had them done. The owner's screenshot, sent with the gate answers, showed three of them off,
  so two secondary ratings changed after the gate. Where nothing can be read, the first wait
  should ask the owner for a screenshot or a reading, so the findings rest on it (piece 1).
- **F66:** Phase 7's block has no `overrides` field, so the run put its two Phase 7 overrides
  in its notes. Phase 4's field takes a `phase` key, but Phase 4's block is emitted before
  Phase 7 runs (piece 1).

After the gate, the owner asked the session to review and merge that pull request, and to check
the branches before calling any safe to delete. That work found three more, also applied in
v0.40.0:

- **F67:** a reviewer that hadn't written the change read the diff cold and found three defects.
  The run's tests, its revert probe, CI and a first review had all passed them: a test message
  that pytest cut short, a strict decode that crashed the gate script on output that wasn't
  UTF-8, and a false claim in the decision record. The self-check is said to catch failures
  "without a second reader". A second reader should go over the whole branch before the run
  hands over, after the decision record is written (piece 1).
- **F68:** no block holds work the owner asks for after Phase 9, such as a review, a merge or a
  branch check, so the run added its own. When the owner asks the run to merge, the block
  should record the head it merged and the default branch's CI read afterwards (piece 1).
- **F69:** nothing says what to check before advising that a branch be deleted. Asked to check
  first, the run found a sibling repository's record naming one branch as staying, because
  citations had broken once when it was deleted. Before a deletion is advised, the branch
  should have no open pull request and its work should be on the default branch. Every commit
  cited through it, in the repository or a sibling, should be reachable from the default
  branch, and a sibling promised the branch should be told (piece 4).

On 2026-09-30 the owner raised one more, applied in v0.40.0: they had to ask a working
session on another of their repositories what it was waiting on before its next release.

- **F70:** a session that stops with work outstanding should say what it's waiting on, and from
  whom, without being asked. Run reports already list what remains for the human, but the
  starter context file gives the working sessions it sets up no such rule (piece 2).

On 2026-09-30 the owner named FFmpeg as a model of open-source practice. Its tree and history,
read that day, are in `research/runs/2026-09-30-ffmpeg-reference.md`. Reading it raised nine
more, which the owner approved the same day and v0.40.0 applies:

- **F71:** the run looks for CI only in `.github/workflows/`. FFmpeg's is in
  `.forgejo/workflows/`, and its GitHub repository is a mirror whose pull requests are ignored,
  so a run would report no CI. Before reading CI and settings, the run should find the forge
  the contributing guide names as canonical, and read that one (piece 4).
- **F72:** `SECURITY.md` is due at T3, and FFmpeg has none: its private list and page are
  named in `MAINTAINERS`. A security contact named in a file a reader looks in, such as the
  README, the contributing guide or a maintainers list, should count (piece 3).
- **F73:** the standard names Conventional Commits as the commit grammar. FFmpeg's hook rejects
  it and requires "area: summary", which 2,970 of its last 3,004 subjects follow. A repository
  should state one grammar and check it with a commit-msg hook, and either family should count
  (piece 3).
- **F74:** nothing says which merge strategy to use. FFmpeg's master rejects merge commits; the
  first live repository keeps them, because its sibling cites branch commits: its record says
  the cited commits became unreachable when a branch went four minutes after a squash merge.
  The context file should name the strategy and why, the platform should allow only that one,
  and where commits are cited from outside only a merge commit keeps them (piece 3).
- **F75:** nothing says a release tag is annotated. FFmpeg's are, and `git describe` builds
  its version from them. The first live repository's 62 are all lightweight, made by
  `gh release create`, so they carry no tagger or date, and `git describe` passes over them
  without `--tags` (piece 5).
- **F76:** nothing covers an interface others build on. FFmpeg keeps each library's API
  compatible within a major version, logs every change in `doc/APIchanges`, and deprecates
  before it removes, on a schedule. A repository whose API, command-line options or config
  keys others depend on should log changes to them, and deprecate in one release before
  removing in a later one (piece 3).
- **F77:** nothing covers keeping more than one release line. FFmpeg's point releases come from
  `release/X.Y` branches, take only a security fix, a documented bug or documentation, and keep
  compatibility; 78 of its last 80 backports name their source commit. Where a repository keeps
  a second line, it should follow the same rules (piece 5).
- **F78:** nothing asks for damaged-input tests. FFmpeg's checklist has every decoder and
  demuxer fed damaged data, and it must not crash, loop or allocate without bound. Code that
  parses input it doesn't control should have such a test (piece 3).
- **F79:** nothing covers mixed licences. FFmpeg's `LICENSE.md` lists which files are GPL, and
  the GPL parts stay off unless `--enable-gpl` is passed. Where licences mix, each file should
  name its own, and the licence file should say which parts are which (piece 3).

Approving them, the owner asked for the practices of more than one maintainer as well, asked
rather than inferred, also applied in v0.40.0:

- **F80:** `CODEOWNERS` was due from a second committer, read from the history's authors, and
  nothing else checked a team's practices. Whether anyone else maintains, reviews or commits is
  now the fourth thing a run can't detect, asked at the Phase 3 wait and drafted from the
  authors. Once the human says so, dimension 6 checks who reviews what, review before merging,
  the contributing guide's review rules, sign-off for outside contributions, and a security
  contact that isn't one inbox (pieces 3 and 4).

On 2026-09-30 the owner asked what the two live repositories had found through their own
iteration, to leverage it. Their context files, decision logs, tools and the tests that guard
their process were read that day, and each lesson was checked against the standard. Twenty-two
are missing, awaiting the owner's approval:

- **F81:** a test run that stops early can exit 0: a live repository merged a pull request
  whose suite had run 76% of its tests. The suite should write a marker as its last act, and
  CI should fail without it (piece 3).
- **F82:** a check that sweeps a computed list passes when the list is empty, as a
  parametrised test over nothing reports one skip; an audit there found 52 such gates beside
  54 that worked. A sweep should assert a floor on what it examined, and that its data isn't
  trivially empty. It should take its population from the tree, and keep an allowlist whose
  every entry carries a reason, is checked for staleness and can only go. A scheduled audit
  should be able to report that it measured nothing (piece 3).
- **F83:** a revert proves a test only when it landed and built. A revert broken by a stray edit
  didn't build and still read as proof, and a restore with `git checkout --` destroyed
  uncommitted work. A revert probe should confirm the file changed and the build succeeded,
  and restore from a copy checked by hash (piece 3).
- **F84:** a stand-in more permissive than what it stands for hides the bug. A fixture stopped a
  thread production never stopped, hiding a crash for five releases, and another passed only
  on a record that couldn't occur. Fixtures, harnesses and test environments should be no more
  permissive than production, able to occur, and able to tell the cases under test apart
  (piece 3).
- **F85:** "couldn't check" read as "passed": a guard whose listing command failed found no
  offenders, a probe graded crashes as clean refusals, and a gate closed a round because files
  existed. A check should have three outcomes, fail closed on the third, read declared
  fields, count its matches, and be tested for each way it could wrongly say yes (piece 3).
- **F86:** a check that only warns gates nothing: the rule cited most there, a regression test
  for every bug, had no `exit 1`. An opt-out should carry a written reason, and a bare marker
  should be refused (piece 3).
- **F87:** an intermittent failure met with a wider timeout stays: a test timed out fourteen
  times in full suites and took a second alone. One network call took 80 of a check's 137
  seconds. A flaky test should get instrumentation and kept artifacts, and gates should run
  against recorded responses rather than the network (piece 3).
- **F88:** a mutation score can measure the edit rather than the defect: a first sweep scored
  100% because one test hashed the source tree. A sweep should first run an inert edit, and
  tools that write into the tree should share one lock that fails closed (piece 3).
- **F89:** a gating tool was pinned in one file and installed from another, looser range, and a
  stale global binary produced 118 phantom errors. Workflows should take the gating tools'
  pins from the project's own file, and a run should record which binary and version ran
  (piece 3).
- **F90:** CI missed what it should cover. A job with no timeout runs to the platform's
  360-minute default; CI fired only on a mirror branch nobody worked on; an advertised build
  configuration failed the first time it was compiled; and a depth-1 checkout turned
  history-reading tests red. Every job should set a timeout, CI should run on the branch where
  work lands and build each configuration users are told to build, and a test that reads
  history should fail rather than skip without it (piece 3).
- **F91:** events a workflow makes with its default token start no other workflow, so four
  releases never reached the package index. A release that must start another workflow should
  hand off through `workflow_dispatch` (piece 5).
- **F92:** a truncated merge output hid a conflict, and its markers shipped through nine green
  jobs. Output that lists work to do should be read whole, and a sweep should refuse conflict
  markers at the start of a line (piece 3).
- **F93:** cloud sessions don't run a repository's setup script, so a pre-commit guard was off
  in every web session. What a session needs, such as `core.hooksPath`, should come from a
  committed SessionStart hook (piece 3).
- **F94:** a rule nothing runs does nothing: of 187 rules audited there, 29% were gated, and a
  third would fail no test if broken. Each rule in the context file should name what fails
  when it's broken, or say it's advice, and a handover should be refused until the tree is
  pushed and every hash and URL it quotes resolves (piece 3).
- **F95:** sessions kept re-deriving settled facts, three of them four times in one session.
  Where that happens, the facts should be indexed, each with the command that re-checks it,
  and a tool should run the index (piece 3).
- **F96:** agents' shell habits cost hours. Waiting on `pgrep -f` matched its own shell and
  looped for 78 minutes, two suites in one build directory left a log that read as both pass
  and fail, and a seven-lane fan-out lost 16 of 17 agents to usage limits. A run should wait
  on a PID, run one suite per build directory, treat a subagent's finding as a lead to verify,
  and read a fan-out's failures before its results (piece 1).
- **F97:** a fact kept by hand in two places drifts: a sibling's sentence said "eight" while its
  table held nine rows. A fact stated twice should be generated from one source, as the first
  live repository generates its half of a shared contract, or a test should check the copies
  agree in both directions (piece 3).
- **F98:** a release was announced before it was proven: it failed 2 of 33 tests from a fresh
  clone. Separately, a green suite with ten green checks still had three blocking defects that
  an adversarial review found. A release should be proven from what users install, and at T3
  a review told to refute it should read the release's diff (piece 5).
- **F99:** cited commits were stranded three ways: a squash merge, the branch deleted after it,
  and an amend of regenerated files. A test should fail when a cited commit isn't reachable, a
  cited commit should never be amended, and regenerated files should go in their own commit
  (piece 3).
- **F100:** a sibling read a relayed message and concluded the other side's lap was unsent,
  while it sat released on that side's `main`, one fetch and one grep away. A claim about
  another repository should cite `repo@sha:path:line` from its committed files, shared files
  should be checked byte for byte at a named commit, and a bug shape the peer reports should
  be looked for at home (piece 5).
- **F101:** a review loop between repositories ran to lap 39 by one side's recount, 37 by the
  other's, and produced no release. Close conditions
  should be fixed at the start, a new finding should go to the next round unless it breaks what
  is under review, each agreed change should be tracked to the commit that lands it, and a
  consumer's parser should be read, and taught both forms, before output it parses changes
  (piece 5).
- **F102:** a live repository's owner told its sessions to stop adding Markdown files for their
  own sake. A commit that adds a document should name the existing homes it considered and
  rejected, as that repository's rule now says (piece 5).

Building `git-workflows`, its cold review and the owner's question about slow CI found five more
on 2026-09-30, each checked against its source that day. They await the owner's approval:

- **F103:** dimension 2's lockfile table offers `uv sync --frozen` as well as `--locked`, but
  `--frozen` installs from the lockfile without checking it, so drift passes. It should name
  `--locked` only (uv's CLI reference).
- **F104:** the facts table and dimension 7 say push protection is on by default for public
  repositories. GitHub's docs split it in two. Push protection for users is on by default, and
  stops a user's own pushes of secrets to public repositories. Push protection for the
  repository has to be turned on, and only it raises alerts when someone bypasses it.
- **F105:** the starter CI file has the collection guard only, which counts the tests
  collected, not those that ran. It should add the completion guard this repository's CI and
  `git-workflows`' `tests.yml` use: the test report must exist, and count at least the
  baseline.
- **F106:** dimension 10 says that under squash merging the pull request's title becomes the
  subject, so the grammar check reads the title. GitHub's default squash message takes a
  one-commit pull request's own commit message instead. The rule should also set the
  repository's default squash title to the pull request's title, and audit that setting.
- **F107:** the starter CI runs on `push` and `pull_request`, so each pull request's commits run
  twice, once as the branch and once merged with its base. That costs little in a fast suite
  and doubles a slow one. The starter should say so, and offer `push` on the default branch
  with `pull_request` where CI is slow.

The owner asked for one more rule, researched before it's written:

- **Fewest dependencies, newest versions:** a repository the standard sets up or audits runs on
  as few dependencies as possible, each at its newest version, so there's less to keep current
  and less for CI and dependency tools to check. R21 tests the aim against the evidence, and
  asks where it needs a limit. Its checked result goes into the standard as a change of its
  own, in dimensions 2, 6 and 8 and in what a new project starts with, so the pieces move text
  that already carries it.

The owner also asked for one command that starts the standard from any repository, researched
before it's built:

- **The front door:** a short command, typed in a repository's session, starts a run. In an
  existing repository it reads the repository first, drafts the Phase 3 answers with where it
  found each, and asks only what no repository shows. In a new or nearly empty one it
  interviews the owner and recommends a language, runtime and shape. Every run still stops
  for approval before it writes anything. The skill reaches cloud sessions by upload to the
  owner's claude.ai account, with the pinned link as a fallback. R22's result came in two
  passes, both filed and checked:
  [the first](research/runs/2026-09-27-R22-one-command-front-door.md) and
  [a deeper one](research/runs/2026-09-27-R22-deeper-pass.md). It goes into piece 1, with F18,
  F26, F30 and F38. Both halves of the first live audit's report are triaged, as above.
  What it adds to the plan:
  - **Which copy ran:** the reference file's SHA-256 in `SKILL.md`'s metadata, checked by a
    standard-library script from a `` !`command` `` line, which a cloud session runs for a
    synced skill. The script needs tests of its own, since ruff and coverage don't reach
    `skills/`, and `skillcheck` should compare the hash with the file, so that no release
    ships a mismatch that stops every run. The deeper pass keeps the uploaded skill thin
    instead: it fetches the reference at a pinned commit with `curl` and hashes that, so the
    pin decides the version, at the cost of a fetch on every run. A hash shows that a copy is
    whole, not that it's current, so the run also compares its version with `main`'s. The
    first pass has it ask whether to go on when `main` is newer, a stop the standard's two
    waits don't include; the deeper pass warns without stopping.
  - **The questions:** a draft of each answer the repository shows, with its evidence and one
    word of confidence. The first pass asks three outright every run: where it runs,
    production and dependents. The deeper pass asks five, adding work or personal and how long
    it must live, with no answer pre-selected. Every question offers "Not sure", an option is
    marked recommended only beside its evidence, and a re-check asks "Is that still the
    case?" (F38). `AskUserQuestion` takes at most four questions a call, and how it shows in
    the mobile app isn't documented, so the questions also need a numbered list answered in
    one reply. The studies behind these are checked, except the first pass's row 58.
  - **Where the answers are kept:** R22 proposes a dated block in the decision record, with no
    addresses, hostnames or names. The run report's Phase 3 block already defines those
    answers' fields, and one schema is easier to keep than two.
  - **When it loads:** a description narrowed to runs that name it, since an uploaded skill
    can't carry `disable-model-invocation`. That needs the trigger evaluations the authoring
    review asks for. The Help Center gives an uploaded skill's description 200 characters at
    most, where the specification allows 1,024. This skill's is 446.
  - **Enforcing the waits:** a committed project skill can carry `disable-model-invocation`
    and hooks, and a PreToolUse hook that exits with code 2 blocks the call. The deeper pass
    has Phase 8 offer each repository such a skill after its first approved run, with a hook
    that blocks writes until approval. That puts a skill and a hook into other repositories,
    so it needs a review of its own.
  - **A new project's recommendation:** at least two languages compared, each dependency
    checked against its registry, and each version against current release notes. Code models
    favour Python, name packages that don't exist (at least 5.2% of those from commercial
    models) and use deprecated APIs: the first pass's rows 64 and 66, and the deeper pass's
    F35. This joins R21's rule in piece 5.
  - **The plugin's version:** the catalog pins 0.1.1, and Claude Code updates an installed copy
    only when that string changes, so a copy installed before v0.37.0 still has v0.36.0. How
    claude.ai decides that a personal marketplace's copy changed isn't documented. By the Help
    Center, an organisation's GitHub-synced marketplace syncs when a merged pull request
    changes the version. Releasing at each standard change, or leaving the version out so
    that installs follow `main`, is the owner's choice.
  - **Tests in the owner's browser** settle what's left. Three are in the first pass's section
    10: what refreshes claude.ai's copy, with Check for updates tried before any version
    change; what a same-name upload does; and whether `skillOverrides` reaches a synced skill
    (F37). A fourth comes with the first upload: whether a description over 200 characters
    is accepted.

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
