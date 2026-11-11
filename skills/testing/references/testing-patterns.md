# Testing patterns

Read this for choosing a language's test framework, coverage, property-based or mutation tool
at its current version; gating on coverage; mocking a library you don't own; contract tests
between services; and runner settings that let an empty run go green.

Proving a check can fail is `test-gates`; what output is checked against, `test-oracles`;
intermittent failures, `flaky-tests`; tests an AI agent writes, `agent-written-tests`. CI is
git-workflows' `ci-workflows` and `ci-speed`; GUI tests, user-experience's `gui-testing`. The
standard's dimension 5, *Testing and verification*, says when to add a coverage threshold and
mutation testing.

## Rules

1. **Read coverage as a map of code no test runs, never as proof it's tested.** It shows code
   ran, not that a test checked it (facts `tp-google`, `tp-google-mutation`). Measure branches
   (fact `tp-branch`); judge assertions by mutation testing.
2. **The team sets the target, and the gate falls on the change** (fact `tp-google`). Count
   integration and system tests' coverage too.
3. **A missing or failed coverage report fails the job,** never reading as 0% or a pass.
4. **Mock only types you own** (fact `tp-goos-own`). Wrap a third-party API in your own
   adapter, double that, and test it against the real thing: a throwaway container (fact
   `tp-testcontainers`) or a recorded response (`test-oracles`).
5. **A contract test gates a deploy between services.** With Pact: `can-i-deploy
   --to-environment` before, `record-deployment` once done, never tags (fact `tp-pact`).
6. **No tests, and an expected failure that passes, fail the run,** by the settings below.
7. **Property-based tests where an invariant is easy to state; mutation testing on the diff
   where tests are the gate** (fact `tg-mutation-diff`). Parsers and checkers come first, by
   this repository's own practice.
8. **Start from the table below, at its facts' versions,** pinned as the standard's *Language
   toolchains* says.

### Runner settings that fail open

| Runner | Passes over nothing when | Make it fail |
|---|---|---|
| pytest | A wrapper maps exit 5 (no tests) to success; an `xfail` test passes | Keep exit 5 a failure (fact `tp-pytest-empty`); `strict_xfail = true`, `xfail_strict` before 9 (fact `tp-pytest-xfail`) |
| Jest | `--passWithNoTests`, in config or on the command line | Remove it (fact `tp-jest-empty`) |
| bats | Before 1.14 a run with no tests passes; before 1.12, one `bats:focus` filtered to nothing | 1.14 or later, without `--allow-empty-suite` (fact `tp-bats-empty`) |
| Pester | Pester 5 skips an empty or `$null` `-ForEach` | Pester 6, which throws, with no `-AllowNullOrEmptyForEach` (fact `tp-pester-empty`) |

bats' `--abort`, which stops at the first failure, suits local runs, not CI's full record.

### Frameworks and tools per language

| Language | Tests: run with | Coverage | Property-based | Mutation | Facts |
|---|---|---|---|---|---|
| Python | pytest: `pytest` | coverage.py, `--branch` | Hypothesis | mutmut | `uxt-pytest`, `tp-py-tools` |
| JS, TS | Vitest: `npx vitest run`; Jest: `npx jest` | Vitest's `--coverage`; c8 | fast-check | StrykerJS | `tp-js-tools` |
| C#, .NET | xUnit v3, NUnit 5, MSTest 4: `dotnet test` | coverlet.collector | FsCheck | Stryker.NET | `tp-dotnet-tools` |
| Java, Kotlin | JUnit 6: `mvn test`, `gradle test` | JaCoCo | jqwik | PIT | `tp-jvm-tools` |
| Go | `go test ./...` | `go test -cover` | Fuzzing: `go test -fuzz` | — | `tp-go` |
| Rust | `cargo test`; `cargo nextest run` | cargo-llvm-cov | proptest | cargo-mutants | `tp-rust-tools` |
| PHP | PHPUnit 13, Pest 5 | PHPUnit's own | — | Infection | `tp-php-tools` |
| Ruby | RSpec, Minitest | SimpleCov | — | mutant | `tp-ruby-tools` |
| PowerShell | Pester 6: `Invoke-Pester` | Pester's own | — | — | `ps-tool-versions` |
| Bash | bats: `bats tests` | — | — | — | `sh-bats-version` |
| C | `meson test` | — | Fuzzing: libFuzzer | — | `cb-libfuzzer` |
| Browser | Playwright, Cypress 16, Selenium 4; axe-core | — | — | — | `uxt-playwright`, `tp-browser-tools` |

A dash is a tool not checked yet. Idioms such as fixtures, parameters and async tests are in
`coding`'s `python-coding`, `javascript-coding`, `csharp-coding`, `powershell-scripts`,
`bash-coding` and `c-build` modules.

### Strategy, still being checked

The test pyramid, the trophy and Google's test sizes disagree on the mix of tests. Their
sources, test-data patterns and metamorphic testing wait on research run R06c. Hardware
acceptance runs and fault injection are the planned `acceptance-runs` module.

## Mistakes

- **Tests added to reach a number,** copied or with no assertion (fact `tp-google`). Delete
  them; a mutation run shows where assertions are missing.
- **Mocking a library's own client,** such as an HTTP or cloud SDK class. The test passes while
  the library behaves otherwise. Mock your adapter.
- **`pytest || [ $? -eq 5 ]` or `--passWithNoTests` to turn a job with no tests green,** as AI
  assistants suggest. Give the job tests, or remove it.
- **`-AllowNullOrEmptyForEach` added to get a Pester 6 upgrade through.** Find why the data is
  empty. `Assert-MockCalled` is gone too (fact `tp-pester-empty`): use `Should -Invoke`.
- **Cypress written from memory of 15.x.** 16.0.0 removed `cy.exec()`, `cy.end()` and
  `Cypress.env()` (fact `tp-browser-tools`): use `cy.task()`, `cy.env()` or `Cypress.expose()`.

## Audit

Severity uses the standard's status words.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| A runner passes over no tests | `git grep -n -e passWithNoTests -e allow-empty-suite -e AllowNullOrEmptyForEach`; exit 5 mapped to 0 | `GAP`; `BLOCKER` where a merge rests on it | Rule 6's settings |
| `xfail` isn't strict | `xfail` markers, with no `strict_xfail`, `xfail_strict` or `strict` set | `GAP` | `strict_xfail = true` |
| Coverage counts lines only, or passes with no report | The coverage command; a run with the report deleted | `GAP` | Branch coverage; fail the step |
| Tests mock third-party types | Mock targets naming an outside package | `GAP` | An adapter you own |
| Contract checks use tags, or record no deployment | `can-i-deploy` calls; the deploy's last step | `DRIFT` | Rule 5 |
| A tool is behind its fact's version | Lockfiles and pins | `DRIFT` | Upgrade |

## Why

### Coverage

- **The advice:** branch coverage, read as a map; a per-change gate the team sets.
- **The reason:** Google found covered statements nothing asserted on, and coverage runs
  failing about one time in seven (fact `tp-google-mutation`). Line coverage counts an `if`
  covered when one way ran (fact `tp-branch`).
- **What others do, and why:** Google gives 60%, 75% and 90% as guidance, leaves the figure to
  each team, holds changed code higher, and warns a checkbox gate backfires (fact `tp-google`).
- **What it costs, and when to choose differently:** slower runs. Generated code leaves by a
  reviewed list, never by a lower figure.

### Doubles and contracts

- **The advice:** mock only your own types; test adapters against the real dependency.
- **The reason:** a mock of a library's type encodes a guess at its behavior, and the test
  agrees with the guess when the library doesn't. GOOS files the rule under third-party code
  (fact `tp-goos-own`).
- **What others do, and why:** Pact checks a provider against each consumer's recorded
  expectations, and its broker says if a version is safe to deploy (fact `tp-pact`).
- **What it costs, and when to choose differently:** an adapter, containers in CI, a broker.
  A library with no I/O is called directly.

### Runner settings

- **The advice:** no tests, and an unexpected pass, are failures.
- **The reason:** a run that collected nothing checked nothing, a couldn't-check that
  `test-gates` fails. A passing non-strict `xfail` hides an unrecorded fix (fact
  `tp-pytest-xfail`).
- **What others do, and why:** pytest, bats 1.14 and Pester 6 fail an empty run by default,
  and Pants keeps pytest's exit 5 a failure (facts `tp-pytest-empty`, `tp-bats-empty`,
  `tp-pester-empty`).
- **What it costs, and when to choose differently:** a matrix leg with no tests gets tests or
  goes. A monorepo task may allow empty runs where another check counts each package's tests.

## Facts

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `tp-google` | Google (2020): coverage shows code ran; unit coverage is one piece; 60/75/90% are guidelines, teams choose; 99% per commit; checkbox gates and copied tests backfire | [Google](https://testing.googleblog.com/2020/08/code-coverage-best-practices.html) | "it just guarantees that they have been executed by a test" and "Unit test code coverage is only a piece of the puzzle" and "encourage every team to select the value" and "per-commit coverage goals of 99% are reasonable" and "as it can backfire" and "copy/pasting tests just for the sake of increasing coverage" | 2026-11-11 | 2027-05-11 |
| `tp-google-mutation` | Covered statements go unasserted; about 15% of coverage calculations fail at Google | [Petrovic and Ivankovic, 2018](https://research.google.com/pubs/archive/46584.pdf) | "coverage alone might be misleading" and "About 15% of coverage statement calculations fail across Google." | 2026-11-11 | 2027-05-11 |
| `tp-branch` | Branch coverage tracks which way each branch went | [coverage.py](https://coverage.readthedocs.io/en/latest/branch.html) | "coverage.py tracks which of those destinations are actually visited" | 2026-11-11 | 2027-05-11 |
| `tp-goos-own` | GOOS, chapter 8, "Building on Third-Party Code" | [GOOS](https://growing-object-oriented-software.com/toc.html) | "Only Mock Types That You Own" | 2026-11-11 | 2027-05-11 |
| `tp-pact` | `can-i-deploy --to-environment`; `record-deployment` last; environments replace tags | [can-i-deploy](https://docs.pact.io/pact_broker/can_i_deploy); [deployments](https://docs.pact.io/pact_broker/recording_deployments_and_releases); [CLI](https://docs.pact.io/pact_broker/client_cli/readme) | "--to-environment ENVIRONMENT" and "at the very end of the deployment process" and "superseded by first class support" | 2026-11-11 | 2027-02-11 |
| `tp-testcontainers` | Testcontainers: 13 languages, among them Java, Go, .NET, Node.js, Python, Rust, Ruby, PHP | [Testcontainers](https://testcontainers.com/) | "Node.js" and "Haskell" | 2026-11-11 | 2027-02-11 |
| `tp-pytest-empty` | pytest exits 5 on no tests; Pants fails that by default | [pytest](https://docs.pytest.org/en/stable/reference/exit-codes.html); [Pants](https://www.pantsbuild.org/dev/reference/subsystems/pytest) | "No tests were collected" and "By default, Pants treats this as a test failure." | 2026-11-11 | 2027-02-11 |
| `tp-pytest-xfail` | `xfail` isn't strict by default; pytest 9 renamed `xfail_strict` to `strict_xfail` | [Skipping](https://docs.pytest.org/en/stable/how-to/skipping.html); [Reference](https://docs.pytest.org/en/stable/reference/reference.html) | "Both XFAIL and XPASS don't fail the test suite by default." and "Renamed from xfail_strict to strict_xfail." | 2026-11-11 | 2027-02-11 |
| `tp-jest-empty` | `--passWithNoTests` passes a run with no tests | [Jest CLI](https://jestjs.io/docs/cli) | "Allows the test suite to pass when no files are found." | 2026-11-11 | 2027-02-11 |
| `tp-bats-empty` | bats 1.14.0 fails a run with no tests; 1.13.0 added `--abort`; 1.12.0 fixed focus filtering all | [Changelog](https://raw.githubusercontent.com/bats-core/bats-core/master/docs/CHANGELOG.md) | "exit with error when no tests are found" and "to stop test suite execution on first failure" and "when all tests have been filtered out" | 2026-11-11 | 2027-02-11 |
| `tp-pester-empty` | Pester 6 throws on an empty `-ForEach`; `Assert-MockCalled` is removed | [v5 to v6](https://pester.dev/docs/migrations/v5-to-v6) | "instead of silently skipping the block or test" and "Both were deprecated back in v5 and are now fully removed." | 2026-11-11 | 2027-02-11 |
| `tp-py-tools` | Hypothesis 6.170.15, mutmut 3.8.1 | [hypothesis](https://pypi.org/pypi/hypothesis/json); [mutmut](https://pypi.org/pypi/mutmut/json) | "6.170.15" and "3.8.1" | 2026-11-11 | 2027-02-11 |
| `tp-js-tools` | Vitest 5.1.0, Jest 30.5.2, fast-check 4.10.2, StrykerJS 10.1.1 | [vitest](https://registry.npmjs.org/vitest); [jest](https://registry.npmjs.org/jest); [fast-check](https://registry.npmjs.org/fast-check); [stryker](https://registry.npmjs.org/@stryker-mutator/core) | "5.1.0" and "30.5.2" and "4.10.2" and "10.1.1" | 2026-11-11 | 2027-02-11 |
| `tp-dotnet-tools` | xunit.v3 4.0.3, NUnit 5.0.0, MSTest 4.5.2, FsCheck 3.6.0, Stryker.NET 5.1.0 | [xunit.v3](https://api.nuget.org/v3-flatcontainer/xunit.v3/index.json); [nunit](https://api.nuget.org/v3-flatcontainer/nunit/index.json); [mstest](https://api.nuget.org/v3-flatcontainer/mstest/index.json); [fscheck](https://api.nuget.org/v3-flatcontainer/fscheck/index.json); [stryker](https://api.nuget.org/v3-flatcontainer/dotnet-stryker/index.json) | "4.0.3" and "5.0.0" and "4.5.2" and "3.6.0" and "5.1.0" | 2026-11-11 | 2027-02-11 |
| `tp-jvm-tools` | JUnit 6.1.3, jqwik 1.10.2, PIT 1.30.2 | [junit](https://repo1.maven.org/maven2/org/junit/jupiter/junit-jupiter/maven-metadata.xml); [jqwik](https://repo1.maven.org/maven2/net/jqwik/jqwik/maven-metadata.xml); [pitest](https://repo1.maven.org/maven2/org/pitest/pitest/maven-metadata.xml) | "6.1.3" and "1.10.2" and "1.30.2" | 2026-11-11 | 2027-02-11 |
| `tp-go` | Go 1.27.4, 2026-11-10 | [Go releases](https://go.dev/doc/devel/release) | "go1.27.4 (released 2026-11-10)" | 2026-11-11 | 2027-02-11 |
| `tp-rust-tools` | cargo-nextest 0.9.151, proptest 1.12.0, cargo-mutants 27.1.0 | [nextest](https://crates.io/api/v1/crates/cargo-nextest); [proptest](https://crates.io/api/v1/crates/proptest); [mutants](https://crates.io/api/v1/crates/cargo-mutants) | "0.9.151" and "1.12.0" and "27.1.0" | 2026-11-11 | 2027-02-11 |
| `tp-php-tools` | PHPUnit 13.4.6, Pest 5.3.5, Infection 0.35.10 | [phpunit](https://repo.packagist.org/p2/phpunit/phpunit.json); [pest](https://repo.packagist.org/p2/pestphp/pest.json); [infection](https://repo.packagist.org/p2/infection/infection.json) | "13.4.6" and "5.3.5" and "0.35.10" | 2026-11-11 | 2027-02-11 |
| `tp-ruby-tools` | rspec-core 3.13.7, minitest 6.1.0, mutant 0.17.1 | [rspec-core](https://rubygems.org/api/v1/versions/rspec-core.json); [minitest](https://rubygems.org/api/v1/versions/minitest.json); [mutant](https://rubygems.org/api/v1/versions/mutant.json) | "3.13.7" and "6.1.0" and "0.17.1" | 2026-11-11 | 2027-02-11 |
| `tp-browser-tools` | Cypress 16.3.0, whose 16.0.0 removed `cy.exec()`, `cy.end()`, `Cypress.env()`; Selenium 4.52.0; axe-core, @axe-core/playwright 4.14.0 | [cypress](https://registry.npmjs.org/cypress); [changelog](https://docs.cypress.io/app/references/changelog); [selenium](https://pypi.org/pypi/selenium/json); [axe-core](https://registry.npmjs.org/axe-core); [@axe-core/playwright](https://registry.npmjs.org/@axe-core/playwright) | "16.3.0" and "Removed the cy.end() command" and "4.52.0" and "4.14.0" | 2026-11-11 | 2027-02-11 |

## Sources

| Source | Used for | License |
|---|---|---|
| [Google Testing Blog](https://testing.googleblog.com/2020/08/code-coverage-best-practices.html); [Petrovic and Ivankovic](https://research.google.com/pubs/archive/46584.pdf) | Coverage | None stated; authors' copyright: our own words, short quotes |
| [Growing Object-Oriented Software](https://growing-object-oriented-software.com/toc.html) | Mocking your own types | All rights reserved: the heading only |
| [Pact docs](https://docs.pact.io/) | Contract gates | None stated: our own words, short quotes |
| Docs of pytest, Pants, Jest, Cypress, coverage.py, Testcontainers, Pester; bats-core's changelog | Runner settings | Varied (bats-core, Pester's docs MIT): our own words, short quotes |
| Package registries, go.dev | Versions | Metadata: facts only |
