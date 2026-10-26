# Intake, wave 1: the six old language skills and the `coding` skill

Filed 2026-10-26. The rebuild plan's intake step for wave 1, in `ROADMAP.md`'s *Rebuilding the
owner's older skills*: for each old skill, what its successor covers, what was dropped and why,
and its defects, so none is repeated. Company detail and repository names are left out.

The old skills are the owner's claude.ai skills `python-coding`, `javascript-coding`,
`html-coding`, `csharp-coding`, `powershell-scripts` and `bash-coding`, read from the synced
copies in a Claude Code session on 2026-10-26. Their successors are the `coding` skill's modules
of the same names. Nothing was copied from them: none of their examples had been run and none of
their facts had a source. The old `code-standards`, which the language skills told the reader to
load first, wasn't among the synced copies, so `coding`'s contract was written from the
project-bootstrap-and-audit standard and this repository's own rules instead.

Each module was written from primary sources, with research runs R09, R10, R11 and R15 as leads,
and each claim used was checked at its source that day.

## `python-coding`

- **Covered:** current type-hint syntax, no deprecated APIs, a version floor (now
  `requires-python`), specific exceptions, and early checks (now "`assert` isn't validation").
- **Dropped:**
  - docstring layout, file headers, "one class per file", "no nested functions" and `argparse`:
    style and design, for the planned `code-style` and `architecture-and-design` modules;
  - the async reference, for the planned `performance-and-concurrency` module;
  - the pytest reference, for the planned testing skill;
  - the pandas and NumPy reference, for the planned data skill;
  - a refusal table, response templates and notes on long conversations: general behavior, not
    Python, and unsourced.
- **Defects not to repeat:**
  - no example had ever been run, and no fact had a source or a version;
  - an email pattern called RFC 5322 compliant that isn't;
  - a rule against nested functions, broken by its own async example;
  - a parameter annotated `callable = None`, which isn't a valid type;
  - `asyncio.gather(..., return_exceptions=True)` typed as `list[dict]`, though it can hold
    exceptions;
  - a pandas `fillna(..., inplace=True)` on a selected column, which pandas 3's copy-on-write
    breaks;
  - `localhost` and non-reserved email domains in examples.
- **Company detail:** none.

## `javascript-coding`

- **Covered:** strict TypeScript and `unknown` over `any`, ES modules and the `node:` prefix,
  `util.parseArgs`, `async` and `Promise.all`, checking `response.ok`, and input validation, made
  specific: shells, `eval`, prototype pollution, path traversal and ReDoS.
- **Dropped:**
  - naming, doc-comment layout, barrel files and import order: settled by a formatter or linter,
    and unsourced;
  - its refusal list and notes on large files and long conversations: agent behavior;
  - React, and serverless handlers for three hosting platforms: frameworks, out of scope;
  - bundler configuration, out of scope;
  - ES5 and Babel advice: TypeScript 6.0 deprecated `target` `es5`;
  - error classes and exit codes, for the planned `error-handling` module.
- **Defects not to repeat:**
  - "Node.js 20+" (Node 20 ended 2026-04-30), "TypeScript 5.0+" and ES2022;
  - a `tsconfig.json` with `moduleResolution` `bundler` for Node code and no `types`, which loses
    Node's types from TypeScript 6.0;
  - a line counter that overcounts by one on a trailing newline, and exits through
    `main().then(process.exit)`;
  - a serverless handler sending a wildcard CORS header, and one casting parsed JSON with `as`
    unchecked;
  - React examples that fail strict TypeScript, read a stale value, or make an `<article>`
    clickable with no keyboard handler;
  - `fetch` calls with no timeout.
- **Company detail:** none.

## `html-coding`

- **Covered:** semantic elements, heading order and `lang`; alt text, empty for decoration;
  labels, contrast and visible focus; input `type`, `autocomplete` and fieldsets; custom
  properties and `prefers-color-scheme`; logical properties; Subresource Integrity, never with an
  invented hash; and `target="_blank"`.
- **Dropped:**
  - HTML email layout, with no home yet;
  - class-naming schemes, fixed breakpoints, print styles, an `@layer` example and browser
    support percentages: unsourced or preference;
  - a refusal table and notes on conversations: the model's own policy, not markup;
  - CSRF checks, which are server-side, for each server language's module;
  - web component patterns, for `javascript-coding`.
- **Defects not to repeat:**
  - a web component that put its attributes into `shadowRoot.innerHTML`: a cross-site
    scripting hole;
  - "skip SRI for internal tools", and a pinned CDN script with a placeholder hash;
  - "always add `rel="noopener noreferrer"`", though the HTML Standard now implies `noopener`;
  - `focusable="false"` for a browser no longer supported, a deprecated `clip: rect()` hiding
    pattern, and a dated copyright line.
- **Company detail:** none.

## `csharp-coding`

- **Covered:** nullable reference types; `.Result`, `.Wait()`, `async void`, `ConfigureAwait`
  and `await using`; `HttpClient` lifetime and typed clients in singletons; reusing
  `JsonSerializerOptions` and source generation under NativeAOT; `DllImport` against
  `LibraryImport`, reading the last error at once, and `SafeHandle`; no trimming for WinForms and
  WPF; checking that a suggested package exists; and System.CommandLine's changed API.
- **Dropped:**
  - "always omit the W suffix": wrong under `LibraryImport`, which needs the export's exact name;
  - "LibraryImport isn't supported in WinForms or WPF": no source;
  - "always set `PublishTrimmed=false`" for WinForms and WPF: the SDK already turns trimming off;
  - `SecureString` advice: no source;
  - installing a Windows service with `sc`, for the planned `windows-admin` module;
  - EF Core, dependency injection lifetimes and logging, with no planned home yet;
  - toast notifications, desktop type aliases and DPI manifests, unsourced today;
  - xUnit and MSTest, for the planned testing skill.
- **Defects not to repeat:**
  - .NET 8 and C# 12 as the default target, packages pinned at 8.0.0, and System.CommandLine at
    2.0.0-beta4;
  - a settings loader with an empty `catch { }`;
  - unpinned P/Invoke tables, never run;
  - a log of errors met in the owner's own projects, which named them.
- **Company detail:** none, but it named the owner's own projects, and none of those names came
  across.

## `powershell-scripts`

- **Covered:** `CmdletBinding`, parameter validation, approved verbs and `SupportsShouldProcess`;
  `-ErrorAction Stop` inside `try`; `Get-CimInstance` and `Get-WinEvent` over the removed WMI v1
  and event log cmdlets; objects, not `Write-Host`; `@()` around a result that may be one object;
  `+=` in long loops; no `Read-Host` in jobs; and `#Requires`.
- **Dropped:**
  - deploying a vendor's client software: company detail, and Group Policy deployment belongs to
    the planned `windows-admin` module;
  - Active Directory and VMware, for `windows-admin`;
  - detecting an interactive session from the host's name or the command line: fragile, and
    `-NonInteractive` turns a prompt into an error instead;
  - "`$PSBoundParameters` doesn't work in background jobs": no source;
  - PowerShell 2.0 advice: out of date;
  - an output path and a web search step from claude.ai, which don't fit Claude Code;
  - a refusal list: model policy, not coding guidance;
  - a required logging template and a progress-bar threshold: no source.
- **Defects not to repeat:**
  - `[ValidateRange(1, 100)]` on a `[string]$ComputerName` parameter;
  - "piping an empty result to `ForEach-Object` runs the block": wrong;
  - "one object has a `$null` `.Count`": wrong since PowerShell 3.0;
  - "`+=` on arrays is slow" with no version: 7.5 made it faster;
  - no dated versions, no example ever run, and no guidance on `Invoke-Expression`, execution
    policy or plain-text passwords.
- **Company detail:** yes. One reference file named a third-party product, internal-style file
  share and server names, and an installer version. None of it came across.

## `bash-coding`

- **Covered:** strict mode, quoting, arrays, `[[ ]]`, arithmetic, `read -r`, `find -print0` with
  `xargs -0`, `mktemp` with traps, POSIX and macOS portability, ShellCheck and bats, `eval`,
  unsafe `rm`, and secrets in arguments.
- **Dropped:**
  - cookbooks for `grep`, `awk`, `jq`, `cut` and `sort`: reference material, not coding rules;
  - coverage tools and bats test design, for the planned testing skill;
  - GitHub Actions workflows, for git-workflows;
  - `sudo` and dropping privileges, for the planned operations skill;
  - a refusal table: general policy;
  - GNU against BSD tool tables, unsourced except `sed -i`, which was kept.
- **Defects not to repeat:**
  - `((count++))` under `set -e` in its main example, which stops the script when `count` is 0;
  - `readonly SCRIPT_DIR="$(...)"`, which hides the command's failure;
  - an unquoted `for file in $pattern`;
  - `find /logs ... -delete` with no dry run;
  - a comment after a line-continuation backslash, a syntax error;
  - `ls | xargs` and `find | xargs` without `-print0`, and `while read line` without `IFS=` or
    `-r`;
  - a `mysql` option that doesn't exist;
  - `curl --oauth2-bearer "$VAR"` described as hiding the token, though it's still on the
    command line;
  - a wrong fix for ShellCheck's SC2046;
  - an action pinned to `@master`;
  - a realistic-looking fake API key;
  - a table saying POSIX `sh` has no `$'...'`, which POSIX.1-2024 added.
- **Company detail:** none.

## What the research runs got wrong, found while writing

Each was checked at a primary source on 2026-10-26.

- **R09:** Ruff's own settings recommend `requires-python` over an explicit `target-version`.
  Ruff's default rules now include `UP`, most `B` rules and `I001`, so the run's "add them
  explicitly" overstates it; the `S` and `DTZ` rules are still off. ty is at 0.0.92, still beta.
- **R10:** Node 24 entered maintenance on 2026-10-20, and Node 26.0.0 shipped on 2026-05-05.
  typescript-eslint supports TypeScript only below 6.1, so it can't run on TypeScript 7 alone.
  Biome's `noFloatingPromises` is still in its experimental group.
- **R10, for HTML:** WCAG 2.2's current Recommendation is dated 2024-12-12. W3C's "Using ARIA"
  is a discontinued draft, so ARIA in HTML and the Authoring Practices Guide are cited instead.
  A `<button>` with no `type` is now in an "Auto" state.
- **R11:** System.CommandLine is at 2.0.14, not 2.0.3. .NET 10's end is 2028-11-14.
- **R15:** "dash 5.13" means dash 0.5.13, and Debian 13 ships 0.5.12, without `pipefail`.
