# Verification: R03 (2026-09-23)

Checked by the receiving session on 2026-09-23. Only the claims this intake relies on were
checked: those behind proposed changes to the standard, anything touching this repository's
files, and dates that need action. The rest is a lead until a skill uses it.

| Claim | Status | Checked against |
|---|---|---|
| ESLint v9 reached end of life on 2026-08-06 | verified | [ESLint v10.0.0 release post](https://eslint.org/blog/2026/02/eslint-v10.0.0-released/) |
| TypeScript 7.0 was announced on 8 July 2026 and ships without a stable API | verified | [Announcing TypeScript 7.0](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/): "TypeScript 7.0 is here, it does not ship with an API" |
| Ruff 0.16 enables 413 rules by default | not checked; it doesn't affect this repository, which selects its rules explicitly and scopes Ruff to `src/` and `tests/` | `pyproject.toml`; CI passes on Ruff 0.16.8 |
| .NET 8 and .NET 9 reach end of support on 10 November 2026 | verified | [.NET Blog](https://devblogs.microsoft.com/dotnet/dotnet-8-9-end-of-support/) |
| Python 3.10 reaches end of life in October 2026 | verified | [Python devguide, versions](https://devguide.python.org/versions/): "3.10 … security … 2026-10" |
| Everything else in the report | not yet checked | checked when a skill that relies on it is built (`research/README.md`) |

---

RESULT-FOR: rmccann-hub/claude-code-skills · RUN: R03 · FORM: research-result v1
Save as: R03-RESULT.md
Receiving session: this is research the repository owner asked for. Check each claim against the source it cites before relying on it. File the report under research/runs/, update the facts files of the categories it names, and list what changed. If you lack context, the owner will attach HANDOFF.md.

# R03 — Code style, naming, comments and docstrings, formatting, and types (checked 23 September 2026)

Most of the "What we believe" list still holds, but the tooling under it has moved a long way in 2026. TypeScript 7 (the native Go compiler) went GA on 8 July 2026. ESLint 10 removed eslintrc, and ESLint 9 reached end of life on 6 August 2026. Ruff 0.16 raised its default rule set from 59 to 413 rules. Pyrefly reached 1.0 while ty is still in beta. mypy is now on the 2.x line. PER Coding Style is at 3.1 and *replaces* PSR-12 rather than merely extending it. detekt 2.0 and Psalm 7 are both still pre-release.

Method note: I read quoted text either from the fetched page or from the search-engine extract of that page, both on 2026-09-23. Rows marked "prior knowledge, not re-verified this run" are well-known facts whose source text I could not re-read in this session. Check those before filing.

## 1. Summary

**TL;DR**
- **TypeScript 7.0 is GA** (8 July 2026) and its `tsc` is the Go-native compiler. TypeScript 6.0 (23 March 2026) turned `strict` on by default and deprecated legacy options, which 7.0 removes. The 7.0 programmatic API is not yet stable (expected in 7.1, stable targeted for 24 November 2026), so typescript-eslint-style tooling still needs the 6.x API through the `@typescript/typescript6` alias.
- **The Python toolchain consolidated.** Ruff (linter plus formatter) replaces Black, Flake8, isort and pydocstyle. v0.16.0 (23 July 2026) enables 413 rules by default. For type checking, mypy 2.x and pyright are established, Pyrefly 1.0 (12 May 2026) is production-stable, and ty is still a 0.0.x beta.
- **Pin versions and act on the end-of-support dates below.** ESLint v9 has been EOL since 2026-08-06. Python 3.10 reaches EOL on 2026-10-31. .NET 8 and .NET 9 reach end of support on 2026-11-10. detekt 2.0, ktlint 2.0, Psalm 7 and oxfmt are all pre-1.0 or pre-release.

**Also important**
- ESLint v10.0.0 (6 February 2026) removed eslintrc completely, and flat config (`eslint.config.*`) is now the only format. v10 looks up the config from each linted file's directory, which helps monorepos.
- Biome v2 is stable and has type-aware lint rules that don't need the TypeScript compiler. v2.4 was the first minor release of 2026. Oxlint has been stable (1.x) since June 2025 and is at v1.79.0. Its formatter, oxfmt, is v0.64.0, i.e. not 1.0.
- golangci-lint v2 (March 2025) changed the config schema, and v2.13.2 (27 August 2026) is current. The official golangci-lint migration guide says "The linters stylecheck, gosimple, and staticcheck has been merged inside the staticcheck."
- PHP: PER-CS 3.x "extends, expands and replaces PSR-12". PHPStan 2.x has levels 0–10 (level 10 is new in 2.0), and 2.2 shipped on 28 May 2026. Psalm has "the only active maintainer", its stable line is 6.17.0 and 7.0 has been in beta since at least April 2026. That is a bus-factor risk.
- The TC39 type-annotations proposal is still at **Stage 1**, with no sign of progress since 2023. Don't plan around native JavaScript type syntax.
- EditorConfig's specification is at **0.17.2**.
- Naming evidence: full-word identifiers let 72 professional C# developers find defects about **19% faster** than letters or abbreviations (Hofmeister et al., EMSE 2019). Descriptive compound names were about **14% faster** in a study of 88 Java developers (Schankin et al., ICPC 2018). The effect is real but modest, and some studies found no difference (contested).
- Complexity: Sonar's cognitive-complexity rule defaults to **15** per function. Clippy raised its `cognitive_complexity` threshold to 50 (rust-clippy PR #3963) and later removed the lint "from default set of enabled lints" (PR #5428). The current Clippy lint list says "This lint has been left in restriction so as to not mislead users into using this lint as a measurement tool."
- LLM-generated code differs measurably in style from human code (Wang et al., FSE 2025), for example by using fewer idioms. LLMs are also shifting real-world naming: Python snake_case function names rose from 40.7% to 49.8% between Q1 2023 and Q3 2025. Enforce style with formatters and linters, not with prompts.
- .NET 10 is the current LTS (supported until 10 November 2028). .NET 11 launches on 10–13 November 2026.

## 2. Corrections

| # | What we believed | Status | Correct fact | Source |
|---|---|---|---|---|
| C1 | "PHP-FIG's PER Coding Style, which extends PSR-12" | **Partly wrong / out of date** | PER-CS "extends, expands and replaces PSR-12". The current version is **3.1**, and 3.0 was released on 14 July 2025. Projects should pin a PER-CS major version. | https://www.php-fig.org/per/coding-style/meta/ ; https://www.php-fig.org/per/coding-style/ |
| C2 | "Among Python type checkers, mypy and pyright are established, while Astral's ty and Meta's pyrefly are newer" | **Out of date** | Pyrefly reached **1.0 on 12 May 2026** and is marked Production/Stable. ty is still **beta (0.0.x)**, with stable still "targeted for 2026". mypy moved to **2.x** (2.0 on 6 May 2026). Google has stopped feature work on pytype: "We are making Python 3.12 the last supported version for Pytype." | https://pypi.org/project/pyrefly/ ; https://astral.sh/blog/ty ; https://mypy-lang.org/news.html ; https://github.com/google/pytype/issues/1925 |
| C3 | "ESLint with flat config" | **Confirmed, and stronger now** | Since ESLint v10.0.0 (6 February 2026), flat config is the *only* config system. ESLint v9 reached EOL on 2026-08-06. | https://eslint.org/blog/2026/02/eslint-v10.0.0-released/ |
| C4 | TypeScript baseline via typescript-eslint | **Needs updating** | TypeScript 6.0 (23 March 2026) turns `strict: true` on by default. TypeScript 7.0 (8 July 2026) ships the native compiler with no stable programmatic API yet, which is expected in 7.1. Tools that need the TypeScript API run against 6.x through `@typescript/typescript6`. | https://www.infoq.com/news/2026/08/typescript-7-released/ ; https://visualstudiomagazine.com/articles/2026/07/08/typescript-7-arrives-to-rock-vs-code-with-go-powered-speed.aspx |
| C5 | JS/TS formatters: "Biome, Prettier and oxlint" | **Incomplete** | Oxlint is a *linter*. Oxc's *formatter* is **oxfmt**, which is pre-1.0 (v0.64.0) and passed "around 95% of Prettier's JavaScript and TypeScript tests" at alpha. Prettier 3.9 (27 June 2026) is still the reference formatter. | https://github.com/oxc-project/oxc/releases/tag/apps_v1.79.0 ; https://voidzero.dev/posts/announcing-oxfmt-alpha ; https://prettier.io/blog/2026/06/27/3.9.0 |
| C6 | "ruff (Python)" | **Confirmed; add the default change** | Ruff v0.16.0 (23 July 2026) enables 413 rules by default (up from 59) and formats Python code blocks in Markdown by default. Unpinned CI can break on upgrade. | https://astral.sh/blog/ruff-v0.16.0 |
| C7 | "ktlint and detekt (Kotlin)" | **Confirmed; version caveat** | detekt 2.0 is "still available only as a pre-release" (2.0.0-alpha.6). The stable line is 1.23.x. ktlint 2.0 is in alpha according to a mirror (not verified on a primary source). | https://github.com/detekt/detekt |
| C8 | "PHPStan and Psalm" | **Confirmed; maintenance caveat** | Psalm's README names Daniil Gentili as "the only active maintainer". The stable line is 6.17.0, and 7.0.0-beta19 (15 April 2026) is still a pre-release. | https://github.com/vimeo/psalm |
| C9 | "golangci-lint v2" | **Confirmed** | The current version is v2.13.2 (27 August 2026). | https://golangci-lint.run/docs/welcome/install/local/ |
| C10 | "TypeScript has no official style guide" | **Confirmed (not contradicted)** | No official TypeScript style guide was found. The TypeScript team's own coding guidelines page is for contributors to the compiler, not for users (prior knowledge, not re-verified this run). | not found (a primary source that states this) |
| C11 | "Go doc comments (syntax updated in Go 1.19)" | **Confirmed (prior knowledge, not re-verified this run)** | The doc comment syntax (headings, lists, links) was introduced with Go 1.19, as documented at https://go.dev/doc/comment. | https://go.dev/doc/comment |
| C12 | "rustfmt style guide (style edition 2024)" | **Not re-verified** | Style edition 2024 shipped with the Rust 2024 edition (Rust 1.85, February 2025) according to prior knowledge. I did not re-read the source text this run. | https://doc.rust-lang.org/nightly/style-guide/ |
| C13 | "PSR-5 is still a draft" | **Not re-verified** | PSR-5 (PHPDoc) is listed by PHP-FIG as Draft according to prior knowledge. No acceptance was found in this run's searches. | https://www.php-fig.org/psr/ |

## 3. Facts table

| # | Fact | Value | Source URL | Exact quote | Date |
|---|---|---|---|---|---|
| F1 | TypeScript 7 GA | 8 July 2026 | https://visualstudiomagazine.com/articles/2026/07/08/typescript-7-arrives-to-rock-vs-code-with-go-powered-speed.aspx | "Microsoft says TypeScript 7, announced July 8, brings native Go performance to VS Code, Visual Studio and other editors." | 2026-07-08 |
| F2 | TS 7.0 API gap | Stable API expected in 7.1 | https://www.infoq.com/news/2026/08/typescript-7-released/ | "TypeScript 7.0 ships without a stable programmatic API, which the team expects to land in 7.1" | 2026-08 |
| F3 | TS 6 compatibility package | `@typescript/typescript6` | https://www.infoq.com/news/2026/08/typescript-7-released/ | "Microsoft published a compatibility package, @typescript/typescript6, that provides a tsc6 binary and re-exports the 6.0 API so existing tooling keeps working" | 2026-08 |
| F4 | TS 7.1 schedule (secondary) | Beta 6 Oct 2026; stable 24 Nov 2026 | https://diegobetto.com/en/typescript-7-whats-new/ | "beta is planned for October 6, 2026, with stable targeted for November 24, 2026" | read 2026-09-23 |
| F5 | TS 6.0 release and defaults (secondary) | 23 March 2026; `strict` on by default | https://noqta.tn/en/blog/typescript-6-release-features-migration-guide-2026 | "TypeScript 6.0 landed on March 23, 2026" / "TypeScript 6.0 ships with strict mode by default, ES2025 target" | read 2026-09-23 |
| F6 | TS 6.0 deprecations (primary plan) | Removed in TS 7 | https://github.com/microsoft/TypeScript/issues/54500 | "these options will be removed entirely in TypeScript 7 (the native TypeScript port)" | read 2026-09-23 |
| F7 | ESLint v10.0.0 | 6 February 2026 | https://eslint.org/blog/2026/02/eslint-v10.0.0-released/ | "Published 06 Feb, 2026" / "We just pushed ESLint v10.0.0, which is a major release upgrade of ESLint." | 2026-02-06 |
| F8 | eslintrc removed | v10 | https://eslint.org/docs/latest/use/migrate-to-10.0.0 | "the eslintrc config system has been completely removed in ESLint v10.0.0" | read 2026-09-23 |
| F9 | ESLint v9 EOL | 2026-08-06 | https://eslint.org/blog/2026/02/eslint-v10.0.0-released/ | "ESLint v9.x reached end-of-life on 2026-08-06 and is no longer maintained." | read 2026-09-23 |
| F10 | ESLint latest minor | v10.11.0 (date not found) | https://eslint.org/blog/2025/11/eslint-v10.0.0-alpha.0-released/ | "We just pushed ESLint v10.11.0, which is a minor release upgrade of ESLint." | read 2026-09-23 |
| F11 | ESLint v10 Node support | ^20.19.0 \|\| ^22.13.0 \|\| >=24 | https://infoq.com/news/2026/04/eslint-10-release | "Node.js support has been tightened to ^20.19.0 \|\| ^22.13.0 \|\| >=24." | 2026-04 |
| F12 | Ruff v0.16.0 | 23 July 2026; 413 default rules | https://astral.sh/blog/ruff-v0.16.0 | "Ruff now enables 413 rules by default, up from 59 in previous versions." | 2026-07-23 |
| F13 | Ruff replaces older tools | Black, Flake8, isort, pydocstyle, pyupgrade | https://astral.sh/blog/ruff-v0.16.0 | "Ruff can be used to replace Black, Flake8 (plus dozens of plugins), isort, pydocstyle, pyupgrade, and more" | 2026-07-23 |
| F14 | Ruff latest | released 16 Sep 2026 (version number not captured) | https://pypi.org/project/ruff/ | "Released: Sep 16, 2026 Latest release" | read 2026-09-23 |
| F15 | ty status | Beta; stable targeted for 2026 | https://astral.sh/blog/ty | "Today, we're announcing the Beta release of ty." / "we're working towards a Stable release next year" | 2025-12-16 |
| F16 | ty latest | release dated 17 Sep 2026 (0.0.x) | https://github.com/astral-sh/ty/releases | "Released on 2026-09-17." | read 2026-09-23 |
| F17 | Pyrefly latest | Released 12 May 2026; Production/Stable | https://pypi.org/project/pyrefly/ | "Latest release · Released: May 12, 2026" / "Development Status · 5 - Production/Stable" | read 2026-09-23 |
| F18 | Pyrefly = 1.0 (secondary) | 1.0 on 12 May 2026 | https://www.danilchenko.dev/posts/pyrefly-vs-mypy-vs-ty/ | "The 1.0 release on May 12, 2026 marks production readiness." | read 2026-09-23 |
| F19 | mypy 2.x | 2.0 on 6 May; 2.3 on 13 Jul 2026 | https://mypy-lang.org/news.html | "13 Jul 2026 · Mypy 2.3 was released." / "6 May 2026 · Mypy 2.0 was released." | read 2026-09-23 |
| F20 | mypy latest on PyPI | 15 Aug 2026 (version not captured) | https://pypi.org/project/mypy/ | "Released: Aug 15, 2026 Latest release" | read 2026-09-23 |
| F21 | mypy native parser | To become default "soon" | https://mypy-lang.blogspot.com/2026/07/mypy-23-released.html | "We are planning to enable the new native parser (--native-parser) by default soon." | 2026-07 |
| F22 | Python 3.10 EOL | 31 Oct 2026 | https://www.herodevs.com/blog-posts/python-end-of-life-dates-every-versions-support-timeline | "Python 3.10 reaches end of life on October 31, 2026." | read 2026-09-23 |
| F23 | Python 3.15 | rc2 on 1 Sep 2026; final expected in October | https://www.herodevs.com/blog-posts/python-end-of-life-dates-every-versions-support-timeline | "3.15.0rc2 shipped September 1, 2026) with the final release expected in October" | read 2026-09-23 |
| F24 | Biome v2 | Type-aware linting without tsc | https://biomejs.dev/blog/biome-v2/ | "the first JavaScript and TypeScript linter that provides type-aware linting rules that doesn't rely on the TypeScript compiler!" | 2025-06 |
| F25 | Oxlint stable | 1.0 | https://voidzero.dev/posts/announcing-oxlint-1-stable | "The first stable version Oxlint has been released!" | 2025-06-10 |
| F26 | Oxlint/oxfmt latest | v1.79.0 / v0.64.0 | https://github.com/oxc-project/oxc/releases/tag/apps_v1.79.0 | "Release oxlint v1.79.0 & oxfmt v0.64.0" | read 2026-09-23 |
| F27 | Prettier 3.9 | 27 June 2026 | https://prettier.io/blog/2026/06/27/3.9.0 | "We are excited to announce Prettier 3.9!" | 2026-06-27 |
| F28 | golangci-lint latest | v2.13.2, 27 Aug 2026 | https://mise-versions.jdx.dev/tools/golangci-lint | "2.13 · 2.13.2 · Aug 27, 2026" | read 2026-09-23 |
| F29 | golangci-lint v2 config | `linters.default` replaces enable-all/disable-all | https://ldez.github.io/blog/2025/03/23/golangci-lint-v2/ | "The enable-all and disable-all options have been replaced with a single, more intuitive option: linters.default." | 2025-03-23 |
| F30 | PER-CS scope | Replaces PSR-12 | https://www.php-fig.org/per/coding-style/meta/ | "This PER extends, expands and replaces PSR-12, and is therefore also an extension of PSR-1." | read 2026-09-23 |
| F31 | PER-CS 3.0 release | 14 July (2025) | https://github.com/php-fig/per-coding-style/releases/tag/3.0.0 | "Jean85 released this · 14 Jul 08:30 · 3.0.0" | read 2026-09-23 |
| F32 | PER-CS acronym naming | `XmlFormatter`, not `XMLFormatter` | https://www.php-fig.org/per/coding-style/meta/migration-3.0/ | "When they are used, only the first character should be uppercased: XmlFormatter, not XMLFormatter." | read 2026-09-23 |
| F33 | PHPStan 2.2 | 28 May 2026 | https://phpstan.org/blog/releases | "PHPStan 2.2: Unsealed Array Shapes, Safer Array Keys, and More! May 28, 2026" | read 2026-09-23 |
| F34 | PHPStan level 10 | Introduced in 2.0 (11 Nov 2024) | https://phpstan.org/blog/releases | "PHPStan 2.0 Released With Level 10 and Elephpants! November 11, 2024" | read 2026-09-23 |
| F35 | Psalm maintainer | One active maintainer | https://github.com/vimeo/psalm | "Daniil Gentili, the only active maintainer of Psalm" | read 2026-09-23 |
| F36 | TC39 type annotations | Stage 1 | https://github.com/tc39/proposal-type-annotations/blob/main/README.md | "The following is a Stage 1 proposal." | read 2026-09-23 |
| F37 | EditorConfig spec | 0.17.2 | https://spec.editorconfig.org/index.html | "This is version 0.17.2 of this specification." | read 2026-09-23 |
| F38 | .NET 10 support | Until 10 Nov 2028 | https://devblogs.microsoft.com/dotnet/announcing-dotnet-10/ | ".NET 10 is a Long Term Support (LTS) release and will be supported for three years until November 10, 2028." | 2025-11 |
| F39 | .NET 8/9 EOS | 10 Nov 2026 | https://devblogs.microsoft.com/dotnet/dotnet-8-9-end-of-support/ | ".NET 8 and .NET 9 will both reach end of support on November 10, 2026." (.NET Blog, Rahul Bhandari) | 2026-06-29 |
| F40 | Checkstyle | 14.1.0, 30 Aug 2026 | https://checkstyle.org/releasenotes.html | "Release 14.1.0 · 30.08.2026" | 2026-08-30 |
| F41 | PMD | 7.27.0, 28 Aug 2026 | https://github.com/pmd/pmd/releases | "PMD 7.27.0 (28-August-2026) Latest" | 2026-08-28 |
| F42 | SpotBugs | 4.10.4 | https://spotbugs.readthedocs.io/en/latest/introduction.html | "This document describes version 4.10.4 of SpotBugs." | read 2026-09-23 |
| F43 | Error Prone | 2.50.0, 10 Jun 2026 (latest tag seen) | https://github.com/google/error-prone/tags | "Release Error Prone 2.50.0 · Jun 10, 2026" | read 2026-09-23 |
| F44 | google-java-format | 1.36.1, 30 Jul 2026 | https://github.com/google/google-java-format/releases | "v1.36.1 Latest … released this 30 Jul" | 2026-07-30 |
| F45 | RuboCop | 1.91.0, 10 Sep 2026 | https://rubygems.org/gems/rubocop/versions | "1.91.0 September 10, 2026" | 2026-09-10 |
| F46 | PHP-CS-Fixer | v3.95.26, 19 Sep 2026 | https://github.com/PHP-CS-Fixer/PHP-CS-Fixer/releases | "v3.95.26 Adalbertus Latest … released this · 19 Sep" | 2026-09-19 |
| F47 | detekt 2.0 status | Pre-release (2.0.0-alpha.6) | https://github.com/detekt/detekt | "detekt 2.0 is recommended for its new features, but it is still available only as a pre-release." | read 2026-09-23 |
| F48 | Identifier study | Words 19% faster than letters/abbreviations | https://neverworkintheory.org/2021/08/09/abbreviated-vs-full-names.html (secondary summary of Hofmeister et al.) | "We found that word identifiers led to a 19% increase in speed to find defects compared to meaningless single letters and abbreviations" | 2021-08-09 |
| F49 | Descriptive names study | about 14% faster, 88 Java developers | https://dl.acm.org/doi/10.1145/3196321.3196332 | "finding the semantic defect about 14% faster than with shorter but less descriptive identifier names" | 2018 |
| F50 | Sonar cognitive complexity default | 15 | https://github.com/SonarSource/eslint-plugin-sonarjs/blob/master/docs/rules/cognitive-complexity.md | "The maximum authorized complexity can be provided. Default is 15." | read 2026-09-23 |
| F51 | LLM influence on naming | snake_case 40.7% → 49.8% | https://arxiv.org/abs/2506.12014 | "the proportion of snake_case function names in Python code increased from 40.7% in Q1 2023 to 49.8% in Q3 2025" | 2025/2026 |

## 4. Findings

### Q1. Style guides and naming rules per language

Where a row says "prior knowledge", the naming rules are the long-standing, widely documented ones. I did not re-read them this run, so verify them against the URL before filing.

| Language | Official or most-adopted guide | Variables | Constants | Functions/methods | Types | Files/modules | URL |
|---|---|---|---|---|---|---|---|
| Python | PEP 8 (official for the stdlib, de facto everywhere) | `lower_snake` | `UPPER_SNAKE` | `lower_snake` | `CapWords` | short `lowercase` modules, underscores allowed | https://peps.python.org/pep-0008/ (prior knowledge) |
| TypeScript/JS | **No official guide (confirmed).** De facto: typescript-eslint `recommended`/`strict`, plus the Google TypeScript Style Guide (secondary) | `camelCase` | `UPPER_SNAKE` or `camelCase` | `camelCase` | `PascalCase` | kebab-case or camelCase by project convention | https://typescript-eslint.io/users/configs ; https://google.github.io/styleguide/tsguide.html (prior knowledge) |
| C# | Microsoft .NET naming guidelines (Framework Design Guidelines) and C# coding conventions | `camelCase` locals/params; `_camelCase` private fields | `PascalCase` | `PascalCase` | `PascalCase`; interfaces `I`-prefixed | file named after its type | https://learn.microsoft.com/dotnet/standard/design-guidelines/naming-guidelines ; https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions (prior knowledge) |
| PowerShell | Approved verbs (`Get-Verb`) plus the community PowerShell Practice and Style guide (secondary) | `$PascalCase` or `$camelCase` | — | `Verb-Noun`, approved verb, singular noun | `PascalCase` classes | `.ps1`/`.psm1`, module named after its folder | https://learn.microsoft.com/powershell/scripting/developer/cmdlet/approved-verbs-for-windows-powershell-commands ; https://github.com/PoshCode/PowerShellPracticeAndStyle (prior knowledge) |
| Go | Effective Go, Go Code Review Comments, Google Go Style Guide | `mixedCaps`; export by capital letter; initialisms keep case (`URL`, `ID`) | `MixedCaps` (not UPPER_SNAKE) | `MixedCaps` | `MixedCaps` | short lowercase package names, no underscores | https://go.dev/doc/effective_go ; https://go.dev/wiki/CodeReviewComments ; https://google.github.io/styleguide/go/ (prior knowledge) |
| Rust | Rust API Guidelines (naming, C-CASE) plus the Rust Style Guide | `snake_case` | `SCREAMING_SNAKE` | `snake_case` | `UpperCamelCase`; acronyms as one word (`Uuid`) | `snake_case` modules and crates | https://rust-lang.github.io/api-guidelines/naming.html ; https://doc.rust-lang.org/nightly/style-guide/ (prior knowledge) |
| Java | Google Java Style (most adopted). Oracle's 1997 conventions are historical. | `lowerCamelCase` | `UPPER_SNAKE` | `lowerCamelCase` | `UpperCamelCase` | one top-level class per file; lowercase packages with no underscores | https://google.github.io/styleguide/javaguide.html (prior knowledge) |
| Kotlin | Kotlin coding conventions (official) | `camelCase` | `UPPER_SNAKE` for `const val` and top-level immutable values | `camelCase` | `PascalCase` | file named after its single class, otherwise PascalCase describing contents | https://kotlinlang.org/docs/coding-conventions.html (prior knowledge) |
| C | **No official guide.** Most adopted: Linux kernel coding style, plus the SEI CERT C standard for safety (secondary) | `lower_snake` | `UPPER_SNAKE` macros | `lower_snake` | `lower_snake` or `_t` | `lower_snake.c/.h` | https://www.kernel.org/doc/html/latest/process/coding-style.html (prior knowledge) |
| C++ | C++ Core Guidelines (guidance, not a formatting guide), plus Google C++ Style (most adopted naming) | Google: `snake_case`; members `snake_` | Google: `kConstant` | Google: `PascalCase` | `PascalCase` | `snake_case.cc/.h` | https://isocpp.github.io/CppCoreGuidelines/ ; https://google.github.io/styleguide/cppguide.html (prior knowledge) |
| PHP | PSR-1 plus **PER-CS 3.1** (replaces PSR-12) | `$camelCase` (PSR-1 leaves it open; consistency required) | `UPPER_SNAKE` class constants | `camelCase` methods | `StudlyCaps`; acronyms `XmlFormatter` (PER-CS 3.0) | PSR-4 autoload: one class per file, path matches namespace | https://www.php-fig.org/per/coding-style/ ; https://www.php-fig.org/psr/psr-1/ |
| Ruby | Community Ruby Style Guide (enforced by RuboCop) | `snake_case` | `SCREAMING_SNAKE` | `snake_case`; predicates end in `?`, dangerous methods in `!` | `CamelCase` | `snake_case.rb` | https://rubystyle.guide/ (prior knowledge) |
| Bash | Google Shell Style Guide | `lower_snake` locals | `UPPER_SNAKE` for constants and env vars, `readonly` | `lower_snake` | — | `.sh` for libraries; executables may omit the extension | https://google.github.io/styleguide/shellguide.html (prior knowledge) |
| SQL | **No official guide.** Most adopted: Simon Holywell's SQL Style Guide (secondary), or the dialect defaults encoded in SQLFluff | `snake_case` identifiers | — | — | tables: Holywell prefers collective names (`staff`) | — | https://www.sqlstyle.guide/ (prior knowledge) |
| VBA | **No official guide.** Microsoft publishes VBA language docs only. Most adopted: Rubberduck's inspections (secondary) | `camelCase` or `PascalCase`; Hungarian notation is widespread but discouraged by Rubberduck | `UPPER_SNAKE` | `PascalCase` | `PascalCase` | module names `PascalCase` | https://rubberduckvba.com/ (prior knowledge) |

Position: for this repository, adopt the formatter's style as the language style wherever an official formatter exists (gofmt, rustfmt, ruff format, dotnet format, google-java-format, ktlint). Write naming rules down only for the things a formatter can't enforce.

### Q2. Doc comment formats

| Language | Format | A public API doc must include | Render/check tool |
|---|---|---|---|
| Python | PEP 257 docstrings, in Google or NumPy section style | Summary line; Args/Parameters; Returns; Raises. Types go in annotations, not in the docstring. | Sphinx (+napoleon), mkdocstrings; checked by Ruff `D` (pydocstyle) rules (F13) |
| TS/JS | JSDoc (JS type checking); TSDoc (TypeScript syntax standard) | Summary; `@param`; `@returns`; `@throws`; `@deprecated`; `@example` | TypeDoc, API Extractor; eslint-plugin-jsdoc; Oxlint includes eslint-plugin-jsdoc rules (per its 1.0 post). TSDoc's current release status was not found this run. |
| C# | XML documentation comments (`///`) | `<summary>`, `<param>`, `<returns>`, `<exception>` | Compiler `GenerateDocumentationFile`, warning CS1591 for missing docs; DocFX (prior knowledge) |
| PowerShell | Comment-based help | `.SYNOPSIS`, `.DESCRIPTION`, `.PARAMETER`, `.EXAMPLE`, `.OUTPUTS` | `Get-Help`; platyPS; PSScriptAnalyzer `ProvideCommentHelp` (prior knowledge) |
| Go | Go doc comments (1.19 syntax) | Every exported name has a comment starting with the name | `go doc`, pkg.go.dev; golangci-lint `godoc-lint`, revive (golangci-lint changelog lists godoc-lint 0.11.1) |
| Rust | rustdoc (`///`, `//!`, Markdown) | Summary; `# Examples`; `# Errors`; `# Panics`; `# Safety` for `unsafe` | `cargo doc`; `#![warn(missing_docs)]`; clippy `missing_errors_doc` / `missing_panics_doc` (prior knowledge) |
| Java | Javadoc | Summary; `@param`, `@return`, `@throws` | `javadoc -Xdoclint`; Checkstyle `JavadocMethod` |
| Kotlin | KDoc | Summary; `@param`, `@return`, `@throws` | Dokka; detekt `UndocumentedPublic*` rules (prior knowledge) |
| C/C++ | Doxygen | `@brief`, `@param`, `@return`, ownership and thread-safety notes | Doxygen; clang `-Wdocumentation`; clang-tidy (prior knowledge) |
| PHP | PHPDoc (PSR-5 still a draft, not re-verified) | Summary; `@param`, `@return`, `@throws`; generics via `@template` | phpDocumentor; PHPStan and Psalm read PHPDoc types (the PHPStan/Psalm comparison covers `@template`) |
| Ruby | YARD (RDoc is the stdlib default) | Summary; `@param`, `@return`, `@raise` | `yard doc`, `yard stats --list-undoc`; RuboCop `Style/Documentation` |
| Bash | Google Shell Style function header comments | Description; Globals; Arguments; Outputs; Returns | No renderer (by convention) (prior knowledge) |
| SQL / VBA | No standard | — | not found |

### Q3. Formatters, linters and type checkers

| Language | Formatter | Linter | Type checker | Status notes |
|---|---|---|---|---|
| Python | ruff format (Black-compatible) | ruff (v0.16 defaults) | mypy 2.x, pyright; Pyrefly 1.x; ty (beta) | Black, Flake8, isort and pydocstyle are **superseded by Ruff** for new projects (F13). pytype has stopped new-feature work, with Python 3.12 as its last supported version (github.com/google/pytype/issues/1925). |
| TS/JS | Prettier 3.9; Biome 2.x; oxfmt (pre-1.0) | ESLint 10 + typescript-eslint; Biome; Oxlint 1.x | tsc 7 (Go) / tsc 6 for API-dependent tooling | ESLint 9 EOL. typescript-eslint's TS 7 support: version not found; see F2/F3. |
| C# | dotnet format | Roslyn analyzers (`AnalysisLevel`), `.editorconfig` severity | compiler with nullable enabled | .NET 8/9 EOS on 10 Nov 2026 |
| PowerShell | Invoke-Formatter (PSScriptAnalyzer) | PSScriptAnalyzer 1.25.0 (date not found) | — | — |
| Go | gofmt / goimports | go vet, staticcheck, golangci-lint v2.13.2 | compiler | golangci-lint v2 merged stylecheck and gosimple into staticcheck (official golangci-lint migration guide, PR #5487) |
| Rust | rustfmt | clippy | compiler | versions track the Rust toolchain (6-weekly); the current Rust version was not captured this run |
| Java | google-java-format 1.36.1 | Checkstyle 14.1.0, PMD 7.27.0, SpotBugs 4.10.4, Error Prone 2.50.0 | javac (+ NullAway/JSpecify, prior knowledge) | all active |
| Kotlin | ktlint (1.8.x stable per mirror; 2.0 alpha) | detekt 1.23.x stable; 2.0 alpha.6 | kotlinc | detekt 2.0 is not final (F47) |
| C/C++ | clang-format (LLVM 22.1.x confirmed; 23.1.0 claimed by Wikipedia, unverified) | clang-tidy | compiler | — |
| PHP | PHP-CS-Fixer v3.95.26 (the `@PER-CS` ruleset exists; prior knowledge) | PHPStan 2.x | PHPStan / Psalm 6.17.0 | Psalm has a single maintainer, and 7.0 has been in beta since April 2026 or earlier |
| Ruby | RuboCop 1.91.0 / Standard | RuboCop | Sorbet; RBS + Steep | Standard, Sorbet and Steep versions: not found this run |
| Bash | shfmt | ShellCheck | — | versions not found this run |
| SQL | SQLFluff (fix) | SQLFluff | — | version not found |
| YAML | — | yamllint | — | version not found |

Recommended configurations (positions):
- **Python:** a `pyproject.toml` `[tool.ruff]` section with `target-version` pinned. Accept the v0.16 default set, or `select = ["E4","E7","E9","F"]` to restore the old defaults (F12, whose source lists this exact config). Pick one type checker in CI (mypy `--strict` or pyright `strict`). Run Pyrefly or ty alongside it as advisory until ty is stable.
- **TS:** `eslint.config.mjs` with `tseslint.configs.strictTypeChecked` + `stylisticTypeChecked` (config names are prior knowledge; verify on typescript-eslint.io). Pin `typescript` 6.x through the alias until typescript-eslint supports TS 7's API.
- **Go:** `.golangci.yml` with `version: "2"` and `linters.default: standard`, plus errcheck, govet, staticcheck and ineffassign (F29; secondary dev.to guidance).

### Q4. Naming and comprehension evidence

- Hofmeister, Siegmund and Holt, "Shorter Identifier Names Take Longer to Comprehend" (EMSE 24(1):417–443, 2019; SANER 2017). The study had 72 professional C# developers find defects. Words beat letters and abbreviations by about 19%, and letters and abbreviations did not differ from each other. The ACM abstract also says "in many cases, there is no statistical difference between full words and abbreviations" (https://dl.acm.org/doi/10.1007/s10664-018-9621-x).
- Schankin et al., ICPC 2018. The study had 88 Java developers. With descriptive compound names they found the defect "about 14% faster" (F49).
- **Contested:** Scanniello et al. (TOSEM 2017) "found no difference in development effort or efficiency when using abbreviated identifier names", and Beniamini et al. (ICPC 2017) found no comprehension difference for single-letter variables in some settings. Both are summarised by neverworkintheory.org (secondary). My position: prefer full words, allow only well-known abbreviations (`id`, `url`, `http`), and don't treat length as a goal in itself.
- Booleans (`is_`/`has_` prefixes) and units in names (`timeout_ms`): **no peer-reviewed comprehension study was found this run**. The guidance exists in style guides and books (for example the Google style guides, prior knowledge), which are secondary. Position: include units whenever the type doesn't carry them.

### Q5. Type strictness

- **Python:** the typing specification (https://typing.python.org/en/latest/spec/, prior knowledge) is the conformance target. mypy 2.0 changed defaults: `--local-partial-types` was planned as the 2.0 default (mypy 1.20 post), and parallel checking with `--num-workers` is experimental. Pyrefly 1.0 is stable. ty is beta, and its conformance is reported at 53.2% against Pyrefly's 87.8% on the March 2026 suite (secondary: danilchenko.dev), so ty is **not ready as a CI gate**. Recommendation: `mypy --strict` or pyright `"typeCheckingMode": "strict"`.
- **TypeScript:** `strict` is the default from 6.0 (F5). Also enable `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` (neither is part of `strict`), `verbatimModuleSyntax` (explicit `import type`), and `erasableSyntaxOnly` (TS 5.8+; bans enums, namespaces and parameter properties so that Node type-stripping works). The last two facts are prior knowledge, not re-verified this run.
- **C#:** `<Nullable>enable</Nullable>` plus `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` (or `WarningsAsErrors=nullable`) (prior knowledge).
- **PHP:** put `declare(strict_types=1);` in every file. PHPStan levels run 0–10, and level 10 was added in 2.0 (F34). Target level 8+ for new code and use a baseline for legacy code.
- **Ruby:** RBS (the stdlib signature language) with Steep, or Sorbet (`# typed: strict`). Versions were not found this run.
- **TC39 type annotations:** Stage 1. The README still carries the notice "This document has not been updated regularly", and the latest meeting notes it points to are from 2023. It is effectively stalled (F36).

### Q6. Comments for future maintainers

- **Why, not what:** Google's style guides and PEP 8 both say comments should explain intent and must be kept up to date. PEP 8: "Comments that contradict the code are worse than no comments" (prior knowledge, not re-verified this run).
- **TODO/FIXME:** the Google style guides require `TODO` with a bug or issue link or an owner (prior knowledge). Ruff's `TD` (flake8-todos) and `FIX` rules can enforce this (prior knowledge). Position: `TODO(#123): …`, and lint for TODOs that have no issue link.
- **Licence headers:** use SPDX short identifiers (`SPDX-License-Identifier: Apache-2.0`) and REUSE (`reuse lint`) for machine-checkable compliance. The current REUSE spec version was not found this run.

### Q7. Formatting consensus

| Formatter | Indent | Line length |
|---|---|---|
| gofmt | tabs | none |
| rustfmt | 4 spaces | 100 (`max_width`) |
| ruff format / Black | 4 spaces | 88 |
| Prettier | 2 spaces | 80 (`printWidth`) |
| Biome | tabs (default) | 80 |
| google-java-format | 2 spaces (+4 continuation) | 100 |
| ktlint (Kotlin conventions) | 4 spaces | 140 in ktlint_official (prior knowledge) |
| dotnet format | 4 spaces | none enforced |
| PER-CS | 4 spaces | soft limit 120, SHOULD ≤ 80 (prior knowledge) |
| shfmt | tabs by default; Google style uses 2 spaces | Google: 80 |
| clang-format (LLVM style) | 2 spaces | 80 |

All rows are prior knowledge except the Biome row, which is also prior knowledge. Verify each against the tool's documentation before filing. EditorConfig spec 0.17.2 (F37) defines `indent_style`, `indent_size`, `tab_width`, `end_of_line`, `charset`, `trim_trailing_whitespace`, `insert_final_newline` and `root`. `max_line_length` is only a "domain-specific" wiki property, not part of the spec (per the EditorConfig wiki properties page). The spec also says "EditorConfig plugins shall ignore unrecognized keys".

### Q8. Readability metrics

- **Cyclomatic complexity** (McCabe) counts independent paths. It is reported by ESLint `complexity` (default 20), Ruff `C901` (`max-complexity`, default 10), gocyclo, PMD and Checkstyle (prior knowledge).
- **Cognitive complexity** (SonarSource) adds penalties for nesting and ignores constructs that are easy to read. It is reported by SonarQube/SonarLint (default 15, F50; 25 for C/C++/Objective-C per a secondary source), eslint-plugin-sonarjs, gocognit (in golangci-lint) and clippy `cognitive_complexity`. For clippy, the threshold was raised to 50 (rust-clippy PR #3963) and the lint was removed from the default set (PR #5428). It now sits in the restriction group "so as to not mislead users into using this lint as a measurement tool" (Clippy lint list).
- **Position:** gate on cognitive complexity at 15 per function for application code, and use cyclomatic complexity as a testability signal (≤10), not as a gate.

### Q9. Style mistakes AI assistants make

- Wang et al., "Beyond Functional Correctness: Investigating Coding Style Inconsistencies in Large Language Models" (FSE 2025) built a taxonomy of LLM-versus-human style differences in readability, conciseness and robustness. One example: LLM code "often does not use advanced syntax features of the Python language, such as Pythonic idioms", e.g. list comprehensions (https://dl.acm.org/doi/10.1145/3715749).
- Xu et al., "code_transformed" (EACL 2026 Findings) found measurable shifts in real-world naming style towards LLM traits (F51).
- Per-language vendor guidance on AI style errors: **not found** this run.

## 5. Tools

| Tool | Purpose | Current version | Released | Install or run command | Config file | Source |
|---|---|---|---|---|---|---|
| ruff | Python lint + format | latest on PyPI (0.16.x line) | 2026-09-16 | `uv tool install ruff@latest` | `pyproject.toml` / `ruff.toml` | https://pypi.org/project/ruff/ |
| mypy | Python types | 2.3.x (latest PyPI upload 2026-08-15) | 2026-07-13 (2.3) | `pip install mypy` | `pyproject.toml` / `mypy.ini` | https://mypy-lang.org/news.html |
| pyright | Python types | not found | not found | `npm i -D pyright` | `pyrightconfig.json` | not found |
| Pyrefly | Python types | 1.x (1.0 released 2026-05-12) | 2026-05-12 | `pip install pyrefly` | `pyrefly.toml` / `pyproject.toml` | https://pypi.org/project/pyrefly/ |
| ty | Python types (beta) | 0.0.x | 2026-09-17 | `uv tool install ty@latest` | `ty.toml` / `pyproject.toml` | https://github.com/astral-sh/ty/releases |
| TypeScript | compiler | 7.0.x (GA) | 2026-07-08 | `npm i -D typescript` | `tsconfig.json` | F1 |
| ESLint | JS lint | 10.11.0 | not found | `npm i -D eslint` | `eslint.config.*` | F10 |
| typescript-eslint | TS lint | not found | not found | `npm i -D typescript-eslint` | `eslint.config.*` | not found |
| Prettier | JS/TS format | 3.9.x (3.9.6 per npm, unverified) | 2026-06-27 (3.9.0) | `npm i -D prettier` | `.prettierrc` | F27 |
| Biome | JS/TS lint + format | 2.4.x (patch not found) | 2026 | `npm i -D @biomejs/biome` | `biome.json` | https://biomejs.dev/blog/biome-v2/ |
| Oxlint / oxfmt | JS/TS lint / format | 1.79.0 / 0.64.0 | not found | `npm i -D oxlint` | `.oxlintrc.json` | F26 |
| dotnet format | C# format | ships with the .NET SDK (10.x) | 2025-11 (.NET 10) | `dotnet format` | `.editorconfig` | F38 |
| PSScriptAnalyzer | PowerShell lint | 1.25.0 | not found | `Install-PSResource PSScriptAnalyzer` | `PSScriptAnalyzerSettings.psd1` | https://www.powershellgallery.com/packages/PSScriptAnalyzer/1.25.0 |
| golangci-lint | Go lint runner | 2.13.2 | 2026-08-27 | `curl -sSfL https://golangci-lint.run/install.sh \| sh -s v2.13.2` | `.golangci.yml` | F28 |
| gofmt / go vet / staticcheck | Go | tracks Go / not found | — | `gofmt -l .` / `go vet ./...` | — | not found |
| rustfmt / clippy | Rust | tracks the toolchain | — | `cargo fmt` / `cargo clippy` | `rustfmt.toml` / `clippy.toml` | not found |
| Checkstyle | Java style | 14.1.0 | 2026-08-30 | Maven/Gradle plugin | `checkstyle.xml` | F40 |
| PMD | Java static analysis | 7.27.0 | 2026-08-28 | `pmd check` | ruleset XML | F41 |
| SpotBugs | Java bugs | 4.10.4 | by 2026-08-20 | Gradle/Maven plugin | filter XML | F42 |
| Error Prone | Java compiler checks | 2.50.0 | 2026-06-10 | javac plugin | build flags | F43 |
| google-java-format | Java format | 1.36.1 | 2026-07-30 | jar / plugin | — | F44 |
| ktlint | Kotlin lint + format | 1.8.x (unverified) | not found | `ktlint` CLI | `.editorconfig` | mirror only |
| detekt | Kotlin static analysis | 1.23.8 stable; 2.0.0-alpha.6 | not found | Gradle plugin | `detekt.yml` | F47 |
| clang-format / clang-tidy | C/C++ | LLVM 22.1.x confirmed | not found | `clang-format -i` | `.clang-format` / `.clang-tidy` | https://github.com/llvm/llvm-project/releases/tag/llvmorg-22.1.0 |
| PHP-CS-Fixer | PHP format | 3.95.26 | 2026-09-19 | `composer require --dev friendsofphp/php-cs-fixer` | `.php-cs-fixer.dist.php` | F46 |
| PHPStan | PHP analysis | 2.2.x | 2026-05-28 (2.2) | `composer require --dev phpstan/phpstan` | `phpstan.neon` | F33 |
| Psalm | PHP analysis | 6.17.0 (7.0.0-beta19 pre-release) | not found | `composer require --dev vimeo/psalm` | `psalm.xml` | F35 |
| RuboCop | Ruby lint + format | 1.91.0 | 2026-09-10 | `gem install rubocop` | `.rubocop.yml` | F45 |
| Standard / Sorbet / Steep | Ruby | not found | not found | `gem install standard` / `sorbet` / `steep` | `.standard.yml` / `sorbet/config` / `Steepfile` | not found |
| ShellCheck / shfmt | Shell | not found | not found | `shellcheck *.sh` / `shfmt -d .` | `.shellcheckrc` / `.editorconfig` | not found |
| SQLFluff | SQL | not found | not found | `pip install sqlfluff` | `.sqlfluff` | not found |
| yamllint | YAML | not found | not found | `pip install yamllint` | `.yamllint` | not found |
| EditorConfig | cross-editor basics | spec 0.17.2 | not found | editor plugin | `.editorconfig` | F37 |

## 6. Changing in the next 12 months

- **Python 3.10 EOL on 31 October 2026 (within 12 months).** Python 3.15 final is expected in October 2026 (F22, F23). Raise `target-version` and `python_requires`.
- **.NET 8 and .NET 9 end of support on 10 November 2026 (within 12 months).** .NET 11 launches on 10–13 November 2026 (F39).
- **ESLint v9 has been EOL since 6 August 2026 (already passed).** Migrate to v10 flat config (F9).
- **TypeScript 7.1:** beta on 6 October 2026 and stable targeted for 24 November 2026 (secondary, F4). It is expected to stabilise the API that typescript-eslint and framework tooling need. Options deprecated in 6.0 are already removed in 7.0 (F6).
- **mypy:** the native parser will become the default "soon" (F21).
- **ty stable:** still "targeted for 2026" (no date found).
- **detekt 2.0, ktlint 2.0, Psalm 7 and oxfmt 1.0:** all pre-release, with no GA dates found.
- **Ruff:** v0.16 changed the default rule set. Expect further rule recategorisation ("look forward to upcoming developments in this area", F12 source).

## 7. Common mistakes

- **Leaving tools unpinned:** Simon Willison's CI "started failing thanks to new default Ruff checks and my unpinned "ruff" dev dependency" (https://simonwillison.net/2026/Jul/25/ruff/, secondary, 2026-07-25).
- Generating `.eslintrc.*` files or using `--env`/`--rulesdir` flags, which v10 no longer honours (F8). AI assistants trained on pre-2024 code do this often. That last point is my inference, not a sourced finding.
- Assuming TypeScript 7 works with every tool: until 7.1 there is no stable API, so use the `@typescript/typescript6` alias (F2, F3).
- Relying on implicit tsconfig defaults: 6.0 changed `strict`, `module`, `target` and `types` (`types: []`) (F5, F6).
- Using ty as the only CI type gate while it is in beta (F15).
- Writing `XMLFormatter` in PER-CS projects (F32), or citing PSR-12 as current.
- LLM output that ignores idioms (for example writing loops instead of comprehensions) and drifts in naming style (Q9 sources).
- Suppressing lint rules instead of refactoring when complexity rules fire (cyclomatic rules push people to disable comments, per jfmengels.net, secondary).

## 8. Sources and licences

Licences are prior knowledge unless the source text was read this run. Verify each one before adapting any material.

| Source | Licence | Quote? | Paraphrase? | Adapt code? | Attribution |
|---|---|---|---|---|---|
| PEPs (peps.python.org) | Public domain (PEP text) | Yes | Yes | Yes | Courtesy link |
| Google Style Guides | CC BY 3.0 | Yes | Yes | Yes, with attribution | "Google Style Guide, CC BY 3.0" plus a link |
| Microsoft Learn (.NET, PowerShell docs) | CC BY 4.0 (docs); MIT (code samples) | Yes | Yes | Yes | Credit Microsoft plus a link; keep the MIT notice for code |
| PowerShell Practice and Style | CC BY-SA 4.0 (verify) | Brief | Yes | Only under the SA terms, so avoid mixing into Apache-2.0 files | Credit plus the licence |
| go.dev docs | CC BY 4.0 (text); BSD-3 (code) | Yes | Yes | Yes | Credit "The Go Authors" |
| Rust API Guidelines / Style Guide | MIT or Apache-2.0 | Yes | Yes | Yes | Keep the notice |
| C++ Core Guidelines | MIT-style (Standard C++ Foundation) | Yes | Yes | Yes | Keep the notice |
| Ruby Style Guide | CC BY 3.0 | Yes | Yes | Yes | Credit plus a link |
| Kotlin docs | Apache-2.0 | Yes | Yes | Yes | NOTICE-compatible |
| PHP-FIG PSR/PER | MIT | Yes | Yes | Yes | Keep the copyright notice |
| ESLint, Ruff, ty, typescript-eslint, Biome, Oxc docs | MIT | Yes | Yes | Yes | Keep the MIT notice for copied code |
| EditorConfig spec | not found | Brief quote only | Yes | not found | Link |
| TC39 proposal repo | not found (TC39 repos usually use the Ecma licence) | Brief | Yes | Avoid | Link |
| Microsoft devblogs, InfoQ, Visual Studio Magazine, dev.to, Medium, pydevtools, herodevs | All rights reserved | Brief fair-use quote only | Yes | No | Name plus link |
| ACM/arXiv papers (Hofmeister, Schankin, Wang, Xu) | Publisher copyright or arXiv licence | Brief | Yes | No | Full citation |
| Simon Holywell SQL Style Guide | CC BY-SA 4.0 (verify) | Brief | Yes | SA terms apply | Credit |
| Rubberduck | GPL-3.0 (code) | Brief | Yes | No (GPL) | Link |

## 9. Not found, contested, not covered

- **Not found:** current versions and dates for pyright, typescript-eslint, Standard, Sorbet, Steep, ShellCheck, shfmt, SQLFluff, yamllint, staticcheck and Rust/rustfmt/clippy. Also the exact release numbers for ruff 0.16.x and mypy 2.3.x, the dates for ESLint 10.11.0, oxlint 1.79.0, PSScriptAnalyzer 1.25.0 and Psalm 6.17.0, TSDoc's release status, the REUSE spec version, the EditorConfig spec licence, peer-reviewed studies on boolean prefixes and units in names, and per-language vendor guidance on AI style errors.
- **Contested:** abbreviations and comprehension (Hofmeister/Schankin versus Scanniello/Beniamini, Q4). Which type checker to recommend (pydevtools recommends Pyrefly, others keep mypy; both secondary). The LLVM current version (a primary source confirms 22.1.x; Wikipedia claims 23.1.0 on 25 August 2026).
- **Unverified secondary claims flagged:** "Astral, now part of OpenAI" (pydevtools); TS 7.1 dates (Diego Betto blog); ty and Pyrefly conformance percentages (danilchenko.dev).
- **Not covered in depth:** SQL and VBA naming beyond the community guides; C naming beyond the Linux kernel style; the full list of TypeScript strictness flags in 7.0.