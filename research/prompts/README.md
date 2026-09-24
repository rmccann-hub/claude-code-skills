# Research runs

Twenty-one prompts, one file each. Each file is the whole prompt: paste all of it into a new
claude.ai chat with Research turned on (or Web search, if Research isn't offered). Run them
in any order, several at a time in separate chats. Priority 1 first.

Each report starts with a line naming itself, so you only send the saved report back, with
no message. Save each one under the name its second line gives, for example `R01-RESULT.md`.

| Run | Priority | File | Covers | Categories |
|---|---|---|---|---|
| R01 | 1 | [R01-agents-and-ai-security.md](R01-agents-and-ai-security.md) | Agent context files, Claude Code configuration, and AI agent security | agent-context-files, ai-agent-security, project-bootstrap-and-audit, skill-builder |
| R02 | 1 | [R02-structure-docs-file-size.md](R02-structure-docs-file-size.md) | Repository structure, documentation, Markdown, file size and splitting | repo-structure, documentation, markdown, code-style (file and function size) |
| R03 | 1 | [R03-style-naming-comments-types.md](R03-style-naming-comments-types.md) | Code style, naming, comments and docstrings, formatting, and types | code-style, types, and the style section of every language skill |
| R04 | 1 | [R04-secure-coding.md](R04-secure-coding.md) | Secure coding, input handling, threat modelling, authentication and cryptography | secure-coding, input-handling, configuration, and the security file of every skill |
| R05 | 1 | [R05-supply-chain-versioning-releases.md](R05-supply-chain-versioning-releases.md) | Supply chain, dependencies, versioning, changelogs, releases, deprecation, and keeping current | supply-chain-security, versioning-and-releases, keeping-current, ci-cd |
| R06 | 2 | [R06-testing.md](R06-testing.md) | Testing | testing, and the testing file of every language skill |
| R07 | 2 | [R07-errors-logging-performance.md](R07-errors-logging-performance.md) | Error handling, logging, observability, performance, concurrency, and log analysis | error-handling, logging-and-observability, performance-and-concurrency, log-analysis |
| R08 | 1 | [R08-git-github-cicd.md](R08-git-github-cicd.md) | Git, GitHub, code review, and CI/CD | git-and-review, ci-cd, and the standard's CI, dependency and security dimensions |
| R09 | 2 | [R09-python.md](R09-python.md) | Python and Python for data | python, and the Python side of data-and-sql and excel |
| R10 | 2 | [R10-typescript-web.md](R10-typescript-web.md) | TypeScript, JavaScript, Node.js, HTML, CSS and the web front end | typescript-javascript, html-css, accessibility (web), visual-theme (CSS) |
| R11 | 2 | [R11-dotnet-powershell-windows.md](R11-dotnet-powershell-windows.md) | C# and .NET, PowerShell, Windows Server and Active Directory | csharp-dotnet, powershell, windows-server, and legacy-languages (.NET Framework, Windows PowerShell 5.1, VBScript) |
| R12 | 3 | [R12-go-rust-c-cpp.md](R12-go-rust-c-cpp.md) | Go, Rust, C and C++ | go, rust, c, cpp, and legacy-languages (C89, C++98) |
| R13 | 3 | [R13-java-kotlin-php-ruby-perl.md](R13-java-kotlin-php-ruby-perl.md) | Java, Kotlin, PHP, Ruby and Perl | java, kotlin, php, ruby, and legacy-languages (Perl, PHP 5-7, Java 8) |
| R14 | 2 | [R14-data-sql.md](R14-data-sql.md) | Data and SQL | data-and-sql, epicor-kinetic (SQL Server), excel (data connections) |
| R15 | 3 | [R15-shell-config-containers-linux-cloud.md](R15-shell-config-containers-linux-cloud.md) | Shell, configuration formats, containers, Kubernetes, infrastructure as code, Linux, networking and cloud | shell, config-formats, containers, kubernetes, infrastructure-as-code, cloud, linux, networking-security, linux-gaming |
| R16 | 2 | [R16-office-epicor-solidworks.md](R16-office-epicor-solidworks.md) | Office (Excel, Word, VBA), Epicor Kinetic and SOLIDWORKS | excel, vba, word-documents, epicor-kinetic, solidworks-api, legacy-languages (VBA, VBScript) |
| R17 | 3 | [R17-legacy-modernization.md](R17-legacy-modernization.md) | Legacy languages and modernization | legacy-languages, legacy-modernization |
| R18 | 3 | [R18-accessibility-i18n-privacy-licensing.md](R18-accessibility-i18n-privacy-licensing.md) | Accessibility, internationalization, privacy and licensing compliance | accessibility, internationalization, privacy-and-compliance, documentation (licences and notices) |
| R19 | 3 | [R19-architecture-api-planning-optimization.md](R19-architecture-api-planning-optimization.md) | Architecture, API design, planning, optimization and scheduling | architecture-and-design, api-design, optimization-and-scheduling |
| R20 | 3 | [R20-design-dataviz-documents.md](R20-design-dataviz-documents.md) | Visual design, data visualization, documents and output formats | visual-theme, data-visualization, documentation (output), word-documents (styling) |
| R21 | 1 | [R21-fewest-dependencies-newest-versions.md](R21-fewest-dependencies-newest-versions.md) | Fewest dependencies and newest versions: what a dependency costs, when to add or remove one, which runtime versions to target and test, and CI that checks less | project-bootstrap-and-audit (dimensions 2, 6 and 8), keeping-current, supply-chain-security, ci-cd, and the dependency advice in every language skill |

Already covered in the building session, so there's no run for them: the skill-authoring
rules; licensing and ownership; the licences of reference sources; this repository's own
platform and tool versions.
