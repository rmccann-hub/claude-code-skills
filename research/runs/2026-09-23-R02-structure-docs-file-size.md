# Verification: R02 (2026-09-23)

Checked by the receiving session on 2026-09-23. Only the claims this intake relies on were
checked: those behind proposed changes to the standard, anything touching this repository's
files, and dates that need action. The rest is a lead until a skill uses it.

| Claim | Status | Checked against |
|---|---|---|
| Anthropic: "target under 200 lines per CLAUDE.md file" | verified | [Claude Code memory docs](https://code.claude.com/docs/en/memory) |
| The standard's "about 300 lines is the outer limit anyone recommends" is false | **contradicted**: 200 lines is inside 300. The report compares it with the 500-line figure for `SKILL.md`, which loads on demand, not with always-loaded context. The standard's line stands; what's new is a primary number it can cite | [Claude Code memory docs](https://code.claude.com/docs/en/memory); the standard's *Budgets* |
| No primary source gives the standard's 150, 30 or 50 line budgets | consistent with the standard, which already calls its budgets "unmeasured" heuristics | the standard's *Limitations* |
| `SKILL.md` body under 500 lines; references one level deep; reference files over 100 lines start with a table of contents | verified | [Agent Skills best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |
| `@imports` don't reduce context and nest up to four hops | verified | [Claude Code memory docs](https://code.claude.com/docs/en/memory) |
| Everything else in the report | not yet checked | checked when a skill that relies on it is built (`research/README.md`) |

---

RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R02 · FORM: research-result v1
Save as: R02-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.

# R02: Repository structure, documentation, Markdown, file size and splitting

The main finding is that the standard's always-loaded-context numbers are wrong. Anthropic's own current guidance is to keep each CLAUDE.md file under 200 lines and each SKILL.md body under 500 lines, so "about 300 lines is the outer limit anyone recommends" is false. The 150-line prune point and the 30-line shim and 50-line rule-file budgets have no primary source. Most linter default thresholds in "What we believe" check out; the corrections are in GitHub's community-health file locations, Material for MkDocs' support window, and those context-size numbers.

Research date: 23 September 2026 (the prompt says 22 September). Where a source gives no date of its own, the date shown is the date I read it (2026-09-23). This run ran out of search budget, so several standard-priority questions are only partly covered. They are listed in section 9.

## 1. Summary

- **CLAUDE.md size:** Anthropic says "target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence." Claude Code loads a CLAUDE.md of up to 4 MiB in full and does not cut it off. Only the auto-memory index MEMORY.md is truncated, after 200 lines or 25 KB.
- **SKILL.md size:** "Keep SKILL.md body under 500 lines for optimal performance." Reference files should be linked one level deep from SKILL.md. Reference files longer than 100 lines should start with a table of contents.
- **Why chains fail for agents:** Anthropic warns that Claude "might use commands like `head -100` to preview content rather than reading entire files" when it follows nested references. For agents, use one index with direct leaves (hub and spoke), not a chain.
- **Imports don't save context:** CLAUDE.md `@imports` can nest up to four hops, but imported files still load at launch. Path-scoped `.claude/rules/` files and skills are what actually cut always-loaded context.
- **GitHub file locations are narrower than we believed:** issue templates must sit in `.github/ISSUE_TEMPLATE`, discussion forms in `.github/DISCUSSION_TEMPLATE`, and FUNDING.yml in `.github`. Only the other supported files may be in the root, `.github/` or `docs/`. A LICENSE cannot be supplied as an organisation-wide default.
- **Contributor Covenant 3.0:** released 28 July 2025. Its text is licensed CC BY-SA 4.0.
- **MADR:** 4.0.0 (17 September 2024) is still the current release.
- **Material for MkDocs:** entered maintenance mode on 5 November 2025. 9.7.0 (11 November 2025) was the last feature release, with "critical bug fixes and security updates … for 12 months at least". That guaranteed window can end from November 2026, within 12 months. The latest release found is 9.7.7 (17 July 2026). Its successor Zensical is still pre-1.0 (0.0.64).
- **CommonMark:** the current spec is 0.31.2 (28 January 2024). There is still no 1.0.
- **GitHub alerts:** the five types NOTE, TIP, IMPORTANT, WARNING and CAUTION are confirmed. GitHub launched them in December 2023. They are a GitHub extension, and other renderers show them as plain blockquotes.
- **Linter defaults confirmed:** ESLint max-lines 300 and max-lines-per-function 50; Pylint max-module-lines 1000, max-statements 50, max-branches 12; RuboCop MethodLength 10 and ClassLength 100; golangci-lint funlen 60 lines and 40 statements; Checkstyle FileLength 2000; SwiftLint file_length warning 400 and error 1000.
- **Ruff C901 is off by default:** Ruff's default rule selection is E4, E7, E9 and F, so C901 must be selected explicitly. Its default is 10: Ruff's settings docs (as published on PyPI for ruff 0.0.159) say "The maximum McCabe complexity to allow before triggering C901 errors. Default value: 10". The clippy `too_many_lines` threshold of 100 (pedantic group) still has no primary source. The best secondary evidence is chesedo/cs-timespan-automated-v1#128, which reproduced it with a real clippy run ("trips clippy::pedantic's too_many_lines (threshold 100) — confirmed by running cargo clippy … -D clippy::pedantic").
- **Vale's repository moved:** it is now `vale-cli/vale` (v3.22.0, 17 September 2026). D2's repository now appears as `d2lang/d2`. Update any pinned URLs.
- **Mermaid 12.0.0 is out:** the GitHub release tag mermaid@12.0.0 dates from about 10 September 2026 (per the newreleases.io mirror). Its notes say: "This is a breaking release (ES2024, Safari 17.4+, Node 22.12+). Existing flowcharts, state and class diagrams will re-lay out and recolour; add layout: dagre, theme: default and look: classic to your config to keep the old look." Check Mermaid on GitHub and in any docs site before pinning it.
- **Go layout:** go.dev's "Organizing a Go module" is the only official Go layout guidance. The popular `golang-standards/project-layout` repository says it is "NOT an official standard defined by the core Go dev team".

## 2. Corrections

| # | What we believed | Verdict | Correct fact | Source |
|---|---|---|---|---|
| C1 | Community health files (README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, SUPPORT, FUNDING, CODEOWNERS, issue and PR templates) are recognised in the root, docs/ or .github/. | **Partly wrong** | "Issue templates and their configuration file must be in a folder called .github/ISSUE_TEMPLATE. A FUNDING.yml file must be in the .github folder. All other supported files may be in the root of the repository, the .github folder, or the docs folder." Discussion forms must be in `.github/DISCUSSION_TEMPLATE`. "You cannot create a default license file." GitHub's own list does not include CODEOWNERS or README among community health files. They follow separate rules (see Finding 2). | https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file |
| C2 | (the standard, 2026-09) For always-loaded context, prune past about 150 lines; about 300 lines is the outer limit anyone recommends. | **Wrong** | Anthropic's target for CLAUDE.md is "under 200 lines per CLAUDE.md file". For on-demand SKILL.md bodies it recommends "under 500 lines". So 300 is not an outer limit anyone recommends. No primary source was found for a 150-line prune point. | https://code.claude.com/docs/en/memory ; https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| C3 | (the standard, 2026-09) A tool shim should be about 30 lines, and a scoped rule file about 50. | **Not found (unsourced)** | Anthropic gives no line budgets for shims or rule files. It says only that each rules file "should cover one topic". Label these as house heuristics, not sourced facts. | https://code.claude.com/docs/en/memory |
| C4 | Material for MkDocs entered maintenance mode in late 2025. | **Confirmed, with an end-of-support flag added** | Maintenance mode was announced 5 November 2025, and 9.7.0 on 11 November 2025 was the last feature release. Fixes are guaranteed "for 12 months at least", so the guarantee can end as early as November 2026. | https://squidfunk.github.io/mkdocs-material/changelog/ |
| C5 | ruff C901 max-complexity 10. | **Needs a qualifier** | C901 is not in Ruff's default rule set; you must select it (`C90`/`C901`). The default is 10: Ruff's settings docs (as published on PyPI for ruff 0.0.159) say "The maximum McCabe complexity to allow before triggering C901 errors. Default value: 10". That is an old version, and the current docs.astral.sh settings page was not re-read. | https://github.com/PaloAltoNetworks/shifter/issues/1135 (secondary) ; https://docs.astral.sh/ruff/rules/complex-structure/ ; https://pypi.org/project/ruff/0.0.159/ |
| C6 | SwiftLint file_length warning at 400. | **Confirmed; add the error level** | The defaults are "warning: 400, error: 1000". | https://github.com/realm/SwiftLint/issues/543 |
| C7 | golangci-lint funlen 60 lines or 40 statements. | **Confirmed; add a nuance** | In golangci-lint v2, `ignore-comments` defaults to true. The standalone funlen tool's historical defaults were 50 lines and 35 statements, so don't confuse the two. | https://golangci-lint.run/docs/linters/configuration/ ; https://pkg.go.dev/github.com/golangci/funlen |
| C8 | Diataxis is the most widely cited documentation framework. | **Not verified** | No source measuring citation counts was found. Treat this as an opinion, not a fact. | — |

## 3. Facts table

| # | Fact | Value | Source URL | Exact quote | Date |
|---|---|---|---|---|---|
| F1 | CLAUDE.md size target | under 200 lines | https://code.claude.com/docs/en/memory | "target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence." | read 2026-09-23 |
| F2 | Auto-memory load limit | first 200 lines or 25 KB of MEMORY.md | https://code.claude.com/docs/en/memory | "Every session (first 200 lines or 25KB)" | read 2026-09-23 |
| F3 | CLAUDE.md is loaded in full | up to 4 MiB | https://code.claude.com/docs/en/memory | "Claude Code loads a CLAUDE.md file of up to 4 MiB in full and skips a larger file. Shorter files produce better adherence." | read 2026-09-23 |
| F4 | Import depth | 4 hops | https://code.claude.com/docs/en/memory | "Imported files can recursively import other files, with a maximum depth of four hops." | read 2026-09-23 |
| F5 | Imports do not save context | — | https://code.claude.com/docs/en/memory | "imported files still load and enter the context window at launch" | read 2026-09-23 |
| F6 | HTML comments in CLAUDE.md | removed before injection | https://code.claude.com/docs/en/memory | "Block-level HTML comments (`<!-- maintainer notes -->`) in CLAUDE.md files are stripped before the content is injected into Claude's context." | read 2026-09-23 |
| F7 | SKILL.md body length | under 500 lines | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | "Keep SKILL.md body under 500 lines for optimal performance" | read 2026-09-23 |
| F8 | Reference depth | one level | same | "Keep references one level deep from SKILL.md." | read 2026-09-23 |
| F9 | Table of contents threshold | over 100 lines | same | "For reference files longer than 100 lines, include a table of contents at the top." | read 2026-09-23 |
| F10 | Skill name and description limits | 64 and 1,024 characters | same | "Maximum 64 characters" / "Maximum 1,024 characters" | read 2026-09-23 |
| F11 | GitHub template locations | .github/ISSUE_TEMPLATE, .github/FUNDING.yml | https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file | "A FUNDING.yml file must be in the .github folder." | read 2026-09-23 |
| F12 | No default licence | — | same | "You cannot create a default license file." | read 2026-09-23 |
| F13 | Contributor Covenant 3.0 release | 28 July 2025 | https://ethicalsource.dev/blog/contributor-covenant-3/ | "CHICAGO, IL—July 28, 2025. … announced the release of Contributor Covenant 3.0" | 2025-07-28 |
| F14 | MADR current release | 4.0.0, 2024-09-17 | https://adr.github.io/madr/ | "2024-09-17: Release of MADR 4.0.0." | 2024-09-17 |
| F15 | CommonMark spec | 0.31.2, 2024-01-28 | https://spec.commonmark.org/ | "Latest version (0.31.2) (2024-01-28)" | 2024-01-28 |
| F16 | Material for MkDocs support | at least 12 months from November 2025 | https://squidfunk.github.io/mkdocs-material/changelog/ | "We will provide critical bug fixes and security updates for Material for MkDocs for 12 months at least." | 2025-11-11 |
| F17 | ESLint max-lines default | 300 | https://eslint.org/docs/latest/rules/max-lines | "\"max\" (default 300) enforces a maximum number of lines in a file." | read 2026-09-23 |
| F18 | ESLint max-lines-per-function default | 50 | https://eslint.org/docs/latest/rules/max-lines-per-function | "\"max\" (default 50) enforces a maximum number of lines in a function." | read 2026-09-23 |
| F19 | Pylint max-module-lines | 1000 | https://pylint.readthedocs.io/en/stable/user_guide/configuration/all-options.html | "Maximum number of lines in a module. Default: 1000" | Pylint 4.0.8 docs, read 2026-09-23 |
| F20 | Pylint design defaults | max-statements 50, max-branches 12 | https://pylint.pycqa.org/en/latest/user_guide/configuration/all-options.html | "max-branches = 12 … max-statements = 50" | read 2026-09-23 |
| F21 | golangci-lint funlen | 60 lines / 40 statements | https://golangci-lint.run/docs/linters/configuration/ | "# Default: 60 … # Default: 40" | read 2026-09-23 |
| F22 | RuboCop MethodLength / ClassLength | 10 / 100 | https://docs.rubocop.org/rubocop/latest/cops_metrics.html | "Max \| `10` \| Integer" / "Max \| `100` \| Integer" (via subagent) | RuboCop 1.91 docs, read 2026-09-23 |
| F23 | Checkstyle FileLength | 2000 | https://checkstyle.sourceforge.io/checks/sizes/filelength.html | "To configure the check to accept files with up to 2000 lines" | read 2026-09-23 |
| F24 | SonarJS cognitive complexity | 15 | https://github.com/SonarSource/eslint-plugin-sonarjs/blob/master/docs/rules/cognitive-complexity.md | "The maximum authorized complexity can be provided. Default is 15." | read 2026-09-23 |
| F25 | SwiftLint file_length | warning 400, error 1000 | https://github.com/realm/SwiftLint/issues/543 | "file_length \| no \| no \| yes \| warning: 400, error: 1000" | read 2026-09-23 |
| F26 | Go layout grows with need | internal/, cmd/ | https://go.dev/doc/modules/layout | "cmd/ prog1/ main.go prog2/ main.go" (layout example) | read 2026-09-23 |
| F27 | src layout needs installation | — | https://github.com/pypa/packaging.python.org/blob/main/source/discussions/src-layout-vs-flat-layout.rst | "The src layout requires installation of the project to be able to run its code, and the flat layout does not." | read 2026-09-23 |
| F28 | GitHub alerts launch | December 2023 | https://github.com/orgs/community/discussions/16925 | "Update - 14 December 2023" (general-availability update for the five types) | 2023-12-14 |

## 4. Findings

### 4.1 Repository layouts (Priority 1)

- **Python (PyPA):** the PyPA guide sets out both layouts neutrally. In the src layout, importable code moves into `src/<package>/`, while `tests/`, `docs/`, `tools/` and `pyproject.toml` stay at the root. The key difference: "The src layout requires installation of the project to be able to run its code, and the flat layout does not." The src layout also "helps enforce that an editable installation is only able to import files that were meant to be importable." PyPA does not mandate either layout. pyOpenSci (secondary) "strongly suggest[s], but do[es] not require" src and puts `docs/` and `tests/` next to `src/`. **Recommendation:** use the src layout for libraries.
- **Go:** go.dev's "Organizing a Go module" grows the layout in stages: a single package at the root, then supporting packages, then `internal/` for private code, then `cmd/<prog>/main.go` for each binary. Tests sit next to the code (`auth.go`, `auth_test.go`). `golang-standards/project-layout` itself says "This is NOT an official standard defined by the core Go dev team." Do not recommend `pkg/` as a standard.
- **Skills and plugins:** Anthropic's example skill has `SKILL.md` at the skill root, sibling reference files (`FORMS.md`, `reference.md`, `examples.md`) or a `reference/` folder, and a `scripts/` folder whose contents are "executed, not loaded". Claude Code project instructions go in `./CLAUDE.md` or `./.claude/CLAUDE.md`, and rules go in `.claude/rules/*.md` (found recursively, optionally scoped with `paths:` frontmatter).
- **Node/TypeScript workspaces, .NET, Rust/Cargo, Maven/Gradle, PowerShell modules, documentation sites:** not verified in this run (see section 9).

### 4.2 Professional repository files (Priority 2)

- GitHub's default community health files can live in a public `.github` repository, and GitHub "will use and display default files for any repository owned by the account … that does not have its own file of that type."
- **Placement rules:** issue templates and `config.yml` go in `.github/ISSUE_TEMPLATE`; discussion forms in `.github/DISCUSSION_TEMPLATE`; FUNDING.yml in `.github`; everything else in the root, `.github/` or `docs/`.
- **LICENSE has no default:** "License files must be added to individual repositories so the file will be included when a project is cloned, packaged, or downloaded."
- **Code of conduct:** Contributor Covenant 3.0 (28 July 2025) replaces "Project Maintainers" with "Community Moderators" and reframes enforcement around "Addressing and Repairing Harm". Its attribution text reads: "Contributor Covenant is stewarded by the Organization for Ethical Source and licensed under CC BY-SA 4.0." Django adopted it in April 2026, which shows real uptake.
- **Not verified in this run:** README, CODEOWNERS and SECURITY.md locations and precedence; the status of the standard-readme spec; RFC 9116 security.txt; CITATION.cff; .editorconfig; .gitattributes; CHANGELOG conventions.

### 4.3 File size, function size and complexity (Priority 3)

| Linter / rule | Default | On by default? | Verdict |
|---|---|---|---|
| ESLint `max-lines` | 300 | No: not in `eslint:recommended` (recommended-set status not re-read this run) | Confirmed (value) |
| ESLint `max-lines-per-function` | 50 | Same as above | Confirmed (value) |
| Pylint `too-many-lines` (C0302) / `max-module-lines` | 1000 | Yes | Confirmed |
| Pylint `too-many-statements` / `max-statements` | 50 | Yes | Confirmed |
| Pylint `too-many-branches` / `max-branches` | 12 | Yes | Confirmed |
| Ruff C901 `max-complexity` | 10 ("Default value: 10" in Ruff's settings docs for 0.0.159 on PyPI; current docs not re-read) | **No**: default select is E4, E7, E9, F | Qualified |
| SonarSource cognitive complexity (S3776) | 15 (confirmed for JS; other languages not checked) | Yes, in Sonar way | Partly confirmed |
| RuboCop `Metrics/MethodLength` / `ClassLength` | 10 / 100 | Yes | Confirmed |
| golangci-lint `funlen` | 60 lines / 40 statements | Not in the default linter set (not re-verified) | Confirmed (values) |
| clippy `too_many_lines` | 100 (secondary: reproduced by a clippy run in chesedo/cs-timespan-automated-v1#128; rust-clippy#16674 calls it an opt-in function-level lint) | No (pedantic) | Secondary sources only |
| Checkstyle `FileLength` | 2000 | Only if configured | Confirmed |
| SwiftLint `file_length` | warning 400, error 1000 | Yes | Confirmed |

- **What ESLint itself says:** "While there is not an objective maximum number of lines considered acceptable in a file, most people would agree it should not be in the thousands. Recommendations usually range from 100 to 500 lines." This is the most honest primary statement found: the thresholds are conventions, not evidence-based limits.
- **Clippy is adding a file-length lint:** a proposed restriction lint `too_many_lines_in_file` is in an open PR (rust-lang/rust-clippy#16675). The PR says "The threshold is configurable via `too-many-lines-in-file-threshold` in `clippy.toml` (default: 1000)", and the page notes "This lint has been nominated for inclusion. A FCP topic has been created on Zulip." It had not shipped as of the date I read it.
- **Research linking size to defects or review quality:** not found in this run. There is known literature, but I did not retrieve it (see section 9). Treat any claim like "files over N lines have more defects" as unsourced here.

### 4.4 Splitting documents for readers (Priority 4)

- **Human docs:** guidance from the Google developer documentation style guide, the Microsoft Writing Style Guide, Diataxis and Write the Docs on page length, one topic per page and tables of contents was not retrieved in this run.
- **Agent-facing docs (sourced):** Anthropic prescribes hub and spoke. SKILL.md "serves as an overview that points Claude to detailed materials as needed, like a table of contents", and all reference files "should link directly from SKILL.md". A chain (A → B → C) is marked as a bad example, because Claude may only partially read nested files.
- **Recommendation:** use an index plus leaves for anything an agent reads. Add "next/previous" links only for human tutorials, and never make a leaf depend on reading another leaf first.

### 4.5 Progressive disclosure for AI agents (Priority 5)

- **Three loading levels:** "At startup, only the metadata (name and description) from all Skills is pre-loaded. Claude reads SKILL.md only when the Skill becomes relevant, and reads additional files only as needed."
- **Size and structure rules:** the SKILL.md body stays under 500 lines, references are one level deep, and reference files longer than 100 lines get a table of contents so Claude "can see the full scope of available information even when previewing with partial reads."
- **What goes where:** CLAUDE.md is for "facts Claude should hold in every session". Multi-step procedures belong in a skill or a path-scoped rule. Rules without `paths` load at launch "with the same priority as `.claude/CLAUDE.md`".
- **Published evidence on how agents read long or chained files:** the only primary evidence found is Anthropic's own statement about `head -100` partial reads and "Longer files consume more context and reduce adherence." No independent benchmark was found.

### 4.6 Markdown (Standard 6)

- **CommonMark:** 0.31.2 (28 January 2024). CommonMark has still not published a 1.0 spec.
- **GitHub alerts:** the syntax is `> [!NOTE]` and so on, with five types. Unsupported types such as `[!INFO]` render as ordinary blockquotes.
- **Not verified in this run:** the GFM spec version, and whether footnotes and alerts are in the GFM spec itself or are only GitHub product features.
- **markdownlint-cli2:** 0.23.3, published about 22 September 2026 (a relative npm date). The version of the core `markdownlint` library was not found.
- **Vale:** v3.22.0 (17 September 2026); the repository is now `vale-cli/vale`.
- **lychee:** v0.24.2 is the newest release I saw, but I could not confirm it is the latest.
- **Relaxing rules for agent-oriented files:** MD033 (inline HTML) is the rule that XML-style prompt tags trip. That is standard markdownlint knowledge, but I did not re-read the rule page in this run.

### 4.7 Docs as code (Standard 7)

| Tool | Version | Date | Note |
|---|---|---|---|
| MkDocs | 1.6.1 | 2024-08-30 | Top entry in the release notes; no newer release in two years |
| Material for MkDocs | 9.7.7 | 2026-07-17 | Maintenance mode; guarantee runs to at least November 2026 |
| Zensical | 0.0.64 | not captured | Pre-1.0 successor from the Material team |
| Sphinx | 9.0.x series (exact latest not found) | — | |
| Docusaurus | 3.10.2 | 2026-07-10 | |
| Starlight | 0.41.11 | about 2026-09-23 | Still 0.x |
| mdBook | 0.5.4 | about June 2026 | |
| DocFX | 2.80.1 | 2026-09-18 | |

- **Choosing a tool:** for a new Markdown-first site, MkDocs plus Material now means taking on a stack whose core has had no release since August 2024 and whose theme is in maintenance mode. Choose Zensical only if you accept pre-1.0 churn. Otherwise use Starlight or Docusaurus for JS ecosystems, Sphinx for Python API docs, mdBook for Rust books, and DocFX for .NET.

### 4.8 Decision records (Standard 8)

- **MADR 4.0.0** (17 September 2024) ships four templates (full, minimal, bare, bare-minimal). It renamed "Deciders" to "decision-makers" and moved "Confirmation" under "Decision Outcome".
- **Where to store them:** MADR suggests `docs/decisions/` with files named `nnnn-title.md`. MADR "does not enforce any repository or directory organization structure".
- **Superseding:** in 4.0.0 the status field holds only an identifier ("Removed link to ADR in status field. Only identifier should be put.").
- **Nygard's format:** not re-verified in this run.

### 4.9 Diagrams as code (Standard 9)

- **Mermaid:** 12.0.0, confirmed by the GitHub release tag mermaid@12.0.0 in mermaid-js/mermaid (via the newreleases.io mirror, about 10 September 2026). It is a breaking release: ELK replaces dagre as the default layout, and existing diagrams "will re-lay out and recolour".
- **Structurizr:** 2026.09.19.
- **PlantUML:** v1.2026.8 (aggregator source only).
- **D2:** version not found.
- **Rendering on GitHub:** which of these GitHub renders natively was not verified in this run. The widely known fact that GitHub renders Mermaid code blocks should be re-checked against GitHub Docs before filing.

### 4.10 Comments versus documentation (Standard 10)

- Not covered in this run, apart from one related, sourced point. In CLAUDE.md, block-level HTML comments are removed before the content reaches the model, so they are a sanctioned place for notes to human maintainers that cost no tokens.

## 5. Tools

| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |
|---|---|---|---|---|---|---|
| markdownlint-cli2 | Markdown lint | 0.23.3 | about 2026-09-22 | `npx markdownlint-cli2 "**/*.md"` | `.markdownlint-cli2.jsonc` / `.markdownlint.json` (not re-verified) | https://www.npmjs.com/package/markdownlint-cli2 |
| Vale | Prose lint | 3.22.0 | 2026-09-17 | `vale .` | `.vale.ini` | https://github.com/vale-cli/vale/releases/tag/v3.22.0 |
| lychee | Link check | 0.24.2 (latest not confirmed) | not found | `lychee .` | `lychee.toml` | https://github.com/lycheeverse/lychee/releases/tag/lychee-v0.24.2 |
| ESLint | JS/TS lint (max-lines) | not captured | — | `npx eslint .` | `eslint.config.js` | https://eslint.org/docs/latest/rules/max-lines |
| Pylint | Python lint | 4.0.8 (docs) | not captured | `pylint src` | `pyproject.toml [tool.pylint]` | https://pylint.readthedocs.io/en/stable/user_guide/configuration/all-options.html |
| Ruff | Python lint | not captured | — | `ruff check --select C901` | `pyproject.toml [tool.ruff.lint]` | https://docs.astral.sh/ruff/rules/complex-structure/ |
| RuboCop | Ruby lint | 1.91 (docs) | not captured | `rubocop` | `.rubocop.yml` | https://docs.rubocop.org/rubocop/latest/cops_metrics.html |
| golangci-lint | Go lint (funlen) | not captured | — | `golangci-lint run` | `.golangci.yml` | https://golangci-lint.run/docs/linters/configuration/ |
| SwiftLint | Swift lint | 0.65.1 (docs) | not captured | `swiftlint` | `.swiftlint.yml` | https://realm.github.io/SwiftLint/file_length.html |
| Material for MkDocs | Docs theme | 9.7.7 | 2026-07-17 | `pip install mkdocs-material` | `mkdocs.yml` | https://pypi.org/project/mkdocs-material/ |
| Zensical | Docs SSG | 0.0.64 | not captured | `pip install zensical` | `zensical.toml` / reads `mkdocs.yml` | https://pypi.org/project/zensical/ |
| Docusaurus | Docs SSG | 3.10.2 | 2026-07-10 | `npx create-docusaurus@latest` | `docusaurus.config.js` | https://github.com/facebook/docusaurus/releases |
| DocFX | .NET docs | 2.80.1 | 2026-09-18 | `dotnet tool install -g docfx` | `docfx.json` | https://github.com/dotnet/docfx/releases/tag/v2.80.1 |
| Mermaid | Diagrams | 12.0.0 (GitHub release tag, via newreleases.io) | about 2026-09-10 | `npm i mermaid` | — | https://newreleases.io/project/github/mermaid-js/mermaid/release/mermaid@12.0.0 |

## 6. Changing in the next 12 months

- **Material for MkDocs (flag: end of support within 12 months).** The guaranteed critical and security fix window ("12 months at least" from 5–11 November 2025) can end from November 2026. Plan a move to Zensical or another tool.
- **MkDocs core:** no release since 1.6.1 (30 August 2024). Treat it as effectively unmaintained (secondary: fpgmaas.com, "MkDocs has not seen any real development for over 18 months").
- **Mermaid 12 (breaking):** per the 12.0.0 release notes, ELK replaces dagre as the default layout, redux-color/neo replace default/classic as the default theme and look, and the minimum targets are now ES2024, Safari 17.4+ and Node.js v22.12+ (PR #8213). To keep the old look, set `layout: dagre`, `theme: default` and `look: classic`. Test diagrams before upgrading.
- **clippy `too_many_lines_in_file`:** a proposed lint (PR #16675, default threshold 1000). It has been "nominated for inclusion" with an FCP topic on Zulip, but is not yet released.
- **Anthropic docs change often:** Claude Code's memory docs cite behaviour changes by version (for example v2.1.198, v2.1.207, v2.1.211, v2.1.217). Re-check the numbers above each quarter.

## 7. Common mistakes (including AI assistants')

- **Treating `@imports` as context savings.** The docs say imported files "still load and enter the context window at launch".
- **Chaining references** (SKILL.md → advanced.md → details.md). This produces partial `head -100` reads.
- **Leaving out a table of contents** in reference files over 100 lines.
- **Assuming Ruff enforces complexity by default.** C901 must be selected; setting `max-complexity` alone does nothing (secondary: PaloAltoNetworks/shifter#1135; astral-sh/ruff#4266).
- **Setting clippy thresholds without enabling the lint group.** A `too-many-lines-threshold` in `clippy.toml` is dead config unless `clippy::pedantic` or the lint itself is enabled (secondary: pmcfadin/cqlite#4042).
- **Putting issue templates or FUNDING.yml in `docs/` or the root.** They must sit under `.github/`.
- **Copying `golang-standards/project-layout` as "the standard".**
- **Writing alert types GitHub doesn't support** (`[!INFO]`, `[!DANGER]`) or expecting alerts to render outside GitHub.
- **Hard-coding time-sensitive statements in skills.** Anthropic advises an "old patterns" section instead.

## 8. Sources and licences

| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |
|---|---|---|---|---|---|
| GitHub Docs | CC BY 4.0 for docs text (per github/docs repo; not re-verified this run) | Yes | Yes | Yes (verify the code licence) | "GitHub Docs", with URL |
| Anthropic / Claude docs | Proprietary terms; no open licence found | Brief quotes only | Yes | Small snippets under fair use only | Cite URL |
| PyPA Packaging User Guide | Page text under PSF License v2; code examples additionally licensed (exact licence cut off in snippet) | Yes | Yes | Yes | Cite PyPA and URL |
| go.dev | Not verified this run | Brief | Yes | Not verified | Cite URL |
| CommonMark spec | CC BY-SA 4.0 | Yes | Yes | Share-alike applies to adapted spec text; keep it out of Apache-2.0 files or license the derivative CC BY-SA | "CommonMark Spec by John MacFarlane", CC BY-SA 4.0 |
| Contributor Covenant 3.0 | CC BY-SA 4.0 | Yes | Yes | Adopting it as CODE_OF_CONDUCT.md is intended; keep its attribution block | Keep the "adapted from the Contributor Covenant, version 3.0" block |
| ESLint docs | MIT | Yes | Yes | Yes | Copyright notice ("OpenJS Foundation and other contributors") |
| Pylint, RuboCop, golangci-lint, Checkstyle, SwiftLint, SonarJS docs | Not verified this run | Brief | Yes | Not verified | Cite URL |
| MADR | Not verified this run (repository licence not read) | Brief | Yes | Not verified | Cite adr.github.io/madr |
| Material for MkDocs changelog | Not verified this run | Brief | Yes | — | Cite URL |
| Secondary (pyOpenSci, fpgmaas.com, GitHub issues) | Varies | Brief | Yes | No | Label "secondary" |

## 9. Not found, contested, not covered

**Not found**
- A primary source for "prune past about 150 lines", "shim about 30 lines" or "scoped rule about 50 lines".
- A source ranking Diataxis as the most widely cited framework.
- The current version of the core markdownlint library.
- The D2 version.
- The exact latest Sphinx release.
- The lychee release date.
- Ruff's current docs statement of the `max-complexity` default. Only the old 0.0.159 settings docs on PyPI were found, and they say "Default value: 10".
- Primary confirmation of clippy `too_many_lines` (group and threshold).
- Research linking file or function size to defects or to review quality.

**Contested (resolved)**
- **Mermaid's latest version:** npm snippets showed both 12.0.0 (about 13 days before 23 September 2026) and 11.17.2 (about 15 days before). The GitHub release tag mermaid@12.0.0 (via newreleases.io) confirms 12.0.0 as the newer, breaking release. The 11.17.2 snippet was probably cached.

**Not covered (search budget exhausted)**
- **Q1 layouts:** Node/TypeScript workspaces, .NET, Cargo, Maven/Gradle, PowerShell, documentation sites.
- **Q2 files:** README sections and standard-readme status, CODEOWNERS and SECURITY locations, security.txt (RFC 9116), CITATION.cff, .editorconfig, .gitattributes, CHANGELOG.
- **Q4:** Google, Microsoft and Write the Docs guidance on page length and navigation.
- **Q6:** the GFM spec version, whether footnotes and alerts are in the GFM spec, and markdownlint rule and config-file names.
- **Q8:** Nygard's format.
- **Q9:** GitHub native rendering of Mermaid and other diagram formats.
- **Q10:** comments versus docs.
- **End-of-support dates:** for every tool except Material for MkDocs.