# Configuration

Read this for how a program takes its settings: the order of defaults, files, environment and
flags, naming environment variables, loading settings once into a typed object, checking them at
startup with errors that name the setting, getting secrets in, and feature flags.

The syntax and parsing of YAML, JSON, TOML and XML files is config-formats'. Checking text from
users and networks is input-handling's, and typed objects in general are types'. Language modules
name their own settings libraries and secret APIs. What may be committed is the
project-bootstrap-and-audit standard's dimension 7, and reading settings once in one module its
*Project shapes and layout*, under Wiring; this module covers both in code. A secret already
committed is git-workflows'.

## Rules

1. **Document one precedence, and apply it per setting:** defaults, then files, then the
   environment, then flags, each overriding the one before.
2. **Give each setting one name and one place it's read.** Load every source once, at startup,
   in one module, and pass the result down.
3. **Check every setting at startup, and fail with the setting's name,** its source and what's
   accepted, before any work starts. Report every error, not only the first.
4. **Parse into a typed object, not a map of strings.** Numbers, booleans, durations, enums,
   paths and URLs are converted at load time, and an unknown key is an error.
5. **Name environment variables in uppercase, with the program's prefix:** `MYAPP_DB_URL`.
6. **Secrets come from the environment or a secret store,** never the repository, a flag or a
   default, and never reach a log, an error message or a child process that doesn't need them.
7. **A required setting has no default.** A default is safe in every deployment, or there is none.
8. **A feature flag is a setting with an owner and a removal date.**

### Layers and precedence

- Merge key by key: a file that sets `port` overrides only `port`. Git reads its files in order
  and the last value wins (fact `config-git-order`); .NET's host and pydantic-settings each rank
  flags over the environment over files (facts `config-dotnet-order`, `config-pydantic-order`).
- A missing file at the default path is fine. A missing file at a path the user named is an
  error.
- Keep each value's source, so `--print-config` can say `port=8080 (MYAPP_PORT)`.
- A user's settings file goes in the platform's per-user folder: on Linux and the BSDs,
  `$XDG_CONFIG_HOME/myapp/` (fact `config-xdg`); elsewhere, the folder the platform's API gives.
- A `.env` file is for local development: ignored by git, beside a committed `.env.example`
  holding `CHANGEME`. The real environment wins over it (fact `js-env-file`).

### Checking at startup

Print every problem together and exit non-zero. Each names the setting and its source, with
the value only when it isn't secret:

```text
configuration:
  MYAPP_DB_URL (environment): required, not set
  MYAPP_PORT="80a" (environment): expected an integer from 1 to 65535
```

- The loader takes the environment as an argument, so a test passes a dictionary instead.
- Check settings that depend on each other: a certificate needs its key. A reload checks the new
  set whole, and keeps the old one if it fails.

### Environment variables

- POSIX's tools use uppercase names and leave lowercase ones to applications (fact
  `config-posix-names`). Uppercase with a prefix is the usual choice, and the prefix keeps clear
  of `PATH`, `HOME`, `DEBUG` and other programs' names. Nest with `__`: `MYAPP_DB__POOL_SIZE`.
- Every value is a string. Parse booleans against a documented set, and decide once whether an
  empty value means unset.
- Don't pass settings around by changing the environment at run time. Linux's `/proc` shows only
  the environment a program started with (fact `config-environ`), and every child inherits it.

### Secrets

Dimension 7 says what counts as a secret, and that secrets reach code through environment
variables, never a tracked file. In the code:

- Hold a secret in a type whose printed form is redacted, so a log of the settings doesn't
  carry it.
- Never take one as a flag: any user can read a process's command line (facts `sh-cmdline`,
  `csec-cmdline`). Take a variable, or a path to a file.
- Start a child process with an explicit, minimal environment when it needs none of the secrets
  (facts `config-systemd-env`, `config-owasp-env`).
- Fetch from a secret store at startup, and again when a credential expires. A store that can't
  be reached is an error, never a reason to fall back to a default.

### Feature flags

A flag is a setting like any other, with an owner and a removal date beside it in the code. A
release flag goes once the rollout ends, and tests cover both paths meanwhile (fact
`config-toggle-life`).

## Mistakes

- **`os.getenv("TIMEOUT", 30)` deep in the code.** It returns a string when set and an integer
  when not, and a misspelled name returns the default silently. Read it once, typed.
- **`bool(os.getenv("DEBUG"))`.** The string `"false"` is truthy in Python and JavaScript. Parse
  it against a set.
- **Checking a setting when it's first used.** A bad path fails hours after the deploy, mid-job.
- **Catching a parse error and using the default.** It ignores the operator's value. Fail.
- **Logging the environment or the settings object at startup.** Every secret goes with it.
- **One file per deployment, such as `config.prod.yaml` with production's hosts,** or
  `if env == "production"` in the code. Set each setting on its own, per deployment (fact
  `config-12factor`).
- **Two names for one setting,** such as `DB_URL` and `DATABASE_URL`.
- **What AI assistants get wrong:** reading a variable the project never sets, adding a settings
  library or `.env` loader the project already has, writing a default from memory, and putting a
  realistic-looking key in `.env.example` instead of `CHANGEME`.

## Audit

Severity uses the standard's status words, defined in this skill's `SKILL.md`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Settings read outside the settings module | `os.environ`, `getenv`, `process.env`, `Environment.GetEnvironmentVariable` or `$env:` elsewhere | `DRIFT` | Read it in the settings module, and pass it down |
| Bad settings get past startup, or the error names no setting | Start it with a required setting unset, and with a bad number | `GAP` | Check every setting at load; name each, its source and what's accepted |
| A secret in a tracked file or a default | Dimension 7's scan, and the defaults in the settings module | `BLOCKER` for a real secret | Dimension 7's remedy, then rotate it |
| A secret taken as a flag | `--password`, `--token` or `--key` in the argument parser | `GAP`; `BLOCKER` where a script or unit passes a real one | A variable or a file path |
| Settings or the environment logged | Log calls given the settings object or the environment | `BLOCKER` where a secret reaches the log | Redact secrets in the type's printed form |
| Flags past their removal date | Flags with no owner or date, or a date passed | `DRIFT` | Remove the flag and its dead path |

## Why

### One documented precedence

- **The advice:** defaults, files, environment, flags, merged key by key.
- **The reason:** a person changing a setting must know which source wins.
- **What others do:** git, .NET and pydantic-settings publish their orders, cited above;
  pydantic-settings puts values passed in code above the environment, which suits tests.
- **What it costs:** the merge code, and a record of each value's source.

### Read once, check at startup, typed

- **The advice:** one module loads every source, checks every value and hands a typed object to
  the rest of the program.
- **The reason:** a value checked at first use fails late, far from the change that broke it,
  and a string read in ten places is parsed ten ways. Code that reads its own environment can't
  be tested without setting it (the standard's Wiring).
- **What others do:** .NET checks options at first use unless told to at startup (fact
  `config-validate-on-start`).
- **When to choose differently:** a check that needs a service which may not be up yet belongs in
  a readiness probe, so the program can start and wait.

### Environment variables, and twelve-factor

- **The advice:** per-deployment values in the environment, under one prefix, each on its own.
- **The reason:** twelve-factor keeps settings apart from code, tests that by asking whether the
  code could be published without exposing a credential, and never groups variables into named
  deployments, which multiply (fact `config-12factor`).
- **What it costs:** flat strings, typed only by the parsing code.
- **When to choose differently:** structured settings that rarely change, such as a routing
  table, belong in a file, with the environment overriding single keys.

### Secrets in the environment, or in files

- **The advice:** the standard's: secrets reach code through environment variables, so filling
  them stays swappable without a change to the repository.
- **What it costs:** systemd and OWASP warn that children inherit the environment and that it
  reaches logs and dumps (facts `config-systemd-env`, `config-owasp-env`), though on Linux it's
  harder to read than a command line (facts `config-environ`, `csec-cmdline`). Hence the redacted
  type, the minimal child environment, and no flags.
- **When to choose differently:** where the platform hands secrets over as files, such as
  systemd's credentials, a variable naming the file keeps the environment as the interface. A
  repository the standard audits records that in its decision record, as dimension 7 differs.

### Feature flags with an end

- **The advice:** each flag has an owner and a removal date.
- **The reason:** flags are inventory with a carrying cost, release toggles should last a week
  or two, and some teams' tests fail once a flag outlives its date (fact `config-toggle-life`).
  Old flags pile up, and their combinations go untested.
- **When to choose differently:** an operations switch meant to stay, such as a kill switch, is a
  documented setting, not a flag.

## Facts

Practices and defaults, each named elsewhere by its ID.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `config-12factor` | Twelve-factor keeps settings apart from code, each variable set on its own | [III. Config](https://12factor.net/config) | "could be made open source at any moment, without compromising any credentials" and "They are never grouped together as" | 2026-11-11 | 2027-05-11 |
| `config-posix-names` | POSIX's utilities use uppercase names; lowercase ones are left to applications | [POSIX.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap08.html) | "do not begin with a digit" and "containing lowercase letters is reserved for applications" | 2026-11-11 | 2027-05-11 |
| `config-environ` | `/proc/<pid>/environ` is the starting environment, behind a ptrace check | [proc_pid_environ(5)](https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html) | "This file contains the initial environment" and "governed by a ptrace access mode" | 2026-11-11 | 2027-05-11 |
| `config-systemd-env` | systemd: environment variables don't suit secrets; use credentials | [systemd.exec(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html) | "environment variables are not suitable for passing secrets" and "propagated down the process tree" and "Use LoadCredential=" | 2026-11-11 | 2027-02-11 |
| `config-owasp-env` | OWASP: variables reach logs and dumps; for secrets, a last resort | [Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) | "may be included in logs or system dumps" and "not recommended unless the other methods are not possible" | 2026-11-11 | 2027-05-11 |
| `config-git-order` | Git reads its files in order, the last value winning | [git-config](https://git-scm.com/docs/git-config) | "with last value found taking precedence over values read earlier" | 2026-11-11 | 2027-02-11 |
| `config-dotnet-order` | .NET's host ranks flags, environment, `appsettings.{Environment}.json`, `appsettings.json` | [Configuration](https://learn.microsoft.com/en-us/dotnet/core/extensions/configuration) | "from highest to lowest priority" | 2026-11-11 | 2027-02-11 |
| `config-pydantic-order` | pydantic-settings ranks flags, code, environment, `.env`, secrets, defaults | [Settings Management](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) | "in descending order of priority" and "Arguments passed to the Settings class initialiser." | 2026-11-11 | 2027-02-11 |
| `config-validate-on-start` | .NET checks options at run time unless `ValidateOnStart` is called | [Options pattern](https://learn.microsoft.com/en-us/dotnet/core/extensions/options) | "you can configure it to occur at startup by instead chaining a call to ValidateOnStart" | 2026-11-11 | 2027-02-11 |
| `config-xdg` | A user's settings go under `$XDG_CONFIG_HOME`, else `$HOME/.config` | [XDG Base Directory](https://specifications.freedesktop.org/basedir-spec/latest/) | "a default equal to $HOME/.config should be used" | 2026-11-11 | 2027-05-11 |
| `config-toggle-life` | Release toggles last a week or two; flags carry a cost; some tests fail past a flag's date | [Feature Toggles](https://martinfowler.com/articles/feature-toggles.html) | "much longer than a week or two" and "inventory which comes with a carrying cost" and "if a feature flag is still around after its" | 2026-11-11 | 2027-05-11 |

## Sources

Rules are in our own words; each quote is a dated fact above.

| Source | Used for | License |
|---|---|---|
| [The Twelve-Factor App](https://12factor.net/config) | Settings apart from code | CC BY 4.0 (its repository): short quotes, attributed |
| [POSIX.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/) | Variable names | IEEE and The Open Group, all rights reserved: short quotes |
| [man7.org](https://man7.org/linux/man-pages/) (proc_pid_environ(5)) | `/proc` access | Each page's own license: short quotes |
| [systemd.exec(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html) | Secrets in the environment | LGPL-2.1-or-later: our own words, short quotes |
| [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) | Secrets in the environment | CC BY-SA 4.0: short quotes with attribution, our own words otherwise |
| [Git documentation](https://git-scm.com/docs/git-config) | Git's order | GPL-2.0: our own words, short quotes |
| [Microsoft Learn](https://learn.microsoft.com/dotnet/) (configuration, options) | .NET's order and startup checks | CC BY 4.0 text, MIT code: short quotes, attributed |
| [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) | Its order | MIT: short quotes |
| [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/latest/) | A user's settings folder | Not stated on the page: short quotes only |
| [Pete Hodgson, Feature Toggles](https://martinfowler.com/articles/feature-toggles.html) | Flag lifetimes | © Martin Fowler: quoted, never adapted |
