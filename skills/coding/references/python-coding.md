# Python coding

Read this for writing, reviewing or fixing Python 3 code: a project's `pyproject.toml`, uv, Ruff
and a type checker, type hints, idioms, running a subprocess, loading untrusted data, temporary
files and paths, time zones, and which Python versions to target.

It covers the code. Which Python releases are current, the lockfile and CI are the
project-bootstrap-and-audit standard's *Language toolchains*. Test design is the testing
skill's; here pytest is named only as the runner. Exceptions, retries and timeouts as a strategy
are `error-handling`. Which dependencies to trust, and how to pin them, are
`supply-chain-security`. Async and threads are `performance-and-concurrency`, injection beyond
the Python calls below is `secure-coding`, and time zone policy beyond Python's API is
`internationalization`. pandas and NumPy work belongs to a planned data skill, and Python 2 to
`legacy-languages`.

Contents: [Rules](#rules), [Mistakes](#mistakes), [Audit](#audit), [Why](#why),
[Facts](#facts), [Sources](#sources).

## Rules

1. **Set a project up with `pyproject.toml`, uv and the src layout,** and run every tool
   through `uv run`. A one-file script declares its dependencies inline instead.
2. **Lint and format with Ruff, and turn on its security and time zone rules** (`S`, `DTZ`),
   which its defaults leave out.
3. **Annotate new code, and check it with a type checker in strict mode.** Unannotated code is
   barely checked.
4. **Never hand untrusted input to a shell, `eval`, `pickle` or `yaml.load`.** Pass
   `subprocess` a list, and parse data with `json` or `yaml.safe_load`.
5. **Make temporary files with `tempfile`'s safe functions, and confine every path built from
   input** to its base directory, archives included.
6. **Use aware datetimes:** UTC inside the program, `zoneinfo` at its edges, never `utcnow()`.
7. **Name the encoding on every text file you open.**
8. **Declare the oldest Python you test in `requires-python`,** as `>=3.12`, with no upper
   bound. Which branches are still supported is the standard's *Language toolchains*: 3.10 has
   ended, and 3.11 ends in 2027-10 (facts `py-eol-310`, `py-eol-311`).

### The project and its tools

- **`pyproject.toml` holds the project:** its `[project]` table, `requires-python`, a `dev`
  dependency group for Ruff, pytest and the type checker, which stays out of the built package
  (fact `py-dep-groups`), and each tool's settings under `[tool.*]`.
- **The src layout** puts the package under `src/<name>/`, so tests import the installed copy,
  not the working tree (fact `py-src-layout`). `uv init` creates it, with a build system,
  since uv 0.12 (fact `py-uv-init`).
- **Run tools through uv:** `uv run ruff check`, `uv run mypy`, `uv run pytest`, in the
  project's environment at the versions its lockfile pins. `uv add --dev ruff` adds a tool to
  the group. Which tools, and pinning them, are the standard's *Language toolchains*.
- **A one-file script** carries a `# /// script` block with its `requires-python` and
  dependencies (fact `py-inline-script`), written by `uv add --script`, and runs with
  `uv run script.py`.

Ruff reads its target version from `requires-python` (fact `py-ruff-target`), as below.

```toml
[project]
name = "example-tool"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[project.scripts]
example-tool = "example_tool.cli:main"

[dependency-groups]
dev = ["mypy", "pytest", "ruff"]

[tool.ruff.lint]
extend-select = ["S", "DTZ"]

[tool.mypy]
strict = true
```

### Types

- **Annotate every new function's parameters and return.** mypy skips the body of a function
  with no annotations (fact `py-mypy-untyped`), so an unannotated module passes while checking
  nothing.
- **Strict mode** turns on mypy's optional checks: `strict = true` under `[tool.mypy]`. Pyrefly
  is stable too (fact `py-pyrefly-stable`). Astral's ty is still in beta (fact `py-ty-beta`),
  so it isn't a project's only gate.
- **Write current syntax:** `list[str]`, `X | None`, and the `type` statement for an alias from
  3.12 (fact `py-type-stmt`). Ruff's `UP` rules rewrite the old forms.
- **Check types where data comes in.** `json.loads` and `yaml.safe_load` return `Any`, which
  strict mode won't let you return as a `dict`. Check the shape, as `read_config` does below.

### Idioms

- **A mutable default is shared across calls** (fact `py-mutable-default`). Default to `None`
  and make a new list inside, as below. Ruff's `B006` catches it.
- **`assert` isn't validation.** `python -O` removes it (fact `py-assert-o`). Raise an
  exception for anything a caller can get wrong.
- **Pass `encoding="utf-8"` to every text `open()`,** `read_text()` and `write_text()`. 3.15
  made UTF-8 the default, and its notes still ask for an explicit encoding, because older
  Pythons use the locale's (fact `py-utf8-default`).
- **Use `pathlib` for paths,** `with` for anything that must be closed, and `secrets`, not
  `random`, for tokens and passwords (fact `py-secrets`).

```python
def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    tags = [] if tags is None else tags
    tags.append(tag)
    return tags
```

### Untrusted input

- **`subprocess` with a list, never `shell=True` on input.** With a shell, quoting is the
  caller's job (fact `py-subprocess-shell`). Put `--` before input that could start with `-`,
  where the program accepts it, and set a timeout. On Windows a `.bat` or `.cmd` file runs in
  a shell whatever you pass (fact `py-subprocess-shell`).
- **No `eval` or `exec` on input** (fact `py-eval`). `ast.literal_eval` runs no code, but its
  docs don't recommend it for untrusted data either (fact `py-literal-eval`). Use `json.loads`.
- **No `pickle` on data from outside** (fact `py-pickle`), and `yaml.safe_load`, never
  `yaml.load` (fact `py-yaml-load`).
- **Archives:** extract with `filter="data"`, which 3.14 made `tarfile`'s default and older
  versions need written out (fact `py-tar-filter`). `zipfile` warns that members can land
  outside the target (fact `py-zip-extract`).

```python
import subprocess
import tarfile
from pathlib import Path

import yaml


def search(pattern: str, root: Path) -> str:
    result = subprocess.run(
        ["grep", "-r", "-n", "--", pattern, str(root)],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if result.returncode > 1:  # grep exits 1 for no match, 2 for an error
        raise RuntimeError(result.stderr.strip())
    return result.stdout


def read_config(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise TypeError(f"{path}: expected a mapping at the top level")
    return data


def unpack(archive: Path, dest: Path) -> None:
    with tarfile.open(archive) as tar:
        tar.extractall(dest, filter="data")
```

### Temporary files and paths

- **`tempfile.TemporaryDirectory`, `NamedTemporaryFile` or `mkstemp`,** never `mktemp`, whose
  name another process can take first (fact `py-mktemp`), and never a fixed name under `/tmp`.
- **Confine a path built from input:** resolve it, then check it's inside the base.
  `is_relative_to` compares strings and doesn't treat `..` specially (fact
  `py-is-relative-to`), so it's safe only after `resolve()`.

```python
from pathlib import Path

UPLOADS = Path("/srv/uploads").resolve()


def upload_path(name: str) -> Path:
    target = (UPLOADS / name).resolve()
    if not target.is_relative_to(UPLOADS):
        raise ValueError(f"{name!r} is outside {UPLOADS}")
    return target
```

### Time zones

- **`datetime.now(UTC)`, never `utcnow()`,** which returns a naive value and is deprecated
  (fact `py-utcnow`). Store, compare and compute in UTC.
- **`ZoneInfo("America/New_York")` for a named zone,** at input and display. Declare the
  `tzdata` package where the system may have no time zone database, as on Windows (fact
  `py-tzdata`).
- **Naive and aware values don't mix:** subtracting or ordering them raises `TypeError` (fact
  `py-naive-aware`).
- **Adding a `timedelta` to a local time moves the wall clock,** not elapsed time (fact
  `py-wall-clock`). Across a daylight-saving change, "a day later" in New York is 25 hours on:

```python
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

NEW_YORK = ZoneInfo("America/New_York")

stamp = datetime(2026, 11, 1, 4, 30, tzinfo=UTC)
local = stamp.astimezone(NEW_YORK)
print(local)  # 2026-11-01 00:30:00-04:00

print(local + timedelta(days=1))  # 2026-11-02 00:30:00-05:00, 25 hours on
print((stamp + timedelta(days=1)).astimezone(NEW_YORK))  # 2026-11-01 23:30:00-05:00
```

## Mistakes

- **`subprocess.run(f"convert {name}", shell=True)`.** The input becomes shell syntax. Pass a
  list.
- **`yaml.load` or `pickle.loads` on an upload, a request or a cache others can write.** Both
  can run code. Use `yaml.safe_load`, and JSON instead of pickle.
- **`eval(text)` to parse a number or a list.** Use `int()`, `float()` or `json.loads`.
- **`datetime.utcnow()`, or `datetime.now()` with no zone,** compared with an aware value. It
  raises `TypeError`, or stores a local time with nothing to say so. Use `datetime.now(UTC)`.
- **"Same time tomorrow" as 24 hours in UTC, or "24 hours on" as a day in local time.** Wall
  clock goes in the local zone, elapsed time in UTC.
- **`open(path)` with no encoding,** which reads differently before 3.15 where the locale isn't
  UTF-8.
- **`def f(items=[])`,** which every call shares, and **`assert user.is_admin`,** which
  `python -O` removes.
- **`tempfile.mktemp()`, a fixed `/tmp/app.log`, or an unchecked `base / name`.**
- **Adding mypy to unannotated code and calling it typed,** or trusting Ruff's defaults to find
  security problems. Neither checks what you think.
- **`from typing import List, Optional`** in new code, or an upper bound such as `<3.15` in
  `requires-python`, which blocks every user of the next release.

## Audit

Severity uses the standard's status words. The `S` and `DTZ` codes are Ruff's, run as
`uv run ruff check --extend-select <codes> .`.

| Check | What to look for | Severity | Fix |
|---|---|---|---|
| Shell commands from input | `S602`, `S604`, `S605` (fact `py-ruff-security-off`) | `BLOCKER` where input reaches it, else `GAP` | A list of arguments, no shell (fact `py-subprocess-shell`) |
| Code run from data | `eval`, `exec`, `pickle`, `yaml.load`: `S301`, `S307`, `S506` | `BLOCKER` where input reaches it, else `GAP` | `json.loads`, `yaml.safe_load` (facts `py-pickle`, `py-yaml-load`) |
| Unsafe temporary files | `mktemp`, or a fixed path under `/tmp`: `S306`, `S108` | `GAP` | `tempfile.TemporaryDirectory` or `mkstemp` (fact `py-mktemp`) |
| Paths from input | A request's or an archive's name joined to a base with no check; `extractall` without `filter=` | `BLOCKER` where reachable, else `GAP` | Resolve, then `is_relative_to`; `filter="data"` (facts `py-is-relative-to`, `py-tar-filter`) |
| Naive datetimes | `DTZ` | `GAP` | `datetime.now(UTC)`, `zoneinfo` (facts `py-utcnow`, `py-naive-aware`) |
| Text opened with no encoding | `open(` and `read_text(` with no `encoding=` | `GAP` | `encoding="utf-8"` (fact `py-utf8-default`) |
| Ruff's security and time zone rules | `[tool.ruff.lint]` without `S` and `DTZ` | `GAP` | `extend-select = ["S", "DTZ"]` |
| No type checker, or not strict | No mypy or Pyrefly settings; mypy without `strict = true` | `GAP` | Strict mode, raised module by module |
| A type check that checks nothing | A type checker in CI over unannotated code | `DRIFT` | Annotate, or set `disallow_untyped_defs` (fact `py-mypy-untyped`) |
| `requires-python` | Missing, with an upper bound, or naming an ended branch | `GAP` | `>=` the oldest supported version you test (facts `py-requires-upper`, `py-eol-310`) |
| `assert` for checks | `assert` outside tests guarding input or permissions | `GAP` | Raise an exception (fact `py-assert-o`) |

## Why

### 1. `pyproject.toml`, uv and the src layout

- **The advice:** one `pyproject.toml`, uv to lock and run, the package under `src/`.
- **The reason:** with the package at the root, Python imports the working tree first, so
  tests pass against files the built package leaves out (fact `py-src-layout`). Running through
  uv means every command uses the locked environment, not whatever is installed.
- **What others do, and why:** Poetry, which the standard also supports, manages projects the
  same way, and pip-tools suits a team that wants pip alone. The flat layout runs from the
  source tree without an install.
- **What it costs:** an install before the code runs, which `uv run` does each time.
- **When to choose differently:** a one-file script needs only inline metadata (fact
  `py-inline-script`). Keep a working Poetry project on Poetry.

### 2. Ruff, with `S` and `DTZ`

- **The advice:** Ruff for lint and format, with the security and time zone rules selected.
- **The reason:** Ruff's default rules catch classic mistakes such as a mutable default (fact
  `py-ruff-defaults`), but its security rules are off by default (fact `py-ruff-security-off`),
  so `shell=True` passes, and so does `datetime.now()` with no zone, a `DTZ` rule.
- **What others do, and why:** flake8 with plugins, isort and Black, which Ruff's linter and
  formatter are built to replace; Bandit, from which the `S` rules derive.
- **What it costs:** `S603` and `S607` flag every `subprocess` call, the safe one above
  included. Review each, and suppress it with a comment saying what was checked.
- **When to choose differently:** a project on flake8 and Black can stay, and add Bandit.

### 3. Annotations and strict checking

- **The advice:** annotate new code, and run mypy or Pyrefly in strict mode.
- **The reason:** a checker sees only what's annotated (fact `py-mypy-untyped`), and strict
  mode is where it finds `Any` leaking from parsed data, `None` where a value is needed, and
  missing returns.
- **What others do, and why:** many projects type gradually, strict for new modules and lenient
  for old ones, as mypy's guide to existing code describes.
- **What it costs:** time, and on old code, hundreds of errors at once.
- **When to choose differently:** on a large untyped codebase, start with
  `disallow_untyped_defs` per module, and raise the rest module by module.

### 4 and 5. Untrusted input, temporary files and paths

- **The advice:** list arguments for `subprocess`, JSON or `safe_load` for data, no `eval`,
  `tempfile`'s safe functions, and a containment check on every path from input.
- **The reason:** each unsafe call runs or writes what the input says, and Python's own docs
  warn on every one (facts `py-subprocess-shell`, `py-eval`, `py-pickle`, `py-yaml-load`,
  `py-mktemp`).
- **What it costs:** pipes and globbing are written in Python instead, and the containment
  check also rejects a symlink in the base that points out, since `resolve()` follows it.
- **When to choose differently:** `pickle` between processes inside one trust boundary, such as
  a cache only the program writes, signed with `hmac` where it could be tampered with.

### 6. Aware datetimes, UTC inside

- **The advice:** UTC for every stored or compared time, a named zone for input and display.
- **The reason:** a naive value doesn't say which clock it's on, mixing the two raises
  `TypeError` (fact `py-naive-aware`), and local arithmetic moves the wall clock (fact
  `py-wall-clock`), so durations come out an hour off twice a year.
- **What it costs:** converting at the edges, and `tzdata` as a dependency on Windows.
- **When to choose differently:** a calendar's "every morning at nine" is a wall-clock rule:
  keep the local time and its zone, and compute each occurrence in that zone.

### 7. An explicit encoding

Before 3.15 the default is the locale's, so the same code reads a file differently on another
machine, and 3.15's notes still ask for it (fact `py-utf8-default`). It costs a keyword per call.

### 8. `requires-python`

- **The advice:** the oldest version you test, with `>=` and no upper bound.
- **The reason:** an upper bound blocks every user of the next release (fact
  `py-requires-upper`), and a floor below what you test promises what nobody checked.
- **When to choose differently:** an application deployed on one known interpreter pins it in
  `.python-version`, which `uv init` writes.

## Facts

Versions, dates and defaults, each named elsewhere in this module by its ID. Checked
2026-10-26.

| ID | Fact | Source | Quote | Checked | Check by |
|---|---|---|---|---|---|
| `py-eol-311` | Python 3.11 gets security fixes only, until 2027-10 | [Status of Python versions](https://devguide.python.org/versions/) | "3.11 PEP 664 security 2022-10-24 2027-10" | 2026-10-26 | 2027-04-26 |
| `py-eol-310` | Python 3.10 reached its end of life on 2026-10-01 | [Status of Python versions](https://devguide.python.org/versions/) | "3.10 PEP 619 end-of-life 2021-10-04 2026-10-01" | 2026-10-26 | 2027-04-26 |
| `py-uv-init` | `uv init` defines a build system and puts the code under `src/`, for applications since uv 0.12 | [Creating projects](https://docs.astral.sh/uv/concepts/projects/init/) | "In both cases, uv prefers to define a build system and place source files in a dedicated src/" and "Prior to v0.12, uv did not define a build system for applications by default." | 2026-10-26 | 2027-04-26 |
| `py-src-layout` | The src layout keeps the working tree off the import path, so the installed copy is tested | [src layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) | "The src layout helps prevent accidental usage of the in-development copy of the code." | 2026-10-26 | 2027-10-26 |
| `py-dep-groups` | Dependency groups in `pyproject.toml` stay out of the built package's metadata | [Dependency Groups](https://packaging.python.org/en/latest/specifications/dependency-groups/) | "such that they are not included in project metadata when it is built" | 2026-10-26 | 2027-10-26 |
| `py-inline-script` | A one-file script can declare its dependencies and Python version inline | [Inline script metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/) | "This specification defines a metadata format that can be embedded in single-file Python scripts" | 2026-10-26 | 2027-10-26 |
| `py-requires-upper` | The packaging guide warns against an upper bound in `requires-python` | [Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) | "Think twice before applying an upper bound" | 2026-10-26 | 2027-10-26 |
| `py-ruff-target` | Ruff reads the target version from `requires-python`, and recommends it over its own setting | [Ruff settings](https://docs.astral.sh/ruff/settings/) | "If you're already using a pyproject.toml file, we recommend project.requires-python instead" | 2026-10-26 | 2027-04-26 |
| `py-ruff-defaults` | Ruff's default rule set is its first five categories, which include the mutable default argument rule, `B006` | [The Ruff Linter](https://docs.astral.sh/ruff/linter/) | "The first five categories compose the default rule set" | 2026-10-26 | 2027-04-26 |
| `py-ruff-security-off` | Ruff's security rules are off by default | [The Ruff Linter](https://docs.astral.sh/ruff/linter/) | "while the remaining four (security, formatting, pedantic, and restriction) are off by default." | 2026-10-26 | 2027-04-26 |
| `py-mypy-untyped` | By default, mypy doesn't check the body of a function with no annotations | [mypy command line](https://mypy.readthedocs.io/en/stable/command_line.html) | "(By default the bodies of functions without annotations are not type checked.)" | 2026-10-26 | 2027-04-26 |
| `py-pyrefly-stable` | Pyrefly is marked production-stable on PyPI | [pyrefly on PyPI](https://pypi.org/pypi/pyrefly/json) | "Development Status :: 5 - Production/Stable" | 2026-10-26 | 2027-04-26 |
| `py-ty-beta` | ty is marked beta on PyPI | [ty on PyPI](https://pypi.org/pypi/ty/json) | "Development Status :: 4 - Beta" | 2026-10-26 | 2027-04-26 |
| `py-type-stmt` | The `type` statement for aliases arrived in Python 3.12 | [Simple statements](https://docs.python.org/3/reference/simple_stmts.html) | "type is a soft keyword." and "Added in version 3.12." | 2026-10-26 | 2027-10-26 |
| `py-mutable-default` | A default argument is evaluated once, when the function is defined | [More on defining functions](https://docs.python.org/3/tutorial/controlflow.html) | "Important warning: The default value is evaluated only once." | 2026-10-26 | 2027-10-26 |
| `py-assert-o` | `python -O` drops `assert` statements | [Simple statements](https://docs.python.org/3/reference/simple_stmts.html) | "The current code generator emits no code for an assert statement when optimization is requested at compile time." | 2026-10-26 | 2027-10-26 |
| `py-utf8-default` | Python 3.15 made UTF-8 the default encoding, and still asks for an explicit one | [What's New in Python 3.15](https://docs.python.org/3/whatsnew/3.15.html) | "Python now uses UTF-8 as the default encoding, independent of the system" and "For best compatibility between versions of Python, ensure that an explicit encoding argument is always provided." | 2026-10-26 | 2027-04-26 |
| `py-secrets` | `secrets`, not `random`, for security tokens | [secrets](https://docs.python.org/3/library/secrets.html) | "secrets should be used in preference to the default pseudo-random number generator in the random module" | 2026-10-26 | 2027-10-26 |
| `py-subprocess-shell` | With `shell=True`, quoting input is the caller's job, and on Windows a batch file runs in a shell regardless | [subprocess](https://docs.python.org/3/library/subprocess.html) | "If the shell is invoked explicitly, via shell=True, it is the application's responsibility to ensure that all whitespace and metacharacters are quoted appropriately to avoid shell injection vulnerabilities." and "may be launched by the operating system in a system shell regardless of the arguments passed to this library." | 2026-10-26 | 2027-10-26 |
| `py-eval` | `eval` runs arbitrary code | [Built-in functions](https://docs.python.org/3/library/functions.html) | "This function executes arbitrary code. Calling it with untrusted user-supplied input will lead to security vulnerabilities." | 2026-10-26 | 2027-10-26 |
| `py-literal-eval` | `ast.literal_eval` isn't recommended for untrusted data | [ast](https://docs.python.org/3/library/ast.html) | "Calling it on untrusted data is thus not recommended." | 2026-10-26 | 2027-10-26 |
| `py-pickle` | Unpickling can run code | [pickle](https://docs.python.org/3/library/pickle.html) | "The pickle module is not secure. Only unpickle data you trust." | 2026-10-26 | 2027-10-26 |
| `py-yaml-load` | PyYAML's `yaml.load` isn't safe on untrusted data | [PyYAML documentation](https://pyyaml.org/wiki/PyYAMLDocumentation) | "It is not safe to call yaml.load with any data received from an untrusted source!" | 2026-10-26 | 2027-10-26 |
| `py-mktemp` | `tempfile.mktemp` is deprecated and unsafe | [tempfile](https://docs.python.org/3/library/tempfile.html) | "Use of this function may introduce a security hole in your program." | 2026-10-26 | 2027-10-26 |
| `py-is-relative-to` | `PurePath.is_relative_to` compares strings, and doesn't resolve `..` | [pathlib](https://docs.python.org/3/library/pathlib.html) | "This method is string-based; it neither accesses the filesystem nor treats" ... "segments specially." | 2026-10-26 | 2027-10-26 |
| `py-tar-filter` | `tarfile` extraction defaults to the `data` filter from 3.14; earlier versions need it set | [tarfile](https://docs.python.org/3/library/tarfile.html) | "Changed in version 3.14: The filter parameter now defaults to 'data'." and "to support Python versions with a less secure default (3.13 and lower)" | 2026-10-26 | 2027-10-26 |
| `py-zip-extract` | `zipfile` extraction from an untrusted archive can write outside the target | [zipfile](https://docs.python.org/3/library/zipfile.html) | "It is possible that files are created outside of path" | 2026-10-26 | 2027-10-26 |
| `py-utcnow` | `datetime.utcnow()` returns a naive value, and is deprecated since 3.12; `datetime.UTC` arrived in 3.11 | [datetime](https://docs.python.org/3/library/datetime.html) | "Return the current UTC date and time, with tzinfo None." and "Deprecated since version 3.12: Use datetime.now() with UTC instead." and "Alias for the UTC time zone singleton datetime.timezone.utc." | 2026-10-26 | 2027-10-26 |
| `py-naive-aware` | Subtracting a naive datetime from an aware one raises `TypeError` | [datetime](https://docs.python.org/3/library/datetime.html) | "If one is aware and the other is naive, TypeError is raised." | 2026-10-26 | 2027-10-26 |
| `py-wall-clock` | Adding a `timedelta` to an aware datetime makes no time zone adjustment | [datetime](https://docs.python.org/3/library/datetime.html) | "no time zone adjustments are done even if the input is aware." | 2026-10-26 | 2027-10-26 |
| `py-tzdata` | `zoneinfo` may need the `tzdata` package, notably on Windows | [zoneinfo](https://docs.python.org/3/library/zoneinfo.html) | "it is recommended to declare a dependency on tzdata." | 2026-10-26 | 2027-10-26 |

## Sources

Every source, with its license and how this module uses it. The rules and examples are this
module's own words and code.

| Source | Used for | License |
|---|---|---|
| [Python documentation](https://docs.python.org/3/) (library, reference, tutorial, What's New) | Security warnings, `datetime` and `zoneinfo`, encodings, idioms | PSF License Version 2 for text: short quotes, with attribution |
| [Python Developer's Guide](https://devguide.python.org/versions/) | End-of-life dates | CC0 1.0: facts with short quotes |
| [Python Packaging User Guide](https://packaging.python.org/) | The src layout, dependency groups, inline script metadata, `requires-python` | CC BY-SA 3.0: short quotes with attribution, everything else in our own words |
| [uv documentation](https://docs.astral.sh/uv/) | `uv init`, the src layout and development dependencies | MIT or Apache-2.0: facts with short quotes |
| [Ruff documentation](https://docs.astral.sh/ruff/) | Default rules, the `S` and `DTZ` rules, the target version | MIT: facts with short quotes |
| [mypy documentation](https://mypy.readthedocs.io/en/stable/) | Strict mode, unannotated functions, adopting types gradually | MIT: facts with short quotes |
| [PyPI metadata](https://pypi.org/) for Pyrefly and ty | Each checker's release status | MIT (both projects): the classifiers, quoted |
| [PyYAML documentation](https://pyyaml.org/wiki/PyYAMLDocumentation) | `yaml.load` and `safe_load` | MIT (the project): one short quote |
